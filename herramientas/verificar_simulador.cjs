// Lógica real del portal con DOM mínimo. La verificación visual se realiza aparte.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'..'),storage=new Map(),elements=new Map();
function element(id){if(!elements.has(id))elements.set(id,{innerHTML:'',textContent:'',value:'',disabled:false,classList:{toggle(){},add(){},remove(){}},addEventListener(){},querySelector(){return null},querySelectorAll(){return []},scrollIntoView(){},focus(){}});return elements.get(id)}
for(const [id,value] of Object.entries({mode:'estudio',moduleFilter:'0',topicFilter:'',examMinutes:'50',examDistribution:'balanced',readerDoc:'0',readerPage:'1'}))element(id).value=value;
const historic={fecha:'2026-10-05T12:00:00Z',tipo:'especificos',aciertos:40,total:50,sinResponder:0};
storage.set('pjm-history',JSON.stringify([historic]));storage.set('pjm-errors',JSON.stringify(['P001']));
const context={window:{location:{search:''}},document:{getElementById:element,querySelector(){return null},querySelectorAll(){return []},addEventListener(){}},localStorage:{getItem:k=>storage.has(k)?storage.get(k):null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)},setInterval(){return 1},clearInterval(){},setTimeout(){},Date,Math,JSON,Set,Map,Array,Object,Number,String,Boolean,RegExp,Blob,URL,URLSearchParams,console};
vm.createContext(context);
for(const file of ['datos-preguntas.js','fuentes-2026.js','app.js'])vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),context);
const run=code=>vm.runInContext(code,context),rows=()=>JSON.parse(storage.get('pjm-history'));
let checks=0;function check(fn){fn();checks++}
async function start(mode){element('mode').value=mode;await run('start()');return run('current.length')}
function complete(n){run(`current.forEach((q,i)=>{if(i<${n})answers[i]=q.correcta});finish(activeMode)`)}
(async()=>{
  check(()=>assert.deepEqual(rows(),[historic]));
  check(()=>assert.equal(run('modules.length'),5));
  check(()=>assert.equal(run('modules.reduce((n,m)=>n+m.apartados.length,0)'),27));
  check(()=>assert.equal(run("bank.filter(q=>q.etapa==='especificos'&&q.version!==2026).length"),0));
  check(()=>assert(run('numBank.length')>=100));
  await start('especificos');
  check(()=>assert.equal(run('current.length'),50));
  check(()=>assert.equal(run('activeMinutes'),50));
  check(()=>assert.equal(element('clock').textContent,'50:00'));
  for(let m=1;m<=5;m++)check(()=>assert.equal(run(`current.filter(q=>q.modulo===${m}).length`),10));
  check(()=>assert(run('current.every(q=>Array.isArray(q._order)&&q._order.length===q.opciones.length)')));
  check(()=>assert(!element('exam').innerHTML.includes('source-link')));
  complete(50);
  check(()=>assert.equal(rows()[0].aciertos,50));
  check(()=>assert.equal(rows()[0].sinResponder,0));
  check(()=>assert(element('exam').innerHTML.includes('.pdf#page=')));
  const size=rows().length;run('finish(activeMode)');check(()=>assert.equal(rows().length,size));

  // Distribución proporcional al peso del temario (M1:9, M2:24, M3:6, M4:4, M5:7)
  element('examDistribution').value='proportional';
  await start('especificos');
  check(()=>assert.equal(run('current.length'),50));
  for(const [m,cnt] of [[1,9],[2,24],[3,6],[4,4],[5,7]]){
    check(()=>assert.equal(run(`current.filter(q=>q.modulo===${m}).length`),cnt));
  }
  run('finished=true');

  element('examMinutes').value='40';element('examDistribution').value='random';await start('especificos');
  check(()=>assert.equal(run('activeMinutes'),40));
  check(()=>assert.equal(run('new Set(current.map(q=>q.id)).size'),50));
  complete(35);check(()=>assert.equal(rows()[0].sinResponder,15));
  check(()=>assert(element('exam').innerHTML.includes('Alcanzaste el mínimo')));
  // Con 15 sin responder (>3), las omitidas no deben contaminar pjm-errors
  storage.set('pjm-errors','[]');
  await start('especificos');
  complete(10); // 10 correctas, 40 sin responder
  check(()=>assert.deepEqual(JSON.parse(storage.get('pjm-errors')),[]));

  // Entrenador de números, plazos y competencias
  element('moduleFilter').value='0';element('topicFilter').value='';
  await start('numeros');
  check(()=>assert.equal(run('current.length'),12));
  check(()=>assert(run("current.every(q=>q.etapa==='numeros')")));
  complete(12);
  check(()=>assert.equal(rows()[0].aciertos,12));

  storage.set('pjm-errors','[]');
  element('moduleFilter').value='4';element('topicFilter').value='4.3';await start('estudio');
  check(()=>assert(run("current.every(q=>q.modulo===4&&q.subtema==='4.3')")));
  check(()=>assert.equal(run('deadline'),null));
  check(()=>assert(element('exam').innerHTML.includes('Profundizar en la fuente')));
  const studyTotal=run('current.length');complete(studyTotal-1);
  await start('errores');check(()=>assert.equal(run('current.length'),1));complete(1);
  check(()=>assert.deepEqual(JSON.parse(storage.get('pjm-errors')),[]));
  storage.set('pjm-errors','["P001"]');await start('errores');
  check(()=>assert(element('exam').textContent.includes('No hay errores activos')));
  await start('lectura');
  check(()=>assert.equal(run('current.length'),10));
  check(()=>assert.equal(run('new Set(current.map(q=>q.texto)).size'),1));
  check(()=>assert.equal(run('activeMinutes'),30));
  complete(7);check(()=>assert.equal(rows()[0].aciertos,7));
  check(()=>assert.equal(rows()[0].sinResponder,3));
  check(()=>assert(element('exam').innerHTML.includes('id="readingText"')));
  check(()=>assert(element('exam').innerHTML.includes('href="#readingText"')));
  await start('institucional');check(()=>assert.equal(run('current.length'),20));
  check(()=>assert.equal(run('activeMinutes'),15));
  run('deadline=Date.now()-1000;tick(activeMode)');
  check(()=>assert.equal(rows()[0].sinResponder,20));
  check(()=>assert.equal(run('finished'),true));
  check(()=>assert.deepEqual(rows().at(-1),historic));
  run('renderHistory()');check(()=>assert(element('history').innerHTML.includes('Resultado conservado')));
  element('readerDoc').value='1';element('readerPage').value='999';run('renderReader()');
  check(()=>assert.equal(Number(element('readerPage').value),39));
  check(()=>assert(element('pdfFrame').src.includes('?p=39#page=39')));
  element('readerPage').value='-8';run('renderReader()');check(()=>assert.equal(Number(element('readerPage').value),1));
  check(()=>assert(!run("markdown('[x](javascript:alert)')").includes('href=')));
  check(()=>assert(run("markdown('[ir](#seccion-1)')").includes('href="#seccion-1"')));
  const multi=run('bank.find(q=>q.fuentes?.length>1)');
  check(()=>assert.equal((run('questionSources(bank.find(q=>q.fuentes?.length>1))').match(/Abrir PDF/g)||[]).length,multi.fuentes.length));
  const historyBefore=storage.get('pjm-history');storage.set('pjm-history','[]');storage.set('pjm-seen-2026','{}');
  element('moduleFilter').value='1';element('topicFilter').value='';
  const seenStudy=new Set(),totalM1=run("bank.filter(q=>q.etapa==='especificos'&&q.modulo===1).length");
  while(seenStudy.size<totalM1){
    await start('estudio');const ids=run('current.map(q=>q.id)');
    check(()=>assert(ids.every(id=>!seenStudy.has(id))));
    ids.forEach(id=>seenStudy.add(id));
    // Simula abandonar, sin guardar resultado: la exposición igual debe persistir.
    run('finished=true');
  }
  check(()=>assert.equal(seenStudy.size,totalM1));
  await start('estudio');check(()=>assert(element('exam').innerHTML.includes('Ya viste todas')));run('finished=true');
  storage.set('pjm-seen-2026','{}');
  element('examDistribution').value='balanced';const examIds=new Set();
  for(let i=0;i<3;i++){
    await start('especificos');const ids=run('current.map(q=>q.id)');
    check(()=>assert.equal(ids.length,50));check(()=>assert(ids.every(id=>!examIds.has(id))));
    ids.forEach(id=>examIds.add(id));run('finished=true');
  }
  storage.set('pjm-seen-2026','{}');const readTexts=new Set();
  const totalTexts=run("new Set(bank.filter(q=>q.etapa==='lectura').map(q=>q.texto)).size");
  for(let i=0;i<totalTexts;i++){
    await start('lectura');const text=run('current[0].texto');
    check(()=>assert(!readTexts.has(text)));readTexts.add(text);run('finished=true');
  }
  await start('lectura');check(()=>assert.equal(run('current.length'),10));run('finished=true');
  storage.set('pjm-seen-2026','{}');
  const oldIds=run("bank.filter(q=>q.etapa==='especificos'&&q.modulo===1).slice(0,10).map(q=>q.id)");
  storage.set('pjm-history',JSON.stringify([{fecha:'2026-10-14',items:oldIds.map(id=>({id}))}]));
  await start('estudio');check(()=>assert(run('current.map(q=>q.id)').every(id=>!oldIds.includes(id))));run('finished=true');
  const counters=JSON.parse(storage.get('pjm-seen-2026'));check(()=>assert.equal(counters[oldIds[0]].count,1));
  run('seenQuestions()');check(()=>assert.equal(JSON.parse(storage.get('pjm-seen-2026'))[oldIds[0]].count,1));
  storage.set('pjm-history',historyBefore);

  // Verificación de Taller (deduplicación de intentos y normalización de fecha due a medianoche)
  const tallerElements=new Map();
  function tEl(id){if(!tallerElements.has(id))tallerElements.set(id,{innerHTML:'',textContent:'',value:'all',hidden:false,disabled:false,style:{setProperty(){}},options:[],classList:{toggle(){}},setAttribute(){},addEventListener(){},querySelector(){return null},querySelectorAll(){return []},scrollIntoView(){},focus(){},insertAdjacentHTML(){}});return tallerElements.get(id)}
  const tStorage=new Map();
  tStorage.set('pjm-taller-2026',JSON.stringify({
    version:1,
    seen:{},
    results:[
      {attemptId:'A-2',kind:'open',id:'O1',assessment:'self',due:Date.now()+86400000*3,finished:2000},
      {attemptId:'A-1',kind:'open',id:'O1',assessment:'pending',finished:1000}
    ],
    drafts:{}
  }));
  const tCtx={window:{location:{search:''}},document:{getElementById:tEl,querySelector(){return null},querySelectorAll(){return []}},localStorage:{getItem:k=>tStorage.get(k)||null,setItem:(k,v)=>tStorage.set(k,v)},setInterval(){return 1},clearInterval(){},setTimeout(){},Date,Math,JSON,Set,Map,Array,Object,Number,String,Boolean,RegExp,Blob,URL,URLSearchParams,console};
  vm.createContext(tCtx);
  for(const file of ['taller-datos.js','taller.js'])vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),tCtx);
  const latestFree=vm.runInContext('window.TallerTest.latestFreeResults()',tCtx);
  check(()=>assert.equal(latestFree.length,1));
  check(()=>assert.equal(latestFree[0].attemptId,'A-2'));
  const dueTs=vm.runInContext('window.TallerTest.dueMidnight(1)',tCtx);
  check(()=>assert.equal(new Date(dueTs).getHours(),0));
  check(()=>assert.equal(new Date(dueTs).getMinutes(),0));

  console.log(`PASS: ${checks} comprobaciones. Selección, distribución proporcional, entrenador de números, rotación sin repetición, migración de historial, abandonos, taller y lector.`);
  fs.mkdirSync(path.join(root,'validaciones'),{recursive:true});
  fs.writeFileSync(path.join(root,'validaciones','validacion-logica-2026.json'),JSON.stringify({fecha:'2026-10-21',comprobaciones:checks,resultado:'PASS',alcance:'DOM simulado; selección sin repetición, distribución proporcional, entrenador de números, taller y lector'},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
