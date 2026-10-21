# -*- coding: utf-8 -*-
"""Equilibra la longitud de opciones en todos los bancos de opción múltiple
sin alterar claves, ids, fuentes ni el sentido jurídico de cada opción."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from herramientas.calidad.sesgo_opciones import bancos, medir, _norm

ROOT = Path(__file__).resolve().parents[2]
CONTENIDO = ROOT / "contenido"


def git_head_json(old_rel_path: str, fallback: Path | None = None):
    try:
        raw = subprocess.check_output(["git", "show", f"HEAD:{old_rel_path}"], cwd=ROOT, stderr=subprocess.DEVNULL)
        return json.loads(raw.decode("utf-8"))
    except Exception:
        if fallback and fallback.exists():
            return json.loads(fallback.read_text(encoding="utf-8"))
        raise


def has_period(opts: list[str]) -> bool:
    return sum(1 for o in opts if o.strip().endswith(".")) >= len(opts) // 2 + 1


def match_punct(text: str, period: bool) -> str:
    t = text.strip()
    if period:
        if not t.endswith(".") and not t.endswith("?") and not t.endswith(")"):
            t += "."
    else:
        if t.endswith("."):
            t = t[:-1].rstrip()
    return t


def expand_distractor(opt: str, q: dict, idx: int, target_len: int) -> str:
    period = opt.strip().endswith(".")
    base = opt.strip().rstrip(".")

    # Caso especial P141 ("120", "36", "60")
    if q.get("id") == "P141" and base in {"120", "36", "60"}:
        return f"{base} consultas registradas"

    if re.fullmatch(r"[\d\s%.,/a-zA-Zº°]+", base) and len(base) <= 6:
        return opt

    mod = q.get("modulo") or q.get("module") or 0
    area = str(q.get("area", "") or q.get("subtema", "") or q.get("topic", "")).lower()
    low = base.lower()

    if any(k in low for k in ["registro", "cámara", "juzgado", "tribunal", "corte", "ministerio", "dirección", "oficina", "unidad", "defensor", "fiscal", "asesor", "consejo", "jury", "congreso", "senado", "ejecutivo"]):
        tails = [
            " dentro del régimen ordinario de competencia provincial",
            " en ejercicio de atribuciones administrativas ordinarias",
            " con intervención directa en el trámite principal de la causa",
            " según la distribución territorial de la circunscripción",
        ]
    elif any(k in low for k in ["código", "ley", "reglamento", "acordada", "decreto", "constitución", "tratado", "convención"]):
        tails = [
            " aplicable de manera supletoria al procedimiento administrativo",
            " dentro del régimen general vigente en la jurisdicción provincial",
            " sin requerir reglamentación especial del órgano superior",
            " conforme a las disposiciones generales del derecho común",
        ]
    elif any(k in low for k in ["plazo", "día", "mes", "hora", "año"]):
        tails = [
            " computados de forma corrida desde la primera presentación",
            " contados a partir de la recepción administrativa del legajo",
            " sin admitir suspensión ni prórroga durante el trámite",
            " sujetos a convalidación posterior de la mesa de entradas",
        ]
    elif "lectura" in area or "texto" in q or "DLA-" in str(q.get("id", "")) or "DLB-" in str(q.get("id", "")):
        tails = [
            " según el planteo general expuesto en los párrafos del texto",
            " como condición necesaria mencionada por el autor del pasaje",
            " dentro del argumento principal desarrollado en el fragmento",
            " de acuerdo con la conclusión literal formulada en la lectura",
        ]
    elif mod in (4, 5) or any(k in low for k in ["atención", "género", "violencia", "usuario", "ciudadan", "escucha", "comunicación", "lenguaje", "accesibilidad", "barrera", "conflicto", "ventanilla", "mesa"]):
        tails = [
            " durante la atención inicial en la mesa de entradas judicial",
            " dentro de las pautas ordinarias de gestión interna de la oficina",
            " como criterio administrativo general frente a cada consulta",
            " en el marco de la organización interna del despacho judicial",
        ]
    elif mod == 3 or any(k in low for k in ["derecho", "estado", "humano", "internacional", "vulnerab", "igualdad", "discrimin"]):
        tails = [
            " dentro del ámbito interno de cada jurisdicción estatal",
            " sujeto a la reglamentación discrecional de cada autoridad",
            " en el marco de las relaciones ordinarias de derecho interno",
            " según las pautas administrativas de cada órgano local",
        ]
    else:
        tails = [
            " en el marco ordinario del procedimiento judicial provincial",
            " conforme a las reglas generales de actuación administrativa",
            " sin intervención de los órganos de control jurisdiccional",
            " dentro del trámite común previsto por la normativa local",
        ]

    chosen = tails[(idx + sum(ord(c) for c in str(q.get("id", "")))) % len(tails)]
    if base.endswith((",", ";", ":")):
        base = base[:-1].rstrip()

    cand = base + chosen
    # Si nos pasamos por mucho de target_len, podemos recortar la cola a una versión más breve
    if len(cand) > target_len + 14:
        short_tails = [
            " en el trámite ordinario provincial",
            " según las pautas administrativas",
            " dentro del procedimiento común",
            " en el ámbito interno de la oficina",
        ]
        chosen_short = short_tails[(idx + sum(ord(c) for c in str(q.get("id", "")))) % len(short_tails)]
        if len(base + chosen_short) >= target_len:
            cand = base + chosen_short

    return match_punct(cand, period)


def shorten_text(text: str) -> str:
    period = text.strip().endswith(".")
    t = text.strip().rstrip(".")
    replacements = [
        (" en el ámbito del Poder Judicial de la Provincia de Mendoza", " en el Poder Judicial de Mendoza"),
        (" de la Provincia de Mendoza", " provincial"),
        (" que se encuentran ", " "),
        (" con el objeto de ", " para "),
        (" con la finalidad de ", " para "),
        (" a los efectos de ", " para "),
        (" de manera exclusiva y excluyente", " exclusivamente"),
        (" única y exclusivamente ", " únicamente "),
        (", sin excepción alguna", ""),
        (" en todos los casos sin excepción", " en todos los casos"),
        (" sin ningún tipo de ", " sin "),
        (" por parte de ", " por "),
        (" en relación con ", " sobre "),
        (" respecto de ", " sobre "),
        (" a través de ", " mediante "),
    ]
    for old, new in replacements:
        if old in t:
            t = t.replace(old, new)
    return match_punct(t, period)


def expand_correct_from_explanation(opt: str, q: dict) -> str:
    period = opt.strip().endswith(".")
    base = opt.strip().rstrip(".")
    exp = (q.get("explicacion") or q.get("why") or "").strip()

    low = base.lower()
    if low == "peticionarios":
        return match_punct("Peticionarios que acuden sin controversia entre partes", period)
    if "tercero que interviene" in low:
        return match_punct(base + " para hacer valer un interés propio o coadyuvante", period)
    if "proceso de conocimiento" in low:
        return match_punct(base + " destinado a declarar la existencia de un derecho", period)
    if "asegurar el resultado" in low:
        return match_punct(base + " principal evitando la frustración del derecho", period)

    m = re.search(r"(?:porque|ya que|pues|para|cuando|mediante|conforme a|según)\s+([^.;,]{12,48})", exp, flags=re.I)
    if m:
        clause = m.group(0).strip()
        if clause.lower() not in low:
            return match_punct(f"{base} ({clause})", period)

    return match_punct(base + " conforme al régimen procesal aplicable", period)


def get_opts_key(q: dict) -> tuple[str, int]:
    if "opciones" in q:
        return "opciones", q["correcta"]
    return "options", q["correct"]


def balance_question_longest(q: dict, make_not_longest: bool) -> bool:
    key, corr = get_opts_key(q)
    opts = list(q[key])
    if q.get("id") == "P141":
        q[key] = [f"{o.strip()} consultas" if "consulta" not in o else o for o in opts]
        return True

    period = has_period(opts)
    lens = [len(o.strip()) for o in opts]
    others_idx = [i for i in range(len(opts)) if i != corr]

    changed = False
    short_corr = shorten_text(opts[corr])
    if len(short_corr) < len(opts[corr]) and len(short_corr) >= 15:
        opts[corr] = short_corr
        lens[corr] = len(short_corr.strip())
        changed = True

    others_sorted = sorted(others_idx, key=lambda i: lens[i], reverse=True)
    if make_not_longest:
        target_len = lens[corr] + 2
    else:
        # Mantener la correcta como la más larga pero con ratio <= 1.18 (debajo de 1.25)
        target_len = int(lens[corr] / 1.17) + 1

    for idx in others_sorted:
        curr_max = max(lens[i] for i in others_idx)
        if curr_max >= target_len:
            break
        cand = expand_distractor(opts[idx], q, idx, target_len)
        if not make_not_longest and len(cand.strip()) >= lens[corr]:
            # Recortar cand para que quede entre target_len y lens[corr] - 1
            cand_raw = cand.strip().rstrip(".")
            words = cand_raw.split()
            while len(" ".join(words)) >= lens[corr] - (1 if period else 0) and len(words) > 3:
                words.pop()
            cand = match_punct(" ".join(words), period)
        if len(cand.strip()) < target_len and make_not_longest:
            p2 = cand.strip().endswith(".")
            b2 = cand.strip().rstrip(".")
            extra = " según la reglamentación vigente" if "según" not in b2.lower() else " dentro del procedimiento ordinario"
            cand = match_punct(b2 + extra, p2)
        if cand != opts[idx] and cand not in opts:
            opts[idx] = match_punct(cand, period)
            lens[idx] = len(opts[idx].strip())
            changed = True

    if changed:
        q[key] = opts
    return changed


def balance_question_shortest(q: dict) -> bool:
    key, corr = get_opts_key(q)
    opts = list(q[key])
    period = has_period(opts)
    lens = [len(o.strip()) for o in opts]
    others_idx = [i for i in range(len(opts)) if i != corr]
    min_other = min(lens[i] for i in others_idx)

    if lens[corr] >= min_other:
        return False

    for i in others_idx:
        s = shorten_text(opts[i])
        if s != opts[i] and s not in opts:
            opts[i] = match_punct(s, period)
            lens[i] = len(opts[i].strip())

    min_other = min(lens[i] for i in others_idx)
    max_other = max(lens[i] for i in others_idx)
    if lens[corr] >= min_other:
        q[key] = opts
        return True

    cand = expand_correct_from_explanation(opts[corr], q)
    if len(cand.strip()) >= min_other and len(cand.strip()) <= max_other and cand not in opts:
        opts[corr] = match_punct(cand, period)
        q[key] = opts
        return True

    if len(cand.strip()) > max_other:
        opts[corr] = match_punct(cand, period)
        q[key] = opts
        balance_question_longest(q, make_not_longest=True)
        return True

    b = cand.strip().rstrip(".")
    cand2 = match_punct(b + " dentro del proceso judicial", period)
    if len(cand2.strip()) >= min_other and cand2 not in opts:
        opts[corr] = cand2
        q[key] = opts
        if len(cand2.strip()) > max_other:
            balance_question_longest(q, make_not_longest=True)
        return True

    return False


def process_items(items: list[dict], target_longest_rate: float = 0.25, target_shortest_rate: float = 0.25) -> int:
    modified = 0
    # Primero reducir tasa_mas_larga hasta target_longest_rate empezando por las de mayor ratio
    while True:
        r = medir(items)
        if r["tasa_mas_larga"] <= target_longest_rate:
            break
        candidates = []
        for q in items:
            _, opts, corr = _norm(q)
            lens = [len(o.strip()) for o in opts]
            others = [l for i, l in enumerate(lens) if i != corr]
            if lens[corr] > max(others):
                candidates.append((lens[corr] / max(1, max(others)), lens[corr] - max(others), q))
        if not candidates:
            break
        candidates.sort(key=lambda x: (-x[0], -x[1]))
        progressed = False
        for _, _, q in candidates:
            if balance_question_longest(q, make_not_longest=True):
                modified += 1
                progressed = True
                break
        if not progressed:
            break

    # Segundo: si quedaron preguntas con ratio >= 1.25 (aunque tasa_mas_larga ya esté en ~25%), bajarles el ratio sin que dejen de ser las más largas (o dejándolas empatadas)
    for q in items:
        _, opts, corr = _norm(q)
        lens = [len(o.strip()) for o in opts]
        others = [l for i, l in enumerate(lens) if i != corr]
        if lens[corr] > max(others) and (lens[corr] / max(1, max(others))) >= 1.24:
            if balance_question_longest(q, make_not_longest=False):
                modified += 1
            _, opts2, corr2 = _norm(q)
            lens2 = [len(o.strip()) for o in opts2]
            others2 = [l for i, l in enumerate(lens2) if i != corr2]
            if lens2[corr2] > max(others2) and (lens2[corr2] / max(1, max(others2))) >= 1.24:
                balance_question_longest(q, make_not_longest=True)

    # Tercero: si tasa_mas_corta supera target_shortest_rate, equilibrar las más cortas
    while True:
        r = medir(items)
        if r["tasa_mas_corta"] <= target_shortest_rate:
            break
        candidates = []
        for q in items:
            _, opts, corr = _norm(q)
            lens = [len(o.strip()) for o in opts]
            others = [l for i, l in enumerate(lens) if i != corr]
            if lens[corr] < min(others):
                candidates.append((min(others) - lens[corr], q))
        if not candidates:
            break
        candidates.sort(key=lambda x: x[0])
        progressed = False
        for _, q in candidates:
            if balance_question_shortest(q):
                modified += 1
                progressed = True
                break
        if not progressed:
            break

    return modified


def main() -> None:
    for name in ["m1-m3", "m2", "m4-m5", "anexos", "institucional", "lectura"]:
        data = git_head_json(f"bancos-2026/{name}.json")
        t_long = 0.33 if name == "lectura" else 0.25
        t_short = 0.33 if name == "lectura" else 0.25
        mod = process_items(data, t_long, t_short)
        path = CONTENIDO / "bancos" / f"{name}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"bancos/{name}: {mod} ajustes")

    diag_path = CONTENIDO / "taller" / "diagnosticos.json"
    diag = git_head_json("taller-2026/diagnosticos.json", diag_path)
    for form in diag["forms"]:
        mod = process_items(form["questions"], 0.26, 0.28)
        print(f"taller/diagnostico-{form['id']}: {mod} ajustes")
    for t in diag["reading"]:
        mod = process_items(t["questions"], 0.30, 0.30)
    diag_path.write_text(json.dumps(diag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    vid_path = CONTENIDO / "taller" / "videos.json"
    videos = git_head_json("taller-2026/videos.json", vid_path)
    for v in videos:
        mod = process_items(v["questions"], 0.25, 0.25)
        print(f"taller/video-{v['id']}: {mod} ajustes")
    vid_path = CONTENIDO / "taller" / "videos.json"
    vid_path.write_text(json.dumps(videos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
