from pathlib import Path
import zipfile,json,hashlib
ROOT=Path(__file__).resolve().parent
names=['index.html','estudio.css','app.js','datos-preguntas.js','fuentes-2026.js','indice-2026.json','preguntas.json','textos.json','CUADERNO-DE-EJERCICIOS.html','README.md','GUIA-CONCURSO-2026.md','MANUAL-DE-PREPARACION.md','BIBLIOTECA-Y-TEMARIO.md','PLAN-DE-ESTUDIO.md','PLAN-DE-ESTUDIO-2026.md','ACTUALIZACION-2026.md','EVALUACIONES-REALES-Y-ANTECEDENTES.md','REVISION-CONTENIDO.md','VERIFICACION.md','memoria.html','memoria.css','memoria.js','memoria-datos.json','memoria-datos.js','generar_memoria.py','preparar_material.py','verificar_simulador.cjs','verificar_enlaces_2026.py','integrar_documentos_2026.py','integrar_bancos_2026.py','generar_fuentes_2026.py','descargar_2026.py','descargar_referencias_2026.py','empaquetar.py','validacion-datos-2026.json','validacion-logica-2026.json','validacion-enlaces-2026.json']
files=[ROOT/name for name in names]
files.extend(ROOT/name for name in ['mapas.js','mapas.css','preparar_mapas.py','validacion-mapas-2026.json','validacion-mapas-navegador-2026.json','output/playwright/comprobar-mapas.js'])
files.extend(p for p in (ROOT/'mapas-2026').glob('*') if p.suffix in {'.json','.md'})
files.extend(ROOT/name for name in ['output/playwright/comprobar-rotacion.js','validacion-rotacion-2026.json'])
files.extend(ROOT/name for name in ['taller.html','taller.css','taller.js','taller-datos.js','preparar_taller.py','integrar_taller.py','corregir_taller.py','generar_videos_practica.py','validacion-taller-2026.json','validacion-taller-navegador-2026.json','validacion-taller-video-2026.json'])
files.extend(p for p in (ROOT/'taller-datos').glob('*.json'))
files.extend(p for p in (ROOT/'videos').glob('*') if p.suffix in {'.mp4','.vtt','.html'})
files.extend(ROOT/'video-estudio'/name for name in ['index.html','v1.source','v2.source','hyperframes.json','package.json','meta.json','BRIEF.md','assets/gsap.min.js'])
files.extend(ROOT/name for name in ['output/playwright/comprobar-taller.js','output/playwright/comprobar-taller-video.js','output/video-check-v1.json','output/video-check-v2.json'])
files.append(ROOT/'validacion-navegador-2026.json')
files.extend([ROOT/'output/playwright/comprobar-portal.js',ROOT/'output/playwright/comprobar-final.js',ROOT/'output/playwright/comprobar-navegacion.js'])
for folder in ['biblioteca','estudio-2026','bancos-2026','historico-prepublicacion']:
    files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and 'juvenil-paginas' not in p.parts and '__pycache__' not in p.parts and (folder=='biblioteca' or p.suffix in {'.md','.json'}))
files=sorted(set(files))
missing=[str(p) for p in files if not p.exists()]
if missing:raise SystemExit('Faltan archivos: '+repr(missing))
manifest={p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
out=ROOT/'PREPARACION-JUDICIAL-MENDOZA-2026-TALLER.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:z.write(p,p.relative_to(ROOT).as_posix())
    z.writestr('MANIFIESTO-ARCHIVOS.json',json.dumps(manifest,ensure_ascii=False,indent=2))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    for name,meta in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==meta['sha256'],name
    assert all(name in z.namelist() for name in ['index.html','memoria.html','datos-preguntas.js'])
report={'zip':str(out),'archivos':len(files)+1,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'crc_y_hashes':'PASS'}
(ROOT/'verificacion-paquete-2026.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
