import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import argparse
import glob

'''
python separate_in_speach.py --input_dir ＜path to input file＞

python separate_in_speach.py --input_dir ＜path to input dir＞ --outdir ＜path to out dir＞ --max 5000 --min 2000 --freq -40
'''

parser = argparse.ArgumentParser(description='description of your command')
parser.add_argument('--input_dir', type=str, required=True,
                    help='path to input dir')
parser.add_argument( '--out_dir', type=str, required=False,default='./Result_split_audio',
                    help='path to outdir')
parser.add_argument( '--max', type=int,required=False, default=5000,
                    help='max_chunk_len')
parser.add_argument( '--min', type=int,required=False, default=2000,
                    help='min_chunk_len')
parser.add_argument( '--freq', type=int,required=False, default=-40,
                    help='frequency')
parser.add_argument( '--keep_silence', type=int, required=False, default=500,
                    help='keep_silence')
parser.add_argument( '--margin', type=int,required=False, default=0,
                    help='Adjust the length of the margin when cutting the video')
parser.add_argument( '--padding', type=bool, required=False, default=True,
                    help='whether to pad the last chunk')

args = parser.parse_args()

def separate(input_file):
    if os.path.splitext(input_file)[1] == ".mp3":
        audio = AudioSegment.from_mp3(input_file)
    elif os.path.splitext(input_file)[1] == ".wav":
        audio = AudioSegment.from_wav(input_file)
    else:
        raise ValueError("Invalid file format. Only MP3 and WAV files are supported.")

    # 発話ごとに区切るための設定
    min_silence_len = 1000  # 無音が1秒以上続いたら区切る
    silence_thresh = args.freq  # 音量が-40dB以下を無音と判定

    # 無音の部分で区切る
    chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=args.keep_silence)

    min_chunk_len = args.min + args.keep_silence  # 2秒+keep_silence
    max_chunk_len = args.max  # 5秒

    output_chunks = []

    for chunk in chunks:
        print(len(chunk))
        if len(chunk) > 2000: #if len(chunk) > min_chunk_len:
            if len(chunk) > max_chunk_len:
                # sub_chunks = [chunk[i:i + max_chunk_len] for i in range(0, len(chunk), max_chunk_len)]
                sub_chunks = [chunk[i:i + max_chunk_len + args.margin] for i in range(0, len(chunk) - args.margin, max_chunk_len)]

                if len(sub_chunks[-1])<min_chunk_len:

                    if args.padding:  ##最後のチャンクはつなげて使用
                        output_chunks.extend(sub_chunks[0:-2])
                        output_chunks.append(sub_chunks[-2]+sub_chunks[-1])
                    else: ##最後のチャンクは捨てる
                        output_chunks.append(sub_chunks[0:-1])

                else :
                    output_chunks.extend(sub_chunks)
            else:
                output_chunks.append(chunk)
        else:
            pass
    
    return output_chunks



print("Running...")

last_output_chunks=[]

# mp3ファイルを読み込む
input_dir = glob.glob(args.input_dir+"/*")
output_dir = os.path.join(args.out_dir,os.path.basename(args.input_dir))


# 出力ディレクトリがなければ作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#dir 内のすべてを処理
for i in input_dir:
    print(i)
    last_output_chunks.extend(separate(i))

print("Saving in path : "+output_dir)

for i, chunk in enumerate(last_output_chunks):
    print("Saving "+os.path.basename(args.input_dir)+f"_chunk_{i}.wav")
    chunk.export(os.path.join(output_dir, (f"_chunk_{i}.wav")), format="wav")