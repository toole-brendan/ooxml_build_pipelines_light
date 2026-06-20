#!/usr/bin/env python3
"""Launcher for the deck_consolidated PowerPoint build pipeline.

Run via:
    python build_deck.py

Output:
    20260605_Distributed Shipbuilding Consolidated_vS.pptx  (at the project root, projects/distributed_shipbuilding/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_consolidated/lib.py``
and the slide modules under ``deck_consolidated/slides/``. There is no vendored
copy of the engine in this pipeline -- it imports the single source of truth at
``deck_core``.
"""
import sys

from deck_consolidated.lib import build


if __name__ == "__main__":
    sys.exit(build())
