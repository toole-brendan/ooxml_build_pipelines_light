"""workbook_master_tam - Distributed Shipbuilding Master TAM workbook pipeline.

One workbook spanning all three programs - Virginia, Columbia (the former
"submarines" workbook, split by class) and DDG-51 (the former "ddg" workbook) -
plus the cross-program outsourcing-ceiling layer and a top portfolio summary.

Hybrid layout (chosen 2026-06-20): the submarine model carries Virginia/Columbia
as columns (it was already built that way); DDG keeps its own bespoke model; the
ceiling sheets already span all three. Tabs are grouped by FUNCTION (the engine
enforces group contiguity) with program as the inner axis. Each former workbook
is relocated into its own sub-package under sheets/ (submarines/ ddg/ ceiling/),
each with a thin _bind.py binding its namespaced extracted-data dir.

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; sheet modules import ``workbook_core.*`` directly.

Two dirs are put on sys.path so both packages import regardless of entry point:
  - the build dir (this package's parent, ``.../tam/master/``) so
    ``workbook_master_tam`` resolves;
  - the workspace root (five levels up) so ``workbook_core`` resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PROJECT_ROOT = str(_HERE.parents[1])   # projects/distributed_shipbuilding/tam/master/  (holds workbook_master_tam + build_workbook.py)
_CORE_DIR = str(_HERE.parents[5])       # workspace root                                 (holds workbook_core)

for _p in (_PROJECT_ROOT, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
