"""Launcher profesional SOLO CONSOLA para IQ Opción IA 2.8.7.

Uso:
  python IQ_Opcion_IA_2.8.py --perfil balanceado
  python IQ_Opcion_IA_2.8.py --perfil agresivo
"""
import argparse
import os
import runpy


def main():
    parser = argparse.ArgumentParser(description="IQ Opción IA 2.8 - Modo Consola")
    parser.add_argument("--perfil", choices=["balanceado", "agresivo"], default=None,
                        help="Aplicar preset de configuración antes de iniciar")
    args, unknown = parser.parse_known_args()

    # Forzar consola/headless
    os.environ["HEADLESS"] = "true"

    if args.perfil:
        # Guardar selección para que la tome la app en el menú/config
        try:
            import json
            cfg = "IQ_Option 2.8.7.4_config.json"
            data = {}
            if os.path.exists(cfg):
                with open(cfg, "r", encoding="utf-8") as f:
                    data = json.load(f) or {}
            data["PERFIL_CONFIG_PRESET"] = args.perfil.upper()
            with open(cfg, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

    # Pasar bandera --console al script principal
    import sys
    sys.argv = ["IQ_Opcion_IA_2.8.7.py", "--console", *unknown]
    runpy.run_path("IQ_Opcion_IA_2.8.7.py", run_name="__main__")


if __name__ == "__main__":
    main()
