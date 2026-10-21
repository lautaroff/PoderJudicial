(() => {
  'use strict';
  const data=window.TALLER;
  const $=id=>document.getElementById(id),KEY='pjm-taller-2026',DAY=86400000;
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  if(!data){$('counts').textContent='Faltan los datos del taller. Conservá taller-datos.js junto a esta página.';return;}
  const labels={open:'Explicar sin opciones',cases:'Comparar casos',sequences:'Ordenar procesos',errors:'Buscar el error',diagnostics:'Diagnósticos reservados',videos:'Jornadas de video',results:'Resultados y repasos'};
  const modules=Object.fromEntries(data.modules.map(m=>[m.id,m]));
  let state={version:1,seen:{},results:[],drafts:{},videoNotes:{},ui:{},active:null},view='open',exercise=null,timer=null,videoStage=null,ttsEnabled=false,lastSpokenScene=-1;
  try{
    const saved=JSON.parse(localStorage.getItem(KEY)||'null');
    if(saved&&typeof saved==='object'&&!Array.isArray(saved)){
      state={
        version:1,
        seen:saved.seen&&typeof saved.seen==='object'?saved.seen:{},
        results:Array.isArray(saved.results)?saved.results:[],
        drafts:saved.drafts&&typeof saved.drafts==='object'?saved.drafts:{},
        videoNotes:saved.videoNotes&&typeof saved.videoNotes==='object'?saved.videoNotes:{},
        ui:saved.ui&&typeof saved.ui==='object'?saved.ui:{},
        active:saved.active||null
      };
    }
  }catch{}
  function dueMidnight(days){const d=new Date();d.setHours(0,0,0,0);d.setDate(d.getDate()+days);return d.getTime();}
  function stopSpeech(){try{if(typeof window!=='undefined'&&window.speechSynthesis)window.speechSynthesis.cancel();}catch{}}
  function speakText(text){
    try{
      if(!ttsEnabled||typeof window==='undefined'||!window.speechSynthesis||!window.SpeechSynthesisUtterance)return;
      window.speechSynthesis.cancel();
      const u=new window.SpeechSynthesisUtterance(text);
      u.lang='es-AR';
      u.rate=1.02;
      window.speechSynthesis.speak(u);
    }catch{}
  }
  function latestFreeResults(){
    const seen=new Set(),out=[];
    for(const r of state.results){
      if(!['open','cases','sequences','errors'].includes(r.kind))continue;
      const k=r.kind+':'+r.id;
      if(!seen.has(k)){seen.add(k);out.push(r);}
    }
    return out;
  }
  function syncUiState(){
    state.ui={
      view,
      module:$('module')?.value||'all',
      topic:$('topic')?.value||'all',
      exercise:$('exercise')?.value||'',
      diagMinutes:$('diagMinutes')?.value||'50',
      ttsEnabled,
      videoStage:videoStage?{id:videoStage.id,mode:videoStage.mode}:null
    };
  }
  function save(){syncUiState();try{localStorage.setItem(KEY,JSON.stringify(state));$('storageNotice').textContent='Guardado automáticamente en este navegador. Descargá una copia para conservar tus respuestas.';}catch{$('storageNotice').textContent='El navegador no permite guardar. Podés descargar tus avances mientras la página siga abierta.';}}
  function confirmAction(message){return new Promise(resolve=>{const dialog=$('confirmDialog');$('confirmText').textContent=message;const done=v=>{dialog.close();$('confirmNo').onclick=null;$('confirmYes').onclick=null;dialog.oncancel=null;resolve(v);};$('confirmNo').onclick=()=>done(false);$('confirmYes').onclick=()=>done(true);dialog.oncancel=e=>{e.preventDefault();done(false);};dialog.showModal();});}
  function sources(items){return '<div class="sources">'+(items||[]).map(s=>{const file=s.file||modules[s.module]?.file;if(!file||!/^(biblioteca\/|videos\/|https:\/\/)/.test(file))return '';const href=file+(s.page?'#page='+s.page:s.time!==undefined?'#t='+s.time:'');return '<a href="'+esc(href)+'" target="_blank" rel="noopener">'+esc(s.label||'Fuente')+(s.page?' · PDF p. '+s.page:s.time!==undefined?' · '+formatSeconds(s.time):'')+' ↗</a>';}).join('')+'</div>';}
  const date=t=>new Date(t).toLocaleString('es-AR',{dateStyle:'short',timeStyle:'short'});
  function formatSeconds(s){return String(Math.floor(s/60)).padStart(2,'0')+':'+String(Math.floor(s%60)).padStart(2,'0');}
  function shuffle(items){const a=[...items];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
  function buildOptionOrders(questions){return Object.fromEntries((questions||[]).map(q=>[q.id,shuffle(q.options.map((_,i)=>i))]));}
  function markSeen(key){const old=state.seen[key],entry={firstOpened:old?.firstOpened||Date.now(),opens:(Number(old?.opens)||0)+1};state.seen[key]=entry;save();return Boolean(old);}
  function setView(next,preferredExercise){stopSpeech();view=next;const free=['open','cases','sequences','errors'].includes(next);document.querySelectorAll('[data-view]').forEach(b=>{const active=b.dataset.view===view;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});for(const id of ['practice','diagnostics','videos','results'])$(id).hidden=id!==(free?'practice':next);if(free)refreshExercises(preferredExercise);if(next==='diagnostics')renderDiagnosticMenu();if(next==='videos')renderVideoMenu();if(next==='results')renderResults();save();$(free?'practice':view)?.scrollIntoView({behavior:'auto',block:'start'});}
  async function navigate(next){if(state.active&&next!==(state.active.kind==='video'?'videos':'diagnostics')){if(!(await confirmAction('Hay un cuestionario en curso. Podés volver después: el reloj seguirá corriendo. ¿Cambiar de sección?')))return;}setView(next);}
  const pool=()=>data[view]||[];
  function refreshExercises(preferred){const module=$('module').value,oldTopic=$('topic').value,topics=[...new Set(pool().filter(x=>module==='all'||String(x.module)===module).map(x=>x.topic))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));$('topic').innerHTML='<option value="all">Todos los apartados</option>'+topics.map(t=>'<option value="'+esc(t)+'">'+esc(t)+'</option>').join('');$('topic').value=topics.includes(oldTopic)?oldTopic:'all';const topic=$('topic').value,items=pool().filter(x=>(module==='all'||String(x.module)===module)&&(topic==='all'||x.topic===topic));$('exercise').innerHTML=items.map(x=>'<option value="'+esc(x.id)+'">'+esc('M'+x.module+' · '+x.topic+' · '+x.title)+'</option>').join('');if(preferred&&items.some(x=>x.id===preferred))$('exercise').value=preferred;showExercise();}
  function selected(){return pool().find(x=>x.id===$('exercise').value);}
  function badge(item){return '<span class="module-tag">M'+item.module+' · '+esc(modules[item.module].title)+' · '+esc(item.topic)+'</span>';}
  function confidence(name,value){return '<div class="confidence"><span>Antes de corregir, mi seguridad:</span>'+[['high','Alta'],['medium','Media'],['low','Baja']].map(([v,l])=>'<label><input type="radio" name="'+name+'" value="'+v+'" '+(v===value?'checked':'')+'>'+l+'</label>').join('')+'</div>';}
  function draftFor(item){const key=view+':'+item.id;if(!state.drafts[key])state.drafts[key]={id:item.id,kind:view,started:Date.now(),texts:{},confidence:'',committed:false,rating:{}};return state.drafts[key];}
  function textarea(id,label,text,disabled){return '<label class="answer-label" for="'+id+'">'+label+'</label><textarea id="'+id+'" '+(disabled?'disabled':'')+' placeholder="Escribí tu respuesta o resumí lo que explicaste en voz alta.">'+esc(text||'')+'</textarea>';}
  function showExercise(){exercise=selected();if(!exercise){$('workarea').innerHTML='<p>No hay ejercicios en esta selección.</p>';return;}const item=exercise,draft=draftFor(item);$('workarea').style.setProperty('--accent',modules[item.module].color);let body='';
    if(view==='cases')body='<article class="paper">'+badge(item)+'<h2>'+esc(item.title)+'</h2><p>Respondé ambos casos antes de mirar la comparación. Identificá el dato que cambia la decisión.</p></article><div class="comparison">'+[['a','Caso A'],['b','Caso B']].map(([key,title])=>'<article class="paper"><h3>'+title+'</h3><div class="bodytext">'+esc(item[key].text)+'</div><p class="prompt">'+esc(item[key].prompt)+'</p>'+textarea('answer-'+key,'Tu respuesta al '+title,draft.texts[key],draft.committed)+'</article>').join('')+'</div>';
    else if(view==='sequences'){if(!draft.order)draft.order=shuffle(item.steps.map(s=>s.id));body='<article class="paper">'+badge(item)+'<h2>'+esc(item.title)+'</h2><p class="notice">'+esc(item.scope)+'</p><p class="prompt">'+esc(item.prompt)+'</p><ol class="sequence">'+draft.order.map((id,i)=>{const step=item.steps.find(s=>s.id===id);return '<li><span class="number">'+(i+1)+'</span><span class="step-text">'+esc(step.text)+'</span><span class="moves"><button data-move="up" data-index="'+i+'" aria-label="Subir paso '+(i+1)+'" '+(draft.committed||!i?'disabled':'')+'>↑</button><button data-move="down" data-index="'+i+'" aria-label="Bajar paso '+(i+1)+'" '+(draft.committed||i===draft.order.length-1?'disabled':'')+'>↓</button></span></li>';}).join('')+'</ol>'+textarea('answer-main','Explicá el orden y el acto desde el que corre el plazo, si corresponde',draft.texts.main,draft.committed)+'</article>';}
    else body='<article class="paper">'+badge(item)+'<h2>'+esc(item.title)+'</h2><p class="prompt">'+esc(item.prompt)+'</p>'+(view==='errors'?'<div class="flawed">'+esc(item.flawed)+'</div>':'')+textarea('answer-main',view==='errors'?'Identificá el error, corregilo y justificá':'Tu explicación sin opciones',draft.texts.main,draft.committed)+'</article>';
    body+='<article class="paper">'+(draft.committed?'<p class="chip">Primera respuesta conservada · '+date(draft.committedAt)+'</p>':confidence('free-confidence',draft.confidence)+'<button id="commit" class="primary">Conservar respuesta y ver corrección</button><p class="muted">Después de revelar, tu respuesta inicial queda fija. Para un nuevo intento podés comenzar otra vuelta; se registrará como repetición.</p>');if(draft.committed)body+=renderModel(item,draft);body+='</article>';$('workarea').innerHTML=body;
    $('workarea').querySelectorAll('textarea').forEach(el=>el.addEventListener('input',()=>{draft.texts[el.id.replace('answer-','')]=el.value;save();}));
    $('workarea').querySelectorAll('[name="free-confidence"]').forEach(el=>el.onchange=()=>{draft.confidence=el.value;save();});
    $('workarea').querySelectorAll('[data-move]').forEach(button=>button.onclick=()=>{
      const index=Number(button.dataset.index),dir=button.dataset.move,to=index+(dir==='up'?-1:1);
      [draft.order[index],draft.order[to]]=[draft.order[to],draft.order[index]];
      save();showExercise();
      const sameDir=$('workarea').querySelector?.(`[data-index="${to}"][data-move="${dir}"]`);
      const anyDir=$('workarea').querySelector?.(`[data-index="${to}"][data-move]`);
      const targetBtn=(sameDir&&!sameDir.disabled)?sameDir:anyDir;
      targetBtn?.focus?.();
    });
    if($('commit'))$('commit').onclick=()=>commitFree(item,draft);if($('save-rating'))$('save-rating').onclick=()=>saveRating(item,draft);if($('new-attempt'))$('new-attempt').onclick=async()=>{if(await confirmAction('La respuesta anterior seguirá en resultados. ¿Comenzar otro intento de este ejercicio?')){delete state.drafts[view+':'+item.id];save();showExercise();}};$('workarea').querySelectorAll('[data-rating]').forEach(el=>el.onchange=()=>{draft.rating[el.dataset.rating]=el.value;save();});save();}
  function criteria(item){if(view==='cases')return [['a',item.a],['b',item.b]].flatMap(([prefix,x])=>x.checkpoints.map(c=>({...c,id:prefix+':'+c.id,text:'Caso '+prefix.toUpperCase()+': '+c.text})));return item.checkpoints||[];}
  function renderModel(item,draft){let out='<h3>Comparar con la respuesta de referencia</h3>';if(view==='cases')out+=[['a','A'],['b','B']].map(([k,l])=>'<h4>Caso '+l+'</h4><div class="model">'+esc(item[k].model)+'</div>'+sources(item[k].sources)).join('')+'<p><strong>Dato que cambia:</strong> '+esc(item.changed)+'</p><p>'+esc(item.keyDifference)+'</p>'+sources(item.sources);else if(view==='sequences'){const matches=draft.order.filter((id,i)=>id===item.correct[i]).length;out+='<p><strong>'+matches+' de '+item.correct.length+' pasos en su posición.</strong> Ese dato no califica tu explicación.</p><ol>'+item.correct.map(id=>'<li>'+esc(item.steps.find(s=>s.id===id).text)+'</li>').join('')+'</ol><div class="model">'+esc(item.explanation)+'</div>'+item.links.map(l=>'<p>'+esc(l.because)+'</p>').join('')+sources(item.sources)+'<p class="muted">Compará tu justificación con estos vínculos. No se interpreta la coincidencia de orden como dominio de todas las excepciones.</p>';}else out+='<div class="model">'+esc(item.model)+'</div>'+(item.explanation?'<p>'+esc(item.explanation)+'</p>':'')+sources(item.sources);
    const points=criteria(item);if(points.length)out+='<h3>Rúbrica de autoevaluación</h3><p class="muted">Marcá cada criterio después de contrastar tu primera respuesta. Una frase parecida no basta si cambia el órgano, la condición o la excepción.</p>'+points.map(c=>'<label class="criterion"><span>'+esc(c.text)+(c.critical?'<span class="critical">Criterio esencial: una confusión requiere repaso</span>':'')+'</span><select data-rating="'+esc(c.id)+'"><option value="">Elegir estado</option>'+[['0','Omitido / incorrecto'],['1','Parcial'],['2','Correcto y preciso']].map(([v,l])=>'<option value="'+v+'" '+(draft.rating[c.id]===v?'selected':'')+'>'+l+'</option>').join('')+'</select></label>').join('')+'<div class="bar"><button id="save-rating" class="primary">Guardar autoevaluación</button><button id="new-attempt">Comenzar otro intento</button></div>';else out+='<div class="bar"><button id="save-rating" class="primary">Registrar comparación</button><button id="new-attempt">Comenzar otro intento</button></div>';if(draft.assessed)out+='<p class="notice">Autoevaluación guardada. Próximo repaso sugerido: '+date(draft.due)+'. No equivale a una nota oficial.</p>';return out;}
  function commitFree(item,draft){const keys=view==='cases'?['a','b']:['main'];if(keys.some(k=>(draft.texts[k]||'').trim().length<15)){alertInline('Escribí al menos una explicación breve en cada respuesta antes de revelar.');return;}if(!draft.confidence){alertInline('Marcá tu seguridad antes de ver la corrección.');return;}draft.committed=true;draft.committedAt=Date.now();draft.repeat=markSeen(view+':'+item.id);const record={attemptId:item.id+'-'+draft.started,kind:view,id:item.id,module:item.module,topic:item.topic,title:item.title,started:draft.started,finished:draft.committedAt,repeat:draft.repeat,texts:{...draft.texts},confidence:draft.confidence,order:draft.order?[...draft.order]:undefined,assessment:'pending'};state.results.unshift(record);draft.attemptId=record.attemptId;save();showExercise();}
  function alertInline(message){let p=$('exercise-alert');if(!p){p=document.createElement('p');p.id='exercise-alert';p.className='notice';p.setAttribute('role','alert');$('workarea').append(p);}p.textContent=message;p.scrollIntoView({behavior:'auto'});}
  function saveRating(item,draft){const points=criteria(item);if(points.some(c=>!Object.hasOwn(draft.rating,c.id)||draft.rating[c.id]==='')){alertInline('Compará todos los criterios antes de guardar.');return;}const score=points.reduce((s,c)=>s+Number(draft.rating[c.id]),0),max=points.length*2,critical=points.filter(c=>c.critical&&Number(draft.rating[c.id])<2).length;draft.assessed=true;draft.due=dueMidnight((max&&score/max>=.85&&!critical)?3:1);const record=state.results.find(r=>r.attemptId===draft.attemptId);if(record)Object.assign(record,{assessment:'self',rating:{...draft.rating},score,max,critical,due:draft.due,positionScore:view==='sequences'?draft.order.filter((id,i)=>id===item.correct[i]).length:undefined,positionTotal:item.correct?.length});save();showExercise();}
  function completed(key){return state.results.filter(r=>r.key===key&&r.assessment==='objective');}
  function diagnosticCard(key,title,description,button,form){const seen=state.seen[key],a=completed('spec:A')[0],due=form==='B'&&a?a.finished+3*DAY:null;return '<article class="menu-card"><p class="eyebrow">'+(seen?'Exposición previa registrada':'Reservado para primera exposición')+'</p><h3>'+esc(title)+'</h3><p>'+esc(description)+'</p>'+(seen?'<p class="chip warning">Ya abierto: '+date(seen.firstOpened)+'</p>':'')+(due?'<p class="muted">Comparación diferida sugerida desde '+date(due)+'.</p>':'')+'<button class="primary" data-diagnostic="'+key+'">'+button+'</button></article>';}
  function renderDiagnosticMenu(){$('diagnostic-menu').innerHTML=data.diagnostics.forms.map(f=>diagnosticCard('spec:'+f.id,'Específicos · forma '+f.id,'50 preguntas nuevas, cuatro opciones y confianza previa. Diez por módulo, por decisión de práctica.','Iniciar forma '+f.id,f.id)).join('')+data.diagnostics.reading.map(t=>diagnosticCard('read:'+t.id,'Lectura · '+t.title,'Texto original nuevo, diez preguntas, tres opciones y treinta minutos.','Leer y responder',t.form)).join('');$('diagnostic-menu').querySelectorAll('[data-diagnostic]').forEach(b=>b.onclick=()=>startDiagnostic(b.dataset.diagnostic));if(state.active?.kind==='diagnostic')renderQuiz('diagnostic-area');else $('diagnostic-area').innerHTML='';}
  async function startDiagnostic(key){if(state.active&&!(await confirmAction('Hay un cuestionario en curso. Terminará como abandonado y se conservará la exposición. ¿Comenzar otro?')))return;if(state.active)abandonActive();const [type,id]=key.split(':'),obj=type==='spec'?data.diagnostics.forms.find(f=>f.id===id):data.diagnostics.reading.find(t=>t.id===id),a=completed('spec:A')[0],early=type==='spec'&&id==='B'&&a&&Date.now()<a.finished+3*DAY;if(early&&!(await confirmAction('Todavía no pasaron tres días desde la forma A. Podés continuar; quedará identificado como diagnóstico anticipado. ¿Iniciar B ahora?')))return;const repeat=markSeen(key),started=Date.now();state.active={kind:'diagnostic',key,type,id,started,deadline:started+(type==='spec'?Number($('diagMinutes').value):30)*60000,minutes:type==='spec'?Number($('diagMinutes').value):30,answers:{},confidence:{},repeat,early:Boolean(early),order:obj.questions.map(q=>q.id),optionOrders:buildOptionOrders(obj.questions)};save();renderQuiz('diagnostic-area');$('diagnostic-area').scrollIntoView({behavior:'auto'});}
  function activeQuestions(active){if(active.kind==='video'){const v=data.videos.find(v=>v.id===active.id);return {questions:v.questions,text:null,title:v.title};}if(active.type==='spec'){const f=data.diagnostics.forms.find(f=>f.id===active.id);return {questions:f.questions,text:null,title:'Específicos · forma '+f.id};}const t=data.diagnostics.reading.find(t=>t.id===active.id);return {questions:t.questions,text:t.text,title:'Lectura · '+t.title};}
  function renderQuiz(area){
    const active=state.active;if(!active)return;
    const info=activeQuestions(active);
    const notesNote=(active.kind==='video'&&state.videoNotes?.[active.id]?.trim())?'<details class="paper video-notes-review" open><summary><strong>Mis apuntes tomados durante el video</strong></summary><div class="preserved">'+esc(state.videoNotes[active.id])+'</div></details>':'';
    const questionsHtml=info.questions.map((q,i)=>{
      const optOrder=active.optionOrders?.[q.id]||q.options.map((_,idx)=>idx);
      const curConf=active.confidence[q.id]||'';
      return '<fieldset class="question"><legend class="qtitle">'+(i+1)+'. '+esc(q.prompt)+'</legend>'+optOrder.map(origIdx=>'<label class="option"><input type="radio" name="dq'+i+'" value="'+origIdx+'" '+(active.answers[q.id]===origIdx?'checked':'')+'><span>'+esc(q.options[origIdx])+'</span></label>').join('')+'<div class="confidence-question"><span>Mi seguridad antes de corregir:</span><div class="confidence-pills" role="group" aria-label="Seguridad en pregunta '+(i+1)+'">'+[['high','Alta'],['medium','Media'],['low','Baja / conjetura']].map(([v,l])=>'<button type="button" class="conf-pill'+(curConf===v?' active':'')+'" data-conf-q="'+esc(q.id)+'" data-conf-v="'+v+'">'+l+'</button>').join('')+'</div><select data-confidence="'+esc(q.id)+'" aria-label="Selector de seguridad pregunta '+(i+1)+'"><option value="">Sin indicar</option>'+[['high','Alta'],['medium','Media'],['low','Baja / conjetura']].map(([v,l])=>'<option value="'+v+'" '+(curConf===v?'selected':'')+'>'+l+'</option>').join('')+'</select></div></fieldset>';
    }).join('');
    const bodyHtml=info.text?'<div class="reading-split"><article class="paper" id="diagnosticText"><h3>Texto original de práctica</h3><div class="passage">'+esc(info.text)+'</div></article><div class="questions-col">'+questionsHtml+'</div></div>':questionsHtml;
    $(area).innerHTML='<div class="clockbar"><strong>'+esc(info.title)+'</strong><span id="answered">'+Object.keys(active.answers).length+' de '+info.questions.length+' respondidas</span><span id="quiz-clock" class="clock"></span></div>'+notesNote+bodyHtml+'<button id="finish-diagnostic" class="primary">Terminar y corregir</button>';
    info.questions.forEach((q,i)=>$(area).querySelectorAll('[name="dq'+i+'"]').forEach(el=>el.onchange=()=>{active.answers[q.id]=Number(el.value);$('answered').textContent=Object.keys(active.answers).length+' de '+info.questions.length+' respondidas';save();}));
    $(area).querySelectorAll('[data-confidence]').forEach(el=>el.onchange=()=>{
      const qid=el.dataset.confidence;active.confidence[qid]=el.value;
      $(area).querySelectorAll(`[data-conf-q="${qid}"]`).forEach(b=>b.classList.toggle('active',b.dataset.confV===el.value));
      save();
    });
    $(area).querySelectorAll('[data-conf-q]').forEach(btn=>btn.onclick=()=>{
      const qid=btn.dataset.confQ,val=btn.dataset.confV;
      active.confidence[qid]=val;
      const sel=$(area).querySelector(`[data-confidence="${qid}"]`);if(sel)sel.value=val;
      $(area).querySelectorAll(`[data-conf-q="${qid}"]`).forEach(b=>b.classList.toggle('active',b===btn));
      save();
    });
    $('finish-diagnostic').onclick=async()=>{const omissions=info.questions.filter(q=>active.answers[q.id]===undefined).length,noConfidence=info.questions.filter(q=>active.answers[q.id]!==undefined&&!active.confidence[q.id]).length;if((omissions||noConfidence)&&!(await confirmAction('Quedan '+omissions+' preguntas sin responder y '+noConfidence+' respuestas sin confianza indicada. ¿Terminar igualmente?')))return;finishQuiz(area,'submitted');};
    clearInterval(timer);tick(area);if(state.active)timer=setInterval(()=>tick(area),500);
  }
  function tick(area){if(!state.active)return;const remaining=Math.max(0,Math.ceil((state.active.deadline-Date.now())/1000));if($('quiz-clock'))$('quiz-clock').textContent=formatSeconds(remaining);if(!remaining)finishQuiz(area,'expired');}
  function finishQuiz(area,status){const active=state.active;if(!active)return;clearInterval(timer);const info=activeQuestions(active),items=info.questions.map(q=>({id:q.id,module:q.module,topic:q.topic,response:active.answers[q.id],confidence:active.confidence[q.id]||'',correct:active.answers[q.id]===q.correct})),score=items.filter(i=>i.correct).length,missing=items.filter(i=>i.response===undefined).length,highErrors=items.filter(i=>i.response!==undefined&&!i.correct&&i.confidence==='high').length,uncertainCorrect=items.filter(i=>i.correct&&i.confidence==='low').length;const result={attemptId:active.key+'-'+active.started,kind:active.kind,key:active.key,id:active.id,title:info.title,started:active.started,finished:Date.now(),minutes:active.minutes,repeat:active.repeat,early:active.early,supported:Boolean(active.supported),assessment:'objective',score,max:items.length,missing,highErrors,uncertainCorrect,status,items};state.results.unshift(result);state.active=null;if(result.kind!=='diagnostic')videoStage=null;save();$(area).innerHTML=quizCorrection(result,info);$(area).scrollIntoView({behavior:'auto'});if(result.kind==='diagnostic')renderDiagnosticCardsOnly();}
  function renderDiagnosticCardsOnly(){const content=$('diagnostic-area').innerHTML;renderDiagnosticMenu();$('diagnostic-area').innerHTML=content;}
  function quizCorrection(result,info){const threshold=result.key.startsWith('spec:')?35:result.key.startsWith('read:')?7:15;return '<article class="paper"><p class="eyebrow">Corrección por clave · práctica original</p><h2>'+esc(info.title)+'</h2><div class="score">'+result.score+' / '+result.max+'</div><p>'+result.missing+' sin responder · '+result.highErrors+' errores con seguridad alta · '+result.uncertainCorrect+' aciertos con seguridad baja.</p><p>'+esc(result.supported?'Estudio apoyado: pudiste consultar escenas y fuentes.':result.repeat?'Repetición: no se presenta como primera exposición.':result.early?'Primera exposición, anticipada respecto del intervalo propuesto.':'Primera exposición registrada.')+'</p><p class="muted">Mínimo de referencia del formato: '+threshold+'. Este resultado no acredita aprobación oficial ni predice tu nota.</p><button onclick="window.print()">Imprimir corrección</button></article>'+(info.text?'<article class="paper" id="diagnosticText"><h3>Texto de práctica</h3><div class="passage">'+esc(info.text)+'</div></article>':'')+info.questions.map((q,i)=>{const item=result.items[i];return '<article class="question '+(item.correct?'correct':'incorrect')+'"><p class="qtitle">'+(i+1)+'. '+esc(q.prompt)+'</p><p>Tu respuesta: '+(item.response===undefined?'Sin responder':esc(q.options[item.response]))+'</p><p><strong>Correcta: '+esc(q.options[q.correct])+'</strong></p><p>'+esc(q.why)+'</p>'+sources(q.sources)+(q.evidence?'<p class="muted">'+esc(q.evidence)+'</p><a href="#diagnosticText">Volver al pasaje ↑</a>':'')+'</article>';}).join('');}
  function abandonActive(){if(!state.active)return;const a=state.active;state.results.unshift({attemptId:a.key+'-'+a.started,kind:a.kind,key:a.key,id:a.id,title:activeQuestions(a).title,started:a.started,finished:Date.now(),repeat:a.repeat,assessment:'abandoned',status:'abandoned',answers:{...a.answers}});state.active=null;clearInterval(timer);save();}
  function renderVideoMenu(){$('video-menu').innerHTML=data.videos.map(v=>'<article class="menu-card"><p class="eyebrow">Práctica original · '+Math.round(v.duration/60)+' minutos</p><h3>'+esc(v.title)+'</h3><p>'+esc(v.description)+'</p><div class="bar"><button data-video="'+v.id+'" data-mode="study">Ver y estudiar escenas</button><button class="primary" data-video="'+v.id+'" data-mode="trial">Ensayo de una visualización</button></div></article>').join('');$('video-menu').querySelectorAll('[data-video]').forEach(b=>b.onclick=()=>startVideo(b.dataset.video,b.dataset.mode));if(state.active?.kind==='video')renderQuiz('video-area');else if(videoStage?.id)startVideo(videoStage.id,videoStage.mode,true);else $('video-area').innerHTML='';}
  async function startVideo(id,mode,restoring=false){
    if(!restoring&&state.active&&!(await confirmAction('Hay un cuestionario en curso. Quedará como abandonado. ¿Comenzar el video?')))return;
    if(!restoring&&state.active)abandonActive();
    stopSpeech();lastSpokenScene=-1;
    const v=data.videos.find(v=>v.id===id);if(!v)return;
    videoStage={id,mode,started:Date.now(),lastTime:0,repeat:restoring?Boolean(state.seen['video-content:'+id]):markSeen('video-content:'+id)};
    save();
    $('video-area').innerHTML='<article class="paper"><h3>'+esc(v.title)+'</h3><p class="muted">'+(v.narration?'Narración sintética y subtítulos.':'Video de lectura y esquemas; podés activar la narración por voz del navegador.')+' '+(mode==='trial'?'Una visualización. Al terminar se habilita el cuestionario de quince minutos.':'Podés revisar escenas y fuentes; se registra como estudio apoyado.')+'</p><video id="training-video" class="video-player" '+(mode==='study'?'controls':'')+' playsinline preload="metadata" src="'+esc(v.file)+'"><track kind="captions" src="'+esc(v.captions)+'" srclang="es" label="Español" default></video><p id="video-status" role="status">Listo para iniciar.</p><div class="bar"><button id="play-video" class="primary">Comenzar video</button><button id="toggle-narration" type="button" aria-pressed="'+String(ttsEnabled)+'">'+(ttsEnabled?'🔊 Narración por voz: activa':'🔈 Activar narración por voz (TTS)')+'</button><button id="video-questionnaire" '+(mode==='trial'?'disabled':'')+'>Responder cuestionario</button></div><div class="video-notes-box"><label for="video-notes-input"><strong>Mis apuntes durante el video</strong> (se conservan y podrás consultarlos al responder el cuestionario)</label><textarea id="video-notes-input" placeholder="Anotá acá plazos, órganos, edades o palabras clave mientras mirás el video…">'+esc(state.videoNotes?.[id]||'')+'</textarea></div>'+(mode==='study'?'<details><summary>Escenas y fuentes para estudiar</summary>'+v.scenes.map(s=>'<div class="video-scene"><strong>'+formatSeconds(s.start)+' · '+esc(s.title)+'</strong><p>'+esc(s.text)+'</p>'+sources(s.sources)+'</div>').join('')+'</details>':'')+'</article>';
    const el=$('training-video');
    if($('video-notes-input'))$('video-notes-input').oninput=e=>{state.videoNotes[id]=e.target.value;save();};
    if($('toggle-narration'))$('toggle-narration').onclick=()=>{
      ttsEnabled=!ttsEnabled;
      $('toggle-narration').setAttribute('aria-pressed',String(ttsEnabled));
      $('toggle-narration').textContent=ttsEnabled?'🔊 Narración por voz: activa':'🔈 Activar narración por voz (TTS)';
      save();
      if(!ttsEnabled)stopSpeech();
      else if(el&&!el.paused){
        const curScene=v.scenes.findIndex((s,idx)=>el.currentTime>=s.start&&el.currentTime<(v.scenes[idx+1]?.start??v.duration+5));
        if(curScene>=0){lastSpokenScene=curScene;speakText(v.scenes[curScene].title+'. '+v.scenes[curScene].text);}
      }
    };
    $('play-video').onclick=async()=>{try{await el.play();$('play-video').disabled=true;$('video-status').textContent='Video en reproducción.';}catch{$('video-status').textContent='El navegador no pudo reproducirlo. Abrí el MP4 de esta jornada desde la carpeta videos.';}};
    el.onpause=()=>stopSpeech();
    el.onended=()=>{stopSpeech();if(mode==='trial'){$('video-status').textContent='Terminó el video. Comienza el plazo de quince minutos.';beginVideoQuiz(v,mode);}else{$('video-status').textContent='Video completo. Podés repasar o responder.';$('video-questionnaire').disabled=false;}};
    $('video-questionnaire').onclick=()=>beginVideoQuiz(v,mode);
    if(mode==='trial')el.addEventListener('seeking',()=>{if(videoStage&&el.currentTime>videoStage.lastTime+2)el.currentTime=videoStage.lastTime;});
    el.addEventListener('timeupdate',()=>{
      if(videoStage)videoStage.lastTime=Math.max(videoStage.lastTime,el.currentTime);
      if(ttsEnabled&&!el.paused){
        const curScene=v.scenes.findIndex((s,idx)=>el.currentTime>=s.start&&el.currentTime<(v.scenes[idx+1]?.start??v.duration+5));
        if(curScene>=0&&curScene!==lastSpokenScene){
          lastSpokenScene=curScene;
          speakText(v.scenes[curScene].title+'. '+v.scenes[curScene].text);
        }
      }
    });
    if(!restoring)$('video-area').scrollIntoView({behavior:'auto'});
  }
  function beginVideoQuiz(v,mode){stopSpeech();const el=$('training-video');el?.pause();const key='video:'+v.id,repeat=markSeen(key)||Boolean(videoStage?.repeat),started=Date.now();state.active={kind:'video',key,id:v.id,type:'video',started,deadline:started+15*60000,minutes:15,answers:{},confidence:{},repeat,supported:mode==='study',optionOrders:buildOptionOrders(v.questions)};videoStage=null;save();renderQuiz('video-area');$('video-area').scrollIntoView({behavior:'auto'});}
  function renderResults(){
    const objective=state.results.filter(r=>r.assessment==='objective'),self=state.results.filter(r=>r.assessment==='self');
    const latestFree=latestFreeResults();
    const pending=latestFree.filter(r=>r.assessment==='pending'),due=latestFree.filter(r=>r.assessment==='self'&&r.due<=Date.now());
    $('result-summary').innerHTML='<div class="history-grid"><article class="paper"><h3>Cuestionarios por clave</h3><p>'+objective.length+' completados · '+objective.filter(r=>!r.repeat&&!r.supported).length+' primeras exposiciones.</p><p>'+objective.reduce((n,r)=>n+r.highErrors,0)+' errores registrados con seguridad alta.</p><p class="muted">Las repeticiones y anticipaciones se identifican en cada registro.</p></article><article class="paper"><h3>Respuestas y autoevaluación</h3><p>'+self.length+' rúbricas guardadas · '+pending.length+' respuestas vigentes por comparar.</p><p>'+due.length+' ejercicios con fecha de repaso alcanzada.</p><p class="muted">Una rúbrica valorada por vos se conserva como autoevaluación; no se mezcla con una nota por clave.</p></article></div>';
    $('result-list').innerHTML=state.results.map(r=>'<article class="result-row"><time>'+date(r.finished)+'</time><h3>'+esc(r.title)+'</h3><span class="chip">'+esc(r.assessment==='objective'?'Por clave':r.assessment==='self'?'Autoevaluación':r.assessment==='pending'?'Respuesta conservada':'Abandonado')+'</span><span class="chip '+(r.repeat?'warning':'')+'">'+(r.repeat?'Repetición':'Primera exposición')+'</span>'+(r.supported?'<span class="chip warning">Estudio apoyado</span>':'')+(r.early?'<span class="chip warning">Anticipado</span>':'')+(r.score!==undefined?'<p>'+r.score+' / '+r.max+(r.assessment==='self'?' puntos de rúbrica propia':' aciertos')+'</p>':'')+(r.critical?'<p>'+r.critical+' criterios esenciales requieren repaso.</p>':'')+(r.due?'<p>Repaso sugerido: '+date(r.due)+'</p>':'')+(r.texts?'<details><summary>Primera respuesta conservada</summary>'+Object.entries(r.texts).map(([k,t])=>'<p class="muted">'+esc(k==='main'?'Respuesta':'Caso '+k.toUpperCase())+'</p><div class="preserved">'+esc(t)+'</div>').join('')+'</details>':'')+(r.assessment==='objective'?'<p>'+r.missing+' sin responder · '+r.highErrors+' errores con seguridad alta.</p><button data-review-result="'+esc(r.attemptId)+'">Ver corrección completa</button>':'<button data-reopen="'+esc(r.id)+'" data-kind="'+esc(r.kind)+'">Volver al ejercicio</button>')+'</article>').join('')||'<article class="paper">Todavía no hay respuestas completadas. Comenzá por explicar un concepto sin opciones.</article>';
    $('result-list').querySelectorAll('[data-reopen]').forEach(b=>b.onclick=()=>{setView(b.dataset.kind);$('module').value='all';$('topic').value='all';refreshExercises(b.dataset.reopen);});
    $('result-list').querySelectorAll('[data-review-result]').forEach(b=>b.onclick=()=>{if(state.active){$('result-list').insertAdjacentHTML('afterbegin','<p class="notice">Terminá el cuestionario en curso antes de consultar correcciones.</p>');return;}const r=state.results.find(x=>x.attemptId===b.dataset.reviewResult),info=activeQuestions({kind:r.kind,id:r.id,type:r.key.startsWith('spec:')?'spec':'read'}),area=r.kind==='video'?'video-area':'diagnostic-area';setView(r.kind==='video'?'videos':'diagnostics');$(area).innerHTML=quizCorrection(r,info);$(area).scrollIntoView({behavior:'auto'});});
  }
  function exportState(){const blob=new Blob([JSON.stringify({fecha:new Date().toISOString(),taller:state},null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='mis-respuestas-taller-judicial-2026.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
  document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>navigate(b.dataset.view));
  $('module').innerHTML='<option value="all">Los cinco módulos</option>'+data.modules.map(m=>'<option value="'+m.id+'">M'+m.id+' · '+esc(m.title)+'</option>').join('');
  $('module').onchange=()=>{$('topic').value='all';refreshExercises();save();};
  $('topic').onchange=()=>{refreshExercises();save();};
  $('exercise').onchange=()=>{showExercise();save();};
  if($('diagMinutes'))$('diagMinutes').onchange=()=>save();
  $('next').onclick=()=>{const options=[...$('exercise').options],index=options.findIndex(o=>o.value===$('exercise').value);if(options.length){$('exercise').value=options[(index+1)%options.length].value;showExercise();save();}};
  $('exportar').onclick=exportState;
  $('exportar-results').onclick=exportState;
  if($('importar')&&$('importar-file')){
    $('importar').onclick=()=>$('importar-file').click();
    if($('importar-results'))$('importar-results').onclick=()=>$('importar-file').click();
    $('importar-file').onchange=async e=>{
      const file=e.target.files?.[0];if(!file)return;
      try{
        const raw=JSON.parse(await file.text());
        const incoming=raw?.taller||(raw?.results?raw:null);
        if(incoming&&typeof incoming==='object'){
          state={
            version:1,
            seen:{...state.seen,...(incoming.seen||{})},
            results:Array.isArray(incoming.results)?incoming.results:state.results,
            drafts:{...state.drafts,...(incoming.drafts||{})},
            videoNotes:{...state.videoNotes,...(incoming.videoNotes||{})},
            ui:incoming.ui||state.ui,
            active:incoming.active||state.active
          };
          save();setView(view);
          $('storageNotice').textContent='Avances del taller importados correctamente.';
        }else{
          $('storageNotice').textContent='El archivo seleccionado no contiene datos válidos del taller.';
        }
      }catch{
        $('storageNotice').textContent='No se pudo leer el archivo JSON seleccionado.';
      }
      e.target.value='';
    };
  }
  $('review-due').onclick=()=>{
    const latestFree=latestFreeResults();
    const pending=latestFree.find(r=>r.assessment==='pending'||(r.assessment==='self'&&r.due<=Date.now()));
    if(!pending){$('result-list').insertAdjacentHTML('afterbegin','<p class="notice">No hay repasos pendientes con fecha alcanzada. Podés practicar otro concepto o usar un diagnóstico reservado.</p>');return;}
    const dKey=pending.kind+':'+pending.id;
    if(pending.assessment==='self'&&state.drafts[dKey]?.assessed){
      delete state.drafts[dKey];
      save();
    }
    setView(pending.kind);$('module').value='all';$('topic').value='all';refreshExercises(pending.id);
  };
  $('counts').textContent=data.open.length+' preguntas abiertas · '+data.cases.length+' pares de casos · '+data.sequences.length+' secuencias · '+data.errors.length+' errores para corregir · dos formas reservadas y dos jornadas de video.';
  if(state.ui?.ttsEnabled!==undefined)ttsEnabled=Boolean(state.ui.ttsEnabled);
  if(state.ui?.diagMinutes&&$('diagMinutes'))$('diagMinutes').value=state.ui.diagMinutes;
  if(state.ui?.videoStage?.id)videoStage=state.ui.videoStage;
  if(state.active){
    const active=state.active;
    if(active.kind==='diagnostic')setView('diagnostics');
    else setView('videos');
  }else{
    let initialView=state.ui?.view&&labels[state.ui.view]?state.ui.view:'open';
    const savedMod=state.ui?.module||'all',savedTop=state.ui?.topic||'all',savedEx=state.ui?.exercise||'';
    try{
      const params=new URLSearchParams(window.location?.search||'');
      const hasUrlParams=Boolean(params.get('view')||params.get('module')||params.get('topic'));
      if(params.get('view')&&labels[params.get('view')])initialView=params.get('view');
      else if(params.get('module')||params.get('topic'))initialView=['open','cases','sequences','errors'].includes(initialView)?initialView:'open';
      if(hasUrlParams){
        setView(initialView);
        if(params.get('module')){$('module').value=params.get('module');refreshExercises();}
        if(params.get('topic')){$('topic').value=params.get('topic');refreshExercises();}
      }else{
        $('module').value=savedMod;
        $('topic').value=savedTop;
        setView(initialView,savedEx);
        if(['open','cases','sequences','errors'].includes(initialView)&&savedTop!=='all'){
          $('topic').value=savedTop;
          refreshExercises(savedEx);
        }
      }
    }catch{
      setView(initialView);
    }
  }
  save();
  window.TallerTest={state:()=>state,data,finish:()=>finishQuiz(state.active?.kind==='video'?'video-area':'diagnostic-area','submitted'),latestFreeResults,dueMidnight};
})();
