# Revisión de implementación de mapas M1

21/10/2026. Propiedad de esta entrega: `m1.json` y este cierre. No se modificaron datos compartidos ni archivos de interfaz. La auditoría previa sigue en `estudio-2026/AUDITORIA-MAPAS-M1.md`.

## Entrega y cobertura

11 vistas reales, 213 nodos contando todos los hijos; hasta tres niveles, 14 aristas explícitas y 295 referencias de fuente (284 en nodos y 11 en raíces). Tres IDs existentes se conservan y se sustituyen con contenido enriquecido. Cada vista tiene actividad con respuesta, cautelas, fuentes y enlaces a vistas relacionadas. Las clasificaciones, matrices y secuencias tienen su tipo; no todo se presenta como cadena de mando.

| Propuesta auditada | ID implementado | Qué se puede estudiar |
|---|---|---|
| Estado existente | `estado` | Elementos, constituyente/constituido, representación, república y autonomía. |
| A: panorama judicial | `m1-estructura-judicial` | Dos órdenes, niveles provinciales/federales, autoridades ministeriales, revisión y superintendencia. |
| B: escala normativa | `m1-normas` | Cinco niveles del esquema M1, constitucionalidad y límites territoriales. |
| C: designación/remoción | `m1-designacion` | Cuatro carriles con aristas secuenciales y cuadro de remoción. |
| Corte existente | `corte` | Tres funciones con ejemplos, prudencia y límites. |
| Complemento Ley9423 | `m1-corte-organizacion` | Pleno, colegio sorteado, Sala Administrativa, Presidencia, soportes y pleno/plenaria. |
| D: órganos/funciones | `m1-organos-funciones` | Matriz Nación/Mendoza/municipio y función por contenido; controles DNU. |
| E: jerarquía verdadera | `administracion` | Ejemplo A/B/C, grado, línea, staff, facultades y competencia del órgano. |
| F: formas administrativas | `m1-formas-administrativas` | Cinco figuras, elementos, caracteres, nueve clases, cuatro vicios y reglamentos. |
| G: empleo | `m1-empleo` | Matriz de deberes/prohibiciones, fuentes, residencia, orden válida y plazos. |
| Capa territorial compartida | `m1-territorio` | Las cuatro circunscripciones y los 18 departamentos, con FAQ oficial. |

## Verificación realizada

- Lectura del contrato `FORMATO.md`; JSON parseado y campos obligatorios comprobados.
- Cada nodo e hijo lleva fuente primaria propia. Páginas de módulos cotejadas contra `indice-2026.json`; referencias locales existen y páginas PDF dentro de límites reales. HTML usa sección, sin página inventada.
- ID único dentro de cada vista, extremos de aristas existentes y relacionados resolubles dentro de estas 11 vistas. Las aristas de flujo conectan pasos hermanos; no repiten cada vínculo padre/hijo.
- El texto M1 completo se revisó durante auditoría; recuadros de misión/visión inspeccionados visualmente. La tabla gráfica p.12 se contrasta con transcripción de guía previamente revisada; sus datos se conservan como comparación, sin inventar total de diputados.
- Ley9423 leída directamente: pp.1–4 durante auditoría y pp.5–7 durante implementación. Norma de siete páginas, no remisión fantasma al desarrollo faltante de M2. Secretarías se expresa como posibilidad normativa, sin afirmar dotación efectiva actual.
- Reglamento PJ leído pp.1,2,6; DL560 pp.4–6; modificación Ley9665 contrastada en HTML local. Los nodos agrupan reglas; no sustituyen literalidad de todos los incisos, accesibles desde la fuente y guía existente.
- Constitución Nacional oficial consultada para art.120 (Ministerio Público independiente) y art.99 incs.3–4 (DNU y designación/edad federal). Los nodos correspondientes enlazan fuente oficial por sección.
- Distribución territorial tomada de verificación oficial FAQ2026 documentada por auditoría consolidada; M2 pp.11/36 confirma existencia de cuatro circunscripciones. No se asignan competencias materiales ni rutas recursivas a partir de departamentos.

## Límites resueltos en el contenido

Superintendencia, revisión judicial y jerarquía fiscal tienen etiquetas distintas. La subordinación explícita del MPF queda anidada Procurador → integrantes propios, sin incluir jueces o defensores. Ministerio Público nacional se representa independiente con fuente art.120 CN. Se distingue mínimo constitucional de siete y composición legal de siete de la Corte mendocina.

Colegio de tres ministros sorteados no se confunde con tres autoridades de Sala Administrativa. Sentencia en pleno art.9 y plenaria art.10 tienen condiciones y recursos diferenciados. No se reconstruyen salas permanentes antiguas ni se presentan plazos históricos de implementación como futuros del concurso.

Se excluyen como afirmaciones operativas pena capital, causal de crímenes comunes supuestamente exclusiva provincial y redacción defectuosa DNU de p.38. El control DNU se ancla en art.99 inc.3: la ley especial regula el mecanismo, no aprueba por sí cada decreto. Buena conducta se acompaña de responsabilidad y límite federal de nuevo nombramiento a los 75 años.

Los esquemas tienen actividades originales respondidas. No se convierten en directorio vivo de oficinas, reglas exhaustivas de competencia ni asesoramiento para casos reales. El territorio es distribución geográfica y el ejemplo administrativo A/B/C está expresamente rotulado didáctico.

## Integración

La raíz contiene `version`, `maps` y `coverage`. Reemplazar únicamente `estado`, `corte` y `administracion`; agregar los otros ocho IDs. Conservar tarjetas, pares y casos actuales. Los IDs de vistas y `related` ya coinciden con reservas compartidas. No se ejecutó ni modificó interfaz en esta entrega: verificación de presentación corresponde a integración del coordinador.

## Cierre de la revisión final

La continuación conservó las 11 vistas y los 213 IDs de nodos existentes. Se cotejó nuevamente la Ley 9423 completa y se precisaron la elección de ambas vicepresidencias, las oportunidades de convocatoria del art. 9, la convocatoria de la plenaria del art. 10 y los órganos alcanzados por el recurso jerárquico. Se explicitó que el plazo familiar corre desde el cambio y que su inciso no lo califica como corrido. Se corrigieron espacios y una referencia territorial abreviada de los requisitos del Senado.

La clasificación DNU/delegado ahora enlaza directamente los arts. 99 inc. 3 y 76 de la Constitución Nacional oficial, cotejados en línea; no descansa sólo en el párrafo erróneo del módulo. La validación final no encontró campos faltantes, nodos sin fuente, páginas fuera de rango, IDs duplicados, extremos de aristas inválidos, relacionados rotos ni marcadores pendientes. Cobertura M1-A a M1-G y complementos completa. El contenido de esta entrega está cerrado; la comprobación visual y de los modos de práctica se realiza al integrarlo en la interfaz.
