#!/usr/bin/env python3
"""Launcher for the doc_distributed_shipbuilding (Distributed Shipbuilding) Word pipeline.

Run via:
    python build_doc.py

Output:
    <date>_Distributed Shipbuilding_Sourcing-Openings Methodology_vS.docx
    (at the project root, projects/distributed_shipbuilding/)

The shared raw-OOXML engine is the canonical ``docx_core`` package at the
workspace root; all pipeline-specific binding lives in
``doc_distributed_shipbuilding/lib.py`` and the page modules under
``doc_distributed_shipbuilding/pages/``. There is no vendored copy of the engine
in this pipeline -- it imports the single source of truth at ``docx_core``.
"""
import sys

from doc_distributed_shipbuilding.lib import build


if __name__ == "__main__":
    sys.exit(build())
