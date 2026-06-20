#!/usr/bin/env python3
"""Launcher for the deck_submarines_draft (DRAFT submarines) PowerPoint pipeline.

A second, parallel build to ``build_deck.py``: it renders the reviewed DRAFT
slide modules under ``deck_submarines_draft/slides_draft/`` rather than the real
``deck_submarines/slides/`` set, and writes a distinct DRAFT .pptx so the two
pipelines never clobber each other.

Run via:
    python build_drafts.py

Output:
    20260602_Distributed Shipbuilding Submarines_DRAFT_vS.pptx  (at the project root, projects/distributed_shipbuilding/submarines/)

The shared raw-OOXML engine is the canonical ``deck_core`` package at the
workspace root; all pipeline-specific binding lives in
``deck_submarines_draft/lib.py`` and the slide modules under
``deck_submarines_draft/slides_draft/``.
"""
import sys

from deck_submarines_draft.lib import build


if __name__ == "__main__":
    sys.exit(build())
