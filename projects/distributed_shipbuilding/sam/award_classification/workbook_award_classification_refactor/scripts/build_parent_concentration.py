"""build_parent_concentration - capability-domain concentration at UEI vs ULTIMATE-PARENT grain.

NOTE (2026-06-22): the Parent Concentration *sheet* is now fully LIVE - it computes these metrics
with formulas off the program-vendor sheets (parent grain via three hidden per-row helpers:
Parent Key / Parent Domain $ / Parent Domain Rows), exactly like Domain Concentration. So
extracted/parent_concentration.csv is no longer wired into the build; this script is kept only as
an offline CROSS-CHECK of the live formulas (its output matches the live formula semantics on
every program x domain row). The workbook no longer reads the CSV.

Reviewer finding #6: the live Domain Concentration sheet treats each UEI as an independent
firm, but Supplier Master carries standardized parents, so the UEI view understates strategic
concentration. This emits extracted/parent_concentration.csv with BOTH grains per
(program x domain) so the numbers can be cross-checked against the live sheet.

Computed at build from the same inputs the live sheet resolves from - the archetype resolution
(override-first -> NAICS-6 map -> D0), the transaction-grain FY2026$ deflation, and the
Supplier Master parent map - so it stays consistent with each rebuild. Concentration ratios use
POSITIVE spend (consistent with the live HHI and the corrected Top-1 share).

    python3 scripts/build_parent_concentration.py
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "extracted"
TAX = ROOT / "workbook_award_classification_refactor/sheets/_taxonomy.py"

_PROG = {"ddg": "DDG", "virginia": "Virginia", "columbia": "Columbia"}


def _f(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def _fed_fy(date: str) -> int | None:
    if not date or len(date) < 7:
        return None
    y, m = int(date[:4]), int(date[5:7])
    return y + 1 if m >= 10 else y


def _domains() -> list[tuple[str, str]]:
    import re
    txt = TAX.read_text()
    blk = txt[txt.index("DOMAINS"):txt.index("OUTPUTS")]
    return re.findall(r'\("(D\d+)",\s*"([^"]+)"', blk)


def _factors() -> dict[str, float]:
    """fed-FY -> deflate-to-FY2026 factor (102.10 / index); <=FY12 uses the FY2002 index."""
    base = None
    rows = {}
    for r in csv.DictReader((EXTRACTED / "deflators.csv").open(encoding="utf-8-sig")):
        rows[r["FY"]] = _f(r["Procurement TOA (FY2025=100)"])
    base = rows["FY2026"]
    out = {}
    for fy in range(2013, 2027):
        out[fy] = base / rows[f"FY{fy}"]
    le = base / rows["≤FY12"]
    for fy in range(1990, 2013):
        out[fy] = le
    return out


def _resolve_d():
    """(program, UEI) -> resolved Capability Domain (override-first -> NAICS-6 map -> D0)."""
    ov = {}
    for r in csv.DictReader((EXTRACTED / "vendor_archetype_overrides.csv").open(encoding="utf-8-sig")):
        d = (r["Capability Domain (D)"] or "").strip()
        if d:
            ov[(r["Program"].strip(), r["Subawardee UEI"].strip())] = d
    nm = {}
    for r in csv.DictReader((EXTRACTED / "naics6_archetype_map.csv").open(encoding="utf-8-sig")):
        d = (r["Capability Domain (D)"] or "").strip()
        if d:
            nm[r["NAICS-6"].strip()] = d
    sm_naics, parent = {}, {}
    for r in csv.DictReader((EXTRACTED / "supplier_master.csv").open(encoding="utf-8-sig")):
        key = (r["Program"].strip(), r["Subawardee UEI"].strip())
        sm_naics[key] = (r["Primary NAICS-6"] or "").strip()
        parent[key] = (r["Parent UEI"] or "").strip() or key[1]
    resolved = {}
    for key, naics in sm_naics.items():
        resolved[key] = ov.get(key) or nm.get(naics) or "D0"
    return resolved, parent


def _dollars(factors):
    """(program, UEI) -> lifetime FY2026$ (sum of deflated nominal subaward amounts)."""
    out: dict[tuple, float] = {}
    for stem, prog in _PROG.items():
        for x in list(csv.reader((EXTRACTED / f"{stem}_subaward_transactions.csv").open(encoding="utf-8")))[1:]:
            if len(x) < 26:
                continue
            uei = x[0].strip()
            if not uei:
                continue
            fy = _fed_fy(x[8])
            fac = factors.get(fy, 1.0) if fy else 1.0
            out[(prog, uei)] = out.get((prog, uei), 0.0) + _f(x[10]) / 1e6 * fac
    return out


def _conc(values: list[float]):
    """(top1_share, hhi, eff_firms) over POSITIVE values; (None,None,None) if no positive mass."""
    pos = [v for v in values if v > 0]
    tot = sum(pos)
    if tot <= 0:
        return None, None, None
    shares = [v / tot for v in pos]
    hhi = sum(s * s for s in shares)
    return max(pos) / tot, hhi, (1 / hhi if hhi else None)


def compute():
    factors = _factors()
    resolved, parent = _resolve_d()
    dollars = _dollars(factors)
    domains = _domains()
    rows = []
    for prog in ("Virginia", "Columbia", "DDG"):
        for code, name in domains:
            members = {uei: dollars.get((prog, uei), 0.0)
                       for (p, uei), d in resolved.items() if p == prog and d == code}
            if not members:
                continue
            u_t1, u_hhi, u_eff = _conc(list(members.values()))
            if u_t1 is None:
                continue
            pagg: dict[str, float] = {}
            for uei, v in members.items():
                pagg[parent.get((prog, uei), uei)] = pagg.get(parent.get((prog, uei), uei), 0.0) + v
            p_t1, p_hhi, p_eff = _conc(list(pagg.values()))
            rows.append([prog, code, name,
                         f"{u_t1 * 100:.1f}", f"{u_hhi:.3f}", f"{u_eff:.2f}",
                         sum(1 for v in members.values() if v > 0),
                         f"{p_t1 * 100:.1f}", f"{p_hhi:.3f}", f"{p_eff:.2f}",
                         sum(1 for v in pagg.values() if v > 0)])
    return rows


def main(write=True):
    rows = compute()
    if write:
        with (EXTRACTED / "parent_concentration.csv").open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["Program", "Domain", "Domain Name",
                        "UEI Top-1 %", "UEI HHI", "UEI Eff Firms", "UEI Suppliers",
                        "Parent Top-1 %", "Parent HHI", "Parent Eff Firms", "Parent Firms"])
            w.writerows(rows)
        print(f"wrote {EXTRACTED / 'parent_concentration.csv'} : {len(rows)} (program x domain) rows")
    return rows


if __name__ == "__main__":
    main()
