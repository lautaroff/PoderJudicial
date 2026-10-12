async page => {
  await page.reload();
  const result={fecha:'2026-10-12',checks:0,failures:[],requests:[]};
  function check(v,label){result.checks++;if(!v)result.failures.push(label)}
  check(await page.evaluate(()=>PREGUNTAS.length)===575,'575 finales');
  check(await page.evaluate(()=>PREGUNTAS.filter(q=>q.etapa==='lectura'&&q.revision==='2026-10-12').length)===60,'60 lecturas revisadas');
  await page.locator('.module-card button').nth(2).click();
  const m3=page.locator('#catalogo h3').filter({hasText:'Módulo 3. Derechos Humanos'});
  check(await m3.count()===1,'guía M3');
  check(await m3.evaluate(e=>e.getBoundingClientRect().top>=-20&&e.getBoundingClientRect().top<150),'entrada al apartado M3');
  await page.locator('.sidebar [data-tab="practica"]').click();
  await page.locator('#moduleFilter').selectOption('1');await page.locator('#topicFilter').selectOption('1.2');await page.locator('#start').click();
  check(await page.evaluate(()=>current.length>0&&current.every(q=>q.subtema.startsWith('1.2.'))),'filtro de apartado con sus subapartados');
  await page.locator('#finish').click();await page.locator('dialog [data-answer="yes"]').click();
  await page.locator('#mode').selectOption('institucional');await page.locator('#start').click();
  check(await page.locator('fieldset.question').count()===20,'institucional20');
  const keys=await page.evaluate(()=>current.map(q=>q.correcta));
  for(let i=0;i<20;i++)await page.locator(`[name="q${i}"][value="${keys[i]}"]`).check();
  await page.locator('#finish').click();
  check(await page.locator('.result').innerText()==='20 / 20','corrección institucional');
  check(await page.locator('#exam a[href*=".pdf#page="]').count()>=20,'institucional con fuentes locales');
  const normHtml=await page.evaluate(()=>questionSources(PREGUNTAS.find(q=>q.id==='N2-095')));
  check(normHtml.includes('Ley-24522-Concursos-y-Quiebras-lectura.html'),'fuente normativa suplementaria');
  await page.locator('.sidebar [data-tab="inicio"]').click();
  await page.evaluate(()=>{['pjm-history','pjm-errors','pjm-coverage-2026','pjm-memoria-2026'].forEach(k=>localStorage.removeItem(k));});
  page.on('request',r=>result.requests.push(r.url()));
  await page.reload();
  check(result.requests.every(url=>!/^https?:/.test(url)||new URL(url).hostname==='127.0.0.1'),'carga sin peticiones externas');
  await page.screenshot({path:'output/playwright/portal-final-2026.png',fullPage:false});
  if(result.failures.length)throw Error(JSON.stringify(result));
  return result;
}
