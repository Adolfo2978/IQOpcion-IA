# Auditoría técnica — IQ_Opcion_IA_2.8.py

## Resumen ejecutivo
- Líneas totales: **24802**
- Definiciones top-level (funciones/clases): **67**
- Imports detectados: **41**
- Imports duplicados: **6** → collections.deque, datetime.datetime, typing.Dict, typing.List, typing.Optional, typing.Tuple

## Hallazgos de riesgo (AST)
- `silent_exception` en línea **203**, exc=Exception
- `silent_exception` en línea **2035**, exc=Exception
- `silent_exception` en línea **2098**, exc=Exception
- `silent_exception` en línea **2807**, exc=Exception
- `silent_exception` en línea **2912**, exc=Exception
- `silent_exception` en línea **7139**, exc=Exception
- `silent_exception` en línea **8274**, exc=Exception
- `silent_exception` en línea **8297**, exc=Exception
- `silent_exception` en línea **8330**, exc=BaseException
- `silent_exception` en línea **8356**, exc=BaseException
- `silent_exception` en línea **9232**, exc=Exception
- `silent_exception` en línea **9346**, exc=Exception
- `silent_exception` en línea **9397**, exc=Exception
- `silent_exception` en línea **10153**, exc=Exception
- `silent_exception` en línea **10161**, exc=Exception
- `silent_exception` en línea **10231**, exc=Exception
- `silent_exception` en línea **10312**, exc=Exception
- `silent_exception` en línea **10331**, exc=Exception
- `silent_exception` en línea **10531**, exc=Exception
- `silent_exception` en línea **14545**, exc=Exception
- `silent_exception` en línea **14617**, exc=Exception
- `silent_exception` en línea **14637**, exc=Exception
- `silent_exception` en línea **16055**, exc=Exception
- `silent_exception` en línea **16090**, exc=Exception
- `silent_exception` en línea **18481**, exc=Exception
- `silent_exception` en línea **19307**, exc=Exception
- `silent_exception` en línea **19313**, exc=Exception
- `silent_exception` en línea **22944**, exc=Exception
- `silent_exception` en línea **23591**, exc=BaseException
- `silent_exception` en línea **24288**, exc=Exception
- `silent_exception` en línea **24297**, exc=Exception
- `silent_exception` en línea **24313**, exc=Exception
- `silent_exception` en línea **24342**, exc=Exception
- `silent_exception` en línea **24599**, exc=Exception
- `silent_exception` en línea **24641**, exc=Exception
- `silent_exception` en línea **3291**, exc=Exception
- `silent_exception` en línea **3304**, exc=Exception
- `silent_exception` en línea **3314**, exc=Exception
- `silent_exception` en línea **8165**, exc=Exception
- `silent_exception` en línea **9527**, exc=Exception
- `silent_exception` en línea **10211**, exc=Exception
- `silent_exception` en línea **10215**, exc=Exception
- `silent_exception` en línea **10220**, exc=Exception
- `silent_exception` en línea **10224**, exc=Exception
- `silent_exception` en línea **10300**, exc=Exception
- `silent_exception` en línea **10349**, exc=Exception
- `silent_exception` en línea **10632**, exc=Exception
- `silent_exception` en línea **12295**, exc=Exception
- `silent_exception` en línea **13481**, exc=Exception
- `silent_exception` en línea **14811**, exc=Exception
- `silent_exception` en línea **15182**, exc=Exception
- `silent_exception` en línea **17271**, exc=Exception
- `silent_exception` en línea **17328**, exc=Exception
- `silent_exception` en línea **19874**, exc=Exception
- `silent_exception` en línea **20686**, exc=Exception
- `silent_exception` en línea **20753**, exc=Exception
- `silent_exception` en línea **20783**, exc=Exception
- `silent_exception` en línea **23513**, exc=BaseException
- `silent_exception` en línea **23604**, exc=BaseException
- `silent_exception` en línea **24590**, exc=Exception
- `silent_exception` en línea **24648**, exc=Exception
- `silent_exception` en línea **2233**, exc=Exception
- `silent_exception` en línea **2280**, exc=Exception
- `silent_exception` en línea **2910**, exc=Exception
- `silent_exception` en línea **4610**, exc=Exception
- `silent_exception` en línea **4616**, exc=Exception
- `silent_exception` en línea **4715**, exc=Exception
- `silent_exception` en línea **7561**, exc=Exception
- `silent_exception` en línea **10054**, exc=Exception
- `silent_exception` en línea **10193**, exc=Exception
- `silent_exception` en línea **10229**, exc=Exception
- `silent_exception` en línea **10339**, exc=Exception
- `silent_exception` en línea **10343**, exc=Exception
- `silent_exception` en línea **10824**, exc=Exception
- `silent_exception` en línea **12683**, exc=Exception
- `silent_exception` en línea **13275**, exc=Exception
- `silent_exception` en línea **14029**, exc=BaseException
- `silent_exception` en línea **14807**, exc=Exception
- `silent_exception` en línea **15036**, exc=Exception
- `silent_exception` en línea **16244**, exc=BaseException

## Bloques más grandes (mantenibilidad)
- ClassDef `IQOptionBridge` líneas 9289-14083 (**4795** líneas)
- ClassDef `ConfiguracionDialog` líneas 18428-19830 (**1403** líneas)
- ClassDef `EstrategiaMultiTimeframe` líneas 5639-6915 (**1277** líneas)
- ClassDef `SeguimientoSenales` líneas 7524-8404 (**881** líneas)
- ClassDef `MarketMakerStrategy` líneas 4773-5632 (**860** líneas)
- ClassDef `AnalizadorMercado` líneas 15192-16007 (**816** líneas)
- ClassDef `ConfiguracionTrading` líneas 2542-3315 (**774** líneas)
- ClassDef `TelegramNotifier` líneas 16014-16704 (**691** líneas)
- ClassDef `MotorTradingIntegrado` líneas 1770-2432 (**663** líneas)
- ClassDef `AutoTrainer` líneas 8410-9066 (**657** líneas)

## Smoke tests funcionales (datos sintéticos)
- `skipped`: **True**
- `reason`: **numpy/pandas no disponibles en el entorno**

## Recomendaciones prioritarias
1. Evitar `FORCE_CONSOLE = True` hardcodeado para no anular los argumentos CLI.
2. Reducir bloques monolíticos (clases/métodos muy extensos) y extraer módulos por dominio.
3. Reemplazar `except Exception/BaseException: pass` por manejo explícito + logging contextual.
4. Eliminar imports duplicados y consolidar typing/import section para mejorar legibilidad.
