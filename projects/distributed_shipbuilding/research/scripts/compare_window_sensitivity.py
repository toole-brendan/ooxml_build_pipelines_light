#!/usr/bin/env python3
"""
Compare lane gate readings across analysis windows (window-sensitivity check).

Reads the headline FY22-25 worktype_scorecard.csv plus the sensitivity copies
produced by re-running compute_competability_signals.py + build_target_list.py
under COMP_WINDOW / COMP_OUTDIR (sensitivity_fy20_25/, sensitivity_fy19_25/),
re-applies build_target_list.gate() to each, and writes one row per lane with
gate / pool / HHI / credible-entrant-rate / pre-window-share per window plus a
gate_stable flag.

The unbucketed lane is excluded (never gated by rule).

Output: extracted/window_sensitivity_comparison.csv + console table.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import EXTRACTED, UNBUCKETED
from build_target_list import gate

WINDOWS = [
    ("fy22_25", EXTRACTED),                          # headline
    ("fy20_25", EXTRACTED / "sensitivity_fy20_25"),
    ("fy19_25", EXTRACTED / "sensitivity_fy19_25"),
]


def load_scorecard(d: Path) -> dict[tuple[str, str], dict]:
    with (d / "worktype_scorecard.csv").open(encoding="utf-8-sig", newline="") as fh:
        return {(r["program"], r["work_type"]): r for r in csv.DictReader(fh)}


def main() -> int:
    cards = {w: load_scorecard(d) for w, d in WINDOWS}
    lanes = [k for k in sorted(cards["fy22_25"]) if k[1] != UNBUCKETED]

    rows = []
    for program, ln in lanes:
        row = {"program": program, "work_type": ln}
        gates = []
        for w, _ in WINDOWS:
            r = cards[w][(program, ln)]
            g = gate(r)
            gates.append(g)
            row[f"gate_{w}"] = g
            row[f"pool_$M_{w}"] = r["pool_dollars_fy22_25_$M"]
            row[f"hhi_{w}"] = r["hhi_fy22_25"]
            row[f"cred_entrant_rate_{w}"] = r["credible_entrant_rate"]
            row[f"pre_window_share_{w}"] = r["pre_fy22_record_share"]
            row[f"censored_{w}"] = float(r["pre_fy22_record_share"] or 0) < 0.15
        row["gate_stable"] = len(set(gates)) == 1
        rows.append(row)

    out = EXTRACTED / "window_sensitivity_comparison.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    flips = [r for r in rows if not r["gate_stable"]]
    print(f"{'lane':<24} {'FY22-25':<15} {'FY20-25':<15} {'FY19-25':<15}")
    for r in rows:
        mark = "  <-- FLIP" if not r["gate_stable"] else ""
        print(f"{r['program']:<11} {r['work_type']:<12} "
              f"{r['gate_fy22_25']:<15} {r['gate_fy20_25']:<15} "
              f"{r['gate_fy19_25']:<15}{mark}")
    print(f"\n{len(rows) - len(flips)}/{len(rows)} lane gates stable across all "
          f"three windows; wrote {out.name}")
    for r in flips:
        print(f"  FLIP: {r['program']}/{r['work_type']} — "
              + ", ".join(f"{w}={r[f'gate_{w}']} (hhi {r[f'hhi_{w}']})"
                          for w, _ in WINDOWS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
