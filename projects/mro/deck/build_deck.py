#!/usr/bin/env python3
"""Launcher for the deck_mro (Navy & USCG vessel MRO) PowerPoint build pipeline.

Run via:
    python build_deck.py

Output:
    <date>_Defense Drivers MRO_vS.pptx  (at the project root, projects/mro/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_mro/lib.py`` and the
slide modules under ``deck_mro/slides/``. There is no vendored copy of the engine
in this pipeline -- it imports the single source of truth at ``deck_core``.
"""
import sys

from deck_mro.lib import build


if __name__ == "__main__":
    sys.exit(build())
