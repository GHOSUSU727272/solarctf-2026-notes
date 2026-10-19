import zlib,tarfile
from pathlib import Path
base=Path('/home/anonim/ctf-workspace/live-20261017/neuropet')
raw=(base/'neuropet.ab').read_bytes()
assert raw.startswith(b'ANDROID BACKUP')
plain=zlib.decompress(raw[24:])
(base/'backup.tar').write_bytes(plain)
with tarfile.open(base/'backup.tar') as tar:
    members=tar.getmembers()
    print('SIZE',len(plain),'MEMBERS',len(members))
    for member in members[:150]:print(member.name,member.size)
