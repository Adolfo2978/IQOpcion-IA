# Auditoría técnica — IQ_Opcion_IA_2.8.py

## Resumen ejecutivo
- Líneas totales: **24801**
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
- `silent_exception` en línea **10152**, exc=Exception
- `silent_exception` en línea **10160**, exc=Exception
- `silent_exception` en línea **10230**, exc=Exception
- `silent_exception` en línea **10311**, exc=Exception
- `silent_exception` en línea **10330**, exc=Exception
- `silent_exception` en línea **10530**, exc=Exception
- `silent_exception` en línea **14544**, exc=Exception
- `silent_exception` en línea **14616**, exc=Exception
- `silent_exception` en línea **14636**, exc=Exception
- `silent_exception` en línea **16054**, exc=Exception
- `silent_exception` en línea **16089**, exc=Exception
- `silent_exception` en línea **18480**, exc=Exception
- `silent_exception` en línea **19306**, exc=Exception
- `silent_exception` en línea **19312**, exc=Exception
- `silent_exception` en línea **22943**, exc=Exception
- `silent_exception` en línea **23590**, exc=BaseException
- `silent_exception` en línea **24287**, exc=Exception
- `silent_exception` en línea **24296**, exc=Exception
- `silent_exception` en línea **24312**, exc=Exception
- `silent_exception` en línea **24341**, exc=Exception
- `silent_exception` en línea **24598**, exc=Exception
- `silent_exception` en línea **24640**, exc=Exception
- `silent_exception` en línea **3291**, exc=Exception
- `silent_exception` en línea **3304**, exc=Exception
- `silent_exception` en línea **3314**, exc=Exception
- `silent_exception` en línea **8165**, exc=Exception
- `silent_exception` en línea **9527**, exc=Exception
- `silent_exception` en línea **10210**, exc=Exception
- `silent_exception` en línea **10214**, exc=Exception
- `silent_exception` en línea **10219**, exc=Exception
- `silent_exception` en línea **10223**, exc=Exception
- `silent_exception` en línea **10299**, exc=Exception
- `silent_exception` en línea **10348**, exc=Exception
- `silent_exception` en línea **10631**, exc=Exception
- `silent_exception` en línea **12294**, exc=Exception
- `silent_exception` en línea **13480**, exc=Exception
- `silent_exception` en línea **14810**, exc=Exception
- `silent_exception` en línea **15181**, exc=Exception
- `silent_exception` en línea **17270**, exc=Exception
- `silent_exception` en línea **17327**, exc=Exception
- `silent_exception` en línea **19873**, exc=Exception
- `silent_exception` en línea **20685**, exc=Exception
- `silent_exception` en línea **20752**, exc=Exception
- `silent_exception` en línea **20782**, exc=Exception
- `silent_exception` en línea **23512**, exc=BaseException
- `silent_exception` en línea **23603**, exc=BaseException
- `silent_exception` en línea **24589**, exc=Exception
- `silent_exception` en línea **24647**, exc=Exception
- `silent_exception` en línea **2233**, exc=Exception
- `silent_exception` en línea **2280**, exc=Exception
- `silent_exception` en línea **2910**, exc=Exception
- `silent_exception` en línea **4610**, exc=Exception
- `silent_exception` en línea **4616**, exc=Exception
- `silent_exception` en línea **4715**, exc=Exception
- `silent_exception` en línea **7561**, exc=Exception
- `silent_exception` en línea **10053**, exc=Exception
- `silent_exception` en línea **10192**, exc=Exception
- `silent_exception` en línea **10228**, exc=Exception
- `silent_exception` en línea **10338**, exc=Exception
- `silent_exception` en línea **10342**, exc=Exception
- `silent_exception` en línea **10823**, exc=Exception
- `silent_exception` en línea **12682**, exc=Exception
- `silent_exception` en línea **13274**, exc=Exception
- `silent_exception` en línea **14028**, exc=BaseException
- `silent_exception` en línea **14806**, exc=Exception
- `silent_exception` en línea **15035**, exc=Exception
- `silent_exception` en línea **16243**, exc=BaseException

## Bloques más grandes (mantenibilidad)
- ClassDef `IQOptionBridge` líneas 9289-14082 (**4794** líneas)
- ClassDef `ConfiguracionDialog` líneas 18427-19829 (**1403** líneas)
- ClassDef `EstrategiaMultiTimeframe` líneas 5639-6915 (**1277** líneas)
- ClassDef `SeguimientoSenales` líneas 7524-8404 (**881** líneas)
- ClassDef `MarketMakerStrategy` líneas 4773-5632 (**860** líneas)
- ClassDef `AnalizadorMercado` líneas 15191-16006 (**816** líneas)
- ClassDef `ConfiguracionTrading` líneas 2542-3315 (**774** líneas)
- ClassDef `TelegramNotifier` líneas 16013-16703 (**691** líneas)
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
