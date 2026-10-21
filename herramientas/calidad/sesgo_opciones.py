"""Detecta pistas involuntarias en preguntas de opción múltiple.

Mide, por banco, cuántas veces la opción correcta es estrictamente la más larga
(o la más corta). Un estudiante que elige «la más larga» no debería superar
claramente el azar. El orden de las opciones se mezcla en la aplicación, así
que la posición de la clave no se evalúa aquí.

Uso:  python herramientas/calidad/sesgo_opciones.py [--json] [--estricto]
"""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
CONTENIDO = ROOT / 'contenido'

# Margen tolerado sobre el azar (1/n). Bancos chicos toleran algo más de ruido.
MARGEN = 0.10
MARGEN_CHICO = 0.15


def _norm(q):
    """Devuelve (id, opciones, índice correcto) para ambos formatos de datos."""
    if 'opciones' in q:
        return q['id'], q['opciones'], q['correcta']
    return q['id'], q['options'], q['correct']


def bancos():
    for name in ['m1-m3', 'm2', 'm4-m5', 'anexos', 'institucional', 'lectura']:
        path = CONTENIDO / 'bancos' / f'{name}.json'
        yield f'bancos/{name}', json.loads(path.read_text(encoding='utf-8'))
    diag = json.loads((CONTENIDO / 'taller' / 'diagnosticos.json').read_text(encoding='utf-8'))
    for form in diag['forms']:
        yield f"taller/diagnostico-{form['id']}", form['questions']
    yield 'taller/diagnostico-lectura', [q for t in diag['reading'] for q in t['questions']]
    for video in json.loads((CONTENIDO / 'taller' / 'videos.json').read_text(encoding='utf-8')):
        yield f"taller/video-{video['id']}", video['questions']


def medir(items):
    longest = shortest = 0
    flagged = []
    n_options = 0
    for q in items:
        qid, options, correct = _norm(q)
        n_options = max(n_options, len(options))
        lengths = [len(o.strip()) for o in options]
        others = [l for i, l in enumerate(lengths) if i != correct]
        if lengths[correct] > max(others):
            longest += 1
            ratio = lengths[correct] / max(1, max(others))
            if ratio >= 1.25:
                flagged.append({'id': qid, 'ratio': round(ratio, 2)})
        if lengths[correct] < min(others):
            shortest += 1
    total = len(items)
    chance = 1 / n_options if n_options else 0
    limit = chance + (MARGEN if total >= 40 else MARGEN_CHICO)
    return {
        'total': total,
        'opciones': n_options,
        'azar': round(chance, 3),
        'limite': round(limit, 3),
        'correcta_mas_larga': longest,
        'tasa_mas_larga': round(longest / total, 3) if total else 0,
        'correcta_mas_corta': shortest,
        'tasa_mas_corta': round(shortest / total, 3) if total else 0,
        'ok': total == 0 or (longest / total <= limit and shortest / total <= limit),
        'marcadas': sorted(flagged, key=lambda x: -x['ratio']),
    }


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true', help='Salida completa en JSON')
    parser.add_argument('--estricto', action='store_true', help='Termina con error si algún banco supera el límite')
    args = parser.parse_args()
    report = {name: medir(items) for name, items in bancos()}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for name, r in report.items():
            estado = 'OK ' if r['ok'] else 'ALTO'
            print(f"{estado} {name:28} n={r['total']:3}  más larga {r['tasa_mas_larga']:.0%}  "
                  f"más corta {r['tasa_mas_corta']:.0%}  (límite {r['limite']:.0%}; marcadas ≥1.25×: {len(r['marcadas'])})")
    if args.estricto and not all(r['ok'] for r in report.values()):
        sys.exit(1)
    return report


if __name__ == '__main__':
    main()
