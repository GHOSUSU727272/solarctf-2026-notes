from pathlib import Path
import mmap,struct
p=Path(__file__).parent
fh=(p/'extracted/memory.elf').open('rb');mem=mmap.mmap(fh.fileno(),0,access=mmap.ACCESS_READ)
phoff=struct.unpack_from('<Q',mem,32)[0];n=struct.unpack_from('<H',mem,56)[0]
segs=[struct.unpack_from('<IIQQQQQQ',mem,phoff+56*i) for i in range(n)];segs=[x for x in segs if x[0]==1]
def poff(pa):
 for seg in segs:
  if seg[4]<=pa<seg[4]+seg[5]:return seg[2]+pa-seg[4]
 raise ValueError(hex(pa))
def phys(pa,n):return mem[poff(pa):poff(pa)+n]
def u64(pa):return int.from_bytes(phys(pa,8),'little')
def translate(va,dtb=0xb9c2000):
 table=dtb&~0xfff
 for shift in [39,30,21,12]:
  entry=u64(table+((va>>shift)&511)*8)
  if not entry&1:raise ValueError(('unmapped',hex(va),shift,hex(entry)))
  if shift in [30,21] and entry&128:return (entry&0x000ffffffffff000)&~((1<<shift)-1)|(va&((1<<shift)-1))
  table=entry&0x000ffffffffff000
 return table|(va&0xfff)
def virt(va,n):
 out=b''
 while n:
  take=min(n,4096-(va&4095));out+=phys(translate(va),take);va+=take;n-=take
 return out
