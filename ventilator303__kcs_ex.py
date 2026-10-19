import numpy as np,wave
from scipy.signal import butter,sosfilt
from pathlib import Path
root=Path('/home/anonim/ctf-workspace/live-20261017/ventilator303')
with wave.open(str(root/'ventilator303.wav')) as w:
 sr=w.getframerate()
 samples=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype('float32')[18*sr:158*sr]
a=sosfilt(butter(3,[950,1450],btype='bandpass',fs=sr,output='sos'),samples)
b=sosfilt(butter(3,[2100,2700],btype='bandpass',fs=sr,output='sos'),samples)
cum1=np.r_[0,np.cumsum(a*a,dtype='float64')]
cum2=np.r_[0,np.cumsum(b*b,dtype='float64')]
for phase,inv,off,baud in [(49,0,8,300),(0,1,7,300),(36.75,0,8,300)]:
 step=sr/baud
 ctr=np.arange(phase+step/2,len(samples)-step/2,step)
 st=np.maximum(0,np.round(ctr-0.43*step).astype(int))
 en=np.minimum(len(samples),np.round(ctr+0.43*step).astype(int))
 bits=(((cum1[en]-cum1[st]) > (cum2[en]-cum2[st]))^inv).astype('uint8')
 n=(len(bits)-off)//10
 arr=bits[off:off+n*10].reshape((-1,10))
 valid=(arr[:,0]==0)&(arr[:,9]==1)
 data=np.sum(arr[:,1:9].astype('uint16')*(1<<np.arange(8,dtype='uint16')),axis=1).astype('uint8')
 print('PHASE',phase,'INV',inv,'VALID',valid.mean(),'PRINTABLE',((data>=32)&(data<127)).mean(),flush=True)
 for point in [0,500,1000,1500,2000,2500,3000,3500,4000]:
  print('AT',point,repr(bytes(data[point:point+60])),flush=True)
 (root/f'kcs_{int(phase)}_{inv}.bin').write_bytes(bytes(data))
