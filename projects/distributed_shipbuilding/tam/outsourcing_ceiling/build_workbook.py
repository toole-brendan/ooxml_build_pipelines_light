"""Launcher for the workbook_outsourcing_ceiling build pipeline.

Run via:
    python3.12 build_workbook.py

Output:
    20260615_Distributed Shipbuilding Outsourcing Ceiling_vS.xlsx
    (at the project root, projects/distributed_shipbuilding/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in
``workbook_outsourcing_ceiling/lib.py`` and the sheet modules under
``workbook_outsourcing_ceiling/sheets/``.

Regenerate the data first if the cost funnels changed:
    python3.12 build_ceiling_base.py
"""
import sys

from workbook_outsourcing_ceiling.lib import build


if __name__ == "__main__":
    sys.exit(build())
