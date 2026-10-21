# Revisión final de mapas M3–M5

Fecha: 21/10/2026. Estado de autoría: **completo**. Archivo de datos: `mapas-2026/m3-m5.json`. Se retomaron las once vistas ya guardadas y se completaron las ampliaciones y las dos vistas restantes de M5. No se modificó la aplicación ni `memoria-datos.json` desde esta tarea; integración y prueba de interfaz corresponden al integrador.

## Alcance y cobertura

**13 vistas: seis IDs actuales conservados y siete vistas nuevas. Diez guiones A–J implementados, incluidos B y J.** Las tarjetas, contrastes y casos existentes se conservan para la integración. Las actividades de recuperación de estas trece vistas son originales y tienen respuesta explicada.

| Propuesta | Vistas | Cobertura implementada |
|---|---|---|
| M3-A | `m3-proteccion` | Tutela interna/internacional, sistemas y funciones, instrumentos, convencionalidad y enfoque de políticas; jerarquía enlazada a m1-normas. |
| M3-B | `m3-red-derechos` | Implementada también la profundización opcional: propiedades, tres clasificaciones equivalentes y franja histórica sin jerarquía de valor. |
| M3-C | `derechos` | Titular y garante, principios, atribución y diligencia, igualdad situada, razonabilidad y medidas de equiparación; barreras enlazadas a accesibilidad. |
| M4-D | `m4-desigualdades`, `genero` | Construcción de desigualdades y tres herramientas; contexto de diversidad y marco normativo en la entrada conservada. |
| M4-E | `m4-ciclo-respuesta`, `violencias` | Ciclo no universal, propiedades/riesgo, mitos, respuesta institucional y retractación; definición legal y ejes tipo/modalidad conservados. |
| M4-F | `m4-protocolo` | Consulta sin obligación de denunciar, formalización, vías y condiciones distintas, recomendaciones y respuesta fundada RRHH; cotejo del original PDF17–19. |
| M5-G | `m5-atencion`, `servicio` | Niveles de principios/calidad/pilares, diagnóstico, simplificación y quejas; seis etapas con contacto/emoción/estrategia y capas formal/humana. |
| M5-H | `m5-comunicacion` | Cinco dimensiones, diez técnicas, no verbal contextual, escucha, situaciones difíciles y cinco medios de retroalimentación. |
| M5-I | `accesibilidad` | Acceso amplio/integral, modelo social, diseño/ajustes, cuatro dimensiones, familias M3 y barreras M5 separadas, adaptaciones y responsabilidades. |
| M5-J | `competencias` | Implementada también la profundización opcional: cinco componentes, iceberg, cuatro idoneidades, habilidades, cuatro etapas y ética con ocho cualidades. |

## Recuentos verificados

Nodos principales = primer nivel de cada grupo. Nodos totales = principales más todos sus hijos. Las aristas explícitas no incluyen las relaciones padre/hijo, que ya están expresadas en el árbol.

| ID | Módulo | Grupos | Nodos principales | Nodos totales | Aristas |
|---|---:|---:|---:|---:|---:|
| `derechos` | 3 | 5 | 17 | 25 | 7 |
| `genero` | 4 | 5 | 8 | 8 | 0 |
| `violencias` | 4 | 3 | 17 | 18 | 0 |
| `servicio` | 5 | 4 | 10 | 28 | 7 |
| `accesibilidad` | 5 | 6 | 25 | 26 | 14 |
| `competencias` | 5 | 6 | 22 | 30 | 8 |
| `m3-proteccion` | 3 | 5 | 12 | 31 | 4 |
| `m3-red-derechos` | 3 | 3 | 11 | 15 | 4 |
| `m4-desigualdades` | 4 | 4 | 11 | 13 | 5 |
| `m4-ciclo-respuesta` | 4 | 4 | 14 | 19 | 7 |
| `m4-protocolo` | 4 | 5 | 13 | 28 | 10 |
| `m5-atencion` | 5 | 6 | 21 | 43 | 10 |
| `m5-comunicacion` | 5 | 6 | 22 | 38 | 8 |
| **Total** | **3–5** | **62** | **203** | **322** | **84** |

## Fidelidad de las relaciones

- M3 conserva el vínculo persona titular / Estado primer garante; distingue abstención, conductas activas, protección como especie y satisfacción. Los actos de agentes prevaliéndose del poder público pueden comprometer al Estado aun fuera de competencia. El daño privado no lo hace automáticamente: se analiza la diligencia estatal. Pro personae distingue selección e interpretación. La igualdad sustantiva considera efectos de reglas aparentemente neutrales y razonabilidad de respuestas.
- La clasificación de derechos y su cronología no forman una jerarquía de importancia. Los instrumentos constitucionales se enumeran en detalles desplegables con sus nombres, y las cuatro elevaciones posteriores conservan las leyes del listado de M3 p. 5. La jerarquía enlaza a `m1-normas` sin duplicar su pirámide. Comisión y Corte tienen funciones diferenciadas; no se les atribuyen efectos idénticos. El control de convencionalidad conserva el límite de competencia de cada agencia.
- M4 separa asignaciones sociales de capacidades naturales, y orientación/identidad/expresión de presunciones culturales. El marco de protección no equipara el rango de bloque constitucional, Yogyakarta y ley especial. Tipos y modalidades de violencia siguen como ejes cruzados. Ciclo, propiedades y evaluación de riesgo están separados; el círculo no es condición necesaria ni predictor universal.
- En el protocolo laboral, consultar no obliga a denunciar. La compulsa administrativa requiere voluntad expresa; la vía por delito perseguible de oficio conserva su regla específica; la instancia privada requiere asesoramiento y voluntad de remisión; el colegio profesional requiere consentimiento previo. El relato en consulta puede activar la función de comunicación ante posible delito de oficio según el original p. 13. Las recomendaciones preventivas de PDF19 conservan sus condiciones, incluido cambio de destino de afectada solo a pedido expreso; RRHH responde fundada y ágilmente. No son sanciones automáticas.
- M5 distingue siete principios de servicio, marco de función pública, cinco dimensiones SERVQUAL y cuatro pilares. El viaje conserva seis estaciones y añade punto de contacto, emoción posible y estrategia; separa garantías jurídicas y expectativas humanas sin reemplazar unas por otras. Los circuitos de diagnóstico, quejas y comunicación contienen acciones y límites de competencia.
- Las tres familias de barreras M3 más género, las cuatro dimensiones de accesibilidad y las cinco barreras M5 se presentan en paneles distintos con vínculos muchos a muchos. Diseño universal y ajuste razonable no son sinónimos. Las adaptaciones parten de necesidades observadas, y la respuesta individual se distingue de la política institucional.
- Los cinco componentes profesionales, iceberg, cuatro idoneidades, habilidades, etapas de aprendizaje y ética son modelos complementarios. No hay correspondencias artificiales. Se incluyen ocho cualidades éticas. Las notas 7/38/55 y 77/23 se acotan al material y no se convierten en reglas universales o de evaluación individual.

## Comprobaciones realizadas

1. Parseo del JSON UTF-8: correcto. Trece IDs de mapa únicos y diez entradas de cobertura válidas. Todos los IDs originales de nodos de los seis mapas compartidos siguen presentes.
2. Cada nodo e hijo contiene ID, etiqueta, detalle y al menos una fuente primaria. Cada hijo tiene relación propia; todos los grupos tienen ID y relación. Cada vista tiene raíz documentada, actividad respondida y precauciones concretas.
3. Fuentes comprobadas contra los PDF locales de programa M3 (contenido pp. 2–23), M4 (pp. 2–10) y M5 (pp. 2–30), y pasajes pertinentes del protocolo original (PDF8–9, 13, 15–20). Se verificó además la tabla de idoneidad M5 PDF25 en imagen de página. Las páginas representan posición PDF, incluida portada.
4. Comprobación automática de existencia de archivos de fuente y rango de páginas: correcta. No se usan páginas ficticias para HTML ni fuentes externas nuevas.
5. Todas las aristas tienen extremos existentes dentro de su propia vista, etiqueta no vacía y tipo permitido. Enlaces `related` válidos dentro de M3–M5 o al ID reservado `m1-normas`.
6. Ningún marcador de trabajo pendiente ni ejercicio genérico sin respuesta específica. Máximo de seis grupos por vista; los detalles extensos se guardan como hijos desplegables.

**Resultado de validación de datos: 0 errores.** Este cierre verifica contenidos y contrato de datos; no afirma una prueba de navegador de la integración realizada por otra tarea. No se hizo commit ni push.
