from pathlib import Path
import fitz,json,re
root=Path(__file__).resolve().parent
rows=json.loads((root/'catalogo.json').read_text(encoding='utf8'))
titles={}
for p in (root/'pdf').glob('*.pdf'):
 if 'Modulo-3' not in p.name and 'Modulo-1' not in p.name:continue
 for page in fitz.open(p):
  lines=[x.strip() for x in page.get_text().splitlines() if x.strip()]
  for i,line in enumerate(lines):
   if 'youtu' in line:
    u=re.search(r'https?://\S+',line)
    if u and i:titles[u.group(0)]=lines[i-1]
for r in rows:
 if r['url'] in titles:r['titulo']=titles[r['url']]
 if 'youtu' in r['url']:r['tipo']='video histórico enlazado';r['limite_verificacion']='HTTP 200 sólo confirma página, no reproducción ni disponibilidad de subtítulos'
 r['etiquetas']=['histórico-2023','fuente-oficial-o-enlazada-en-material-oficial']
(root/'catalogo.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
text='''# Biblioteca y temario histórico para adelantar el ingreso judicial de Mendoza

Verificado el 5 de octubre de 2026. El material oficial de la convocatoria 2026 se anuncia para el 12 de octubre. Esta biblioteca conserva antecedentes y no certifica que todos estos contenidos entren en 2026. El programa 2023 y sus cuatro módulos se descargaron íntegros desde el sitio oficial y tienen texto extraído para búsqueda. Los enlaces adicionales aparecen en esos documentos o en el índice oficial histórico. El catálogo JSON conserva URL, HTTP, tamaño, SHA-256 y páginas de cada PDF.

## Qué estudiar del antecedente 2023

- Módulo 1: Constitución y derechos humanos; división de funciones del Estado; derecho federal, común, administrativo y local; historia judicial mendocina; misión y objetivos; Corte, tribunales, circunscripciones, fueros e instancias; MPF y Defensa; Junta Electoral; Consejo de la Magistratura; Jury; organización administrativa; empleado público y violencia de género. Leyes referenciadas en el programa: 552, 8008, 8928, 2551, 6561, 4970, 8946, 4969 y 9003.
- Módulo 2: vocabulario jurídico claro; competencia, principios, procesos, etapas, plazos, actuaciones y publicidad por fuero. Civil/comercial, tributario, paz, concursal (9001); familia (9120); laboral (2144); penal y juvenil (6730), jurados; administrativo y constitucional (3918, 9003, 9001, 9423).
- Módulo 3: documento electrónico, firma digital, MEED y portal de causas; IURIX ADF, FLEX y LED; comunicación SINEA; seguridad informática; crear y compartir documentos, hojas, formularios y presentaciones. Los videos se enlazan sin descargarse.
- Módulo 4: comprensión lectora, calidad y gestión pública; estadística descriptiva, tablas, gráficos e indicadores judiciales.

Prioridad inmediata: comprensión lectora y nociones institucionales. Estos temas permiten adelantar habilidades; las leyes, composición, sistemas y procedimientos se deben contrastar con el material 2026. No memorizar nombres de autoridades, capturas antiguas ni plazos de leyes históricas como si fueran actuales.

## Cambios y fuentes que no deben mezclarse

La convocatoria 2023 tenía dos exámenes de 80 y 64 preguntas con ponderación y penalización. Su protocolo segundo examen está guardado sólo como antecedente: no trasladar sus notas mínimas, penalización, plataforma ni retorno entre páginas a 2026. Las páginas viejas `/concurso-2023/` y `/concursos/concurso-2023/programa-y-material-de-estudio/` dieron HTTP 404 en descarga directa aunque el buscador conservaba contenido indexado. La página histórica accesible actual es [Concurso administrativo 2023](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2023/).

El antiguo portal [RRHH: exámenes](https://www2.jus.mendoza.gov.ar/rhumanos/documentacion/examen.php?left=60px) sigue HTTP200 y describe dactilografía, ortografía, teoría, informática y psicofísico. Se descargó su DOC de requisitos en `biblioteca/historico/aspirantes_ingreso_web.doc`; el portal de requisitos refiere una acordada de 2005. Eso no es material vigente ni demuestra que todas sus etapas se repitan. El portal [llamado 2016 y evaluaciones 2017](https://sic.jus.mendoza.gov.ar/web/direccion-de-recursos-humanos/requisitos1) está indexado pero su hostname no resolvió desde esta máquina. No se recuperó de allí un manual completo. El concurso MPF 2025 corresponde a otra convocatoria; no integra automáticamente este temario.

## Exámenes auténticos, modelos y búsquedas

No se localizó un banco público oficial completo de preguntas y respuestas del concurso SCJ administrativo 2023 ni de 2026. La revisión del examen individual 2023 estaba limitada a usuarios Moodle y un período específico, según las instrucciones históricas. Los simulacros preparados en esta carpeta por Codex deben presentarse como práctica original, nunca como examen filtrado o réplica oficial.

Sí se localizó un antecedente auténtico: [sentencia Valverde, 25/06/2025, CUIJ 13-07361172-9](https://www2.jus.mendoza.gov.ar/listas/proveidos/vertexto.php?ide=11361105857), HTTP200, texto guardado en `biblioteca/textos/fallo-valverde-2025.txt`. Debate preguntas del examen de 14/06/2023 y referencias concretas a material; no reproduce íntegros los enunciados y las cuatro alternativas. Permite observar temas: organización de Paz; injusticia simbólica; deberes estatales sobre derechos humanos; acción de desalojo; cámaras legislativas; responsabilidad política de ministros de Corte. La revisión aceptó un error material de la pregunta 13. Las opiniones del impugnante no son respuestas correctas; estudiar las explicaciones del informe y el texto oficial.

Se encontró [modelo ortográfico atribuido a Mendoza 2015 en un blog](https://ortografiarafaela.blogspot.com/2018/03/ejercicio-5.html): atribución secundaria no autenticada, y etapa distinta de 2026. Se revisaron resultados de búsquedas en portales oficiales antiguos, UNCuyo, sitios gremiales, medios y repositorios de documentos. No se halló allí otro examen administrativo completo verificable. Resultados de MPF Nación, Perú, magistratura, gobierno provincial o exámenes sanitarios fueron descartados por concurso diferente. Ninguna búsqueda puede garantizar cobertura absoluta de internet o archivos privados.

## Inventario descargable y enlaces

'''
text+=f'{len(rows)} recursos únicos catalogados; {sum("archivo" in r for r in rows)} PDFs descargados; {sum(r.get("paginas",0) for r in rows)} páginas. '+f'{sum("youtu" in r["url"] for r in rows)} enlaces de video. HTTP200 de YouTube no confirma reproducción.\n\n'
text+='| Recurso | Verificación | Copia local |\n|---|---|---|\n'
for r in rows:
 name=r['titulo'].replace('|','/')
 local='[PDF]('+r['archivo']+')' if 'archivo'in r else 'Enlace; sin copia'
 status=str(r.get('http','error conexión'))
 text+=f'| [{name}]({r["url"]}) | HTTP {status} | {local} |\n'
(root.parent/'BIBLIOTECA-Y-TEMARIO.md').write_text(text,encoding='utf8')
print(len(rows),sum('archivo'in r for r in rows),sum(r.get('paginas',0) for r in rows))
