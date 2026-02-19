"""IQ Opción IA 2.8 - Launcher SOLO CONSOLA.

Permite seleccionar preset de configuración:
- BALANCEADO
- AGRESIVO

Ejemplos:
  python IQ_Opcion_IA_2.8.py --perfil balanceado
  python IQ_Opcion_IA_2.8.py --perfil agresivo
"""

import argparse
import json
import os
import runpy
import sys
from typing import Dict

CONFIG_PATH = "IQ_Option 2.8.4_config.json"

PRESETS: Dict[str, Dict[str, object]] = {
    "BALANCEADO": {
        "PERFIL_CONFIG_PRESET": "BALANCEADO",
        "UMBRAL_CONFIANZA_COMBINADA": 88.0,
        "UMBRAL_SEÑAL_DESTACADA": 82.0,
        "UMBRAL_SEÑAL_CONFIRMADA": 90.0,
        "AUTO_EJECUTAR_MIN_CONFIANZA": 84.0,
        "UMBRAL_IA_DIRECCION": 50.0,
        "UMBRAL_TECNICO_DIRECCION": 48.0,
        "FILTRO_WM_HABILITADO": False,
        "MAX_TRADES_POR_HORA": 6,
        "MAX_TRADES_POR_DIA": 30,
        "AUTO_EJECUTAR_COOLDOWN_PAR_SEG": 120,
        "COOLDOWN_POST_LOSS_SEC": 120,
        "MAX_OPERACIONES_SIMULTANEAS": 1,
        "INTERES_COMPUESTO_ACTIVO": True,
        "PORCENTAJE_INVERSION": 0.03,
    },
    "AGRESIVO": {
        "PERFIL_CONFIG_PRESET": "AGRESIVO",
        "UMBRAL_CONFIANZA_COMBINADA": 86.0,
        "UMBRAL_SEÑAL_DESTACADA": 80.0,
        "UMBRAL_SEÑAL_CONFIRMADA": 88.0,
        "AUTO_EJECUTAR_MIN_CONFIANZA": 82.0,
        "UMBRAL_IA_DIRECCION": 48.0,
        "UMBRAL_TECNICO_DIRECCION": 46.0,
        "FILTRO_WM_HABILITADO": False,
        "MAX_TRADES_POR_HORA": 8,
        "MAX_TRADES_POR_DIA": 40,
        "AUTO_EJECUTAR_COOLDOWN_PAR_SEG": 90,
        "COOLDOWN_POST_LOSS_SEC": 90,
        "MAX_OPERACIONES_SIMULTANEAS": 1,
        "INTERES_COMPUESTO_ACTIVO": True,
        "PORCENTAJE_INVERSION": 0.03,
    },
}


def _cargar_config(path: str) -> Dict[str, object]:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _guardar_config(path: str, data: Dict[str, object]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def _aplicar_preset(perfil: str, path: str) -> None:
    perfil = perfil.upper()
    if perfil not in PRESETS:
        perfil = "BALANCEADO"
    data = _cargar_config(path)
    data.update(PRESETS[perfil])
    _guardar_config(path, data)


def main() -> None:
    parser = argparse.ArgumentParser(description="IQ Opción IA 2.8 - Modo Consola")
    parser.add_argument(
        "--perfil",
        choices=["balanceado", "agresivo"],
        default="balanceado",
        help="Preset de configuración a aplicar antes de iniciar",
    )
    parser.add_argument(
        "--solo-config",
        action="store_true",
        help="Solo aplica/guarda configuración y termina",
    )
    args, unknown = parser.parse_known_args()

    _aplicar_preset(args.perfil, CONFIG_PATH)

    if args.solo_config:
        print(f"Preset {args.perfil.upper()} aplicado en {CONFIG_PATH}")
        return

    # Forzar modo consola/headless
    os.environ["HEADLESS"] = "true"
    sys.argv = ["IQ_Opcion_IA_2.8.7.py", "--console", *unknown]
    runpy.run_path("IQ_Opcion_IA_2.8.7.py", run_name="__main__")


if __name__ == "__main__":
    main()
