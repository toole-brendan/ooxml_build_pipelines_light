#!/usr/bin/env python3
"""
Pull General Dynamics 10-K data from EDGAR for FY2020-FY2025 (FY ends Dec 31).

GD reports 4 segments: Aerospace, Marine Systems, Combat Systems, Technologies.
The Marine Systems segment includes BIW (DDG-51 prime) + Electric Boat (submarine
prime) + NASSCO (auxiliary ships, San Diego). Even though we can't extract a
BIW-only number from the segment data, the segment total + program narrative gives
us a denominator for triangulating BIW outsourcing.

Outputs to edgar_research/:
  - gd_10k_files/<FY>/              raw HTML cache per FY
  - gd_marine_systems_segment.csv   Marine Systems segment financials per FY
  - gd_program_narrative.csv        DDG + BIW + destroyer keyword snippets
  - gd_summary_memo.md              prose writeup
"""
import csv
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT = REPO / "edgar_research"
CACHE = OUT / "gd_10k_files"
CACHE.mkdir(parents=True, exist_ok=True)

USER_AGENT = "ddg-research toole.brendan@gmail.com"

# 10-K filings (accession numbers from EDGAR submissions JSON)
TEN_K_FILINGS = [
    (2020, "0000040533-21-000010"),
    (2021, "0000040533-22-000007"),
    (2022, "0000040533-23-000014"),
    (2023, "0000040533-24-000007"),
    (2024, "0000040533-25-000008"),
    (2025, "0000040533-26-000006"),
]

# CIK 0000040533 = General Dynamics Corporation
BASE_ARCHIVE = "https://www.sec.gov/Archives/edgar/data/40533"


def fetch(url, out_path):
    out_path = Path(out_path)
    if out_path.exists() and out_path.stat().st_size > 1000:
        return True
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["curl", "-sS", "--max-time", "60", "-A", USER_AGENT, url, "-o", str(out_path)],
        capture_output=True, text=True, timeout=90,
    )
    if result.returncode != 0:
        print(f"  curl rc={result.returncode}: {result.stderr[:200]}", flush=True)
        return False
    return out_path.exists() and out_path.stat().st_size > 0


def html_to_text(html_path):
    class T(HTMLParser):
        def __init__(self): super().__init__(); self.t = []
        def handle_data(self, d): self.t.append(d)
    p = T()
    try: p.feed(Path(html_path).read_text(errors="replace"))
    except Exception: return ""
    return re.sub(r"\s+", " ", " ".join(p.t)).strip()


def pull_filing(fy, accn):
    accn_nodash = accn.replace("-", "")
    base = f"{BASE_ARCHIVE}/{accn_nodash}"
    fy_dir = CACHE / str(fy)
    fy_dir.mkdir(exist_ok=True)

    if not fetch(f"{base}/index.json", fy_dir / "index.json"):
        print(f"  FY{fy}: failed to fetch index")
        return None
    if not fetch(f"{base}/MetaLinks.json", fy_dir / "MetaLinks.json"):
        print(f"  FY{fy}: failed to fetch MetaLinks")
        return None

    metalinks = json.load(open(fy_dir / "MetaLinks.json"))
    instance = list(metalinks["instance"].keys())[0]
    reports = metalinks["instance"][instance]["report"]
    primary_doc = instance

    targets = {}
    wanted = {"Segment Information", "Description of the Business", "Description of Business",
              "Revenue", "Revenue Recognition", "Business Segment Information"}
    for rid, rdata in reports.items():
        short = rdata.get("shortName", "")
        if short in wanted and short not in targets:
            targets[short] = rid

    for short, r in targets.items():
        fetch(f"{base}/{r}.htm", fy_dir / f"{r}.htm")

    fetch(f"{base}/{primary_doc}", fy_dir / "10k_main.htm")

    return {"fy": fy, "accn": accn, "primary_doc": primary_doc,
            "targets": targets, "dir": fy_dir}


def numify(s):
    if s is None: return None
    s = str(s).replace(",", "").replace("$", "").strip()
    if s in ("—", "-", ""): return 0
    try: return int(s)
    except ValueError: return None


def parse_segment_table(seg_text):
    """GD's segment table — TWO formats across FY20-FY25 books, both with the
    main income-statement table containing 9 numbers per "Marine Systems" row.

    OLD format (FY20-FY23 books): rev(3) + op_earnings(3) + identifiable_assets(3)
      e.g. "Marine Systems 9,979 9,183 8,502 854 785 761 9,871 9,027 8,245"
       → rev = 9,979 (Y) / 9,183 (Y-1) / 8,502 (Y-2)
       → op_earnings = 854 / 785 / 761
       → assets = 9,871 / 9,027 / 8,245

    NEW format (FY24+ books): rev(3) + cost_of_sales(3) [in parens=negative] + op_earnings(3)
      e.g. "Marine Systems 14,343 12,461 11,040 (13,408) (11,587) (10,143) 935 874 897"
       → rev = 14,343 / 12,461 / 11,040
       → cost_of_sales = -13,408 / -11,587 / -10,143
       → op_earnings = 935 / 874 / 897

    Detection rule: if any of positions 4-6 contain parens (negative), it's NEW format,
    use positions 7-9 as op earnings. Otherwise it's OLD, use positions 4-6.

    There's a second table with 9 different numbers (assets/capex/depreciation) — we
    skip that by only parsing the FIRST occurrence of the income-statement row.
    """
    out = {}
    m_header = re.search(r"(\d{4})\s+(\d{4})\s+(\d{4})\b", seg_text)
    if not m_header:
        return out
    years = [int(m_header.group(i)) for i in (1,2,3)]

    # Capture 9 cells after "Marine Systems", each optionally wrapped in parens
    # (negative). The (\()? group tells us if the cell was parens-wrapped.
    rx = (r"Marine Systems"
          + r"\s+\$?\s*(\()?\s*([\d,]+)\s*\)?" * 9)
    matches = list(re.finditer(rx, seg_text))
    if not matches:
        return out

    # Take the FIRST occurrence — that's the income-statement row (revenue + COS + OpEarn
    # or revenue + OpEarn + Assets). Subsequent occurrences are the assets/capex table.
    m = matches[0]
    # Groups: each cell is two groups (paren-flag, number). 9 cells × 2 = 18 groups.
    cells = []
    for i in range(9):
        paren = m.group(1 + 2*i)
        num = numify(m.group(2 + 2*i))
        cells.append({"value": num, "negative": paren == "("})

    rev_cells = cells[0:3]
    mid_cells = cells[3:6]
    last_cells = cells[6:9]

    # Detection: if any middle cell is in parens, it's the new format (COS) — use last
    is_new_format = any(c["negative"] for c in mid_cells)
    if is_new_format:
        op_cells = last_cells
        cos_cells = mid_cells
        assets_cells = None
    else:
        op_cells = mid_cells
        cos_cells = None
        assets_cells = last_cells

    for col, fy in enumerate(years):
        rec = {"fy_in_note": fy}
        rec["marine_systems_revenue_$M"] = rev_cells[col]["value"]
        rec["marine_systems_op_earnings_$M"] = op_cells[col]["value"]
        if cos_cells:
            v = cos_cells[col]["value"]
            rec["marine_systems_cost_of_sales_$M"] = -v if v else 0
        if assets_cells:
            rec["marine_systems_assets_$M"] = assets_cells[col]["value"]
        rec["table_format"] = "new" if is_new_format else "old"
        if rec["marine_systems_revenue_$M"]:
            out[fy] = rec
    return out


KEYWORDS = [
    ("DDG",            r"\bDDG\b"),
    ("DDG 51 / 1000",  r"\bDDG\s*(?:51|1000)\b"),
    ("Arleigh Burke",  r"\bArleigh\s*Burke\b"),
    ("Flight III",     r"\bFlight\s*III\b"),
    ("Destroyer",      r"\bdestroyer\b"),
    ("Bath Iron Works", r"\bBath\s*Iron\s*Works\b"),
    ("BIW",            r"\bBIW\b"),
    ("Marine Systems", r"\bMarine\s*Systems\b"),
    ("Aegis",          r"\bAegis\b"),
    ("Electric Boat",  r"\bElectric\s*Boat\b"),
    ("NASSCO",         r"\bNASSCO\b"),
    ("Virginia (sub)", r"\bVirginia\s+(?:Class|Block)\b"),
    ("Columbia (sub)", r"\bColumbia\s+(?:Class|Block)\b"),
    ("Backlog",        r"\bbacklog\b"),
    ("MYP / Multi-Year", r"\bmulti[- ]?year\b"),
]


def extract_program_narrative(full_text, fy):
    snippets = []
    seen = set()
    for label, pattern in KEYWORDS:
        for m in re.finditer(pattern, full_text, re.I):
            start = max(0, m.start() - 200)
            end = min(len(full_text), m.end() + 400)
            ctx = full_text[start:end]
            ctx = re.sub(r"^[^.]*\.\s*", "", ctx, count=1)
            m2 = re.search(r"\.[A-Z]", ctx)
            if m2: ctx = ctx[:m2.start()+1]
            ctx = ctx.strip()
            if len(ctx) < 50 or len(ctx) > 800: continue
            key = ctx[:120]
            if key in seen: continue
            seen.add(key)
            has_dollar = bool(re.search(r"\$\s*[\d,\.]+\s*(billion|million|B|M)", ctx, re.IGNORECASE))
            has_count = bool(re.search(r"\b\d+\s+(destroyers?|ships?|DDGs?|submarines?)\b", ctx, re.IGNORECASE))
            if has_dollar or has_count:
                snippets.append({
                    "fy_book": fy, "keyword": label,
                    "has_dollar": "Y" if has_dollar else "",
                    "snippet": ctx,
                })
    return snippets


def main():
    print(f"=== GD 10-K research pull (Marine Systems) ===\n")

    filings = []
    for fy, accn in TEN_K_FILINGS:
        print(f"[FY{fy}] accn={accn}")
        info = pull_filing(fy, accn)
        if info: filings.append(info)

    # Parse Segment Information
    segment_rows = []
    for f in filings:
        # Try multiple shortName variants (GD uses "Business Segment Information" or similar)
        seg_r = None
        for k in ("Segment Information", "Business Segment Information"):
            if k in f["targets"]:
                seg_r = f["targets"][k]
                break
        if not seg_r:
            print(f"FY{f['fy']} BOOK — no Segment Information R-file found (targets: {list(f['targets'].keys())})")
            continue
        seg_text = html_to_text(f["dir"] / f"{seg_r}.htm")
        parsed = parse_segment_table(seg_text)
        for fy_in_note, rec in sorted(parsed.items()):
            rec["fy_book"] = f["fy"]
            rec["accn"] = f["accn"]
            segment_rows.append(rec)
            print(f"  FY{f['fy']} book reports FY{fy_in_note}: "
                  f"Marine Systems rev=${rec.get('marine_systems_revenue_$M','?'):,}M "
                  f"OpEarn=${rec.get('marine_systems_op_earnings_$M','?')}M")

    fields = sorted({k for r in segment_rows for k in r.keys()})
    front = ["fy_book", "fy_in_note", "accn"]
    fields = front + [f for f in fields if f not in front]
    with open(OUT / "gd_marine_systems_segment.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for r in segment_rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"\nWrote {OUT/'gd_marine_systems_segment.csv'} ({len(segment_rows)} rows)")

    # Reconciled
    most_recent = {}
    for r in segment_rows:
        fy = r["fy_in_note"]
        if fy not in most_recent or r["fy_book"] > most_recent[fy]["fy_book"]:
            most_recent[fy] = r
    with open(OUT / "gd_marine_systems_segment_reconciled.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for fy in sorted(most_recent):
            w.writerow({k: most_recent[fy].get(k, "") for k in fields})
    print(f"Wrote {OUT/'gd_marine_systems_segment_reconciled.csv'} ({len(most_recent)} rows)")

    # Narrative
    narrative_rows = []
    for f in filings:
        full_text = html_to_text(f["dir"] / "10k_main.htm")
        snips = extract_program_narrative(full_text, f["fy"])
        narrative_rows.extend(snips)
        print(f"  FY{f['fy']} 10-K: {len(snips)} program-narrative snippets")

    with open(OUT / "gd_program_narrative.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=["fy_book", "keyword", "has_dollar", "snippet"])
        w.writeheader()
        for r in narrative_rows:
            w.writerow(r)
    print(f"Wrote {OUT/'gd_program_narrative.csv'} ({len(narrative_rows)} rows)")

    print("\nMarine Systems per-FY (reconciled, most recent vintage):")
    print(f"  {'FY':>4}  {'Revenue $M':>11}  {'OpEarn $M':>10}  {'Margin':>7}")
    for fy in sorted(most_recent):
        r = most_recent[fy]
        rev = r.get("marine_systems_revenue_$M", 0) or 0
        oi  = r.get("marine_systems_op_earnings_$M", 0) or 0
        margin = 100*oi/rev if rev else 0
        print(f"  {fy:>4}  {rev:>11,}  {oi:>10,}  {margin:>6.1f}%")

    print("\nDONE")


if __name__ == "__main__":
    main()
