"""Alias de compatibilidad para ejecutar la versión 2.8.6.

Este archivo existe para quienes lanzan el bot con `IQ_Opcion_IA_2.8.py`.
Redirige la ejecución al script principal actual.
"""

from runpy import run_path
from pathlib import Path


if __name__ == "__main__":
    run_path(str(Path(__file__).with_name("IQ_Opcion_IA_2.8.6.py")), run_name="__main__")
