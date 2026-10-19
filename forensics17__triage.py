from pathlib import Path
import gzip,re,os,collections
p=Path('/home/anonim/ctf-workspace/live-20261017/forensics17/extracted')
print('webfiles',[(str(x.relative_to(p)),x.stat().st_size) for x in (p/'[root]'/'var'/'www').rglob('*') if x.is_file()][:50])
print('system files',[(str(x.relative_to(p)),x.stat().st_size) for x in (p/'system').rglob('*') if x.is_file()][:30])
print('found special files')
for x in p.rglob('*'):
 if not x.is_file():continue
 if re.search(r'webshell|malware|implant|backdoor|flag|payload|\.(php|phtml|sh)$',x.name,re.I):
  print(x.relative_to(p),x.stat().st_size)
count=0
for f in (p/'live_response'/'process'/'proc').glob('*/strings.txt.gz'):
 try: data=gzip.open(f,'rb').read()
 except:continue
 hits=[]
 for regex in [rb'SOLARCTF[^\s]{0,120}',rb'CTF\{[^\}]{1,110}\}',rb'(curl|wget|python|bash|nc |/tmp/|/dev/shm/|flag|passwd|base64|eval\(|system\().{0,150}']:
  for m in re.finditer(regex,data,re.I):
   found=m.group(0)[:160].decode('latin1','replace')
   if found not in hits:hits.append(found)
 if hits:
  print('PID',f.parts[-2],'HITS',hits[:14]);count+=1
print('Processes with hits:',count)
