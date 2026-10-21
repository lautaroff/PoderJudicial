/* Offline atlas. Revealing an answer never records successful recall. */
(() => {
  'use strict';
  const data = window.PJM_MEMORIA;
  const KEY = 'pjm-memoria-2026';
  const atlas = window.PJM_MAPAS;
  const $ = id => document.getElementById(id);
  const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const modules = Object.fromEntries(data.modules.map(m => [m.id,m]));
  let state = {version:1,cards:{},cases:{},mapHistory:[],mapDrafts:{}};
  let storageOK = true;
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if(saved && typeof saved==='object' && !Array.isArray(saved)) {
      state = {...saved,version:1,mapDrafts:saved.mapDrafts && typeof saved.mapDrafts==='object' ? saved.mapDrafts : {},cards: saved.cards && typeof saved.cards==='object' ? saved.cards : {},cases:saved.cases && typeof saved.cases==='object' ? saved.cases : {},mapHistory:Array.isArray(saved.mapHistory) ? saved.mapHistory : []};
    }
  } catch { storageOK=false; }
  let moduleFilter = 'all';
  let view='mapas';
  let currentMap = data.maps.some(m=>m.id==='m1-estructura-judicial') ? 'm1-estructura-judicial' : data.maps[0].id;
  try {const linked=new URLSearchParams(location.hash.slice(1)).get('map');if(data.maps.some(m=>m.id===linked))currentMap=linked;} catch {}
  let mapQuery='';
  let presentation='diagram';
  let groupFocus='all';
  let mapMode='read';
  let session=[];
  let cardIndex=0;
  let revealed=false;
  let sessionRated=0;
  let sessionSkipped=0;
  const intervals=[1,3,7,14,30];
  const now=()=>Date.now();
  const filtered = items => items.filter(x => moduleFilter==='all' || String(x.module)===moduleFilter);
  function formatDate(value) { return new Date(value).toLocaleDateString('es-AR',{day:'numeric',month:'long'}); }
  function storageNotice(){ $('storage-notice').textContent=storageOK ? 'Tus repasos se guardan sólo en este navegador. Exportalos para conservar una copia.' : 'El navegador no pudo guardar los repasos. Podés continuar y exportar una copia al terminar.'; }
  function save(){ try {localStorage.setItem(KEY,JSON.stringify(state));storageOK=true;} catch {storageOK=false;} storageNotice();updateStats(); }
  function sources(items){return atlas.sources(items,modules);}
  function badge(m){return `<span class="module-tag">M${m} · ${esc(modules[m].name)}</span>`;}
  function updateStats(){
    const cards=filtered(data.cards);
    const seen=cards.filter(c=>state.cards[c.id] && Number(state.cards[c.id].ratings)>0).length;
    const due=cards.filter(c=>state.cards[c.id] && Number(state.cards[c.id].due)<=now()).length;
    const newer=cards.filter(c=>!state.cards[c.id] || !Number(state.cards[c.id].ratings)).length;
    $('stats').textContent=`${cards.length} tarjetas · ${seen} autoevaluadas · ${due} para hoy · ${newer} nuevas`;
  }
  function setView(next){
    view=next;
    document.querySelectorAll('.view').forEach(el=>el.hidden=el.id!==next);
    document.querySelectorAll('.mode').forEach(el=>{const active=el.dataset.view===next;el.classList.toggle('active',active);el.setAttribute('aria-pressed',String(active));});
    if(next==='mapas') renderMapMenu();
    if(next==='tarjetas') startSession();
    if(next==='contrastes') renderPairs();
    if(next==='casos') renderCases();
  }
  function availableMaps(){
    const query=mapQuery.trim().toLocaleLowerCase('es');
    return filtered(data.maps).filter(m=>!query || [m.title,m.area||'',...atlas.flatten(m).map(n=>n.label)].join(' ').toLocaleLowerCase('es').includes(query));
  }
  function renderMapMenu(){
    const available=availableMaps();
    if(available.length && !available.some(m=>m.id===currentMap)){currentMap=available[0].id;mapMode='read';groupFocus='all';}
    $('catalog-count').textContent=`${available.length} mapas disponibles · ${data.maps.length} en el atlas`;
    $('map-menu').innerHTML=available.length ? data.modules.map(mod=>{
      const items=available.filter(m=>m.module===mod.id);if(!items.length)return '';
      return `<details class="catalog-module" ${moduleFilter!=='all'||mapQuery||items.some(m=>m.id===currentMap)?'open':''}><summary>M${mod.id} · ${esc(mod.name)} <span>(${items.length})</span></summary>${items.map(m=>`<button class="map-choice ${m.id===currentMap?'selected':''}" data-map="${esc(m.id)}" style="--accent:${mod.color}" aria-pressed="${m.id===currentMap}"><small>${esc(atlas.kinds[m.kind]||'Mapa conceptual')}</small>${esc(m.title)}${m.area?`<span class="map-area">${esc(m.area)}</span>`:''}</button>`).join('')}</details>`;
    }).join('') : '<p class="catalog-empty">No hay mapas con esa búsqueda. Probá el nombre de un tema u órgano.</p>';
    if(available.length)renderMap();else $('map-panel').innerHTML='<p class="notice">Cambiá la búsqueda para encontrar otro mapa.</p>';
  }
  function renderMap(){
    const m=data.maps.find(x=>x.id===currentMap);if(!m)return;
    $('map-panel').innerHTML=atlas.render(m,{mode:mapMode,presentation,group:groupFocus,modules});
    $('map-panel').querySelectorAll('[data-related-map]').forEach(b=>{const target=data.maps.find(x=>x.id===b.dataset.relatedMap);if(target)b.textContent=`M${target.module} · ${target.title}`;else b.hidden=true;});
    const explanation=$('map-explanation');if(explanation)explanation.value=state.mapDrafts[currentMap]||'';
    const viewport=$('map-panel').querySelector('.flow-viewport');if(viewport)viewport.scrollLeft=Math.max(0,(viewport.scrollWidth-viewport.clientWidth)/2);
    try {history.replaceState(null,'','#map='+encodeURIComponent(currentMap));}catch{}
  }
  function openMap(id){
    const m=data.maps.find(x=>x.id===id);if(!m)return;
    if(moduleFilter!=='all'&&String(m.module)!==moduleFilter){moduleFilter=String(m.module);$('modulo').value=moduleFilter;}
    currentMap=id;mapMode='read';groupFocus='all';mapQuery='';$('map-search').value='';renderMapMenu();updateStats();
    $('map-panel').querySelector('h3')?.focus({preventScroll:true});
  }
  function checkMap(){
    let correct=0,total=0,blank=0;
    $('map-panel').querySelectorAll('select[data-answer]').forEach(select=>{
      total++;
      const node=select.closest('.node');
      const yes=select.value===select.dataset.answer;
      if(yes) correct++;
      if(!select.value) blank++;
      node.classList.toggle('correct',yes);node.classList.toggle('incorrect',!yes);
      node.querySelector('.node-result').textContent=yes?'Coincide. Explicá también la relación.':(!select.value?'Sin completar. ': 'Para revisar. ')+`Concepto: ${select.dataset.answer}.`;
    });
    $('map-feedback').textContent=`${correct} de ${total} etiquetas coinciden${blank?` · ${blank} sin completar`:''}. La comprobación evalúa asociación de pistas; completala explicando la relación sin mirar.`;
    state.mapHistory.push({map:currentMap,group:groupFocus,correct,total,blank,at:now()});
    state.mapHistory=state.mapHistory.slice(-50);save();
  }
  function startSession(shuffle=false){
    let available=filtered(data.cards);
    const deck=$('deck').value;
    if(deck==='due') available=available.filter(c=>!state.cards[c.id] || !Number(state.cards[c.id].ratings) || Number(state.cards[c.id].due)<=now());
    if(deck==='review') available=available.filter(c=>state.cards[c.id] && state.cards[c.id].review);
    available.sort((a,b)=>{
      const sa=state.cards[a.id],sb=state.cards[b.id];
      const duea=sa && Number(sa.ratings)>0 ? Number(sa.due) || 0 : Number.MAX_SAFE_INTEGER;
      const dueb=sb && Number(sb.ratings)>0 ? Number(sb.due) || 0 : Number.MAX_SAFE_INTEGER;
      return duea-dueb;
    });
    if(shuffle) for(let i=available.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[available[i],available[j]]=[available[j],available[i]];}
    session=available;cardIndex=0;revealed=false;sessionRated=0;sessionSkipped=0;$('schedule-note').textContent='';renderCard();
  }
  function renderCard(){
    const c=session[cardIndex];
    $('card-counter').textContent=session.length ? `${Math.min(cardIndex+1,session.length)} / ${session.length} en esta sesión` : 'Sin tarjetas en esta selección';
    if(!c){
      const complete=session.length>0;
      $('flashcard').style.setProperty('--accent','var(--m2)');
      $('flashcard').innerHTML=`<div class="empty"><p class="eyebrow">${complete?'Recorrido completado':'La memoria también necesita tiempo'}</p><h3>${complete?'Cerrá con una explicación propia.':'No hay tarjetas pendientes aquí.'}</h3><p>${complete?`${sessionRated} autoevaluadas y ${sessionSkipped} pasadas sin evaluar. Explicá un concepto que hoy te costó y comprobá su página.`:'Elegí «Todas» para practicar sin modificar la fecha de las demás, o cambiá de módulo. Las tarjetas nuevas aparecen en «Pendientes y nuevas».'}</p><button class="primary" id="all-cards">Practicar todas</button></div>`;
      return;
    }
    $('flashcard').style.setProperty('--accent',modules[c.module].color);
    const old=state.cards[c.id];
    const planned=old && old.due ? `Próximo repaso: ${formatDate(old.due)}` : 'Tarjeta nueva';
    $('flashcard').innerHTML=`<div class="flash-top">${badge(c.module)}<p class="small">${esc(planned)}</p></div><h3>${esc(c.question)}</h3>${revealed?`<section class="answer" aria-label="Respuesta y ayuda de memoria"><p>${esc(c.answer)}</p><p class="memory-cue"><strong>Ayuda propia · ${esc(c.title)}</strong>${esc(c.cue)}</p>${c.note?`<p class="small">${esc(c.note)}</p>`:''}${sources(c.sources)}<div class="rate-actions"><button class="review-btn" data-rate="review">Necesito revisarla<small>Releer la página · volver mañana</small></button><button class="primary" data-rate="recall">La recordé y pude explicarla<small>Programar el siguiente repaso</small></button></div><p class="small">Marcá «La recordé» si recuperaste la idea antes de revelar y pudiste justificarla. Dar vuelta la tarjeta no registra un acierto.</p></section>`:`<p class="small">Respondé en voz alta o en papel. Agregá un ejemplo antes de comprobar.</p><button class="primary" id="reveal-card">Ver respuesta y fuente</button>${sources(c.sources)}`}<div class="flash-nav"><button class="quiet" id="previous-card" ${cardIndex===0?'disabled':''}>← Anterior</button><button class="quiet" id="skip-card">Pasar sin evaluar →</button></div>`;
  }
  function focusCard(selector='h3'){
    const target=$('flashcard').querySelector(selector);
    if(target){target.tabIndex=-1;target.focus({preventScroll:true});}
  }
  function rateCard(kind){
    const c=session[cardIndex];
    if(!c || !revealed) return;
    const old=state.cards[c.id] || {};
    const streak=kind==='recall' ? Math.max(0,Number(old.streak)||0)+1 : 0;
    const days=kind==='recall' ? intervals[Math.min(streak-1,intervals.length-1)] : 1;
    const due=now()+days*24*60*60*1000;
    state.cards[c.id]={last:now(),due,streak,interval:days,review:kind==='review',ratings:(Number(old.ratings)||0)+1,lastResult:kind};
    sessionRated++;save();cardIndex++;revealed=false;renderCard();focusCard();
    $('schedule-note').textContent=`${c.title}: ${kind==='recall'?'recuperación autoevaluada':'para revisar'}. Próximo repaso: ${formatDate(due)} (${days} ${days===1?'día':'días'}).`;
  }
  function renderPairs(){
    $('pair-list').innerHTML=filtered(data.pairs).map(p=>`<article class="pair" style="--accent:${modules[p.module].color}"><header class="pair-head">${badge(p.module)}<h3>${esc(p.title)}</h3></header><p class="pair-criterion"><strong>La pregunta que los separa:</strong><br>${esc(p.criterion)}</p><details><summary>Comprobar las dos ideas +</summary><div class="pair-body"><p class="pair-half">${esc(p.a)}</p><p class="pair-half">${esc(p.b)}</p></div>${sources(p.sources)}</details></article>`).join('');
  }
  function renderCases(){
    $('case-list').innerHTML=filtered(data.cases).map(c=>`<article class="case" data-case="${esc(c.id)}" style="--accent:${modules[c.module].color}">${badge(c.module)}<h3>${esc(c.text)}</h3><div class="case-options">${c.options.map((o,i)=>`<button class="case-option" data-choice="${i}"><span>${String.fromCharCode(65+i)}</span>${esc(o)}</button>`).join('')}</div><div class="case-result" aria-live="polite"></div>${sources(c.sources)}</article>`).join('');
  }
  function answerCase(button){
    const el=button.closest('[data-case]');
    const c=data.cases.find(c=>c.id===el.dataset.case);
    if(el.dataset.answered) return;
    const choice=Number(button.dataset.choice),yes=choice===c.correct;
    el.dataset.answered='true';
    el.querySelectorAll('[data-choice]').forEach(b=>{b.disabled=true;b.classList.toggle('is-correct',Number(b.dataset.choice)===c.correct);b.classList.toggle('is-wrong',b===button&&!yes);});
    el.querySelector('.case-result').innerHTML=`<strong>${yes?'Coincide con el criterio del material.':'Hay una distinción para revisar.'}</strong>${esc(c.why)}<br><button class="quiet case-reset" data-reset-case>Intentar otra vez</button>`;
    const old=state.cases[c.id] || {};
    state.cases[c.id]={attempts:(Number(old.attempts)||0)+1,last:now(),lastCorrect:yes};save();
  }
  function exportState(){
    const text=JSON.stringify({format:'pjm-memoria-2026',exportedAt:new Date().toISOString(),state},null,2);
    const blob=new Blob([text],{type:'application/json;charset=utf-8'});
    const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='mis-repasos-memoria-2026.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  document.querySelectorAll('.mode').forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));
  document.querySelectorAll('[data-territory]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();moduleFilter=a.dataset.territory;$('modulo').value=moduleFilter;mapMode='read';groupFocus='all';setView('mapas');updateStats();}));
  $('modulo').addEventListener('change',()=>{moduleFilter=$('modulo').value;mapMode='read';groupFocus='all';setView(view);updateStats();});
  $('map-menu').addEventListener('click',e=>{const b=e.target.closest('[data-map]');if(b)openMap(b.dataset.map);});
  $('map-search').addEventListener('input',()=>{mapQuery=$('map-search').value;renderMapMenu();});
  $('map-panel').addEventListener('change',e=>{if(e.target.id==='map-group'){groupFocus=e.target.value;renderMap();}});
  $('map-panel').addEventListener('input',e=>{if(e.target.id==='map-explanation'){state.mapDrafts[currentMap]=e.target.value.slice(0,6000);save();}});
  $('map-panel').addEventListener('click',e=>{
    const zoom=e.target.closest('[data-diagram-zoom]');if(zoom){
      const surface=$('map-panel').querySelector('.flow-surface'),viewport=$('map-panel').querySelector('.flow-viewport');if(!surface||!viewport)return;
      const w=Number(surface.dataset.width),h=Number(surface.dataset.height),old=Number(surface.dataset.scale)||1;
      const kind=zoom.dataset.diagramZoom,scale=kind==='fit'?Math.max(.12,Math.min(1,(viewport.clientWidth-12)/w)):kind==='reset'?1:Math.max(.12,Math.min(1.5,old+(kind==='in'?.15:-.15)));
      surface.style.transform=`scale(${scale})`;surface.dataset.scale=scale;surface.parentElement.style.width=`${w*scale}px`;surface.parentElement.style.height=`${h*scale}px`;
      $('map-panel').querySelector('.diagram-scale').textContent=`${Math.round(scale*100)} %`;viewport.scrollLeft=Math.max(0,(w*scale-viewport.clientWidth)/2);return;
    }
    const related=e.target.closest('[data-related-map]');if(related){openMap(related.dataset.relatedMap);return;}
    const drawing=e.target.closest('[data-presentation]');if(drawing){presentation=drawing.dataset.presentation;renderMap();$('map-panel').querySelector(`[data-presentation="${presentation}"]`).focus({preventScroll:true});return;}
    const expand=e.target.closest('[data-expand-levels]');if(expand){const trees=[...$('map-panel').querySelectorAll('.child-tree')];const opening=trees.some(x=>!x.open);trees.forEach(x=>x.open=opening);expand.textContent=opening?'Contraer niveles':'Desplegar niveles';return;}
    const jump=e.target.closest('[data-jump-node]');if(jump){const n=[...$('map-panel').querySelectorAll('[data-node-id]')].find(x=>x.dataset.nodeId===jump.dataset.jumpNode);if(n){let parent=n.parentElement;while(parent&&parent!==$('map-panel')){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}n.scrollIntoView({block:'center',inline:'center',behavior:'instant'});n.classList.add('node-highlight');setTimeout(()=>n.classList.remove('node-highlight'),1800);}return;}

    const mode=e.target.closest('[data-map-mode]');if(mode){mapMode=mode.dataset.mapMode;renderMap();$('map-panel').querySelector(`[data-map-mode="${mapMode}"]`).focus({preventScroll:true});return;}
    if(e.target.closest('#check-map')){checkMap();return;}
    const label=e.target.closest('.node-label');if(label && mapMode==='recall'){const shown=label.getAttribute('aria-expanded')==='true';label.textContent=shown?'¿Qué concepto es? · revelar':label.dataset.label;label.setAttribute('aria-expanded',String(!shown));}
  });
  $('deck').addEventListener('change',()=>startSession());$('mezclar').addEventListener('click',()=>startSession(true));
  $('flashcard').addEventListener('click',e=>{
    if(e.target.closest('#reveal-card')){revealed=true;renderCard();focusCard('.answer');return;}
    const rate=e.target.closest('[data-rate]');if(rate){rateCard(rate.dataset.rate);return;}
    if(e.target.closest('#previous-card')){if(cardIndex>0)cardIndex--;revealed=false;renderCard();focusCard();return;}
    if(e.target.closest('#skip-card')){cardIndex++;sessionSkipped++;revealed=false;renderCard();focusCard();return;}
    if(e.target.closest('#all-cards')){$('deck').value='all';startSession();}
  });
  $('case-list').addEventListener('click',e=>{
    const choice=e.target.closest('[data-choice]');if(choice){answerCase(choice);return;}
    const reset=e.target.closest('[data-reset-case]');if(reset){const el=reset.closest('[data-case]');delete el.dataset.answered;el.querySelectorAll('[data-choice]').forEach(b=>{b.disabled=false;b.classList.remove('is-correct','is-wrong');});el.querySelector('.case-result').innerHTML='';}
  });
  window.addEventListener('hashchange',()=>{try{const id=new URLSearchParams(location.hash.slice(1)).get('map');if(id&&id!==currentMap)openMap(id);}catch{}});
  $('exportar').addEventListener('click',exportState);
  storageNotice();updateStats();renderMapMenu();
})();
