import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import argparse

'''
python separate_in_speach.py --input ＜path to input file＞

python separate_in_speach.py --input ＜path to input file＞ --outdir ＜path to out dir＞ --max 5000 --min 2000 --freq -40
'''

parser = argparse.ArgumentParser(description='description of your command')
parser.add_argument('--input', type=str, required=True,
                    help='path to input file')
parser.add_argument( '--outdir', type=str, required=False,default='./Result_split_audio',
                    help='path to outdir')
parser.add_argument( '--max', type=int,required=False, default=5000,
                    help='max_chunk_len')
parser.add_argument( '--min', type=int,required=False, default=2000,
                    help='min_chunk_len')
parser.add_argument( '--freq', type=int,required=False, default=-40,
                    help='frequency')
args = parser.parse_args()

print("Running...")

# mp3ファイルを読み込む
input_file = args.input
output_dir = args.outdir

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
chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

# 出力ディレクトリがなければ作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

min_chunk_len = args.min  # 2秒
max_chunk_len = args.max  # 5秒

output_chunks = []

for chunk in chunks:
    print(len(chunk))
    if len(chunk) > min_chunk_len:
        if len(chunk) > max_chunk_len:
            sub_chunks = [chunk[i:i + max_chunk_len] for i in range(0, len(chunk), max_chunk_len)]
            if len(sub_chunks[-1])<min_chunk_len:
                output_chunks.extend(sub_chunks[0:-1])
            else :
                output_chunks.extend(sub_chunks)
            
        else:
            output_chunks.append(chunk)
    else:
        pass

for i, chunk in enumerate(output_chunks):
    print("Saving "+os.path.splitext(os.path.basename(input_file))[0]+f"_chunk_{i}.wav")
    chunk.export(os.path.join(output_dir, (os.path.splitext(os.path.basename(input_file))[0]+f"_chunk_{i}.wav")), format="wav")