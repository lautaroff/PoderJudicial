from pathlib import Path
import json, re, fitz, hashlib

ROOT = Path(__file__).resolve().parents[1]
INTEGRADO = ROOT / 'contenido' / 'integrado'
manifest = json.loads((ROOT / 'biblioteca/2026/programa/manifest.json').read_text(encoding='utf-8'))
refs = json.loads((ROOT / 'biblioteca/2026/referencias/manifest.json').read_text(encoding='utf-8'))
defs = [
    (1, 'Organización del Estado', 'Estado', '#285dab', 'estudio-2026/GUIA-M1-M3.md', [(1, 'Conceptos claves de Estado y derecho', 2), (2, 'Funciones del poder estatal', 10), (3, 'Poder Judicial de Mendoza', 25), (4, 'Funciones de la Suprema Corte', 28), (5, 'Organización administrativa', 30), (6, 'Estatuto del empleado público', 38)]),
    (2, 'El Poder Judicial de Mendoza', 'Fueros', '#0b7274', 'estudio-2026/GUIA-M2.md', [(1, 'Civil, comercial, tributario, paz y concursal', 2), (2, 'Familia', 63), (3, 'Laboral', 70), (4, 'Penal y penal juvenil', 86)]),
    (3, 'Derechos Humanos', 'Derechos', '#7354a5', 'estudio-2026/GUIA-M1-M3.md', [(1, 'Derechos y protección normativa', 3), (2, 'Principios', 5), (3, 'Características y clasificación', 8), (4, 'Obligaciones de los Estados', 10), (5, 'Grupos en situación de vulnerabilidad', 16), (6, 'Enfoque de derechos humanos', 18)]),
    (4, 'Violencia de Género', 'Género', '#af466c', 'estudio-2026/GUIA-M4-M5.md', [(1, 'Conceptos elementales', 2), (2, 'Diversidad', 4), (3, 'Tipos y modalidades de violencia', 5), (4, 'Revictimización y violencia institucional', 8), (5, 'Protocolo de violencia laboral', 9)]),
    (5, 'Atención para un Servicio de Justicia', 'Atención', '#936c17', 'estudio-2026/GUIA-M4-M5.md', [(1, 'Justicia centrada en la ciudadanía', 2), (2, 'Experiencia del usuario de justicia', 6), (3, 'Comunicación y lenguaje claro', 8), (4, 'Atención y resolución de conflictos', 14), (5, 'Accesibilidad universal e inclusión', 18), (6, 'Perfil del agente judicial', 23)]),
]
docs = []
mods = []
for rec in manifest['documentos']:
    match = re.search(r'Modulo-(\d)', rec['archivo'])
    id = int(match.group(1)) if match else 0
    title = next((d[1] for d in defs if d[0] == id), 'Índice de contenidos')
    doc = fitz.open(ROOT / rec['archivo'])
    assert len(doc) == rec['paginas']
    assert hashlib.sha256((ROOT / rec['archivo']).read_bytes()).hexdigest() == rec['sha256']
    docs.append({'id': id, 'titulo': title, 'archivo': rec['archivo'], 'url': rec['url'], 'paginas': len(doc), 'textos': [p.get_text(sort=True) for p in doc]})
    if id:
        d = next(x for x in defs if x[0] == id)
        mods.append({'id': id, 'titulo': title, 'corto': d[2], 'color': d[3], 'guia': d[4], 'archivo': rec['archivo'], 'url': rec['url'], 'paginas': len(doc), 'apartados': [{'id': str(id) + '.' + str(n), 'titulo': t, 'pagina': p} for n, t, p in d[5]]})
for i, rec in enumerate(refs):
    if rec.get('archivo', '').endswith('.pdf'):
        doc = fitz.open(ROOT / rec['archivo'])
        docs.append({'id': 100 + i, 'titulo': rec['titulo'], 'archivo': rec['archivo'], 'url': rec['url'], 'paginas': len(doc), 'textos': [p.get_text(sort=True) for p in doc]})
payload = {'fecha': '2026-10-12', 'modulos': sorted(mods, key=lambda m: m['id']), 'documentos': sorted(docs, key=lambda d: d['id']), 'referencias': refs}
(ROOT / 'fuentes-2026.js').write_text('window.FUENTES2026 = ' + json.dumps(payload, ensure_ascii=False) + ';\n', encoding='utf-8')
INTEGRADO.mkdir(parents=True, exist_ok=True)
(INTEGRADO / 'indice-2026.json').write_text(json.dumps(payload['modulos'], ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'documentos_lector': len(docs), 'apartados': sum(len(m['apartados']) for m in mods), 'paginas_oficiales': sum(r['paginas'] for r in manifest['documentos'])}))
