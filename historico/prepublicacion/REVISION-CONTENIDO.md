# Revisión independiente del material preparatorio

Revisión de Codex, 5 de octubre de 2026. Alcance: muestra deliberada de 30 preguntas, lectura directa de las páginas PDF que citan y comparación de claves con los textos; integridad de los 43 PDF del catálogo histórico. Esta revisión no certifica el temario oficial de 2026 ni la dificultad real del examen.

## Integridad de la biblioteca

Se verificaron 43 archivos en `biblioteca/pdf/`: todos comienzan con `%PDF`, se abren con PyMuPDF, su SHA-256 coincide con `biblioteca/catalogo.json` y su cantidad de páginas coincide. Cero divergencias. La acordada 2026 se gestiona aparte y no integra esa cuenta histórica.

## Muestra de preguntas

Se examinaron P001, P006, P011, P016, P021, P026, P031, P036, P041, P046, P051, P056, P061, P066, P071, P076, P081, P086, P091, P096, P101, P105, P109, P113, P117, P121, P141, P152, P163 y P174. Son 20 específicas, 6 institucionales y 4 de lectura. La selección abarca instituciones, derechos, administración, proceso civil, paz, familia, trabajo, penal, cuatro textos y una operación aritmética.

No se encontraron claves conceptualmente incorrectas en esta muestra. Las alternativas seleccionadas responden a la pregunta; las otras alternativas no son defensibles bajo sus enunciados. P163: 180/200 × 100 = 90 %. Los conceptos jurídicos se contrastaron con el antecedente oficial 2023 y no se presentan como programa confirmado 2026. P141, P152, P163 y P174 corresponden a textos originales explícitamente etiquetados.

| Preguntas | Evidencia examinada | Resultado |
|---|---|---|
| P001, P006, P011, P016, P021, P026, P031, P036 | Módulo 1, pp. 2, 3, 10, 18, 37, 60, 121, 129 | Claves y referencias apoyadas |
| P041, P046, P051, P056, P061, P066, P071, P076 | Módulo 2, pp. 3, 7, 9, 10, 18, 20, 4, 17 | Claves apoyadas; P076 cita sección general de procesos universales |
| P081, P086, P091 | Módulo 2, pp. 91, 137, 160 | Claves apoyadas; formulaciones generales sin copiar detalles históricos variables |
| P096 | Módulo 2, pp. 178–179 | Clave correcta; mejor anclar en p. 179, donde aparece art. 18 |
| P101 | Módulo 1, pp. 1–2 | Clave correcta; p. 2 contiene definición expresa de población como elemento humano |
| P105, P117, P121 | Módulo 1, pp. 3, 115, 131 | Claves y referencias apoyadas |
| P109 | Módulo 1, pp. 101–102 | Clave correcta; p. 102 contiene aplicación por jueces locales |
| P113 | Módulo 1, pp. 108–111 | Clave correcta; p. 108 sólo introduce organización, pp. 110–111 fundamentan división y servicios comunes |
| P141, P152, P163, P174 | Cuatro textos originales anexos a las preguntas | Claves correctas; dos mejoras de redacción comunicadas abajo |

## Mejoras concretas comunicadas al autor

1. P109: pasar referencia de Módulo 1 p. 101 a p. 102. P113: usar pp. 110–111 en vez de únicamente p. 108. P096 y su pareja: p. 179 en vez de 178. P101: p. 2 en vez de 1. Estas observaciones afinan trazabilidad, no cambian las claves.
2. Texto L1: las consultas de requisitos son 60 de 120, exactamente 50 %. La frase que las llama mayoría puede inducir a confusión; conviene “categoría más frecuente” o “mayor proporción”. Se comunicó para corregir el texto de las diez preguntas de ese grupo y su fuente común.
3. P174: “¿Qué garantizaba la respuesta sobre el resultado?” presupone una garantía cuando la clave justamente niega un resultado garantizado. Conviene “¿Qué aclaraba la respuesta respecto del resultado?”. La respuesta existente es inequívoca entre las alternativas, pero se puede mejorar la consigna.

La muestra y las páginas extraídas están conservadas en `biblioteca/revision-muestra.json` y `biblioteca/revision-paginas.txt` como evidencia de la revisión inicial. Se debe releer la versión final del banco después de las correcciones; las capturas de muestra no son el banco vigente.

## Límites pedagógicos y actualización

Los distractores de muchas preguntas son muy evidentes: resultan útiles para aprender conceptos, pero no permiten estimar el nivel del examen real. Las 100 específicas se construyen como 50 pares de definición y caso, y por eso no equivalen a 100 conceptos independientes. La aplicación debe evitar presentar su puntuación como pronóstico de ingreso o aprobación oficial.

El material de lectura original entrena atención, inferencia y números; no reemplaza los futuros videos institucionales. Las referencias y etiquetas históricas son claras. Deben recalibrarse leyes y procedimientos cuando aparezca el programa 2026 el 12 de octubre, incluyendo temas ausentes en el banco inicial. No se ha reconstruido una evaluación oficial completa ni se afirma haber agotado fuentes privadas.

## Revisión del manual y del plan

Se leyeron `MANUAL-DE-PREPARACION.md` y `PLAN-DE-ESTUDIO.md` una vez publicados. El manual cubre las cuatro áreas históricas: organización/derechos y administración, nociones jurídicas por fuero, informática, y comprensión/calidad/estadística. La cobertura es introductoria y remite correctamente a fuentes completas y anexos; no promete desarrollar íntegramente las 1.727 páginas de biblioteca. Las referencias generales a los cuatro PDF y sus cantidades de páginas coinciden con los archivos. Se contrastaron además las fórmulas de tasa de resolución y tasa de sentencia con M4 pp. 26–27; son correctas. El ejemplo de media/mediana/moda 2, 3, 3, 4, 18 produce 6, 3, 3 y rango 16 correctamente.

Las distinciones normativas revisadas —Constitución/reforma, poderes constituidos, ley de fondo/competencia federal, órgano/función, juicio político/Jury, acto/reglamento/hecho, cautelar/sentencia, imputación/condena, libertad física/datos personales— no presentan un error sustantivo identificado. El manual evita fijar como actuales edades juveniles, composición variable, plazos y cuantías del antecedente. La informatización y calidad/estadística quedan explícitamente como complementos cuya inclusión 2026 falta confirmar.

El plan distingue fechas de estudio de fechas oficiales, dedica el 12 de octubre a actualizar, no extrapola ponderaciones 2023 ni promete ingreso por aprobar ejercicios. Da pautas de tiempo, recuperación y corrección concretas. Los simulacros siguen el banco y aclara que no representan un reparto curricular oficial.

Se comunicaron dos ajustes al autor: normalizar espacios entre palabras y números (por ejemplo, “para2026”, “del5al11” y “redactá20preguntas”), y sincronizar cantidades/textos/simulacros con la ampliación de 180 a 240 preguntas. En la primera versión del manual se describían 100 específicas y cuatro textos; la ampliación anunciada llevará 140 específicas y seis textos. Esta actualización requiere verificar el banco final, no asumir que el anuncio ya la completó.

Alcance final: revisión humana por Codex de conceptos y ejemplos seleccionados, lectura completa del plan y cobertura general del manual; no auditoría de cada línea jurídica frente a toda legislación vigente ni certificación de un programa todavía no publicado. Las verificaciones documentadas son suficientes para presentarlo como preparación anticipada con sus límites explícitos, y no como un curso oficial completo 2026.

## Cierre sobre la versión final de 240 preguntas

Se verificó el banco final: 240 ID únicos; 140 preguntas específicas, 40 institucionales y 60 lectoras en seis grupos de diez. Manual y plan ya describen esas cantidades e incluyen los bloques P181–P220, P221–P230 y P231–P240. El espaciado fue corregido en los documentos.

Las seis observaciones iniciales están resueltas: P096 apunta a M2 p. 179; P101 a M1 p. 2; P109 a M1 p. 102; P113 a M1 p. 110; el texto L1 dice “categoría más frecuente”; P174 pregunta qué aclaraba la respuesta respecto del resultado. Las claves no cambiaron porque eran correctas.

Se revisaron doce preguntas adicionales: P181, P185, P189, P193, P197, P201, P205, P209, P215, P219, P225 y P235. Las diez jurídicas se contrastaron con sus páginas de los módulos 1 y 2 y contexto pertinente; las dos lectoras con sus textos L5 y L6 completos. No se identificó clave incorrecta ni alternativa igualmente correcta en esta selección. P219 está sustentada expresamente en M2 p. 181: el apartado de inocencia diferencia sentencia no firme de sentencia con autoridad de cosa juzgada. P215 limita su pregunta a interpretación normativa del antecedente; no afirma que cualquier versión fáctica del trabajador sea prueba concluyente.

Los textos L5 y L6 incorporan límites de muestras, causalidad, observación/hipótesis/recomendación, recepción/decisión, acceso a información personal y trazabilidad. P225 interpreta correctamente el conector de contraste: las entrevistas tienen utilidad para detectar obstáculos aunque no permitan generalizar a toda la población. P235 identifica correctamente que conservar antecedentes permite saber qué ocurrió y cuándo, sin acreditar ausencia de errores.

El alcance acumulado es una muestra de 42 preguntas diferentes más relectura de seis ítems/textos corregidos. No equivale a validar exhaustivamente las 240 preguntas. La etiqueta de dificultad “intermedia-avanzada” es una clasificación didáctica interna, no una calibración empírica frente al examen real. Las nuevas preguntas suman contrastes conceptuales útiles, pero conservan distractores de facilidad desigual.

No quedan correcciones concretas pendientes de las observaciones comunicadas en esta revisión. Continúa pendiente la actualización contra material oficial 2026 cuando se publique.
