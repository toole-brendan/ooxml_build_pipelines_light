#!/usr/bin/env python3
"""Launcher for the deck_army (U.S. Army Market Mapping) PowerPoint build pipeline.

Run via:
    python build_deck.py

Output:
    <date>_US Army Market Mapping_vS.pptx  (at the project root, projects/army/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_army/lib.py`` and the
slide modules under ``deck_army/slides/``. There is no vendored copy of the engine
in this pipeline -- it imports the single source of truth at ``deck_core``.
"""
import sys

from deck_army.lib import build


if __name__ == "__main__":
    sys.exit(build())
