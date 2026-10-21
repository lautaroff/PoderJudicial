# Auditoría de mapas y esquemas del programa 2026

Revisión: 21/10/2026. Pedido: detectar qué temas conviene representar visualmente y cuáles necesitan profundización, comparando con los recursos que ya existen. Revisión realizada por tres agentes GPT-6.1 Sol y consolidada en este informe. Es una auditoría con propuestas; los mapas sugeridos todavía no se incorporaron al atlas.

## El hallazgo que motivó la revisión

**Falta un mapa de la estructura del Poder Judicial que permita ubicarse antes de estudiar cada órgano.** La explicación existe en la guía y en el PDF, pero los mapas actuales de M1 son `estado`, `corte` y `administracion`. El primero explica el Estado; el segundo clasifica tres funciones de la Suprema Corte; el tercero reúne conceptos administrativos. Ninguno muestra el conjunto de la organización judicial.

La fuente para empezar ese mapa es [M1, PDF p. 26](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=26). Las autoridades y funciones de los ministerios públicos se desarrollan en [M1, PDF p. 27](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=27) y [p. 28](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=28). La explicación escrita está en [la guía, apartado 1.3](GUIA-M1-M3.md).

El dibujo debe distinguir los niveles jurisdiccionales, las funciones, las relaciones administrativas y el territorio. Dibujar todos esos vínculos con una misma flecha vertical enseñaría relaciones que el material no establece.

## Qué falta representar o profundizar

| Módulo | Nuevas vistas de mayor utilidad | Recursos que conviene ampliar o reutilizar |
|---|---|---|
| **1 · Estado** | Panorama judicial, jerarquía normativa, circuitos de designación y remoción. | `corte`: integración, atribuciones y ejemplos; `administracion`: jerarquía real, competencia y formas de actuación; tablas de órganos y empleo judicial ya existentes. |
| **2 · Poder Judicial** | Vías y bifurcaciones por fuero; Paz, apremio, concursal, organización de Familia, Laboral y régimen juvenil. | `fueros` como entrada general; `proceso` y `penal` como vistas iniciales enlazadas a detalles. Adaptar los gráficos concursales oficiales, que ya existen en el PDF. |
| **3 · Derechos Humanos** | Sistemas de protección, normas, responsabilidad estatal y barreras de acceso. | Separar visualmente los principios, las características, las categorías y las obligaciones que hoy quedan concentradas alrededor de `derechos`. |
| **4 · Género** | Construcción social y estereotipos, ciclo de violencia, ruta del protocolo y decisiones sobre actuaciones posteriores. | Conservar la distinción de diversidad y la matriz de tipos/modalidades; añadir ejemplos y acceso al protocolo original para sus condiciones. |
| **5 · Servicio** | Circuito de comunicación y atención, situaciones difíciles y aplicación de competencias. | Enlazar el viaje del usuario con conductas concretas; ampliar accesibilidad y desempeño mediante decisiones y casos, aprovechando los mapas actuales. |

Estas son familias de representaciones, no un compromiso de crear un dibujo separado por cada sustantivo. Las matrices detalladas de los informes permiten decidir qué merece mapa propio y qué funciona mejor como una vista desplegable, una tabla o un ejercicio.

## Qué se comparó

Los cinco PDF principales suman **217 páginas**: M1 39, M2 113, M3 23, M4 10 y M5 32. El índice oficial agrega otras tres páginas. Las remisiones normativas pertinentes se revisan en los informes de cada módulo. La [página oficial del material](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026-material-de-estudio/) identifica estos cinco módulos como bibliografía del examen de conocimientos específicos.

Se compararon el contenido de los PDF, las guías explicadas, los esquemas ya incluidos en ellas y el atlas `memoria-datos.json`. No se considera que un tema falte del paquete porque no tenga mapa: puede estar cubierto en una guía, una tabla, una tarjeta o un ejercicio. La auditoría distingue esa situación de una ausencia de contenido.

| Módulo | Mapas actuales | Nodos | Tarjetas | Contrastes | Casos |
|---|---:|---:|---:|---:|---:|
| 1 · Organización del Estado | 3 | 18 | 24 | 3 | 3 |
| 2 · Poder Judicial de Mendoza | 3 | 19 | 24 | 2 | 3 |
| 3 · Derechos Humanos | 1 | 11 | 24 | 2 | 3 |
| 4 · Violencia de Género | 2 | 18 | 24 | 2 | 3 |
| 5 · Atención para un Servicio de Justicia | 3 | 15 | 24 | 3 | 3 |
| **Total** | **12** | **81** | **120** | **12** | **15** |

El [inventario verificable](AUDITORIA-MAPAS-INVENTARIO.json) registra IDs, títulos, ramas, fuentes y hashes de los archivos comparados. Las auditorías detalladas identifican los apartados revisados y las propuestas por módulo:

- [Módulo 1: Estado y organización judicial](AUDITORIA-MAPAS-M1.md).
- [Módulo 2: fueros y procesos](AUDITORIA-MAPAS-M2.md).
- [Módulos 3, 4 y 5: derechos, género y servicio](AUDITORIA-MAPAS-M3-M5.md).

## Prioridades de producción

Las prioridades expresan utilidad para comprender y evitar confusiones; no predicen cuántas preguntas tomará el examen. Este orden de construcción tampoco impone estudiar los módulos en una secuencia rígida.

| Tanda | Qué producir | Resultado buscado |
|---|---|---|
| **Primera: resolver la falta señalada** | Panorama judicial con sus vistas, detalle de Corte conforme a Ley 9423 y ampliación de funciones. | Poder ubicar un órgano, explicar su tarea y distinguir la relación que tiene con otros. |
| **Base complementaria de M1** | Escala normativa; carriles de designación/remoción; profundización de jerarquía y competencia administrativa. | Distinguir tres preguntas distintas: qué norma prevalece, cómo se ocupa un cargo y qué puede hacer cada órgano. |
| **Despliegue de M2** | Una entrada por materias con detalles por vía, actores, instancias y decisiones. Adaptación de gráficos concursales; rutas de Paz, Familia, Laboral y Penal Juvenil. | Que el mapa general de fueros deje de ser la única ubicación visual de temas muy diferentes. |
| **M3** | Nuevo panorama de protección normativa e internacional; ampliar obligaciones, responsabilidad e igualdad situada. | Separar normas, derechos, principios, obligaciones y mecanismos de protección sin jerarquizar derechos. |
| **M4** | Construcción de desigualdades; dinámica de violencia y respuesta institucional; circuito del protocolo laboral. | Recuperar relaciones y condiciones. Conservar los ejes de tipos/modalidades y las tres dimensiones de diversidad. |
| **M5** | Servicio y mejora; comunicación comprensible; ampliación de accesibilidad enlazada con barreras de M3. | Practicar decisiones concretas de atención y justificar qué respuesta ayuda a ejercer derechos. |
| **Profundización posterior** | Tablas de actividad administrativa y deberes; red histórica de derechos; modelos del perfil profesional. | Añadir vistas solo cuando faciliten recuperar algo que las guías y tarjetas actuales no permiten dominar. |

En M1, el informe distingue **tres mapas nuevos prioritarios y dos ampliaciones**; la organización interna de la Corte y el territorio se integran como detalles conectados. M2 detalla **104 subtemas y 20 paquetes visuales**: tres ampliaciones y 17 paquetes nuevos o adaptados, con prioridades y profundizaciones posteriores. Para M3–M5, propone **ocho paquetes iniciales**: seis vistas nuevas y dos ampliaciones profundas, con enriquecimientos auxiliares de mapas existentes. Un paquete puede contener varias vistas; esos recuentos no se deben sumar como si todos fueran organigramas independientes.

## Hallazgos que requieren conservar las condiciones de la fuente

Además de detectar mapas faltantes, la revisión identifica puntos donde un esquema demasiado breve podría fijar una regla incorrecta:

- **Organización de la Corte:** la remisión de M1 a M2 no basta para conocer el detalle de Ley 9423. Usar la norma enlazada en los anexos y distinguir pleno, colegio, Sala Administrativa, sentencia en pleno y sentencia plenaria. El informe M1 asigna artículos y páginas a cada grupo.
- **Protocolo laboral:** la condición de consentimiento cambia según la vía. El original distingue compulsa administrativa, delito perseguible de oficio, delito dependiente de instancia privada y colegio profesional. Ver [PDF p. 17](../biblioteca/2026/referencias/Protocolo-Violencia-Laboral-30979.pdf#page=17) y [p. 18](../biblioteca/2026/referencias/Protocolo-Violencia-Laboral-30979.pdf#page=18). La etiqueta abreviada de M4 no debe convertirse en una condición universal.
- **Medidas preventivas del protocolo:** distinguir la recomendación provisional de la Dirección y la respuesta fundada de Recursos Humanos. No representarlas como sanciones automáticas. Ver [original, PDF p. 19](../biblioteca/2026/referencias/Protocolo-Violencia-Laboral-30979.pdf#page=19).
- **Derechos y barreras:** una clasificación de derechos no establece mayor importancia de unos; las tres familias de barreras de M3, las cuatro dimensiones de accesibilidad y las cinco barreras enumeradas en M5 contestan preguntas distintas. El informe M3–M5 propone paneles conectados, sin equivalencias artificiales.
- **Procesos y plazos de M2:** los gráficos del PDF y los resúmenes tienen condiciones y algunas inconsistencias que ya estaban advertidas en las guías. El informe M2 identifica cuáles se pueden adaptar y qué debe cotejarse con la norma antes de publicar una regla cerrada. En el Código Juvenil escaneado distingue las páginas verificadas visualmente de los detalles que requieren cotejo final. La auditoría propone la cobertura visual; esos detalles no se presentan como mapas finales ya validados.

## Cómo debería organizarse el mapa general del Poder Judicial

La mejor solución es una entrada común con varias vistas conectadas, en lugar de un único dibujo con todas las oficinas amontonadas.

| Vista | Pregunta que resuelve | Contenido y fuente | Relación que debe distinguir |
|---|---|---|---|
| Nación y provincia | ¿En qué orden de justicia estoy? | Justicia federal y provincial; coexistencia territorial. [M1 p. 22](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=22), [p. 23](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=23). | Coexistencia y competencia. El asiento de un tribunal federal en Mendoza no lo convierte en tribunal provincial. |
| Órganos jurisdiccionales de Mendoza | ¿Qué lugar ocupa este órgano? | Suprema Corte, Cámaras, primera instancia y demás órganos creados por ley. [M1 p. 26](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=26). Detalles de cada fuero: M2. | Nivel institucional; no una orden del superior sobre cómo resolver cada causa. Las vías recursivas necesitan etiquetas y condiciones propias. |
| Ministerios públicos y tareas | ¿Quién acusa, quién defiende y quién decide? | MPF y Procurador General; Ministerio Público de la Defensa y Pupilar y Defensor/a General. [M1 pp. 27–28](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-1-Organizacion-del-Estado-Material-de-Estudio.pdf#page=27). Juez/MPF/OGAP en [M2 pp. 93–94](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-2-El-Poder-Judicial-de-Mendoza-Material-de-Estudio.pdf#page=93). | Función y organización propia de cada institución. No colocar a fiscales o defensores debajo de los jueces como subordinados que reciben instrucciones de ellos. |
| Gobierno y administración de la Corte | ¿Quién organiza y con qué facultad? | Funciones de M1 1.4; pleno, colegio, Sala Administrativa y Presidencia conforme a [Ley 9423, pp. 1–6](../biblioteca/2026/referencias/Ley-9423.pdf#page=1). [Mapa de lectura normativa](GUIA-ANEXOS.md). | Integración, atribución y superintendencia, distintas de una secuencia de apelación. |
| Territorio | ¿Dónde actúa y qué circunscripción corresponde? | Cuatro circunscripciones: [M2 p. 11](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-2-El-Poder-Judicial-de-Mendoza-Material-de-Estudio.pdf#page=11), [p. 36](../biblioteca/2026/programa/Concurso-Ingreso-2026-SCJM-Modulo-2-El-Poder-Judicial-de-Mendoza-Material-de-Estudio.pdf#page=36) y [FAQ oficial 2026](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026/). | Distribución territorial, no jerarquía entre circunscripciones. |

La Ley 9423 requiere atención especial: M1 promete un desarrollo en M2 que la revisión del paquete no localizó. Por eso la guía ya completa la remisión con el PDF de la ley. Un mapa nuevo debe enlazar esa norma y evitar reconstruir la Corte con un organigrama antiguo de salas permanentes.

Para la vista territorial, el micrositio oficial consultado el 21/10/2026 permite completar los departamentos:

| Circunscripción | Departamentos |
|---|---|
| Primera | Capital, Godoy Cruz, Maipú, Las Heras, Guaymallén, Luján de Cuyo y Lavalle. |
| Segunda | San Rafael, General Alvear y Malargüe. |
| Tercera | San Martín, Junín, Santa Rosa, La Paz y Rivadavia. |
| Cuarta | Tunuyán, Tupungato y San Carlos. |

Fuente: [preguntas frecuentes de la convocatoria 2026](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026/). No hace falta memorizar direcciones, teléfonos o nombres actuales de autoridades para completar este esquema del programa.

## Elegir la representación según la pregunta

| Si querés recordar… | Conviene… | Hay que evitar… |
|---|---|---|
| De qué se compone algo | Árbol de clasificación con ramas anidadas. | Que la altura de una categoría sugiera mayor importancia jurídica. |
| Qué órgano tiene qué atribución | Organigrama o red institucional con relaciones identificadas. | Mezclar pertenencia, coordinación, designación y revisión recursiva. |
| Qué ocurre antes o después | Flujo con pasos y bifurcaciones. | Dar por obligatorias todas las etapas o convertir una excepción en regla general. |
| Qué plazo corresponde | Línea temporal con inicio, duración, destinatario y excepción. | Un número sin indicar desde cuándo corre o de qué clase de días se trata. |
| Cómo distinguir dos conceptos | Tabla o contraste con un mismo caso. | Dos definiciones aisladas que no muestran la diferencia que decide el caso. |
| Cómo se relacionan tipos y contextos | Matriz de ejes independientes. | Emparejar cada tipo de violencia con una única modalidad. |
| Qué derechos y deberes se conectan | Red conceptual con verbos en los enlaces. | Una pirámide de derechos más y menos importantes. |

## Consolidación para evitar mapas repetidos

Las propuestas de los agentes se complementan. Al producirlas conviene resolver estos cruces una sola vez:

| Cruce | Decisión de diseño |
|---|---|
| Escala normativa de M1 y protección normativa de M3 | Compartir la vista de jerarquía. Desde M3 abrir sus instrumentos y mecanismos de protección, sin recrear otra pirámide con niveles distintos. |
| Panorama judicial de M1 y organización de cada fuero en M2 | Un mapa institucional de entrada y vistas de detalle por fuero. Las mismas instituciones conservan su nombre y se enlazan; cada detalle explica la relación particular que corresponda. |
| Circunscripciones en M1, Paz, Familia, Laboral y Penal | Una capa territorial común. Los repartos de órganos por fuero requieren su fuente particular; el color de una circunscripción no reemplaza la regla de competencia. |
| Vulnerabilidad, barreras y accesibilidad en M3–M5 | Un núcleo transversal de casos y vistas conectadas. Conservar las clasificaciones de cada fuente, sin convertirlas en una única lista artificial. |
| Herramientas digitales de los distintos fueros | Reunirlas en la matriz funcional V20 de M2 y enlazar desde los recorridos. El Bus Federal mantiene su flujo específico V07. |
| Protocolo laboral de género y atención general de M5 | Mantener circuitos propios y conectar principios comunes de trato, orientación y privacidad. La pauta general de atención no sustituye las condiciones del protocolo especial. |

## Condiciones para que los nuevos mapas ayuden a recordar

1. **Una pregunta central por vista.** El mapa general ubica; los detalles se abren por órgano, fuero o trámite. No copiar páginas enteras dentro de recuadros.
2. **Ubicación estable.** Mantener la disposición al ocultar etiquetas o practicar. Así la posición puede servir de pista para recuperar lo estudiado. El significado debe quedar escrito y no depender sólo del color.
3. **Fuente en cada concepto.** Conservar el acceso al PDF y a la página exacta en lectura, recuperación y reconstrucción. Para anexos, mostrar también artículo y nombre de la norma. Un enlace general al inicio del módulo no basta para un mapa de detalle.
4. **Relaciones que se puedan decir en voz alta.** Por ejemplo: «esta autoridad designa con acuerdo de…», «este órgano revisa cuando…» o «este derecho exige al Estado…». Acertar un nombre no demuestra que se entendió la relación.
5. **Recuperación con dificultad gradual.** Ver el mapa; ocultar nombres; reconstruir ramas; explicar vínculos; resolver un caso que cambie una condición. Comprobar con la fuente después del intento.
6. **Reglas y excepciones juntas.** Incluir condiciones, bifurcaciones y límites que cambian la respuesta. Una mnemotecnia no debe borrar una excepción legal.
7. **Versiones legibles en pantalla chica.** Dar una vista por niveles y una alternativa textual desplegable. Evitar depender de desplazarse por un lienzo enorme o de letras diminutas.

## Un límite de la herramienta actual

La representación actual utiliza la misma estructura de raíz → grupos → nodos en `memoria.js`, función `renderMap`. Esto sirve para los mapas sintéticos existentes, pero no representa por sí solo relaciones entre nodos de distintas ramas ni una profundidad variable. Los tipos `concept`, `sequence` y `matrix` comparten la estructura HTML, con diferencias de presentación.

Por eso **añadir más tarjetas al dibujo actual no alcanza para producir el organigrama solicitado**. La ampliación debería permitir ramas anidadas para la organización institucional y flujos con bifurcaciones para los procesos. Las secuencias actuales numeran dentro de cada grupo: si se diseña un recorrido continuo, esa numeración debe comprobarse. Evidencia: [renderizado de mapas](../memoria.js) y [estilos del atlas](../memoria.css).

Esto es un hallazgo para una implementación posterior. Esta revisión no modifica el funcionamiento del simulador, el atlas ni los historiales de estudio.

## Comprobación de la entrega

La [verificación mecánica](AUDITORIA-MAPAS-VERIFICACION.json) comprueba que los enlaces locales de estos informes resuelvan, que las referencias de Markdown estén definidas, que las páginas enlazadas existan dentro de sus PDF y que el inventario coincida con los archivos fuente. Las comprobaciones de contenido y sus límites se explican en cada informe; esta validación de enlaces no equivale a certificar por sí sola una regla jurídica.
