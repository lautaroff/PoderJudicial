"""Integra entregables revisados; no modifica las guías ni bancos de los autores."""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
ESTUDIO = ROOT / 'estudio-2026'


def rooted(text, folder='estudio-2026'):
    def link(m):
        label, url = m.groups()
        if url.startswith(('http:', 'https:', '#')):
            return m.group(0)
        url = url.removeprefix('../')
        stem = url.split('#')[0]
        if not (ROOT / stem).exists() and (ROOT / folder / stem).exists():
            url = folder + '/' + url
        return '[' + label + '](' + url + ')'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)


old = ROOT / 'historico' / 'prepublicacion'
old.mkdir(parents=True, exist_ok=True)

guide = (old / 'GUIA-CONCURSO-2026.md').read_text(encoding='utf-8')
guide = guide.replace('Verificación: 5 de octubre de 2026. Preparación con Codex. Esta guía cubre las reglas publicadas y las nueve etapas; el programa y los videos de 2026 todavía no están publicados. Ningún material histórico permite prometer conocer el examen futuro completo.', 'Verificación: 12 de octubre de 2026. Preparación con Codex. Esta guía cubre las nueve etapas. Ya se publicó el índice y los cinco módulos para conocimientos específicos; la página oficial aclara que las etapas previas no se rigen por esa bibliografía. Los videos de evaluación y sus cuestionarios futuros no se conocen de antemano.')
guide = guide.replace('## Lo urgente y lo que todavía falta', '## Estado de la convocatoria y lo que falta confirmar')
guide = guide.replace('Inscripción exclusivamente digital desde', 'El plazo publicado de inscripción fue exclusivamente digital desde', 1)
guide = guide.replace('El programa y material oficial se anuncian para **el 12/10/2026**. Los horarios y fechas de evaluación serán comunicados por Recursos Humanos; pueden modificarse cuando existan circunstancias que lo ameriten. Hoy no corresponde inventar un cronograma de exámenes. [A26 art. 4.d, art. 5 y art. 20, pp. 11 y 19]', 'El programa oficial **ya está publicado**: índice y cinco módulos, 220 páginas PDF, más las remisiones indicadas dentro de los módulos. La [publicación del material](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026-material-de-estudio/) informa que las fechas de exámenes aún no están definidas. Consultar [la actualización y comparación](estudio-2026/ACTUALIZACION-2026.md) y [la biblioteca](estudio-2026/BIBLIOTECA-Y-TEMARIO.md). Los horarios y fechas serán comunicados por Recursos Humanos. [A26 art. 4.d, art. 5 y art. 20, pp. 11 y 19]')
guide = guide.replace('**Hay una contradicción en el micrositio:** el resumen del examen específico dice 50 minutos, pero las preguntas frecuentes dicen 40. La acordada dispone expresamente **40 minutos para 50 preguntas**; la noticia oficial también informa 40. Entrenar con 40 y solicitar aclaración', '**Hay una contradicción visible:** la nueva página del material y el resumen del examen específico dicen **50 minutos**, pero las preguntas frecuentes dicen 40. La acordada dispone expresamente **40 minutos para 50 preguntas**; la noticia oficial también informa 40. El portal permite entrenar con ambos tiempos. Comprobar la comunicación de Recursos Humanos y solicitar aclaración')
guide = guide.replace('**50 preguntas, 4 opciones, una correcta, 40 minutos**.', '**50 preguntas, 4 opciones, una correcta. La publicación del material indica 50 minutos; la Acordada 32.748 dispone 40 minutos.**')
guide = guide.replace('El ritmo global es 48 segundos por pregunta, incluyendo marcación y control. Practicar 50 en 40 minutos;', 'El ritmo global es 60 segundos por pregunta con 50 minutos, o 48 segundos con 40, incluyendo marcación y control. Practicar con ambos tiempos;')
guide = guide.replace('Sirve para adelantar conceptos; no demuestra que todas esas unidades entrarán en 2026.', 'Se aprovechan los conceptos que coinciden con el programa nuevo. Para preparar el escrito, estudiar desde 2026; la [comparación detallada](estudio-2026/ACTUALIZACION-2026.md) señala cambios y exclusiones de prioridad.')
start = guide.index('## Checklist de actualización del 12 de octubre')
guide = guide[:start] + '''## Checklist actual de preparación

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
(ESTUDIO / 'GUIA-CONCURSO-2026.md').write_text(guide, encoding='utf-8')

m13 = rooted((ESTUDIO / 'GUIA-M1-M3.md').read_text(encoding='utf-8'))
m1, m3 = m13.split('## Módulo 3.', 1)
m2 = rooted((ESTUDIO / 'GUIA-M2.md').read_text(encoding='utf-8'))
m45 = rooted((ESTUDIO / 'GUIA-M4-M5.md').read_text(encoding='utf-8'))
anexos = rooted((ESTUDIO / 'GUIA-ANEXOS.md').read_text(encoding='utf-8'))
intro = '''# Manual completo de preparación · programa 2026

Actualizado al 12/10/2026. Explicaciones originales basadas en los cinco módulos oficiales, con enlaces a la página PDF que permite profundizar. Leer el original completo, después recuperar sin mirar y comprobar con práctica. Este manual desarrolla conocimientos específicos; las otras etapas tienen su [guía de reglas](estudio-2026/GUIA-CONCURSO-2026.md).

Recorrido: módulos 1 a 5, lecturas obligatorias y anexo penal juvenil. Consultar las [erratas y límites de revisión](estudio-2026/REVISION-CONTENIDO.md) cuando dos pasajes difieren. La página PDF cuenta desde la primera hoja del archivo, aunque la numeración impresa sea distinta. Las pistas de memoria son ayudas didácticas, no categorías jurídicas nuevas.

'''


def lower_title(s):
    return re.sub(r'^# ', '## ', s, count=1)


manual = intro + lower_title(m1) + '\n\n' + lower_title(m2) + '\n\n## Módulo 3.' + m3 + '\n\n' + lower_title(m45) + '\n\n' + lower_title(anexos)
(ESTUDIO / 'MANUAL-DE-PREPARACION.md').write_text(manual, encoding='utf-8')

program = json.loads((ROOT / 'biblioteca/2026/programa/manifest.json').read_text(encoding='utf-8'))['documentos']
refs = json.loads((ROOT / 'biblioteca/2026/referencias/manifest.json').read_text(encoding='utf-8'))
hist = json.loads((ROOT / 'biblioteca/catalogo.json').read_text(encoding='utf-8'))
table = '\n'.join('| [' + r['titulo'].replace('Concurso-Ingreso-2026-SCJM-', '').replace('-Material-de-Estudio', '').replace('-', ' ') + '](' + r['archivo'] + ') | ' + str(r['paginas']) + ' | [Fuente oficial](' + r['url'] + ') |' for r in program)
reftable = '\n'.join('| [' + r['titulo'].replace('-', ' ') + '](' + r.get('lectura', r.get('archivo', r['url'])) + ') | ' + str(r.get('paginas', 'HTML')) + ' | ' + r['alcance'] + ' | [Fuente](' + r['url'] + ') |' for r in refs)
biblio = '''# Biblioteca y temario 2026

Consulta y descarga: 12/10/2026. El [sitio oficial](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026-material-de-estudio/) publica seis PDF para el escrito de conocimientos específicos. Los originales completos están disponibles localmente y en el lector del portal. Las guías, preguntas y memoria visual son elaboración de apoyo.

## Programa oficial completo · 220 páginas PDF

| Archivo | Páginas | Procedencia |
|---|---:|---|
''' + table + '''

Los 27 apartados principales del índice se registran en el portal con acceso al inicio de cada sección. Se conservan también todos los subapartados, tablas, gráficos y bibliografía de los originales. Las portadas y gráficos cuentan como páginas: 220 no significa 220 páginas de prosa.

## Referencias fuera del programa: alcance individual

No hay que atribuir el mismo peso a una lectura obligatoria, un anexo, una recomendación, una norma citada y un enlace de servicio. Esta tabla conserva esas diferencias. Las copias HTML incluyen enlace al original y fecha; no son PDF paginados ni una edición normativa propia.

| Recurso local | Extensión | Alcance de estudio | Procedencia |
|---|---:|---|---|
''' + reftable + '''

El anexo procesal juvenil está escaneado: el lector conserva sus 29 hojas; hay OCR auxiliar separado que puede omitir palabras. Para interpretar una regla, prevalece la imagen original, no el OCR. La revisión del anexo se realizó también visualmente. El DL 560 descargado es una copia antigua; no llamarlo texto consolidado a octubre de 2026. Leer los artículos requeridos con la modificatoria indicada y las advertencias de revisión.

M2 pp. 110–113 contiene separador y tres gráficos concursales dentro del mismo PDF. Los enlaces a las leyes juveniles se encuentran en p. 109. Las demás remisiones normativas se explican en [la guía de anexos](estudio-2026/GUIA-ANEXOS.md) y [la revisión M2](estudio-2026/REVISION-M2.md). La sola cita de una ley o de un libro no permite deducir que se exige memorizarlo entero.

## Material anterior conservado

El [catálogo histórico](biblioteca/catalogo.json) contiene ''' + str(len(hist)) + ''' registros de la investigación previa. Incluye programa y módulos 2023, normas, fuentes audiovisuales y antecedentes. Los archivos descargados siguen en `biblioteca/pdf`, `biblioteca/2023` y sus carpetas de texto. El [inventario anterior](historico/prepublicacion/BIBLIOTECA-Y-TEMARIO.md) conserva su detalle y sus límites de descarga: un registro no equivale necesariamente a un PDF disponible.

Las guías y preguntas anteriores al 12/10 están en `historico/prepublicacion/`. Las 140 preguntas específicas históricas se retiraron del simulador activo; no se borraron del archivo. Los ejercicios institucionales son práctica general: se enlazan a fuentes 2026 cuando coinciden y mantienen identificadas las ampliaciones históricas. Comprensión lectora usa textos originales de entrenamiento. No son cuestionarios de los videos 2026.

## Trazabilidad y uso de los enlaces

- [Manifiesto del programa](biblioteca/2026/programa/manifest.json): URL, fecha, tamaño, páginas, SHA-256 y enlaces internos extraídos.
- [Manifiesto de referencias](biblioteca/2026/referencias/manifest.json): procedencia, alcance, copia local, estado HTTP y SHA-256.
- Cada pregunta específica, tarjeta y nodo conceptual enlaza a su PDF y página. Las normas disponibles sólo como HTML se identifican por artículo, sin inventar una página.
- En simulacro, la referencia aparece al corregir; en estudio, mapas y tarjetas se puede abrir para profundizar.
- `#page=18` pide al visor abrir la hoja 18. Si el visor del dispositivo ignora ese fragmento, escribir el número indicado en su control de páginas. El lector del portal también permite elegir documento y hoja.

## Qué todavía depende de publicaciones oficiales

El cronograma, los videos de evaluación, el texto del examen de comprensión, los cuestionarios reales y las instrucciones OMR no pueden reconstruirse a partir del programa específico. Se preparan sus habilidades y reglas publicadas, manteniendo esa diferencia. No se encontró una rectificación formal de la discrepancia de duración 40/50 minutos.
'''
(ESTUDIO / 'BIBLIOTECA-Y-TEMARIO.md').write_text(biblio, encoding='utf-8')

print(json.dumps({'manual_palabras': len(manual.split()), 'referencias': len(refs), 'programa_paginas': sum(r['paginas'] for r in program)}, ensure_ascii=False))
