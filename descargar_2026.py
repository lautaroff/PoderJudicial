"""Copia verificable de la publicación oficial; no altera los originales."""
from pathlib import Path
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import json, hashlib, re, datetime
import requests, fitz
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent
DEST=ROOT/'biblioteca'/'2026'/'programa'
DEST.mkdir(parents=True,exist_ok=True)
PAGE='https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026-material-de-estudio/'
html=requests.get(PAGE,timeout=90); html.raise_for_status()
(DEST/'pagina-material-oficial.html').write_text(html.text,encoding='utf-8')
soup=BeautifulSoup(html.text,'html.parser')
urls=sorted({urljoin(PAGE,str(v)) for tag in soup.find_all(True) for k,v in tag.attrs.items() if isinstance(v,str) and '.pdf' in v.lower()})
urls=[u for u in urls if '/2026/10/' in u and 'Concurso-Ingreso-2026-SCJM-' in u]
def download(url):
    r=requests.get(url,timeout=120); r.raise_for_status()
    if not r.content.startswith(b'%PDF'): raise ValueError(url)
    path=DEST/Path(urlparse(url).path).name
    path.write_bytes(r.content)
    doc=fitz.open(path)
    txt=path.with_suffix('.txt')
    txt.write_text('\n\n'.join(f'=== PÁGINA PDF {i+1} ===\n'+p.get_text(sort=True) for i,p in enumerate(doc)),encoding='utf-8')
    links=[]
    for i,p in enumerate(doc):
        for link in p.get_links():
            if link.get('uri'): links.append({'pagina_pdf':i+1,'url':link['uri']})
    textlinks=re.findall(r'https?://[^\s<>]+',txt.read_text(encoding='utf-8'))
    return {'titulo':path.stem,'url':url,'archivo':path.relative_to(ROOT).as_posix(),'texto':txt.relative_to(ROOT).as_posix(),'paginas':len(doc),'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'enlaces_pdf':links,'urls_texto':textlinks}
with ThreadPoolExecutor(max_workers=6) as pool:
    records=list(pool.map(download,urls))
if len(records)!=6: raise ValueError(f'Esperados 6 documentos: {len(records)}')
manifest={'consulta':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pagina':PAGE,'documentos':records}
(DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'archivo':r['archivo'],'paginas':r['paginas'],'enlaces':len(r['enlaces_pdf'])} for r in records],ensure_ascii=False,indent=2))
