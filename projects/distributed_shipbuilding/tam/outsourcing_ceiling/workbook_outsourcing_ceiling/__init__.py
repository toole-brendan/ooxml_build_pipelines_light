"""workbook_outsourcing_ceiling - Distributed Shipbuilding Outsourcing Ceiling pipeline.

A parameterized, source-anchored estimate of the THEORETICAL ceiling on
new-construction outsourcing for the three programs (Virginia, Columbia,
DDG-51) and the hours->dollars bridge that makes the Navy's labor-hours
outsourcing figure usable in a dollar model. Sizes, per class:
  - the irreducible prime-yard core  (core = L * (1 - h))  and
  - the outsourcing ceiling          (ceiling = 1 - core)  as shares of
    P-5c Basic Construction,
then converts an hours-based share to a dollar share via core + pass-through
material. It replaces the flat, unsourced x1.30 intent uplift carried in the
sub/ddg Assumptions and deck_primary with a structural ceiling backed by:
  - h ~ 50% of submarine construction labor hours (RADM Rucker, Defense News 2022),
  - L ~ 40%+ shipyard labor share of ship cost (O'Rourke CRS testimony 2025;
    CBO Shipbuilding Composite Index 2024).

Thin per-pipeline package: binds the output path, the extracted-data dir, and
the docProps identity (lib.py), and registers the sheet modules (sheets/). The
shared raw-OOXML engine is the canonical ``workbook_core`` package at the
workspace root; the sheet modules import ``workbook_core.*`` directly.

This module makes both packages importable regardless of entry point by putting
two dirs on sys.path:
  - the build dir (this package's parent,
    ``projects/distributed_shipbuilding/workbook_outsourcing_ceiling/``) so
    ``workbook_outsourcing_ceiling`` resolves;
  - the workspace root (four levels up) so ``workbook_core`` resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_PROJECT_ROOT = str(_HERE.parents[1])   # projects/distributed_shipbuilding/workbook_outsourcing_ceiling/
_CORE_DIR = str(_HERE.parents[5])       # workspace root (holds workbook_core)

for _p in (_PROJECT_ROOT, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
