"""Filesystem paths for the Saronic awards mini-workbook.

EXTRACTED points at the contracts research dir's extracted/ CSVs (the raw pulls);
OUT is the built xlsx. Both derive from this file's location so the package is
relocatable.
"""
from __future__ import annotations

from pathlib import Path

_PKG = Path(__file__).resolve().parent          # .../research/contracts/workbook
CONTRACTS = _PKG.parent                          # .../research/contracts
EXTRACTED = CONTRACTS / "extracted"
OUT = CONTRACTS / "Saronic_USV_Awards_Evidence.xlsx"
