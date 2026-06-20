#!/usr/bin/env python3
"""Launcher for the deck_primary (New Construction methodology deck) build pipeline.

Run via:
    python build_deck.py

Output:
    20260610_Distributed Shipbuilding New Construction_vS.pptx  (at projects/distributed_shipbuilding/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_primary/lib.py``
and the slide modules under ``deck_primary/slides/``. There is no vendored copy
of the engine in this pipeline -- it imports the single source of truth at
``deck_core``.
"""
import sys

from deck_primary.lib import build


if __name__ == "__main__":
    sys.exit(build())
