"""verify_crosstab - prove the native _crosstab builders reproduce the v4.33 cross-tab
formula strings byte-for-byte.

Transitional QA: the native Services §1/§2/§3 (and the Depot/Output SUMIFS blocks) are
loops over the axis constants in workbook_mro.sheets._crosstab. Because the structured-ref
SUMIFS strings are position-independent, a faithful loop produces the *exact* extracted
formula text - so this check (no soffice needed) is a fast, deterministic equivalence gate
that runs before the heavyweight tie_out recompute. Retires with extracted/v433 in Phase 4.

Run:  python qa/verify_crosstab.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
sys.path.insert(0, str(_HERE.parents[1]))          # projects/mro/workbook/ -> workbook_mro
sys.path.insert(0, str(_HERE.parents[5]))          # workspace root -> workbook_core

from workbook_mro.sheets import _crosstab as X  # noqa: E402

V433 = _HERE.parents[1] / "extracted" / "v433"


def _col_letter(n: int) -> str:           # 0-indexed
    s, n = "", n + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _load(slug: str):
    d = json.load((V433 / f"{slug}.json").open(encoding="utf-8"))
    return {(c["r"], c["c"]): c for c in d["cells"]}


def _check_section(rc, data_lo, data_hi, total_row, col0, axis, mk_crit, total_col):
    """Generate every cell formula for a cross-tab section; diff vs the JSON."""
    diffs, total = [], 0
    # data rows: one SUMIFS per axis column + a SUM(...) total column
    for i, (code, _desc) in enumerate(X.PSC_ROWS):
        r = data_lo + i
        for j, label in enumerate(axis):
            c = col0 + j
            want = X.sumifs_award("FY2025 Obligation", *mk_crit(code, label))
            total += 1
            got = rc.get((r, c), {}).get("p")
            if got != want:
                diffs.append((r, c, want, got))
        # total column = SUM(first..last) across this row
        first, last = _col_letter(col0), _col_letter(total_col - 1)
        want = f"SUM({first}{r}:{last}{r})"
        total += 1
        got = rc.get((r, total_col), {}).get("p")
        if got != want:
            diffs.append((r, total_col, want, got))
    # totals row: SUM(col{lo}:col{hi}) per column, including the total column
    for c in range(col0, total_col + 1):
        L = _col_letter(c)
        want = f"SUM({L}{data_lo}:{L}{data_hi})"
        total += 1
        got = rc.get((total_row, c), {}).get("p")
        if got != want:
            diffs.append((total_row, c, want, got))
    return total, diffs


def main() -> int:
    rc = _load("Services")
    specs = [
        # name, data_lo, data_hi, total_row, col0, axis, mk_crit, total_col
        ("§1 vessel type", 6, 70, 71, 2, X.VESSEL_TYPES,
         lambda code, lab: [("PSC", code), ("Vessel Type", X.axis_crit(lab))], 19),
        ("§2 Navy hull", 76, 140, 141, 2, X.HULL_PROGRAMS_NAVY,
         lambda code, lab: [("PSC", code), ("Hull Program", X.axis_crit(lab)), ("Service", "Navy")], 31),
        ("§3 CG hull", 145, 209, 210, 2, X.HULL_PROGRAMS_CG,
         lambda code, lab: [("PSC", code), ("Hull Program", X.axis_crit(lab)), ("Service", "Coast Guard")], 18),
    ]
    ok = True
    for name, lo, hi, tr, col0, axis, mk, tc in specs:
        n, diffs = _check_section(rc, lo, hi, tr, col0, axis, mk, tc)
        status = "OK" if not diffs else f"FAIL ({len(diffs)} diffs)"
        print(f"  {name}: {n} formulas  {status}")
        for r, c, want, got in diffs[:4]:
            print(f"    r{r}c{c}: want {want!r}  got {got!r}")
        ok = ok and not diffs
    print("CROSSTAB VERIFY", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
