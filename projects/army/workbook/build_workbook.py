"""Launcher for the workbook_army build pipeline.

Run via:
    python build_workbook.py

Output:
    <date>_US Army Market Mapping_vS.xlsx  (at the project root, projects/army/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in ``workbook_army/lib.py`` and
the sheet modules under ``workbook_army/sheets/``.
"""
import sys

from workbook_army.lib import build


if __name__ == "__main__":
    sys.exit(build())
