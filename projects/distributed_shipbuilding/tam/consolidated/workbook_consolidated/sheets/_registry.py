"""_registry - the shared supplier evidence registry (operating-entity overrides).

NON-sheet helper (renders nothing; NOT in SHEETS). Loads the project-level
`vendor_evidence_registry.csv` (keyed by operating-entity UEI) once and exposes it
as a dict so data_entity_master can classify records registry-FIRST, before falling
back to the NAICS/name ladder in `_taxonomy.classify`. This is the governing signal:
operating-entity NAICS resolved via SAM, adjudicated into role/bucket + scenario
flags. Domain data; lives at project level, never in workbook_core (locked-core).

`residual` in the registry = identity-resolved but unbucketable; in the workbook it
joins the supplier-addressable floor as unbucketed supplier (matches the
reconciliation).

SCAFFOLD NOTE: the submarines pipeline normalizes registry `gfe` -> `gfe_sib` and
ddg normalizes it -> `gfe_mib`. The consolidated workbook (submarines + ddg) passes
registry `gfe` through unchanged here; decide the role label your consolidated
sheets expect when you wire the first data sheet and extend `_ROLE_MAP` if needed.
"""
from __future__ import annotations

import csv

from workbook_consolidated.lib import REGISTRY_CSV

_ROLE_MAP = {"residual": "supplier"}


def load_registry() -> dict[str, dict]:
    """uei -> {role, bucket, modular, vls}. Empty dict if the file is absent."""
    out: dict[str, dict] = {}
    if not REGISTRY_CSV.exists():
        return out
    with REGISTRY_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            uei = (r.get("uei") or "").strip()
            if not uei:
                continue
            role = (r.get("role") or "").strip()
            role = _ROLE_MAP.get(role, role)
            flags = (r.get("scenario_flags") or "")
            out[uei] = {
                "role": role,
                "bucket": (r.get("bucket") or "").strip(),
                "modular": "modular" in flags,
                "vls": "vls_boundary" in flags,
            }
    return out
