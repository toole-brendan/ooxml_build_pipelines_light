"""doc_army - U.S. Army Market Mapping Word build pipeline.

Thin per-program package: binds the output path and the docProps identity
(lib.py), and registers the page modules (pages/). The shared raw-OOXML engine is
the canonical ``docx_core`` package at the workspace root; the page modules import
``docx_core.*`` directly. There is no vendored copy of the engine inside this
pipeline -- it imports the single source of truth at ``<workspace root>/docx_core``.

This module makes both packages importable regardless of entry point by putting
two dirs on sys.path:
  - the build dir (this package's parent, ``projects/army/doc/``)
    so ``doc_army`` resolves;
  - the workspace root (four levels up) so ``docx_core`` resolves.
When the build is launched via ``build_doc.py`` the build dir is already
sys.path[0]; the workspace root is prepended here so the ``docx_core`` import
resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PROJECT_ROOT = str(_HERE.parents[1])   # projects/army/doc/   (holds doc_army + build_doc.py)
_CORE_DIR = str(_HERE.parents[4])       # workspace root       (holds docx_core)

for _p in (_PROJECT_ROOT, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
