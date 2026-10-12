"""Valida y empaqueta datos embebidos: el portal funciona sin fetch ni servidor."""
from pathlib import Path
import json,html,re,collections,hashlib
import fitz
ROOT=Path(__file__).resolve().parent
names=['README.md','ACTUALIZACION-2026.md','GUIA-CONCURSO-2026.md','MANUAL-DE-PREPARACION.md','BIBLIOTECA-Y-TEMARIO.md','PLAN-DE-ESTUDIO.md','EVALUACIONES-REALES-Y-ANTECEDENTES.md','REVISION-CONTENIDO.md','VERIFICACION.md']
names += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'estudio-2026').glob('*.md'))]
names += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'historico-prepublicacion').glob('*.md'))]
docs={}
for name in names:
    path=ROOT/name
    assert path.exists(),name
    def link(m):
        label,url=m.groups()
        if url.startswith(('http:','https:','#')):return m.group(0)
        url=url.removeprefix('../')
        stem=url.split('#')[0]
        if not (ROOT/stem).exists() and (path.parent/stem).exists():url=(path.parent/Path(stem)).relative_to(ROOT).as_posix()+('#'+url.split('#',1)[1] if '#' in url else '')
        return '['+label+']('+url+')'
    docs[name]=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,path.read_text(encoding='utf-8'))
questions=json.loads((ROOT/'preguntas.json').read_text(encoding='utf-8'))
seen=set();pagecache={};sources_checked=0
def check_pdf(value,label):
    global sources_checked
    match=re.match(r'([^|]+\.pdf)#page=(\d+)',value)
    assert match,(label,'Sin PDF/página',value)
    name,page=match.groups();name=name.strip();page=int(page)
    assert (ROOT/name).exists(),(label,'Fuente ausente',name)
    if name not in pagecache:
        with fitz.open(ROOT/name) as d:pagecache[name]=len(d)
    assert 1<=page<=pagecache[name],(label,page,pagecache[name])
    sources_checked+=1
for q in questions:
    assert q['id'] not in seen,('ID repetido',q['id'])
    seen.add(q['id'])
    assert q['etapa'] in {'especificos','institucional','lectura'}
    assert len(q['opciones'])==(3 if q['etapa']=='lectura' else 4),q['id']
    assert type(q['correcta']) is int and 0<=q['correcta']<len(q['opciones']),q['id']
    assert all(q.get(k) for k in ['pregunta','explicacion','fuente']),q['id']
    assert len(set(q['opciones']))==len(q['opciones']),q['id']
    assert '\ufffd' not in json.dumps(q,ensure_ascii=False),q['id']
    if q['etapa']=='lectura':assert q.get('texto'),q['id']
    else:check_pdf(q['fuente'],q['id'])
    for r in q.get('referencias_adicionales',[]):
        assert r['url'].startswith(('biblioteca/','https://')),q['id']
        if r['url'].startswith('biblioteca/'):assert (ROOT/r['url'].split('#')[0]).exists(),q['id']
    for f in q.get('fuentes',[]):check_pdf(f['archivo']+'#page='+str(f['pagina']),q['id'])
    if q['etapa']=='especificos':
        assert q['version']==2026 and q['modulo'] in range(1,6),q['id']
        assert re.fullmatch(str(q['modulo'])+r'\.[1-6](?:\.[1-3])?',q['subtema']),q['id']
counts=collections.Counter(q['etapa'] for q in questions)
assert counts['especificos']>=400 and counts['institucional']==40 and counts['lectura']==60,counts
groups=collections.Counter(q['texto'] for q in questions if q['etapa']=='lectura')
assert len(groups)==6 and all(n==10 for n in groups.values())
coverage=set('.'.join(q['subtema'].split('.')[:2]) for q in questions if q['etapa']=='especificos')
index=json.loads((ROOT/'indice-2026.json').read_text(encoding='utf-8'))
expected={a['id'] for m in index for a in m['apartados']}
assert coverage==expected,('Apartados',coverage^expected)
(ROOT/'datos-preguntas.js').write_text('window.PREGUNTAS = '+json.dumps(questions,ensure_ascii=False)+';\nwindow.DOCUMENTOS = '+json.dumps(docs,ensure_ascii=False)+';\n',encoding='utf-8')

esc=html.escape
parts=['''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cuaderno de ejercicios · 2026</title><style>body{max-width:900px;margin:40px auto;font:17px/1.6 Segoe UI,sans-serif;padding:20px;color:#1c354a}article{margin:28px 0;break-inside:avoid}h1,h2{font-family:Georgia,serif}a{color:#285dab}nav a{margin-right:18px}small{overflow-wrap:anywhere}@media print{nav,button{display:none}h2{break-before:page}}</style></head><body><h1>Cuaderno de ejercicios originales</h1><p>Actualización: 12 de octubre de 2026. Preparación independiente. Los específicos usan el programa 2026 y sus remisiones; institucionales son práctica general con sus fuentes identificadas y comprensión usa seis textos originales. No son preguntas oficiales. Las soluciones explicadas están al final, con acceso a la fuente.</p><nav><a href="index.html">Volver al portal</a><a href="#especificos">Específicos</a><a href="#lectura">Lectura</a><a href="#institucional">Institucionales</a><a href="#soluciones">Soluciones</a><button onclick="window.print()">Imprimir</button></nav>''']
for stage in ['especificos','lectura','institucional']:
    parts.append('<h2 id="'+stage+'">'+stage.capitalize()+'</h2>')
    stageqs=[q for q in questions if q['etapa']==stage]
    if stage=='especificos':stageqs.sort(key=lambda q:(q['modulo'],q['subtema'],q['id']))
    last=None
    for q in stageqs:
        if q.get('texto') and q['texto']!=last:
            last=q['texto'];parts.append('<blockquote>'+esc(last).replace('\n','<br>')+'</blockquote>')
        parts.append('<article id="'+esc(q['id'])+'"><small>'+esc(str(q.get('subtema',q['tema'])))+'</small><p><strong>'+esc(q['id']+'. '+q['pregunta'])+'</strong></p><ol type="A">'+''.join('<li>'+esc(o)+'</li>' for o in q['opciones'])+'</ol></article>')
parts.append('<h2 id="soluciones">Soluciones explicadas</h2>')
for q in questions:
    source=q['fuente'];first=source.split('|')[0].strip()
    if '.pdf#page=' in first:
        links='<a href="'+esc(first,quote=True)+'" target="_blank">Abrir PDF · página '+esc(first.split('#page=')[1])+'</a>'
        if len(q.get('fuentes',[]))>1:
            links=' · '.join('<a href="'+esc(f['archivo']+'#page='+str(f['pagina']),quote=True)+'" target="_blank">'+esc(f.get('descripcion','Fuente'))+' · PDF '+str(f['pagina'])+'</a>' for f in q['fuentes'])
    else:links=esc(source)+' · <a href="#'+esc(q['id'])+'">Volver al ejercicio y su texto</a>'
    links+=''.join(' · <a href="'+esc(r['url'],quote=True)+'" target="_blank">'+esc(r['label'])+'</a>' for r in q.get('referencias_adicionales',[]))
    parts.append('<article><strong>'+esc(q['id'])+' · '+chr(65+q['correcta'])+'</strong><p>'+esc(q['explicacion'])+'</p><small>'+links+'</small></article>')
parts.append('</body></html>')
(ROOT/'CUADERNO-DE-EJERCICIOS.html').write_text('\n'.join(parts),encoding='utf-8')
report={'preguntas':len(questions),'por_etapa':dict(counts),'textos_lectura':len(groups),'apartados_cubiertos':len(coverage),'documentos_embebidos':len(docs),'referencias_pdf_validadas':sources_checked,'pdf_distintos_en_preguntas':len(pagecache)}
(ROOT/'validacion-datos-2026.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
portal=ROOT/'index.html';markup=portal.read_text(encoding='utf-8')
for resource in ['estudio.css','app.js','datos-preguntas.js','fuentes-2026.js']:
    digest=hashlib.sha256((ROOT/resource).read_bytes()).hexdigest()[:12]
    markup=re.sub('"'+re.escape(resource)+r'(?:\?v=[^"\s]+)?"','"'+resource+'?v='+digest+'"',markup)
portal.write_text(markup,encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
