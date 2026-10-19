from pathlib import Path
import struct
P=Path(__file__).parent
def run(name,param=0):
 b=(P/(name+'.dec')).read_bytes();s=[param];pc=0;out={};trace=[]
 for step in range(100000):
  at=pc;op=b[pc];pc+=1
  trace.append((at,hex(op),s[-5:]))
  if op==0x0d:break
  elif op==0x14:s.append(struct.unpack_from('<I',b,pc)[0]);pc+=4
  elif op==0x1b:s.pop()
  elif op==0x22:s.append(s[-1])
  elif op in (0x29,0x30,0x37,0x3e,0x45,0x4c,0x61):
   x=s.pop();y=s.pop()
   val={0x29:lambda:y+x,0x30:lambda:x-y,0x37:lambda:y*x,0x3e:lambda:y^x,0x45:lambda:x<<(y&31),0x4c:lambda:x>>(y&31),0x61:lambda:int(x==y)}[op]()
   s.append(val&0xffffffff)
  elif op==0x53:
   k=b[pc]&7;pc+=1;x=s.pop();s.append(((x<<k)&255)|((x&255)>>(8-k)))
  elif op==0x5a:s[-1]=(s[-1]*0x41c64e6d+0x3039)&0xffffffff
  elif op==0x68:
   dst=struct.unpack_from('<I',b,pc)[0];pc+=4
   if s.pop()==0:pc=dst
  elif op==0x6f:pc=struct.unpack_from('<I',b,pc)[0]
  elif op==0x7d:
   sid=b[pc];n=struct.unpack_from('<H',b,pc+1)[0];pc+=3
   data=bytes((v&255) for v in s[-n:]) if n else b''
   if n:del s[-n:]
   out[sid]=data
   print('EMIT',sid,n,repr(data),data.hex())
  elif op==0x84:pass
  else:raise ValueError((at,hex(op)))
 else:raise RuntimeError('step limit')
 (P/(name+'_vm_trace.txt')).write_text('\n'.join(map(str,trace)))
 for i,v in out.items():(P/(name+'_segment_'+str(i)+'.bin')).write_bytes(v)
 print('HALT',name,'steps',step,'stack',s)
 return out
if __name__=='__main__':
 run('mood');run('devroom')
