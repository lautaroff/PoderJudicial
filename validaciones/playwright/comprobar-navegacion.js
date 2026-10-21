async page => {
  await page.reload();await page.setViewportSize({width:1440,height:960});
  let checks=0;const failures=[];
  const check=(value,label)=>{checks++;if(!value)failures.push(label)};
  await page.evaluate(()=>window.scrollTo(0,900));
  const rects=await page.evaluate(()=>{const n=document.querySelector('.sidebar nav').getBoundingClientRect(),s=document.querySelector('.side-note').getBoundingClientRect();return {navBottom:n.bottom,noteTop:s.top}});
  check(rects.noteTop>=rects.navBottom,'sin superposición al desplazar');
  await page.locator('.sidebar [data-tab="practica"]').click();
  check(await page.locator('#practica').evaluate(e=>Math.abs(e.getBoundingClientRect().top)<5),'inicio de práctica visible');
  await page.locator('.sidebar [data-tab="inicio"]').click();
  check(await page.evaluate(()=>window.scrollY)===0,'volver al inicio');
  await page.screenshot({path:'output/playwright/portal-final-2026.png'});
  await page.setViewportSize({width:390,height:844});
  check(await page.evaluate(()=>getComputedStyle(document.querySelector('.sidebar')).position)!=='sticky','menú móvil no cubre lectura');
  check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'sin desborde móvil');
  await page.screenshot({path:'output/playwright/inicio-mobile-2026.png',fullPage:true});
  await page.setViewportSize({width:1440,height:960});
  if(failures.length)throw Error(JSON.stringify({checks,failures,rects}));
  return {checks,failures,rects};
}
