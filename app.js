'use strict';
const bank=window.PREGUNTAS||[],sources=window.FUENTES2026||{},modules=sources.modulos||[],numBank=(window.NUMEROS&&window.NUMEROS.items)||[];
let current=[],answers={},typedAnswers={},discarded={},flagged={},deadline=null,timer=null,finished=true,activeMode='',activeMinutes=0,currentTab='inicio',currentOpenDoc='',currentOpenDocMod=0;
const $=id=>document.getElementById(id);
const safe=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normStr=s=>String(s??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim().toLowerCase().replace(/\s+/g,' ');
const read=(key,fallback)=>{try{const value=JSON.parse(localStorage.getItem(key));return value===null?fallback:value}catch{return fallback}};
const save=(key,value)=>{try{localStorage.setItem(key,JSON.stringify(value))}catch{if($('bankStatus'))$('bankStatus').textContent='El navegador no permite guardar avances; descargá tus resultados al terminar.'}};
const allowed=url=>/^(https?:\/\/|biblioteca\/|estudio-2026\/|historico(?:-prepublicacion)?\/|contenido\/|validaciones\/|videos\/|(?:index|memoria|taller|CUADERNO-DE-EJERCICIOS)\.html(?:[?#].*)?$|validacion-[a-z0-9-]+\.json$|[A-Z][A-Z0-9-]+\.md(?:#.*)?$|#)/i.test(url);

const TOPIC_MAP={
  '1.1':'estado','1.2':'m1-organos-funciones','1.3':'m1-estructura-judicial','1.4':'m1-corte-organizacion','1.5':'administracion','1.6':'m1-empleo',
  '2.1':'proceso','2.2':'m2-familia','2.3':'m2-proceso-laboral','2.4':'penal',
  '3.1':'derechos','3.2':'derechos','3.3':'m3-red-derechos','3.4':'m3-red-derechos','3.5':'m3-proteccion','3.6':'m3-proteccion',
  '4.1':'genero','4.2':'m4-desigualdades','4.3':'violencias','4.4':'m4-ciclo-respuesta','4.5':'m4-protocolo',
  '5.1':'m5-atencion','5.2':'servicio','5.3':'m5-comunicacion','5.4':'m5-comunicacion','5.5':'accesibilidad','5.6':'competencias'
};
const PROPORTIONAL_WEIGHTS={1:9,2:24,3:6,4:4,5:7};
const ERROR_TAGS=[
  ['plazo','Plazo o número'],['organo','Órgano o competencia'],['condicion','Condición o excepción'],['lectura','Lectura rápida del enunciado']
];

function sourceLink(value){const source=String(value??''),parts=source.split('|'),first=parts[0].trim(),web=source.match(/https?:\/\/[^\s|]+/g),page=first.match(/#page=(\d+)/);let out='';if(allowed(first))out='<a class="source-link" href="'+safe(first)+'" target="_blank" rel="noopener">'+(page?'Abrir PDF · página '+page[1]:'Consultar fuente')+' ↗</a>';else if(/^Texto original/i.test(first))out='<a class="source-link" href="#readingText">Volver al texto de práctica ↑</a>';if(web?.length&&web[0]!==first)out+='<a class="source-link" href="'+safe(web[0])+'" target="_blank" rel="noopener">Fuente oficial en línea ↗</a>';const caption=parts.slice(1).join(' · ').replace(/(?:URL\s*)?https?:\/\/[^\s|]+/g,'').trim();return out+'<span class="source-caption">'+safe(caption||(!allowed(first)?source:''))+'</span>'}
function questionSources(q){
  if(q.sources?.length){
    return q.sources.map(s=>sourceLink((s.file||'')+(s.page?'#page='+s.page:'')+' | '+(s.label||'Fuente oficial'))).join('');
  }
  const primary=q.fuentes?.length>1?q.fuentes.map(f=>sourceLink(f.archivo+'#page='+f.pagina+' | '+(f.descripcion||'Fuente del concepto')+(f.url?' | '+f.url:''))).join(''):sourceLink(q.fuente);
  return primary+(q.referencias_adicionales||[]).map(r=>allowed(r.url)?'<a class="source-link" href="'+safe(r.url)+'" target="_blank" rel="noopener">'+safe(r.label)+' ↗</a>'+(r.oficial&&allowed(r.oficial)?'<a class="source-link" href="'+safe(r.oficial)+'" target="_blank" rel="noopener">Norma oficial en línea ↗</a>':''):'').join('');
}
function bridgeLinks(modulo,subtema){
  if(!modulo||!subtema)return '';
  const baseTopic=String(subtema).split('.').slice(0,2).join('.');
  const mapId=TOPIC_MAP[baseTopic]||('m'+modulo);
  return '<div class="bridge-links"><button type="button" class="bridge-btn" data-practice-topic="'+safe(baseTopic)+'" data-practice-mod="'+safe(modulo)+'">Practicar '+safe(baseTopic)+'</button><a class="bridge-btn" href="memoria.html#map='+safe(mapId)+'">Mapa '+safe(baseTopic)+' ↗</a><a class="bridge-btn" href="taller.html?module='+safe(modulo)+'&topic='+safe(baseTopic)+'">Taller '+safe(baseTopic)+' ↗</a></div>';
}
function markdown(text){const inline=s=>safe(s).replace(/\[([^\]]+)\]\(([^)]+)\)/g,(_,label,url)=>{const clean=url.replace(/^historico-prepublicacion\//,'historico/prepublicacion/');return allowed(clean)?'<a href="'+clean+'"'+(/\.md(?:#|$)/i.test(clean)||/^(?:memoria|taller|index)\.html/i.test(clean)?'':' target="_blank" rel="noopener"')+'>'+label+'</a>':label+' ('+url+')'}).replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/`([^`]+)`/g,'<code>$1</code>');let table=false;const out=[],toc=[];let headingCount=0;for(const line of text.split('\n')){if(line.startsWith('|')){if(!table){out.push('<div style="overflow-x:auto"><table>');table=true}if(!/^\|[\s:|\-]+\|$/.test(line))out.push('<tr>'+line.split('|').slice(1,-1).map(c=>'<td>'+inline(c.trim())+'</td>').join('')+'</tr>');continue}if(table){out.push('</table></div>');table=false}const h=line.match(/^(#{1,6})\s+(.+)/);if(h){const level=Math.min(h[1].length+1,6),id='heading-'+headingCount++;if(h[1].length===2)toc.push('<a href="#'+id+'">'+inline(h[2])+'</a>');out.push('<h'+level+' id="'+id+'">'+inline(h[2])+'</h'+level+'>')}else if(/^[-*] /.test(line))out.push('<p style="margin:7px 0 7px 16px">• '+inline(line.slice(2))+'</p>');else if(/^> ?/.test(line))out.push('<blockquote>'+inline(line.replace(/^> ?/,''))+'</blockquote>');else if(line.trim())out.push('<p>'+inline(line)+'</p>')}if(table)out.push('</table></div>');return (toc.length?'<nav class="toc" aria-label="Apartados del documento">'+toc.join('')+'</nav>':'')+out.join('')}
function ask(message){return new Promise(resolve=>{const dialog=document.createElement('dialog');dialog.innerHTML='<p>'+safe(message)+'</p><div class="bar"><button data-answer="no">Cancelar</button><button class="primary" data-answer="yes">Continuar</button></div>';document.body.append(dialog);const done=value=>{dialog.close();dialog.remove();resolve(value)};dialog.querySelector('[data-answer="no"]').onclick=()=>done(false);dialog.querySelector('[data-answer="yes"]').onclick=()=>done(true);dialog.addEventListener('cancel',e=>{e.preventDefault();done(false)});dialog.showModal()})}
function saveUiState(){
  save('pjm-ui-2026',{
    tab:currentTab,
    mode:$('mode')?.value||'estudio',
    moduleFilter:$('moduleFilter')?.value||'0',
    topicFilter:$('topicFilter')?.value||'',
    numKindFilter:$('numKindFilter')?.value||'',
    examMinutes:$('examMinutes')?.value||'50',
    examDistribution:$('examDistribution')?.value||'balanced',
    readerDoc:$('readerDoc')?.value||'1',
    readerPage:$('readerPage')?.value||'1',
    openDoc:currentOpenDoc,
    openDocMod:currentOpenDocMod
  });
}
function tab(name){currentTab=name;document.querySelectorAll('main>section').forEach(s=>s.classList.toggle('hide',s.id!==name));document.querySelectorAll('.sidebar [data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab===name));if(name==='historial')renderHistory();if(name==='inicio'){renderCoverage();window.scrollTo?.({top:0,behavior:'auto'});}else $(name)?.scrollIntoView({behavior:'auto',block:'start'});saveUiState()}
function showDoc(name,moduleId,anchor){const key=window.DOCUMENTOS?.[name]?name:(window.DOCUMENTOS?.['estudio-2026/'+name]?'estudio-2026/'+name:name);const doc=window.DOCUMENTOS?.[key];if(!doc)return;currentOpenDoc=key;currentOpenDocMod=moduleId||0;tab('documentos');$('catalogo').innerHTML='<article class="card"><button id="closeDoc">Cerrar lectura</button>'+markdown(doc)+'</article>';$('closeDoc').onclick=()=>{currentOpenDoc='';currentOpenDocMod=0;$('catalogo').innerHTML='';saveUiState()};$('catalogo').scrollIntoView({behavior:'auto'});$('catalogo').focus({preventScroll:true});if(moduleId){const target=[...($('catalogo').querySelectorAll?.('h3')||[])].find(h=>h.textContent.startsWith('Módulo '+moduleId+'.'));if(target)target.scrollIntoView({behavior:'auto'})}else if(anchor){const slug=normStr(anchor.replace(/^#/,'')).replace(/[^a-z0-9]+/g,'');const target=[...($('catalogo').querySelectorAll?.('h2,h3,h4')||[])].find(h=>normStr(h.textContent).replace(/[^a-z0-9]+/g,'').includes(slug));if(target)target.scrollIntoView({behavior:'auto'})}}
document.addEventListener('click',e=>{
  const tabButton=e.target.closest('[data-tab]'),docButton=e.target.closest('[data-doc]'),readerButton=e.target.closest('[data-reader]'),pracButton=e.target.closest('[data-practice-topic]'),numButton=e.target.closest('[data-practice-num]'),a=e.target.closest('a');
  if(tabButton){tab(tabButton.dataset.tab);return}
  if(docButton){showDoc(docButton.dataset.doc,Number(docButton.dataset.module));return}
  if(readerButton){openReader(Number(readerButton.dataset.reader),1);return}
  if(pracButton){
    tab('practica');$('mode').value='estudio';updateFilters();
    $('moduleFilter').value=String(pracButton.dataset.practiceMod||'0');updateTopics();
    $('topicFilter').value=String(pracButton.dataset.practiceTopic||'');
    start();return;
  }
  if(numButton){
    tab('practica');$('mode').value='numeros';updateFilters();
    $('moduleFilter').value=String(numButton.dataset.practiceMod||'0');updateTopics();
    $('topicFilter').value=String(numButton.dataset.practiceNum||'');
    start();return;
  }
  if(a){
    const href=a.getAttribute('href')||'';
    const [base,hash]=href.split('#');
    if(base&&(window.DOCUMENTOS?.[base]||window.DOCUMENTOS?.['estudio-2026/'+base])){
      e.preventDefault();showDoc(base,0,hash);
    }
  }
});
function shuffle(arr){const out=[...arr];for(let i=out.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[out[i],out[j]]=[out[j],out[i]]}return out}
function seenQuestions(){
  const stored=read('pjm-seen-2026',{}),seen=stored&&typeof stored==='object'&&!Array.isArray(stored)?stored:{};
  const legacy={};
  for(const row of read('pjm-history',[]))for(const item of row.items||[]){
    if(!item.id)continue;
    const entry=legacy[item.id]||(legacy[item.id]={count:0,last:0});
    entry.count++;entry.last=Math.max(entry.last,Date.parse(row.fecha)||0);
  }
  for(const [id,entry] of Object.entries(legacy))if(!seen[id])seen[id]=entry;
  return seen;
}
function variedQuestions(pool,n,seen){
  return shuffle(pool).sort((a,b)=>((seen[a.id]?.count||0)-(seen[b.id]?.count||0))||((seen[a.id]?.last||0)-(seen[b.id]?.last||0))).slice(0,n);
}
function variedReading(pool,seen){
  const texts=shuffle([...new Set(pool.map(q=>q.texto))]);
  const exposure=text=>pool.filter(q=>q.texto===text).reduce((r,q)=>({count:r.count+(seen[q.id]?.count||0),last:Math.max(r.last,seen[q.id]?.last||0)}),{count:0,last:0});
  texts.sort((a,b)=>{const x=exposure(a),y=exposure(b);return x.count-y.count||x.last-y.last;});
  return pool.filter(q=>q.texto===texts[0]);
}
function normalizeNumItem(it){
  const f0=it.sources?.[0];
  const fuenteStr=f0?`${f0.file}#page=${f0.page} | ${f0.label||('M'+it.module)}`:'';
  if(it.options){
    return {...it,etapa:'numeros',modulo:it.module,subtema:it.topic,tema:`Entrenador · ${it.kind}`,pregunta:it.prompt,opciones:it.options,correcta:it.correct,explicacion:it.explanation,fuente:fuenteStr,isCloze:false};
  }
  return {...it,etapa:'numeros',modulo:it.module,subtema:it.topic,tema:`Entrenador · ${it.kind}`,pregunta:it.prompt,opciones:[it.answer],correcta:0,explicacion:it.explanation,fuente:fuenteStr,isCloze:true};
}
function updateFilters(){
  const mode=$('mode').value;
  $('studyFilters')?.classList.toggle('hide',mode!=='estudio'&&mode!=='numeros');
  $('numKindWrap')?.classList.toggle('hide',mode!=='numeros');
  $('examFilters')?.classList.toggle('hide',mode!=='especificos');
}
function updateTopics(){
  const mod=Number($('moduleFilter').value),topics=[...new Set(bank.filter(q=>q.etapa==='especificos'&&(!mod||q.modulo===mod)).flatMap(q=>[q.subtema,q.subtema?.split('.').slice(0,2).join('.')]).filter(Boolean))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true})),children={'1.2.1':'Poder Legislativo','1.2.2':'Poder Ejecutivo','1.2.3':'Poder Judicial'};
  $('topicFilter').innerHTML='<option value="">Todos los apartados</option>'+topics.map(t=>{const info=modules.flatMap(m=>m.apartados||[]).find(a=>a.id===t);return '<option value="'+safe(t)+'">'+safe(t+' · '+(info?.titulo||children[t]||'Ampliación normativa'))+'</option>'}).join('');
}
function persistActiveQuiz(){
  if(finished||!current.length){try{localStorage.removeItem('pjm-active-quiz-2026')}catch{}return;}
  save('pjm-active-quiz-2026',{activeMode,activeMinutes,deadline,answers,typedAnswers,discarded,flagged,items:current.map(q=>({id:q.id,_order:q._order}))});
}
function renderOptionMarkup(q,i){
  if(q.isCloze){
    const val=typedAnswers[i]??'';
    return '<div class="cloze-row"><input type="text" class="cloze-input" data-cloze="'+i+'" value="'+safe(val)+'" placeholder="Escribí el número o término…" autocomplete="off">'+(q.unit?'<span class="muted"><strong>'+safe(q.unit)+'</strong></span>':'')+'</div>';
  }
  const order=Array.isArray(q._order)&&q._order.length===q.opciones.length?q._order:q.opciones.map((_,j)=>j);
  return order.map(origIdx=>{
    const o=q.opciones[origIdx];
    const isDisc=Boolean(discarded[i+':'+origIdx]);
    const isChecked=answers[i]===origIdx;
    return '<div class="option-row"><label class="option'+(isDisc?' discarded':'')+'" data-opt-label="'+i+':'+origIdx+'"><input type="radio" name="q'+i+'" value="'+origIdx+'"'+(isChecked?' checked':'')+'> <span>'+safe(o)+'</span></label><button type="button" class="discard-btn'+(isDisc?' active':'')+'" data-discard="'+i+':'+origIdx+'" title="Tachar / descartar opción" aria-label="Descartar opción">✕</button></div>';
  }).join('');
}
function renderOmrSheet(n,mode){
  if(!['especificos','institucional','lectura'].includes(mode))return '';
  return '<details class="omr-sheet" open><summary><strong>Grilla rápida de preguntas (OMR)</strong> · clic para saltar o revisar marcadas (⚑)</summary><div class="omr-grid" id="omrGrid">'+Array.from({length:n},(_,i)=>'<button type="button" class="omr-bubble'+(answers[i]!==undefined?' done':'')+(flagged[i]?' flagged':'')+'" data-jump-q="'+i+'">'+(i+1)+'</button>').join('')+'</div></details>';
}
function updateOmrAndProgress(){
  const n=current.length;
  const count=Object.keys(answers).length;
  if($('answered'))$('answered').textContent=count+' de '+n+' respondidas';
  if($('progress'))$('progress').value=count;
  const grid=$('omrGrid');
  if(grid?.querySelectorAll){
    grid.querySelectorAll('[data-jump-q]').forEach(btn=>{
      const idx=Number(btn.dataset.jumpQ);
      btn.classList.toggle('done',answers[idx]!==undefined);
      btn.classList.toggle('flagged',Boolean(flagged[idx]));
    });
  }
  persistActiveQuiz();
}
function bindExamEvents(mode){
  const n=current.length;
  current.forEach((q,i)=>{
    document.querySelectorAll('[name="q'+i+'"]').forEach(el=>el.addEventListener('change',()=>{
      answers[i]=Number(el.value);
      updateOmrAndProgress();
    }));
  });
  document.querySelectorAll?.('[data-cloze]')?.forEach(inp=>inp.addEventListener('input',()=>{
    const i=Number(inp.dataset.cloze),q=current[i],val=inp.value;
    typedAnswers[i]=val;
    if(!val.trim()){delete answers[i];}
    else{
      const ok=(q.accept||[q.answer]).some(a=>normStr(a)===normStr(val));
      answers[i]=ok?0:-1;
    }
    updateOmrAndProgress();
  }));
  document.querySelectorAll?.('[data-discard]')?.forEach(btn=>btn.addEventListener('click',()=>{
    const key=btn.dataset.discard;
    discarded[key]=!discarded[key];
    btn.classList.toggle('active',Boolean(discarded[key]));
    const lbl=document.querySelector?.('[data-opt-label="'+key+'"]');
    lbl?.classList.toggle('discarded',Boolean(discarded[key]));
    persistActiveQuiz();
  }));
  document.querySelectorAll?.('[data-flag-q]')?.forEach(btn=>btn.addEventListener('click',()=>{
    const idx=Number(btn.dataset.flagQ);
    flagged[idx]=!flagged[idx];
    btn.classList.toggle('flagged',Boolean(flagged[idx]));
    btn.textContent=flagged[idx]?'⚑ Marcada para revisar':'⚑ Marcar duda';
    updateOmrAndProgress();
  }));
  document.querySelectorAll?.('[data-jump-q]')?.forEach(btn=>btn.addEventListener('click',()=>{
    const target=$('q-card-'+btn.dataset.jumpQ);
    target?.scrollIntoView({behavior:'smooth',block:'start'});
  }));
  if($('finish'))$('finish').onclick=async()=>{if(Object.keys(answers).length<n&&!(await ask('Hay preguntas sin responder. ¿Terminar igualmente?')))return;finish(mode)};
}
function renderActiveExam(selectionNote){
  const n=current.length,mode=activeMode;
  const questionsHtml=current.map((q,i)=>'<fieldset class="question" id="q-card-'+i+'"><legend>'+(i+1)+'. '+safe(q.pregunta)+'</legend><p class="question-meta"><span>'+safe(q.modulo?'Módulo '+q.modulo+' · '+q.subtema+' · '+q.tema:q.tema)+'</span><button type="button" class="flag-btn'+(flagged[i]?' flagged':'')+'" data-flag-q="'+i+'">'+(flagged[i]?'⚑ Marcada para revisar':'⚑ Marcar duda')+'</button></p>'+renderOptionMarkup(q,i)+(q.trap&&mode==='estudio'?'<div class="trap-box"><strong>Cuidado con la trampa:</strong> '+safe(q.trap)+'</div>':'')+(mode==='estudio'||mode==='numeros'?'<details><summary>Profundizar en la fuente</summary>'+questionSources(q)+'</details>':'')+'</fieldset>').join('');
  const bodyHtml=mode==='lectura'
    ?'<div class="reading-split"><article class="card reading-pane"><h3>Texto de práctica original</h3><div class="text" id="readingText">'+safe(current[0].texto)+'</div></article><div class="reading-questions">'+questionsHtml+'</div></div>'
    :questionsHtml;
  $('exam').innerHTML='<p class="notice" role="status">'+safe(selectionNote)+'</p><div class="exam-bar"><strong id="answered">'+Object.keys(answers).length+' de '+n+' respondidas</strong><span id="paceInfo" class="pace-chip'+(deadline?'':' hide')+'"></span><span id="clock" class="timer"></span></div><progress id="progress" max="'+n+'" value="'+Object.keys(answers).length+'"></progress>'+renderOmrSheet(n,mode)+bodyHtml+'<button id="finish" class="primary">Terminar y corregir</button>';
  bindExamEvents(mode);
  if(deadline){tick(mode);timer=setInterval(()=>tick(mode),500)}else if($('clock'))$('clock').textContent='Sin reloj';
}
async function start(){
  if(current.length&&!finished&&!(await ask('¿Reiniciar esta práctica? Se perderán las respuestas actuales.')))return;
  clearInterval(timer);
  const mode=$('mode').value,seen=seenQuestions();
  let pool=bank,n=10,min=0,selectionNote='';
  if(mode==='errores'){
    const ids=read('pjm-errors',[]);
    pool=bank.filter(q=>ids.includes(q.id));
    n=pool.length;
    if(!n){$('exam').textContent='No hay errores activos guardados. Los ítems históricos retirados no se mezclan con el programa nuevo.';return}
  }else if(mode==='numeros'){
    const mod=Number($('moduleFilter').value),topic=$('topicFilter').value,kind=$('numKindFilter')?.value||'';
    pool=numBank.map(normalizeNumItem).filter(q=>(!mod||q.modulo===mod)&&(!topic||q.subtema===topic||q.subtema.startsWith(topic+'.'))&&(!kind||q.kind===kind));
    const unseen=pool.filter(q=>!seen[q.id]?.count);
    if(unseen.length){pool=unseen;selectionNote='Entrenador de precisión: ítems nuevos de números, plazos y competencias.';}
    else if(pool.length){selectionNote='Repaso de números, plazos y competencias priorizando los menos vistos.';}
    n=Math.min(12,pool.length);
  }else if(mode==='estudio'){
    const mod=Number($('moduleFilter').value),topic=$('topicFilter').value;
    pool=bank.filter(q=>q.etapa==='especificos'&&(!mod||q.modulo===mod)&&(!topic||q.subtema===topic||q.subtema.startsWith(topic+'.')));
    const unseen=pool.filter(q=>!seen[q.id]?.count);
    if(unseen.length){pool=unseen;selectionNote='Sólo preguntas sin exposición registrada en este navegador.';}
    else if(pool.length)selectionNote='Ya viste todas las preguntas de esta selección. Esta vuelta prioriza las menos vistas y más antiguas; podés ampliar el apartado para encontrar nuevas.';
    n=Math.min(10,pool.length);
  }else{
    pool=bank.filter(q=>q.etapa===mode);
    n={especificos:50,institucional:20,lectura:10}[mode];
    min={especificos:Number($('examMinutes').value)||50,institucional:15,lectura:30}[mode];
    if(mode==='lectura'&&pool.length){pool=variedReading(pool,seen)}
  }
  if(!n||pool.length<n){$('exam').textContent='No hay suficientes preguntas para esta selección. Elegí otro apartado.';return}
  if(mode==='especificos'&&$('examDistribution').value==='balanced'){
    const chosen=modules.flatMap(m=>variedQuestions(pool.filter(q=>q.modulo===m.id),10,seen));
    if(chosen.length!==50){$('exam').textContent='Faltan preguntas para una distribución de diez por módulo.';return}
    current=shuffle(chosen);
  }else if(mode==='especificos'&&$('examDistribution').value==='proportional'){
    const chosen=modules.flatMap(m=>variedQuestions(pool.filter(q=>q.modulo===m.id),PROPORTIONAL_WEIGHTS[m.id]||10,seen));
    if(chosen.length!==50){$('exam').textContent='Faltan preguntas para la distribución proporcional.';return}
    current=shuffle(chosen);
  }else{
    current=mode==='errores'?shuffle(pool).slice(0,n):variedQuestions(pool,n,seen);
  }
  current=current.map(q=>({...q,_order:q.isCloze?[0]:shuffle(q.opciones.map((_,j)=>j))}));
  const fresh=current.filter(q=>!seen[q.id]?.count).length;
  if(mode!=='estudio'&&mode!=='numeros')selectionNote=mode==='errores'?'Repaso intencional de errores guardados.':fresh+' preguntas sin exposición registrada · '+(n-fresh)+' ya vistas. Se prioriza material nuevo; las repeticiones necesarias mantienen el tamaño y formato del examen.';
  const shownAt=Date.now();
  current.forEach(q=>{seen[q.id]={count:(seen[q.id]?.count||0)+1,last:shownAt};});
  save('pjm-seen-2026',seen);
  answers={};typedAnswers={};discarded={};flagged={};finished=false;activeMode=mode;activeMinutes=min;deadline=min?Date.now()+min*60000:null;
  $('resumeBanner')?.classList.add('hide');
  persistActiveQuiz();
  renderActiveExam(selectionNote);
  $('exam').scrollIntoView({behavior:'auto'});
}
function tick(mode){
  if(finished)return;
  const remaining=Math.max(0,Math.ceil((deadline-Date.now())/1000));
  $('clock').textContent=String(Math.floor(remaining/60)).padStart(2,'0')+':'+String(remaining%60).padStart(2,'0');
  if($('paceInfo')&&activeMinutes>0&&current.length>0){
    const totalSec=activeMinutes*60,elapsed=Math.max(0,totalSec-remaining);
    const expectedQ=Math.min(current.length,Math.max(1,Math.ceil((elapsed/totalSec)*current.length)));
    $('paceInfo').textContent=`Ritmo: pregunta ${expectedQ} de ${current.length}`;
  }
  if(!remaining)finish(mode);
}
function finish(mode){
  if(finished)return;
  finished=true;clearInterval(timer);
  try{localStorage.removeItem('pjm-active-quiz-2026')}catch{}
  const score=current.filter((q,i)=>answers[i]===q.correcta).length,missing=current.filter((q,i)=>answers[i]===undefined).length;
  const errors=new Set(read('pjm-errors',[]));
  const errMeta=read('pjm-error-meta-2026',{});
  current.forEach((q,i)=>{
    if(q.etapa==='numeros')return;
    if(answers[i]===q.correcta){
      errors.delete(q.id);
      if(errMeta[q.id]){errMeta[q.id].streak=(errMeta[q.id].streak||0)+1;}
    }else if(answers[i]!==undefined || missing<=3){
      errors.add(q.id);
      errMeta[q.id]={...(errMeta[q.id]||{}),fails:((errMeta[q.id]?.fails)||0)+1,streak:0,last:Date.now()};
    }
  });
  save('pjm-errors',[...errors]);
  save('pjm-error-meta-2026',errMeta);
  const rows=read('pjm-history',[]);
  rows.unshift({version:2026,fecha:new Date().toISOString(),tipo:mode,minutos:activeMinutes,aciertos:score,total:current.length,sinResponder:missing,items:current.map((q,i)=>({id:q.id,modulo:q.modulo,subtema:q.subtema,correcta:answers[i]===q.correcta}))});
  save('pjm-history',rows);
  const threshold={especificos:35,institucional:15,lectura:7}[mode];
  $('exam').innerHTML='<article class="card"><p class="eyebrow">Corrección de práctica</p><div class="result">'+score+' / '+current.length+'</div><p>'+(score/current.length*10).toFixed(1)+' / 10 en esta práctica · '+missing+' sin responder.</p><p>'+(threshold?(score>=threshold?'Alcanzaste':'No alcanzaste')+' el mínimo de referencia ('+threshold+').':'Repaso completado; priorizá entender cada error.')+'</p><p class="muted">No acredita aprobación oficial. Abrí la página de origen y explicá la regla con tus palabras.</p><button onclick="window.print()">Imprimir corrección</button></article>'+(mode==='lectura'?'<article class="card" id="readingText"><h3>Texto de práctica original</h3><div class="text">'+safe(current[0].texto)+'</div></article>':'')+current.map((q,i)=>{
    const isOk=answers[i]===q.correcta;
    const userAns=q.isCloze?(typedAnswers[i]?.trim()?safe(typedAnswers[i]):'Sin responder'):(answers[i]===undefined?'Sin responder':safe(q.opciones[answers[i]]));
    const rightAns=q.isCloze?safe(q.answer+(q.unit?' '+q.unit:'')):safe(q.opciones[q.correcta]);
    const savedReason=errMeta[q.id]?.reason||'';
    const tagRow=!isOk?'<div class="error-tags"><span>¿Por qué falló?</span>'+ERROR_TAGS.map(([k,lbl])=>'<button type="button" class="error-tag-btn'+(savedReason===k?' active':'')+'" data-err-id="'+safe(q.id)+'" data-err-tag="'+k+'">'+safe(lbl)+'</button>').join('')+'</div>':'';
    return '<article class="question '+(isOk?'correct':'incorrect')+'"><p class="question-meta">'+safe(q.modulo?'Módulo '+q.modulo+' · '+q.subtema+' · '+q.tema:q.tema)+'</p><strong>'+(i+1)+'. '+safe(q.pregunta)+'</strong><p>Tu respuesta: '+userAns+'<br><strong>Respuesta correcta: '+rightAns+'</strong></p><p>'+safe(q.explicacion)+'</p>'+(q.trap?'<div class="trap-box"><strong>Trampa frecuente:</strong> '+safe(q.trap)+'</div>':'')+questionSources(q)+bridgeLinks(q.modulo,q.subtema)+tagRow+'</article>';
  }).join('');
  document.querySelectorAll?.('[data-err-tag]')?.forEach(btn=>btn.addEventListener('click',()=>{
    const qid=btn.dataset.errId,tag=btn.dataset.errTag,meta=read('pjm-error-meta-2026',{});
    meta[qid]={...(meta[qid]||{}),reason:tag};
    save('pjm-error-meta-2026',meta);
    btn.parentElement?.querySelectorAll('[data-err-tag]').forEach(b=>b.classList.toggle('active',b===btn));
  }));
  renderCoverage();
  $('exam').scrollIntoView({behavior:'auto'});
}
function renderHistory(){
  const rows=read('pjm-history',[]),errMeta=read('pjm-error-meta-2026',{});
  $('history').innerHTML=rows.length?rows.map(r=>'<article class="card"><strong>'+safe(r.tipo)+' · '+r.aciertos+'/'+r.total+'</strong><p>'+safe(new Date(r.fecha).toLocaleString('es-AR'))+' · '+r.sinResponder+' sin responder'+(r.minutos?' · '+r.minutos+' minutos':'')+'</p><p class="muted">'+(r.version===2026?'Preparación actualizada 2026':'Resultado conservado de la preparación anterior')+'</p></article>').join(''):'<article class="card">Todavía no hay prácticas completas. Podés empezar por un módulo sin reloj.</article>';
  const items=rows.filter(r=>r.version===2026).flatMap(r=>r.items||[]);
  const reasons=Object.values(errMeta).reduce((acc,x)=>{if(x.reason)acc[x.reason]=(acc[x.reason]||0)+1;return acc},{});
  const reasonSummary=Object.keys(reasons).length?'<p class="muted">Motivos de error etiquetados: '+ERROR_TAGS.filter(([k])=>reasons[k]).map(([k,l])=>l+': '+reasons[k]).join(' · ')+'</p>':'';
  $('performance').innerHTML='<div class="card"><h3>Aciertos por módulo</h3><p class="muted">Incluye repeticiones. No equivale a cobertura total ni a una predicción del examen.</p>'+modules.map(m=>{const qs=items.filter(q=>q.modulo===m.id),ok=qs.filter(q=>q.correcta).length;return '<div class="performance-row"><span>M'+m.id+' · '+safe(m.corto)+'</span><progress max="'+(qs.length||1)+'" value="'+ok+'"></progress><span>'+ok+'/'+qs.length+'</span></div>'}).join('')+reasonSummary+'</div>';
}
function topicMastery(topicId){
  const rows=read('pjm-history',[]).filter(r=>r.version===2026);
  const items=rows.flatMap(r=>r.items||[]).filter(i=>i.subtema===topicId||String(i.subtema||'').startsWith(topicId+'.'));
  const taller=read('pjm-taller-2026',{}).results||[];
  const tItems=taller.filter(r=>r.topic===topicId&&['self','objective'].includes(r.assessment));
  const total=items.length+tItems.length;
  if(!total)return {cls:'',label:'Sin práctica'};
  const ok=items.filter(i=>i.correcta).length+tItems.filter(r=>r.max&&r.score/r.max>=0.75).length;
  const rate=ok/total;
  if(total>=5&&rate>=0.8)return {cls:'ok',label:`Dominado (${Math.round(rate*100)}%)`};
  if(rate>=0.6)return {cls:'mid',label:`En avance (${Math.round(rate*100)}%)`};
  return {cls:'low',label:`Reforzar (${Math.round(rate*100)}%)`};
}
function renderCoverage(){
  const checked=new Set(read('pjm-coverage-2026',[]));
  $('coverage').innerHTML=modules.map(m=>'<details style="--module:'+m.color+'"><summary>M'+m.id+' · '+safe(m.titulo)+'</summary>'+m.apartados.map(a=>{
    const st=topicMastery(a.id);
    const mapId=TOPIC_MAP[a.id]||('m'+m.id);
    return '<div class="coverage-row"><label><input type="checkbox" data-coverage="'+safe(a.id)+'" '+(checked.has(a.id)?'checked':'')+'><span>'+safe(a.id+' · '+a.titulo)+' <span class="mastery-pill '+st.cls+'">'+safe(st.label)+'</span><br><a href="'+safe(m.archivo+'#page='+a.pagina)+'" target="_blank" rel="noopener">PDF · página '+a.pagina+' ↗</a></span></label><div class="bridge-links"><button type="button" class="bridge-btn" data-practice-topic="'+safe(a.id)+'" data-practice-mod="'+m.id+'">Preguntas</button><button type="button" class="bridge-btn" data-practice-num="'+safe(a.id)+'" data-practice-mod="'+m.id+'">Plazos/N°</button><a class="bridge-btn" href="memoria.html#map='+safe(mapId)+'">Mapa ↗</a><a class="bridge-btn" href="taller.html?module='+m.id+'&topic='+safe(a.id)+'">Taller ↗</a></div></div>';
  }).join('')+'</details>').join('');
  updateCoverageSummary();
}
function updateCoverageSummary(){const checked=read('pjm-coverage-2026',[]),total=modules.reduce((s,m)=>s+m.apartados.length,0);$('coverageSummary').textContent=checked.length+' de '+total+' apartados marcados como estudiados.'}
$('coverage').addEventListener('change',e=>{if(!e.target.dataset.coverage)return;const ids=new Set(read('pjm-coverage-2026',[]));if(e.target.checked)ids.add(e.target.dataset.coverage);else ids.delete(e.target.dataset.coverage);save('pjm-coverage-2026',[...ids]);updateCoverageSummary()});
function openReader(id,page){$('readerDoc').value=String(id);$('readerPage').value=page;renderReader();tab('lector')}
function renderReader(){const doc=(sources.documentos||[]).find(d=>d.id===Number($('readerDoc').value));if(!doc)return;const page=Math.min(doc.paginas,Math.max(1,parseInt($('readerPage').value,10)||1));$('readerPage').value=page;$('readerPage').max=doc.paginas;const href=doc.archivo+'#page='+page;const frameHref=doc.archivo+'?p='+page+'#page='+page;$('pdfFrame').src=frameHref;$('readerOriginal').href=href;$('readerStatus').textContent=doc.titulo+' · página PDF '+page+' de '+doc.paginas;$('pageText').textContent=doc.textos?.[page-1]||'Esta página contiene principalmente imágenes. Consultá el PDF original.';$('readerPrev').disabled=page===1;$('readerNext').disabled=page===doc.paginas;saveUiState()}
$('readerDoc').onchange=()=>{$('readerPage').value=1;renderReader()};$('readerGo').onclick=renderReader;$('readerPage').onkeydown=e=>{if(e.key==='Enter')renderReader()};$('readerPrev').onclick=()=>{$('readerPage').value=Number($('readerPage').value)-1;renderReader()};$('readerNext').onclick=()=>{$('readerPage').value=Number($('readerPage').value)+1;renderReader()};
$('mode').onchange=()=>{updateFilters();saveUiState()};$('moduleFilter').onchange=()=>{updateTopics();saveUiState()};if($('topicFilter'))$('topicFilter').onchange=saveUiState;if($('numKindFilter'))$('numKindFilter').onchange=saveUiState;if($('examMinutes'))$('examMinutes').onchange=saveUiState;if($('examDistribution'))$('examDistribution').onchange=saveUiState;$('start').onclick=start;$('reviewErrors').onclick=()=>{tab('practica');$('mode').value='errores';updateFilters();start()};
$('clear').onclick=async()=>{if(await ask('¿Borrar resultados y errores? Las casillas de temas estudiados y la memoria visual se conservarán.')){save('pjm-history',[]);save('pjm-errors',[]);save('pjm-error-meta-2026',{});renderHistory();renderCoverage()}};
$('export').onclick=()=>{const blob=new Blob([JSON.stringify({resultados:read('pjm-history',[]),errores:read('pjm-errors',[]),erroresMeta:read('pjm-error-meta-2026',{}),cobertura:read('pjm-coverage-2026',[]),memoria:read('pjm-memoria-2026',{}),taller:read('pjm-taller-2026',{}),preguntasVistas:read('pjm-seen-2026',{})},null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='mis-avances-judicial-2026.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};
if($('importBtn')&&$('importFile')){
  $('importBtn').onclick=()=>$('importFile').click();
  $('importFile').onchange=async e=>{
    const file=e.target.files?.[0];if(!file)return;
    try{
      const raw=JSON.parse(await file.text());
      if(Array.isArray(raw.resultados))save('pjm-history',raw.resultados);
      if(Array.isArray(raw.errores))save('pjm-errors',raw.errores);
      if(raw.erroresMeta&&typeof raw.erroresMeta==='object')save('pjm-error-meta-2026',raw.erroresMeta);
      if(Array.isArray(raw.cobertura))save('pjm-coverage-2026',raw.cobertura);
      if(raw.memoria&&typeof raw.memoria==='object')save('pjm-memoria-2026',raw.memoria.state||raw.memoria);
      if(raw.state&&raw.format==='pjm-memoria-2026')save('pjm-memoria-2026',raw.state);
      if(raw.taller&&typeof raw.taller==='object')save('pjm-taller-2026',raw.taller);
      if(raw.preguntasVistas&&typeof raw.preguntasVistas==='object')save('pjm-seen-2026',raw.preguntasVistas);
      renderHistory();renderCoverage();
      if($('importStatus'))$('importStatus').textContent='Avances importados correctamente.';
    }catch{
      if($('importStatus'))$('importStatus').textContent='El archivo seleccionado no tiene un formato JSON válido de avances.';
    }
    e.target.value='';
  };
}
$('moduleCards').innerHTML=modules.map(m=>'<article class="module-card" style="--module:'+m.color+'"><span class="module-no">MÓDULO '+m.id+'</span><h3>'+safe(m.titulo)+'</h3><p>'+m.paginas+' páginas · '+m.apartados.length+' apartados</p><button data-module="'+m.id+'" data-doc="'+safe(m.guia)+'">Estudiar la guía</button><a href="'+safe(m.archivo)+'" target="_blank" rel="noopener">PDF oficial ↗</a></article>').join('');
const docNames=[['ACTUALIZACION-2026.md','Qué cambió y qué sigue sirviendo'],['MANUAL-DE-PREPARACION.md','Manual completo 2026'],['GUIA-CONCURSO-2026.md','Etapas y reglas del concurso'],['PLAN-DE-ESTUDIO.md','Plan de 28 sesiones'],['estudio-2026/GUIA-M1-M3.md','M1 Estado + M3 Derechos Humanos'],['estudio-2026/GUIA-M2.md','M2 Poder Judicial y fueros'],['estudio-2026/GUIA-M4-M5.md','M4 Género + M5 Atención'],['estudio-2026/GUIA-ANEXOS.md','Normativa y anexo penal juvenil'],['estudio-2026/GUIA-MAPAS-2026.md','Cómo estudiar con los mapas'],['BIBLIOTECA-Y-TEMARIO.md','Biblioteca y alcance de referencias'],['REVISION-CONTENIDO.md','Erratas y revisión de contenidos']];$('docButtons').innerHTML=docNames.map(([name,title])=>'<button data-doc="'+name+'">'+title+'</button>').join('')+'<a class="button" href="CUADERNO-DE-EJERCICIOS.html" target="_blank">Ejercicios para imprimir ↗</a>';
$('pdfList').innerHTML=(sources.documentos||[]).map(d=>'<article class="source-row"><div class="bar"><a href="'+safe(d.archivo)+'" target="_blank" rel="noopener">'+safe(d.titulo)+'</a><button data-reader="'+d.id+'">Leer acá</button></div><p>'+d.paginas+' páginas · original oficial</p></article>').join('');$('referenceList').innerHTML=(sources.referencias||[]).map(r=>'<article class="source-row">'+(r.archivo?'<a href="'+safe(r.lectura||r.archivo)+'" target="_blank" rel="noopener">'+safe(r.titulo)+'</a>':'<strong>'+safe(r.titulo)+'</strong>')+'<p>'+safe(r.alcance)+(r.error?' · Descarga pendiente: '+safe(r.error):'')+'</p></article>').join('');$('readerDoc').innerHTML=(sources.documentos||[]).map(d=>'<option value="'+d.id+'">'+safe(d.titulo)+'</option>').join('');$('moduleFilter').innerHTML='<option value="0">Todos los módulos</option>'+modules.map(m=>'<option value="'+m.id+'">M'+m.id+' · '+safe(m.corto)+'</option>').join('');
renderCoverage();renderReader();updateTopics();updateFilters();if(bank.length){$('bankStatus').textContent=bank.filter(q=>q.etapa==='especificos').length+' preguntas específicas 2026 + '+numBank.length+' ítems de plazos y números + '+bank.filter(q=>q.etapa!=='especificos').length+' ejercicios generales de lectura e institucionales.';$('start').disabled=false}else $('bankStatus').textContent='Falta el banco de preguntas. Conservá datos-preguntas.js junto a este archivo.';
(function checkSavedQuizAndParams(){
  const savedUi=read('pjm-ui-2026',null);
  if(savedUi&&typeof savedUi==='object'){
    if(savedUi.mode&&$('mode'))$('mode').value=savedUi.mode;
    if(savedUi.moduleFilter&&$('moduleFilter')){$('moduleFilter').value=savedUi.moduleFilter;updateTopics();}
    if(savedUi.topicFilter!==undefined&&$('topicFilter'))$('topicFilter').value=savedUi.topicFilter;
    if(savedUi.numKindFilter!==undefined&&$('numKindFilter'))$('numKindFilter').value=savedUi.numKindFilter;
    if(savedUi.examMinutes&&$('examMinutes'))$('examMinutes').value=savedUi.examMinutes;
    if(savedUi.examDistribution&&$('examDistribution'))$('examDistribution').value=savedUi.examDistribution;
    updateFilters();
    if(savedUi.readerDoc&&$('readerDoc')){$('readerDoc').value=savedUi.readerDoc;if(savedUi.readerPage)$('readerPage').value=savedUi.readerPage;renderReader();}
    if(savedUi.openDoc)showDoc(savedUi.openDoc,savedUi.openDocMod||0);
    if(savedUi.tab)tab(savedUi.tab);
  }
  const savedQuiz=read('pjm-active-quiz-2026',null);
  if(savedQuiz&&Array.isArray(savedQuiz.items)&&savedQuiz.items.length){
    const allPool=[...bank,...numBank.map(normalizeNumItem)];
    const restored=savedQuiz.items.map(it=>{const found=allPool.find(q=>q.id===it.id);return found?{...found,_order:it._order}:null}).filter(Boolean);
    if(restored.length===savedQuiz.items.length){
      current=restored;answers=savedQuiz.answers||{};typedAnswers=savedQuiz.typedAnswers||{};discarded=savedQuiz.discarded||{};flagged=savedQuiz.flagged||{};
      activeMode=savedQuiz.activeMode;activeMinutes=savedQuiz.activeMinutes||0;deadline=savedQuiz.deadline||null;finished=false;
      if(deadline&&deadline<=Date.now()){
        finish(activeMode);
      }else{
        renderActiveExam('Práctica en curso recuperada automáticamente en el punto donde habías quedado.');
        if($('resumeBanner')){
          $('resumeBanner').classList.remove('hide');
          $('resumeBanner').innerHTML='<strong>Tenés una práctica en curso ('+safe(savedQuiz.activeMode)+') recuperada automáticamente.</strong> <div class="bar" style="margin-top:8px"><button type="button" id="resumeQuizBtn" class="primary">Ir a las preguntas</button><button type="button" id="discardQuizBtn">Descartar práctica</button></div>';
          if($('resumeQuizBtn'))$('resumeQuizBtn').onclick=()=>{
            $('resumeBanner').classList.add('hide');
            $('exam')?.scrollIntoView({behavior:'auto'});
          };
          if($('discardQuizBtn'))$('discardQuizBtn').onclick=()=>{
            clearInterval(timer);finished=true;current=[];answers={};typedAnswers={};discarded={};flagged={};
            try{localStorage.removeItem('pjm-active-quiz-2026')}catch{}
            $('resumeBanner').classList.add('hide');
            $('exam').innerHTML='';
          };
        }
        if(!new URLSearchParams(window.location?.search||'').get('doc'))tab('practica');
      }
    }
  }
  try{
    const params=new URLSearchParams(window.location?.search||'');
    if(params.get('doc')){showDoc(params.get('doc'));}
    else if(params.get('practiceTopic')||params.get('practiceModule')){
      tab('practica');$('mode').value=params.get('mode')||'estudio';updateFilters();
      if(params.get('module')||params.get('practiceModule')){$('moduleFilter').value=params.get('module')||params.get('practiceModule');updateTopics();}
      if(params.get('practiceTopic'))$('topicFilter').value=params.get('practiceTopic');
      start();
    }
  }catch{}
})();
