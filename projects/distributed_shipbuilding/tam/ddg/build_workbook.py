"""Launcher for the workbook_ddg build pipeline.

Run via:
    python build_workbook.py

Output:
    20260601_Distributed Shipbuilding DDG_vS.xlsx  (at the project root, projects/distributed_shipbuilding/ddg/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in ``workbook_ddg/lib.py`` and
the sheet modules under ``workbook_ddg/sheets/``.
"""
import sys

from workbook_ddg.lib import build


if __name__ == "__main__":
    sys.exit(build())
