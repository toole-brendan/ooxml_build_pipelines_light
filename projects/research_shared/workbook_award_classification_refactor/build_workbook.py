"""Launcher for the workbook_award_classification_refactor build pipeline.

Run via:
    python build_workbook.py

Output:
    award_classification_refactor.xlsx  (at the project root, projects/research_shared/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in
``workbook_award_classification_refactor/lib.py`` and the sheet modules under
``workbook_award_classification_refactor/sheets/``.
"""
import sys

from workbook_award_classification_refactor.lib import build


if __name__ == "__main__":
    sys.exit(build())
