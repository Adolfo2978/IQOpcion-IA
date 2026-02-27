# Auditoría técnica — IQ_Opcion_IA_2.8.py

## Resumen ejecutivo
- Líneas totales: **25072**
- Definiciones top-level (funciones/clases): **67**
- Imports detectados: **42**
- Imports duplicados: **6** → collections.deque, datetime.datetime, typing.Dict, typing.List, typing.Optional, typing.Tuple

## Hallazgos de riesgo (AST)
- `silent_exception` en línea **211**, exc=Exception
- `silent_exception` en línea **2161**, exc=Exception
- `silent_exception` en línea **2224**, exc=Exception
- `silent_exception` en línea **2954**, exc=Exception
- `silent_exception` en línea **3059**, exc=Exception
- `silent_exception` en línea **7306**, exc=Exception
- `silent_exception` en línea **8441**, exc=Exception
- `silent_exception` en línea **8464**, exc=Exception
- `silent_exception` en línea **8497**, exc=BaseException
- `silent_exception` en línea **8523**, exc=BaseException
- `silent_exception` en línea **9399**, exc=Exception
- `silent_exception` en línea **9513**, exc=Exception
- `silent_exception` en línea **9573**, exc=Exception
- `silent_exception` en línea **9622**, exc=Exception
- `silent_exception` en línea **10354**, exc=Exception
- `silent_exception` en línea **10362**, exc=Exception
- `silent_exception` en línea **10432**, exc=Exception
- `silent_exception` en línea **10451**, exc=Exception
- `silent_exception` en línea **10550**, exc=Exception
- `silent_exception` en línea **10571**, exc=Exception
- `silent_exception` en línea **10590**, exc=Exception
- `silent_exception` en línea **10793**, exc=Exception
- `silent_exception` en línea **14815**, exc=Exception
- `silent_exception` en línea **14887**, exc=Exception
- `silent_exception` en línea **14907**, exc=Exception
- `silent_exception` en línea **16325**, exc=Exception
- `silent_exception` en línea **16360**, exc=Exception
- `silent_exception` en línea **18751**, exc=Exception
- `silent_exception` en línea **19577**, exc=Exception
- `silent_exception` en línea **19583**, exc=Exception
- `silent_exception` en línea **23214**, exc=Exception
- `silent_exception` en línea **23861**, exc=BaseException
- `silent_exception` en línea **24558**, exc=Exception
- `silent_exception` en línea **24567**, exc=Exception
- `silent_exception` en línea **24583**, exc=Exception
- `silent_exception` en línea **24612**, exc=Exception
- `silent_exception` en línea **24869**, exc=Exception
- `silent_exception` en línea **24911**, exc=Exception
- `silent_exception` en línea **3438**, exc=Exception
- `silent_exception` en línea **3451**, exc=Exception
- `silent_exception` en línea **3461**, exc=Exception
- `silent_exception` en línea **8332**, exc=Exception
- `silent_exception` en línea **9727**, exc=Exception
- `silent_exception` en línea **10412**, exc=Exception
- `silent_exception` en línea **10416**, exc=Exception
- `silent_exception` en línea **10421**, exc=Exception
- `silent_exception` en línea **10425**, exc=Exception
- `silent_exception` en línea **10559**, exc=Exception
- `silent_exception` en línea **10609**, exc=Exception
- `silent_exception` en línea **10894**, exc=Exception
- `silent_exception` en línea **12557**, exc=Exception
- `silent_exception` en línea **13746**, exc=Exception
- `silent_exception` en línea **15081**, exc=Exception
- `silent_exception` en línea **15452**, exc=Exception
- `silent_exception` en línea **17541**, exc=Exception
- `silent_exception` en línea **17598**, exc=Exception
- `silent_exception` en línea **20144**, exc=Exception
- `silent_exception` en línea **20956**, exc=Exception
- `silent_exception` en línea **21023**, exc=Exception
- `silent_exception` en línea **21053**, exc=Exception
- `silent_exception` en línea **23783**, exc=BaseException
- `silent_exception` en línea **23874**, exc=BaseException
- `silent_exception` en línea **24860**, exc=Exception
- `silent_exception` en línea **24918**, exc=Exception
- `silent_exception` en línea **2359**, exc=Exception
- `silent_exception` en línea **2406**, exc=Exception
- `silent_exception` en línea **3057**, exc=Exception
- `silent_exception` en línea **4771**, exc=Exception
- `silent_exception` en línea **4777**, exc=Exception
- `silent_exception` en línea **4876**, exc=Exception
- `silent_exception` en línea **7728**, exc=Exception
- `silent_exception` en línea **10255**, exc=Exception
- `silent_exception` en línea **10394**, exc=Exception
- `silent_exception` en línea **10430**, exc=Exception
- `silent_exception` en línea **10599**, exc=Exception
- `silent_exception` en línea **10603**, exc=Exception
- `silent_exception` en línea **11086**, exc=Exception
- `silent_exception` en línea **12945**, exc=Exception
- `silent_exception` en línea **13540**, exc=Exception
- `silent_exception` en línea **14299**, exc=BaseException

## Bloques más grandes (mantenibilidad)
- ClassDef `IQOptionBridge` líneas 9456-14353 (**4898** líneas)
- ClassDef `ConfiguracionDialog` líneas 18698-20100 (**1403** líneas)
- ClassDef `EstrategiaMultiTimeframe` líneas 5800-7076 (**1277** líneas)
- ClassDef `SeguimientoSenales` líneas 7691-8571 (**881** líneas)
- ClassDef `MarketMakerStrategy` líneas 4934-5793 (**860** líneas)
- ClassDef `AnalizadorMercado` líneas 15462-16277 (**816** líneas)
- ClassDef `ConfiguracionTrading` líneas 2668-3462 (**795** líneas)
- ClassDef `MotorTradingIntegrado` líneas 1842-2558 (**717** líneas)
- ClassDef `TelegramNotifier` líneas 16284-16974 (**691** líneas)
- ClassDef `AutoTrainer` líneas 8577-9233 (**657** líneas)

## Smoke tests funcionales (datos sintéticos)
- `skipped`: **True**
- `reason`: **numpy/pandas no disponibles en el entorno**

## Recomendaciones prioritarias
1. Evitar `FORCE_CONSOLE = True` hardcodeado para no anular los argumentos CLI.
2. Reducir bloques monolíticos (clases/métodos muy extensos) y extraer módulos por dominio.
3. Reemplazar `except Exception/BaseException: pass` por manejo explícito + logging contextual.
4. Eliminar imports duplicados y consolidar typing/import section para mejorar legibilidad.
