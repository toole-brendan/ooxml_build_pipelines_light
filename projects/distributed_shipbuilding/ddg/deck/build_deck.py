#!/usr/bin/env python3
"""Launcher for the deck_ddg (destroyers) PowerPoint build pipeline.

Run via:
    python build_deck.py

Output:
    20260602_Distributed Shipbuilding DDG_vS.pptx  (at the project root, projects/distributed_shipbuilding/ddg/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_ddg/lib.py`` and the
slide modules under ``deck_ddg/slides/``. There is no vendored copy of the engine
in this pipeline -- it imports the single source of truth at ``deck_core``.
"""
import sys

from deck_ddg.lib import build


if __name__ == "__main__":
    sys.exit(build())
