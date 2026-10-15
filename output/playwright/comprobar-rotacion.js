async page=>{
  const keys=['pjm-history','pjm-errors','pjm-seen-2026'];
  const backup=await page.evaluate(keys=>Object.fromEntries(keys.map(k=>[k,localStorage.getItem(k)])),keys);
  const report={fecha:'2026-10-15',checks:0,failures:[]};
  const check=(v,label)=>{report.checks++;if(!v)report.failures.push(label)};
  try{
    await page.evaluate(keys=>keys.forEach(k=>localStorage.removeItem(k)),keys);await page.reload();
    await page.locator('.sidebar [data-tab="practica"]').click();
    await page.locator('#moduleFilter').selectOption('1');await page.locator('#start').click();
    const first=await page.evaluate(()=>current.map(q=>q.id));
    check(first.length===10,'primera tanda diez');
    check(await page.locator('#exam .notice').innerText().then(t=>t.includes('Sólo preguntas')),'avisa selección nueva');
    await page.reload();await page.locator('.sidebar [data-tab="practica"]').click();
    await page.locator('#moduleFilter').selectOption('1');await page.locator('#start').click();
    const second=await page.evaluate(()=>current.map(q=>q.id));
    check(second.every(id=>!first.includes(id)),'no repite después de abandonar y recargar');
    await page.evaluate(()=>{current.forEach((q,i)=>answers[i]=q.correcta);finish(activeMode)});
    check(await page.locator('.result').innerText()==='10 / 10','corrección preservada');
    await page.locator('#start').click();const third=await page.evaluate(()=>current.map(q=>q.id));
    check(third.every(id=>![...first,...second].includes(id)),'tercera tanda distinta');
    await page.evaluate(()=>{finished=true;const seen=seenQuestions();bank.filter(q=>q.etapa==='especificos'&&q.modulo===1).forEach(q=>seen[q.id]??={count:1,last:1});localStorage.setItem('pjm-seen-2026',JSON.stringify(seen));});
    await page.locator('#start').click();check(await page.locator('#exam .notice').innerText().then(t=>t.includes('Ya viste todas')),'avisa agotamiento');
    check(await page.locator('fieldset.question').count()===10,'repaso disponible tras agotar');
    await page.evaluate(()=>{finished=true;localStorage.setItem('pjm-seen-2026','{}');localStorage.setItem('pjm-history','[]')});
    await page.locator('#mode').selectOption('especificos');await page.locator('#start').click();
    const exam1=await page.evaluate(()=>current.map(q=>q.id));await page.evaluate(()=>finished=true);
    await page.locator('#start').click();const exam2=await page.evaluate(()=>current.map(q=>q.id));
    check(exam2.length===50&&exam2.every(id=>!exam1.includes(id)),'dos simulacros completos sin repetición');
    check(await page.evaluate(()=>modules.every(m=>current.filter(q=>q.modulo===m.id).length===10)),'conserva diez por módulo');
  }finally{await page.evaluate(b=>Object.entries(b).forEach(([k,v])=>v===null?localStorage.removeItem(k):localStorage.setItem(k,v)),backup);await page.reload();}
  console.log(JSON.stringify(report));return report;
}
