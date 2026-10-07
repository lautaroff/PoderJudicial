from pathlib import Path
import requests, fitz, json, hashlib, concurrent.futures, re
from urllib.parse import urlsplit,unquote,urljoin
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
urls=[('Programa 2023','https://jusmendoza.gob.ar/wp-content/uploads/2023/04/Programa-para-aspirantes-Ingreso-Poder-Judicial-de-Mendoza.pdf'),('Módulo 1','https://jusmendoza.gob.ar/wp-content/uploads/2023/04/Modulo-1-Concurso-Ingreso-2023.pdf'),('Módulo 2','https://jusmendoza.gob.ar/wp-content/uploads/2023/04/Modulo-2-Concurso-Ingreso-2023.pdf'),('Módulo 3 actualizado junio 2023','https://jusmendoza.gob.ar/wp-content/uploads/2023/06/Modulo-3-Concurso-Ingreso-2023-2.pdf'),('Módulo 4','https://jusmendoza.gob.ar/wp-content/uploads/2023/04/Mo%CC%81dulo-4-Concurso-Ingreso-2023.pdf'),('Manual IURIX FLEX','https://jusmendoza.gob.ar/wp-content/uploads/2022/12/Manual-de-uso-del-Sistema-IURIX-FLEX.pdf'),('Calidad y Gestión Pública','https://jusmendoza.gob.ar/wp-content/uploads/2022/12/Manual-de-Calidad-y-Gestion-Publica.pdf'),('Protocolo segundo examen 2023','https://jusmendoza.gob.ar/wp-content/uploads/2023/09/Metodologia-y-protocolo-de-buenas-practicas-para-el-segundo-examen-de-conocimiento.pdf')]
extra=ROOT/'enlaces-extra.json'
if extra.exists(): urls+= [(x['titulo'],x['url']) for x in json.loads(extra.read_text(encoding='utf-8'))]
def get(pair):
 title,url=pair; rec={'titulo':title,'url':url,'fecha_verificacion':'2026-10-05','alcance':'antecedente histórico; no programa oficial 2026'}
 try:
  r=requests.get(url,timeout=45);rec.update(http=r.status_code,url_final=r.url)
  if r.status_code==200 and r.content[:4]==b'%PDF':
   name=unquote(urlsplit(url).path.split('/')[-1]); p=ROOT/'pdf'/name;p.parent.mkdir(exist_ok=True);p.write_bytes(r.content)
   rec.update(archivo=str(p.relative_to(ROOT.parent)).replace('\\','/'),bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
   doc=fitz.open(p);rec['paginas']=len(doc);t=ROOT/'textos'/f'{p.stem}.txt';t.parent.mkdir(exist_ok=True);t.write_text('\n'.join(f'\n--- PÁGINA {i+1} ---\n'+page.get_text() for i,page in enumerate(doc)),encoding='utf-8');rec['texto']=str(t.relative_to(ROOT.parent)).replace('\\','/')
  elif any(x in url for x in ['youtube','youtu.be','vimeo']):rec['tipo']='video enlazado, no descargado'
  else:rec['tipo']=r.headers.get('content-type','')
 except Exception as e:rec['error']=str(e)
 return rec
items=[];seen=set()
for title,url in urls:
 if url not in seen: items.append((title,url));seen.add(url)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: rows=list(pool.map(get,items))
(ROOT/'catalogo.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
