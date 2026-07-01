"""tag_ddg_transactions_lifecycle - materialize the per-transaction construction-lifecycle columns.

The lifecycle analogue of tag_ddg_transactions_hulls: it appends to extracted/ddg_subaward_transactions.csv
the per-ROW lifecycle attributes that a date-window join cannot be a live Excel formula. Two axes
(see _lifecycle.py / the briefing):

  - A/B (exact hull): the hull is known, so the purchase date maps to ONE construction stage.
      `Lifecycle Stage` (Long-lead / Construction / Outfit / test / Post-delivery / ...),
      `Lifecycle Stage Basis` (the reason), `Date Source Confidence` (Actual / Projected / Estimated).
  - C/D (family-level): the hull is unknown, so timing NARROWS the candidate set (it never assigns a
      hull). `Narrowing Result` (Single / 2-3 / Still family-level / Exception / No data) +
      `Lifecycle Confidence` (its own axis) + `Date Source Confidence`. `Lifecycle Stage` stays blank -
      the per-candidate stages live on DDG C-D Lifecycle Candidates (build_ddg_cd_lifecycle.py).
  - X / unassigned: all blank.

These columns feed two live roll-ups: DDG Hull x Lifecycle Stage SUMIFS on (Assigned Hull x Lifecycle
Stage); DDG C-D Lifecycle Coverage SUMIFS on Narrowing Result. The hull family + assignment are
re-derived with the shared _hull_logic.resolve() (the same rule the sheet formulas reproduce), and the
narrowing with _lifecycle.narrow() (the same rule build_ddg_cd_lifecycle expands) - so the tx columns
and the candidate grain are consistent (the partition integrity check diffs them).

Idempotent. Run AFTER tag_ddg_transactions_hulls.py (needs the regex hull-evidence columns):
    python3 scripts/tag_ddg_transactions_swbs.py
    python3 scripts/tag_ddg_transactions_hulls.py
    python3 scripts/tag_ddg_transactions_lifecycle.py    # these 5 lifecycle columns
    python3 build_workbook.py
"""
from __future__ import annotations

import csv
from collections import Counter

from _paths import EXTRACTED  # noqa: E402
from _hull_logic import load_map, hull_set, resolve  # noqa: E402
from _lifecycle import (  # noqa: E402
    load_milestones, stage_for, reason_for, narrow, parse_iso, _hull_num,
)

TX_CSV = EXTRACTED / "ddg_subaward_transactions.csv"

# Must already be on the CSV (the hull tagger's regex evidence) - the lifecycle columns sit after them.
REQUIRED = ["Direct Hull Text", "Prime Requirement Hull Text", "Prime PIID", "Subaward Date"]

# The 5 MATERIALIZED lifecycle columns this step appends.
LIFECYCLE_COLS = ["Lifecycle Stage", "Lifecycle Stage Basis", "Date Source Confidence",
                  "Narrowing Result", "Lifecycle Confidence"]


def build() -> None:
    fam_info = load_map()
    milestones = load_milestones()
    with TX_CSV.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        rows = list(reader)

    # idempotent: drop any prior lifecycle columns, keep the rest in order, re-append.
    keep = [i for i, h in enumerate(header) if h not in LIFECYCLE_COLS]
    base_header = [header[i] for i in keep]
    missing = [c for c in REQUIRED if c not in base_header]
    assert not missing, f"required columns absent - run tag_ddg_transactions_hulls.py first: {missing}"
    idx = {h: base_header.index(h) for h in REQUIRED}

    out_rows = []
    stage_hist: Counter = Counter()      # A/B stage distribution
    narrow_hist: Counter = Counter()     # C/D narrowing-result distribution
    for r in rows:
        base = [r[i] if i < len(r) else "" for i in keep]

        def g(col):
            return base[idx[col]] if idx[col] < len(base) else ""

        piid = (g("Prime PIID") or "").strip()
        direct = hull_set(g("Direct Hull Text"))
        req = hull_set(g("Prime Requirement Hull Text"))
        assigned, _scope, _basis, conf = resolve(piid, direct, req, fam_info)
        d = parse_iso(g("Subaward Date"))

        stage = basis = date_conf = narrowing = lconf = ""
        if conf in ("A", "B") and assigned:
            hull = _hull_num(assigned)
            win = milestones.get(hull)
            if win is not None:
                stage, _match, date_conf = stage_for(d, win)
                basis = reason_for(hull, stage, _match, d, win)
            else:
                stage, basis, date_conf = "No schedule data", f"No schedule dates for {assigned}", ""
            stage_hist[stage] += 1
        elif conf in ("C", "D"):
            fam = fam_info.get(piid, {}).get("family", set())
            nr = narrow(fam, d, milestones)
            narrowing, lconf, date_conf = nr.narrowing_result, nr.lifecycle_confidence, nr.date_conf
            narrow_hist[narrowing] += 1

        out_rows.append(base + [stage, basis, date_conf, narrowing, lconf])

    with TX_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(base_header + LIFECYCLE_COLS)
        w.writerows(out_rows)

    print("\n==== tagged DDG transactions with construction-lifecycle columns ====")
    print(f"file: {TX_CSV}")
    print(f"rows                              : {len(out_rows)}")
    print(f"columns                           : {len(base_header) + len(LIFECYCLE_COLS)}")
    print("A/B exact-hull stage distribution :")
    for s, n in stage_hist.most_common():
        print(f"    {s:<24}: {n}")
    print("C/D narrowing-result distribution :")
    for s, n in narrow_hist.most_common():
        print(f"    {s:<28}: {n}")
    print("Lifecycle Stage is blank for C/D (per-candidate stages live on the Candidates sheet).")


if __name__ == "__main__":
    build()
