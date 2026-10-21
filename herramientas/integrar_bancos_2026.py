"""Integra bancos revisados y conserva la práctica general anterior identificada."""
from pathlib import Path
import json, collections

ROOT = Path(__file__).resolve().parents[1]
BANCOS = ROOT / 'contenido' / 'bancos'
INTEGRADO = ROOT / 'contenido' / 'integrado'

questions = []
for name in ['m1-m3', 'm2', 'm4-m5', 'anexos']:
    qs = json.loads((BANCOS / f'{name}.json').read_text(encoding='utf-8'))
    for q in qs:
        q['version'] = 2026
    questions.extend(qs)

old = json.loads((ROOT / 'historico' / 'prepublicacion' / 'preguntas.json').read_text(encoding='utf-8'))
catalog = json.loads((ROOT / 'biblioteca' / 'catalogo.json').read_text(encoding='utf-8'))

institutional = BANCOS / 'institucional.json'
if institutional.exists():
    revised = json.loads(institutional.read_text(encoding='utf-8'))
    assert len(revised) == 40 and all(q['etapa'] == 'institucional' for q in revised)
    questions.extend(revised)

reading = BANCOS / 'lectura.json'
if reading.exists():
    revised = json.loads(reading.read_text(encoding='utf-8'))
    assert len(revised) == 60 and all(q['etapa'] == 'lectura' for q in revised)
    questions.extend(revised)

for q in old:
    if q['etapa'] == 'especificos':
        continue
    if q['etapa'] == 'institucional' and institutional.exists():
        continue
    if q['etapa'] == 'lectura' and reading.exists():
        continue
    q['alcance'] = 'Práctica general; no reproduce videos ni exámenes oficiales 2026'
    if q['etapa'] == 'institucional':
        first = q['fuente'].split('|')[0].strip()
        url = first.split('#')[0]
        record = next((r for r in catalog if r['url'] == url and r.get('archivo')), None)
        if record:
            q['fuente'] = record['archivo'] + ('#' + first.split('#', 1)[1] if '#' in first else '') + ' | Antecedente institucional histórico 2023; práctica general, no video 2026 | ' + first
    questions.append(q)

assert len({q['id'] for q in questions}) == len(questions)
INTEGRADO.mkdir(parents=True, exist_ok=True)
(INTEGRADO / 'preguntas.json').write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({
    'total': len(questions),
    'etapas': dict(collections.Counter(q['etapa'] for q in questions)),
    'modulos_especificos': dict(sorted(collections.Counter(q['modulo'] for q in questions if q['etapa'] == 'especificos').items()))
}, ensure_ascii=False))
