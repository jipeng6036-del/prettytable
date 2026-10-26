import csv,hashlib,importlib.metadata,io,json,sys
from pathlib import Path
from prettytable import from_csv,from_html_one
import prettytable
lane=sys.argv[1]
manifest=json.loads(Path('/evidence/source-manifest.json').read_text())
package=Path(prettytable.__file__).parent
installed=[]
for item in manifest['entries']:
    if item['path'].startswith('src/prettytable/'):
        path=package/Path(item['path']).relative_to('src/prettytable')
        raw=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        assert blob==item['candidateBlob' if lane=='candidate' else 'baselineBlob'],(path,blob)
        installed.append({'file':str(path),'blob':blob})
out=Path('/evidence')/('file-'+lane+('-'+sys.argv[2] if len(sys.argv)>2 else ''))
out.mkdir(exist_ok=True)
html='<table><tr><th><b>Name</b></th><th>Role</th></tr><tr><td><a href="/alice">Alice</a> Example</td><td><em>Engineer</em></td></tr></table>'
(out/'input.html').write_text(html,encoding='utf8')
table=from_html_one((out/'input.html').read_text(encoding='utf8'))
(out/'output.txt').write_text(table.get_string(),encoding='utf8')
with (out/'output.csv').open('w',encoding='utf8',newline='') as file:
    file.write(table.get_csv_string())
with (out/'output.csv').open(encoding='utf8',newline='') as file:
    decoded=list(csv.reader(file))
with (out/'output.csv').open(encoding='utf8',newline='') as file:
    restored=from_csv(file)
expected=[['Name','Role'],['Alice Example','Engineer']]
result={'lane':lane,'python':sys.version,'module':prettytable.__file__,'version':importlib.metadata.version('prettytable'),'installedSourceBlobs':installed,'fieldNames':table.field_names,'rows':table.rows,'csvReadFromDisk':decoded,'restoredFields':restored.field_names,'restoredRows':restored.rows,'textReadFromDisk':(out/'output.txt').read_text(encoding='utf8'),'correct':decoded==expected,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='result.json'}}
assert decoded==[table.field_names,*table.rows]
assert [restored.field_names,*restored.rows]==decoded
assert ('Alice Example' in result['textReadFromDisk'])==result['correct']
assert result['correct']==(lane=='candidate')
(out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
