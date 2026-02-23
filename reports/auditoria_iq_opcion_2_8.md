# Auditoría técnica — IQ_Opcion_IA_2.8.py

## Resumen ejecutivo
- Líneas totales: **24782**
- Definiciones top-level (funciones/clases): **67**
- Imports detectados: **41**
- Imports duplicados: **6** → collections.deque, datetime.datetime, typing.Dict, typing.List, typing.Optional, typing.Tuple

## Hallazgos de riesgo (AST)
- `silent_exception` en línea **203**, exc=Exception
- `silent_exception` en línea **2035**, exc=Exception
- `silent_exception` en línea **2098**, exc=Exception
- `silent_exception` en línea **2807**, exc=Exception
- `silent_exception` en línea **2912**, exc=Exception
- `silent_exception` en línea **7135**, exc=Exception
- `silent_exception` en línea **8270**, exc=Exception
- `silent_exception` en línea **8293**, exc=Exception
- `silent_exception` en línea **8326**, exc=BaseException
- `silent_exception` en línea **8352**, exc=BaseException
- `silent_exception` en línea **9228**, exc=Exception
- `silent_exception` en línea **9342**, exc=Exception
- `silent_exception` en línea **9393**, exc=Exception
- `silent_exception` en línea **10148**, exc=Exception
- `silent_exception` en línea **10156**, exc=Exception
- `silent_exception` en línea **10226**, exc=Exception
- `silent_exception` en línea **10307**, exc=Exception
- `silent_exception` en línea **10326**, exc=Exception
- `silent_exception` en línea **10526**, exc=Exception
- `silent_exception` en línea **14525**, exc=Exception
- `silent_exception` en línea **14597**, exc=Exception
- `silent_exception` en línea **14617**, exc=Exception
- `silent_exception` en línea **16035**, exc=Exception
- `silent_exception` en línea **16070**, exc=Exception
- `silent_exception` en línea **18461**, exc=Exception
- `silent_exception` en línea **19287**, exc=Exception
- `silent_exception` en línea **19293**, exc=Exception
- `silent_exception` en línea **22924**, exc=Exception
- `silent_exception` en línea **23571**, exc=BaseException
- `silent_exception` en línea **24268**, exc=Exception
- `silent_exception` en línea **24277**, exc=Exception
- `silent_exception` en línea **24293**, exc=Exception
- `silent_exception` en línea **24322**, exc=Exception
- `silent_exception` en línea **24579**, exc=Exception
- `silent_exception` en línea **24621**, exc=Exception
- `silent_exception` en línea **3291**, exc=Exception
- `silent_exception` en línea **3304**, exc=Exception
- `silent_exception` en línea **3314**, exc=Exception
- `silent_exception` en línea **8161**, exc=Exception
- `silent_exception` en línea **9523**, exc=Exception
- `silent_exception` en línea **10206**, exc=Exception
- `silent_exception` en línea **10210**, exc=Exception
- `silent_exception` en línea **10215**, exc=Exception
- `silent_exception` en línea **10219**, exc=Exception
- `silent_exception` en línea **10295**, exc=Exception
- `silent_exception` en línea **10344**, exc=Exception
- `silent_exception` en línea **10627**, exc=Exception
- `silent_exception` en línea **12290**, exc=Exception
- `silent_exception` en línea **13461**, exc=Exception
- `silent_exception` en línea **14791**, exc=Exception
- `silent_exception` en línea **15162**, exc=Exception
- `silent_exception` en línea **17251**, exc=Exception
- `silent_exception` en línea **17308**, exc=Exception
- `silent_exception` en línea **19854**, exc=Exception
- `silent_exception` en línea **20666**, exc=Exception
- `silent_exception` en línea **20733**, exc=Exception
- `silent_exception` en línea **20763**, exc=Exception
- `silent_exception` en línea **23493**, exc=BaseException
- `silent_exception` en línea **23584**, exc=BaseException
- `silent_exception` en línea **24570**, exc=Exception
- `silent_exception` en línea **24628**, exc=Exception
- `silent_exception` en línea **2233**, exc=Exception
- `silent_exception` en línea **2280**, exc=Exception
- `silent_exception` en línea **2910**, exc=Exception
- `silent_exception` en línea **4606**, exc=Exception
- `silent_exception` en línea **4612**, exc=Exception
- `silent_exception` en línea **4711**, exc=Exception
- `silent_exception` en línea **7557**, exc=Exception
- `silent_exception` en línea **10049**, exc=Exception
- `silent_exception` en línea **10188**, exc=Exception
- `silent_exception` en línea **10224**, exc=Exception
- `silent_exception` en línea **10334**, exc=Exception
- `silent_exception` en línea **10338**, exc=Exception
- `silent_exception` en línea **10819**, exc=Exception
- `silent_exception` en línea **12678**, exc=Exception
- `silent_exception` en línea **13270**, exc=Exception
- `silent_exception` en línea **14009**, exc=BaseException
- `silent_exception` en línea **14787**, exc=Exception
- `silent_exception` en línea **15016**, exc=Exception
- `silent_exception` en línea **16224**, exc=BaseException

## Bloques más grandes (mantenibilidad)
- ClassDef `IQOptionBridge` líneas 9285-14063 (**4779** líneas)
- ClassDef `ConfiguracionDialog` líneas 18408-19810 (**1403** líneas)
- ClassDef `EstrategiaMultiTimeframe` líneas 5635-6911 (**1277** líneas)
- ClassDef `SeguimientoSenales` líneas 7520-8400 (**881** líneas)
- ClassDef `MarketMakerStrategy` líneas 4769-5628 (**860** líneas)
- ClassDef `AnalizadorMercado` líneas 15172-15987 (**816** líneas)
- ClassDef `ConfiguracionTrading` líneas 2542-3315 (**774** líneas)
- ClassDef `TelegramNotifier` líneas 15994-16684 (**691** líneas)
- ClassDef `MotorTradingIntegrado` líneas 1770-2432 (**663** líneas)
- ClassDef `AutoTrainer` líneas 8406-9062 (**657** líneas)

## Smoke tests funcionales (datos sintéticos)
- `skipped`: **True**
- `reason`: **numpy/pandas no disponibles en el entorno**

## Recomendaciones prioritarias
1. Evitar `FORCE_CONSOLE = True` hardcodeado para no anular los argumentos CLI.
2. Reducir bloques monolíticos (clases/métodos muy extensos) y extraer módulos por dominio.
3. Reemplazar `except Exception/BaseException: pass` por manejo explícito + logging contextual.
4. Eliminar imports duplicados y consolidar typing/import section para mejorar legibilidad.
