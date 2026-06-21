"""Launcher for the workbook_master_tam build pipeline.

Run via:
    python build_workbook.py

Output:
    20260620_Distributed Shipbuilding Master TAM_vS.xlsx  (at the project root, projects/distributed_shipbuilding/tam/master/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in ``workbook_master_tam/lib.py``
and the sheet modules under ``workbook_master_tam/sheets/``.
"""
import sys

from workbook_master_tam.lib import build


if __name__ == "__main__":
    sys.exit(build())
