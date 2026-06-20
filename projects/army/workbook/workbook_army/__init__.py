"""workbook_army - U.S. Army Market Mapping workbook build pipeline.

Thin per-program package: binds the output path, the extracted-data dir, and the
docProps identity (lib.py), and registers the sheet modules (sheets/). The shared
raw-OOXML engine is the canonical ``workbook_core`` package at the workspace root;
the sheet modules import ``workbook_core.*`` directly. There is no vendored copy
of workbook_core inside this pipeline -- it imports the single source of truth at
``<workspace root>/workbook_core``.

This module makes both packages importable regardless of entry point by putting
two dirs on sys.path:
  - the build dir (this package's parent, ``projects/army/workbook/``) so
    ``workbook_army`` resolves;
  - the workspace root (four levels up) so ``workbook_core`` resolves.
When the build is launched via ``build_workbook.py`` the build dir is already
sys.path[0]; the workspace root is prepended here so the ``workbook_core`` import
resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PROJECT_ROOT = str(_HERE.parents[1])   # projects/army/workbook/   (holds workbook_army + build_workbook.py)
_CORE_DIR = str(_HERE.parents[4])       # workspace root            (holds workbook_core)

for _p in (_PROJECT_ROOT, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
