"""Integra entregables revisados; no modifica las guías ni bancos de los autores."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent

def rooted(text,folder='estudio-2026'):
    def link(m):
        label,url=m.groups()
        if url.startswith(('http:','https:','#')):return m.group(0)
        url=url.removeprefix('../')
        stem=url.split('#')[0]
        if not (ROOT/stem).exists() and (ROOT/folder/stem).exists():url=folder+'/'+url
        return '['+label+']('+url+')'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)

old=ROOT/'historico-prepublicacion'
old.mkdir(exist_ok=True)
for name in ['MANUAL-DE-PREPARACION.md','PLAN-DE-ESTUDIO.md','GUIA-CONCURSO-2026.md','BIBLIOTECA-Y-TEMARIO.md','README.md','REVISION-CONTENIDO.md','VERIFICACION.md','preguntas.json']:
    if (ROOT/name).exists() and not (old/name).exists():(old/name).write_bytes((ROOT/name).read_bytes())

guide=(old/'GUIA-CONCURSO-2026.md').read_text(encoding='utf-8')
guide=guide.replace('Verificación: 5 de octubre de 2026. Preparación con Codex. Esta guía cubre las reglas publicadas y las nueve etapas; el programa y los videos de 2026 todavía no están publicados. Ningún material histórico permite prometer conocer el examen futuro completo.', 'Verificación: 12 de octubre de 2026. Preparación con Codex. Esta guía cubre las nueve etapas. Ya se publicó el índice y los cinco módulos para conocimientos específicos; la página oficial aclara que las etapas previas no se rigen por esa bibliografía. Los videos de evaluación y sus cuestionarios futuros no se conocen de antemano.')
guide=guide.replace('## Lo urgente y lo que todavía falta','## Estado de la convocatoria y lo que falta confirmar')
guide=guide.replace('Inscripción exclusivamente digital desde','El plazo publicado de inscripción fue exclusivamente digital desde',1)
guide=guide.replace('El programa y material oficial se anuncian para **el 12/10/2026**. Los horarios y fechas de evaluación serán comunicados por Recursos Humanos; pueden modificarse cuando existan circunstancias que lo ameriten. Hoy no corresponde inventar un cronograma de exámenes. [A26 art. 4.d, art. 5 y art. 20, pp. 11 y 19]', 'El programa oficial **ya está publicado**: índice y cinco módulos, 220 páginas PDF, más las remisiones indicadas dentro de los módulos. La [publicación del material](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026-material-de-estudio/) informa que las fechas de exámenes aún no están definidas. Consultar [la actualización y comparación](ACTUALIZACION-2026.md) y [la biblioteca](BIBLIOTECA-Y-TEMARIO.md). Los horarios y fechas serán comunicados por Recursos Humanos. [A26 art. 4.d, art. 5 y art. 20, pp. 11 y 19]')
guide=guide.replace('**Hay una contradicción en el micrositio:** el resumen del examen específico dice 50 minutos, pero las preguntas frecuentes dicen 40. La acordada dispone expresamente **40 minutos para 50 preguntas**; la noticia oficial también informa 40. Entrenar con 40 y solicitar aclaración', '**Hay una contradicción visible:** la nueva página del material y el resumen del examen específico dicen **50 minutos**, pero las preguntas frecuentes dicen 40. La acordada dispone expresamente **40 minutos para 50 preguntas**; la noticia oficial también informa 40. El portal permite entrenar con ambos tiempos. Comprobar la comunicación de Recursos Humanos y solicitar aclaración')
guide=guide.replace('**50 preguntas, 4 opciones, una correcta, 40 minutos**.', '**50 preguntas, 4 opciones, una correcta. La publicación del material indica 50 minutos; la Acordada 32.748 dispone 40 minutos.**')
guide=guide.replace('El ritmo global es 48 segundos por pregunta, incluyendo marcación y control. Practicar 50 en 40 minutos;', 'El ritmo global es 60 segundos por pregunta con 50 minutos, o 48 segundos con 40, incluyendo marcación y control. Practicar con ambos tiempos;')
guide=guide.replace('Sirve para adelantar conceptos; no demuestra que todas esas unidades entrarán en 2026.', 'Se aprovechan los conceptos que coinciden con el programa nuevo. Para preparar el escrito, estudiar desde 2026; la [comparación detallada](ACTUALIZACION-2026.md) señala cambios y exclusiones de prioridad.')
start=guide.index('## Checklist de actualización del 12 de octubre')
guide=guide[:start]+'''## Checklist actual de preparación

- [x] Descargar índice y cinco módulos oficiales, registrar URL y huellas SHA-256.
- [x] Revisar 220 páginas y remisiones; incluir normas obligatorias y anexo juvenil de octubre.
- [x] Comparar 2023 con 2026; renovar preguntas específicas y conservar antecedentes identificados.
- [ ] Comprobar nombre/datos en nómina publicada y conservar constancia de inscripción.
- [ ] Confirmar cronograma, sede y horarios por la web oficial.
- [ ] Confirmar disponibilidad y plazo de habilitación de cada video y formulario.
- [ ] Confirmar la duración definitiva del escrito ante la discrepancia de 40/50 minutos.
- [ ] Leer el instructivo OMR cuando se publique; seguir el marcado indicado.
- [ ] Solicitar adecuaciones razonables aplicables por canal formal con anticipación.
- [ ] Resolver prácticas 20/15, 10/30 y 50/50; agregar 50/40 como entrenamiento exigente.

Las guías, tarjetas y preguntas son elaboración independiente. La bibliografía nueva cubre conocimientos específicos; no autoriza afirmar que se conocen los videos, textos o preguntas futuras ni la batería del psicofísico.
'''
(ROOT/'GUIA-CONCURSO-2026.md').write_text(guide,encoding='utf-8')
(ROOT/'PLAN-DE-ESTUDIO.md').write_bytes((ROOT/'PLAN-DE-ESTUDIO-2026.md').read_bytes())

m13=rooted((ROOT/'estudio-2026/GUIA-M1-M3.md').read_text(encoding='utf-8'))
m1,m3=m13.split('## Módulo 3.',1)
m2=rooted((ROOT/'estudio-2026/GUIA-M2.md').read_text(encoding='utf-8'))
m45=rooted((ROOT/'estudio-2026/GUIA-M4-M5.md').read_text(encoding='utf-8'))
anexos=rooted((ROOT/'estudio-2026/GUIA-ANEXOS.md').read_text(encoding='utf-8'))
intro='''# Manual completo de preparación · programa 2026

Actualizado al 12/10/2026. Explicaciones originales basadas en los cinco módulos oficiales, con enlaces a la página PDF que permite profundizar. Leer el original completo, después recuperar sin mirar y comprobar con práctica. Este manual desarrolla conocimientos específicos; las otras etapas tienen su [guía de reglas](GUIA-CONCURSO-2026.md).

Recorrido: módulos 1 a 5, lecturas obligatorias y anexo penal juvenil. Consultar las [erratas y límites de revisión](REVISION-CONTENIDO.md) cuando dos pasajes difieren. La página PDF cuenta desde la primera hoja del archivo, aunque la numeración impresa sea distinta. Las pistas de memoria son ayudas didácticas, no categorías jurídicas nuevas.

'''
def lower_title(s):return re.sub(r'^# ', '## ',s,count=1)
manual=intro+lower_title(m1)+'\n\n'+lower_title(m2)+'\n\n## Módulo 3.'+m3+'\n\n'+lower_title(m45)+'\n\n'+lower_title(anexos)
(ROOT/'MANUAL-DE-PREPARACION.md').write_text(manual,encoding='utf-8')

program=json.loads((ROOT/'biblioteca/2026/programa/manifest.json').read_text(encoding='utf-8'))['documentos']
refs=json.loads((ROOT/'biblioteca/2026/referencias/manifest.json').read_text(encoding='utf-8'))
hist=json.loads((ROOT/'biblioteca/catalogo.json').read_text(encoding='utf-8'))
table='\n'.join('| ['+r['titulo'].replace('Concurso-Ingreso-2026-SCJM-','').replace('-Material-de-Estudio','').replace('-',' ')+']('+r['archivo']+') | '+str(r['paginas'])+' | [Fuente oficial]('+r['url']+') |' for r in program)
reftable='\n'.join('| ['+r['titulo'].replace('-',' ')+']('+r.get('lectura',r.get('archivo',r['url']))+') | '+str(r.get('paginas','HTML'))+' | '+r['alcance']+' | [Fuente]('+r['url']+') |' for r in refs)
biblio='''# Biblioteca y temario 2026

Consulta y descarga: 12/10/2026. El [sitio oficial](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026-material-de-estudio/) publica seis PDF para el escrito de conocimientos específicos. Los originales completos están disponibles localmente y en el lector del portal. Las guías, preguntas y memoria visual son elaboración de apoyo.

## Programa oficial completo · 220 páginas PDF

| Archivo | Páginas | Procedencia |
|---|---:|---|
'''+table+'''

Los 27 apartados principales del índice se registran en el portal con acceso al inicio de cada sección. Se conservan también todos los subapartados, tablas, gráficos y bibliografía de los originales. Las portadas y gráficos cuentan como páginas: 220 no significa 220 páginas de prosa.

## Referencias fuera del programa: alcance individual

No hay que atribuir el mismo peso a una lectura obligatoria, un anexo, una recomendación, una norma citada y un enlace de servicio. Esta tabla conserva esas diferencias. Las copias HTML incluyen enlace al original y fecha; no son PDF paginados ni una edición normativa propia.

| Recurso local | Extensión | Alcance de estudio | Procedencia |
|---|---:|---|---|
'''+reftable+'''

El anexo procesal juvenil está escaneado: el lector conserva sus 29 hojas; hay OCR auxiliar separado que puede omitir palabras. Para interpretar una regla, prevalece la imagen original, no el OCR. La revisión del anexo se realizó también visualmente. El DL 560 descargado es una copia antigua; no llamarlo texto consolidado a octubre de 2026. Leer los artículos requeridos con la modificatoria indicada y las advertencias de revisión.

M2 pp. 110–113 contiene separador y tres gráficos concursales dentro del mismo PDF. Los enlaces a las leyes juveniles se encuentran en p. 109. Las demás remisiones normativas se explican en [la guía de anexos](estudio-2026/GUIA-ANEXOS.md) y [la revisión M2](estudio-2026/REVISION-M2.md). La sola cita de una ley o de un libro no permite deducir que se exige memorizarlo entero.

## Material anterior conservado

El [catálogo histórico](biblioteca/catalogo.json) contiene '''+str(len(hist))+''' registros de la investigación previa. Incluye programa y módulos 2023, normas, fuentes audiovisuales y antecedentes. Los archivos descargados siguen en `biblioteca/pdf`, `biblioteca/2023` y sus carpetas de texto. El [inventario anterior](historico-prepublicacion/BIBLIOTECA-Y-TEMARIO.md) conserva su detalle y sus límites de descarga: un registro no equivale necesariamente a un PDF disponible.

Las guías y preguntas anteriores al 12/10 están en `historico-prepublicacion/`. Las 140 preguntas específicas históricas se retiraron del simulador activo; no se borraron del archivo. Los ejercicios institucionales son práctica general: se enlazan a fuentes 2026 cuando coinciden y mantienen identificadas las ampliaciones históricas. Comprensión lectora usa textos originales de entrenamiento. No son cuestionarios de los videos 2026.

## Trazabilidad y uso de los enlaces

- [Manifiesto del programa](biblioteca/2026/programa/manifest.json): URL, fecha, tamaño, páginas, SHA-256 y enlaces internos extraídos.
- [Manifiesto de referencias](biblioteca/2026/referencias/manifest.json): procedencia, alcance, copia local, estado HTTP y SHA-256.
- Cada pregunta específica, tarjeta y nodo conceptual enlaza a su PDF y página. Las normas disponibles sólo como HTML se identifican por artículo, sin inventar una página.
- En simulacro, la referencia aparece al corregir; en estudio, mapas y tarjetas se puede abrir para profundizar.
- `#page=18` pide al visor abrir la hoja 18. Si el visor del dispositivo ignora ese fragmento, escribir el número indicado en su control de páginas. El lector del portal también permite elegir documento y hoja.

## Qué todavía depende de publicaciones oficiales

El cronograma, los videos de evaluación, el texto del examen de comprensión, los cuestionarios reales y las instrucciones OMR no pueden reconstruirse a partir del programa específico. Se preparan sus habilidades y reglas publicadas, manteniendo esa diferencia. No se encontró una rectificación formal de la discrepancia de duración 40/50 minutos.
'''
(ROOT/'BIBLIOTECA-Y-TEMARIO.md').write_text(biblio,encoding='utf-8')

review='''# Revisión de contenido y límites de la preparación

Fecha: 12/10/2026. Se revisaron íntegramente los cinco PDF 2026 (217 páginas) y su índice (3 páginas), además de las remisiones y anexos detallados en la biblioteca. La lectura textual se complementó con inspección de imágenes, tablas y gráficos. Las hojas escaneadas del Código juvenil se revisaron visualmente; el OCR es auxiliar. Esto no equivale a una fe de erratas oficial ni permite conocer preguntas futuras.

## Informes de revisión completos

- [Módulos 1 y 3: cobertura de las 62 páginas, remisiones y contraste 2023](estudio-2026/REVISION-M1-M3.md).
- [Módulo 2: cobertura de las 113 páginas, normas, plazos y reformas](estudio-2026/REVISION-M2.md).
- [Módulos 4 y 5: cobertura de las 42 páginas, protocolo y comparación](estudio-2026/REVISION-M4-M5.md).
- [Lecturas obligatorias y anexo juvenil: revisión independiente](estudio-2026/REVISION-ANEXOS.md).
- [Práctica institucional: 40 preguntas y fuentes actualizadas](estudio-2026/REVISION-INSTITUCIONAL.md).
- [Comprensión lectora: 60 preguntas contrastadas con seis pasajes](estudio-2026/REVISION-LECTURA.md).
- [Comparación general con 2023](ACTUALIZACION-2026.md).
- [Cómo usar el taller de dominio](estudio-2026/COMO-USAR-TALLER.md).
- [Revisión independiente de diagnósticos y videos](estudio-2026/REVISION-INDEPENDIENTE-TALLER.md).
- [Revisión de rúbricas, pares y secuencias](estudio-2026/REVISION-INDEPENDIENTE-RUBRICAS.md).
- [Revisión independiente de los dos nuevos pasajes](estudio-2026/REVISION-INDEPENDIENTE-LECTURA-TALLER.md).

## Hallazgos que cambian cómo estudiar

1. **M1 no termina en sus 39 páginas:** las lecturas obligatorias de p. 39 están incorporadas con detalle. La remisión sobre Ley 9423 al M2 es incompleta; se añadió la ley y un mapa de lectura por artículo.
2. **Régimen juvenil:** el cuerpo de M2 conserva una referencia al código provincial «en estudio», pero su anexo remite a normas publicadas en octubre. Se estudian Ley 9735 y el Código completo; se distingue el modelo anterior de Ley 6354 del nuevo anexo y su régimen de aplicación. Publicación y vigencia son conceptos distintos: no se atribuye una fecha de vigencia sólo por la fecha de publicación.
3. **Plazos y gráficos:** algunos esquemas simplifican supuestos. La revisión M2 diferencia el texto del módulo y los artículos consultados; las preguntas evitan convertir contradicciones en claves ambiguas.
4. **Violencia laboral:** el protocolo original distingue remisión penal de oficio y supuestos que requieren voluntad/conformidad. No memorizar la frase abreviada del módulo como consentimiento obligatorio en toda situación.
5. **Duración:** nueva página 50 minutos frente a Acordada/FAQ 40. Ambos relojes son práctica y la diferencia sigue pendiente de confirmación oficial.

## Banco de práctica y fuentes

Las preguntas específicas nuevas cubren los cinco módulos, los 27 apartados principales y el anexo juvenil. Todas tienen cuatro opciones distintas, una clave, explicación y referencia local a página PDF. Algunas reglas requieren más de una fuente; se conservan ambas. Los gráficos no se sustituyen por texto extraído incompleto.

No se atribuye a este banco distribución oficial, dificultad oficial ni carácter predictivo. Diez preguntas por módulo es un modo de entrenamiento, no un peso anunciado por la Corte. Comprensión tiene seis textos originales con diez preguntas cada uno; se corrige desde cada pasaje. La práctica institucional general no equivale a las dos jornadas reales de video.

## Verificación técnica y preservación

Los controles de formato, rutas y páginas verifican integridad, no por sí solos exactitud jurídica. Los informes documentan el contraste del contenido con sus fuentes y la revisión independiente del anexo. [VERIFICACION.md](VERIFICACION.md) registra las comprobaciones efectivamente realizadas en lógica y navegador.

Se conservan documentos prepublicación, biblioteca histórica e historial del navegador. Los errores de preguntas específicas retiradas no vuelven a seleccionarse en el banco actual. Los resultados anteriores se identifican como históricos y no se mezclan con la estadística por módulo 2026.

## Límites pendientes

No se dispone de un banco oficial completo de exámenes anteriores ni de las preguntas futuras. Los fragmentos auténticos recuperados siguen identificados en [Evaluaciones reales y antecedentes](EVALUACIONES-REALES-Y-ANTECEDENTES.md). No se publica una batería psicofísica oficial que permita prepararla como examen de opciones. Las recomendaciones de estudio y los objetivos 45–50/50 y 9–10/10 son metas personales, no garantías.
'''
(ROOT/'REVISION-CONTENIDO.md').write_text(review,encoding='utf-8')

readme='''# Preparación judicial Mendoza · programa 2026

Abrí [index.html](index.html) con doble clic. Conservá la carpeta completa: funciona sin instalar programas y sin subir resultados. El PDF se abre en el visor del navegador; cada enlace indica su página. En modo estudio podés profundizar mientras practicás; en simulacro, al corregir.

## Por dónde empezar

1. Abrí «Mi recorrido», leé las reglas y el plan de 28 sesiones.
2. Elegí módulo: PDF completo, guía explicada y práctica por apartado.
3. Entrá en [Mapas y tarjetas](memoria.html): ocultá conceptos, reconstruí conexiones y respondé antes de revelar.
4. Entrá al [Taller de dominio](taller.html): explicá sin opciones, compará casos, ordená procesos y corregí errores. Conservá los diagnósticos A/B para comprobar aprendizaje con preguntas nuevas.
5. Alterná comprensión y las dos jornadas de video originales; corregí desde las fuentes. [Rutina del taller](estudio-2026/COMO-USAR-TALLER.md).
6. Consultá las novedades oficiales para fechas, videos y hoja de respuestas.

## Contenido actualizado al 12/10/2026

- Índice y cinco módulos oficiales completos: 220 páginas PDF, con biblioteca y lector por hoja.
- Lecturas obligatorias, normas citadas y anexo penal juvenil de octubre, con alcance documentado.
- Manual completo, guías por módulo, comparación 2023/2026, revisión de erratas y nueve etapas del concurso.
- Banco específico renovado, ejercicios generales y seis textos originales de comprensión; corrección explicada y fuente.
- Mapas, tarjetas, contrastes y casos con recuerdo activo y repaso espaciado.
- Taller: 90 abiertas con rúbricas, 20 pares de casos, 12 secuencias, 20 errores, dos diagnósticos específicos, dos textos nuevos y dos videos de seis minutos con cuestionarios.
- Cuaderno imprimible y archivo histórico conservado.

Las cantidades verificadas se muestran en el portal y en [VERIFICACION.md](VERIFICACION.md). Las guías y ejercicios son preparación independiente; los originales oficiales se mantienen intactos.

## Reglas que conviene tener presentes

La bibliografía nueva es exclusiva de conocimientos específicos. Los videos reales y el texto de comprensión se conocerán según su convocatoria. El escrito tiene 50 preguntas: la nueva página dice 50 minutos, pero Acordada/FAQ dicen 40; el simulador ofrece ambos. No se encontró una rectificación formal que cierre la diferencia. Los mínimos son 15/20 en cada jornada virtual, 7/10 lectura y 35/50 específicos. Entrenar no acredita aprobación ni garantiza nota.

Los avances completados se guardan sólo en este navegador. En el simulador principal cerrar una práctica en curso pierde esas respuestas; el taller conserva borradores y el vencimiento del cuestionario. «Descargar mis avances» del cuaderno exporta resultados, cobertura, memoria visual y taller. El taller también permite descargar su registro. No hay importación automática. Se conserva el historial anterior y se lo identifica como preparación previa.

## Documentos y reproducibilidad

[Manual](MANUAL-DE-PREPARACION.md) · [Plan](PLAN-DE-ESTUDIO.md) · [Etapas](GUIA-CONCURSO-2026.md) · [Biblioteca](BIBLIOTECA-Y-TEMARIO.md) · [Comparación](ACTUALIZACION-2026.md) · [Revisión](REVISION-CONTENIDO.md) · [Ejercicios imprimibles](CUADERNO-DE-EJERCICIOS.html).

Para regenerar datos después de editar guías y bancos: `python integrar_documentos_2026.py`, `python integrar_bancos_2026.py`, `python generar_fuentes_2026.py`, `python preparar_material.py`, `python preparar_taller.py`. Verificar con `node verificar_simulador.cjs`; empaquetar con `python empaquetar.py`. Los MP4 se conservan ya renderizados. Estos scripts requieren Python y las bibliotecas usadas por los autores; estudiar con el paquete generado no requiere ejecutarlos.

Procedencia: [material oficial 2026](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026-material-de-estudio/), [convocatoria y novedades](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026/). Fecha de descarga, URL y SHA-256 en los manifiestos de la biblioteca.

## Copia del repositorio y paquetes ZIP

El repositorio conserva el proyecto completo, incluidos PDF, guías, datos y videos terminados. Después de descargarlo o clonarlo, abrí `index.html` manteniendo sus carpetas. Los ZIP generados se conservan localmente y se excluyen de Git porque superan 100 MiB por archivo. Para generar el paquete completo ejecutá `python empaquetar.py`; comprueba el contenido con CRC y SHA-256 y escribe `PREPARACION-JUDICIAL-MENDOZA-2026-TALLER.zip`. El ZIP preparatorio antiguo también deja de versionarse; su copia local y el historial Git se conservan.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')

name=ROOT/'EVALUACIONES-REALES-Y-ANTECEDENTES.md'
s=name.read_text(encoding='utf-8')
notice='\nActualización 12/10/2026: los antecedentes siguientes conservan su carácter histórico. El escrito actual se prepara desde [el programa 2026 y su comparación](ACTUALIZACION-2026.md). Este documento no convierte los fragmentos recuperados en un examen completo ni en preguntas de la convocatoria actual.\n'
if 'Actualización 12/10/2026:' not in s:s=s.replace('\n', '\n'+notice,1)
name.write_text(s,encoding='utf-8')
print(json.dumps({'manual_palabras':len(manual.split()),'referencias':len(refs),'programa_paginas':sum(r['paginas'] for r in program)},ensure_ascii=False))
