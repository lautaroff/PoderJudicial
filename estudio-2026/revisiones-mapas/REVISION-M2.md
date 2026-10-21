# Revisión de mapas del Módulo 2

Cierre de contenido: 21/10/2026. Archivo entregable: `mapas-2026/m2.json`. Continuación sobre las 16 vistas ya guardadas; no se reinició el trabajo ni se modificaron bancos, HTML, JavaScript, CSS u otros módulos. Sin commit ni push.

## Cobertura final

20 paquetes V01–V20 implementados en 25 mapas: las vistas de jurados y los cuatro detalles juveniles separan recorridos que resultarían demasiado densos en una lámina única.

| Paquete | Mapas | Alcance |
|---|---|---|
| V01 | `fueros` | Sustituye el mapa de entrada; conserva su ID. |
| V02 | `m2-ejes-proceso` | Ejes, participantes, trece principios y vías constitucionales. |
| V03 | `proceso` | Sustituye mapa actual; incorpora audiencia final, prueba y bifurcación. |
| V04 | `m2-notificaciones-cautelares` | Notificaciones, destinos, cautela y cuatro medidas. |
| V05 | `m2-paz` | Competencias, variantes, pequeñas causas y contravencional; desalojo cotejado normativamente. |
| V06 | `m2-oficina-civil` | Expediente, soporte, escritos, tiempos y resoluciones. |
| V07 | `m2-comunicacion` | Fusiona repetición del Bus; incluye controles y circuito de respuesta. |
| V08 | `m2-blsg` | Adaptación del diagrama primario, con decisión y salida incidental. |
| V09 | `m2-tributario` | Ramas tributarias, actores, título, diez excepciones y cierre del apremio. |
| V10 | `m2-concursal` | Clasificación completa, principios, sujetos, satélites y territorio. |
| V11 | `m2-recorridos-concursales` | Tres recorridos primarios adaptados con cotejo LCQ/CPCCyT. |
| V12 | `m2-familia` | Instituciones, territorio, auxiliares, NNA y fuentes/vías sin plazos inventados. |
| V13 | `m2-principios-laborales` | Ramas, principios, gratuidad, poderes y fuentes. |
| V14 | `m2-acceso-laboral` | Despido/riesgos, excepciones y organización/revisión. |
| V15 | `m2-proceso-laboral` | Cuatro períodos, pruebas, controles, excepciones e impulso. |
| V16 | `m2-garantias-penales` | Ejes, ocho garantías y cuatro filtros. |
| V17 | `penal`, `m2-jurados` | Funciones, OGAP y territorio; detalle de competencia, selección, debate y bifurcaciones del veredicto. |
| V18 | `m2-juvenil` | Fuentes y aplicación; órganos, partes, administración, supervisión, garantías y vía no punitiva. |
| V19 | `m2-recorridos-juveniles`, `m2-investigacion-juvenil`, `m2-coercion-custodia-juvenil`, `m2-juicio-alternativas-juveniles`, `m2-revision-ejecucion-juvenil` | Atlas general y cuatro detalles: ocho familias de recorridos, actos iniciales, autoridades, prórrogas, excepciones y efectos. |
| V20 | `m2-sistemas` | Matriz de fueros/herramientas, flujo funcional, fondos/consultas y reglas diferenciadas de acceso y privacidad. |

## Recuentos y validación del archivo

- 25 mapas, 95 grupos y 429 nodos, incluidos 78 hijos; profundidad máxima de nodo: 3 niveles.
- 159 aristas explícitas, todas rotuladas, con extremos de IDs existentes dentro de su mapa y tipo admitido.
- 543 referencias de fuente entre raíces y nodos (se cuentan apariciones, no documentos únicos).
- Todas las raíces tienen fuentes; cada nodo/hijo tiene fuente primaria, detalle y relación; todas las vistas tienen ejercicio con respuesta, precauciones y relaciones a mapas existentes.
- JSON parseado nuevamente; IDs únicos por mapa, sin colisiones de grupo/nodo, cobertura ordenada V01–V20 y sin mapas fuera de cobertura.
- Rutas locales existentes; páginas de PDFs dentro del número real de páginas; HTML con sección y sin página inventada. Sin TODO/TBD/FIXME.
- Revisión de valores visibles para corregir palabras/números pegados, sin cambiar IDs ni rutas de archivos.

La validación de datos no equivale a verificación visual móvil de la aplicación. El integrador realiza el render, la integración y la prueba de práctica/navegación.

## Cotejos realizados en esta continuación

1. Se leyeron formato, auditoría M2 y las 16 vistas existentes. Se revisaron y ampliaron reglas de audiencias, testigos y recepción fuera de sede; clasificación/participantes y nombres de los trece principios; destinos de notificación; territorio y códigos de Paz; conductas del ejecutado; ramas concursales y participación de NNA. No se importaron plazos familiares de ediciones anteriores.
2. Se cotejó visualmente el Código Procesal Penal Juvenil escaneado, páginas PDF 1–28, mediante render de las páginas originales, incluida la continuación de artículos entre páginas. El OCR auxiliar se utilizó para localizar contenido y nunca como única prueba de cifras. La página 29 de firmas no se convierte en regla procesal.
3. Se revisaron las páginas 1–5 de la Ley 9735 en su extracción primaria. Se corrigió la referencia a derogación: art. 14 está en página PDF 5, mientras la modificación del CPP art. 13 comienza en página 4. Organización DRPJ, educación, disciplina y OAP se citaron desde la ley.
4. Se inspeccionaron visualmente M2 páginas 95, 97 y 98 para territorio penal, selección y debate por jurados; y 111, 112 y 113 para recorridos concursales. Las conexiones del gráfico territorial se tradujeron como ubicación/función o revisión según norma, nunca como mando personal entre jueces.
5. Se releyeron CPCCyT art. 237 II.1–12 y art. 242: sentencia inicial del desalojo 5 días, desahucio 15, oposición dentro del plazo otorgado para desalojar; traslado 5, resolución 10 desde firmeza de llamamiento. No se reprodujo el arrastre «pasados 5» del módulo ni el rótulo de prenda con desplazamiento.
6. Se cotejó CPCCyT arts. 359–372: conformidades 30 días desde orden de edictos; doble mayoría; oposición limitada con prueba/resolución; sin inventar una vista autónoma de 10 días. Mediación, homologación parcial, conciliación, rebeldía, plan de saneamiento y fracaso conservan sus condiciones. LCQ arts. 35–43, 46/48 y 230–231 respaldan relojes de informes/exclusividad y separación clausura/conclusión; las restantes remisiones se mantienen como consulta legal por sección, sin extraer relojes gráficos dudosos.
7. Para sistemas se releyeron M2 34–35, 69–70, 77–78 y 99–109: Iurix ADF/Flex, LeD, Portal/MeeD, Agenda, video, SINEJ, correo, BNA Net y ReDAM tienen funciones diferenciadas. Acceso, publicidad y reserva se contrastaron con Código arts. 5–7.
8. CIDH: páginas PDF 30, 31, 35, 36, 42, 57 y 58 cotejadas en extracción primaria; corresponde a inicio de lectura en impresa 17 y cierre en 45. Los cinco principios tienen detalles y referencias; se conserva la fecha 2011 para no transformar ejemplos históricos en legislación mendocina 2026.

## Relojes juveniles preservados

- Art. 4: días hábiles; no borrar unidades expresas de horas, meses o días corridos.
- Art. 25: disposición inmediata y máximo improrrogable 3 horas; art. 26: UPANA máximo 2 días, no pena ni internación definitiva.
- Art. 27: imputación máximo 12 horas desde puesta a disposición y otras 12 con fundamento. Art. 28: DRPJ notificada máximo 3 horas desde imputación e informe dentro de 48 horas; el texto no formula un acto inicial autónomo adicional para este último lapso y el mapa no lo inventa.
- Art. 29: IPP 3 meses desde imputación, otro tanto por decisión judicial a pedido fiscal; suma gravedad/muy difícil investigación puede llevar a máximo total 12 meses con prórrogas.
- Art. 41: requerir restricción en 5 días desde imputación; ampliación única hasta 5 adicionales pedida antes de vencer, juez resuelve **esa ampliación** en 1 día. Preventiva hasta 3 meses desde detención efectiva, prórrogas trimestrales y máximo total 18. La decisión sobre medida se dicta oral e inmediatamente al concluir audiencia; no es un plazo general de 1 día.
- Art. 47: órgano **convocará** audiencia dentro de máximo 2 días hábiles; al finalizar resuelve oral e inmediatamente y **diferirá** fundamentos dentro de 3 días hábiles. No se cambió convocar por celebrar ni diferirá por podrá diferir.
- Arts. 48–52: prórroga de custodia se resuelve en 48 horas previa vista a Asesoría; modificación/suspensión fundada se solicita dentro de 48 horas de producida, con escucha antes de resolver prórroga/modificación. Restitución de derechos: informar cese dentro de 24 horas; accesorias: auto fundado en 1 día. El cese a los 18 es de custodia, no extinción automática de pena.
- Art. 63: flagrancia: audiencia inicial debe celebrarse dentro de 3 días desde imputación formal; prórroga excepcional por período igual con condiciones expresas. No aplicar este reloj a audiencia de custodia.
- Arts. 73–75: revisión amplia escrita y fundada dentro de 10 días de notificada condena; audiencia solo por los supuestos legales, se fija dentro de 10 siguientes; resolución de 5 posteriores según la fórmula literal del art. 74. No completar por suposición el plazo de fase escrita que el artículo no precisa adicionalmente.
- Arts. 19, 78, 86, 89–91: informes ordinarios con periodicidad judicial no superior a 3 meses; salud durante ejecución, informes no más espaciados que 30 días corridos. 1/3, 1/2 y 2/3 habilitan evaluación de progresión/sustitución, sin derecho automático; denegación fija reconsideración no superior a 3 meses.

## Límites y precauciones conservados

- Ocho familias juveniles cubiertas: investigación, coerción, custodia, juicio, restaurativa/prueba, revisión, ejecución y no punibles. No se afirma que cada caso recorra todas las ramas.
- MPF y defensa tienen funciones propias; OGAP/OAP gestionan, supervisor informa y DRPJ ejecuta materialmente. Órgano competente decide; compartir actuaciones no crea subordinación de las partes ni de un juez a otro.
- Organización territorial es la que describe el material del concurso; no certifica dotaciones actuales. Inconsistencias de Paz p. 22 (asiento de Segunda y número/localidades de Santa Rosa) permanecen explícitas, sin corregir por conjetura.
- No se publica una fecha exacta de vigencia inferida solo de publicación de Ley 9735. Los enlaces del Boletín Oficial fueron intentados por la herramienta web y no resultaron accesibles allí; el cotejo es con las copias oficiales ya conservadas en la biblioteca, no una nueva certificación de actualización externa.
- El informe CIDH es histórico y normativo en derechos humanos; sus ejemplos nacionales de 2010/2011 no describen automáticamente la ley positiva de 2026.
- Los mapas sintetizan y enlazan la fuente. No transcriben íntegramente todos los artículos, ni reemplazan la lectura de las partes legales remitidas por el programa.
- No se tocaron `video-estudio/`, los bancos ni los archivos compartidos de aplicación. No hubo commit, push ni despliegue.
