#!/usr/bin/env python3
"""Launcher for the doc_army (U.S. Army Market Mapping) Word pipeline.

Run via:
    python build_doc.py

Output:
    <date>_US Army Market Mapping_vS.docx  (at the project root, projects/army/)

The shared raw-OOXML engine is the canonical ``docx_core`` package at the
workspace root; all pipeline-specific binding lives in ``doc_army/lib.py`` and the
page modules under ``doc_army/pages/``. There is no vendored copy of the engine
in this pipeline -- it imports the single source of truth at ``docx_core``.
"""
import sys

from doc_army.lib import build


if __name__ == "__main__":
    sys.exit(build())
