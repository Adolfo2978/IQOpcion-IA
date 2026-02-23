# Auditoría técnica — IQ_Opcion_IA_2.8.py

## Resumen ejecutivo
- Líneas totales: **24775**
- Definiciones top-level (funciones/clases): **67**
- Imports detectados: **41**
- Imports duplicados: **6** → collections.deque, datetime.datetime, typing.Dict, typing.List, typing.Optional, typing.Tuple

## Hallazgos de riesgo (AST)
- `hardcoded_console_mode` en línea **63**
- `silent_exception` en línea **160**, exc=Exception
- `hardcoded_console_mode` en línea **24709**
- `silent_exception` en línea **106**, exc=Exception
- `silent_exception` en línea **138**, exc=Exception
- `hardcoded_console_mode` en línea **24716**
- `silent_exception` en línea **205**, exc=Exception
- `silent_exception` en línea **2037**, exc=Exception
- `silent_exception` en línea **2100**, exc=Exception
- `silent_exception` en línea **2809**, exc=Exception
- `silent_exception` en línea **2914**, exc=Exception
- `silent_exception` en línea **7137**, exc=Exception
- `silent_exception` en línea **8272**, exc=Exception
- `silent_exception` en línea **8295**, exc=Exception
- `silent_exception` en línea **8328**, exc=BaseException
- `silent_exception` en línea **8354**, exc=BaseException
- `silent_exception` en línea **9230**, exc=Exception
- `silent_exception` en línea **9344**, exc=Exception
- `silent_exception` en línea **9395**, exc=Exception
- `silent_exception` en línea **10150**, exc=Exception
- `silent_exception` en línea **10158**, exc=Exception
- `silent_exception` en línea **10228**, exc=Exception
- `silent_exception` en línea **10309**, exc=Exception
- `silent_exception` en línea **10328**, exc=Exception
- `silent_exception` en línea **10528**, exc=Exception
- `silent_exception` en línea **14527**, exc=Exception
- `silent_exception` en línea **14599**, exc=Exception
- `silent_exception` en línea **14619**, exc=Exception
- `silent_exception` en línea **16037**, exc=Exception
- `silent_exception` en línea **16072**, exc=Exception
- `silent_exception` en línea **18463**, exc=Exception
- `silent_exception` en línea **19289**, exc=Exception
- `silent_exception` en línea **19295**, exc=Exception
- `silent_exception` en línea **22926**, exc=Exception
- `silent_exception` en línea **23573**, exc=BaseException
- `silent_exception` en línea **24270**, exc=Exception
- `silent_exception` en línea **24279**, exc=Exception
- `silent_exception` en línea **24295**, exc=Exception
- `silent_exception` en línea **24324**, exc=Exception
- `silent_exception` en línea **24581**, exc=Exception
- `silent_exception` en línea **24623**, exc=Exception
- `silent_exception` en línea **3293**, exc=Exception
- `silent_exception` en línea **3306**, exc=Exception
- `silent_exception` en línea **3316**, exc=Exception
- `silent_exception` en línea **8163**, exc=Exception
- `silent_exception` en línea **9525**, exc=Exception
- `silent_exception` en línea **10208**, exc=Exception
- `silent_exception` en línea **10212**, exc=Exception
- `silent_exception` en línea **10217**, exc=Exception
- `silent_exception` en línea **10221**, exc=Exception
- `silent_exception` en línea **10297**, exc=Exception
- `silent_exception` en línea **10346**, exc=Exception
- `silent_exception` en línea **10629**, exc=Exception
- `silent_exception` en línea **12292**, exc=Exception
- `silent_exception` en línea **13463**, exc=Exception
- `silent_exception` en línea **14793**, exc=Exception
- `silent_exception` en línea **15164**, exc=Exception
- `silent_exception` en línea **17253**, exc=Exception
- `silent_exception` en línea **17310**, exc=Exception
- `silent_exception` en línea **19856**, exc=Exception
- `silent_exception` en línea **20668**, exc=Exception
- `silent_exception` en línea **20735**, exc=Exception
- `silent_exception` en línea **20765**, exc=Exception
- `silent_exception` en línea **23495**, exc=BaseException
- `silent_exception` en línea **23586**, exc=BaseException
- `silent_exception` en línea **24572**, exc=Exception
- `silent_exception` en línea **24630**, exc=Exception
- `silent_exception` en línea **24728**, exc=Exception
- `silent_exception` en línea **24752**, exc=BaseException
- `silent_exception` en línea **2235**, exc=Exception
- `silent_exception` en línea **2282**, exc=Exception
- `silent_exception` en línea **2912**, exc=Exception
- `silent_exception` en línea **4608**, exc=Exception
- `silent_exception` en línea **4614**, exc=Exception
- `silent_exception` en línea **4713**, exc=Exception
- `silent_exception` en línea **7559**, exc=Exception
- `silent_exception` en línea **10051**, exc=Exception
- `silent_exception` en línea **10190**, exc=Exception
- `silent_exception` en línea **10226**, exc=Exception
- `silent_exception` en línea **10336**, exc=Exception

## Bloques más grandes (mantenibilidad)
- ClassDef `IQOptionBridge` líneas 9287-14065 (**4779** líneas)
- ClassDef `ConfiguracionDialog` líneas 18410-19812 (**1403** líneas)
- ClassDef `EstrategiaMultiTimeframe` líneas 5637-6913 (**1277** líneas)
- ClassDef `SeguimientoSenales` líneas 7522-8402 (**881** líneas)
- ClassDef `MarketMakerStrategy` líneas 4771-5630 (**860** líneas)
- ClassDef `AnalizadorMercado` líneas 15174-15989 (**816** líneas)
- ClassDef `ConfiguracionTrading` líneas 2544-3317 (**774** líneas)
- ClassDef `TelegramNotifier` líneas 15996-16686 (**691** líneas)
- ClassDef `MotorTradingIntegrado` líneas 1772-2434 (**663** líneas)
- ClassDef `AutoTrainer` líneas 8408-9064 (**657** líneas)

## Smoke tests funcionales (datos sintéticos)
- `skipped`: **True**
- `reason`: **numpy/pandas no disponibles en el entorno**

## Recomendaciones prioritarias
1. Evitar `FORCE_CONSOLE = True` hardcodeado para no anular los argumentos CLI.
2. Reducir bloques monolíticos (clases/métodos muy extensos) y extraer módulos por dominio.
3. Reemplazar `except Exception/BaseException: pass` por manejo explícito + logging contextual.
4. Eliminar imports duplicados y consolidar typing/import section para mejorar legibilidad.
