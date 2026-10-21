"""Integra los mapas revisados y valida fuentes, niveles y conexiones del atlas."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit
import argparse
import hashlib
import json
import re
import fitz

ROOT = Path(__file__).resolve().parents[1]
MAPAS_DIR = ROOT / 'contenido' / 'mapas'
INTEGRADO = ROOT / 'contenido' / 'integrado'
VALIDACIONES = ROOT / 'validaciones'
PARTS = ['m1.json', 'm2.json', 'm3-m5.json']
KINDS = {'concept', 'hierarchy', 'sequence', 'matrix', 'cycle', 'compare'}


def nodes_of(m):
    def walk(nodes):
        for node in nodes:
            yield node
            yield from walk(node.get('children', []))
    for group in m['groups']:
        yield from walk(group['nodes'])


def integrate(draft=False):
    mem_path = INTEGRADO / 'memoria-datos.json'
    data = json.loads(mem_path.read_text(encoding='utf-8'))
    preserved = {k: data[k] for k in ['cards', 'pairs', 'cases', 'modules']}
    modules = {m['id']: m for m in data['modules']}
    merged = {m['id']: m for m in data['maps']}
    authored = []
    coverage = []
    for name in PARTS:
        path = MAPAS_DIR / name
        assert path.is_file(), f'Falta {path}'
        part = json.loads(path.read_text(encoding='utf-8'))
        ids = [m['id'] for m in part['maps']]
        assert len(ids) == len(set(ids)), (name, 'mapas duplicados')
        for m in part['maps']:
            assert m['id'] not in authored, ('mapa entre dos autores', m['id'])
            authored.append(m['id'])
            merged[m['id']] = m
        coverage.extend(part.get('coverage', []))
    ordered = {id: i for i, id in enumerate(authored)}
    maps = sorted(merged.values(), key=lambda m: (m['module'], ordered.get(m['id'], 999)))
    all_ids = set(merged)
    errors = []
    pending = []
    pdfs = {}
    sources_count = 0
    total_nodes = 0
    total_edges = 0

    def source(items, label):
        nonlocal sources_count
        assert isinstance(items, list) and items, ('Sin fuentes', label)
        for s in items:
            sources_count += 1
            file = s.get('file') or s.get('url') or modules.get(s.get('module'), {}).get('file')
            assert file, (label, 'fuente sin destino')
            if urlsplit(file).scheme:
                assert file.startswith('https://'), (label, file)
                assert s.get('label') or s.get('module'), (label, 'sin etiqueta')
                continue
            path = (ROOT / file).resolve()
            assert path.is_relative_to(ROOT), (label, 'fuera del proyecto', file)
            assert path.is_file(), (label, 'fuente ausente', file)
            if path.suffix.lower() == '.pdf':
                if file not in pdfs:
                    with fitz.open(path) as doc:
                        pdfs[file] = len(doc)
                assert type(s.get('page')) is int and 1 <= s['page'] <= pdfs[file], (label, s)
            else:
                assert not s.get('page'), (label, 'HTML con página inventada', s)
                assert s.get('section') or s.get('label'), (label, 'sin apartado', s)

    for m in maps:
        assert re.fullmatch(r'[a-z0-9-]+', m['id']), m['id']
        assert m['module'] in modules and m['kind'] in KINDS, m['id']
        for key in ['title', 'root', 'lead', 'groups', 'hint']:
            assert m.get(key), (m['id'], key)
        if m['id'] in authored:
            assert m.get('exercise', {}).get('prompt') and m['exercise'].get('answer'), (m['id'], 'actividad')
        source(m['rootSources'], m['id'])
        ids = set()
        for group in m['groups']:
            assert group.get('title') and group.get('relation') and group.get('nodes'), (m['id'], 'rama vacía')
        for n in nodes_of(m):
            assert re.fullmatch(r'[a-zA-Z0-9-]+', n['id']), (m['id'], n['id'])
            assert n['id'] not in ids, (m['id'], 'ID de nodo repetido', n['id'])
            ids.add(n['id'])
            assert n.get('label') and n.get('detail'), (m['id'], n['id'])
            source(n['sources'], m['id'] + '/' + n['id'])
            total_nodes += 1
        for edge in m.get('edges', []):
            assert edge['from'] in ids and edge['to'] in ids and edge.get('label'), (m['id'], edge)
            assert edge.get('type', 'relation') in {'structure', 'sequence', 'decision', 'feedback', 'relation'}, (m['id'], edge)
            total_edges += 1
        for related in m.get('related', []):
            if related not in all_ids:
                (pending if draft else errors).append([m['id'], 'mapa relacionado ausente', related])
        assert '\ufffd' not in json.dumps(m, ensure_ascii=False), (m['id'], 'carácter dañado')
    if not draft:
        for id in ['m1-estructura-judicial', 'm1-corte-organizacion', 'm1-territorio', 'penal', 'm2-juvenil', 'm2-sistemas', 'm5-atencion', 'm5-comunicacion']:
            assert id in all_ids, ('entrega incompleta', id)
        proposals = {c['proposal'] for c in coverage}
        assert all(f'V{i:02}' in proposals for i in range(1, 21)), ('cobertura M2 incompleta', proposals)
        letters = {c.rsplit('-', 1)[-1] for c in proposals}
        assert all(k in letters for k in 'ABCDEFGHIJ'), ('cobertura M3–5 incompleta', proposals)
        for c in coverage:
            assert c.get('mapIds') and all(id in all_ids for id in c['mapIds']), ('propuesta sin mapa', c)
    assert not errors, errors
    data['maps'] = maps
    data['version'] = '2026-10-21'
    data['mapCoverage'] = coverage
    assert all(data[k] == v for k, v in preserved.items()), 'Se alteró contenido de tarjetas o casos'
    text = json.dumps(data, ensure_ascii=False, indent=2)
    mem_path.write_text(text + '\n', encoding='utf-8')
    (ROOT / 'memoria-datos.js').write_text('window.PJM_MEMORIA = ' + text + ';\n', encoding='utf-8')
    report = {'fecha': '2026-10-21', 'estado': 'BORRADOR' if draft else 'PASS', 'mapas': len(maps), 'mapas_por_modulo': dict(sorted(Counter(m['module'] for m in maps).items())), 'nodos_con_fuente': total_nodes, 'conexiones_explicitas': total_edges, 'referencias': sources_count, 'pdf_distintos': len(pdfs), 'tarjetas_preservadas': len(data['cards']), 'contrastes_preservados': len(data['pairs']), 'casos_preservados': len(data['cases']), 'pendientes': pending, 'errores': errors, 'partes_sha256': {name: hashlib.sha256((MAPAS_DIR / name).read_bytes()).hexdigest() for name in PARTS}}
    VALIDACIONES.mkdir(parents=True, exist_ok=True)
    (VALIDACIONES / 'validacion-mapas-2026.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    markup = (ROOT / 'memoria.html').read_text(encoding='utf-8')
    for resource in ['memoria.css', 'mapas.css', 'memoria-datos.js', 'mapas.js', 'memoria.js']:
        digest = hashlib.sha256((ROOT / resource).read_bytes()).hexdigest()[:12]
        markup = re.sub('"' + re.escape(resource) + r'(?:\?v=[^"\s]+)?"', '"' + resource + '?v=' + digest + '"', markup)
    (ROOT / 'memoria.html').write_text(markup, encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true', help='Integrar avances sin certificar cobertura completa')
    args = parser.parse_args()
    integrate(draft=args.draft)
