"""Launcher for the workbook_ddg_module_cost build pipeline.

Run via:
    python3 build_workbook.py

Output:
    20260625_DDG-51 Module Cost_vS.xlsx   (at ddg_module_cost/)

A small standalone workbook estimating DDG-51 cost per structural module / grand
block / unit. The per-ship Basic-Construction anchor is mirrored from the Master
TAM workbook's DDG-51 SCN-budget slice via build_extracted.py; the structural
counts (4 / 21 / 72) come verbatim from HII's site. The shared raw-OOXML engine
is the canonical ``workbook_core`` package at the workspace root; all
pipeline-specific binding lives in ``workbook_ddg_module_cost/lib.py`` and the
sheet modules under ``workbook_ddg_module_cost/sheets/``.
"""
import sys

from workbook_ddg_module_cost.lib import build


if __name__ == "__main__":
    sys.exit(build())
