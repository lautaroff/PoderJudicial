"""Valida contenidos y fuentes del taller; genera datos locales sin fetch en el navegador."""
from pathlib import Path
from collections import Counter
import json, re, hashlib, subprocess, argparse
import fitz

ROOT = Path(__file__).resolve().parents[1]
INTEGRADO = ROOT / 'contenido' / 'integrado'
TALLER_DIR = ROOT / 'contenido' / 'taller'
VALIDACIONES = ROOT / 'validaciones'

args = argparse.ArgumentParser()
args.add_argument('--draft', action='store_true')
cfg = args.parse_args()


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


modules = read_json(INTEGRADO / 'indice-2026.json')
data = {'modules': [{'id': m['id'], 'title': m['titulo'], 'file': m['archivo'], 'color': m['color']} for m in modules]}
for name in ['open', 'cases', 'sequences', 'errors', 'diagnostics', 'videos']:
    file = {'open': 'abiertas', 'cases': 'casos', 'sequences': 'secuencias', 'errors': 'errores', 'diagnostics': 'diagnosticos', 'videos': 'videos'}[name]
    data[name] = read_json(TALLER_DIR / (file + '.json'))

ids = set()
prompts = set()
pdfs = {}
refs = 0
counts = Counter()
bank_prompts = {re.sub(r'\s+', ' ', q['pregunta']).strip().casefold() for q in read_json(INTEGRADO / 'preguntas.json')}


def identity(item):
    assert item['id'] not in ids, item['id']
    ids.add(item['id'])


def sources(items):
    global refs
    assert items, 'Falta fuente'
    for s in items:
        refs += 1
        file = s['file']
        assert s.get('label'), s
        assert file.startswith(('biblioteca/', 'videos/')), s
        path = ROOT / file
        if cfg.draft and path.suffix == '.mp4' and not path.exists():
            continue
        assert path.is_file(), file
        if path.suffix == '.pdf':
            if file not in pdfs:
                with fitz.open(path) as pdf:
                    pdfs[file] = len(pdf)
            assert type(s.get('page')) is int and 1 <= s['page'] <= pdfs[file], s
        elif path.suffix == '.mp4':
            assert 0 <= s['time'] < 360, s
        else:
            assert not s.get('page'), 'No inventar página en HTML'


def criteria(points):
    assert len(points) >= 2, points
    assert len({c['id'] for c in points}) == len(points), points
    assert all(c.get('text') and type(c.get('critical')) is bool for c in points), points


for name, n in [('open', 90), ('cases', 20), ('sequences', 12), ('errors', 20)]:
    assert len(data[name]) == n, (name, len(data[name]))
    counts[name] = n
    for item in data[name]:
        identity(item)
        assert item['module'] in range(1, 6) and item.get('topic') and item.get('title'), item['id']
        sources(item['sources'])
        if name == 'cases':
            assert item.get('changed') and item.get('keyDifference'), item['id']
            for key in ['a', 'b']:
                part = item[key]
                assert all(part.get(k) for k in ['text', 'prompt', 'model'])
                criteria(part['checkpoints'])
                sources(part['sources'])
        elif name == 'sequences':
            stepids = [s['id'] for s in item['steps']]
            assert 4 <= len(stepids) <= 7 and len(set(stepids)) == len(stepids)
            assert len(item['correct']) == len(stepids) and set(item['correct']) == set(stepids)
            assert item.get('scope') and item.get('explanation')
            assert [(l['from'], l['to']) for l in item['links']] == list(zip(item['correct'], item['correct'][1:])), item['id']
            item['checkpoints'] = [
                {'id': 's1', 'text': 'Explico las dependencias entre pasos con las razones del modelo.', 'critical': True},
                {'id': 's2', 'text': 'Mantengo el supuesto y alcance indicados; no mezclo procedimientos distintos.', 'critical': True},
                {'id': 's3', 'text': 'Si hay plazos, identifico su inicio y unidad; si no, no invento un plazo.', 'critical': True}
            ]
        else:
            assert item.get('prompt') and item.get('model')
            criteria(item['checkpoints'])
            if name == 'errors':
                assert item.get('flawed') and item.get('explanation')


def questionnaire(items, n, optioncount, reserved=False, reading=False):
    assert len(items) == n
    for q in items:
        identity(q)
        assert len(q['options']) == optioncount and len(set(q['options'])) == optioncount, q['id']
        assert type(q['correct']) is int and q['correct'] in range(optioncount) and q.get('why'), q['id']
        prompt = re.sub(r'\s+', ' ', q['prompt']).strip().casefold()
        assert prompt not in prompts, q['id']
        prompts.add(prompt)
        if reserved:
            assert prompt not in bank_prompts, 'Reutiliza pregunta del banco: ' + q['id']
        if reading:
            assert q.get('evidence'), q['id']
        else:
            sources(q['sources'])


forms = data['diagnostics']['forms']
assert [f['id'] for f in forms] == ['A', 'B']
for f in forms:
    questionnaire(f['questions'], 50, 4, True)
    assert Counter(q['module'] for q in f['questions']) == Counter({i: 10 for i in range(1, 6)})
reading = data['diagnostics']['reading']
assert len(reading) == 2
for t in reading:
    assert 600 <= len(t['text'].split()) <= 800, (t['id'], len(t['text'].split()))
    questionnaire(t['questions'], 10, 3, True, True)
assert len(data['videos']) == 2
video_metadata = []
for v in data['videos']:
    assert v['duration'] == 360 and len(v['scenes']) == 12
    questionnaire(v['questions'], 20, 4)
    for i, s in enumerate(v['scenes']):
        assert s['start'] == i * 30 and s['duration'] == 30 and s.get('text')
        sources(s['sources'])
    for file in [v['file'], v['captions'], 'videos/' + v['id'].lower() + '-transcripcion.html']:
        if not (cfg.draft and file.endswith('.mp4')):
            assert (ROOT / file).is_file(), file
    if not cfg.draft:
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(ROOT / v['file'])], text=True))
        stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        assert abs(float(probe['format']['duration']) - 360) < .25
        assert stream['width'] == 1280 and stream['height'] == 720 and (ROOT / v['file']).stat().st_size > 10000
        video_metadata.append({'file': v['file'], 'duration': float(probe['format']['duration']), 'width': stream['width'], 'height': stream['height']})

(ROOT / 'taller-datos.js').write_text('window.TALLER=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
p = ROOT / 'taller.html'
s = p.read_text(encoding='utf-8')
for file in ['taller.css', 'taller.js', 'taller-datos.js']:
    digest = hashlib.sha256((ROOT / file).read_bytes()).hexdigest()[:12]
    s = re.sub(re.escape(file) + r'(?:\?v=[a-zA-Z0-9]+)?', file + '?v=' + digest, s)
p.write_text(s, encoding='utf-8')
report = {
    'status': 'DRAFT' if cfg.draft else 'PASS',
    'ejercicios': dict(counts),
    'diagnosticos_especificos': 100,
    'diagnosticos_lectura': 20,
    'preguntas_videos': 40,
    'ids_unicos': len(ids),
    'referencias': refs,
    'pdfs': len(pdfs),
    'videos': video_metadata,
    'textos_lectura_palabras': [len(t['text'].split()) for t in reading]
}
VALIDACIONES.mkdir(parents=True, exist_ok=True)
(VALIDACIONES / 'validacion-taller-2026.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
