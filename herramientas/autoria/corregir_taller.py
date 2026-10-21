"""Correcciones puntuales verificadas en fuentes primarias; no descarga ni altera originales."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent
def edit_json(name, edit):
    p=ROOT/name
    data=json.loads(p.read_text(encoding='utf-8'))
    edit(data)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def annex(data):
    q=next(q for q in data if q['id']=='N2A-033')
    q['pregunta']='Recibida la solicitud de custodia, ¿dentro de qué plazo máximo convocará a audiencia el órgano jurisdiccional según el art. 47?'
    q['explicacion']='Recibida la solicitud, el órgano jurisdiccional convocará a audiencia dentro del plazo máximo de dos días hábiles. Finalizado el acto, resolverá en forma oral e inmediata y diferirá los fundamentos dentro de los tres días hábiles. El texto exige que el adolescente sea oído y prevé los participantes de la audiencia.'
edit_json('bancos-2026/anexos.json',annex)
for name in ['estudio-2026/GUIA-ANEXOS.md','estudio-2026/REVISION-ANEXOS.md']:
    p=ROOT/name;s=p.read_text(encoding='utf-8')
    s=s.replace('La audiencia debe celebrarse dentro de dos días hábiles','Recibida la solicitud, el órgano jurisdiccional convocará a audiencia dentro del plazo máximo de dos días hábiles')
    s=s.replace('con posibilidad de diferir los fundamentos hasta tres días hábiles','y diferirá los fundamentos dentro de los tres días hábiles')
    s=s.replace('La audiencia debe celebrarse dentro de 2 días hábiles; resolución oral e inmediata, con posibilidad de diferir fundamentos hasta 3 días hábiles.', 'Recibida la solicitud, el órgano jurisdiccional convocará a audiencia dentro del máximo de 2 días hábiles; finalizado el acto resolverá oral e inmediatamente y diferirá los fundamentos dentro de los 3 días hábiles.')
    s=s.replace('la audiencia de custodia debe **celebrarse** en dos días hábiles y el juez puede diferir fundamentos hasta tres días hábiles', 'recibida la solicitud de custodia, el órgano jurisdiccional **convocará a audiencia** dentro del máximo de dos días hábiles; finalizado el acto resolverá oral e inmediatamente y **diferirá los fundamentos** dentro de los tres días hábiles')
    if 'Control literal del art. 47' not in s:
        s+='\n\nControl literal del art. 47 (PDF 14): dice «convocará a audiencia» dentro del máximo de dos días hábiles desde la solicitud; finalizado el acto resolverá oral e inmediatamente y «diferirá los fundamentos» dentro de los tres días hábiles. La pregunta N2A-033 y la guía usan esta formulación, sin transformar la convocatoria en una regla distinta de celebración ni presentar el diferimiento como potestativo.\n'
    p.write_text(s,encoding='utf-8')
def diagnostic(data):
    for f in data['forms']:
        for q in f['questions']:
            if q['id']=='DA-40':q['prompt']=q['prompt'].replace('¿Qué combinación contradice el material?','¿Qué combinación refuta esas afirmaciones y coincide con el material?')
            if q['id']=='DA-44':q['prompt']='Una oficina recibe y registra una queja, pero nunca comunica medidas ni realiza un cierre con aprendizaje y ajustes. ¿Qué quedó incompleto?'
            if q['id']=='DB-03':q['why']='La Constitución distingue al Presidente, jefe supremo de la Nación, jefe del gobierno y responsable político de la administración general (art. 99 inc. 1), del Jefe de Gabinete, que ejerce la administración general (art. 100 inc. 1). Ambos textos se transcriben en M1, página PDF 16.'
            if q['id']=='DB-50' and not any(s.get('page')==15 for s in q['sources']):q['sources'].append({'file':q['sources'][0]['file'],'page':15,'label':'M5 · confidencialidad'})
edit_json('taller-datos/diagnosticos.json',diagnostic)
def opened(data):
    for q in data:
        if q['id']=='O1-009':
            if 'Identificá sus autoridades' not in q['prompt']:q['prompt']+=' Identificá sus autoridades.'
            q['model']=q['model'].replace('Sus misiones y autoridades son distintas.', 'El Procurador General encabeza el MPF; el Defensor o la Defensora General encabeza Defensa y Pupilar. Sus misiones y autoridades son distintas.')
        if q['id']=='O1-014':q['prompt']=q['prompt'].replace('decisión individual de traslado','decisión administrativa individual de traslado de un agente a otra oficina')
        if q['id']=='O2-003':
            q['model']=q['model'].replace('resuelve admisión y producción de prueba','resuelve la admisión y ordena la producción de prueba')
            q['checkpoints'][1]['text']='Ubica admisión y orden de producción de prueba en inicial; recepción oral en final.'
        if q['id']=='O2-006' and 'percepción' not in q['prompt']:q['prompt']+=' Agregá el límite de percepción extrajudicial de los rubros ejecutados.'
        if q['id']=='O2-024':
            q['model']=q['model'].replace('por complejidad','por la cantidad de hechos atribuidos o su evidente complejidad')
            q['checkpoints'][1]['text']='Condiciona ampliación única hasta cinco a pedido previo y cantidad de hechos o evidente complejidad.'
        if q['id'] in ['O2-024','O2-028','O2-030']:
            if 'Regla de cómputo:' not in q['model']:q['model']+=' Regla de cómputo: los plazos expresados en días se cuentan como días hábiles por el art. 4 y las remisiones a los arts. 194–196 CPP; no convertir horas o meses en días ni ignorar supuestos expresamente formulados como días corridos.'
            if not any(s.get('page')==2 for s in q['sources']):q['sources'].append({'file':'biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf','page':2,'label':'Código juvenil · art. 4, cómputo'})
edit_json('taller-datos/abiertas.json',opened)
def cases(data):
    for q in data:
        if q['id']=='C3-003':
            q['b']['text']=q['b']['text'].replace('carece de conexión y habilidad para completarlo','mantiene la misma habilidad, pero carece de conexión para completarlo')
            q['changed']='La disponibilidad de conexión; se mantiene la misma habilidad para utilizar el canal.'
        if q['id']=='C5-001':
            q['a']['prompt']='Redactá una respuesta breve y el cierre de la atención. Usá [fecha], [hora] y [lugar/modalidad] como marcadores de los datos verificados; no inventes valores.'
            q['a']['model']='Su audiencia es el [fecha], a las [hora], en [lugar/modalidad]. Estos son los datos confirmados en el sistema. ¿Podría decirme cuándo y dónde se presentará, para comprobar que la información quedó clara? Los marcadores representan los datos verificados; no se agregan consecuencias ni resultados del juicio.'
edit_json('taller-datos/casos.json',cases)
print('Correcciones de art. 47, DA-40, DA-44 y DB-50 aplicadas.')
