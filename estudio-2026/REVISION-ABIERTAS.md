# Revisión del taller de respuestas abiertas

12/10/2026. Se crearon y revisaron **90 preguntas abiertas originales** en `taller-datos/abiertas.json`. Distribución: M1 **18**, M2 **32**, M3 **14**, M4 **14**, M5 **12**. M2 incluye **16 preguntas juveniles**, O2-017–O2-032, basadas en el Código nuevo y las remisiones pertinentes.

El banco permite explicar, aplicar, comparar y corregir errores. Sus casos son ficticios y sus respuestas modelo son síntesis propias del material oficial. No son preguntas del examen ni anticipan videos institucionales. La respuesta modelo no es la única redacción válida: deben compararse contenido, condiciones y excepciones.

## 1. Rúbricas y uso

Cada objeto conserva el esquema pedido: `id`, `module`, `topic`, `title`, `prompt`, `model`, `checkpoints` y `sources`. Hay **368 criterios**, entre tres y cinco por pregunta, y **199 referencias locales de página**. Se verificó cada modelo y criterio frente a las páginas indicadas; no se añadieron requisitos por mera intuición jurídica o una mención temática genérica.

`critical: true` señala una confusión central que conviene corregir antes de continuar: atribuir una decisión al órgano equivocado, omitir una condición, invertir una regla o contar desde un evento incorrecto. **No calcula nota, no declara aprobación y no compara palabras clave.** La persona responde primero, conserva ese intento y después contrasta con la rúbrica para marcar cada criterio como omitido, parcial o correcto. La revisión del contenido debe considerar expresiones equivalentes y explicación razonada, no coincidencia literal con el modelo.

Las fuentes son PDF oficiales o normas enlazadas por el programa y guardadas en la biblioteca. `page` indica **hoja del archivo PDF**, no numeración histórica de otro documento. La UI puede abrir `file#page=page`. No se necesitaron fuentes HTML para esta selección.

## 2. Cobertura de los 27 apartados

| Apartado oficial | IDs | Cantidad y foco |
|---|---|---|
| 1.1 | O1-001–003 | 3: elementos aplicados, constituyente/constituidos, autonomía. |
| 1.2 | O1-004–006 | 3: órgano y función, límites del Ejecutivo, fondo/proceso/jurisdicción. Comprende los tres poderes del apartado y sus subsecciones. |
| 1.3 | O1-007–009 | 3: misión/visión, designación de jueces inferiores, Ministerios Públicos. |
| 1.4 | O1-010–012 | 3: Ley 9423, colegio y pleno, sentencia en pleno/plenaria y administración. |
| 1.5 | O1-013–015 | 3: competencia, acto/hecho/reglamento, motivación y ejecución. |
| 1.6 | O1-016–018 | 3: obediencia con requisitos, regalo/reserva, residencia y lectura normativa. |
| 2.1 | O2-001–007 | 7: conocimiento/monitorio, cargo/custodia, audiencias, cautelares, JUS, recaudador y concurso/quiebra. |
| 2.2 | O2-008–010 | 3: organización familiar, interés superior/participación, fondo/proceso y asistencia. |
| 2.3 | O2-011–013 | 3: irrenunciabilidad, gratuidad/costas y secuencia laboral. |
| 2.4 | O2-014–032 | 19: teoría del delito, órganos penales, jurados y 16 casos juveniles. |
| 3.1 | O3-001–003 | 3: titular/garante, jerarquía de instrumentos y subsidiariedad. |
| 3.2 | O3-004–006 | 3: dignidad/efectividad, progresividad y acciones positivas. |
| 3.3 | O3-007–008 | 2: clasificación sin jerarquía y características de los derechos. |
| 3.4 | O3-009–010 | 2: agentes, atribución estatal y debida diligencia ante actos privados. |
| 3.5 | O3-011–012 | 2: vulnerabilidad dinámica y efectos de medidas aparentemente neutrales. |
| 3.6 | O3-013–014 | 2: enfoque de derechos y barreras con respuestas. |
| 4.1 | O4-001–003 | 3: perspectiva/transversalidad/interseccionalidad, jerarquías y estereotipos. |
| 4.2 | O4-004–005 | 2: diversidad y rectificación registral de persona adulta. |
| 4.3 | O4-006–008 | 3: tipos/modalidades, ciclo de violencia y mitos. |
| 4.4 | O4-009–011 | 3: revictimización, retractación y perspectiva compatible con garantías. |
| 4.5 | O4-012–014 | 3: recepción, resguardo y diferencias entre compulsas. |
| 5.1 | O5-001–002 | 2: servicio centrado en ciudadanía y principios aplicados. |
| 5.2 | O5-003–004 | 2: recorrido, emociones, momentos críticos y comprensión real. |
| 5.3 | O5-005–006 | 2: reescritura precisa, escucha y retroalimentación. |
| 5.4 | O5-007–008 | 2: conflicto verbal y flujo de quejas. |
| 5.5 | O5-009–010 | 2: accesibilidad/ajustes e idioma/edad/canales. |
| 5.6 | O5-011–012 | 2: competencia, idoneidad, ética y aprendizaje. |

## 3. Juvenil: reglas, condiciones y páginas

Se aprovechó la lectura íntegra y visual de las 29 hojas del Código registrada en REVISION-ANEXOS.md; para redactar cómputos se volvió a las imágenes originales. El OCR auxiliar no se trató como autoridad. Fuentes exactas están en cada pregunta.

| IDs | Núcleo verificado | Hojas del Código |
|---|---|---|
| O2-017–018 | Edad al hecho, duda, aplicación procesal, datos indirectos y reserva con excepciones | 1–3; M2 102 para tramo de edad. |
| O2-019–020 | Tribunal/Juez/ejecución, excepción unipersonal, DRPJ, supervisor y audiencia ante incumplimiento | 4, 6–7; Ley 9735 1 y 3. |
| O2-021–022 | Tres horas, 12 + 12, aviso/informe, UPANA, investigación y adultos | 8–9, con especialidad en 1. |
| O2-023 | Incapacidad sobreviniente, inimputabilidad y atención durante ejecución | 10 y 25. |
| O2-024–025 | Tres relojes de preventiva; custodia, fundamentos, prórroga y cese/traslado | 12–15 y 24. |
| O2-026–028 | Juicio conjunto, separación, registro previo, abreviado y flagrancia | 16–19. |
| O2-029–030 | Restauración, efectos civiles, reserva y revisión amplia | 8, 19–22. |
| O2-031–032 | Educación, fracciones y decisión de progresión; no punibles, protección y archivo | 26–28; Ley 9735 4. |

Precauciones incorporadas:

- **Art. 41:** cinco días desde imputación para pedir preventiva; el día judicial pertenece al pedido de ampliación; duración desde detención efectiva, con máximo total de dieciocho meses. Decisión oral e inmediata al terminar la audiencia. [Código, PDF 12–13](biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=12).
- **Art. 47:** se conserva tenor literal de convocatoria a audiencia dentro de dos días hábiles y fundamentos diferidos dentro de tres hábiles. No se enseña como simple facultad opcional ni se sustituye ese plazo por las 48 horas del art. 48. [Código, PDF 14](biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=14).
- **Art. 33:** un padecimiento por sí no autoriza suspender automáticamente: debe excluir entender/querer, con dictamen forense previo. Se diferencia del sobreseimiento del art. 34 y del control sanitario de ejecución del art. 86. [Código, PDF 10](biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=10) y [PDF 25](biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=25).
- Cumplir 18 hace cesar la custodia en el supuesto del art. 50; no extingue automáticamente condena. Los umbrales de un tercio, mitad y dos tercios tampoco crean progresión automática. [Código, PDF 14](biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=14), [PDF 24](biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=24) y [PDF 26](biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=26).

## 4. Otras precisiones de revisión

- Ley 9423 respalda las preguntas de Corte con sus hojas 1–6; no se trasladan las reglas de recursos de sentencia en pleno a la plenaria.
- El DNU de O1-005 practica condiciones y materias excluidas de M1 16–17; no reproduce la formulación problemática de M1 38 ni convierte la ley especial de regulación del trámite en una supuesta ley individual para cada DNU.
- La residencia de O1-018 distingue requisito y momento de rendir, y documenta fecha de la compilación antigua del DL 560. No predice regla de nombramiento a partir de una simplificación.
- La pregunta de JUS separa capital de accesorios y umbrales generales de pequeña causa; la de gratuidad laboral separa acceso sin pago previo de costas y exención de tasa.
- O4-014 usa el [protocolo original, PDF 17–18](biblioteca/2026/referencias/Protocolo-Violencia-Laboral-30979.pdf#page=17) para evitar consentimiento universal inventado en delitos de oficio. O4-011 agrega M2 90 para respaldar presunción de inocencia.
- No se usaron como certezas generales los porcentajes de comunicación o liderazgo de M5, ni una etiqueta de discapacidad o edad como prueba automática de incapacidad.

## 5. Validaciones y límites

Verificados: 90 IDs únicos; distribución por módulo; 27 temas presentes; tres a cinco criterios con IDs locales únicos y booleanos; modelos, consignas y títulos completos; archivo y página de las 199 fuentes; 16 juveniles con referencia al Código; ausencia de duplicados exactos de consignas entre sí y con los bancos de opciones del paquete.

La cobertura de los 27 apartados **no equivale a preguntar cada párrafo o artículo**. Los modelos breves seleccionan los puntos pedidos por la consigna; para ampliar se abre la fuente. Las adaptaciones de atención admiten varias soluciones razonables. El taller no otorga calificación oficial y no puede garantizar una nota de examen. Se guardaron únicamente el JSON de abiertas y este registro, sin cambios a la aplicación ni bancos anteriores.
