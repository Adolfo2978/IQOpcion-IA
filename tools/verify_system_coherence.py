#!/usr/bin/env python3
"""Verificación de coherencia del sistema (modo offline/sin broker)."""
from __future__ import annotations

import ast
import json
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List

TARGET = Path('IQ_Opcion_IA_2.8.py')


def _load_class(name: str, extra_ns: dict):
    mod = ast.parse(TARGET.read_text(encoding='utf-8'))
    cls = next(n for n in mod.body if isinstance(n, ast.ClassDef) and n.name == name)
    m = ast.Module(body=[cls], type_ignores=[])
    ast.fix_missing_locations(m)
    ns = dict(extra_ns)
    exec(compile(m, str(TARGET), 'exec'), ns)
    return ns[name]


def check_dependencies() -> dict:
    out = {}
    for m in ('numpy', 'pandas', 'sklearn'):
        try:
            __import__(m)
            out[m] = True
        except Exception:
            out[m] = False
    return out


def check_operations_repository() -> dict:
    Repo = _load_class('OperationsRepository', {
        'os': os,
        'json': json,
        'datetime': datetime,
        'List': List,
        'logger': logging.getLogger('verify'),
    })
    with tempfile.TemporaryDirectory() as td:
        repo = Repo(str(Path(td) / 'trades.json'))
        base = {'simbolo': 'EURUSD', 'direccion': 'CALL', 'indicadores': {'RSI': 55, 'stoch_k': 45}}
        repo.agregar_trade(base, True)
        repo.agregar_trade(base, False)
        repo.agregar_trade(base, None)
        stats = repo.obtener_estadisticas()
        return {
            'total_trades': stats.get('total_trades', -1),
            'wins': stats.get('trades_exitosos', -1),
            'losses': int(stats.get('total_trades', 0) - stats.get('trades_exitosos', 0)),
            'pending_ignored': stats.get('total_trades', -1) == 2,
        }


def check_sync_hooks() -> dict:
    src = TARGET.read_text(encoding='utf-8')
    mod = ast.parse(src)

    forced_literal = False
    for n in mod.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id == 'FORCE_CONSOLE':
                    if isinstance(n.value, ast.Constant) and n.value.value is True:
                        forced_literal = True

    return {
        'register_trade_context_call': 'register_trade_context(' in src,
        'feedback_uses_order_id': 'trade_id=order_id' in src,
        'startup_not_forced_console_literal': not forced_literal,
    }


def main() -> None:
    deps = check_dependencies()
    repo = check_operations_repository()
    hooks = check_sync_hooks()

    ok_repo = (repo['total_trades'] == 2 and repo['wins'] == 1 and repo['losses'] == 1 and repo['pending_ignored'])
    ok_hooks = all(hooks.values())

    report = {
        'dependencies': deps,
        'operations_repository': repo,
        'sync_hooks': hooks,
        'status': {
            'repository_ok': ok_repo,
            'hooks_ok': ok_hooks,
            'overall_offline_ok': bool(ok_repo and ok_hooks),
        }
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not (ok_repo and ok_hooks):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
