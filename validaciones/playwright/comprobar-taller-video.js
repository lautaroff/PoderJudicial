async page => {
 const report={checks:0,failures:[],nota:'Reproducción real breve; el evento ended se dispara en prueba para verificar la transición sin esperar seis minutos.'};
 const check=(v,l)=>{report.checks++;if(!v)report.failures.push(l)};
 await page.reload();const backup=await page.evaluate(()=>localStorage.getItem('pjm-taller-2026'));
 await page.evaluate(()=>localStorage.removeItem('pjm-taller-2026'));await page.reload();await page.setViewportSize({width:1440,height:1000});
 try{
  await page.locator('[data-view="videos"]').click();await page.locator('[data-video="V1"][data-mode="trial"]').click();
  await page.waitForFunction(()=>document.getElementById('training-video').readyState>=1);
  check(await page.locator('#training-video').evaluate(e=>Math.abs(e.duration-360)<.1),'V1 duración real seis minutos');
  check(await page.locator('#training-video').getAttribute('controls')===null,'ensayo sin controles de salto');check(await page.locator('#video-questionnaire').isDisabled(),'cuestionario bloqueado antes de finalizar');
  await page.locator('#play-video').click();await page.waitForFunction(()=>document.getElementById('training-video').currentTime>.2);
  check(await page.locator('#training-video').evaluate(e=>!e.paused&&!e.error),'MP4 reproduce');
  await page.locator('#training-video').evaluate(e=>{e.currentTime=200});await page.waitForFunction(()=>document.getElementById('training-video').currentTime<10);check(true,'salto adelantado se revierte');
  await page.screenshot({path:'output/playwright/video-practica-2026.png',fullPage:true});
  await page.locator('#training-video').evaluate(e=>e.dispatchEvent(new Event('ended')));
  check(await page.locator('#video-area fieldset').count()===20,'fin de video habilita veinte preguntas');
  let a=await page.evaluate(()=>TallerTest.state().active);check(a.minutes===15&&!a.supported&&!a.repeat,'ensayo quince minutos sin apoyo');
  check(await page.locator('#video-area .sources').count()===0,'ensayo sin pistas de fuentes');
  await page.locator('#finish-diagnostic').click();await page.locator('#confirmYes').click();check(await page.locator('#video-area .sources a[href*="#t="]').count()===20,'corrección enlaza a escenas');
  await page.locator('[data-video="V1"][data-mode="study"]').click();await page.locator('#video-questionnaire').click();a=await page.evaluate(()=>TallerTest.state().active);check(a.repeat&&a.supported,'ver clip nuevamente queda identificado');await page.locator('#finish-diagnostic').click();await page.locator('#confirmYes').click();
  await page.locator('[data-video="V2"][data-mode="study"]').click();await page.waitForFunction(()=>document.getElementById('training-video').readyState>=1);check(await page.locator('#training-video').evaluate(e=>Math.abs(e.duration-360)<.1&&!e.error),'V2 metadatos reales');
  await page.locator('[data-view="diagnostics"]').click();await page.locator('#diagMinutes').selectOption('40');await page.locator('[data-diagnostic="spec:A"]').click();a=await page.evaluate(()=>TallerTest.state().active);check(a.minutes===40&&a.deadline-a.started===2400000,'diagnóstico cuarenta minutos');
  await page.locator('[data-view="open"]').click();await page.locator('#confirmYes').click();check(await page.evaluate(()=>Boolean(TallerTest.state().active)),'cambiar sección conserva cuestionario');
  await page.evaluate(()=>{TallerTest.state().active.deadline=Date.now()-1;});await page.waitForFunction(()=>TallerTest.state().active===null);check(await page.evaluate(()=>TallerTest.state().results[0].status==='expired'),'vence aunque esté en otra sección');
  await page.evaluate(()=>{const orig=URL.createObjectURL;URL.createObjectURL=b=>{window.exportBlob=b;return orig(b)}});await page.locator('#exportar').click();const exp=await page.evaluate(async()=>JSON.parse(await exportBlob.text()));check(exp.taller.results.length===3&&exp.taller.seen['video-content:V1'].opens===2,'exportación completa del taller');
  await page.goto('http://127.0.0.1:8766/index.html');check(await page.locator('a[href="taller.html"]').count()===2,'portal ofrece taller en menú y recorrido');await page.locator('[data-tab="historial"]').first().click();await page.evaluate(()=>{const orig=URL.createObjectURL;URL.createObjectURL=b=>{window.exportBlob=b;return orig(b)}});await page.locator('#export').click();const all=await page.evaluate(async()=>JSON.parse(await exportBlob.text()));check(Boolean(all.taller)&&Array.isArray(all.resultados)&&Object.hasOwn(all,'memoria'),'exportación del cuaderno incluye taller e historial');
  await page.goto('http://127.0.0.1:8766/memoria.html');check(await page.locator('a[href="taller.html"]').count()===1,'mapas enlazan al taller');
 }finally{await page.evaluate(saved=>saved===null?localStorage.removeItem('pjm-taller-2026'):localStorage.setItem('pjm-taller-2026',saved),backup);await page.goto('http://127.0.0.1:8766/taller.html');}
 console.log(JSON.stringify(report));return report;
}
