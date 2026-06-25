#!/usr/bin/env python3
"""Launcher for the deck_awards_methodology PowerPoint build pipeline.

Run via:
    python build_deck.py

Output:
    <date>_Awards Methodology_vS.pptx  (at the deck root, projects/awards_methodology/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_awards_methodology/lib.py``
and the slide modules under ``deck_awards_methodology/slides/``. There is no vendored
copy of the engine in this pipeline -- it imports the single source of truth at
``deck_core``.
"""
import sys

from deck_awards_methodology.lib import build


if __name__ == "__main__":
    sys.exit(build())
