import numpy as np,wave
from collections import Counter
w=wave.open('/home/anonim/ctf-workspace/live-20261017/ventilator303/ventilator303.wav')
a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16)
sr=w.getframerate()
for t0,t1 in [(3,6),(18,25),(30,33),(60,63),(140,143),(160,163)]:
    seg=a[t0*sr:t1*sr]
    for thr in [0,2000,8000]:
        bits=(seg>thr).astype('int8')
        changes=np.flatnonzero(np.diff(bits)!=0)
        runs=np.diff(changes)
        c=Counter(int(x) for x in runs if x<220)
        print('T',t0,t1,'THR',thr,'MOST',c.most_common(14),flush=True)
