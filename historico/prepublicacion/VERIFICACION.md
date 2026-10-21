# Verificación del paquete preparatorio

Fecha: 5 de octubre de 2026.

- La Acordada 32.748 se inspeccionó visualmente. La página 14 del PDF establece 50 preguntas, cuatro opciones, 40 minutos y mínimo de 35 respuestas correctas para conocimientos específicos.
- Los 43 PDF del inventario histórico se abrieron y contrastaron con sus hashes y números de páginas. Las rutas descargadas del catálogo existen.
- La revisión independiente de contenido está en `REVISION-CONTENIDO.md`. Registra muestras revisadas, correcciones y sus límites; no constituye una garantía de exactitud absoluta.
- `python preparar_material.py` verifica IDs únicos, etapas, cantidad de opciones, claves dentro del rango, explicaciones, fuentes, textos de lectura agrupados y cantidades mínimas. Genera los datos del simulador y el cuaderno imprimible.
- `node --check app.js` verifica sintaxis.
- `node verificar_simulador.cjs` comprueba corrección completa, parcial y omisiones; agrupación de lectura; persistencia y repaso de errores; doble envío y finalización por tiempo agotado. Es una prueba de lógica con DOM simulado.
- En navegador se verificaron carga del banco, simulacro específico de 50 preguntas/200 opciones/40 minutos, lectura de 10 preguntas/30 opciones/30 minutos, selección de respuestas, correcciones, explicaciones y registro del resultado. Durante la comprobación de envío con omisiones, el diálogo nativo bloqueó el control automatizado del navegador; se sustituyeron los diálogos nativos por confirmaciones dentro de la página. La lógica final de omisiones y vencimiento se verificó con el programa anterior; esa sustitución no tiene comprobación visual completa.

El resultado de una práctica no acredita aprobación del concurso. Falta contrastar el paquete con el programa y los videos oficiales 2026 cuando sean publicados. Tampoco se verificó la reproducción completa de los videos históricos: están enlazados y el catálogo distingue disponibilidad HTTP de reproducción.
