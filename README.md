# Separate mp3 or wav Voice Data for RVC train


音声を利用するときは、法律に即した利用をしてください。  
When using voice, please use it according to the law.  

https://ja.wikibooks.org/wiki/%E8%91%97%E4%BD%9C%E6%A8%A9%E6%B3%95%E7%AC%AC30%E6%9D%A1


https://github.com/ddPn08/rvc-webui
こちらでも使えます．

### ja  

RVC のデータセット作成のためのコードです。
mp3 もしくは wav ファイルを含むディレクトリを入力とし、処理されたwav ファイルを返します。  
結果は--out_dir で指定したディレクトリの下に入力時のディレクトリ名を作成し、その中に保存されます。

- 音声ファイルを等間隔で分割するコードaudio_to_copas.py と  
- 発話ごとに音声を分割し、適切な長さに区切るseparate_in_speach.py があります。  

### en  
Code for RVC dataset creation.
Takes a directory containing mp3 or wav files as input and returns the processed wav file.  
The result will be saved in the input directory name created under the directory specified by --out_dir.

- Code audio_to_copas.py that divides the audio file at equal intervals and  
- There is audio_to_copas.py that divides the audio for each utterance and divides it into appropriate length  

## Install

python version is 3.10

### clone  
Use command to clone or download file 
```
git clone https://github.com/teftef6220/Voice_Separation_and_Selection.git
```

Because RVC becomes noise for learning even in silent parts and BGM

For RVC voice selection
- Convert mp3 data to wav data separated by n seconds and save
- You can change the number of seconds to cut
- If there is more than half of the monotonous sound such as silence or BGM, remove it from the data set

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

# Run separate_in_speach.py 

### ja  
このコードは音声発話ごとに分けて分割します。このコードでは分割する音声の長さをミリ秒で指定できます。
--max に最大、--min に最小を指定することで発話を始点として min ~ max までの間に分けてくれます。

- ただ長すぎる場合は--max ミリ秒ごとに分割します。また端数は --min ミリ秒より短い場合は切り捨てられます。
- 例えば16秒の音声を発話を起点に5秒に分割する場合 5+5+5+1と分割され、paddingを True の時、最後の1秒を一つ前のチャンクにつけて 5+5+6 秒にすることができます。
- また、paddingを False の時、最後の 1 秒は保存されずスルーされます。つまり 5+5+5 秒にすることができます。

### en  
Splits mp3 or wav files into utterances.
 
- If the speech file is too long, divide it into n parts (for example, if it is 16 seconds, divide it into 5+5+5+1 and don't save the last short part)
- If the speech file is too short not save 
```
python separate_in_speach.py --input_dir ＜path to input file＞
```

You can also change the length of the cut audio. The maximum length can be specified with --max and the minimum with --min. The unit is milliseconds. You can also set the gain with --freq

--input_dir : path to input dir

--out_dir : path to out dir

--max : Maximum length of clipped audio (unit: milliseconds)

--min : Minimum clipped audio (unit: milliseconds)

--freq : Volume threshold for judging silence (unit: dB)  

--keep_silence : A measure of how long to keep silence. Leave some space at the end of the cut audio. (Unit: ms)  

--margin : Margin when cutting audio and audio. Basically 0 is fine. (Unit: ms)  

--padding : Whether to add padding to the last chunk when cutting an audio file.  
```
python separate_in_speach.py --input_dir ＜path to input file＞ --outdir ＜path to out dir＞ --max 5000 --min 2000 --freq -40 --keep_silence 500 --margin 0 --padding True
```
