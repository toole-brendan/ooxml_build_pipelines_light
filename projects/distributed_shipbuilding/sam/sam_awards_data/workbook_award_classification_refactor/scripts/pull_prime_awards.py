"""pull_prime_awards - authoritative prime-award detail for the in-scope primes.

The prime fields embedded on the subaward rows are per-report SNAPSHOTS (base date and
total contract value vary row-to-row), so the real prime period of performance and
obligations come from a direct USAspending award-detail pull (no API key). ONE GET per
in-scope prime, keyed on the Prime Contract Key (USAspending generated_unique_award_id)
already carried on the transaction sheets.

Prime dollars are NOMINAL cumulative obligations (not deflated) - a different basis from
the FY2026$ subaward columns; prime PoP includes option years. Both captioned on the sheet.

Output:
  extracted/prime_awards.csv               one row per (Program x Prime PIID)
  research_pulls/prime_awards_raw/<piid>.json   faithful full award record (project rule)

Run:
    python3 scripts/pull_prime_awards.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from _paths import REPO  # noqa: E402
PKG = REPO / ("projects/distributed_shipbuilding/sam/sam_awards_data/"
             "workbook_award_classification_refactor")
EXTRACTED = PKG / "extracted"
RAW = PKG / "research_pulls" / "prime_awards_raw"
sys.path.insert(0, str(REPO / "projects/army/research/contracts/scripts"))
from _common import http_get  # noqa: E402  (IPv4-forced GET; no key needed for USAspending)

PROGRAMS = [("DDG", "ddg"), ("Virginia", "virginia"), ("Columbia", "columbia")]

# Block / Multi-Year-Procurement vintage per in-scope prime PIID. NOT a field in any pull -
# hand-derived from the award description + the well-known hull->block boundaries (Virginia
# Block IV = SSN 792-801, Block V = SSN 802-811, Block VI = SSN 812+). Kept here (not the
# CSV) so a re-pull preserves it; edit a label in ONE place. Used by the Subaward Activity
# block/MYP rollup (looked up into the engagement grain by PIID).
BLOCK_MYP = {
    "N0002411C2307": "DDG FY11 (single-ship)",
    "N0002411C2309": "DDG FY11 (single-ship)",
    "N0002413C2305": "DDG FY13-17 MYP",
    "N0002413C2307": "DDG FY13-17 MYP",
    "N0002418C2305": "DDG FY18-22 MYP",
    "N0002418C2307": "DDG FY18-22 MYP",
    "N0002423C2307": "DDG FY23-27 MYP",
    "N0002412C2115": "Virginia Block IV (LLTM)",
    "N0002416C2111": "Virginia LYS (cross-block)",
    "N0002417C2100": "Virginia Block V (LLTM)",
    "N0002424C2110": "Virginia Block VI (LLTM)",
    "N0002417C2117": "Columbia (design/build)",
}

HEADERS = ["Program", "Prime PIID", "Prime Entity Name", "Award Description", "Block / MYP",
           "Date Signed", "PoP Start", "PoP Current End", "PoP Potential End",
           "Total Obligated $M (nominal)", "Base + All Options $M (nominal)",
           "USAspending Subaward Count", "USAspending Subaward $M"]


def _scope() -> dict:
    """{(program, piid): prime_contract_key} for the in-scope primes, from the tx sheets."""
    out = {}
    for label, stem in PROGRAMS:
        for r in csv.DictReader((EXTRACTED / f"{stem}_subaward_transactions.csv").open()):
            out.setdefault((label, r["Prime PIID"]), r["Prime Contract Key"])
    return out


def _date(x) -> str:
    return (x or "").split(" ")[0]


def _m(x):
    return round(float(x) / 1e6, 3) if x not in (None, "") else ""


def build():
    RAW.mkdir(parents=True, exist_ok=True)
    order = {label: i for i, (label, _) in enumerate(PROGRAMS)}
    rows, failed = [], []
    for (label, piid), key in sorted(_scope().items(),
                                     key=lambda kv: (order[kv[0][0]], kv[0][1])):
        txt, status = http_get(f"https://api.usaspending.gov/api/v2/awards/{key}/", timeout=90)
        if not txt:
            failed.append((piid, status))
            print(f"  WARN {piid}: HTTP {status} (no body)")
            continue
        d = json.loads(txt)
        (RAW / f"{piid}.json").write_text(json.dumps(d, indent=2))
        pop = d.get("period_of_performance") or {}
        rec = d.get("recipient") or {}
        rows.append([
            label, piid, rec.get("recipient_name") or "", d.get("description") or "",
            BLOCK_MYP.get(piid, ""),
            _date(d.get("date_signed")), _date(pop.get("start_date")),
            _date(pop.get("end_date")), _date(pop.get("potential_end_date")),
            _m(d.get("total_obligation")), _m(d.get("base_and_all_options")),
            d.get("subaward_count") or "", _m(d.get("total_subaward_amount"))])
        print(f"  {label:9s} {piid}: PoP {_date(pop.get('start_date'))}..{_date(pop.get('end_date'))}"
              f"  oblig ${_m(d.get('total_obligation')):>12,}M")

    path = EXTRACTED / "prime_awards.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        w.writerows(rows)
    print(f"\noutput: {path}  ({len(rows)} primes)")
    # integrity: start <= current end on every row; every prime carries a Block / MYP label.
    for r in rows:
        s, e = r[6], r[7]
        if s and e:
            assert s <= e, f"{r[1]}: PoP start {s} > end {e}"
    missing_block = [r[1] for r in rows if not r[4]]
    assert not missing_block, f"BLOCK_MYP missing label for: {missing_block}"
    if failed:
        print(f"FAILED ({len(failed)}): {failed}  -- re-run; the sheet needs all 12.")


if __name__ == "__main__":
    build()
