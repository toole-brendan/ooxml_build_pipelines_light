"""build_subaward_activity - the (subawardee UEI x prime PIID) activity spine + UEI rollup.

Produces TWO spines, both read straight from the three committed *_subaward_transactions.csv
fact sheets (no corpus dependency - runs in this tree):
  - extracted/subaward_activity.csv        ONE row per (Program, Subawardee UEI, Prime PIID)
  - extracted/subaward_vendor_rollup.csv   ONE row per Subawardee UEI (the §2 rollup spine)

The §1 spine materializes only the row IDENTITY plus the one count Excel can't do live:

    Program | Prime PIID | Subawardee UEI | Subawardee Vendor Name |
    Reports | Distinct Subaward Numbers | Correction Actions |
    First Action | Last Action | Activity Span (Years) | Net Subaward $M (FY2026$)

Materialized here: Program, Prime PIID, Subawardee UEI, Subawardee Vendor Name
(dollar-modal as-reported name), and Distinct Subaward Numbers (a distinct count over
subAwardNumber, which has no clean/performant live-Excel form at this row count).

Left BLANK here (the sheet fills them with live formulas over the transaction leaves -
COUNTIFS / MINIFS / MAXIFS / SUMIFS keyed on UEI + Prime PIID, 3-way additive across the
three program sheets since PIIDs are program-disjoint): Reports, Correction Actions,
First Action, Last Action, Activity Span (Years), Net Subaward $M (FY2026$).

NOTE on framing: FFATA subaward records carry NO modification / action-type field (verified
against the live API - 28 fields, none of them an amendment flag; subAwardReportNumber is a
UUID, primeAwardType is the prime's type). subAwardNumber is also used inconsistently (a
blanket/IDIQ number can cover hundreds of separate dated actions). So the honest unit is the
dated subaward report; "Activity Span" = first-to-last reported action date, a reporting-based
lower bound, NOT a contractual period of performance.

Run:
    python3 scripts/build_subaward_activity.py
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

from _paths import REPO  # noqa: E402
EXTRACTED = REPO / ("projects/distributed_shipbuilding/sam/sam_awards_data/"
                    "workbook_award_classification_refactor/extracted")

# program label (as shown) -> committed transaction CSV stem; fixed display order.
PROGRAMS = [("DDG", "ddg"), ("Virginia", "virginia"), ("Columbia", "columbia")]

HEADERS = ["Program", "Prime PIID", "Subawardee UEI", "Subawardee Vendor Name",
           "Reports", "Distinct Subaward Numbers", "Correction Actions",
           "First Action", "Last Action", "Activity Span (Years)",
           "Net Subaward $M (FY2026$)"]

# Vendor-rollup spine (§2): ONE row per Subawardee UEI, collapsing all of that vendor's
# (PIID, program) engagements. Only the three distinct-counts are materialized here (no clean
# live-Excel form at this grain); the sheet fills Reports / Corrections / First / Last /
# Portfolio Span / Net $M / Portfolio Type with live formulas keyed on UEI alone (3-way
# additive across the program leaves, exactly like §1 but without the PIID criterion).
ROLLUP_HEADERS = ["Subawardee UEI", "Subawardee Vendor Name", "Distinct PIIDs",
                  "Distinct Programs", "Distinct Subaward Numbers"]


def _modal(counts: Counter) -> str:
    """dollar-modal key, ties broken by the key itself for deterministic output."""
    return max(counts, key=lambda k: (counts[k], k)) if counts else ""


def build():
    rows = []
    order = {label: i for i, (label, _) in enumerate(PROGRAMS)}
    per_program = {}
    # Per-UEI accumulators span ALL programs (a vendor can appear on >1 program / PIID).
    uei_agg: dict[str, dict] = defaultdict(
        lambda: {"names": Counter(), "allnames": Counter(),
                 "subnos": set(), "piids": set(), "progs": set(), "gross": 0.0})
    for label, prog in PROGRAMS:
        tx = list(csv.DictReader((EXTRACTED / f"{prog}_subaward_transactions.csv").open()))
        agg: dict[tuple, dict] = defaultdict(
            lambda: {"names": Counter(), "subnos": set(), "gross": 0.0})
        for r in tx:
            amt = float(r["Subaward Amount $"] or 0)
            d = agg[(r["Subawardee UEI"], r["Prime PIID"])]
            d["names"][r["Subawardee Vendor Name"]] += amt if amt > 0 else 0.0
            d["subnos"].add(r["Subaward Number"])
            d["gross"] += amt
            u = uei_agg[r["Subawardee UEI"]]
            u["names"][r["Subawardee Vendor Name"]] += amt if amt > 0 else 0.0
            u["allnames"][r["Subawardee Vendor Name"]] += 1
            u["subnos"].add(r["Subaward Number"])
            u["piids"].add(r["Prime PIID"])
            u["progs"].add(label)
            u["gross"] += amt
        per_program[label] = len(agg)
        for (uei, piid), d in agg.items():
            # fall back to record-count modal name when every action nets <= 0
            name = _modal(d["names"]) or _modal(Counter(
                r["Subawardee Vendor Name"] for r in tx
                if r["Subawardee UEI"] == uei and r["Prime PIID"] == piid))
            rows.append({"label": label, "piid": piid, "uei": uei, "name": name,
                         "nsub": len(d["subnos"]), "gross": d["gross"]})

    # Program order, then PIID, then biggest relationship first within a PIID.
    rows.sort(key=lambda x: (order[x["label"]], x["piid"], -x["gross"]))

    path = EXTRACTED / "subaward_activity.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADERS)
        for x in rows:
            # blanks are the live-formula columns (Reports / Corrections / dates / span / $).
            w.writerow([x["label"], x["piid"], x["uei"], x["name"],
                        "", x["nsub"], "", "", "", "", ""])

    # integrity: one row per distinct relationship, every row keyed + counted.
    keys = {(x["label"], x["uei"], x["piid"]) for x in rows}
    assert len(keys) == len(rows), (len(keys), len(rows))
    assert all(x["nsub"] >= 1 for x in rows)

    print(f"output: {path}  ({len(rows)} relationships)")
    for label, _ in PROGRAMS:
        print(f"  {label:9s} relationships : {per_program[label]}")
    print(f"  distinct subaward #s (sum): {sum(x['nsub'] for x in rows)}")

    # --- §2 vendor rollup: one row per UEI, biggest vendor first ---------------------
    rollup = []
    for uei, u in uei_agg.items():
        name = _modal(u["names"]) or _modal(u["allnames"])
        rollup.append({"uei": uei, "name": name, "npiid": len(u["piids"]),
                       "nprog": len(u["progs"]), "nsub": len(u["subnos"]),
                       "gross": u["gross"]})
    rollup.sort(key=lambda x: (-x["gross"], x["uei"]))

    rpath = EXTRACTED / "subaward_vendor_rollup.csv"
    with rpath.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(ROLLUP_HEADERS)
        for x in rollup:
            w.writerow([x["uei"], x["name"], x["npiid"], x["nprog"], x["nsub"]])

    # integrity: one row per distinct UEI; every vendor has >=1 PIID/program/subaward.
    assert len({x["uei"] for x in rollup}) == len(rollup)
    assert all(x["npiid"] >= 1 and x["nprog"] >= 1 and x["nsub"] >= 1 for x in rollup)
    # every §1 relationship's UEI must exist in the rollup spine (the live UEI keys align).
    assert {x["uei"] for x in rows} == {x["uei"] for x in rollup}
    print(f"output: {rpath}  ({len(rollup)} vendors)")
    print(f"  vendors on >1 PIID    : {sum(1 for x in rollup if x['npiid'] > 1)}")
    print(f"  vendors on >1 program : {sum(1 for x in rollup if x['nprog'] > 1)}")


if __name__ == "__main__":
    build()
