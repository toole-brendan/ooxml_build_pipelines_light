"""Launcher for the workbook_sea_range_telemetry build pipeline.

Run via:
    python build_workbook.py

Output:
    20260607_Sea Range Telemetry_vS.xlsx  (at the project root, projects/sea_range_telemetry/)

The shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; all pipeline-specific binding lives in ``workbook_sea_range_telemetry/lib.py``
and the sheet modules under ``workbook_sea_range_telemetry/sheets/``.
"""
import sys

from workbook_sea_range_telemetry.lib import build


if __name__ == "__main__":
    sys.exit(build())
