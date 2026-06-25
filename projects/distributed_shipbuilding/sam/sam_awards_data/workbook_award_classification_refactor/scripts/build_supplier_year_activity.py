"""build_supplier_year_activity - the (Program x Subawardee UEI x Federal FY) activity spine.

One row per (Program, Federal FY, Subawardee UEI), read straight from the three committed
*_subaward_transactions.csv fact sheets (no corpus dependency - runs in this tree):

    extracted/supplier_year_activity.csv

Materializes only the row IDENTITY plus the one count Excel can't do live at this grain:

    Program | Federal FY | Subawardee UEI | Distinct Subaward Numbers

Materialized here: Program, Federal FY (= calendar year, +1 from October on, the federal-
fiscal-year convention used across the workbook), Subawardee UEI, and Distinct Subaward Numbers
(a distinct count over Subaward Number, with no clean/performant live-Excel form at this row
count - exactly as build_subaward_activity materializes it).

Left BLANK here (the Supplier-Year Activity sheet fills them with live formulas over the
transaction leaves + a single Supplier Master match): Subawardee Vendor Name, Parent Key,
Capability Domain (D), Primary Output (P), Net Subaward $M, Positive Supplier $M, Reports,
Prior-Year Active, Earlier-Year Active, Activity Status, Active FYs.

ALL available fiscal years are emitted (not only the FY2022-FY2025 reporting window): FY2022's
"first observed" status is defined against the full pre-FY2022 history, so the earlier years must
be present in the spine even though Where to Play only renders the recent window.

Run:
    python3 scripts/build_supplier_year_activity.py
"""
from __future__ import annotations

import csv
from collections import defaultdict

from _paths import EXTRACTED

# program label (as shown / keyed) -> committed transaction CSV stem; fixed display order.
PROGRAMS = [("DDG", "ddg"), ("Virginia", "virginia"), ("Columbia", "columbia")]

# Materialized identity + the distinct count (everything else is a live sheet formula).
STATIC_HEADERS = ["Program", "Federal FY", "Subawardee UEI", "Distinct Subaward Numbers"]

# Filled live on the Supplier-Year Activity sheet (blank in the CSV).
FORMULA_HEADERS = [
    "Subawardee Vendor Name", "Parent Key", "Capability Domain (D)", "Primary Output (P)",
    "Net Subaward $M", "Positive Supplier $M", "Reports",
    "Prior-Year Active", "Earlier-Year Active", "Activity Status", "Active FYs",
]

HEADERS = STATIC_HEADERS + FORMULA_HEADERS


def _federal_fy(raw_date: str) -> int:
    """Federal FY of an ISO action date: calendar year, +1 from October on (Oct 1 start).
    Mirrors _fiscal._federal_fy_expr and the _integrity date-coverage guard."""
    y, m, _d = (int(v) for v in raw_date[:10].split("-"))
    return y + int(m >= 10)


def build() -> None:
    order = {label: i for i, (label, _stem) in enumerate(PROGRAMS)}
    rows: list[tuple[str, int, str, int]] = []

    for label, stem in PROGRAMS:
        # (UEI, Federal FY) -> set of distinct Subaward Numbers observed in that supplier-year.
        activity: dict[tuple[str, int], set[str]] = defaultdict(set)
        path = EXTRACTED / f"{stem}_subaward_transactions.csv"
        with path.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                uei = (r.get("Subawardee UEI") or "").strip()
                raw = (r.get("Subaward Date") or "").strip()
                if not uei or not raw:
                    continue
                activity[(uei, _federal_fy(raw))].add((r.get("Subaward Number") or "").strip())
        for (uei, fy), subnos in activity.items():
            rows.append((label, fy, uei, len(subnos)))

    # Program order, then UEI, then fiscal year - stable, reader-friendly.
    rows.sort(key=lambda x: (order[x[0]], x[2], x[1]))

    out = EXTRACTED / "supplier_year_activity.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADERS)
        for label, fy, uei, ndistinct in rows:
            w.writerow([label, fy, uei, ndistinct] + [""] * len(FORMULA_HEADERS))

    # integrity: one row per (Program, FY, UEI); every row keyed + counted.
    keys = {(label, fy, uei) for label, fy, uei, _n in rows}
    assert len(keys) == len(rows), (len(keys), len(rows))
    assert all(n >= 1 for _l, _f, _u, n in rows)
    print(f"output: {out}  ({len(rows)} supplier-year rows)")
    for label, _stem in PROGRAMS:
        n = sum(1 for lab, _f, _u, _n in rows if lab == label)
        print(f"  {label:9s} supplier-years : {n}")


if __name__ == "__main__":
    build()
