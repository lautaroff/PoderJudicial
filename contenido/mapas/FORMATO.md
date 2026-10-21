# Datos de los mapas ampliados

Contrato de integración, 21/10/2026. Cada autor escribe solo su JSON (`m1.json`, `m2.json`, `m3-m5.json`) y un breve cierre `REVISION-*.md`. El integrador conserva las tarjetas, contrastes, casos y sus IDs actuales. Los mapas con un ID existente sustituyen únicamente ese mapa.

```json
{
  "version": "2026-10-21",
  "maps": [{
    "id": "m1-estructura-judicial",
    "module": 1,
    "title": "Dónde está cada órgano",
    "root": "Organización judicial",
    "rootSources": [{"module": 1, "page": 26}],
    "lead": "Qué representa esta vista y cómo leer sus relaciones.",
    "kind": "hierarchy",
    "area": "Organización judicial",
    "priority": 1,
    "groups": [{
      "id": "jurisdiccion",
      "title": "Órganos jurisdiccionales",
      "relation": "es ejercido por",
      "nodes": [{
        "id": "scjm",
        "label": "Suprema Corte",
        "detail": "Explicación precisa y breve, con condiciones esenciales.",
        "sources": [{"module": 1, "page": 26}],
        "children": [{
          "id": "pleno",
          "label": "Pleno",
          "relation": "funciona en",
          "detail": "Detalle de organización, sin inventar subordinación.",
          "sources": [{"file": "biblioteca/2026/referencias/Ley-9423.pdf", "label": "Ley 9423 · art. 2", "page": 1}]
        }]
      }]
    }],
    "edges": [{"from": "scjm", "to": "pleno", "label": "funciona en", "type": "structure"}],
    "related": ["corte"],
    "hint": "Ayuda de memoria propia que no cambie la regla.",
    "exercise": {"prompt": "Una actividad para recuperar o aplicar relaciones.", "answer": "Respuesta explicada con criterio y límites."},
    "cautions": ["Un límite necesario para interpretar este dibujo."]
  }],
  "coverage": [{"proposal": "M1-A", "mapIds": ["m1-estructura-judicial"], "note": "Vista general y detalles conectados."}]
}
```

`kind`: `concept`, `hierarchy`, `sequence`, `matrix`, `cycle` o `compare`. Una clasificación no implica mando. `children` permite niveles reales; cada hijo conserva fuentes propias. `edges` es opcional: conectar IDs del mismo mapa con una relación explícita, sobre todo en procesos, decisiones y ciclos. No duplicar todas las conexiones padre/hijo en `edges`: el árbol ya las muestra. Tipos de arista: `structure`, `sequence`, `decision`, `feedback`, `relation`.

Fuentes: `{module, page}` para los cinco PDF; `{file, label, page}` para PDF de referencia. Para HTML local usar `{file, label, section}` sin página inventada; excepcionalmente `{url, label, section}` para una fuente oficial en línea. Cada nodo debe tener al menos una fuente primaria. No dejar `TODO`, números sin cotejar ni condiciones abiertas: cotejar el original, o limitar la afirmación a lo que sí se comprobó y dar acceso al artículo completo.

Escribir español legible; no pegar palabras/números. Máximo aconsejado de 4–6 grupos por vista y 3 niveles de detalle, salvo recorridos que necesiten una agrupación mayor. Los detalles se pueden desplegar; no necesitan repetir todo el texto del PDF. Las prácticas y mnemotecnias son originales.

IDs compartidos reservados: `m1-normas`, `m1-estructura-judicial`, `m1-corte-organizacion`, `m1-territorio`; M3 enlaza la escala de M1. Barreras de M3 se profundizan en `accesibilidad`, con sus taxonomías separadas. El integrador comprobará fuentes, aristas, IDs, enlaces entre mapas y modos de práctica.
