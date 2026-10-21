"""Cierre documental y reloj único por intento; evita regeneraciones que borren las mejoras."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'taller.js';s=p.read_text(encoding='utf-8')
s=s.replace("const repeat=markSeen(key);state.active={kind:'diagnostic'", "const repeat=markSeen(key),started=Date.now();state.active={kind:'diagnostic'")
s=s.replace("id,started:Date.now(),deadline:Date.now()+(type==='spec'", "id,started,deadline:started+(type==='spec'")
s=s.replace("repeat=markSeen(key)||Boolean(videoStage?.repeat);state.active", "repeat=markSeen(key)||Boolean(videoStage?.repeat),started=Date.now();state.active")
s=s.replace("type:'video',started:Date.now(),deadline:Date.now()+15", "type:'video',started,deadline:started+15")
p.write_text(s,encoding='utf-8')
p=ROOT/'PLAN-DE-ESTUDIO-2026.md';s=p.read_text(encoding='utf-8').replace('## Objetivo personal de preparación\n\n## Usar el taller','## Usar el taller');p.write_text(s,encoding='utf-8')
p=ROOT/'estudio-2026/REVISION-PEDAGOGICA.md';s=p.read_text(encoding='utf-8').replace('Los formatos propuestos abajo **todavía no están implementados**.', 'Esta revisión precedió la implementación. **Los formatos prioritarios ya están incorporados al taller**, junto con secuencias, párrafos con error, dos textos nuevos y dos videos originales. Ver [cómo usar el taller](COMO-USAR-TALLER.md) y [la verificación](../VERIFICACION.md). Las conclusiones sobre límites de la nota siguen vigentes.')
p.write_text(s,encoding='utf-8')
for name in ['REVISION-INDEPENDIENTE-RUBRICAS.md','REVISION-INDEPENDIENTE-TALLER.md']:
    p=ROOT/'estudio-2026'/name;s=p.read_text(encoding='utf-8')
    if 'Cierre de integración posterior' not in s:s+='\n\n## Cierre de integración posterior\n\nLa integración corrigió los hallazgos documentados: en rúbricas, enunciados, condiciones y fuentes; en diagnósticos DA-40, DA-44, DB-03 y DB-50. C5-001A incluye una respuesta redactada con marcadores, O1-009 pide e identifica las autoridades y O2-024/028/030 explicitan cómputo con fuente en art. 4. Las citas adicionales de escenas/preguntas fueron incorporadas y las claves de videos ya no siguen un ciclo 0–1–2–3. Los MP4 terminados y el navegador se verifican en VERIFICACION.md; esta nota registra integración, sin ampliar retrospectivamente el alcance del revisor.\n'
    p.write_text(s,encoding='utf-8')
print('Cierre aplicado: documentos y reloj único.')
