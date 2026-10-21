"""Integridad local de fuentes y paginación. No sustituye contraste semántico."""
from pathlib import Path
import json, re, hashlib
from urllib.parse import unquote
import fitz

ROOT = Path(__file__).resolve().parents[1]
INTEGRADO = ROOT / 'contenido' / 'integrado'
VALIDACIONES = ROOT / 'validaciones'
pages = {}
checked = 0
links = 0
errors = []


def pdf(path, page, label):
    global checked
    path = unquote(path).removeprefix('../')
    file = ROOT / path
    if not file.exists():
        errors.append([label, 'No existe', path])
        return
    if path not in pages:
        with fitz.open(file) as doc:
            pages[path] = len(doc)
    if not 1 <= int(page) <= pages[path]:
        errors.append([label, 'Página fuera de rango', page, pages[path]])
    checked += 1


def markdown(text, label):
    global links
    for _, url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text):
        if url.startswith(('https:', 'http:', '#', 'mailto:')):
            continue
        path = url.split('#')[0].removeprefix('../')
        links += 1
        if path == 'historico-prepublicacion' or path.startswith('historico-prepublicacion/'):
            path = path.replace('historico-prepublicacion', 'historico/prepublicacion', 1)
        if not (ROOT / path).exists() and (ROOT / 'estudio-2026' / path).exists():
            path = 'estudio-2026/' + path
        if not (ROOT / path).exists():
            errors.append([label, 'Enlace ausente', path])
        m = re.search(r'#page=(\d+)', url)
        if path.endswith('.pdf') and m:
            pdf(path, m.group(1), label)


docs = ['README.md']
docs += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT / 'estudio-2026').glob('*.md'))]
for name in docs:
    markdown((ROOT / name).read_text(encoding='utf-8'), name)

visual = json.loads((INTEGRADO / 'memoria-datos.json').read_text(encoding='utf-8'))
mods = {m['id']: m for m in visual['modules']}
sourcecount = 0
concepts = 0


def walk(node, label):
    global sourcecount, concepts
    if isinstance(node, dict):
        if 'sources' in node or 'rootSources' in node:
            concepts += 1
            source_items = node.get('sources', node.get('rootSources'))
            assert source_items, label
            for s in source_items:
                path = s.get('file') or s.get('url') or mods[s['module']]['file']
                if path.startswith(('https:', 'http:')):
                    pass
                elif path.lower().endswith('.pdf'):
                    pdf(path, s['page'], label)
                elif not (ROOT / path).is_file():
                    errors.append([label, 'Fuente local ausente', path])
                elif s.get('page'):
                    errors.append([label, 'Página inventada en fuente no PDF', path])
                sourcecount += 1
        for key, value in node.items():
            walk(value, label + '/' + key)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            walk(value, label + '/' + str(i))


walk(visual, 'memoria')
hashes = 0
records = json.loads((ROOT / 'biblioteca/2026/programa/manifest.json').read_text(encoding='utf-8'))['documentos']
records += json.loads((ROOT / 'biblioteca/2026/referencias/manifest.json').read_text(encoding='utf-8'))
for r in records:
    assert not r.get('error'), r
    file = ROOT / r['archivo']
    if hashlib.sha256(file.read_bytes()).hexdigest() != r['sha256']:
        errors.append([r['titulo'], 'Hash distinto'])
    if file.suffix == '.pdf':
        pdf(r['archivo'], r['paginas'], r['titulo'])
    hashes += 1

report = {
    'fecha': '2026-10-21',
    'documentos_estudio': len(docs),
    'enlaces_locales': links,
    'referencias_pdf_paginadas': checked,
    'conceptos_visuales_con_fuente': concepts,
    'fuentes_visuales': sourcecount,
    'hashes_comprobados': hashes,
    'pdf_distintos': len(pages),
    'errores': errors
}
VALIDACIONES.mkdir(parents=True, exist_ok=True)
(VALIDACIONES / 'validacion-enlaces-2026.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
if errors:
    raise SystemExit(1)
