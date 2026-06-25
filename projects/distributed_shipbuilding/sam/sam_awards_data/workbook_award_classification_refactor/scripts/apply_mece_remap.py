"""apply_mece_remap - one-time, auditable MECE remap of the D axis in the NAICS-6
archetype crosswalk (extracted/naics6_archetype_map.csv).

Applies the 2026-06-20 MECE revision to the Capability Domain (D) of rows the external
research agent left at D0:
  - Non-material SERVICES industry codes        -> D11 (new Services & Non-Material Support)
  - 335312 Motor & Generator Manufacturing      -> D3  (electric power; the D2/D3 crack -
                                                        propulsion-motor firms are overridden to D2)
  - 333611 Turbine & Turbine Generator Sets     -> D2  (turbomachinery / propulsion)
Everything else left at D0 stays D0 (genuinely cross-domain, non-ship, or distribution).
Idempotent: only rewrites rows whose current D is D0 and whose NAICS is in a rule set.
Original is preserved as naics6_archetype_map.pre_mece.csv.
"""
from __future__ import annotations
import csv
from pathlib import Path

EXTRACTED = Path(__file__).resolve().parent.parent / "extracted"
MAP = EXTRACTED / "naics6_archetype_map.csv"

SERVICES = {  # non-material support -> D11 (P6-counterpart on the domain axis)
    "541330", "541611", "541613", "541519", "541511", "541380", "541614", "541990",
    "541620", "561320", "561910", "561612", "561990", "561311", "562910", "562211",
    "611430", "923110", "513210", "811310", "811210", "236210", "236220", "237990",
    "238210", "238220", "238990", "483113", "484121", "488330", "488510", "532490",
    "532412", "532310", "531120", "524291", "713990", "425120",
}
ELECTRIC = {"335312": "D3"}   # motor+generator: generic -> D3; propulsion firms -> D2 override
TURBO = {"333611": "D2"}      # turbine / turbine-generator sets -> turbomachinery (propulsion)

REMAP: dict[str, str] = {}
REMAP.update({n: "D11" for n in SERVICES})
REMAP.update(ELECTRIC)
REMAP.update(TURBO)

DCOL = "Capability Domain (D)"
rows = list(csv.DictReader(MAP.open(encoding="utf-8-sig")))
fields = rows[0].keys()
changed = []
for r in rows:
    nc = (r.get("NAICS-6") or "").strip()
    if (r.get(DCOL) or "").strip() == "D0" and nc in REMAP:
        old, new = r[DCOL], REMAP[nc]
        r[DCOL] = new
        changed.append((nc, old, new, (r.get("NAICS-6 Title") or "")[:46]))

with MAP.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(fields))
    w.writeheader(); w.writerows(rows)

from collections import Counter
c = Counter(n for _, _, n, _ in changed)
print(f"remapped {len(changed)} NAICS-6 rows out of D0: {dict(c)}")
for nc, old, new, title in sorted(changed, key=lambda x: x[2]):
    print(f"  {nc} {old}->{new}  {title}")
