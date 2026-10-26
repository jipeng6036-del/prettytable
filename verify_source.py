import hashlib,json,os,stat,sys
from pathlib import Path
manifest=json.loads(Path('/evidence/source-manifest.json').read_text())
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/work')
blob_key='baselineBlob' if len(sys.argv)>1 else 'candidateBlob'
checked=[]
for item in manifest['entries']:
    path=root/item['path']
    raw=os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    mode='120000' if path.is_symlink() else ('100755' if path.stat().st_mode & stat.S_IXUSR else '100644')
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert blob==item[blob_key],(item['path'],blob)
    assert mode==item['mode'],(item['path'],mode)
    checked.append({'path':item['path'],'blob':blob,'mode':mode})
print(json.dumps({'base':manifest['base'],'verified':len(checked),'files':checked},indent=2))
