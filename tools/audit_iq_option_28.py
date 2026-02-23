#!/usr/bin/env python3
"""Auditoría técnica estática + smoke funcional para IQ_Opcion_IA_2.8.py."""
from __future__ import annotations

import ast
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import numpy as np
    import pandas as pd
    HAS_NUMPY_PANDAS = True
except Exception:
    HAS_NUMPY_PANDAS = False

TARGET = Path("IQ_Opcion_IA_2.8.py")
REPORT = Path("reports/auditoria_iq_opcion_2_8.md")
JSON_OUT = Path("reports/auditoria_iq_opcion_2_8.json")


def unparse_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{unparse_name(node.value)}.{node.attr}"
    return ast.dump(node, include_attributes=False)


def collect_imports(mod: ast.Module) -> list[str]:
    out: list[str] = []
    for n in mod.body:
        if isinstance(n, ast.Import):
            out.extend(a.name for a in n.names)
        elif isinstance(n, ast.ImportFrom):
            base = n.module or ""
            out.extend(f"{base}.{a.name}" for a in n.names)
    return out


def find_nodes(mod: ast.Module, typ: type[ast.AST]) -> list[ast.AST]:
    return [n for n in ast.walk(mod) if isinstance(n, typ)]


def function_spans(mod: ast.Module) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    for n in mod.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            end = getattr(n, "end_lineno", n.lineno)
            spans.append({"name": n.name, "kind": type(n).__name__, "lineno": n.lineno, "end_lineno": end, "size": end - n.lineno + 1})
    return sorted(spans, key=lambda x: x["size"], reverse=True)


def risk_flags(mod: ast.Module) -> list[dict[str, Any]]:
    flags: list[dict[str, Any]] = []
    for n in ast.walk(mod):
        if isinstance(n, ast.ExceptHandler):
            if n.type is None:
                flags.append({"type": "bare_except", "line": n.lineno})
            elif isinstance(n.type, ast.Name) and n.type.id in {"Exception", "BaseException"}:
                # detectar si solo hace pass
                if len(n.body) == 1 and isinstance(n.body[0], ast.Pass):
                    flags.append({"type": "silent_exception", "line": n.lineno, "exc": n.type.id})
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id == "FORCE_CONSOLE":
                    flags.append({"type": "hardcoded_console_mode", "line": n.lineno, "value": ast.unparse(n.value) if hasattr(ast, 'unparse') else 'N/A'})
    return flags


def extract_functions(mod: ast.Module, names: set[str]) -> dict[str, Any]:
    # Compilar únicamente funciones puras para smoke test sin importar todo el módulo.
    picked = [n for n in mod.body if isinstance(n, ast.FunctionDef) and n.name in names]
    picked_mod = ast.Module(body=picked, type_ignores=[])
    ast.fix_missing_locations(picked_mod)
    ns: dict[str, Any] = {"np": np, "pd": pd}
    code = compile(picked_mod, filename=str(TARGET), mode="exec")
    exec(code, ns)
    return ns


def run_smoke(mod: ast.Module) -> dict[str, Any]:
    if not HAS_NUMPY_PANDAS:
        return {"skipped": True, "reason": "numpy/pandas no disponibles en el entorno"}

    targets = {"_ema_series", "_rsi_series", "_atr_series", "_atr_last_from_arrays", "detectar_patron_wm"}
    ns = extract_functions(mod, targets)

    close = pd.Series(np.linspace(100, 120, 120))
    high = close + 0.5
    low = close - 0.5

    ema = ns["_ema_series"](close, 21)
    rsi = ns["_rsi_series"](close, 14)
    atr = ns["_atr_series"](high, low, close, 14)
    atr_last = ns["_atr_last_from_arrays"](high.values, low.values, close.values, 14)

    wm_input = np.concatenate([
        np.linspace(100, 90, 30),
        np.linspace(90, 105, 30),
        np.linspace(105, 92, 30),
        np.linspace(92, 108, 30),
    ])
    pattern = ns["detectar_patron_wm"](pd.Series(wm_input), window=120)

    checks = {
        "ema_has_nan": bool(ema.isna().any()),
        "rsi_range_ok": bool(((rsi.dropna() >= 0) & (rsi.dropna() <= 100)).all()),
        "atr_non_negative": bool((atr.dropna() >= 0).all()),
        "atr_last_positive": bool(atr_last >= 0),
        "wm_output_type": type(pattern).__name__,
    }
    return checks


def main() -> None:
    src = TARGET.read_text(encoding="utf-8")
    mod = ast.parse(src)

    imports = collect_imports(mod)
    import_counts = Counter(imports)
    dups = sorted([k for k, v in import_counts.items() if v > 1])

    spans = function_spans(mod)
    long_blocks = [s for s in spans if s["size"] >= 400][:10]

    flags = risk_flags(mod)
    smoke = run_smoke(mod)

    summary = {
        "file": str(TARGET),
        "total_lines": len(src.splitlines()),
        "top_level_defs": len([n for n in mod.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]),
        "imports_total": len(imports),
        "duplicate_imports": dups,
        "risk_flags": flags,
        "largest_blocks": long_blocks,
        "smoke_checks": smoke,
    }

    JSON_OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    md = []
    md.append("# Auditoría técnica — IQ_Opcion_IA_2.8.py")
    md.append("")
    md.append("## Resumen ejecutivo")
    md.append(f"- Líneas totales: **{summary['total_lines']}**")
    md.append(f"- Definiciones top-level (funciones/clases): **{summary['top_level_defs']}**")
    md.append(f"- Imports detectados: **{summary['imports_total']}**")
    md.append(f"- Imports duplicados: **{len(dups)}** → {', '.join(dups) if dups else 'ninguno'}")
    md.append("")
    md.append("## Hallazgos de riesgo (AST)")
    if flags:
        for f in flags[:80]:
            detail = f", exc={f.get('exc')}" if f.get("exc") else ""
            md.append(f"- `{f['type']}` en línea **{f['line']}**{detail}")
    else:
        md.append("- Sin banderas de riesgo en las reglas configuradas.")
    md.append("")
    md.append("## Bloques más grandes (mantenibilidad)")
    for b in long_blocks:
        md.append(f"- {b['kind']} `{b['name']}` líneas {b['lineno']}-{b['end_lineno']} (**{b['size']}** líneas)")
    if not long_blocks:
        md.append("- No hay bloques >= 400 líneas.")
    md.append("")
    md.append("## Smoke tests funcionales (datos sintéticos)")
    for k, v in smoke.items():
        md.append(f"- `{k}`: **{v}**")

    md.append("")
    md.append("## Recomendaciones prioritarias")
    md.append("1. Evitar `FORCE_CONSOLE = True` hardcodeado para no anular los argumentos CLI.")
    md.append("2. Reducir bloques monolíticos (clases/métodos muy extensos) y extraer módulos por dominio.")
    md.append("3. Reemplazar `except Exception/BaseException: pass` por manejo explícito + logging contextual.")
    md.append("4. Eliminar imports duplicados y consolidar typing/import section para mejorar legibilidad.")

    REPORT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Reportes generados: {REPORT} y {JSON_OUT}")


if __name__ == "__main__":
    main()
