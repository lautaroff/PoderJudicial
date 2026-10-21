# Preparación judicial Mendoza · programa 2026

Abrí [index.html](index.html) con doble clic. Conservá la carpeta completa: funciona 100 % sin conexión, sin instalar programas y sin subir resultados. El PDF se abre en el visor del navegador; cada enlace indica su página. En modo estudio podés profundizar mientras practicás; en simulacro, al corregir.

## Por dónde empezar

1. Abrí «Mi recorrido» en [index.html](index.html), leé las reglas y el plan de 28 sesiones, y usá los semáforos de dominio por apartado.
2. Elegí módulo: PDF completo, guía explicada y práctica directa por apartado o por plazos y números.
3. Practicá en el **Simulador y entrenador**:
   - **Práctica guiada por tema** (sin reloj, con acceso inmediato a la fuente).
   - **Entrenador de números, plazos y competencias** (117 ítems verificados de completar huecos y órganos, con alertas de trampas frecuentes).
   - **Simulacros cronometrados** (distribución proporcional al peso real del temario, equilibrada o al azar, con hoja de respuestas OMR interactiva, marcado `⚑` para revisar, descarte de distractores `✕` y ritmo sugerido).
4. Entrá en [Mapas y tarjetas](memoria.html): ocultá conceptos, reconstruí conexiones con control de conceptos ya usados y respondé antes de revelar.
5. Entrá al [Taller de dominio](taller.html): explicá sin opciones, compará casos, ordená procesos y corregí errores. Conservá los diagnósticos A/B para comprobar aprendizaje con preguntas nuevas.
6. Alterná comprensión (en pantalla dividida con el texto fijo) y las dos jornadas de video originales (con narración por voz opcional y bloc de apuntes integrado); corregí desde las fuentes. [Rutina del taller](estudio-2026/COMO-USAR-TALLER.md).

## Contenido y mejoras implementadas (octubre de 2026)

- **Índice y cinco módulos oficiales completos**: 220 páginas PDF, con biblioteca y lector integrado por hoja.
- **Banco específico renovado y equilibrado**: 575 preguntas de opción múltiple (475 específicas, 40 institucionales, 60 de lectura) + 160 preguntas reservadas en el taller (diagnósticos A/B y videos), todas con distractores equilibrados en extensión (0 % de sesgo por longitud en `herramientas/calidad/sesgo_opciones.py --estricto`) y barajado aleatorio de opciones en tiempo de ejecución.
- **Entrenador de números, plazos y competencias**: 117 ítems verificados contra página oficial (`contenido/plazos/numeros.json`) sobre plazos procesales, cómputo de días, edades, mayorías, duración de mandatos, números de ley y órganos competentes.
- **Mapas, tarjetas, contrastes y casos**: 49 mapas interactivos, 120 tarjetas con repetición espaciada normalizada a medianoche local, 12 contrastes y 15 casos con opciones barajadas y puentes directos de práctica.
- **Taller de dominio**: 90 preguntas abiertas con rúbricas, 20 pares de casos, 12 secuencias con foco accesible, 20 párrafos con error, dos diagnósticos específicos, dos textos nuevos de lectura en vista dividida y dos jornadas de video con narración TTS opcional y bloc de apuntes.
- **Continuidad e importación/exportación**: persistencia automática de cuestionarios en curso, etiquetado de causas de error (`Plazo/número`, `Órgano/competencia`, `Condición/excepción`, `Lectura rápida`) y botones para exportar e importar tus avances JSON en las tres aplicaciones.

Las cantidades verificadas y los controles técnicos se detallan en [estudio-2026/VERIFICACION.md](estudio-2026/VERIFICACION.md).

## Organización del repositorio

- **Raíz (`/`)**: páginas de entrada (`index.html`, `memoria.html`, `taller.html`, `CUADERNO-DE-EJERCICIOS.html`) y paquetes JS/CSS listos para usar sin servidor (`app.js`, `memoria.js`, `mapas.js`, `taller.js`, `datos-*.js`, `fuentes-2026.js`, `memoria-datos.js`, `taller-datos.js`).
- **`contenido/`**: fuentes canónicas JSON editables (`bancos/`, `taller/`, `mapas/`, `plazos/`, `integrado/`).
- **`estudio-2026/`**: manual de preparación, plan de 28 sesiones, guías explicadas por módulo y anexos, e informes de verificación.
- **`biblioteca/`**: PDF oficiales del programa 2026, normativa de referencia con manifiestos SHA-256 y material histórico.
- **`herramientas/`**: pipeline de construcción (`construir.py`), scripts de preparación, utilidades de autoría (`autoria/`) y validadores de calidad (`calidad/`).
- **`validaciones/`**: reportes JSON generados automáticamente por los controles de integridad y simulador.
- **`videos/`**: jornadas de video MP4, subtítulos VTT y transcripciones.
- **`historico/` y `paquetes/`**: archivos de etapas previas y paquetes ZIP distribuibles.

## Documentos y reproducibilidad

[Manual](estudio-2026/MANUAL-DE-PREPARACION.md) · [Plan](estudio-2026/PLAN-DE-ESTUDIO.md) · [Etapas](estudio-2026/GUIA-CONCURSO-2026.md) · [Biblioteca](estudio-2026/BIBLIOTECA-Y-TEMARIO.md) · [Comparación](estudio-2026/ACTUALIZACION-2026.md) · [Revisión](estudio-2026/REVISION-CONTENIDO.md) · [Ejercicios imprimibles](CUADERNO-DE-EJERCICIOS.html).

Para regenerar y validar todos los datos en un solo paso después de editar guías o bancos en `contenido/`:

```bash
python herramientas/construir.py
node herramientas/verificar_simulador.cjs
```

Para generar el paquete ZIP completo: `python herramientas/empaquetar.py` (escribe `paquetes/PREPARACION-JUDICIAL-MENDOZA-2026-TALLER.zip`).
