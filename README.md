# Separate mp3 or wav Voice Data wav for RVC train

## Innstall

### clone  
Use command to clone or download file 
```
git clone https://github.com/teftef6220/Voice_Separation_and_Selection.git
```

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

### run
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
