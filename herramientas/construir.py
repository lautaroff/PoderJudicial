# -*- coding: utf-8 -*-
"""Ejecuta en orden todo el pipeline de construcción y validación de datos."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[0]

STEPS = [
    [sys.executable, str(HERE / "integrar_documentos_2026.py")],
    [sys.executable, str(HERE / "integrar_bancos_2026.py")],
    [sys.executable, str(HERE / "generar_fuentes_2026.py")],
    [sys.executable, str(HERE / "preparar_mapas.py")],
    [sys.executable, str(HERE / "preparar_material.py")],
    [sys.executable, str(HERE / "preparar_taller.py")],
    [sys.executable, str(HERE / "verificar_enlaces_2026.py")],
    [sys.executable, str(HERE / "calidad" / "sesgo_opciones.py"), "--estricto"],
    ["node", str(HERE / "verificar_simulador.cjs")],
    [sys.executable, str(HERE / "verificar_navegador_2026.py")],
]


def main() -> None:
    for cmd in STEPS:
        label = Path(cmd[1]).name
        print(f"==> Ejecutando {label}...")
        subprocess.run(cmd, cwd=ROOT, check=True)
    print("Pipeline de datos completado con éxito.")


if __name__ == "__main__":
    main()
