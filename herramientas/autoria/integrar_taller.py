"""Integra enlaces y preserva el historial previo. Operaciones idempotentes."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'taller.js';s=p.read_text(encoding='utf-8')
s=s.replace("!i.correct&&i.confidence==='high'", "i.response!==undefined&&!i.correct&&i.confidence==='high'")
s=s.replace('early:active.early,assessment:', 'early:active.early,supported:Boolean(active.supported),assessment:')
s=s.replace("esc(result.repeat?'Repetición:","esc(result.supported?'Estudio apoyado: pudiste consultar escenas y fuentes.':result.repeat?'Repetición:")
s=s.replace("objective.filter(r=>!r.repeat).length", "objective.filter(r=>!r.repeat&&!r.supported).length")
s=s.replace("videoStage={id,mode,started:Date.now(),lastTime:0}","videoStage={id,mode,started:Date.now(),lastTime:0,repeat:markSeen('video-content:'+id)}")
s=s.replace('if(el.currentTime>videoStage.lastTime+2)', 'if(videoStage&&el.currentTime>videoStage.lastTime+2)')
s=s.replace("const key='video:'+v.id,repeat=markSeen(key);", "const key='video:'+v.id,repeat=markSeen(key)||Boolean(videoStage?.repeat);")
s=s.replace("+(r.early?'<span", "+(r.supported?'<span class=\"chip warning\">Estudio apoyado</span>':'')+(r.early?'<span")
s=s.replace("b.onclick=()=>{const r=state.results.find(x=>x.attemptId===b.dataset.reviewResult)","b.onclick=()=>{if(state.active){$('result-list').insertAdjacentHTML('afterbegin','<p class=\"notice\">Terminá el cuestionario en curso antes de consultar correcciones.</p>');return;}const r=state.results.find(x=>x.attemptId===b.dataset.reviewResult)")
p.write_text(s,encoding='utf-8')
p=ROOT/'app.js';s=p.read_text(encoding='utf-8')
s=s.replace("memoria:read('pjm-memoria-2026',{})}", "memoria:read('pjm-memoria-2026',{}),taller:read('pjm-taller-2026',{})}")
p.write_text(s,encoding='utf-8')
for file in ['index.html','memoria.html']:
    p=ROOT/file;s=p.read_text(encoding='utf-8')
    if 'href="taller.html"' not in s:
        if file=='index.html':
            s=s.replace('<button data-tab="practica">Practicar</button>', '<a href="taller.html">Taller de dominio ↗</a><button data-tab="practica">Practicar</button>')
            s=s.replace('</div><details class="card"><summary>Qué cambió', '<article class="card"><span class="eyebrow">04 · Aplicar y medir</span><h3>Taller de dominio</h3><p>Explicaciones sin opciones, casos que cambian por un dato, secuencias, errores, diagnósticos nuevos y dos jornadas de video.</p><a class="button" href="taller.html">Entrar al taller</a></article></div><details class="card"><summary>Qué cambió')
        else:s=s.replace('href="index.html"', 'href="index.html"',1).replace('</header>', '<a href="taller.html">Taller de dominio ↗</a></header>',1)
    p.write_text(s,encoding='utf-8')
print('Taller integrado: navegación y exportación de avances.')
