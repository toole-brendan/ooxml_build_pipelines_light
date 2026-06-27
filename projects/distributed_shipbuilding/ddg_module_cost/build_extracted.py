"""build_extracted.py - mirror the DDG-51 ship-cost slice from the Master TAM workbook.

This workbook's only data input is the DDG-51 (LI 2122) SCN-budget slice. Rather
than re-transcribe numbers (and risk drift), this script READS the Master TAM
workbook's already-extracted CSVs and writes the DDG-51 slice into our local
extracted/ddg_ship_cost.csv. The TAM extracted/ dir is the single source of truth;
re-run this only if that slice changes.

Cross-file Excel links are not the repo pattern (accessor cell-refs resolve only
within their own workbook), so we mirror the VALUES at build time and cite the
source on the Ship Cost Basis tab.

Source (../tam/master/extracted/):
    scn_budget.csv     P-5c cost categories, then-year $M (FY2022-2027)
    fydp_outyears.csv  PB2027 P-40 quantities by FY
    deflators.csv      Green Book factor (then-year -> constant FY2026 $)

Output (extracted/):
    ddg_ship_cost.csv  fy, <9 DDG cost categories>, qty, deflator_factor

Run:  python3 build_extracted.py
"""
from __future__ import annotations

import csv
from pathlib import Path

_HERE = Path(__file__).resolve()
TAM_EXTRACTED = _HERE.parent / ".." / "tam" / "master" / "extracted"
OUT = _HERE.parent / "extracted"
OUT.mkdir(exist_ok=True)

_LI_DDG = "2122"
_FY = [2022, 2023, 2024, 2025, 2026, 2027]

# DDG-51 carries 9 of the P-5c categories (no propulsion / technology_insertion).
# Order them outermost-first so the data tab reads structure -> equipment -> total.
_DDG_CATS = ["basic", "plans", "hme", "electronics", "ordnance",
             "other_cost", "gfe", "change_orders", "total"]


def _read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _num(x) -> str:
    """Then-year cell -> trimmed numeric string, or '' for blank/dash."""
    s = (str(x) if x is not None else "").strip().replace(",", "")
    if s in ("", "-"):
        return ""
    try:
        return repr(float(s)) if "." in s or "e" in s.lower() else str(int(s))
    except ValueError:
        return ""


def build_ddg_ship_cost() -> None:
    scn = {int(r["fy"]): r for r in _read(TAM_EXTRACTED / "scn_budget.csv")
           if r.get("li", "").strip() == _LI_DDG}
    fydp = {int(r["fy"]): r for r in _read(TAM_EXTRACTED / "fydp_outyears.csv")
            if r.get("li", "").strip() == _LI_DDG}
    defl = {int(r["fy"]): r for r in _read(TAM_EXTRACTED / "deflators.csv")}

    header = ["fy"] + _DDG_CATS + ["qty", "deflator_factor"]
    rows = []
    for fy in _FY:
        s = scn.get(fy, {})
        cats = [_num(s.get(cat)) for cat in _DDG_CATS]
        qty = _num((fydp.get(fy) or {}).get("qty"))
        factor = _num((defl.get(fy) or {}).get("factor_const_fy2026"))
        rows.append([fy] + cats + [qty, factor])

    with (OUT / "ddg_ship_cost.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote ddg_ship_cost.csv  ({len(rows)} rows, FY{_FY[0]}-{_FY[-1]})")


def main() -> int:
    print("build_extracted: mirroring DDG-51 slice from ../tam/master/extracted/ -> extracted/")
    if not TAM_EXTRACTED.exists():
        raise SystemExit(f"TAM extracted dir not found: {TAM_EXTRACTED.resolve()}")
    build_ddg_ship_cost()
    print("done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
