"""tag_ddg_transactions_swbs - add the SWBS key onto the canonical DDG transactions CSV.

The DDG Subaward SWBS dimension lives ON the real transaction sheet (no separate SWBS
sheet): this step appends to extracted/ddg_subaward_transactions.csv the two MATERIALIZED
columns the SWBS roll-up needs - `HII Work-Item Code` (joined from the HII-Ingalls SWBS
package by Subaward Report ID) and `Builder` (HII-Ingalls for the six HII prime PIIDs,
else GD-BIW) - plus blank placeholders for `SWBS Subsystem`, `SWBS`, `SWBS basis`, which
the sheet fills as live crosswalk-lookup formulas. Idempotent: re-running re-derives the
five columns rather than duplicating them.

Why a separate tagging step (not build_program_transactions.py): the canonical generator
reads the raw FSRS JSON via a tam scope file that the tam/ restructure relocated, so it
can't run right now. This tagger only needs the already-built CSV + the SWBS package, so
it sidesteps that. Run order when the generator is restored:
    python3 scripts/build_program_transactions.py ddg   # regenerates the base 50 cols
    python3 scripts/tag_ddg_transactions_swbs.py         # re-appends the SWBS columns
    python3 build_workbook.py
"""
from __future__ import annotations

import csv
from pathlib import Path

from _paths import AC, EXTRACTED  # noqa: E402  (anchors derive from __file__, so a checkout move needs no edit)
PKG = AC / "ddg_hii_swbs_subaward_package"

TX_CSV = EXTRACTED / "ddg_subaward_transactions.csv"
REC_CSV = PKG / "hii_ddg_record_components.csv"

# The six HII-Ingalls prime PIIDs (the SWBS-eligible hull builder); every other DDG prime
# is GD-Bath Iron Works, whose subawards carry no SWBS coding.
HII_PIIDS = {"N0002411C2307", "N0002411C2309", "N0002412C2312",
             "N0002413C2307", "N0002418C2307", "N0002423C2307"}

# Appended columns: 2 materialized + 3 formula placeholders (filled on the sheet).
SWBS_COLS = ["HII Work-Item Code", "Builder", "SWBS Subsystem", "SWBS", "SWBS basis"]


def load_codes() -> dict[str, str]:
    """Subaward Report ID -> parsed HII work-item code (blank if none)."""
    out: dict[str, str] = {}
    with REC_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            rid = (r.get("sub_report_id") or "").strip()
            if rid:
                out[rid] = (r.get("code") or "").strip()
    return out


def build() -> None:
    codes = load_codes()
    with TX_CSV.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        rows = list(reader)

    # idempotent: drop any prior SWBS columns, keep the rest in order
    keep = [i for i, h in enumerate(header) if h not in SWBS_COLS]
    base_header = [header[i] for i in keep]
    rid_idx = base_header.index("Subaward Report ID")
    piid_idx = base_header.index("Prime PIID")

    out_rows = []
    n_hii = n_coded = 0
    for r in rows:
        base = [r[i] if i < len(r) else "" for i in keep]
        rid = (base[rid_idx] or "").strip()
        piid = (base[piid_idx] or "").strip()
        builder = "HII-Ingalls" if piid in HII_PIIDS else "GD-BIW"
        code = codes.get(rid, "")
        if builder == "HII-Ingalls":
            n_hii += 1
        if code:
            n_coded += 1
        out_rows.append(base + [code, builder, "", "", ""])   # SWBS cols are formulas on the sheet

    with TX_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(base_header + SWBS_COLS)
        w.writerows(out_rows)

    print("\n==== tagged DDG transactions with SWBS key ====")
    print(f"file: {TX_CSV}")
    print(f"rows                              : {len(out_rows)}")
    print(f"columns                           : {len(base_header) + len(SWBS_COLS)}")
    print(f"  Builder HII-Ingalls             : {n_hii}")
    print(f"  rows carrying an HII work-item code: {n_coded}")
    print("SWBS Subsystem / SWBS / SWBS basis left blank -> filled by formula on the sheet.")


if __name__ == "__main__":
    build()
