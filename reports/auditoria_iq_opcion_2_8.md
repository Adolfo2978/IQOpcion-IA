# Auditoría técnica — IQ_Opcion_IA_2.8.py

## Resumen ejecutivo
- Líneas totales: **25016**
- Definiciones top-level (funciones/clases): **67**
- Imports detectados: **42**
- Imports duplicados: **6** → collections.deque, datetime.datetime, typing.Dict, typing.List, typing.Optional, typing.Tuple

## Hallazgos de riesgo (AST)
- `silent_exception` en línea **211**, exc=Exception
- `silent_exception` en línea **2146**, exc=Exception
- `silent_exception` en línea **2209**, exc=Exception
- `silent_exception` en línea **2934**, exc=Exception
- `silent_exception` en línea **3039**, exc=Exception
- `silent_exception` en línea **7280**, exc=Exception
- `silent_exception` en línea **8415**, exc=Exception
- `silent_exception` en línea **8438**, exc=Exception
- `silent_exception` en línea **8471**, exc=BaseException
- `silent_exception` en línea **8497**, exc=BaseException
- `silent_exception` en línea **9373**, exc=Exception
- `silent_exception` en línea **9487**, exc=Exception
- `silent_exception` en línea **9545**, exc=Exception
- `silent_exception` en línea **10301**, exc=Exception
- `silent_exception` en línea **10309**, exc=Exception
- `silent_exception` en línea **10379**, exc=Exception
- `silent_exception` en línea **10398**, exc=Exception
- `silent_exception` en línea **10497**, exc=Exception
- `silent_exception` en línea **10518**, exc=Exception
- `silent_exception` en línea **10537**, exc=Exception
- `silent_exception` en línea **10740**, exc=Exception
- `silent_exception` en línea **14759**, exc=Exception
- `silent_exception` en línea **14831**, exc=Exception
- `silent_exception` en línea **14851**, exc=Exception
- `silent_exception` en línea **16269**, exc=Exception
- `silent_exception` en línea **16304**, exc=Exception
- `silent_exception` en línea **18695**, exc=Exception
- `silent_exception` en línea **19521**, exc=Exception
- `silent_exception` en línea **19527**, exc=Exception
- `silent_exception` en línea **23158**, exc=Exception
- `silent_exception` en línea **23805**, exc=BaseException
- `silent_exception` en línea **24502**, exc=Exception
- `silent_exception` en línea **24511**, exc=Exception
- `silent_exception` en línea **24527**, exc=Exception
- `silent_exception` en línea **24556**, exc=Exception
- `silent_exception` en línea **24813**, exc=Exception
- `silent_exception` en línea **24855**, exc=Exception
- `silent_exception` en línea **3418**, exc=Exception
- `silent_exception` en línea **3431**, exc=Exception
- `silent_exception` en línea **3441**, exc=Exception
- `silent_exception` en línea **8306**, exc=Exception
- `silent_exception` en línea **9675**, exc=Exception
- `silent_exception` en línea **10359**, exc=Exception
- `silent_exception` en línea **10363**, exc=Exception
- `silent_exception` en línea **10368**, exc=Exception
- `silent_exception` en línea **10372**, exc=Exception
- `silent_exception` en línea **10506**, exc=Exception
- `silent_exception` en línea **10556**, exc=Exception
- `silent_exception` en línea **10841**, exc=Exception
- `silent_exception` en línea **12504**, exc=Exception
- `silent_exception` en línea **13690**, exc=Exception
- `silent_exception` en línea **15025**, exc=Exception
- `silent_exception` en línea **15396**, exc=Exception
- `silent_exception` en línea **17485**, exc=Exception
- `silent_exception` en línea **17542**, exc=Exception
- `silent_exception` en línea **20088**, exc=Exception
- `silent_exception` en línea **20900**, exc=Exception
- `silent_exception` en línea **20967**, exc=Exception
- `silent_exception` en línea **20997**, exc=Exception
- `silent_exception` en línea **23727**, exc=BaseException
- `silent_exception` en línea **23818**, exc=BaseException
- `silent_exception` en línea **24804**, exc=Exception
- `silent_exception` en línea **24862**, exc=Exception
- `silent_exception` en línea **2344**, exc=Exception
- `silent_exception` en línea **2391**, exc=Exception
- `silent_exception` en línea **3037**, exc=Exception
- `silent_exception` en línea **4751**, exc=Exception
- `silent_exception` en línea **4757**, exc=Exception
- `silent_exception` en línea **4856**, exc=Exception
- `silent_exception` en línea **7702**, exc=Exception
- `silent_exception` en línea **10202**, exc=Exception
- `silent_exception` en línea **10341**, exc=Exception
- `silent_exception` en línea **10377**, exc=Exception
- `silent_exception` en línea **10546**, exc=Exception
- `silent_exception` en línea **10550**, exc=Exception
- `silent_exception` en línea **11033**, exc=Exception
- `silent_exception` en línea **12892**, exc=Exception
- `silent_exception` en línea **13484**, exc=Exception
- `silent_exception` en línea **14243**, exc=BaseException
- `silent_exception` en línea **15021**, exc=Exception

## Bloques más grandes (mantenibilidad)
- ClassDef `IQOptionBridge` líneas 9430-14297 (**4868** líneas)
- ClassDef `ConfiguracionDialog` líneas 18642-20044 (**1403** líneas)
- ClassDef `EstrategiaMultiTimeframe` líneas 5780-7056 (**1277** líneas)
- ClassDef `SeguimientoSenales` líneas 7665-8545 (**881** líneas)
- ClassDef `MarketMakerStrategy` líneas 4914-5773 (**860** líneas)
- ClassDef `AnalizadorMercado` líneas 15406-16221 (**816** líneas)
- ClassDef `ConfiguracionTrading` líneas 2653-3442 (**790** líneas)
- ClassDef `MotorTradingIntegrado` líneas 1827-2543 (**717** líneas)
- ClassDef `TelegramNotifier` líneas 16228-16918 (**691** líneas)
- ClassDef `AutoTrainer` líneas 8551-9207 (**657** líneas)

## Smoke tests funcionales (datos sintéticos)
- `skipped`: **True**
- `reason`: **numpy/pandas no disponibles en el entorno**

## Recomendaciones prioritarias
1. Evitar `FORCE_CONSOLE = True` hardcodeado para no anular los argumentos CLI.
2. Reducir bloques monolíticos (clases/métodos muy extensos) y extraer módulos por dominio.
3. Reemplazar `except Exception/BaseException: pass` por manejo explícito + logging contextual.
4. Eliminar imports duplicados y consolidar typing/import section para mejorar legibilidad.
