# Preparación judicial Mendoza · programa 2026

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

Desde el 15/10/2026, el simulador registra las preguntas al mostrarlas, incluso si se abandona. En estudio entrega hasta diez preguntas nuevas del filtro elegido, sin rellenar con conocidas si quedan menos de diez. Una vez agotadas, informa que empieza un repaso y prioriza las menos vistas y más antiguas. Los simulacros conservan su cantidad y distribución, priorizando nuevas; si necesitan repetir lo indican. Comprensión alterna los seis pasajes antes de repetir. El historial previo se aprovecha cuando contiene IDs. El registro de exposición también se exporta y se conserva al borrar resultados; «Repasar mis errores» permite repetir intencionalmente.

Desde el 21/10/2026, el atlas incorpora mapas por niveles, flujos con decisiones, búsqueda por concepto y enfoque por rama. Empezá por [la estructura judicial](memoria.html#map=m1-estructura-judicial) y consultá [cómo estudiar con los mapas ampliados](estudio-2026/GUIA-MAPAS-2026.md). Las fuentes siguen disponibles al practicar y las explicaciones propias se conservan al exportar.

## Documentos y reproducibilidad

[Manual](MANUAL-DE-PREPARACION.md) · [Plan](PLAN-DE-ESTUDIO.md) · [Etapas](GUIA-CONCURSO-2026.md) · [Biblioteca](BIBLIOTECA-Y-TEMARIO.md) · [Comparación](ACTUALIZACION-2026.md) · [Revisión](REVISION-CONTENIDO.md) · [Ejercicios imprimibles](CUADERNO-DE-EJERCICIOS.html).

Para regenerar datos después de editar guías y bancos: `python integrar_documentos_2026.py`, `python integrar_bancos_2026.py`, `python generar_fuentes_2026.py`, `python preparar_mapas.py`, `python preparar_material.py`, `python preparar_taller.py`. Verificar con `node verificar_simulador.cjs`; empaquetar con `python empaquetar.py`. Los MP4 se conservan ya renderizados. Estos scripts requieren Python y las bibliotecas usadas por los autores; estudiar con el paquete generado no requiere ejecutarlos.

Procedencia: [material oficial 2026](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026-material-de-estudio/), [convocatoria y novedades](https://jusmendoza.gob.ar/concurso-ingreso-administrativo-2026/). Fecha de descarga, URL y SHA-256 en los manifiestos de la biblioteca.

## Copia del repositorio y paquetes ZIP

El repositorio conserva el proyecto completo, incluidos PDF, guías, datos y videos terminados. Después de descargarlo o clonarlo, abrí `index.html` manteniendo sus carpetas. Los ZIP generados se conservan localmente y se excluyen de Git porque superan 100 MiB por archivo. Para generar el paquete completo ejecutá `python empaquetar.py`; comprueba el contenido con CRC y SHA-256 y escribe `PREPARACION-JUDICIAL-MENDOZA-2026-TALLER.zip`. El ZIP preparatorio antiguo también deja de versionarse; su copia local y el historial Git se conservan.
