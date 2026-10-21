async page => {
  const key='pjm-memoria-2026';
  const backup=await page.evaluate(k=>localStorage.getItem(k),key);
  const report={fecha:'2026-10-21',checks:0,failures:[],maps:[],errors:[],externalRequests:[]};
  const check=(value,label)=>{report.checks++;if(!value)report.failures.push(label);};
  page.on('pageerror',e=>report.errors.push(e.message));
  page.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith('http://127.0.0.1:8767'))report.externalRequests.push(r.url());});
  const seed={version:1,cards:{'m1-01':{ratings:3,streak:2,due:123456,review:false}},cases:{c1:{attempts:2,lastCorrect:true}},mapHistory:[{map:'estado',correct:1,total:9,at:10}],legacyUnknown:{keep:true}};
  try {
    await page.setViewportSize({width:1440,height:1000});
    await page.evaluate(({key,seed})=>localStorage.setItem(key,JSON.stringify(seed)),{key,seed});
    await page.goto('http://127.0.0.1:8767/memoria.html');
    const data=await page.evaluate(()=>({maps:PJM_MEMORIA.maps.map(m=>({id:m.id,module:m.module,title:m.title,kind:m.kind,nodes:PJM_MAPAS.flatten(m).length,groups:m.groups.length})),cards:PJM_MEMORIA.cards.length,pairs:PJM_MEMORIA.pairs.length,cases:PJM_MEMORIA.cases.length}));
    check(data.cards===120&&data.pairs===12&&data.cases===15,'conserva tarjetas, contrastes y casos');
    check(await page.locator('.map-heading h3').innerText().then(t=>t.includes('órgano judicial')),'entrada inicial al panorama judicial');
    for(const m of data.maps){
      await page.locator('#modulo').selectOption(String(m.module));
      await page.locator(`[data-map="${m.id}"]`).click();
      check(await page.locator('.map-heading h3').innerText()===m.title,m.id+': título correcto');
      check(await page.locator('[data-node-id]').count()===m.nodes,m.id+': todos los nodos e hijos renderizados');
      const sourceStats=await page.locator('[data-node-id]').evaluateAll(els=>els.map(el=>({id:el.dataset.nodeId,hasSource:!![...el.children].find(c=>c.classList.contains('sources'))?.querySelector('a'),bad:[...el.querySelectorAll(':scope > .sources a')].some(a=>/undefined|NaN/.test(a.getAttribute('href')))})));
      check(sourceStats.every(s=>s.hasSource&&!s.bad),m.id+': fuente propia en cada nodo');
      await page.locator('[data-map-mode="recall"]').click();
      check(await page.locator('.node-label').evaluateAll(els=>els.every(e=>e.getAttribute('aria-expanded')==='false')),m.id+': etiquetas ocultas');
      const first=page.locator('.node-label').first();await first.click();
      check(await first.getAttribute('aria-expanded')==='true',m.id+': revelar etiqueta');
      await page.locator('[data-map-mode="build"]').click();
      check(await page.locator('select[data-answer]').count()===m.nodes,m.id+': reconstrucción incluye hijos');
      await page.locator('#check-map').click();
      check(await page.locator('#map-feedback').innerText().then(t=>t.includes('sin completar')),m.id+': informa omisiones');
      await page.locator('select[data-answer]').evaluateAll(els=>els.forEach(el=>{el.value=el.dataset.answer;}));
      await page.locator('#check-map').click();
      check(await page.locator('.node.correct').count()===m.nodes,m.id+': corrección de reconstrucción');
      await page.locator('[data-map-mode="read"]').click();
      if(['sequence','cycle'].includes(m.kind)){
        check(await page.locator('.flow-viewport svg .diagram-edge').count()>0,m.id+': conexiones dibujadas');
        await page.locator('[data-diagram-zoom="fit"]').click();
        check(await page.locator('.flow-viewport').evaluate(el=>el.scrollWidth<=el.clientWidth+2),m.id+': ajuste al ancho');
        await page.locator('[data-diagram-zoom="reset"]').click();
        check(await page.locator('.diagram-scale').innerText()==='100 %',m.id+': regreso al tamaño de lectura');
      }
      await page.locator('[data-presentation="outline"]').click();
      check(await page.locator('.outline-map').count()===1&&await page.locator('[data-node-id]').count()===m.nodes,m.id+': lectura por niveles completa');
      if(m.groups>1){await page.locator('#map-group').selectOption('0');check(await page.locator('[data-node-id]').count()<m.nodes,m.id+': enfoque por rama');await page.locator('#map-group').selectOption('all');}
      await page.locator('[data-presentation="diagram"]').click();
      report.maps.push({id:m.id,nodes:m.nodes,kind:m.kind});
    }
    await page.locator('#modulo').selectOption('all');
    await page.locator('#map-search').fill('Corte');
    check(await page.locator('.map-choice').count()>1,'buscar por concepto');
    await page.locator('#map-search').fill('inexistentezzzz');
    check(await page.locator('.catalog-empty').count()===1,'búsqueda vacía clara');
    await page.locator('#map-search').fill('');
    await page.locator('#modulo').selectOption('1');
    await page.locator('[data-map="m1-estructura-judicial"]').click();
    await page.locator('#map-explanation').fill('Primero distingo orden federal y provincial; después órgano y función.');
    await page.reload();
    check(await page.locator('#map-explanation').inputValue()==='Primero distingo orden federal y provincial; después órgano y función.','persistencia de explicación propia');
    const saved=await page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);
    check(JSON.stringify(saved.cards)===JSON.stringify(seed.cards)&&JSON.stringify(saved.cases)===JSON.stringify(seed.cases),'conserva evaluaciones previas');
    check(saved.legacyUnknown.keep===true&&saved.mapHistory.length<=50,'conserva campos previos y limita historial');
    const historyBefore= saved.mapHistory.length;
    await page.locator('[data-map-mode="recall"]').click();await page.locator('.node-label').first().click();
    check(await page.evaluate(k=>JSON.parse(localStorage.getItem(k)).mapHistory.length,key)===historyBefore,'leer y revelar no registra acierto');
    await page.locator('[data-map-mode="read"]').click();
    const downloadPromise=page.waitForEvent('download');await page.locator('#exportar').click();const download=await downloadPromise;
    check(download.suggestedFilename()==='mis-repasos-memoria-2026.json'&&saved.mapDrafts['m1-estructura-judicial']&&saved.legacyUnknown.keep,'exporta explicaciones y avances previos');
    const source=await page.locator('.node > .sources a[href*=".pdf#page="]').first().getAttribute('href');
    const response=await page.request.get(new URL(source,page.url()).href);
    check(response.status()===200,'PDF de concepto disponible con HTTP200');
    const related=page.locator('[data-related-map]').first();const target=await related.getAttribute('data-related-map');await related.click();
    check(new URL(page.url()).hash.includes(target),'mapa relacionado navega y actualiza enlace');
    for(const viewport of [{width:1440,height:1000},{width:390,height:844}]){
      await page.setViewportSize(viewport);
      for(const id of ['m1-estructura-judicial','m4-protocolo','m2-paz','m5-comunicacion']){
        await page.goto('http://127.0.0.1:8767/memoria.html#map='+id);
        const bounds=await page.evaluate(()=>({width:innerWidth,body:document.documentElement.scrollWidth}));
        check(bounds.body<=bounds.width+2,id+': sin desborde de página a '+viewport.width);
        await page.locator('.map-heading').scrollIntoViewIfNeeded();
        if(id==='m1-estructura-judicial')await page.screenshot({path:'output/playwright/mapas-estructura-'+viewport.width+'.png'});
      }
    }
    check(report.errors.length===0,'sin errores JavaScript');check(report.externalRequests.length===0,'sin dependencias HTTP externas');
  } finally {
    await page.evaluate(({key,backup})=>{if(backup===null)localStorage.removeItem(key);else localStorage.setItem(key,backup);},{key,backup});
  }
  console.log(JSON.stringify(report));
  await page.evaluate(report=>window.__MAPAS_REPORT=report,report);
  if(report.failures.length||report.errors.length)throw new Error('Fallaron comprobaciones del atlas');
  return report;
}
