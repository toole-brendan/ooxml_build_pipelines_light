#!/usr/bin/env python3
"""Launcher for the deck_sea_range_telemetry PowerPoint build pipeline.

Run via:
    python build_deck.py

Output:
    20260607_Sea Range Telemetry_vS.pptx  (at the project root, projects/sea_range_telemetry/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``deck_sea_range_telemetry/lib.py``
and the slide modules under ``deck_sea_range_telemetry/slides/``. There is no vendored
copy of the engine in this pipeline -- it imports the single source of truth at
``deck_core``.
"""
import sys

from deck_sea_range_telemetry.lib import build


if __name__ == "__main__":
    sys.exit(build())
