from pathlib import Path
import sys,json
p=Path('/home/anonim/ctf-workspace/live-20261017/task-void')
sys.path.insert(0,str(p))
import diskforensics_mem as m
pg=json.loads((p/'void_text_cont/pages.json').read_text())
base=0x56328fac9000
chunks=[]
for va,pa,yes in pg:
 if base<=va<base+0x20000:
  data=m.phys(pa,4096)
  chunks.append((va-base,data,yes))
print('CHUNKS',[(hex(o),ok,x[:8].hex()) for o,x,ok in chunks])
end=max(o+len(b) for o,b,ok in chunks)
out=bytearray(end)
for off,b,ok in chunks:out[off:off+len(b)]=b
out_file=p/'void_text_cont/recovered_app.elf'
out_file.write_bytes(out)
print('OUTPUT',out_file,len(out),'MAGIC',out[:16].hex())
