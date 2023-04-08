# Separate mp3 or wav Voice Data wav for RVC train
### ja  

RVC のデータセット作成のためのコードです。
mp3 もしくは wav ファイルを入力とし、処理されたwav ファイルを返します。  

・音声ファイルを等間隔で分割するコードaudio_to_copas.py と  
・発話ごとに音声を分割し、適切な長さに区切るaudio_to_copas.py があります。  

### en  
Code for RVC dataset creation.
Takes an mp3 or wav file as input and returns a processed wav file.  

・Code audio_to_copas.py that divides the audio file at equal intervals and  
・There is audio_to_copas.py that divides the audio for each utterance and divides it into appropriate length  

## Install

python version is 3.10

### clone  
Use command to clone or download file 
```
git clone https://github.com/teftef6220/Voice_Separation_and_Selection.git
```

Because RVC becomes noise for learning even in silent parts and BGM

For RVC voice selection
・Convert mp3 data to wav data separated by n seconds and save
- You can change the number of seconds to cut
・If there is more than half of the monotonous sound such as silence or BGM, remove it from the data set

### Create venv 

```
python -m venv venv
```
### activate venv

```
venv\Scripts\activate
```

### install requirements
```
pip install -r requirements.txt
```

# Run audio_to_copas.py 
### ja  
このコードは音声を指定した長さに分割します。

### en  
Enter the folder location, command and run.

```
python audio_to_copas.py --input ＜path to mp3 file＞ --outdir ＜path to out dir＞
```

You can also specify the duration of the wav file to be cut, the frequency (dB) to be considered quiet, and the percentage of quiet.

--time : Output wav file time (unit: second)

--freq : Volume threshold for judging silence (unit: dB)

--rate : Select and delete wav files containing silent sounds at a rate equal to the rate rate or above.(unit: %)

```
python audio_to_copas.py --input ＜path to mp3 file＞ --outdir ＜path to out dir＞ --time 4 --freq -40 --rate 50
```

# Run audio_to_copas.py 

### ja  
このコードは音声発話ごとに分けて分割します。このコードでは分割する音声の長さをミリ秒で指定できます。
--max に最大、--min に最小を指定することで発話を始点として min ~ max までの間に分けてくれます。

・ただ長すぎる場合は--max ミリ秒ごとに分割します。また端数は --min ミリ秒より短い場合は切り捨てられます。
・例えば16秒の音声に分割された場合、 5+5+5+1と分割され、最後の1　秒は保存されず、スルーされます。

### en  
Splits mp3 or wav files into utterances.
 
・If the speech file is too long, divide it into n parts (for example, if it is 16 seconds, divide it into 5+5+5+1 and don't save the last short part)
・Do not save if the speech file is too short
```
python separate_in_speach.py --input ＜path to input file＞
```

You can also change the length of the cut audio. The maximum length can be specified with --max and the minimum with --min. The unit is milliseconds. You can also set the gain with --freq

--max : Maximum length of clipped audio (unit: milliseconds)

--min : Minimum clipped audio (unit: milliseconds)

--freq : Volume threshold for judging silence (unit: dB)
```
python separate_in_speach.py --input ＜path to input file＞ --outdir ＜path to out dir＞ --max 5000 --min 2000 --freq -40
```
