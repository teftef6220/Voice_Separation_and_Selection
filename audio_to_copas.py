import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import librosa
import numpy as np
import argparse
'''
python audio_to_copas.py --input ＜path to mp3 file＞ --outdir ＜path to out dir＞

python audio_to_copas.py --input ＜path to mp3 file＞ --outdir ＜path to out dir＞ --time 4 --freq -40 --rate 50
'''

parser = argparse.ArgumentParser(description='description of your command')
parser.add_argument('--input', type=str, required=True,
                    help='path to input file')
parser.add_argument( '--outdir', type=str, required=True,default='./Result',
                    help='path to outdir')
parser.add_argument( '--time', type=int,required=False, default=4,
                    help='Length of time to separate videos')
parser.add_argument( '--freq', type=int,required=False, default=-40,
                    help='frequency')
parser.add_argument( '--rate', type=int,required=False, default=50,
                    help='Percentage of silence')
args = parser.parse_args()

print("Running...")

# 入力MP3ファイルのパスを設定
input_file = args.input

# 出力WAVファイルを保存するディレクトリを設定
output_directory = args.outdir

# 出力ディレクトリが存在しない場合、作成する
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# MP3ファイルを読み込む
if os.path.splitext(input_file)[1] == ".mp3":
    audio = AudioSegment.from_mp3(input_file)
elif os.path.splitext(input_file)[1] == ".wav":
    audio = AudioSegment.from_wav(input_file)
else:
    raise ValueError("Invalid file format. Only MP3 and WAV files are supported.")


# 6秒ごとに区切る
chunk_length = int(args.time) * 1000  # ミリ秒単位
chunks = make_chunks(audio, chunk_length)

# 各チャンクをWAVファイルとして保存する
for i, chunk in enumerate(chunks):
    output_wav_file = os.path.join(output_directory, f"chunk_{i}.wav")
    chunk.export(output_wav_file, format="wav")
    print(f"Saved {output_wav_file}")

##以下は静音が半分以上を占めるWAVファイルを特定

# 静音と判断する音量しきい値（dB）を設定
silence_threshold = int(args.freq)  # -40 dBを例としていますが、適宜調整してください

# 静音が半分以上を占めるファイルを格納するリスト
files_with_majority_silence = []


# 入力ディレクトリ内のWAVファイルを処理
for file_name in os.listdir(output_directory):
    if file_name.endswith(".wav"):
        input_wav_file = os.path.join(output_directory, file_name)
        
        # 音声ファイルを読み込む
        audio_data, sample_rate = librosa.load(input_wav_file, sr=None)
        
        # 音声データを分割し、各フレームの音量（dB）を計算
        frame_length = 1024
        hop_length = 512
        amplitude = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data, n_fft=frame_length, hop_length=hop_length)), ref=np.max)
        
        # 静音フレームの数をカウント
        silence_frames = sum([1 for frame in amplitude if np.all(frame < silence_threshold)])
        total_frames = len(amplitude)
        
        # 静音が半分以上を占めているかどうかをチェック
        if silence_frames / total_frames > float(args.rate/100):
            files_with_majority_silence.append(input_wav_file)
            os.remove(input_wav_file)##消す

# 結果を表示
print("Files with majority silence, and Delete below:")
for file_name in files_with_majority_silence:
    print(f"- {file_name}")