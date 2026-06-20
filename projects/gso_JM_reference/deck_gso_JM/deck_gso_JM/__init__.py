"""deck_gso_JM - GS&O "Strategy Materials Style Guide" faithful-port pipeline.

A 1:1 native port of the 5-slide GS&O style-guide deck
(20260615_GS&O_Strategy Materials Style Guide.pptx) onto the shared
``deck_core`` engine, following docs/faithful_deck_port_methodology.md. The deck
is a style reference: each slide is a worked example of one exhibit archetype
(bridge charts, bar charts, tables, flow charts), annotated in the source with
floating ``JM:`` reviewer directives. Those directives are build-process meta;
they are NOT rendered (see JM_style_notes.md at the build-dir root, which
captures them verbatim for the style-system reconciliation pass).

Thin per-deck package: binds the output path, the shared template + brand assets,
and the docProps identity (lib.py), and registers the slide modules (slides/).
The raw-OOXML engine is the canonical ``deck_core`` package at the workspace
root; the slide modules import ``deck_core.*`` directly. No vendored engine copy.

Two dirs go on sys.path so both packages resolve regardless of entry point:
  - the build dir (this package's parent) so ``deck_gso_JM`` resolves;
  - the workspace root (four levels up) so ``deck_core`` resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_BUILD_DIR = str(_HERE.parents[1])   # projects/gso_JM_reference/deck_gso_JM/
_CORE_DIR = str(_HERE.parents[4])    # workspace root (holds deck_core)

for _p in (_BUILD_DIR, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
