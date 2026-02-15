# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File para IQ Bot Pro
======================================

Genera un ejecutable portable (.exe) con:
- Todas las dependencias embebidas
- Sin archivos externos visibles
- Datos guardados en AppData (oculto)

Uso:
    pyinstaller IQ_Bot_Pro.spec

Requisitos:
    pip install pyinstaller
"""

import os
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

APP_NAME = 'IQ_Bot_Pro v 2.0'
APP_VERSION = '2.0.0'
MAIN_SCRIPT = 'IQ_Opcion_IA_2.8.4.py'

# Directorio base del proyecto
BASE_DIR = Path(SPEC).parent

# ============================================================================
# HIDDEN IMPORTS
# ============================================================================

# Módulos que PyInstaller no detecta automáticamente
hidden_imports = [
    # PyQt5
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.sip',
    
    # PyTorch
    'torch',
    'torch.nn',
    'torch.optim',
    'torch.utils.data',
    
    # Scikit-learn
    'sklearn',
    'sklearn.preprocessing',
    'sklearn.linear_model',
    'sklearn.ensemble',
    'sklearn.utils',
    'sklearn.utils._cython_blas',
    'sklearn.neighbors._typedefs',
    'sklearn.neighbors._quad_tree',
    'sklearn.tree._utils',
    
    # Pandas / NumPy
    'pandas',
    'pandas.core.arrays.masked',
    'numpy',
    'numpy.core._methods',
    'numpy.lib.format',
    
    # TA-Lib (indicadores técnicos)
    'talib',
    'talib.abstract',
    
    # Networking
    'websocket',
    'websockets',
    'aiohttp',
    'requests',
    
    # IQ Option API
    'iqoptionapi',
    'iqoptionapi.stable_api',
    'iqoptionapi.api',
    
    # Otros
    'json',
    'pickle',
    'base64',
    'logging',
    'threading',
    'queue',
    'datetime',
    'time',
    'os',
    'sys',
    'pathlib',
    
    # Módulo de almacenamiento oculto
    'hidden_storage',
]

# Recolectar submódulos de librerías grandes
hidden_imports += collect_submodules('sklearn')
hidden_imports += collect_submodules('pandas')

# ============================================================================
# DATA FILES (archivos embebidos en el .exe)
# ============================================================================

# Archivos de datos que se incluirán en el bundle
# NOTA: NO incluir configuración ni modelos - se guardan en AppData
datas = [
    # Iconos e imágenes (si existen)
    # ('icons/*.png', 'icons'),
    # ('icons/*.ico', 'icons'),
    
    # Archivo de almacenamiento oculto (módulo auxiliar)
    ('hidden_storage.py', '.'),
]

# ============================================================================
# BINARIES
# ============================================================================

# DLLs adicionales que pueden ser necesarias
binaries = []

# En Windows, incluir DLLs de TA-Lib si están disponibles
if sys.platform == 'win32':
    talib_dll = Path(sys.prefix) / 'Library' / 'bin' / 'ta_lib.dll'
    if talib_dll.exists():
        binaries.append((str(talib_dll), '.'))

# ============================================================================
# ANÁLISIS
# ============================================================================

a = Analysis(
    [MAIN_SCRIPT],
    pathex=[str(BASE_DIR)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir módulos innecesarios para reducir tamaño
        'tkinter',
        'matplotlib',
        'PIL',
        'scipy.spatial.cKDTree',
        'IPython',
        'jupyter',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# ============================================================================
# PYZ (Python archive)
# ============================================================================

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

# ============================================================================
# EXE
# ============================================================================

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
    upx=True,  # Comprimir con UPX si está disponible
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola (GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    
    # Icono de la aplicación (crear si no existe)
    # icon='icons/app.ico',
    
    # Información de versión (Windows)
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)

# ============================================================================
# BUNDLE (solo macOS)
# ============================================================================

if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name=f'{APP_NAME}.app',
        icon=None,  # 'icons/app.icns',
        bundle_identifier='com.iqbotpro.trading',
        info_plist={
            'CFBundleName': APP_NAME,
            'CFBundleDisplayName': 'IQ Bot Pro',
            'CFBundleVersion': APP_VERSION,
            'CFBundleShortVersionString': APP_VERSION,
            'NSHighResolutionCapable': True,
        },
    )
