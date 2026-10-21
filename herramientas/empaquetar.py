from pathlib import Path
import zipfile, json, hashlib

ROOT = Path(__file__).resolve().parents[1]
PAQUETES = ROOT / 'paquetes'
VALIDACIONES = ROOT / 'validaciones'

root_files = [
    'index.html', 'estudio.css', 'app.js', 'datos-preguntas.js', 'fuentes-2026.js',
    'CUADERNO-DE-EJERCICIOS.html', 'README.md',
    'memoria.html', 'memoria.css', 'memoria.js', 'memoria-datos.js', 'mapas.js', 'mapas.css',
    'taller.html', 'taller.css', 'taller.js', 'taller-datos.js'
]
files = [ROOT / name for name in root_files]
files.extend(p for p in (ROOT / 'videos').glob('*') if p.suffix in {'.mp4', '.vtt', '.html'})

for folder in ['biblioteca', 'contenido', 'estudio-2026', 'herramientas', 'validaciones', 'historico']:
    for p in (ROOT / folder).rglob('*'):
        if not p.is_file():
            continue
        if any(skip in p.parts for skip in ('juvenil-paginas', '__pycache__', 'capturas-previas', '.hyperframes', '.thumbnails', 'snapshots', 'node_modules', 'autoria')):
            continue
        files.append(p)

files = sorted(set(files))
missing = [str(p) for p in files if not p.exists()]
if missing:
    raise SystemExit('Faltan archivos: ' + repr(missing))

manifest = {p.relative_to(ROOT).as_posix(): {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
PAQUETES.mkdir(parents=True, exist_ok=True)
out = PAQUETES / 'PREPARACION-JUDICIAL-MENDOZA-2026-TALLER.zip'
with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in files:
        z.write(p, p.relative_to(ROOT).as_posix())
    z.writestr('MANIFIESTO-ARCHIVOS.json', json.dumps(manifest, ensure_ascii=False, indent=2))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    for name, meta in manifest.items():
        assert hashlib.sha256(z.read(name)).hexdigest() == meta['sha256'], name
    assert all(name in z.namelist() for name in ['index.html', 'memoria.html', 'taller.html', 'datos-preguntas.js'])

report = {
    'zip': out.relative_to(ROOT).as_posix(),
    'archivos': len(files) + 1,
    'bytes': out.stat().st_size,
    'sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
    'crc_y_hashes': 'PASS'
}
VALIDACIONES.mkdir(parents=True, exist_ok=True)
(VALIDACIONES / 'verificacion-paquete-2026.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
