"""Launcher for the workbook_award_analysis build pipeline.

Run via:
    python build_workbook.py

Output:
    20260612_Distributed Shipbuilding Award Analysis_vS.xlsx  (at the project root, projects/distributed_shipbuilding/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in ``workbook_award_analysis/lib.py``
and the sheet modules under ``workbook_award_analysis/sheets/``.
"""
import sys

from workbook_award_analysis.lib import build


if __name__ == "__main__":
    sys.exit(build())
