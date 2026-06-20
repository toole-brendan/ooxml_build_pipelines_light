"""doc_outsourced_ceiling - Outsourcing Ceiling methodology Word build pipeline.

Thin per-document package mirroring ``doc_distributed_shipbuilding``: it binds the
output path and the docProps identity (lib.py) and registers the page modules
(pages/). The shared raw-OOXML engine is the canonical ``docx_core`` package at the
workspace root; the page modules import ``docx_core.*`` directly. There is no
vendored copy of the engine inside this pipeline -- it imports the single source of
truth at ``<workspace root>/docx_core``.

This module makes both packages importable regardless of entry point by putting
two dirs on sys.path:
  - the build dir (this package's parent, ``projects/distributed_shipbuilding/doc/``)
    so ``doc_outsourced_ceiling`` resolves;
  - the workspace root (four levels up) so ``docx_core`` resolves.
When the build is launched via ``build_outsourced_ceiling.py`` the build dir is
already sys.path[0]; the workspace root is prepended here so the ``docx_core``
import resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PROJECT_ROOT = str(_HERE.parents[1])   # projects/distributed_shipbuilding/doc/   (holds doc_outsourced_ceiling + build_outsourced_ceiling.py)
_CORE_DIR = str(_HERE.parents[4])       # workspace root                          (holds docx_core)

for _p in (_PROJECT_ROOT, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
