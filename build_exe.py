#!/usr/bin/env python3
"""
Script de Compilación para IQ Bot Pro
======================================

Genera el ejecutable .exe portable con todas las dependencias.

Uso:
    python build_exe.py [--clean] [--debug] [--console]

Opciones:
    --clean     Limpiar builds anteriores antes de compilar
    --debug     Incluir información de depuración
    --console   Mostrar ventana de consola (para debug)
    
Requisitos:
    pip install pyinstaller
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

APP_NAME = 'IQ_Bot_Pro'
APP_VERSION = '2.0.0'
MAIN_SCRIPT = 'IQ_Opcion_IA_2.0.py'
SPEC_FILE = 'IQ_Bot_Pro.spec'

# Directorios
BASE_DIR = Path(__file__).parent
BUILD_DIR = BASE_DIR / 'build'
DIST_DIR = BASE_DIR / 'dist'

# ============================================================================
# FUNCIONES
# ============================================================================

def print_header():
    """Imprime cabecera del script."""
    print("=" * 60)
    print(f"  IQ Bot Pro - Compilador de Ejecutable")
    print(f"  Versión: {APP_VERSION}")
    print(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    print("[1/5] Verificando dependencias...")
    
    # Verificar PyInstaller
    try:
        import PyInstaller
        print(f"  - PyInstaller: v{PyInstaller.__version__}")
    except ImportError:
        print("  ERROR: PyInstaller no instalado")
        print("  Ejecutar: pip install pyinstaller")
        return False
    
    # Verificar script principal
    if not (BASE_DIR / MAIN_SCRIPT).exists():
        print(f"  ERROR: No se encuentra {MAIN_SCRIPT}")
        return False
    print(f"  - Script principal: OK")
    
    # Verificar hidden_storage.py
    if not (BASE_DIR / 'hidden_storage.py').exists():
        print(f"  ERROR: No se encuentra hidden_storage.py")
        return False
    print(f"  - Módulo hidden_storage: OK")
    
    # Verificar dependencias críticas
    critical_deps = ['PyQt5', 'torch', 'sklearn', 'pandas', 'numpy']
    for dep in critical_deps:
        try:
            __import__(dep)
            print(f"  - {dep}: OK")
        except ImportError:
            print(f"  ADVERTENCIA: {dep} no instalado (puede causar errores)")
    
    print()
    return True

def clean_build():
    """Limpia directorios de builds anteriores."""
    print("[2/5] Limpiando builds anteriores...")
    
    dirs_to_clean = [BUILD_DIR, DIST_DIR]
    for d in dirs_to_clean:
        if d.exists():
            shutil.rmtree(d)
            print(f"  - Eliminado: {d.name}/")
    
    # Limpiar archivos .pyc
    for pyc in BASE_DIR.rglob('*.pyc'):
        pyc.unlink()
    
    # Limpiar __pycache__
    for cache in BASE_DIR.rglob('__pycache__'):
        shutil.rmtree(cache)
    
    print()

def create_version_info():
    """Crea archivo de información de versión para Windows."""
    print("[3/5] Generando información de versión...")
    
    version_parts = APP_VERSION.split('.')
    while len(version_parts) < 4:
        version_parts.append('0')
    
    version_info = f'''# UTF-8
#
# Información de versión para Windows
#

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({','.join(version_parts)}),
    prodvers=({','.join(version_parts)}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'IQ Bot Pro'),
            StringStruct(u'FileDescription', u'Trading Bot para IQ Option'),
            StringStruct(u'FileVersion', u'{APP_VERSION}'),
            StringStruct(u'InternalName', u'{APP_NAME}'),
            StringStruct(u'LegalCopyright', u'Copyright 2024'),
            StringStruct(u'OriginalFilename', u'{APP_NAME}.exe'),
            StringStruct(u'ProductName', u'IQ Bot Pro'),
            StringStruct(u'ProductVersion', u'{APP_VERSION}'),
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    version_file = BASE_DIR / 'version_info.txt'
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print(f"  - Creado: version_info.txt")
    print()

def build_executable(debug=False, console=False):
    """Compila el ejecutable."""
    print("[4/5] Compilando ejecutable...")
    print(f"  - Modo debug: {'Sí' if debug else 'No'}")
    print(f"  - Con consola: {'Sí' if console else 'No'}")
    print()
    
    # Construir comando
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
    ]
    
    # Usar spec file si existe, sino construir desde parámetros
    if (BASE_DIR / SPEC_FILE).exists():
        cmd.append(SPEC_FILE)
        
        # Modificar spec temporalmente si se necesita consola
        if console:
            print("  NOTA: Para modo consola, editar IQ_Bot_Pro.spec y cambiar console=True")
    else:
        # Construir sin spec file
        cmd.extend([
            '--name', APP_NAME,
            '--onefile',
            '--windowed' if not console else '--console',
            '--add-data', f'hidden_storage.py{os.pathsep}.',
            MAIN_SCRIPT
        ])
    
    if debug:
        cmd.append('--debug=all')
    
    # Ejecutar PyInstaller
    print("  Ejecutando PyInstaller...")
    print(f"  Comando: {' '.join(cmd)}")
    print()
    print("-" * 60)
    
    result = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        capture_output=False
    )
    
    print("-" * 60)
    print()
    
    return result.returncode == 0

def post_build():
    """Tareas post-compilación."""
    print("[5/5] Finalizando...")
    
    exe_path = DIST_DIR / f'{APP_NAME}.exe'
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"  - Ejecutable creado: {exe_path}")
        print(f"  - Tamaño: {size_mb:.1f} MB")
        
        # Crear archivo README
        readme_content = f'''IQ Bot Pro v{APP_VERSION}
========================

INSTRUCCIONES DE USO:
1. Ejecutar {APP_NAME}.exe
2. Ingresar credenciales de IQ Option
3. Configurar parámetros de trading
4. Iniciar bot

NOTAS:
- Los datos se guardan en: %APPDATA%\\IQ_Bot_Pro
- El modelo de IA aprende automáticamente
- La configuración persiste entre sesiones

SOPORTE:
- Los archivos de configuración están protegidos
- Para resetear: eliminar carpeta %APPDATA%\\IQ_Bot_Pro
'''
        readme_path = DIST_DIR / 'LEEME.txt'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  - Creado: LEEME.txt")
        
        return True
    else:
        print("  ERROR: No se generó el ejecutable")
        return False

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Compilar IQ Bot Pro')
    parser.add_argument('--clean', action='store_true', help='Limpiar antes de compilar')
    parser.add_argument('--debug', action='store_true', help='Modo debug')
    parser.add_argument('--console', action='store_true', help='Mostrar consola')
    args = parser.parse_args()
    
    print_header()
    
    # Verificar dependencias
    if not check_dependencies():
        print("ERROR: Faltan dependencias críticas")
        sys.exit(1)
    
    # Limpiar si se solicita
    if args.clean:
        clean_build()
    
    # Crear info de versión
    create_version_info()
    
    # Compilar
    if not build_executable(debug=args.debug, console=args.console):
        print("ERROR: Falló la compilación")
        sys.exit(1)
    
    # Post-build
    if not post_build():
        print("ERROR: Falló post-compilación")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("  COMPILACIÓN EXITOSA")
    print(f"  Ejecutable: dist/{APP_NAME}.exe")
    print("=" * 60)

if __name__ == '__main__':
    main()
