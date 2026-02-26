# Auditoría técnica — IQ_Opcion_IA_2.8.py

## Resumen ejecutivo
- Líneas totales: **24878**
- Definiciones top-level (funciones/clases): **67**
- Imports detectados: **42**
- Imports duplicados: **6** → collections.deque, datetime.datetime, typing.Dict, typing.List, typing.Optional, typing.Tuple

## Hallazgos de riesgo (AST)
- `silent_exception` en línea **211**, exc=Exception
- `silent_exception` en línea **2043**, exc=Exception
- `silent_exception` en línea **2106**, exc=Exception
- `silent_exception` en línea **2815**, exc=Exception
- `silent_exception` en línea **2920**, exc=Exception
- `silent_exception` en línea **7147**, exc=Exception
- `silent_exception` en línea **8282**, exc=Exception
- `silent_exception` en línea **8305**, exc=Exception
- `silent_exception` en línea **8338**, exc=BaseException
- `silent_exception` en línea **8364**, exc=BaseException
- `silent_exception` en línea **9240**, exc=Exception
- `silent_exception` en línea **9354**, exc=Exception
- `silent_exception` en línea **9412**, exc=Exception
- `silent_exception` en línea **10168**, exc=Exception
- `silent_exception` en línea **10176**, exc=Exception
- `silent_exception` en línea **10246**, exc=Exception
- `silent_exception` en línea **10265**, exc=Exception
- `silent_exception` en línea **10364**, exc=Exception
- `silent_exception` en línea **10385**, exc=Exception
- `silent_exception` en línea **10404**, exc=Exception
- `silent_exception` en línea **10607**, exc=Exception
- `silent_exception` en línea **14621**, exc=Exception
- `silent_exception` en línea **14693**, exc=Exception
- `silent_exception` en línea **14713**, exc=Exception
- `silent_exception` en línea **16131**, exc=Exception
- `silent_exception` en línea **16166**, exc=Exception
- `silent_exception` en línea **18557**, exc=Exception
- `silent_exception` en línea **19383**, exc=Exception
- `silent_exception` en línea **19389**, exc=Exception
- `silent_exception` en línea **23020**, exc=Exception
- `silent_exception` en línea **23667**, exc=BaseException
- `silent_exception` en línea **24364**, exc=Exception
- `silent_exception` en línea **24373**, exc=Exception
- `silent_exception` en línea **24389**, exc=Exception
- `silent_exception` en línea **24418**, exc=Exception
- `silent_exception` en línea **24675**, exc=Exception
- `silent_exception` en línea **24717**, exc=Exception
- `silent_exception` en línea **3299**, exc=Exception
- `silent_exception` en línea **3312**, exc=Exception
- `silent_exception` en línea **3322**, exc=Exception
- `silent_exception` en línea **8173**, exc=Exception
- `silent_exception` en línea **9542**, exc=Exception
- `silent_exception` en línea **10226**, exc=Exception
- `silent_exception` en línea **10230**, exc=Exception
- `silent_exception` en línea **10235**, exc=Exception
- `silent_exception` en línea **10239**, exc=Exception
- `silent_exception` en línea **10373**, exc=Exception
- `silent_exception` en línea **10423**, exc=Exception
- `silent_exception` en línea **10708**, exc=Exception
- `silent_exception` en línea **12371**, exc=Exception
- `silent_exception` en línea **13557**, exc=Exception
- `silent_exception` en línea **14887**, exc=Exception
- `silent_exception` en línea **15258**, exc=Exception
- `silent_exception` en línea **17347**, exc=Exception
- `silent_exception` en línea **17404**, exc=Exception
- `silent_exception` en línea **19950**, exc=Exception
- `silent_exception` en línea **20762**, exc=Exception
- `silent_exception` en línea **20829**, exc=Exception
- `silent_exception` en línea **20859**, exc=Exception
- `silent_exception` en línea **23589**, exc=BaseException
- `silent_exception` en línea **23680**, exc=BaseException
- `silent_exception` en línea **24666**, exc=Exception
- `silent_exception` en línea **24724**, exc=Exception
- `silent_exception` en línea **2241**, exc=Exception
- `silent_exception` en línea **2288**, exc=Exception
- `silent_exception` en línea **2918**, exc=Exception
- `silent_exception` en línea **4618**, exc=Exception
- `silent_exception` en línea **4624**, exc=Exception
- `silent_exception` en línea **4723**, exc=Exception
- `silent_exception` en línea **7569**, exc=Exception
- `silent_exception` en línea **10069**, exc=Exception
- `silent_exception` en línea **10208**, exc=Exception
- `silent_exception` en línea **10244**, exc=Exception
- `silent_exception` en línea **10413**, exc=Exception
- `silent_exception` en línea **10417**, exc=Exception
- `silent_exception` en línea **10900**, exc=Exception
- `silent_exception` en línea **12759**, exc=Exception
- `silent_exception` en línea **13351**, exc=Exception
- `silent_exception` en línea **14105**, exc=BaseException
- `silent_exception` en línea **14883**, exc=Exception

## Bloques más grandes (mantenibilidad)
- ClassDef `IQOptionBridge` líneas 9297-14159 (**4863** líneas)
- ClassDef `ConfiguracionDialog` líneas 18504-19906 (**1403** líneas)
- ClassDef `EstrategiaMultiTimeframe` líneas 5647-6923 (**1277** líneas)
- ClassDef `SeguimientoSenales` líneas 7532-8412 (**881** líneas)
- ClassDef `MarketMakerStrategy` líneas 4781-5640 (**860** líneas)
- ClassDef `AnalizadorMercado` líneas 15268-16083 (**816** líneas)
- ClassDef `ConfiguracionTrading` líneas 2550-3323 (**774** líneas)
- ClassDef `TelegramNotifier` líneas 16090-16780 (**691** líneas)
- ClassDef `MotorTradingIntegrado` líneas 1778-2440 (**663** líneas)
- ClassDef `AutoTrainer` líneas 8418-9074 (**657** líneas)

## Smoke tests funcionales (datos sintéticos)
- `skipped`: **True**
- `reason`: **numpy/pandas no disponibles en el entorno**

## Recomendaciones prioritarias
1. Evitar `FORCE_CONSOLE = True` hardcodeado para no anular los argumentos CLI.
2. Reducir bloques monolíticos (clases/métodos muy extensos) y extraer módulos por dominio.
3. Reemplazar `except Exception/BaseException: pass` por manejo explícito + logging contextual.
4. Eliminar imports duplicados y consolidar typing/import section para mejorar legibilidad.
