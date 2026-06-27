#!/usr/bin/env python3
"""Launcher for the deck_data_reference (single-slide Data Reference deck) build pipeline.

Run via:
    python build_deck.py

Output:
    20260626_Distributed Shipbuilding Data Reference_vS.pptx  (at projects/distributed_shipbuilding/deck_data_reference/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_data_reference/lib.py``
and the slide modules under ``deck_data_reference/slides/``. There is no vendored
copy of the engine in this pipeline -- it imports the single source of truth at
``deck_core``.
"""
import sys

from deck_data_reference.lib import build


if __name__ == "__main__":
    sys.exit(build())
