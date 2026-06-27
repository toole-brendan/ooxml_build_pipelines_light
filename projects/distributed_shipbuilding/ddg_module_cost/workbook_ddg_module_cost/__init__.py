"""workbook_ddg_module_cost - standalone DDG-51 "cost per module" workbook.

A small, self-contained workbook that estimates the cost of a DDG-51 structural
"module" / "grand block" / "unit" by allocating a per-ship construction-cost
anchor down the modular build hierarchy HII (Ingalls) describes:

    1 ship -> 4 modules (hull 1/2/3 + deckhouse) -> 21 grand blocks -> 72 units

It is a transparent TOP-DOWN allocation (no public block-level cost exists). The
per-ship anchor is Basic Construction, mirrored from the Master TAM workbook's
DDG-51 SCN-budget slice (so the two stay coherent); the structural counts come
verbatim from HII's site.

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; sheet modules import ``workbook_core.*`` directly.

Two dirs go on sys.path so both packages import regardless of entry point:
  - the build dir (this package's parent, ``.../ddg_module_cost/``) so
    ``workbook_ddg_module_cost`` resolves;
  - the workspace root (four levels up) so ``workbook_core`` resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PROJECT_ROOT = str(_HERE.parents[1])   # projects/distributed_shipbuilding/ddg_module_cost/
_CORE_DIR = str(_HERE.parents[4])       # workspace root (holds workbook_core)

for _p in (_PROJECT_ROOT, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
