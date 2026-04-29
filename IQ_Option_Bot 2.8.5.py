# IQ_Option 2.2 - Sistema Automático de Trading Binario (CORREGIDO)
# Instalación: pip install -U https://github.com/iqoptionapi/iqoptionapi/archive/refs/heads/master.zip numpy pandas torch matplotlib scipy scikit-learn plyer
#
# USO MULTIPLATAFORMA:
#   Windows GUI:     python IQ_Opcion_IA_2.0.py
#   Windows Consola: python IQ_Opcion_IA_2.0.py --console
#   Linux/Replit:    python IQ_Opcion_IA_2.0.py  (auto-detecta sin display)
#   Forzar consola:  HEADLESS=true python IQ_Opcion_IA_2.0.py
import re
import platform as _platform_early
import os as _os_early
import sys as _sys_early
import argparse as _argparse_early
_parser_early = _argparse_early.ArgumentParser(add_help=False)
_parser_early.add_argument('--console', '-c', action='store_true')
_parser_early.add_argument('--headless', action='store_true')
_args_early, _ = _parser_early.parse_known_args()
_IS_REPLIT_EARLY = _os_early.environ.get('REPL_ID') is not None or _os_early.environ.get('REPLIT') is not None
_HEADLESS_EARLY = _args_early.console or _args_early.headless or _os_early.environ.get('HEADLESS', '').lower() == 'true' or _IS_REPLIT_EARLY or (_platform_early.system() != 'Windows' and _os_early.environ.get('DISPLAY') is None)
if not _HEADLESS_EARLY:
    from tkinter import ttk, messagebox
    import tkinter as tk
else:
    tk = None
    ttk = None
    messagebox = None
from typing import Optional, List, Tuple, cast
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from typing import Dict, Optional
from typing import Tuple
from collections import deque  # Importar deque para el buffer eficiente
import asyncio
import warnings
from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError as _FutTimeoutError,
    as_completed as _futures_as_completed,
)
from functools import lru_cache
import scipy.signal
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta, timezone
import math
import random
import time
import json
import logging
import pickle
import threading
import platform
import sys
import os
import argparse
import traceback
from queue import Queue, Empty
from collections import deque
# Parsear argumentos de línea de comandos PRIMERO
_parser = argparse.ArgumentParser(description='IQ Option Trading Bot 2.0')
_parser.add_argument(
    '--console',
    '-c',
    action='store_true',
    help='Forzar modo consola (sin GUI)')
_parser.add_argument(
    '--headless',
    action='store_true',
    help='Alias de --console')
_args, _unknown = _parser.parse_known_args()
# Configurar modo headless ANTES de importar PyQt5
# Detectar si estamos en un entorno sin display
# En Windows siempre hay GUI disponible, solo Linux/Mac necesitan DISPLAY
IS_WINDOWS = platform.system() == 'Windows'
IS_REPLIT = os.environ.get(
    'REPL_ID') is not None or os.environ.get('REPLIT') is not None
FORCE_CONSOLE = _args.console or _args.headless or os.environ.get(
    'HEADLESS', '').lower() == 'true'
HEADLESS_MODE = False
if FORCE_CONSOLE:
    HEADLESS_MODE = True
elif IS_REPLIT:
    HEADLESS_MODE = True  # Replit siempre es headless
elif not IS_WINDOWS:
    HEADLESS_MODE = os.environ.get('DISPLAY') is None
if HEADLESS_MODE:
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    os.environ['MPLBACKEND'] = 'Agg'  # Matplotlib sin GUI
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
# Configuración de logging - Archivo + Consola en modo headless
_log_handlers: List[logging.Handler] = [
    logging.FileHandler('IQ_Option_2.8.9_pro.log', encoding='utf-8'),
]
if HEADLESS_MODE:
    # En modo consola, también mostrar logs en terminal
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'))
    _log_handlers.append(_console_handler)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=_log_handlers
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(
    __file__)) if "__file__" in globals() else os.getcwd()
DATOS_DIR = os.path.join(BASE_DIR, "Datos")


def datos_rel(filename: str) -> str:
    return os.path.join(DATOS_DIR, filename)


def asegurar_directorio_datos() -> None:
    try:
        os.makedirs(DATOS_DIR, exist_ok=True)
    except Exception:
        pass
    
    # BLOQUE ELIMINADO: Código suelto con variables no definidas
    # if tiempo_actual - ultima_retrain > self.AI_RETRAIN_EVERY_MINUTES * 60:
    #     buffer_nuevos = obtener_ultimos_trades(500)
    #     modelo.retrain(buffer_nuevos)
    #     ultima_retrain = tiempo_actual


def calcular_umbral_combinado(
        umbral_general: float,
        umbral_ia: float,
        umbral_tecnico: float) -> float:
    """
    Evita bloquear operaciones con un umbral combinado imposible.

    Si IA y técnico ya aprobaron sus propios mínimos, la combinación ponderada
    no debe exigir más que el umbral individual más estricto.
    """
    try:
        umbral_general = float(umbral_general or 0.0)
    except Exception:
        umbral_general = 0.0
    try:
        umbral_ia = float(umbral_ia or 0.0)
    except Exception:
        umbral_ia = 0.0
    try:
        umbral_tecnico = float(umbral_tecnico or 0.0)
    except Exception:
        umbral_tecnico = 0.0

    umbral_base = max(umbral_ia, umbral_tecnico)
    if umbral_general <= 0:
        return umbral_base
    return min(umbral_general, umbral_base)


def safe_float(value: Any, default: float = 0.0) -> float:
    """Convierte a float sin exponer None/Unknown al tipado estático."""
    try:
        if value is None:
            return float(default)
        return float(value)
    except Exception:
        return float(default)

def safe_int(value: Any, default: int = 0) -> int:
    """Convierte a int sin exponer None/Unknown al tipado estÃ¡tico."""
    try:
        if value is None:
            return int(default)
        return int(value)
    except Exception:
        return int(default)


def migrar_archivos_datos() -> None:
    try:
        asegurar_directorio_datos()
        for nombre in os.listdir(BASE_DIR):
            ruta = os.path.join(BASE_DIR, nombre)
            if not os.path.isfile(ruta):
                continue
            low = nombre.lower()
            if not (low.endswith(".pkl") or low.endswith(".pth")):
                continue
            destino = os.path.join(DATOS_DIR, nombre)
            if os.path.abspath(ruta) == os.path.abspath(destino):
                continue
            if os.path.exists(destino):
                continue
            try:
                os.replace(ruta, destino)
            except Exception:
                try:
                    import shutil
                    shutil.copy2(ruta, destino)
                except Exception:
                    pass
    except Exception:
        pass


migrar_archivos_datos()


class _IQOptionAPINoiseFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
        except Exception:
            return True
        if "get_all_init_v2 late" in msg or "get_digital_underlying_list_data late" in msg:
            return False
        return True


try:
    _noise_filter = _IQOptionAPINoiseFilter()
    logging.getLogger().addFilter(_noise_filter)
    logging.getLogger("iqoptionapi").addFilter(_noise_filter)
except Exception:
    pass


class LogHandlerGUI(logging.Handler):
    def __init__(self, consola):
        super().__init__()
        self.consola = consola

    def emit(self, record):
        msg = self.format(record)
        self.consola.escribir(msg)


# Mostrar modo de ejecución
# Evita errores de sintaxis por strings multilínea
if HEADLESS_MODE:
    logger.info(
        f"=== MODO CONSOLA (Headless) === Plataforma: {platform.system()}, Replit: {IS_REPLIT}")
# Handler personalizado para enviar logs a la GUI


# ==================================================
# LOGGING SEGURO PARA GUI (THREAD-SAFE)
# ==================================================
_safe_log_emitter = None

class GUILogHandler(logging.Handler):
    """Handler que almacena logs para mostrar en la GUI de forma Thread-Safe"""
    _instance = None
    _logs = deque(maxlen=1000)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def emit(self, record):
        try:
            msg = self.format(record)
            GUILogHandler._logs.append(msg)
            
            # Emitir señal Qt si está disponible (Thread-Safe)
            global _safe_log_emitter
            if _safe_log_emitter:
                _safe_log_emitter.new_log.emit(msg)
        except Exception:
            pass

    @classmethod
    def get_logs(cls):
        """Retorna todos los logs almacenados"""
        return list(cls._logs)

    @classmethod
    def clear_logs(cls):
        """Limpia los logs almacenados"""
        cls._logs.clear()

# Agregar handler de GUI al logger (sin señales todavía)
gui_handler = GUILogHandler()
gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(gui_handler)

# Imports con manejo de errores mejorado
GUI_AVAILABLE = False
MATPLOTLIB_AVAILABLE = False
TORCH_AVAILABLE = False
IQOPTION_AVAILABLE = False
NOTIFICATIONS_AVAILABLE = False
MPLFINANCE_AVAILABLE = False
TALIB_AVAILABLE = False
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
        QGroupBox, QLabel, QPushButton, QProgressBar,
        QPlainTextEdit, QSplitter, QStatusBar, QMessageBox, QGridLayout,
        QAction, QDialog, QFormLayout, QLineEdit,
        QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QCheckBox,
        QDoubleSpinBox, QSpinBox, QTabWidget, QFrame, QTextEdit, QListWidget, QListWidgetItem,
        QSlider, QScrollArea, QRadioButton, QButtonGroup
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize, QRect, QPoint, QObject
    from PyQt5.QtGui import QColor, QFont, QPixmap, QPainter, QBrush, QPen, QIcon, QPalette
    GUI_AVAILABLE = True
    logger.info("PyQt5 cargado exitosamente")

    # ==================================================
    # DEFINIR SafeLogSignal AHORA QUE PyQt ESTÁ DISPONIBLE
    # ==================================================
    class SafeLogSignal(QObject):
        new_log = pyqtSignal(str)
    
    # Inicializar emisor
    try:
        _safe_log_emitter = SafeLogSignal()
    except Exception as e:
        logger.error(f"Error inicializando SafeLogSignal: {e}")

except ImportError as e:
    logger.warning(
        f"PyQt5 no disponible, ejecutando en modo consola. Error: {e}")
    GUI_AVAILABLE = False
try:
    import matplotlib
    if GUI_AVAILABLE:
        matplotlib.use('Qt5Agg')
    else:
        matplotlib.use('Agg')
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    try:
        import mplfinance as mpf
        MPLFINANCE_AVAILABLE = True
        logger.info("mplfinance cargado exitosamente")
    except ImportError:
        logger.warning(
            "mplfinance no disponible, usando método alternativo para gráficos de velas")
        MPLFINANCE_AVAILABLE = False
    MATPLOTLIB_AVAILABLE = True
    logger.info("Matplotlib cargado exitosamente")
except ImportError as e:
    logger.warning(
        f"Matplotlib no disponible, gráficos deshabilitados. Error: {e}")
    MATPLOTLIB_AVAILABLE = False
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.model_selection import train_test_split
    TORCH_AVAILABLE = True
    logger.info("PyTorch cargado exitosamente")
except ImportError as e:
    logger.warning(
        f"PyTorch no disponible, usando red neuronal simulada. Error: {e}")
    TORCH_AVAILABLE = False
# Importación de la API de IQ Option
# PRIORIDAD: iqoptionapi.stable_api (más estable para conexiones WebSocket)
# Variables de disponibilidad
IQOPTION_ASYNC_AVAILABLE = False
IQOPTION_STABLE_AVAILABLE = False
IQOPTION_AVAILABLE = False
IQOptionClient = None
IQ_Option_Stable = None
# PRIMERO: Intentar cargar iqoptionapi.stable_api (RECOMENDADO - más estable)
script_dir = os.path.dirname(os.path.abspath(__file__))
iqoptionapi_local_path = os.path.join(script_dir, 'iqoptionapi')
if os.path.exists(iqoptionapi_local_path):
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
# PRIMERO: Intentar cargar iqoptionapi.stable_api (PRIORIDAD)
try:
    from iqoptionapi.stable_api import IQ_Option as IQ_Option_Stable
    IQOPTION_STABLE_AVAILABLE = True
    IQOPTION_AVAILABLE = True
    logger.info("iqoptionapi.stable_api disponible (PRIORIDAD)")
except ImportError as e:
    logger.warning(f"iqoptionapi.stable_api no disponible: {e}")
# SEGUNDO: Siempre intentar cargar iqoption-async como fallback disponible
try:
    from iqoption_async.client import IQOptionClient  # pyright: ignore[reportMissingImports]
    IQOPTION_ASYNC_AVAILABLE = True
    if not IQOPTION_AVAILABLE:
        IQOPTION_AVAILABLE = True
    logger.info("iqoption-async disponible (FALLBACK)")
except ImportError as e2:
    logger.debug(f"iqoption-async no disponible: {e2}")
if not IQOPTION_AVAILABLE:
    logger.error("Ninguna API de IQ Option disponible")
    logger.error("Instalar con: pip install iqoptionapi")
try:
    import talib  # pyright: ignore[reportMissingImports]
    TALIB_AVAILABLE = True
    logger.info("TA-Lib disponible")
except ImportError as e:
    logger.warning(
        f"TA-Lib no disponible, usando implementación propia. Error: {e}")
    TALIB_AVAILABLE = False
try:
    from plyer import notification  # pyright: ignore[reportMissingImports]
    NOTIFICATIONS_AVAILABLE = True
    logger.info("Sistema de notificaciones disponible")
except ImportError:
    logger.warning("Notificaciones del sistema no disponibles")
    NOTIFICATIONS_AVAILABLE = False
# ==================================================
# HELPER PARA EJECUTAR COROUTINES SINCRONAMENTE
# ==================================================
DEFAULT_TIMEOUT_SECONDS = 60

def seed_everything(seed: int = 42) -> None:
    """Establece seeds para reproducibilidad en RNGs comunes."""
    import random
    random.seed(seed)
    try:
        import numpy as _np
        _np.random.seed(seed)
    except Exception:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if hasattr(torch, 'cuda') and torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except Exception:
        pass

# Garantizar reproducibilidad por defecto
seed_everything(42)

def seed_everything(seed: int = 42) -> None:
    """Establece seeds para reproducibilidad en RNGs comunes."""
    import random
    random.seed(seed)
    try:
        import numpy as _np
        _np.random.seed(seed)
    except Exception:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if hasattr(torch, 'cuda') and torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except Exception:
        pass

# Garantizar reproducibilidad por defecto
seed_everything(42)

def seed_everything(seed: int = 42) -> None:
    import random
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except Exception:
        pass

# Ensure determinism for reproducibility
seed_everything(42)


def _run_async_safe(coro):
    """
    Ejecuta una coroutine de forma síncrona.
    Compatible con PyQt5 y contextos donde ya hay un event loop.
    """
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        # Ya hay un loop corriendo (PyQt5), usar thread pool
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result(timeout=DEFAULT_TIMEOUT_SECONDS)
    else:
        # No hay loop, crear uno nuevo
        return asyncio.run(coro)
# ==================================================
# CAPITULO 1: FEATURE ENGINEERING AVANZADO (Pattern Recognition)
# ==================================================


class FeatureExtractor:
    """
    Extrae EXACTAMENTE 15 características numéricas estables y normalizadas.
    Diseñado para aprendizaje online (SGDClassifier) con datos reales en binarias.
    """

    def __init__(self):
        self.feature_names = [
            'dist_ema_20',          # 0
            'dist_ema_50',          # 1
            'rsi',                  # 2
            'volatility',           # 3
            'vol_spike',            # 4
            'close_lag1',           # 5
            'close_lag2',           # 6
            'high_lag1',            # 7
            'low_lag1',             # 8
            'body_lag1',            # 9
            'price_change_t1',      # 10
            'price_change_t2',      # 11
            'ema_slope',            # 12
            'price_vs_ema_range',   # 13
            'volume_avg_diff'       # 14
        ]

    def _validate_no_lookahead(self, df: pd.DataFrame) -> bool:
        """Guard against lookahead leakage: if the last timestamp is in the future, reject."""
        try:
            if df is None or len(df) == 0:
                return True
            idx = df.index
            if isinstance(idx, pd.DatetimeIndex) and len(idx) > 0:
                last_ts = idx[-1]
                if isinstance(last_ts, pd.Timestamp) and last_ts > pd.Timestamp.now():
                    return False
        except Exception:
            return True
        return True

    def calculate_features(self, df: pd.DataFrame) -> np.ndarray:
        # --- VALIDACIÓN FUERTE ---
        logger.debug(f"[FEATURE] Inicio cálculo de features: df_len={len(df) if df is not None else 0}")
        if df is None or len(df) < 60:
            return np.zeros((1, 15), dtype=np.float32)

        df = df.copy()
        # Lookahead leakage check
        if not self._validate_no_lookahead(df):
            # Return zeros para evitar usar datos futuros
            return np.zeros((1, 15), dtype=np.float32)

        # Asegurar tipos
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)

        # ===============================
        # 1️⃣ TENDENCIA (EMA)
        # ===============================
        df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()

        df['dist_ema_20'] = (df['close'] - df['ema_20']) / \
            (df['ema_20'] + 1e-10)
        df['dist_ema_50'] = (df['close'] - df['ema_50']) / \
            (df['ema_50'] + 1e-10)

        # Pendiente relativa (no absoluta)
        df['ema_slope'] = df['ema_20'].diff() / (df['ema_20'] + 1e-10)

        # ===============================
        # 2️⃣ MOMENTUM (RSI)
        # ===============================
        delta = df['close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / (loss + 1e-10)
        df['rsi'] = (100 - (100 / (1 + rs))).clip(0, 100)

        # ===============================
        # 3️⃣ VOLATILIDAD REAL (ATR)
        # ===============================
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift()).abs()
        low_close = (df['low'] - df['close'].shift()).abs()

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = tr.rolling(14).mean()

        df['volatility'] = df['atr'] / (df['close'] + 1e-10)

        # ===============================
        # 4️⃣ VOLUMEN (SMART MONEY)
        # ===============================
        df['vol_sma'] = df['volume'].rolling(20).mean()
        df['vol_spike'] = df['volume'] / (df['vol_sma'] + 1e-10)
        df['volume_avg_diff'] = (
            df['volume'] - df['vol_sma']) / (df['vol_sma'] + 1e-10)

        # ===============================
        # 5️⃣ CONTEXTO TEMPORAL (LAGS)
        # ===============================
        df['close_lag1'] = (df['close'].shift(
            1) - df['close']) / (df['close'] + 1e-10)
        df['close_lag2'] = (df['close'].shift(
            2) - df['close']) / (df['close'] + 1e-10)

        df['high_lag1'] = (df['high'].shift(1) - df['close']
                           ) / (df['close'] + 1e-10)
        df['low_lag1'] = (df['low'].shift(1) - df['close']) / \
            (df['close'] + 1e-10)

        df['body_lag1'] = (df['close'].shift(
            1) - df['open'].shift(1)) / (df['close'] + 1e-10)

        df['price_change_t1'] = df['close'].pct_change(1)
        df['price_change_t2'] = df['close'].pct_change(2)

        # ===============================
        # 6️⃣ PRECISIÓN DE ENTRADA
        # ===============================
        df['price_vs_ema_range'] = abs(
            df['close'] - df['ema_20']) / (df['atr'] + 1e-10)

        # ===============================
        # 7️⃣ SELECCIÓN FINAL (FIJA)
        # ===============================
        features = df[self.feature_names].fillna(
            0.0).tail(1).values.astype(np.float32)

        # Validación crítica
        if features.shape != (1, 15):
            raise ValueError(
                f"FeatureExtractor ERROR: shape inválido {
                    features.shape}")

        logger.debug(f"[FEATURE] Features calculadas: shape={features.shape}")
        return features

# ==================================================
# CAPITULO 2: AI ENGINE OPTIMIZADO (Aprendizaje Real)
# ==================================================


class AIEngineContinuous:
    """
    Motor IA continuo con aprendizaje REAL por batch.
    Aprende SOLO de resultados reales (WIN / LOSS).
    Optimizado para binarias (una operación a la vez).
    """

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._last_trade_id = None

        self.extractor = FeatureExtractor()
        self.model_path = datos_rel("modelo_continuo.pkl")
        self.scaler_path = datos_rel("scaler_continuo.pkl")

        from sklearn.linear_model import SGDClassifier
        from sklearn.preprocessing import StandardScaler

        self.model = SGDClassifier(
            loss='log_loss',
            penalty='l2',
            alpha=1e-4,
            learning_rate='optimal',
            warm_start=True,
            max_iter=1
        )

        self.scaler = StandardScaler()
        self._lock = threading.RLock()

        self._is_initialized = False
        self._last_features = None
        self._last_direction = None  # CALL / PUT

        # Batch learning
        self.batch_size = 5
        self.trade_buffer = deque(maxlen=self.batch_size)

        self.logger.info(
            f"🧠 AIEngineContinuous listo | Batch Learning REAL ({
                self.batch_size} ops)"
        )
        self._try_load_persisted_state()

    def _try_load_persisted_state(self) -> None:
        try:
            import joblib
            model_loaded = False
            scaler_loaded = False
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                model_loaded = True
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                scaler_loaded = True
            if model_loaded and scaler_loaded:
                self._is_initialized = True
                self.logger.info("✅ IA cargada desde disco (modelo+scaler)")
        except Exception as e:
            self.logger.debug(f"No se pudo cargar IA persistida: {e}")

    # ==================================================
    # PREDICCIÓN
    # =====================================
    def predict_latest(self, df: pd.DataFrame) -> Tuple[float, dict]:
        """
        Retorna confianza (0–100) y metadata.
        🚫 La IA NUNCA habilita trading si confianza < UMBRAL (default 85%)
        """
        # Validación de entrada para seguridad
        if df is None or not isinstance(df, pd.DataFrame):
            self.logger.error("[IA] DF inválido: se esperaba un DataFrame de pandas")
            self._last_direction = None
            return 0.0, {"estado": "DF_INVALIDO"}
        # Validación de entrada
        if df is None or not isinstance(df, pd.DataFrame):
            self.logger.error("[IA] DF inválido: se esperaba un DataFrame de pandas")
            self._last_direction = None
            return 0.0, {"estado": "DF_INVALIDO"}
        try:
            # ==============================
            # VALIDACIÓN DF
            # ==============================
            required = {"open", "high", "low", "close"}
            if not required.issubset(df.columns):
                self.logger.error("[IA] DF inválido → columnas OHLC faltantes")
                self._last_direction = None
                return 0.0, {"estado": "DF_INVALIDO"}

            # ==============================
            # EXTRACCIÓN FEATURES
            # ==============================
            features = self.extractor.calculate_features(df)

            if features is None or np.isnan(features).any():
                self.logger.warning("[IA] Features inválidas → WAIT")
                self._last_direction = None
                return 0.0, {"estado": "WAIT"}

            # Guardar features SOLO si luego hay trade válido
            self._last_features = features.copy()
            self._feedback_consumed = False
            # Generar ID único para este ciclo de predicción
            self._pending_trade_id = int(time.time() * 1000000)
            
            # ==============================
            # MODELO NO ENTRENADO → BLOQUEO TOTAL
            # ==============================
            with self._lock:
                if not self._is_initialized:
                    self.logger.info(
                        "[IA] Estado: NO ENTRENADO | WAIT (sin operación)"
                    )
                    self._last_direction = None
                    return 0.0, {
                        "modelo": "SGD-Batch",
                        "estado": "NO_ENTRENADO",
                        "confidence": 0.0,
                        "direccion": None
                    }

            # ==============================
            # PREDICCIÓN REAL
            # ==============================
            with self._lock:
                X_scaled = self.scaler.transform(features)
                proba_call = float(self.model.predict_proba(X_scaled)[0, 1])

            confidence_raw = round(proba_call * 100, 2)

            # ==============================
            # 🔥 FILTRO CRÍTICO DE CONFIANZA
            # ==============================
            UMBRAL_OPERACION = float(
                getattr(
                    self.config,
                    "UMBRAL_IA_DIRECCION",
                    getattr(self.config, "UMBRAL_COMPRA", 85.0)
                )
            )

            direccion = None
            confidence = confidence_raw

            if confidence_raw >= UMBRAL_OPERACION:
                direccion = "CALL"
            elif (100 - confidence_raw) >= UMBRAL_OPERACION:
                direccion = "PUT"
                confidence = round(100 - confidence_raw, 2)
            else:
                self._last_direction = None
                self.logger.info(
                    f"[IA] Confianza insuficiente ({confidence_raw:.2f}%) "
                    f"< {UMBRAL_OPERACION}% → WAIT"
                )
                return confidence_raw, {
                    "estado": "WAIT",
                    "confidence": confidence_raw,
                    "direccion": None
                }

            # ==============================
            # CONFIRMACIÓN FINAL
            # ==============================
            self._last_direction = direccion
            self.last_confidence = confidence / 100.0

            self.logger.info(
                f"[IA] Predicción VALIDADA | "
                f"Confianza={confidence:.2f}% | "
                f"Dirección={direccion} | "
                f"Entrenada={self._is_initialized} | "
                f"Buffer={len(self.trade_buffer)}"
            )

            return confidence, {
                "modelo": "SGD-Batch",
                "estado": "OK",
                "confidence": confidence,
                "direccion": direccion
            }

        except Exception as e:
            self.logger.error(
                f"❌ Error predict_latest IA: {e}",
                exc_info=True
            )
            self._last_direction = None
            return 0.0, {"estado": "ERROR"}

    def is_initialized(self) -> bool:
        return bool(self._is_initialized)

    def cold_start_training(self, df: pd.DataFrame):
        """
        Entrenamiento inicial con datos históricos (COLD START).
        Simula operaciones binarias reales (CALL / PUT).
        """
        # Validaciones de entrada para evitar errores en producción
        if df is None or not isinstance(df, pd.DataFrame):
            self.logger.error("[IA] Cold Start abortado: DF inválido o no proporcionado")
            return
        required = {"open", "high", "low", "close"}
        if not required.issubset(df.columns):
            self.logger.error(
                f"[IA] Cold Start abortado: DF OHLC inválido. Recibidas={set(df.columns)}"
            )
            return

        try:
            self.logger.info(
                "🧊 Iniciando entrenamiento en frío (histórico)...")

        # ==================================================
        # VALIDACIONES CRÍTICAS (PROBLEMA 5 SOLUCIONADO)
        # ==================================================
            if df is None or len(df) < 100:
                if not getattr(self.config, 'FORZAR_DATOS_REALES', True):
                    self.logger.warning("Datos insuficientes. Generando datos sintéticos para inicialización...")
                    # Generar datos sintéticos para inicializar
                    fechas = pd.date_range(end=datetime.now(), periods=200, freq='min')
                    base_price = 100.0
                    prices = [base_price]
                    for _ in range(199):
                        change = np.random.uniform(-0.001, 0.001)
                        prices.append(prices[-1] * (1 + change))
                    
                    df = pd.DataFrame({
                        'open': prices,
                        'high': [p * 1.0001 for p in prices],
                        'low': [p * 0.9999 for p in prices],
                        'close': prices,
                        'volume': 1000
                    }, index=fechas)
                else:
                    raise ValueError(
                        "DataFrame vacío o insuficiente para cold start y FORZAR_DATOS_REALES=True")

            if getattr(self.config, 'FORZAR_DATOS_REALES', True):
                if isinstance(df, pd.DataFrame) and 'tipo_datos' in df.columns:
                    if (df['tipo_datos'] == 'SINTETICO').any():
                        raise ValueError(
                            "Cold start bloqueado: datos sintéticos detectados y FORZAR_DATOS_REALES=True")

            required = {"open", "high", "low", "close"}
            if not required.issubset(df.columns):
                raise ValueError(
                    f"DF no contiene columnas OHLC válidas. "
                    f"Requeridas={required}, Recibidas={set(df.columns)}"
                )

            if not hasattr(self.model, "partial_fit"):
                raise RuntimeError(
                    f"Modelo {type(self.model).__name__} "
                    "no soporta entrenamiento incremental (partial_fit)"
                )

        # ==================================================
        # DATASET SINTÉTICO PARA ARRANQUE
        # ==================================================
            features = []
            targets = []
            synthetic_returns = []

            ventana_size = 60
            expiracion_velas = 1
            ruido_minimo = 1e-5  # 
