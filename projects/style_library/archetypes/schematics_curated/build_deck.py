#!/usr/bin/env python3
"""Launcher for the schematics archetype reference-port build pipeline.

Run via:
    python3 build_deck.py

Output:
    Schematics (reference port).pptx
    (at projects/style_library/archetypes/schematics_curated/)

A growing library of *schematic* slides - framework diagrams, value-chain maps,
definition tables - ported 1:1 from the source market-analysis decks into native
deck_core modules, to serve as a reference corpus for AI agents authoring custom
slide modules. The corpus is organized by visual archetype rather than by source
deck; this deck holds the "schematic" archetype. Surrounding shapes and pictures
are emitted as idiomatic deck_core primitives by the converter, which lives in
the converter at style_library/_tools/convert_slide.py.

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in ``schematics/lib.py`` and
the slide modules under ``schematics/slides/``. No vendored engine copy.
"""
import sys

from schematics.lib import build


if __name__ == "__main__":
    sys.exit(build())
