"""deck_submarines_draft - DRAFT submarine deck pipeline (reviewed slide modules).

A second, parallel submarine deck pipeline that builds a DRAFT .pptx from the
reviewed slide modules under ``slides_draft/`` -- separate from the real
``deck_submarines`` pipeline so the two never clobber each other. It is wired
identically: the slide modules import the canonical shared engine ``deck_core.*``
directly, and binding lives in ``lib.py``. There is no vendored copy of the engine
inside this pipeline.

This module makes both packages importable regardless of entry point by putting
two dirs on sys.path:
  - the build dir (this package's parent, ``projects/distributed_shipbuilding/submarines/deck/``) so
    ``deck_submarines_draft`` resolves;
  - the workspace root (four levels up) so ``deck_core`` resolves.
When the build is launched via ``build_drafts.py`` the build dir is already
sys.path[0]; the workspace root is prepended here so the ``deck_core`` import
resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PROJECT_ROOT = str(_HERE.parents[1])   # projects/distributed_shipbuilding/submarines/deck/   (holds deck_submarines_draft + build_drafts.py)
_CORE_DIR = str(_HERE.parents[5])       # workspace root              (holds deck_core)

for _p in (_PROJECT_ROOT, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
