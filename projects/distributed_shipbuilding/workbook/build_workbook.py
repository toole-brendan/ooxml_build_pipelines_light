"""Launcher for the workbook_consolidated build pipeline.

Run via:
    python build_workbook.py

Output:
    20260605_Distributed Shipbuilding Consolidated_vS.xlsx  (at the project root, projects/distributed_shipbuilding/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in ``workbook_consolidated/lib.py``
and the sheet modules under ``workbook_consolidated/sheets/``.
"""
import sys

from workbook_consolidated.lib import build


if __name__ == "__main__":
    sys.exit(build())
