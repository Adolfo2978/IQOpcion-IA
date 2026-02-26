#!/usr/bin/env python3
"""Checks de coherencia: repositorio de trades + sincronía IA feedback."""
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


def load_operations_repo_class():
    mod = ast.parse(TARGET.read_text(encoding='utf-8'))
    cls = next(n for n in mod.body if isinstance(n, ast.ClassDef) and n.name == 'OperationsRepository')
    m = ast.Module(body=[cls], type_ignores=[])
    ast.fix_missing_locations(m)
    ns = {
        'os': os,
        'json': json,
        'datetime': datetime,
        'List': List,
        'logger': logging.getLogger('check'),
    }
    exec(compile(m, str(TARGET), 'exec'), ns)
    return ns['OperationsRepository']


def assert_repo_balanced_storage() -> None:
    Repo = load_operations_repo_class()
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / 'trades.json'
        repo = Repo(str(db))

        base = {'simbolo': 'EURUSD', 'direccion': 'CALL', 'indicadores': {'RSI': 55}}
        repo.agregar_trade(base, True)
        repo.agregar_trade(base, False)
        repo.agregar_trade(base, None)  # pendiente: no debe persistirse

        stats = repo.obtener_estadisticas()
        assert stats['total_trades'] == 2, stats
        assert stats['trades_exitosos'] == 1, stats
        assert len(repo.obtener_trades_exitosos()) == 1


def assert_sync_hooks_present() -> None:
    src = TARGET.read_text(encoding='utf-8')
    assert 'register_trade_context(' in src, 'Falta registro de contexto por order_id'
    assert 'trade_id=order_id' in src, 'Falta feedback IA asociado al order_id real'


def main() -> None:
    assert_repo_balanced_storage()
    assert_sync_hooks_present()
    print('OK: coherencia de autoaprendizaje y sincronización IA validada')


if __name__ == '__main__':
    main()
