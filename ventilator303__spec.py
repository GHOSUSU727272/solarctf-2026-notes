import wave, numpy as np
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
base=Path('/home/anonim/ctf-workspace/live-20261017/ventilator303')
with wave.open(str(base/'ventilator303.wav')) as w:
    sr=w.getframerate()
    audio=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype('float32')/32768
print('SAMPLE_RATE',sr,'DURATION',len(audio)/sr,'PEAK',float(abs(audio).max()),flush=True)
freq,t,S=signal.spectrogram(audio,fs=sr,nperseg=2048,noverlap=1024)
power=10*np.log10(S+1e-12)
fig,ax=plt.subplots(figsize=(20,7))
ax.pcolormesh(t,freq,power,shading='auto',cmap='inferno',vmin=-95,vmax=-26)
ax.set_ylim(0,5500)
ax.set_xlabel('Seconds');ax.set_ylabel('Frequency (Hz)')
fig.savefig(base/'spectrogram.png',dpi=110)
print('SAVED',base/'spectrogram.png',flush=True)
