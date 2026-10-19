import numpy as np,wave
from pathlib import Path
from scipy.signal import butter,sosfilt
p=Path('/home/anonim/ctf-workspace/live-20261017/ventilator303/ventilator303.wav')
with wave.open(str(p)) as w:
 sr=w.getframerate()
 samples=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype('float32')
samples=samples[18*sr:158*sr]
a=sosfilt(butter(3,[950,1450],btype='bandpass',fs=sr,output='sos'),samples)
b=sosfilt(butter(3,[2100,2700],btype='bandpass',fs=sr,output='sos'),samples)
# downsample energies smoothed over window
sq1=a*a;sq2=b*b
cum1=np.r_[0,np.cumsum(sq1,dtype='float64')]
cum2=np.r_[0,np.cumsum(sq2,dtype='float64')]
for baud in [300,600,1200]:
 step=sr/baud
 best=[]
 for phase in np.arange(0,step,max(1,step/12)):
  ctr=np.arange(phase+step/2,len(samples)-step/2,step)
  start=np.maximum(0,np.round(ctr-0.43*step).astype(int))
  end=np.minimum(len(samples),np.round(ctr+0.43*step).astype(int))
  e1=(cum1[end]-cum1[start])/(end-start)
  e2=(cum2[end]-cum2[start])/(end-start)
  bits=(e1>e2).astype('uint8')
  for inv in (0,1):
   bit=bits^inv
   for off in range(10):
    n=(len(bit)-off)//10
    arr=bit[off:off+n*10].reshape((-1,10))
    valid=(arr[:,0]==0)&(arr[:,9]==1)
    data=np.sum(arr[:,1:9].astype('uint16')*(1<<np.arange(8,dtype='uint16')),axis=1).astype('uint8')
    asc=((data>=32)&(data<127))
    rating=float(np.mean(valid&asc)) +float(np.mean(valid))*0.2
    best.append((rating,phase,inv,off,int(np.sum(valid)),bytes(data[:160])))
 best.sort(reverse=True,key=lambda t:t[0])
 print('BAUD',baud,'BEST',flush=True)
 for rating,phase,inv,off,valid,preview in best[:4]:
  print(' score',round(rating,4),'phase',round(phase,2),'inv',inv,'off',off,'valid',valid,'preview',repr(preview[:105]),flush=True)
