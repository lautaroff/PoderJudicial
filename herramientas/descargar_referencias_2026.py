"""Descarga referencias explícitas; registra alcance sin ampliar el temario por inferencia."""
from pathlib import Path
import requests, json, hashlib, datetime, html, re
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import fitz
ROOT=Path(__file__).resolve().parent
DEST=ROOT/'biblioteca'/'2026'/'referencias'; DEST.mkdir(parents=True,exist_ok=True)
ITEMS=[
('Reglamento-Poder-Judicial','https://jusmendoza.gob.ar/wp-content/uploads/2022/12/Reglamento-del-Poder-Judicial-de-Mendoza-21-09-1953.pdf','M1 p39: obligatorios arts3 y13; art3 modificado por Ac15422'),
('Acordada-15422','https://jusmendoza.gob.ar/wp-content/uploads/2022/12/Acordada-15422.pdf','M1 p39: lectura obligatoria; residencia'),
('Decreto-Ley-560','https://jusmendoza.gob.ar/wp-content/uploads/2022/12/Decreto-Ley-560.pdf','M1 p39: obligatorio capítuloIII; leer con Ley9665'),
('Ley-9665','https://www.argentina.gob.ar/normativa/provincial/ley-9665-123456789-0abc-defg-566-9000mvorpyel/actualizacion','M1 p39: modificatoria expresamente indicada'),
('Trayectorias-judiciales-2025','https://jusmendoza.gob.ar/wp-content/uploads/2025/06/Trayectorias-judiciales-de-Acceso-a-Justicia-en-Argentina.pdf','M3 p20: lectura recomendada, no declarada obligatoria'),
('CIDH-Justicia-Juvenil','https://www.oas.org/es/cidh/infancia/docs/pdf/justiciajuvenil.pdf','M2 p106: referencia al informe CIDH2011'),
('Ley-9735-Responsabilidad-Penal-Juvenil','https://boe.mendoza.gov.ar/publico/pdf_pedido/76293ce55269c619fc6f8def3da685e7a0e56bd251','M2 p109: anexo leyes publicadas octubre2026'),
('Codigo-Procesal-Penal-Juvenil-2026','https://boe.mendoza.gov.ar/default/public/publico/verpdf/76293ce55269c619fc6f8def3da685e7a0e56bd244/anexo','M2 p109: anexo leyes publicadas octubre2026'),
('WCAG-2.2','https://www.w3.org/TR/WCAG22/','M5 p20: estándar citado; apoyo, sin mandato leer especificación entera'),
('Bus-Federal-Guias','https://www.bus-justicia.org.ar/index.php/bus-federal/guias-tramite','M2 p15: guía operativa; enlace de servicio'),
('Guia-Judicial','https://jusmendoza.gob.ar/guia-judicial-2/','M2 pp2,21: directorio institucional de consulta'),
('Beneficio-Litigar-Sin-Gastos','https://blsg.pjm.gob.ar/','M2 p18: portal de trámite, no PDF adicional'),
('Listas-Proveidos','http://www2.jus.mendoza.gov.ar/listas/proveidos/listas.php','M2 p41: consulta de listas, servicio'),
('Ley-24522-Concursos-y-Quiebras','https://www.argentina.gob.ar/normativa/nacional/ley-24522-1995-25379/actualizacion','M2 p61: conocimiento exigido de las partes respectivas; texto de consulta completo, no obligación de memorizar todos los artículos'),
('Ley-9001-CPCCT','https://www.argentina.gob.ar/normativa/provincial/ley-9001-123456789-0abc-defg-100-9000mvorpyel/actualizacion','M2 p61: arts359–372 y temas procesales mencionados; texto actualizado de consulta'),
('Protocolo-Violencia-Laboral-30979','https://jusmendoza.gob.ar/wp-content/uploads/2023/03/Protocolo-de-Actuacion-frente-a-casos-de-Violencia-Laboral-en-el-Poder-Judicial.pdf','M4 p9: protocolo citado; copia de apoyo enlazada por Dirección de la Mujer'),
('Ley-27801-Regimen-Penal-Juvenil','https://www.argentina.gob.ar/normativa/nacional/ley-27801-423722/texto','M2 pp102–107 y anexo Ley9735: norma nacional citada; texto original oficial de consulta'),
('Ley-9423','https://jusmendoza.gob.ar/wp-content/uploads/2023/05/Ley-N%C2%B0-9423-2.pdf','M1 apartado1.4: norma citada para composición y funciones de la Corte; remisión interna MII incompleta'),
('Ley-9003-Procedimiento-Administrativo','https://www.argentina.gob.ar/normativa/provincial/ley-9003-123456789-0abc-defg-300-9000mvorpyel/actualizacion','M1 apartado1.5: norma citada; consulta para aclarar organización y acto administrativo'),
('Acordada-32299-BLSG','https://jusmendoza.gob.ar/wp-content/uploads/2025/11/Acordada-N%C2%B0-32.299-BLSG.pdf','M2 p18: norma de apoyo para verificar alcance del trámite electrónico de beneficio de litigar sin gastos'),
]
def fetch(item):
    name,url,scope=item
    rec={'titulo':name,'url':url,'alcance':scope,'consulta':'2026-10-12'}
    try:
        existing=DEST/'manifest.json'
        old=json.loads(existing.read_text(encoding='utf-8')) if existing.exists() else []
        saved=next((r for r in old if r['url']==url and r.get('archivo') and (ROOT/r['archivo']).exists()),None)
        if saved: return saved
        r=requests.get(url,timeout=90); rec.update(http=r.status_code,url_final=r.url); r.raise_for_status()
        pdf=r.content.startswith(b'%PDF')
        suffix='.pdf' if pdf else '.html'
        path=DEST/(name+suffix); path.write_bytes(r.content)
        rec.update(archivo=path.relative_to(ROOT).as_posix(),bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
        if pdf:
            doc=fitz.open(path); rec['paginas']=len(doc)
            txt='\n\n'.join(f'=== PÁGINA PDF {i+1} ===\n'+p.get_text(sort=True) for i,p in enumerate(doc))
            rec['enlaces_pdf']=[{'pagina_pdf':i+1,'url':l['uri']} for i,p in enumerate(doc) for l in p.get_links() if l.get('uri')]
        else:
            soup=BeautifulSoup(r.text,'html.parser')
            node=soup.find('main') or soup.find('article') or soup.body or soup
            for tag in node(['script','style','nav','footer','header','form']): tag.decompose()
            txt=node.get_text('\n',strip=True)
            clean=DEST/(name+'-lectura.html')
            clean.write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>'+html.escape(name)+'</title><style>body{max-width:900px;margin:40px auto;padding:20px;font:18px/1.6 system-ui}pre{white-space:pre-wrap}</style><h1>'+html.escape(name)+'</h1><p>Copia de consulta al12/10/2026. '+html.escape(scope)+'</p><p><a href="'+html.escape(url,quote=True)+'">Fuente oficial</a></p><pre>'+html.escape(txt)+'</pre></html>',encoding='utf-8')
            rec['lectura']=clean.relative_to(ROOT).as_posix()
        txtpath=DEST/(name+'.txt'); txtpath.write_text(txt,encoding='utf-8');rec['texto']=txtpath.relative_to(ROOT).as_posix()
    except Exception as e: rec['error']=str(e)
    return rec
with ThreadPoolExecutor(max_workers=8) as pool: records=list(pool.map(fetch,ITEMS))
(DEST/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{k:r[k] for k in ['titulo','http','paginas','error'] if k in r} for r in records],ensure_ascii=False,indent=2))
