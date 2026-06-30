"""tag_ddg_transactions_hulls - materialize the regex hull evidence + write the exception log.

The hull analogue of tag_ddg_transactions_swbs, but it materializes ONLY the four columns that
cannot be a live Excel formula (regex needs Python): `Direct Hull Text` / `Direct Hull Count`
(hulls scanned from Subaward Number + Description) and `Prime Requirement Hull Text` /
`Prime Requirement Hull Count` (from the prime Description of Requirement). The hull CLASSIFICATION
- PIID Candidate Hulls, Assigned Hull, Scope, Basis, Confidence - is a set of LIVE formulas on the
DDG Subaward Transactions sheet (sheets/_hulls.py) so edits to the curated PIID->Hull map flow
through the workbook. This step appends only the regex columns, and writes the exception sidecar
extracted/ddg_hull_exceptions.csv using the shared _hull_logic.resolve() (the same rule the formulas
reproduce; the log is a build-time artifact, not a live view).

Idempotent: re-running drops the four hull columns and re-derives them. Run order (SWBS columns must
already be on the CSV):
    python3 scripts/tag_ddg_transactions_swbs.py    # 5 SWBS columns (if regenerating the base)
    python3 scripts/tag_ddg_transactions_hulls.py   # these 4 regex columns + the exception log
    python3 scripts/build_ddg_vendor_hull.py        # the vendor x hull (x SWBS) spines
    python3 build_workbook.py
Re-running the SWBS tagger afterward re-appends the SWBS columns at the end, so re-run THIS script
after it to restore the [50 raw][5 SWBS][4 hull] column order.
"""
from __future__ import annotations

import csv

from _paths import EXTRACTED  # noqa: E402
from _hull_logic import parse_hulls, hull_str, load_map, resolve  # noqa: E402

TX_CSV = EXTRACTED / "ddg_subaward_transactions.csv"
EXC_CSV = EXTRACTED / "ddg_hull_exceptions.csv"

# The 5 SWBS columns the SWBS tagger appends; asserted present so the hull columns sit after them,
# giving [50 raw][5 SWBS][4 hull].
SWBS_COLS = ["HII Work-Item Code", "Builder", "SWBS Subsystem", "SWBS", "SWBS basis"]

# The 4 MATERIALIZED regex columns. The classification columns (PIID Candidate Hulls, Assigned Hull,
# Hull Assignment Scope / Basis, Hull Confidence) are LIVE formulas on the sheet - not written here.
HULL_COLS = ["Direct Hull Text", "Direct Hull Count",
             "Prime Requirement Hull Text", "Prime Requirement Hull Count"]

# Classification columns this script USED to materialize (now live formulas). They are dropped on
# re-tag so an upgraded CSV does not keep stale static copies alongside the new sheet formulas.
_LEGACY_CLASS = ["PIID Candidate Hulls", "Assigned Hull", "Hull Assignment Scope",
                 "Hull Assignment Basis", "Hull Confidence"]
DROP_COLS = set(HULL_COLS) | set(_LEGACY_CLASS)


def build() -> None:
    fam_info = load_map()
    with TX_CSV.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        rows = list(reader)

    # idempotent: drop any prior hull columns (the 4 regex + the 5 now-formula classifications),
    # keep the rest in order, then re-append only the 4 regex columns.
    keep = [i for i, h in enumerate(header) if h not in DROP_COLS]
    base_header = [header[i] for i in keep]
    missing_swbs = [c for c in SWBS_COLS if c not in base_header]
    assert not missing_swbs, (
        f"SWBS columns absent - run tag_ddg_transactions_swbs.py first: {missing_swbs}")

    idx = {h: base_header.index(h) for h in
           ("Subaward Number", "Subaward Description", "Description of Requirement",
            "Prime PIID", "Subaward Report ID", "Subawardee Vendor Name")}

    out_rows = []
    exceptions = []
    n_conflict = n_multi = 0
    for r in rows:
        base = [r[i] if i < len(r) else "" for i in keep]

        def g(col):
            return base[idx[col]] if idx[col] < len(base) else ""

        piid = (g("Prime PIID") or "").strip()
        direct = parse_hulls(g("Subaward Number"), g("Subaward Description"))
        req = parse_hulls(g("Description of Requirement"))
        out_rows.append(base + [hull_str(direct), len(direct), hull_str(req), len(req)])

        # exception log: the conflict / multi-hull rows (resolve() is the shared rule the formulas
        # reproduce). These carry a blank Assigned Hull on the sheet, so they never roll up.
        _assigned, scope, _basis, conf = resolve(piid, direct, req, fam_info)
        if conf == "X":
            issue = ("Multi-hull (count>1)" if scope == "Multi-hull"
                     else "Direct hull outside PIID family")
            if scope == "Multi-hull":
                n_multi += 1
            else:
                n_conflict += 1
            cand = fam_info.get(piid, {}).get("candidates", "")
            desc = " ".join((g("Subaward Description") or "").split())[:120]
            exceptions.append([
                (g("Subaward Report ID") or "").strip(), piid,
                (g("Subawardee Vendor Name") or "").strip(), issue,
                hull_str(direct), cand, desc,
            ])

    with TX_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(base_header + HULL_COLS)
        w.writerows(out_rows)

    with EXC_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Subaward Report ID", "Prime PIID", "Subawardee Vendor Name", "Issue",
                    "Direct Hull Text", "PIID Candidate Hulls", "Subaward Description (excerpt)"])
        w.writerows(exceptions)

    print("\n==== tagged DDG transactions with regex hull evidence ====")
    print(f"file: {TX_CSV}")
    print(f"rows                              : {len(out_rows)}")
    print(f"columns                           : {len(base_header) + len(HULL_COLS)}")
    print("classification (Assigned Hull etc.) is a LIVE formula on the sheet - not written here.")
    print(f"exception log: {EXC_CSV}")
    print(f"  conflicts (out-of-family)       : {n_conflict}")
    print(f"  multi-hull rows                 : {n_multi}")


if __name__ == "__main__":
    build()
