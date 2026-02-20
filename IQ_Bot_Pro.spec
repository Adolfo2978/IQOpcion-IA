# -*- mode: python ; coding: utf-8 -*-
"""Build spec para IQ_Opcion_IA_2.8.py con datos en /Datos y credenciales incluidas."""

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

APP_NAME = 'IQ_Bot_Pro_v2_8'
MAIN_SCRIPT = 'IQ_Opcion_IA_2.8.py'
BASE_DIR = Path(SPEC).parent
DATOS_DIR = BASE_DIR / 'Datos'

hidden_imports = [
    'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
    'torch', 'torch.nn', 'torch.optim', 'torch.utils.data',
    'pandas', 'numpy', 'sklearn', 'requests', 'aiohttp', 'websocket',
    'iqoptionapi', 'iqoptionapi.stable_api', 'iqoptionapi.api',
]
hidden_imports += collect_submodules('sklearn')
hidden_imports += collect_submodules('pandas')
hidden_imports += collect_submodules('iqoptionapi')

datas = []

# Incluir datos del paquete si aplica
datas += collect_data_files('iqoptionapi', include_py_files=False)

# Incluir directorio Datos completo si existe
if DATOS_DIR.exists():
    datas.append((str(DATOS_DIR), 'Datos'))

# Incluir credenciales si existen en raíz (fallback)
for f in ('iq_creds.json', 'telegram_creds.json'):
    src = BASE_DIR / f
    if src.exists():
        datas.append((str(src), 'Datos'))

binaries = []

a = Analysis(
    [str(BASE_DIR / MAIN_SCRIPT)],
    pathex=[str(BASE_DIR)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['IPython', 'jupyter', 'notebook'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
)
