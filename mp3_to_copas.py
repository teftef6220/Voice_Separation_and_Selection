import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import librosa
import numpy as np

# 入力MP3ファイルのパスを設定
input_mp3_file = "to input mp3 file"

# 出力WAVファイルを保存するディレクトリを設定
output_directory = "to out dir"

# 出力ディレクトリが存在しない場合、作成する
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# MP3ファイルを読み込む
audio = AudioSegment.from_mp3(input_mp3_file)

# 6秒ごとに区切る
chunk_length = 4 * 1000  # ミリ秒単位
chunks = make_chunks(audio, chunk_length)

# 各チャンクをWAVファイルとして保存する
for i, chunk in enumerate(chunks):
    output_wav_file = os.path.join(output_directory, f"chunk_{i}.wav")
    chunk.export(output_wav_file, format="wav")
    print(f"Saved {output_wav_file}")

##以下は静音が半分以上を占めるWAVファイルを特定

# 静音と判断する音量しきい値（dB）を設定
silence_threshold = -40  # -40 dBを例としていますが、適宜調整してください

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
        amplitude = librosa.amplitude_to_db(librosa.stft(audio_data, n_fft=frame_length, hop_length=hop_length), ref=np.max)
        
        # 静音フレームの数をカウント
        silence_frames = sum([1 for frame in amplitude if np.all(frame < silence_threshold)])
        total_frames = len(amplitude)
        
        # 静音が半分以上を占めているかどうかをチェック
        if silence_frames / total_frames > 0.5:
            files_with_majority_silence.append(input_wav_file)
            os.remove(input_wav_file)##消す

# 結果を表示
print("Files with majority silence, and Delete below:")
for file_name in files_with_majority_silence:
    print(f"- {file_name}")
