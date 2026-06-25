#!/usr/bin/env python3
"""Launcher for the deck_commercial_strategy reference-port build pipeline.

Run via:
    python build_deck.py

Output:
    20260325_Commercial Strategy Market Analysis (reference port)_vS.pptx
    (at projects/style_library/)

A growing library of single slides ported 1:1 from the source deck
(/Users/brendantoole/projects3/reference/20260325_Commercial Strategy_Market
Analysis_vS.pptx) into native deck_core modules, to serve as a reference corpus
for AI agents authoring custom slide modules. Native <c:chart> exhibits are
bundled verbatim with their .xlsb (charts are reproduced byte-exact, not rebuilt
from data); the surrounding shapes are emitted as idiomatic deck_core primitives
by _tools/convert_slide.py.

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in
``deck_commercial_strategy/lib.py`` and the slide modules under
``deck_commercial_strategy/slides/``. No vendored engine copy.
"""
import sys

from deck_commercial_strategy.lib import build


if __name__ == "__main__":
    sys.exit(build())
