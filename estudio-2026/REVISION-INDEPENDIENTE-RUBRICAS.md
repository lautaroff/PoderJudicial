# Segunda revisión de rúbricas y ejercicios del taller

Fecha: 12 de octubre de 2026. Archivos revisados, sin modificarlos: `taller-datos/abiertas.json`, `casos.json`, `secuencias.json` y `errores.json`.

Se revisaron **90 abiertas, 20 pares/40 casos, 12 secuencias y 20 detectives**: 142 registros y 162 situaciones o ejercicios individuales. La pasada vuelve a las fuentes originales y distingue corrección conceptual, condiciones del supuesto y correspondencia entre pregunta, modelo y puntos de revisión. El revisor participó previamente en la autoría de casos, secuencias y detectives: se trata de una segunda pasada de contraste, no de independencia de autoría. Las abiertas se revisaron aquí por primera vez.

**Resultado:** no se detectaron fuentes inexistentes, páginas fuera de rango, inversión de los relojes juveniles principales ni una segunda ordenación incompatible con las dependencias de las 12 secuencias dentro de sus alcances. Se identificaron **seis ajustes concretos** para eliminar ambigüedad o completar condiciones y dos mejoras menores de precisión. La integración aplicó correcciones mientras se redactaba este informe; el estado verificado al cierre se registra al final. El revisor conservó los datos intactos.

## Correcciones concretas

| Ítem y campo | Problema comprobado | Corrección propuesta | Fuente |
|---|---|---|---|
| **O2-003**, `checkpoints.c2` | «Ubica admisión/producción de prueba en inicial» puede exigir que se produzca allí la prueba que el modelo correctamente distingue de la recepción oral final. El punto crítico es menos preciso que la solución. | Sustituir por **«Ubica admisión y ordenación de la producción de prueba en la inicial; recepción de prueba oral y alegatos en la final»**. No exigir producción completa en la inicial. | [M2 PDF 8](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-2-El-Poder-Judicial-de-Mendoza-Material-de-Estudio.pdf#page=8), [PDF 9](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-2-El-Poder-Judicial-de-Mendoza-Material-de-Estudio.pdf#page=9), [PDF 10](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-2-El-Poder-Judicial-de-Mendoza-Material-de-Estudio.pdf#page=10). |
| **C3-003**, `a.text`, `b.text`, `changed` | A tiene conexión **y** habilidad; B carece de conexión **y** habilidad. La conclusión sobre acceso es correcta, pero cambian dos variables independientes y no una sola. | Conservar habilidad digital en ambos: A dispone de conexión; B sabe completar el trámite pero **carece de conexión**. Cambiar `changed` a disponibilidad de conexión. Mantener igualdad formal/sustantiva y apoyo o alternativa disponible. | [M3 PDF 17](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-3-Derechos-Humanos-Material-de-Estudio.pdf#page=17), [PDF 18](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-3-Derechos-Humanos-Material-de-Estudio.pdf#page=18). |
| **O1-014**, `prompt` | «Decisión individual de traslado» no identifica qué se traslada. Puede referirse a reasignación administrativa de personal o al traslado procesal de una presentación. La respuesta prevista presupone lo primero. | Precisar **«una decisión administrativa individual que traslada a un agente a otra dependencia»**. Conservar los otros ejemplos de movimiento material de mobiliario y norma general de organización. | [M1 PDF 32](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=32), [PDF 34](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=34). |
| **O2-024**, `model`, `checkpoints.c2` | La ampliación del término fiscal se resume solo «por complejidad». El art. 41 admite que la justifiquen **cantidad de hechos atribuidos o evidente complejidad de la investigación**. Falta la primera alternativa de una condición pedida expresamente. | Usar **«por cantidad de hechos atribuidos o evidente complejidad de la investigación que lo justifiquen, solicitada antes de vencer; una única ampliación de hasta cinco días»**. Mantener que el día judicial resuelve esta ampliación y no la preventiva. | [Código juvenil PDF 12, art. 41](../biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=12). |
| **C5-001A**, `text`, `prompt`, `model` | Se pide redactar la respuesta con fecha/hora/lugar, pero el caso no entrega valores. El modelo describe qué hacer en vez de ofrecer una respuesta redactada. No debe penalizarse al estudiante por no inventar esos datos. | Añadir datos ficticios expresamente proporcionados por el caso, o pedir **«redactá con marcadores [fecha], [hora], [lugar/modalidad] para los datos que el sistema confirme»**. Incluir un modelo redactado con esos marcadores. Si se agregan datos, mantenerlos como parte común de A/B para no crear otra condición variable. | [M5 PDF 16](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-5-Atencion-para-un-Servicio-de-Justicia-Material-de-Estudio.pdf#page=16), precisión informativa en [PDF 9](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-5-Atencion-para-un-Servicio-de-Justicia-Material-de-Estudio.pdf#page=9). |
| **O2-006**, `prompt` o `checkpoints.c3` | El punto crítico exige negar percepción extrajudicial de los rubros, pero la pregunta pide autorización para transar/suspender y límites de representación, sin preguntar esa percepción. La regla incluida en el modelo es correcta; su exigencia crítica no está anunciada claramente. | Agregar al enunciado **«¿Puede además percibir fuera del juicio los rubros ejecutados?»**, o conservar ese dato como ampliación con `critical:false`. La primera opción permite evaluar toda la respuesta modelo sin criterio oculto. | [M2 PDF 44](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-2-El-Poder-Judicial-de-Mendoza-Material-de-Estudio.pdf#page=44). |

Los ajustes anteriores no requieren cambiar cantidad de ejercicios, IDs ni las reglas principales de las soluciones.

## Mejoras menores de precisión

1. **O1-009:** el punto no crítico `c3` pide distinguir Procurador General y Defensor/a General, pero el modelo solo dice que las autoridades son distintas. Agregar sus nombres de cargo al modelo y pedir autoridades en el enunciado, o dejar este punto fuera de lo exigido. [M1 PDF 27](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=27), [PDF 28](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=28).
2. **O2-024, O2-028 y O2-030:** añadir como fuente el **art. 4, PDF 2** y precisar la regla de cómputo en días hábiles conforme al CPP remitido, distinguiéndola de horas y de la formulación expresa «días corridos» del art. 86. Las cifras y los actos iniciales actuales son correctos; esta mejora evita que el alumno complete por su cuenta la clase de días. [Código juvenil PDF 2](../biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=2), [PDF 25, art. 86](../biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=25). No se propone alterar los plazos ni convertir horas en días.

## Revisión de secuencias y orden único

Se comprobó que `correct` contiene una sola vez cada ID de paso y que las dependencias cubren toda la cadena. Ese control acredita coherencia estructural; el contraste siguiente examina si el orden tiene sentido en el supuesto expresado.

| Secuencia | Resultado del contraste |
|---|---|
| S1-001 | Concurso → terna → elección del Ejecutivo → acuerdo → nombramiento. La terna vinculante y el acuerdo impiden adelantar elección o nombramiento. Es juez federal inferior, no Corte nacional. |
| S1-002 | Ingreso → sorteo → dirección del primero → sustanciación hasta estado de resolver → votación. El alcance excluye causas del pleno y subrogaciones; no ordena todas las providencias de la Corte. |
| S2-001 | Contestación anterior a inicial; admisión y preparación antes de prueba oral final; alegatos después de prueba. Está delimitado al conocimiento sin acuerdo. El art. 172 II ya corrige el resumen de p. 34; treinta días de sentencia desde llamamiento firme, no desde demanda. |
| S2-002 | Sentencia inicial → notificación/oposición → traslado → prueba → sentencia de oposición. Correcto para monitorio común con oposición y prueba admitida. Art. 236 III: diez días **de quedar en estado la causa**. No traslada reglas del desalojo. |
| S2-003 | Contestación laboral → traslado a actora → inicial → prueba escrita → vista/alegatos → sentencia. El alcance excluye acuerdo y pericia médica anticipada por accidente/enfermedad. No importa plazos civiles ni el orden de LeD penal. |
| S2-004 | Petición → consulta/identidad → constancia negativa → comunicación → incidente/prueba → dictamen → auto. La prueba del incidente debe acompañar petición y el dictamen precede al auto. Está delimitado a que la persona elige esa vía después de negativa; no implica suspensión del proceso principal. |
| S2-005 | Imputación → requerimiento → convocatoria/citación → audiencia → decisión inmediata al cierre. El alcance excluye ampliación de plazo. Cinco días desde imputación; duración desde detención efectiva. La víctima citada puede faltar sin invalidar. |
| S3-001 | Ruta metodológica inicial: titularidad → barreras → formulación → ejecución → monitoreo → evaluación. El orden es defendible en el primer ciclo definido y no se formula como procedimiento judicial ni prohibición de monitoreo simultáneo o rediseño. |
| S4-001 | Primer episodio completo y comienzo del segundo: tensión → explosión → luna de miel → nueva tensión → segunda explosión. Los episodios están identificados, evitando rotaciones indistintas de un ciclo. No se exige el modelo para reconocer violencia. |
| S5-001 | Los cinco pasos del flujo de quejas están expresamente enumerados en M5 pp. 17–18. No se confunde con recurso judicial ni denuncia penal. |
| S5-002 | Los cuatro estados de aprendizaje son los de la tabla M5 p. 27; se distingue reconocer carencia de ejecutar deliberadamente y automatizar. No impone tiempos. |
| S5-003 | Las seis etapas siguen el mapa ilustrativo M5 pp. 6–7. El alcance reconoce que no es cronograma legal universal ni emoción obligatoria de cada usuario. |

No se detectó una segunda ordenación válida de los pasos **tal como están definidos** en estas 12 rutas. Su validez no debe generalizarse a trayectorias que el `scope` excluye. Las fuentes HTML de S2-001 y S2-002 carecen correctamente de página PDF: [CPCCyT actualizado, arts. 172 II y 236 III](../biblioteca/2026/referencias/Ley-9001-CPCCT-lectura.html).

## Condiciones juveniles contrastadas

Se leyó la transcripción auxiliar de los tramos citados y se volvió a los originales escaneados para condiciones y cifras sensibles. Se contrastaron visualmente PDF **2, 4, 9, 12, 13, 14, 19, 22 y 26**. No se afirma que esta segunda pasada haya vuelto a revisar visualmente todas las 29 hojas del código.

| Ítems | Regla comprobada y decisión |
|---|---|
| O2-017 | Edad al hecho y conservación de actos regularmente cumplidos desde vigencia. La duda se liga a no poder acreditar de inmediato edad mínima/mayoría; no convierte todo cumpleaños posterior en cambio de régimen. |
| O2-018, C2-006 | Art. 6: también identificación indirecta; pedido de sujeto procesal, resolución fundada y dictamen favorable de Asesoría, con estricta necesidad y dignidad. Excepción limitada, no libre difusión. Reserva frente a terceros no excluye defensa/partes constituidas con las reglas específicas. |
| O2-019, C2-005 | Art. 12: tres jueces como regla; excepción material justificada **y** solicitud de partes. Se distingue de art. 63 de flagrancia. «Podrá» no impone conceder. |
| O2-020 | Supervisor informa y órgano judicial decide mediante audiencia contradictoria; informes no superiores a tres meses. No agrava unilateralmente una medida administrativa. |
| O2-021 | Art. 25: disposición inmediata en máximo improrrogable de tres horas. Art. 27: imputación dentro de doce horas desde puesta a disposición, con otras doce fundadas. Art. 28: aviso a DRPJ en máximo tres horas luego de imputar e informe dentro de cuarenta y ocho. El texto del art. 28 no especifica un nuevo acto inicial separado para las cuarenta y ocho: no inventarlo. UPANA no sustituye centro especializado cuando hay preventiva. |
| O2-022 | Art. 29: tres meses desde imputación, prórroga judicial por otro tanto; suma gravedad y muy difícil investigación para máximo total de doce. La investigación conjunta no elimina especialidad. |
| O2-023 | Suspensión por incapacidad sobreviniente y sobreseimiento por inimputabilidad son distintos. Art. 86: informes máximo cada treinta días **corridos**, cómputo íntegro del tratamiento/internación controlados. |
| O2-024, S2-005, E2-003 | Art. 41: requerimiento desde imputación; día judicial para resolver ampliación; duración inicial desde detención efectiva; decisión oral inmediata al concluir audiencia. No hay inversión de esos relojes. Completar las causas de ampliación conforme al hallazgo de arriba. |
| O2-025 | Art. 47 dice **convocará** dentro de dos días hábiles; resuelve oral e inmediatamente y **diferirá** fundamentos dentro de tres hábiles. El modelo actual conserva esa literalidad. Art. 48: cuarenta y ocho horas para prórroga, previa vista a Asesoría. Cese de custodia a los dieciocho no extingue condena automáticamente. |
| O2-026–O2-028 | Separación de jurado del adulto y del proceso correccional; uso controlado de grabación, sin sustitución automática de testigo. Consentimiento reforzado del abreviado y prohibición de decidirlo en inicial de flagrancia. Art. 63: tres días desde imputación y prórroga igual excepcional con fundamentos específicos. |
| O2-029 | Momento de mecanismos hasta apertura del debate y exclusiones de art. 65; reserva de conversaciones del mediador. Extinción civil exige acuerdo expreso, voluntario, informado y homologado con alcance inequívoco, no cualquier solución penal. |
| O2-030 | Revisión amplia solo contra condenatorias por adolescente/defensa; diez días desde notificación para interponer/fundar. Art. 74 fija diez días siguientes para audiencia solicitada/dispuesta y cinco desde sus eventos legales para resolver. No se inventa cinco días desde interposición ni plazo escrito previo que la página no define. |
| O2-031 | Tercio, mitad y dos tercios son umbrales con evaluación, no beneficios automáticos. Reconsideración máximo tres meses si se deniega. Escolarización no se suspende como disciplina. |
| O2-032 | Comprobación limitada no es juicio de culpabilidad. Defensa y protección desde primer acto; archivo y compulsa contravencional parental no son condena al niño. |

Los enlaces exactos están conservados en `sources` de los ejercicios; las páginas visuales más sensibles son [PDF 12](../biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=12), [PDF 14](../biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=14), [PDF 19](../biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=19), [PDF 22](../biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=22) y [PDF 26](../biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf#page=26).

## Fuentes y comprobaciones formales

- **142 IDs únicos**; recuentos 90/20/12/20 correctos.
- **356 referencias PDF** revisadas para existencia y rango, contando fuentes duplicadas de A/B; doce documentos PDF distintos. Dos referencias HTML por artículo, sin hojas inventadas.
- Pasos de secuencias únicos; mismos IDs en `steps` y `correct`; todas las dependencias de la cadena coherentes.
- Cada detector mantiene **un error conceptual relevante**; no se encontró un segundo error independiente que exigiera otra corrección. E2-003 mezcla deliberadamente dos actos iniciales, pero la cifra de tres meses desde detención está correctamente conservada como parte verdadera.
- Los modelos de compulsas O4-012/O4-014 se contrastaron con el [protocolo original PDF 16](../biblioteca/2026/referencias/Protocolo-Violencia-Laboral-30979.pdf#page=16), [PDF 17](../biblioteca/2026/referencias/Protocolo-Violencia-Laboral-30979.pdf#page=17) y [PDF 18](../biblioteca/2026/referencias/Protocolo-Violencia-Laboral-30979.pdf#page=18): no requieren consentimiento universal para delito perseguible de oficio y distinguen trámite administrativo, instancia privada y colegio profesional.
- O3-008 coincide con la formulación del [M3 PDF 9](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-3-Derechos-Humanos-Material-de-Estudio.pdf#page=9) sobre no obligar a renunciar y no transferir/comercializar. No se reportó como errata una respuesta que reproduce ese alcance del programa.

La comprobación formal no prueba por sí el contenido. Las correcciones se recomiendan por su lectura semántica y contraste con la fuente, no por un fallo del validador. **No se modificó ningún JSON ni archivo de aplicación en esta tarea.**

## Estado verificado al cierre

Tras comunicar los hallazgos al agente que integra, se volvieron a leer los campos afectados. Las modificaciones siguientes fueron realizadas por la integración, no por este revisor:

| Hallazgo | Estado observado |
|---|---|
| O2-003 | Corregido: el punto dice admisión y **orden** de producción en inicial, recepción oral en final. |
| C3-003 | Corregido: B mantiene la misma habilidad y cambia únicamente la conexión. |
| O1-014 | Corregido: decisión administrativa de traslado de un agente a otra oficina. |
| O2-024 | Corregido: incorpora cantidad de hechos y evidente complejidad en modelo y punto de revisión. |
| O2-006 | Corregido: el enunciado pide expresamente el límite de percepción extrajudicial. |
| C5-001A | El enunciado ya admite [fecha], [hora] y [lugar/modalidad], resolviendo la falta de valores. El modelo todavía describe acciones: completar con una respuesta redactada utilizando los mismos marcadores. |

Ejemplo propuesto para el último modelo: **«Su audiencia es el [fecha], a las [hora], en [lugar/modalidad], según los datos confirmados en el sistema. Para comprobar que fui claro, ¿podría decirme cuándo y dónde debe presentarse?»** Se aceptan otras formulaciones precisas y respetuosas; no se exige repetir estas palabras.

Las dos mejoras menores —autoridades en O1-009 y fuente/regla de días en las tres abiertas juveniles señaladas— no se observaron aplicadas en esa lectura final. No invalidan las reglas principales, pero mejoran la correspondencia de la autoevaluación con el material.


## Cierre de integración posterior

La integración corrigió los hallazgos documentados: en rúbricas, enunciados, condiciones y fuentes; en diagnósticos DA-40, DA-44, DB-03 y DB-50. C5-001A incluye una respuesta redactada con marcadores, O1-009 pide e identifica las autoridades y O2-024/028/030 explicitan cómputo con fuente en art. 4. Las citas adicionales de escenas/preguntas fueron incorporadas y las claves de videos ya no siguen un ciclo 0–1–2–3. Los MP4 terminados y el navegador se verifican en VERIFICACION.md; esta nota registra integración, sin ampliar retrospectivamente el alcance del revisor.
