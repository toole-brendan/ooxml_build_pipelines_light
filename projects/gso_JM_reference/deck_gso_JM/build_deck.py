#!/usr/bin/env python3
"""Launcher for the deck_gso_JM (GS&O Strategy Materials Style Guide port) build.

Run via:
    python build_deck.py

Output:
    20260615_GSO_Strategy Materials Style Guide_vS.pptx  (at projects/gso_JM_reference/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_gso_JM/lib.py``
and the slide modules under ``deck_gso_JM/slides/``. There is no vendored copy
of the engine in this pipeline -- it imports the single source of truth at
``deck_core``.
"""
import sys

from deck_gso_JM.lib import build


if __name__ == "__main__":
    sys.exit(build())
