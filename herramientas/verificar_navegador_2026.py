# -*- coding: utf-8 -*-
"""Verificación E2E en navegador Chromium real (Playwright) de index.html, memoria.html y taller.html."""
from __future__ import annotations

import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
VALIDACIONES = ROOT / "validaciones"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass


def start_server() -> tuple[socketserver.TCPServer, int]:
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port


def main() -> None:
    httpd, port = start_server()
    base = f"http://127.0.0.1:{port}"
    checks = []
    errors = []

    def record(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "ok": bool(ok), "detail": detail})
        if not ok:
            raise AssertionError(f"Fallo en {name}: {detail}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()
            page.on("pageerror", lambda err: errors.append(f"pageerror: {err}"))
            page.on("console", lambda msg: errors.append(f"console.{msg.type}: {msg.text}") if msg.type == "error" else None)

            # 1. INDEX.HTML: Carga inicial, cobertura, semáforos y puentes
            page.goto(f"{base}/index.html", wait_until="networkidle")
            record("index_sin_errores_iniciales", len(errors) == 0, str(errors))
            cov_rows = page.locator("#coverage .coverage-row").count()
            record("index_27_apartados_cobertura", cov_rows == 27, f"filas={cov_rows}")
            pills = page.locator("#coverage .mastery-pill").count()
            record("index_27_semaforos_dominio", pills == 27, f"pills={pills}")

            # 2. INDEX.HTML: Entrenador de números, plazos y competencias desde puente de apartado
            page.locator("#coverage details").first.locator("summary").click()
            page.locator('[data-practice-num="1.1"]').click()
            q_count = page.locator("#exam .question").count()
            record("index_entrenador_numeros_inicia", q_count > 0, f"preguntas={q_count}")
            # Responder el primer ítem (sea cloze o múltiple opción) y entregar
            first_q = page.locator("#exam .question").first
            if first_q.locator(".cloze-input").count() > 0:
                first_q.locator(".cloze-input").fill("999999")
            else:
                first_q.locator('input[type="radio"]').first.check()
            page.locator("#finish").click()
            if page.locator('dialog [data-answer="yes"]').count() > 0:
                page.locator('dialog [data-answer="yes"]').click()
            record("index_entrenador_numeros_corrige", page.locator("#exam .result").count() == 1)
            tag_btns = page.locator("[data-err-tag]").count()
            record("index_etiquetas_causa_error_visibles", tag_btns >= 4, f"botones={tag_btns}")
            page.locator("[data-err-tag]").first.click()
            record("index_etiqueta_error_activa", "active" in (page.locator("[data-err-tag]").first.get_attribute("class") or ""))

            # 3. INDEX.HTML: Simulacro proporcional, OMR, descarte (✕), bandera (⚑) y persistencia al recargar
            page.locator("#mode").select_option("especificos")
            page.locator("#examDistribution").select_option("proportional")
            page.locator("#start").click()
            record("index_simulacro_50_preguntas", page.locator("#exam .question").count() == 50)
            record("index_omr_50_burbujas", page.locator("#omrGrid .omr-bubble").count() == 50)
            record("index_ritmo_visible", "Ritmo:" in page.locator("#paceInfo").inner_text())

            # Tachado de distractor y bandera de revisión
            page.locator("[data-discard]").first.click()
            record("index_descarte_distractor", "discarded" in (page.locator("#q-card-0 .option").first.get_attribute("class") or ""))
            page.locator('[data-flag-q="0"]').click()
            record("index_bandera_omr_sincronizada", "flagged" in (page.locator('#omrGrid [data-jump-q="0"]').get_attribute("class") or ""))
            page.locator('#q-card-0 input[type="radio"]').first.check()
            record("index_omr_respondida_sincronizada", "done" in (page.locator('#omrGrid [data-jump-q="0"]').get_attribute("class") or ""))

            # Recargar la página y comprobar recuperación automática de práctica en curso
            page.reload(wait_until="networkidle")
            record("index_banner_recuperar_practica", not page.locator("#resumeBanner").evaluate("el => el.classList.contains('hide')"))
            record("index_practica_recuperada_50", page.locator("#exam .question").count() == 50)
            record("index_respuesta_recuperada", "done" in (page.locator('#omrGrid [data-jump-q="0"]').get_attribute("class") or ""))
            record("index_bandera_recuperada", "flagged" in (page.locator('#omrGrid [data-jump-q="0"]').get_attribute("class") or ""))
            record("index_descarte_recuperado", "discarded" in (page.locator("#q-card-0 .option").first.get_attribute("class") or ""))

            # 4. INDEX.HTML: Comprensión lectora en pantalla dividida y parámetro ?doc=
            page.locator("#mode").select_option("lectura")
            page.locator("#start").click()
            if page.locator('dialog [data-answer="yes"]').count() > 0:
                page.locator('dialog [data-answer="yes"]').click()
            record("index_lectura_split_screen", page.locator("#exam .reading-split").count() == 1)

            page.goto(f"{base}/index.html?doc=estudio-2026/GUIA-MAPAS-2026.md", wait_until="networkidle")
            record("index_param_doc_abre_guia", len(page.locator("#catalogo").inner_text()) > 200)

            # Vista móvil 390px sin desborde horizontal
            page.set_viewport_size({"width": 390, "height": 844})
            overflow_index = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
            record("index_mobile_390_sin_desborde", not overflow_index)
            page.set_viewport_size({"width": 1440, "height": 900})

            # 5. MEMORIA.HTML: Mapas, puentes, reconstrucción con (ya usado), zoom persistente, tarjetas y casos
            linked_maps = page.evaluate("""
                [...document.querySelectorAll('#coverage a[href^="memoria.html#map="]')]
                .map(a => a.getAttribute('href').split('#map=')[1])
            """)
            page.goto(f"{base}/memoria.html", wait_until="networkidle")
            all_map_ids = set(page.evaluate("window.PJM_MEMORIA.maps.map(m => m.id)"))
            missing_maps = [m for m in linked_maps if m not in all_map_ids]
            record("puentes_mapas_existen_en_atlas", len(linked_maps) == 27 and len(missing_maps) == 0, f"faltan={missing_maps}")
            flow_map_id = page.evaluate("window.PJM_MEMORIA.maps.find(m => m.kind === 'sequence' || m.kind === 'cycle').id")
            page.goto(f"{base}/memoria.html#map={flow_map_id}", wait_until="networkidle")
            record("memoria_puentes_visibles", page.locator(".map-bridges a").count() == 3)
            page.locator('[data-diagram-zoom="in"]').click()
            scale_before = page.locator(".diagram-scale").inner_text()
            page.locator('[data-map-mode="recall"]').click()
            scale_after = page.locator(".diagram-scale").inner_text()
            record("memoria_zoom_persiste_cambio_modo", scale_before == scale_after and scale_before != "100 %", f"{scale_before} -> {scale_after}")

            page.locator('[data-map-mode="build"]').click()
            selects = page.locator("select[data-answer]")
            first_val = selects.first.locator("option").nth(1).get_attribute("value")
            selects.first.select_option(first_val)
            second_opt_text = selects.nth(1).locator(f'option[value="{first_val}"]').inner_text()
            record("memoria_reconstruir_marca_ya_usado", "(ya usado)" in second_opt_text, second_opt_text)
            # Recargar sin hash para comprobar que persiste el modo build y la opción elegida
            page.goto(f"{base}/memoria.html", wait_until="networkidle")
            record("memoria_reconstruir_persiste_recarga", page.locator("select[data-answer]").first.input_value() == first_val)

            page.locator('[data-view="tarjetas"]').click()
            page.locator("#reveal-card").click()
            page.reload(wait_until="networkidle")
            record("memoria_tarjeta_revelada_persiste_recarga", page.locator('[data-rate="review"]').count() == 1)
            page.locator('[data-rate="review"]').click()
            due_hour = page.evaluate("new Date(Object.values(JSON.parse(localStorage.getItem('pjm-memoria-2026')).cards)[0].due).getHours()")
            record("memoria_tarjeta_due_medianoche", due_hour == 0, f"hora={due_hour}")

            page.locator('[data-view="casos"]').click()
            first_case = page.locator("[data-case]").first
            first_case.locator("[data-choice]").first.click()
            record("memoria_caso_evalua", first_case.get_attribute("data-answered") == "true")
            page.reload(wait_until="networkidle")
            record("memoria_caso_persiste_recarga", page.locator("[data-case]").first.get_attribute("data-answered") == "true")

            page.set_viewport_size({"width": 390, "height": 844})
            overflow_memoria = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
            record("memoria_mobile_390_sin_desborde", not overflow_memoria)
            page.set_viewport_size({"width": 1440, "height": 900})

            # 6. TALLER.HTML: Parámetros URL, foco en secuencias, píldoras de confianza, lectura split, notas y TTS en video
            page.goto(f"{base}/taller.html?module=2&topic=2.1", wait_until="networkidle")
            record("taller_param_modulo_aplicado", page.locator("#module").input_value() == "2")
            record("taller_param_apartado_aplicado", page.locator("#topic").input_value() == "2.1")

            page.locator('[data-view="sequences"]').click()
            page.locator('[data-index="0"][data-move="down"]').click()
            focused_idx = page.evaluate("document.activeElement?.getAttribute('data-index')")
            record("taller_secuencias_preserva_foco", focused_idx == "1", f"focused={focused_idx}")
            page.locator("#answer-main").fill("Borrador persistente de secuencia.")
            page.goto(f"{base}/taller.html", wait_until="networkidle")
            record("taller_vista_y_borrador_persisten_recarga", page.locator("#answer-main").input_value() == "Borrador persistente de secuencia.")

            page.locator('[data-view="diagnostics"]').click()
            page.locator('[data-diagnostic^="read:"]').first.click()
            record("taller_lectura_split_screen", page.locator("#diagnostic-area .reading-split").count() == 1)
            first_pill = page.locator(".conf-pill").first
            first_pill.click()
            qid = first_pill.get_attribute("data-conf-q")
            sel_val = page.locator(f'select[data-confidence="{qid}"]').input_value()
            record("taller_pildora_confianza_sincroniza", sel_val == "high", f"sel={sel_val}")

            # Videos: bloc de notas y paso al cuestionario conservando notas
            page.locator('[data-view="videos"]').click()
            if page.locator("#confirmDialog[open] #confirmYes").count() > 0:
                page.locator("#confirmDialog[open] #confirmYes").click()
            page.locator('[data-video="V1"][data-mode="study"]').click()
            if page.locator("#confirmDialog[open] #confirmYes").count() > 0:
                page.locator("#confirmDialog[open] #confirmYes").click()
            record("taller_video_boton_tts_visible", page.locator("#toggle-narration").count() == 1)
            page.locator("#video-notes-input").fill("Apunte clave de prueba: plazo 5 días hábiles.")
            page.locator("#video-questionnaire").click()
            record("taller_video_notas_visibles_en_cuestionario", "plazo 5 días hábiles" in page.locator(".video-notes-review").inner_text())

            page.set_viewport_size({"width": 390, "height": 844})
            overflow_taller = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
            record("taller_mobile_390_sin_desborde", not overflow_taller)

            record("navegador_sin_errores_consola", len(errors) == 0, str(errors))
            browser.close()
    finally:
        httpd.shutdown()

    out = {
        "fecha": "2026-10-21",
        "estado": "PASS",
        "comprobaciones_totales": len(checks),
        "errores_consola": errors,
        "detalle": checks,
    }
    VALIDACIONES.mkdir(parents=True, exist_ok=True)
    (VALIDACIONES / "validacion-e2e-2026.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"PASS E2E Chromium: {len(checks)} comprobaciones reales en navegador (0 errores JS/consola).")


if __name__ == "__main__":
    main()
