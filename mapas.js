/* Diagramas locales: relaciones explícitas, fuentes y recuperación. Sin dependencias. */
(() => {
  'use strict';
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const kinds = {concept:'Mapa conceptual',hierarchy:'Estructura por niveles',sequence:'Recorrido y decisiones',matrix:'Matriz de categorías',cycle:'Ciclo y relaciones',compare:'Cuadro comparativo'};
  function flatten(map) {
    const out=[];
    function walk(nodes,group,parent=null,depth=0){ for(const node of nodes){out.push({...node,group,parent,depth});walk(node.children||[],group,node.id,depth+1);} }
    map.groups.forEach((group,index)=>walk(group.nodes,index));return out;
  }
  function sourceMarkup(items,modules,compact=false) {
    if(!Array.isArray(items)) return '';
    return '<div class="sources'+(compact?' compact-sources':'')+'">'+items.map(s=>{
      const mod=modules[s.module],file=s.file||s.url||mod?.file;
      if(!file) return '';
      const pdf=/\.pdf(?:$|[?#])/i.test(file),page=Number(s.page),hasPage=pdf&&Number.isInteger(page)&&page>0;
      const href=file+(hasPage?(file.includes('#')?'&':'#')+'page='+page:'');
      const label=s.label||('M'+s.module),suffix=hasPage?' · PDF p. '+page:(s.section&&!label.includes(s.section)?' · '+s.section:'');
      return `<a href="${esc(href)}" target="_blank" rel="noopener" aria-label="Abrir ${esc(label+suffix)}">${esc(label+suffix)} ↗</a>`;
    }).join('')+'</div>';
  }
  function quizLabel(node,mode,labels) {
    if(mode==='build') return `<label class="small" for="answer-${esc(node.id)}">Concepto de esta pista</label><select id="answer-${esc(node.id)}" data-answer="${esc(node.label)}"><option value="">Elegí un concepto…</option>${labels.map(x=>`<option value="${esc(x)}">${esc(x)}</option>`).join('')}</select>`;
    return `<button class="node-label" data-label="${esc(node.label)}" ${mode==='read'?'disabled':''} aria-expanded="${mode==='read'}">${mode==='recall'?'¿Qué concepto es? · revelar':esc(node.label)}</button>`;
  }
  function nodeMarkup(node,ctx,flow=false){
    const {mode,labels,modules}=ctx;
    return `<article class="node atlas-node ${flow?'flow-node':''}" data-node-id="${esc(node.id)}">${node.relation?`<span class="node-relation">${esc(node.relation)}</span>`:''}${quizLabel(node,mode,labels)}<p class="node-explanation">${esc(node.detail)}</p>${sourceMarkup(node.sources,modules,true)}<div class="node-result" aria-live="polite"></div>${!flow&&node.children?.length?`<details class="child-tree" ${mode!=='read'||ctx.mapKind==='hierarchy'?'open':''}><summary>${esc(node.childrenRelation||'Abrir relaciones y niveles')} <span>${node.children.length}</span></summary><div class="tree-descendants">${node.children.map(n=>nodeMarkup(n,ctx)).join('')}</div></details>`:''}</article>`;
  }
  function edgesFor(map,nodes){
    const ids=new Set(nodes.map(n=>n.id)),edges=(map.edges||[]).filter(e=>ids.has(e.from)&&ids.has(e.to)).map(e=>({...e}));
    for(const n of nodes)if(n.parent&&ids.has(n.parent)&&!edges.some(e=>e.from===n.parent&&e.to===n.id))edges.push({from:n.parent,to:n.id,label:n.relation||'incluye',type:'structure'});
    if(!edges.length&&map.kind==='sequence')for(let i=1;i<nodes.length;i++)edges.push({from:nodes[i-1].id,to:nodes[i].id,label:'continúa con',type:'sequence'});
    return edges;
  }
  function layout(nodes,edges){
    const byId=new Map(nodes.map(n=>[n.id,n])),adj=new Map(nodes.map(n=>[n.id,[]])),color=new Map(),back=new Set();
    edges.forEach((e,i)=>{if(e.type!=='feedback'&&e.from!==e.to)adj.get(e.from)?.push({id:e.to,i});else back.add(i);});
    function visit(id){color.set(id,1);for(const e of adj.get(id)||[]){if(color.get(e.id)===1)back.add(e.i);else if(!color.has(e.id))visit(e.id);}color.set(id,2);}
    nodes.forEach(n=>{if(!color.has(n.id))visit(n.id);});
    const indegree=new Map(nodes.map(n=>[n.id,0])),rank=new Map(nodes.map(n=>[n.id,0]));
    edges.forEach((e,i)=>{if(!back.has(i))indegree.set(e.to,indegree.get(e.to)+1);});
    const queue=nodes.filter(n=>indegree.get(n.id)===0).map(n=>n.id);
    for(let i=0;i<queue.length;i++){const id=queue[i];edges.forEach((e,j)=>{if(e.from!==id||back.has(j))return;rank.set(e.to,Math.max(rank.get(e.to),rank.get(id)+1));indegree.set(e.to,indegree.get(e.to)-1);if(indegree.get(e.to)===0)queue.push(e.to);});}
    const levels=[];nodes.forEach(n=>{const r=rank.get(n.id);(levels[r]||=[]).push(n.id);});
    const width=Math.max(328,...levels.map(l=>l.length*300+56)),positions=new Map();
    levels.forEach((level,r)=>level.forEach((id,c)=>positions.set(id,{x:(width-level.length*300)/2+c*300+18,y:40+r*286,w:264,h:190})));
    return {positions,width,height:Math.max(280,levels.length*286+80),back,byId};
  }
  function edgeNames(map,nodes,edges,mode){
    const ids=new Map(nodes.map(n=>[n.id,n]));
    return `<details class="edge-ledger" ${mode!=='read'?'open':''}><summary>Leer las conexiones <span>${edges.length}</span></summary><ol>${edges.map(e=>`<li><button class="edge-jump" data-jump-node="${esc(e.from)}">${mode==='read'?esc(ids.get(e.from)?.label):'Concepto de origen'}</button><span class="edge-verb">${esc(e.label)} →</span><button class="edge-jump" data-jump-node="${esc(e.to)}">${mode==='read'?esc(ids.get(e.to)?.label):'Concepto de destino'}</button></li>`).join('')}</ol></details>`;
  }
  function flowMarkup(map,nodes,ctx){
    const edges=edgesFor(map,nodes),drawing=layout(nodes,edges),{positions,width,height,back}=drawing;
    const paths=edges.map((e,i)=>{
      const a=positions.get(e.from),b=positions.get(e.to);if(!a||!b)return '';
      let d,x,y;
      if(back.has(i)){const side=Math.max(a.x+a.w,b.x+b.w)+22;d=`M ${a.x+a.w} ${a.y+a.h/2} C ${side+24} ${a.y+a.h/2}, ${side+24} ${b.y+b.h/2}, ${b.x+b.w+4} ${b.y+b.h/2}`;x=Math.min(width-115,side-55);y=(a.y+b.y)/2+a.h/2;}
      else {const ax=a.x+a.w/2,bx=b.x+b.w/2,ay=a.y+a.h,by=b.y-7,mid=(ay+by)/2;d=`M ${ax} ${ay} C ${ax} ${mid}, ${bx} ${mid}, ${bx} ${by}`;x=(ax+bx)/2;y=mid;}
      const words=e.label.length>22?e.label.slice(0,19)+'…':e.label;
      return `<g class="diagram-edge ${back.has(i)?'feedback-edge':''}"><path d="${d}" marker-end="url(#atlas-arrow)"/><rect x="${x-68}" y="${y-13}" width="136" height="26" rx="13"/><text x="${x}" y="${y+4}">${esc(words)}</text><title>${esc(e.label)}</title></g>`;
    }).join('');
    return `<div class="diagram-instructions">Seguí las flechas y sus condiciones. Podés desplazar el dibujo en ambas direcciones. Las conexiones completas también se leen al pie.</div><div class="diagram-tools" role="group" aria-label="Escala del diagrama"><button class="quiet" data-diagram-zoom="out" aria-label="Alejar diagrama">−</button><output class="diagram-scale">100 %</output><button class="quiet" data-diagram-zoom="in" aria-label="Acercar diagrama">+</button><button class="quiet" data-diagram-zoom="fit">Ver el conjunto</button><button class="quiet" data-diagram-zoom="reset">Tamaño de lectura</button></div><div class="flow-viewport" tabindex="0" aria-label="Diagrama desplazable de ${esc(map.title)}"><div class="flow-size" style="width:${width}px;height:${height}px"><div class="flow-surface" data-width="${width}" data-height="${height}" style="width:${width}px;height:${height}px"><svg class="flow-lines" width="${width}" height="${height}" aria-hidden="true"><defs><marker id="atlas-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs>${paths}</svg>${nodes.map(n=>{const p=positions.get(n.id);return `<div class="flow-position" style="left:${p.x}px;top:${p.y}px;width:${p.w}px;height:${p.h}px"><span class="flow-group">${esc(map.groups[n.group].title)}</span>${nodeMarkup(n,ctx,true)}</div>`;}).join('')}</div></div></div>${edgeNames(map,nodes,edges,ctx.mode)}`;
  }
  function render(map,{mode='read',presentation='diagram',group='all',modules}){
    const all=flatten(map),nodes=all.filter(n=>group==='all'||String(n.group)===group),labels=[...new Set(nodes.map(n=>n.label))].sort((a,b)=>a.localeCompare(b,'es'));
    const ctx={mode,labels,modules,mapKind:map.kind},flow=presentation==='diagram'&&['sequence','cycle'].includes(map.kind);
    const groups=map.groups.map((g,i)=>({g,i})).filter(x=>group==='all'||String(x.i)===group);
    const branchMarkup=`<div class="branches enhanced-branches" style="--columns:${Math.min(groups.length,map.kind==='matrix'||map.kind==='compare'?2:3)}">${groups.map(({g,i})=>`<section class="branch" data-map-group="${i}"><h4>${esc(g.title)}</h4><span class="relation">${esc(g.relation)}</span><div class="nodes">${g.nodes.map(n=>nodeMarkup(n,ctx)).join('')}</div></section>`).join('')}</div>`;
    return `<div class="map-shell enhanced-map ${esc(map.kind)} ${presentation==='outline'?'outline-map':''}" style="--accent:${modules[map.module].color}"><header class="map-heading"><span class="module-tag">M${map.module} · ${esc(modules[map.module].name)}</span><span class="map-kind">${esc(kinds[map.kind]||kinds.concept)}</span><h3 tabindex="-1">${esc(map.title)}</h3><p>${esc(map.lead)}</p><div class="map-controls">${[['read','Leer'],['recall','Ocultar etiquetas'],['build','Reconstruir']].map(([v,t])=>`<button class="quiet ${mode===v?'pressed':''}" data-map-mode="${v}" aria-pressed="${mode===v}">${t}</button>`).join('')}${mode==='build'?'<button class="primary" id="check-map">Comprobar reconstrucción</button>':''}</div><div class="map-options"><div class="presentation-options" role="group" aria-label="Presentación del mapa"><button data-presentation="diagram" aria-pressed="${presentation==='diagram'}">Diagrama</button><button data-presentation="outline" aria-pressed="${presentation==='outline'}">Por niveles</button></div><label>Enfocar una rama <select id="map-group"><option value="all">El conjunto · ${all.length} conceptos</option>${map.groups.map((g,i)=>`<option value="${i}" ${String(i)===group?'selected':''}>${esc(g.title)}</option>`).join('')}</select></label>${!flow?'<button class="quiet" data-expand-levels>Desplegar niveles</button>':''}</div></header><div class="map-canvas"><p id="map-feedback" class="map-feedback" aria-live="polite">${mode==='recall'?'Recuperá el concepto con su pista y explicá la relación antes de revelar.':mode==='build'?'Elegí cada concepto y explicá por qué corresponde. Las fuentes siguen disponibles.':'Las líneas y los verbos indican la relación; las ramas no implican por sí solas una jerarquía de mando.'}</p><div class="hub"><strong>${esc(map.root)}</strong>${sourceMarkup(map.rootSources,modules)}</div>${flow?flowMarkup(map,nodes,ctx):branchMarkup}${!flow&&map.edges?.length?edgeNames(map,nodes,edgesFor(map,nodes),mode):''}</div>${map.cautions?.length?`<aside class="map-cautions"><strong>Para interpretar bien este mapa</strong><ul>${map.cautions.map(c=>`<li>${esc(c)}</li>`).join('')}</ul></aside>`:''}${map.exercise?`<section class="map-exercise"><p class="eyebrow">Recuperar y aplicar</p><h4>${esc(map.exercise.prompt)}</h4><label class="small" for="map-explanation">Tu explicación · práctica sin calificación automática</label><textarea id="map-explanation" rows="3" placeholder="Primero intentá explicarlo con tus palabras…"></textarea><details><summary>Comparar con una respuesta explicada</summary><p>${esc(map.exercise.answer)}</p></details></section>`:''}<p class="map-hint"><strong>Ayuda de memoria propia.</strong> ${esc(map.hint)}</p>${map.related?.length?`<nav class="related-maps" aria-label="Mapas relacionados"><span>Conectar con</span>${map.related.map(id=>`<button class="quiet" data-related-map="${esc(id)}">${esc(id)}</button>`).join('')}</nav>`:''}</div>`;
  }
  window.PJM_MAPAS={flatten,sources:sourceMarkup,render,kinds,edgesFor};
})();
