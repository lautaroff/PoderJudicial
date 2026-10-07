from pathlib import Path
import zipfile, json, hashlib
ROOT=Path(__file__).resolve().parent
names=['index.html','app.js','datos-preguntas.js','preguntas.json','textos.json','CUADERNO-DE-EJERCICIOS.html','LEEME.md','GUIA-CONCURSO-2026.md','MANUAL-DE-PREPARACION.md','BIBLIOTECA-Y-TEMARIO.md','PLAN-DE-ESTUDIO.md','EVALUACIONES-REALES-Y-ANTECEDENTES.md','REVISION-CONTENIDO.md','VERIFICACION.md','preparar_material.py','verificar_simulador.cjs','empaquetar.py']
files=[ROOT/name for name in names]+[p for p in (ROOT/'biblioteca').rglob('*') if p.is_file()]
missing=[str(p) for p in files if not p.exists()]
if missing: raise SystemExit('Faltan archivos: '+repr(missing))
manifest={p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
out=ROOT/'PREPARACION-JUDICIAL-MENDOZA-2026.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(ROOT).as_posix())
    z.writestr('MANIFIESTO-ARCHIVOS.json',json.dumps(manifest,ensure_ascii=False,indent=2))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert 'index.html' in z.namelist()
print(json.dumps({'zip':str(out),'archivos':len(files)+1,'bytes':out.stat().st_size},ensure_ascii=False))
