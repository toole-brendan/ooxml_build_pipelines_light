"""deck_consolidated - Distributed Shipbuilding Consolidated PowerPoint build pipeline.

Thin per-program package: binds the output path, the shared template + brand
assets, and the docProps identity (lib.py), and registers the slide modules
(slides/). The shared raw-OOXML engine is the canonical ``deck_core`` package at
the workspace root; the slide modules import ``deck_core.*`` directly. There is
no vendored copy of the engine inside this pipeline -- it imports the single
source of truth at ``<workspace root>/deck_core``.

This module makes both packages importable regardless of entry point by putting
two dirs on sys.path:
  - the build dir (this package's parent, ``projects/distributed_shipbuilding/deck/``) so
    ``deck_consolidated`` resolves;
  - the workspace root (four levels up) so ``deck_core`` resolves.
When the build is launched via ``build_deck.py`` the build dir is already
sys.path[0]; the workspace root is prepended here so the ``deck_core`` import
resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PROJECT_ROOT = str(_HERE.parents[1])   # projects/distributed_shipbuilding/deck/   (holds deck_consolidated + build_deck.py)
_CORE_DIR = str(_HERE.parents[5])       # workspace root                (holds deck_core)

for _p in (_PROJECT_ROOT, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
