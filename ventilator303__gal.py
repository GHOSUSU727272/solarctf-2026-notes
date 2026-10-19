import numpy as np,wave
from pathlib import Path
root=Path('/home/anonim/ctf-workspace/live-20261017/ventilator303')
with wave.open(str(root/'ventilator303.wav')) as w: a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16)
print('SAMPLES',len(a),'minmax',a.min(),a.max(),flush=True)
for lvl in [0,512,1500,5000]:
    vals=(a < -lvl).astype('int8')
    cuts=np.flatnonzero(np.diff(vals)!=0)+1
    runs=np.diff(np.r_[0,cuts,len(vals)])
    old=np.r_[0,vals[cuts[:-1]]] if len(cuts)>0 else np.array([0])
    # calculate each segment before its transition, C++ cnt is segment length -1
    dat=0
    half=0
    sync=False
    arr=[]
    for length,cur in zip(runs[:-1],np.r_[0,vals[cuts[:-1]]]):
        if not cur:
            count=int(length)-1
            if count <100:
                if half: dat=(dat>>1)|128
                half^=1
            elif count<230: dat=dat>>1
            else:
                dat=(dat>>1)|(128 if half else 0)
                half=0
                if sync:arr.append(dat)
            if not sync and dat==0xa5:
                sync=True
                arr.append(dat)
    print('LEVEL',lvl,'TRANSITIONS',len(cuts),'SYNC',sync,'SIZE',len(arr),'BEGIN',bytes(arr[:80]),'FLAGS',bytes(arr).find(b'SOLARCTF'),flush=True)
    if sync:(root/f'gal_{lvl}.bin').write_bytes(bytes(arr))
