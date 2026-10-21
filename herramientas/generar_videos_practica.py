"""Dos videos de práctica originales: escenas, subtítulos y preguntas trazables."""
from pathlib import Path
import json,html,requests,random
ROOT=Path(__file__).resolve().parent
V=ROOT/'videos';V.mkdir(exist_ok=True)
PROJ=ROOT/'video-estudio'
modules=json.loads((ROOT/'indice-2026.json').read_text(encoding='utf-8'))
files={m['id']:m['archivo'] for m in modules}
def source(m,p):return {'file':files[m],'page':p,'label':'M'+str(m)}
def scene(title,text,nodes,m,p):return {'title':title,'text':text,'nodes':nodes,'sources':[source(m,p)]}
one=[
scene('Funciones y límites','Esta jornada es una práctica original. Observá relaciones, órganos y límites. Después responderás veinte preguntas sobre lo expuesto. No es un video institucional oficial ni anticipa sus preguntas.','Observar|Relacionar|Responder',1,2),
scene('Cuatro elementos del Estado','Población es el conjunto humano; territorio es el ámbito espacial. Poder es la capacidad de alcanzar fines mediante autoridad y coerción. Gobierno es el conjunto de órganos que ejerce funciones. El gobierno puede cambiar sin que desaparezca el Estado.','Territorio|Población|Poder|Gobierno',1,2),
scene('La Constitución organiza y limita','La Constitución es la norma fundamental. Organiza el poder y reconoce derechos. Una norma inferior no adquiere superioridad por ser más reciente. La supremacía exige compatibilidad con la Constitución y con el bloque constitucional aplicable.','Norma fundamental|Organización|Derechos|Límites',1,3),
scene('Representativa, republicana y federal','La forma representativa permite ejercer el gobierno mediante representantes. La república comprende responsabilidad, publicidad de actos y división de poderes. El federalismo distribuye poder entre el orden federal y entidades locales autónomas; no borra las competencias provinciales.','Representantes|Responsabilidad|Publicidad|Autonomía',1,6),
scene('Órgano y función no son lo mismo','La función no se determina sólo por el nombre del órgano. Un tribunal ejerce jurisdicción al resolver una controversia y también administra cuando organiza recursos o concede una licencia. Debe distinguirse la actividad realizada y su régimen.','Tribunal|Resolver|Organizar|Actividad concreta',1,21),
scene('La Corte también administra','El módulo distingue funciones administrativa, jurisdiccional y dirimente de la Suprema Corte. La superintendencia comprende organización y facultades disciplinarias. Conceder una licencia o nombrar personal son actuaciones administrativas; no constituyen sentencias sobre el fondo de un litigio.','Administrar|Juzgar|Dirimir|Superintendencia',1,28),
scene('El proceso sustituye la fuerza privada','El proceso ofrece un medio pacífico para debatir un conflicto ante un tercero imparcial. Las partes plantean sus pretensiones y defensas. La imparcialidad exige que quien decide no se convierta en defensor de una de las partes.','Conflicto|Debate|Tercero imparcial|Decisión',2,2),
scene('Investigar y decidir se separan','En el modelo acusatorio, el Ministerio Público Fiscal investiga y sostiene la acusación en delitos de acción pública. Los jueces resuelven peticiones desde una posición imparcial y controlan medidas que afectan derechos. Investigar y acusar no equivale a juzgar.','Fiscalía: investigar|Fiscalía: acusar|Juez: controlar|Juez: decidir',2,93),
scene('La OGAP organiza la gestión','La Ley 9040 consolidó la separación entre jurisdicción y gestión administrativa penal. La OGAP organiza audiencias y tareas de gestión. El juez resuelve las cuestiones jurídicas. Administrar una agenda no atribuye potestad para decidir prisión preventiva.','OGAP: agenda|OGAP: gestión|Juez: jurisdicción|Ley 9040',2,94),
scene('La defensa y el jurado','La defensa contradice la acusación y ejerce derechos del imputado. En juicio por jurados, el jurado decide los hechos y emite veredicto; el juez técnico dirige el debate, resuelve cuestiones jurídicas e imparte instrucciones sobre el derecho aplicable.','Defensa: contradecir|Jurado: hechos|Jurado: veredicto|Juez: derecho',2,94),
scene('Publicidad con límites','El acceso a información judicial no implica que cualquier persona pueda consultar cualquier actuación sin condiciones. Hay reglas de publicidad y supuestos de reserva, como las medidas cautelares antes de ser trabadas. Digitalizar un expediente no elimina esos límites.','Publicidad|Reserva|Permisos|Expediente digital',2,6),
scene('Recuperá las relaciones','Sin mirar apuntes, recordá qué integra el Estado y qué distingue órgano de función. Separá fiscal, juez, defensa, jurado y OGAP. En el cuestionario elegí por el contenido del video, no por suponer atribuciones que aquí no se expusieron.','Elementos|Funciones|Roles|Límites',2,94)
]
two=[
scene('Atender con derechos','Esta segunda jornada es una práctica original de observación. El foco es dignidad, comunicación, violencia y accesibilidad. El cuestionario posterior se basa sólo en estas escenas; no corresponde a videos oficiales del concurso.','Dignidad|Comunicación|Barreras|Orientación',5,2),
scene('Dignidad e igualdad','Los derechos humanos corresponden a las personas por su dignidad. La igualdad y la no discriminación orientan la actuación estatal. Una situación de vulnerabilidad no disminuye derechos: obliga a identificar barreras y respuestas que permitan ejercerlos.','Dignidad|Igualdad|No discriminación|Barreras',3,6),
scene('Respetar, proteger y garantizar','Respetar exige que el Estado se abstenga de vulnerar derechos. Proteger requiere enfrentar afectaciones provenientes de terceros. Garantizar exige condiciones y medidas que posibiliten su ejercicio. No son tres nombres para una única conducta.','Respetar: abstenerse|Proteger: terceros|Garantizar: posibilitar',3,10),
scene('Escuchar antes de suponer','Un servicio centrado en la ciudadanía identifica la necesidad real. Las preguntas abiertas permiten describir la situación. Parafrasear con palabras propias ayuda a confirmar lo comprendido. La orientación debe dejar claros los próximos pasos.','Preguntar|Escuchar|Parafrasear|Orientar',5,16),
scene('Lenguaje claro y precisión','Usar lenguaje claro implica facilitar que la persona encuentre, comprenda y use la información. No exige eliminar condiciones relevantes ni prometer un resultado. La explicación debe conservar precisión y distinguir recepción de un trámite de decisión sobre su fondo.','Encontrar|Comprender|Usar|Conservar precisión',5,9),
scene('Tipo y modalidad de violencia','Los tipos describen formas de daño: física, psicológica, sexual, económica o patrimonial, simbólica y política. Las modalidades describen ámbitos o contextos. Un mismo hecho puede combinar un tipo psicológico con una modalidad laboral o digital.','Tipo: forma de daño|Modalidad: contexto|Pueden combinarse',4,5),
scene('Revictimización','Pedir una narración innecesaria y repetida o culpabilizar a quien sufrió violencia puede revictimizar. La atención debe evitar prácticas que agreguen daño. No hay que sustituir el trato respetuoso por prejuicios sobre cómo debería reaccionar una persona afectada.','Evitar repetición innecesaria|No culpabilizar|Trato respetuoso',4,8),
scene('Cuatro lugares donde buscar barreras','La accesibilidad incluye barreras físicas, comunicacionales, actitudinales y tecnológicas. Una rampa no resuelve un formulario que no puede utilizar un lector de pantalla. Facilitar el acceso exige mirar el recorrido completo y las necesidades reales.','Edificio|Mensaje|Trato|Sistema',5,19),
scene('Diseño universal y ajuste razonable','El diseño universal busca que servicios y entornos puedan ser utilizados por la mayor diversidad de personas desde su concepción. Un ajuste razonable responde a una necesidad particular. No conviene exigir una solución idéntica si esa uniformidad mantiene una barrera.','Diseñar para diversidad|Ajustar ante necesidad|Remover barreras',5,19),
scene('Orientar y derivar','El agente debe brindar información precisa sobre el trámite dentro de su competencia. Si una consulta excede sus atribuciones, deriva al área adecuada con información de contacto útil. Orientar no equivale a decidir una controversia ni a garantizar una sentencia favorable.','Información de trámite|Competencia|Derivación|Sin promesas de sentencia',5,16),
scene('Comprobar que la explicación sirva','Antes de cerrar la atención, se verifica si la persona comprendió qué hacer. Pedir que explique el primer paso ayuda a detectar una duda pendiente. La transparencia y la eficiencia no consisten sólo en hablar rápido o reducir controles sin comprender su finalidad.','Verificar comprensión|Primer paso|Dudas pendientes|Respuesta útil',5,16),
scene('Recordá antes de responder','Recuperá obligaciones, barreras y diferencias: tipo y modalidad; diseño universal y ajuste; orientación y decisión. En el cuestionario posterior, cada respuesta debe apoyarse en lo que estas escenas expusieron.','Diferencias|Necesidades|Derechos|Próximos pasos',5,16)
]

def q(prompt,correct,wrong,sc,index,vid):
    options=[correct]+wrong;random.Random(vid+'-'+str(index)).shuffle(options)
    return {'id':vid+'Q'+str(index+1).zfill(2),'prompt':prompt,'options':options,'correct':options.index(correct),'why':correct+' La escena '+str(sc+1)+' desarrolla esta relación.','sources':[{'file':'videos/'+vid.lower()+'.mp4','time':sc*30,'label':'Escena '+str(sc+1)}]}

qa1=[
(1,'¿Qué elemento identifica al conjunto humano?','Población',['Gobierno','Territorio','Poder']),
(1,'¿Qué diferencia al gobierno del poder?','El gobierno identifica órganos; el poder una capacidad estatal',['Ambos designan exclusivamente a jueces','El gobierno es sólo territorio','El poder es únicamente la población']),
(2,'¿Qué posición tiene la Constitución en lo expuesto?','Norma fundamental que organiza y limita',['Reglamento interno de cada oficina','Resolución individual de trámite','Norma que sólo regula la agenda judicial']),
(2,'¿Qué sucede con una norma inferior por ser más reciente?','La fecha no le otorga superioridad constitucional',['Pasa automáticamente sobre la Constitución','Deroga siempre los derechos constitucionales','Se convierte en poder constituyente']),
(3,'¿Qué relación describe el federalismo?','Distribución entre orden federal y entidades locales autónomas',['Eliminación de toda competencia provincial','Concentración de toda decisión en una oficina','Organización exclusiva de partidos políticos']),
(3,'¿Qué rasgos republicanos se mencionaron?','Responsabilidad, publicidad de actos y división de poderes',['Reserva de todos los actos y poder sin límites','Duración vitalicia de todos los cargos','Identidad entre gobierno y población']),
(4,'¿Cómo se reconoce la función de una actuación?','Por la actividad concreta y su régimen',['Sólo por el nombre del edificio','Por la cantidad de empleados del órgano','Por la rapidez con que se realiza']),
(4,'¿Qué ejemplo fue administrativo?','Conceder una licencia al personal',['Resolver el fondo de una controversia','Decidir culpabilidad en un juicio','Impartir veredicto como jurado']),
(5,'¿Qué comprende la superintendencia expuesta?','Organización y facultades disciplinarias',['La investigación fiscal de todos los delitos','La defensa particular de cada litigante','La representación de cada parte']),
(5,'¿Qué tres funciones de la Corte nombró el video?','Administrativa, jurisdiccional y dirimente',['Únicamente fiscal y defensiva','Legislativa, partidaria y comercial','Investigadora, policial y electoral sin límites']),
(6,'¿Qué finalidad del proceso se destacó?','Debatir pacíficamente un conflicto ante tercero imparcial',['Autorizar la fuerza privada','Eliminar todas las defensas','Garantizar éxito al primero que consulte']),
(6,'¿Qué exige la imparcialidad del decisor?','No convertirse en defensor de una parte',['Ayudar sólo a quien parezca más convincente','Asumir simultáneamente la acusación','Decidir por la presión de las partes']),
(7,'¿Quién investiga y sostiene acusación en acción pública?','El Ministerio Público Fiscal',['La OGAP por manejar la agenda','El jurado antes del juicio','El agente de atención al público']),
(7,'¿Qué tarea judicial aparece durante investigación?','Controlar medidas que afectan derechos y resolver peticiones',['Reunir prueba para sostener la acusación','Organizar únicamente calendarios','Defender los intereses de una sola parte']),
(8,'¿Qué tarea corresponde a la OGAP?','Organizar audiencias y gestión administrativa',['Decidir prisión preventiva','Emitir veredicto sobre hechos','Sostener la acusación fiscal']),
(8,'¿Qué ley se nombró respecto de reorganización penal?','Ley 9040',['Ley 9423','Ley 26618','Ley 9665']),
(9,'¿Qué función de la defensa se expuso?','Contradecir la acusación y ejercer derechos del imputado',['Organizar la agenda de todos los jueces','Emitir el veredicto del jurado','Reemplazar el control judicial de medidas']),
(9,'¿Cómo se distinguen jurado y juez técnico?','El jurado decide hechos y veredicto; el juez dirige y resuelve derecho',['El jurado administra OGAP; el juez investiga','Ambos son empleados de mesa de entradas','El jurado sostiene acusación y el juez representa a la defensa']),
(10,'¿Digitalizar un expediente elimina restricciones de acceso?','No; siguen las reglas de publicidad y reserva',['Sí, todo queda abierto sin condiciones','Sí, si alguien conoce el número','Sólo elimina restricciones penales, sin excepción']),
(10,'¿Qué ejemplo de reserva se mencionó?','Medidas cautelares antes de ser trabadas',['Todos los actos republicanos para siempre','Todo trámite de orientación general','La totalidad de Constitución y leyes'])]
qa2=[
(1,'¿En qué se fundamentan los derechos humanos expuestos?','En la dignidad de las personas',['En acertar un cuestionario','En pertenecer al Estado','En la condición de funcionario']),
(1,'¿Qué implica identificar vulnerabilidad?','Detectar barreras sin disminuir derechos',['Reducir derechos por la situación personal','Presumir incapacidad para toda decisión','Aplicar siempre idéntica solución sin considerar necesidades']),
(2,'¿Qué expresa la obligación de respeto?','Abstenerse de vulnerar derechos',['Garantizar siempre un resultado favorable','Resolver únicamente ataques de particulares','Derivar toda actuación sin intervenir']),
(2,'¿Qué relación corresponde a proteger?','Enfrentar afectaciones provenientes de terceros',['Actuar sólo cuando el Estado es autor directo','Eliminar la posibilidad de reclamar','Limitar derechos por comodidad de la oficina']),
(3,'¿Para qué sirve una pregunta abierta?','Para que la persona describa su necesidad real',['Para imponer una respuesta predeterminada','Para decidir la sentencia en ventanilla','Para reemplazar la escucha por suposiciones']),
(3,'¿Qué busca el parafraseo?','Confirmar lo entendido con palabras propias',['Repetir tecnicismos sin explicación','Cambiar el sentido del pedido','Cerrar la consulta antes de oírla']),
(4,'¿Qué debe conservar una explicación clara?','Precisión y condiciones relevantes',['Una promesa de resultado favorable','La menor cantidad de palabras aunque falten requisitos','Todos los tecnicismos sin adaptar']),
(4,'¿Qué diferencia debe mantenerse sobre un trámite?','Recepción no equivale a decisión sobre el fondo',['Recibir significa siempre aprobar','Orientar equivale a sentenciar','Un comprobante demuestra que ganó la parte']),
(5,'¿Qué distinguen tipo y modalidad de violencia?','Forma de daño y ámbito o contexto',['Edad y domicilio de las partes','Órgano competente y monto de tasa','Dos listas que se excluyen necesariamente']),
(5,'¿Puede un hecho combinar afectación psicológica y modalidad digital?','Sí, describen ejes distintos',['No, sólo admite una clasificación total','Sólo si no ocurrió en ámbito privado','No, digital es un tipo corporal']),
(6,'¿Qué práctica puede revictimizar?','Exigir narración innecesaria repetida o culpabilizar',['Evitar preguntas irrelevantes','Tratar con respeto','Escuchar sin imponer prejuicios']),
(6,'¿Qué criterio de trato se expuso?','Evitar prejuicios sobre cómo debería reaccionar la persona',['Exigir una reacción emocional única','Desconfiar siempre si no llora','Valorar la consulta según estereotipos']),
(7,'¿Qué barreras se deben mirar?','Físicas, comunicacionales, actitudinales y tecnológicas',['Sólo el acceso al edificio','Sólo las computadoras de la oficina','Únicamente los horarios internos']),
(7,'¿Por qué una rampa no basta en el ejemplo?','Puede quedar una barrera en el formulario digital',['Porque toda rampa reduce la accesibilidad','Porque el trato no importa','Porque los sistemas nunca generan barreras']),
(8,'¿Qué caracteriza el diseño universal?','Considerar diversidad de personas desde la concepción',['Esperar siempre una petición individual para diseñar','Ofrecer una barrera idéntica a todos','Crear un servicio exclusivo para una única necesidad']),
(8,'¿Qué distingue al ajuste razonable?','Responder a una necesidad particular',['Sustituir toda regla por voluntad del agente','Eliminar toda condición del trámite','Mantener uniformidad aunque impida el acceso']),
(9,'¿Qué corresponde cuando la consulta excede competencia del agente?','Derivar adecuadamente con información útil',['Decidir igual para ahorrar tiempo','Prometer sentencia favorable','Dejar a la persona sin orientación']),
(9,'¿Qué límite conserva la orientación?','No decide controversias ni garantiza sentencias',['Permite resolver cualquier conflicto por cortesía','Reemplaza a los órganos jurisdiccionales','Otorga competencia por experiencia personal']),
(10,'¿Cómo se verifica comprensión en el ejemplo?','Pidiendo que explique el primer paso que daría',['Preguntando sólo si escuchó cada palabra','Acelerando el cierre de la conversación','Repitiendo una frase técnica más fuerte']),
(10,'¿Qué significa eficiencia en lo expuesto?','No basta hablar rápido ni quitar controles sin comprenderlos',['Eliminar todo control sin evaluar finalidad','Derivar cualquier material aunque sea ilegible','Medir sólo segundos de atención'])]
extra1={1:[(1,3)],2:[(1,4),(1,5)],3:[(1,7),(1,8)],4:[(1,29)],5:[(1,29)],6:[(2,3)],10:[(2,5)]}
extra2={1:[(3,8),(3,16),(3,18)],2:[(3,11),(3,12),(3,13)],4:[(5,3),(2,7)],5:[(4,6)],7:[(5,20),(5,21)],9:[(1,32)],10:[(5,15),(5,17)]}
for group,extra in [(one,extra1),(two,extra2)]:
    for index,refs in extra.items():group[index]['sources'] += [source(m,p) for m,p in refs]
two[2]['text']='Respetar exige que el Estado se abstenga de vulnerar derechos. Proteger requiere enfrentar afectaciones provenientes de terceros y es parte de garantizar los derechos. Garantizar exige condiciones y medidas que posibiliten su ejercicio. Estas obligaciones se relacionan; sus ejemplos no describen una única conducta.'
payload=[]
for number,(scenes,items) in enumerate([(one,qa1),(two,qa2)],1):
    vid='V'+str(number)
    for i,s in enumerate(scenes):s.update(start=i*30,duration=30)
    questions=[q(prompt,c,w,sc,i,vid) for i,(sc,prompt,c,w) in enumerate(items)]
    for question,(sc,*_) in zip(questions,items):question['sources']+=scenes[sc]['sources']
    title='Funciones y roles de justicia' if number==1 else 'Derechos, atención y accesibilidad'
    rec={'id':vid,'title':title,'description':'Clip original de lectura y esquemas; veinte preguntas sobre su contenido.','duration':360,'file':'videos/'+vid.lower()+'.mp4','captions':'videos/'+vid.lower()+'.vtt','narration':False,'scenes':scenes,'questions':questions}
    payload.append(rec)
    def stamp(t):return f'{int(t)//3600:02}:{int(t)//60%60:02}:{int(t)%60:02}.000'
    (V/(vid.lower()+'.vtt')).write_text('WEBVTT\n\n'+'\n\n'.join(stamp(s['start'])+' --> '+stamp(s['start']+s['duration'])+'\n'+s['text'] for s in scenes),encoding='utf-8')
    css='''body{margin:0;background:#f1f5f8;font-family:Segoe UI,Arial,sans-serif;color:#1c354a}#root{position:relative;width:1280px;height:720px;overflow:hidden}.clip{position:absolute;inset:0;padding:56px 70px;background:#f1f5f8;box-sizing:border-box}.tag{font-size:18px;letter-spacing:2px;font-weight:700;color:#285dab}h1{font:normal 46px/1.15 Georgia,serif;margin:20px 0 30px;max-width:1100px}.nodes{display:flex;gap:14px;flex-wrap:wrap;margin:20px 0 28px}.node{background:white;border:1px solid #a9bdcc;border-top:5px solid #285dab;padding:16px 21px;font-size:23px;font-weight:600;max-width:480px;line-height:1.35}.caption{font-size:24px;line-height:1.65;max-width:1100px;background:white;border-left:4px solid #0b7274;padding:20px 28px}.foot{position:absolute;bottom:28px;left:70px;font-size:15px;color:#536c7d}'''
    clips=[]
    for i,s in enumerate(scenes):
        nodes=''.join('<div class="node">'+html.escape(n)+'</div>' for n in s['nodes'].split('|'))
        clips.append(f'<section id="{vid.lower()}-escena-{i+1:02}" class="clip" data-start="{s["start"]}" data-duration="30" data-track-index="1"><div class="tag">JORNADA {number} · ESCENA {i+1} / 12</div><h1>'+html.escape(s['title'])+'</h1><div class="nodes">'+nodes+'</div><div class="caption">'+html.escape(s['text'])+'</div><div class="foot">Práctica original · '+html.escape(s['sources'][0]['label'])+' · página PDF '+str(s['sources'][0]['page'])+'</div></section>')
    doc='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'+title+'</title><script src="assets/gsap.min.js"></script><style>'+css+'</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="360" data-width="1280" data-height="720">'+''.join(clips)+'</div><script>window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});tl.to({}, {duration:360});window.__timelines.main=tl;</script></body></html>'
    doc=doc.replace('width:1280px;height:720px','width:100%;height:100%').encode('ascii','xmlcharrefreplace').decode('ascii')
    (PROJ/(vid.lower()+'.source')).write_text(doc,encoding='utf-8')
    (V/(vid.lower()+'-transcripcion.html')).write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>'+title+'</title><style>body{max-width:900px;margin:40px auto;padding:20px;font:18px/1.8 system-ui}</style><h1>'+title+'</h1><p>Práctica original, no video oficial. Transcripción y páginas de respaldo.</p>'+''.join('<h2>'+stamp(s['start'])+' · '+html.escape(s['title'])+'</h2><p>'+html.escape(s['text'])+'</p>'+''.join('<a href="../'+ref['file']+'#page='+str(ref['page'])+'">'+ref['label']+' · PDF '+str(ref['page'])+'</a> · ' for ref in s['sources']) for s in scenes)+'</html>',encoding='utf-8')
(ROOT/'taller-datos/videos.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
(PROJ/'index.html').write_bytes((PROJ/'v1.source').read_bytes())
assets=PROJ/'assets';assets.mkdir(exist_ok=True)
if not (assets/'gsap.min.js').exists():
    r=requests.get('https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js',timeout=30);r.raise_for_status();(assets/'gsap.min.js').write_bytes(r.content)
print(json.dumps({'videos':2,'escenas':24,'preguntas':40,'duracion_segundos_cada_uno':360},ensure_ascii=False))
