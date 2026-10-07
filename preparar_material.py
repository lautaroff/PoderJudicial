"""Empaqueta el material para consulta local sin servidor ni dependencias."""
from pathlib import Path
import json, html, re

ROOT = Path(__file__).resolve().parent
docs = {}
for name in ['GUIA-CONCURSO-2026.md', 'MANUAL-DE-PREPARACION.md', 'BIBLIOTECA-Y-TEMARIO.md', 'PLAN-DE-ESTUDIO.md', 'EVALUACIONES-REALES-Y-ANTECEDENTES.md']:
    path = ROOT / name
    if not path.exists():
        raise SystemExit('Falta documento: ' + name)
    docs[name] = path.read_text(encoding='utf-8')
questions = json.loads((ROOT / 'preguntas.json').read_text(encoding='utf-8'))
if isinstance(questions, dict):
    questions = questions['preguntas']
seen = set()
for q in questions:
    assert q['id'] not in seen, 'ID repetido'
    seen.add(q['id'])
    assert q['etapa'] in {'especificos','institucional','lectura'}
    assert len(q['opciones']) == (3 if q['etapa']=='lectura' else 4), q['id']
    assert isinstance(q['correcta'],int) and 0 <= q['correcta'] < len(q['opciones'])
    assert q['pregunta'] and q['explicacion'] and q['fuente'], q['id']
    assert len(set(q['opciones'])) == len(q['opciones']), q['id']
    if q['etapa']=='lectura': assert q.get('texto'), q['id']
for stage, minimum in [('especificos',100),('institucional',40),('lectura',40)]:
    assert sum(q['etapa']==stage for q in questions) >= minimum, stage
groups = {}
for q in questions:
    if q['etapa']=='lectura': groups[q['texto']] = groups.get(q['texto'],0)+1
assert all(n>=10 for n in groups.values())
(ROOT/'datos-preguntas.js').write_text('window.PREGUNTAS = '+json.dumps(questions,ensure_ascii=False)+';\nwindow.DOCUMENTOS = '+json.dumps(docs,ensure_ascii=False)+';\n',encoding='utf-8')
parts=['<!doctype html><html lang="es"><meta charset="utf-8"><title>Cuaderno de ejercicios</title><style>body{max-width:900px;margin:40px auto;font:17px/1.6 Segoe UI,sans-serif;padding:20px}article{margin:28px 0;break-inside:avoid}h1,h2{color:#17354c}details{margin:10px 0}@media print{details{display:block}summary{display:none}}</style><h1>Cuaderno de ejercicios originales</h1><p>Preparación independiente, 5 de octubre de 2026. No es un examen oficial. Fuentes históricas sujetas al programa 2026. Las soluciones están al final; en pantalla también podés desplegarlas.</p>']
for stage in ['institucional','lectura','especificos']:
    parts.append('<h2>'+stage.capitalize()+'</h2>')
    last_text=None
    for q in [q for q in questions if q['etapa']==stage]:
        if q.get('texto') and q['texto']!=last_text:
            last_text=q['texto'];parts.append('<blockquote>'+html.escape(last_text).replace('\n','<br>')+'</blockquote>')
        parts.append('<article><strong>'+html.escape(str(q['id']))+'. '+html.escape(q['pregunta'])+'</strong><ol type="A">'+''.join('<li>'+html.escape(o)+'</li>' for o in q['opciones'])+'</ol></article>')
parts.append('<h2>Soluciones explicadas</h2>')
for q in questions:
    parts.append('<article><strong>'+html.escape(str(q['id']))+' · '+chr(65+q['correcta'])+'</strong><p>'+html.escape(q['explicacion'])+'</p><small>'+html.escape(q['fuente'])+'</small></article>')
parts.append('</html>')
(ROOT/'CUADERNO-DE-EJERCICIOS.html').write_text('\n'.join(parts),encoding='utf-8')
print(json.dumps({'preguntas':len(questions),'por_etapa':{s:sum(q['etapa']==s for q in questions) for s in ['institucional','lectura','especificos']},'textos_lectura':len(groups),'documentos':len(docs)},ensure_ascii=False))
