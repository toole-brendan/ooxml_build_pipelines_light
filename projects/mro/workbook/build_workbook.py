"""Launcher for the workbook_mro build pipeline.

Run via:
    python build_workbook.py

Output:
    <date>_Defense Drivers MRO_vS.xlsx  (at the project root, projects/mro/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in ``workbook_mro/lib.py`` and
the sheet modules under ``workbook_mro/sheets/``.
"""
import sys

from workbook_mro.lib import build


if __name__ == "__main__":
    sys.exit(build())
