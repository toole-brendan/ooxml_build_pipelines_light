"""Launcher for the workbook_submarines build pipeline.

Run via:
    python build_workbook.py

Output:
    20260601_Distributed Shipbuilding Submarines_vS.xlsx  (at the project root, projects/distributed_shipbuilding/submarines/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in ``workbook_submarines/lib.py``
and the sheet modules under ``workbook_submarines/sheets/``.
"""
import sys

from workbook_submarines.lib import build


if __name__ == "__main__":
    sys.exit(build())
