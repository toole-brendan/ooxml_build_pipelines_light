#!/usr/bin/env python3
"""Launcher for the doc_outsourced_ceiling (Outsourcing Ceiling methodology) Word pipeline.

Run via:
    python build_outsourced_ceiling.py

Output:
    <date>_Outsourcing Ceiling_Methodology_vS.docx
    (at the project root, projects/distributed_shipbuilding/)

The shared raw-OOXML engine is the canonical ``docx_core`` package at the
workspace root; all pipeline-specific binding lives in
``doc_outsourced_ceiling/lib.py`` and the page modules under
``doc_outsourced_ceiling/pages/``. There is no vendored copy of the engine in this
pipeline -- it imports the single source of truth at ``docx_core``.
"""
import sys

from doc_outsourced_ceiling.lib import build


if __name__ == "__main__":
    sys.exit(build())
