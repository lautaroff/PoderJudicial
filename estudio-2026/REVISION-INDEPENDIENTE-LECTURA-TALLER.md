# Revisión independiente de las lecturas del taller

Revisión del 12 de octubre de 2026. Alcance: lectura íntegra de los dos pasajes originales LA y LB y contraste individual de sus 20 preguntas, las tres opciones, la clave, la explicación y la evidencia en `taller-datos/diagnosticos.json`. No se modificó ese archivo ni otros datos del taller.

**Resultado:** no se detectaron claves incorrectas, dos respuestas defendibles en una misma pregunta ni inferencias que requieran conocimientos ajenos al pasaje. Cada respuesta seleccionada tiene respaldo en el texto y las otras dos opciones resultan incompatibles con él o exceden lo que permite concluir.

## Pasajes y tesis

- **LA — «Conservar una obra no es inmovilizar su lectura»:** ocho párrafos, 699 palabras. Su tesis distingue estabilidad material de la obra y revisión de su explicación: la conservación y una interpretación accesible, fundamentada y revisable son compatibles. Los ejemplos del tejido, la inscripción, el cartel antiguo, las capas de información y la reproducción desarrollan esa tesis; no autorizan a presentar hipótesis como hechos ni a equiparar todas las afirmaciones históricas.
- **LB — «Un mapa que elige»:** ocho párrafos, 698 palabras. Expone que todo mapa selecciona según su propósito y que su uso exige comprender escala, orientación, signos, proyección, fecha y límites. Su conclusión propone usar críticamente una representación adecuada a la pregunta, sin rechazar todos los mapas ni suponer que una representación sirve para cualquier decisión.

La numeración siguiente cuenta los párrafos separados por líneas en blanco dentro del campo `text`, desde 1. A, B y C identifican la primera, segunda y tercera opción; corresponden a índices JSON 0, 1 y 2.

## Contraste de las 20 preguntas

| ID | Operación y respaldo preciso | Clave validada |
|---|---|---|
| DLA-01 | Tesis central: distinción entre objeto y explicación; párrafos 1 y 8. | B |
| DLA-02 | Efecto de añadir usos documentados: comprensión mejor fundada, sin alterar fibras ni garantizar unanimidad; párrafo 2. | A |
| DLA-03 | Tratamiento de una hipótesis ceremonial: identificarla y explicar sus razones; párrafo 3. | C |
| DLA-04 | Valor concesivo de «aunque»: reconoce el valor histórico de explicaciones anteriores sin convertirlas en la única voz actual; párrafo 4. | A |
| DLA-05 | Conservación de un cartel antiguo: archivo o reproducción con fecha y contexto, junto a la explicación actual; párrafo 4. | B |
| DLA-06 | Información breve y profundización opcional: atender tiempos e intereses distintos, sin clasificar capacidades; párrafo 5. | C |
| DLA-07 | Utilidad condicionada de una reproducción: evaluar qué ayuda ofrece y qué confusiones puede causar; párrafo 6. | A |
| DLA-08 | Pluralidad interpretativa con fundamento: detalles visibles no convierten cualquier impresión en un hecho histórico; párrafo 7. | B |
| DLA-09 | Referente de «esa distinción»: conocimiento fundado frente a lo discutido o propuesto; final del párrafo 2 y comienzo del 3. | C |
| DLA-10 | Conclusión incompatible: ocultar razones de cambios para aparentar una explicación incuestionable contradice la trazabilidad defendida; párrafo 8. | B |
| DLB-01 | Idea central: la selección permite representar y exige comprender las condiciones de uso; párrafos 1 y 8. | C |
| DLB-02 | Cálculo con la escala expresamente explicada: 1 cm representa 100 m; 3 cm representan 300 m; párrafo 2. | B |
| DLB-03 | Conclusión no autorizada: igual distancia representada no garantiza igual tiempo o esfuerzo; párrafo 2. | A |
| DLB-04 | Uso de un plano girado: puede ayudar a seguir un recorrido si se declara la orientación; párrafo 3. | B |
| DLB-05 | Interpretación del color azul: consultar la leyenda de ese mapa, porque su significado no es universal; párrafo 4. | C |
| DLB-06 | Evaluación según propósito: omitir atajos no prueba un fallo en un mapa que no promete esa función; párrafo 5. | A |
| DLB-07 | Proyección: conocer qué conserva el método antes de comparar apariencias con propiedades reales; párrafo 6. | C |
| DLB-08 | Puente cerrado después de la elaboración: un cambio posterior no implica que el mapa original lo haya inventado; párrafo 7. | B |
| DLB-09 | Inferencia inadecuada: ausencia de datos sobre una zona no demuestra inexistencia de lo representable; párrafo 7. | C |
| DLB-10 | Conclusión: relacionar propósito, escala, orientación, signos, método y fecha con la pregunta del usuario; párrafo 8. | A |

Se comprobó especialmente la inversión de selección en DLA-10, DLB-03 y DLB-09: sus enunciados piden la conclusión incompatible, no autorizada o inadecuada. Las claves cumplen esa consigna. En DLB-02 el cálculo se deriva de una relación proporcionada por el propio texto; no exige recordar una fórmula externa. Las explicaciones y las referencias de evidencia son coherentes con las respuestas seleccionadas.

## Comprobaciones y límites

- Veinte IDs únicos, diez preguntas por pasaje, tres opciones distintas por pregunta y veinte claves dentro del intervalo válido 0–2. Todas incluyen explicación y evidencia; las referencias a párrafos están dentro de los ocho existentes.
- Distribución de posiciones: LA tiene A=3, B=4, C=3; LB tiene A=3, B=3, C=4. No se detectó una secuencia periódica simple de claves.
- Son textos y ejercicios originales de práctica. Su fuente de evidencia es el propio pasaje, no un PDF oficial ni un video institucional real.
- La extensión semejante de ambos textos no demuestra equivalencia de dificultad ni validación psicométrica. Esta revisión verifica contenido y consistencia; no prueba la interfaz, el cronómetro ni el rendimiento de aspirantes.

Versión contrastada: SHA-256 de `taller-datos/diagnosticos.json` = `94460ced0abaa0e538cc5cfcfb9dba577d9644af218bd119489298249eba5794`. No hay correcciones de contenido pendientes detectadas en este alcance.
