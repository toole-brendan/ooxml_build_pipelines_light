#!/usr/bin/env python3
"""
Re-process HII 10-K filings with DDG / Ingalls-focused keywords.

The 10-K HTML cache is already present (symlinked from
submarine_outsourced_work/edgar_research/hii_10k_files/) — same filings, different
keyword extraction.

Outputs to edgar_research/:
  - hii_ingalls_segment.csv             Ingalls segment financials per FY (vs sub
                                        project's hii_nns_segment.csv — same source,
                                        different columns surfaced)
  - hii_ingalls_program_narrative.csv   DDG-keyword snippets per FY
  - hii_ingalls_summary_memo.md         Prose writeup

Why we care: HII Ingalls (Pascagoula, MS) builds DDG-51 (and DDG-1000 originally,
plus LHA, LPD, NSC). The Ingalls segment in the 10-K gives us:
  - segment-level revenue (denominator for outsourcing %)
  - product vs service breakdown
  - operating margin (proxy for in-house value-add)
  - narrative on DDG program awards / backlog
"""
import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT = REPO / "edgar_research"
OUT.mkdir(parents=True, exist_ok=True)
CACHE = OUT / "hii_10k_files"

# Same filings as submarine project
TEN_K_FILINGS = [
    (2021, "0001501585-22-000007"),
    (2022, "0001501585-23-000010"),
    (2023, "0001501585-24-000007"),
    (2024, "0001501585-25-000006"),
    (2025, "0001501585-26-000006"),
]


def html_to_text(html_path):
    class T(HTMLParser):
        def __init__(self): super().__init__(); self.t = []
        def handle_data(self, d): self.t.append(d)
    p = T()
    try:
        p.feed(Path(html_path).read_text(errors="replace"))
    except Exception:
        return ""
    return re.sub(r"\s+", " ", " ".join(p.t)).strip()


def numify(s):
    if s is None: return None
    s = str(s).replace(",", "").replace("$", "").strip()
    if s in ("—", "-", ""): return 0
    try: return int(s)
    except ValueError: return None


def parse_segment_table(seg_text):
    """Same parser as submarine project — captures both Ingalls and NNS columns.
    Returns {fy_in_note: {field: value, ...}}.
    """
    out = {}

    # NEW format (FY24/FY25 books) — table per year, segments as columns
    new_blocks = list(re.finditer(r"Year Ended December 31,\s+(\d{4})", seg_text))
    if new_blocks:
        for i, m in enumerate(new_blocks):
            fy = int(m.group(1))
            bs = m.end()
            be = new_blocks[i+1].start() if i+1 < len(new_blocks) else bs + 3000
            block = seg_text[bs:be]
            m_rev = re.search(r"Total sales and service revenues\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*\(?([\d,]+|—)\)?\s+\$?\s*([\d,]+)", block)
            m_oi  = re.search(r"Total segment operating income\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+|—)\s+\$?\s*([\d,]+)", block)
            m_prod = re.search(r"Product sales\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+|—)\s+\$?\s*([\d,]+)", block)
            m_svc  = re.search(r"Service revenues\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+|—)\s+\$?\s*([\d,]+)", block)
            rec = {"fy_in_note": fy, "format": "new"}
            if m_rev:
                rec["ingalls_total_rev_$M"] = numify(m_rev.group(1))
                rec["nns_total_rev_$M"] = numify(m_rev.group(2))
                rec["mt_total_rev_$M"] = numify(m_rev.group(3))
                rec["consolidated_total_rev_$M"] = numify(m_rev.group(5))
            if m_oi:
                rec["ingalls_op_income_$M"] = numify(m_oi.group(1))
                rec["nns_op_income_$M"] = numify(m_oi.group(2))
                rec["mt_op_income_$M"] = numify(m_oi.group(3))
                rec["consolidated_seg_op_income_$M"] = numify(m_oi.group(5))
            if m_prod:
                rec["ingalls_product_rev_$M"] = numify(m_prod.group(1))
                rec["nns_product_rev_$M"] = numify(m_prod.group(2))
                rec["mt_product_rev_$M"] = numify(m_prod.group(3))
            if m_svc:
                rec["ingalls_service_rev_$M"] = numify(m_svc.group(1))
                rec["nns_service_rev_$M"] = numify(m_svc.group(2))
                rec["mt_service_rev_$M"] = numify(m_svc.group(3))
            if "ingalls_total_rev_$M" in rec:
                out[fy] = rec
    if out: return out

    # OLD format — years as columns, segments as rows
    m_header = re.search(r"Year Ended December 31\s*\(\$\s+in\s+millions\)\s+(\d{4})\s+(\d{4})\s+(\d{4})", seg_text)
    if not m_header: return out
    years = [int(m_header.group(i)) for i in (1,2,3)]
    block = seg_text[m_header.end():m_header.end()+3000]

    def find_row(pat, text):
        rx = pat + r"\s+\$?\s*\(?([\d,]+)\)?\s+\$?\s*\(?([\d,]+)\)?\s+\$?\s*\(?([\d,]+)\)?"
        return re.search(rx, text)

    sales_start = block.find("Sales and Service Revenues")
    if sales_start < 0: return out
    oi_start = block.find("Operating Income", sales_start)
    sales_block = block[sales_start:oi_start] if oi_start > 0 else block[sales_start:]
    oi_block = block[oi_start:oi_start+2000] if oi_start > 0 else ""

    ing_rev = find_row(r"Ingalls", sales_block)
    nns_rev = find_row(r"Newport News", sales_block)
    mt_rev  = find_row(r"(?:Mission Technologies|Technical Solutions)", sales_block)
    ing_oi  = find_row(r"Ingalls", oi_block) if oi_block else None
    nns_oi  = find_row(r"Newport News", oi_block) if oi_block else None
    mt_oi   = find_row(r"(?:Mission Technologies|Technical Solutions)", oi_block) if oi_block else None
    for col, fy in enumerate(years):
        rec = {"fy_in_note": fy, "format": "old"}
        if ing_rev: rec["ingalls_total_rev_$M"] = numify(ing_rev.group(col+1))
        if nns_rev: rec["nns_total_rev_$M"] = numify(nns_rev.group(col+1))
        if mt_rev:  rec["mt_total_rev_$M"] = numify(mt_rev.group(col+1))
        if ing_oi:  rec["ingalls_op_income_$M"] = numify(ing_oi.group(col+1))
        if nns_oi:  rec["nns_op_income_$M"] = numify(nns_oi.group(col+1))
        if mt_oi:   rec["mt_op_income_$M"] = numify(mt_oi.group(col+1))
        if "ingalls_total_rev_$M" in rec:
            out[fy] = rec
    return out


# DDG-relevant keywords
KEYWORDS = [
    ("DDG",            r"\bDDG\b"),
    ("DDG 51 / 1000",  r"\bDDG\s*(?:51|1000)\b"),
    ("Arleigh Burke",  r"\bArleigh\s*Burke\b"),
    ("Flight III",     r"\bFlight\s*III\b"),
    ("Destroyer",      r"\bdestroyer\b"),
    ("Aegis",          r"\bAegis\b"),
    ("SPY-6",          r"\bSPY-?6\b"),
    ("Ingalls",        r"\bIngalls\b"),
    ("Pascagoula",     r"\bPascagoula\b"),
    ("LHA / LPD",      r"\bL[HP][AD]\b"),
    ("NSC",            r"\bNSC\b"),
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
            has_count = bool(re.search(r"\b\d+\s+(destroyers?|ships?|DDGs?)\b", ctx, re.IGNORECASE))
            if has_dollar or has_count:
                snippets.append({
                    "fy_book": fy, "keyword": label,
                    "has_dollar": "Y" if has_dollar else "",
                    "snippet": ctx,
                })
    return snippets


def main():
    print(f"=== HII 10-K re-processing for DDG / Ingalls keywords ===\n")

    segment_rows = []
    narrative_rows = []
    for fy, accn in TEN_K_FILINGS:
        fy_dir = CACHE / str(fy)
        if not fy_dir.exists():
            print(f"  FY{fy}: no cached files at {fy_dir} — skip")
            continue

        # MetaLinks tells us which R-file holds the Segment Information note
        ml_path = fy_dir / "MetaLinks.json"
        if not ml_path.exists():
            print(f"  FY{fy}: no MetaLinks.json")
            continue
        ml = json.load(open(ml_path))
        instance = list(ml["instance"].keys())[0]
        reports = ml["instance"][instance]["report"]
        seg_rid = None
        for rid, rdata in reports.items():
            if rdata.get("shortName") == "Segment Information":
                seg_rid = rid
                break
        if not seg_rid:
            print(f"  FY{fy}: no Segment Information R-file in MetaLinks")
            continue

        seg_text = html_to_text(fy_dir / f"{seg_rid}.htm")
        parsed = parse_segment_table(seg_text)
        for fy_in_note, rec in sorted(parsed.items()):
            rec["fy_book"] = fy
            rec["accn"] = accn
            segment_rows.append(rec)
            print(f"  FY{fy} book → FY{fy_in_note}: Ingalls rev=${rec.get('ingalls_total_rev_$M','?'):,}M  "
                  f"OpInc=${rec.get('ingalls_op_income_$M','?')}M")

        # Narrative
        full_text = html_to_text(fy_dir / "10k_main.htm")
        snips = extract_program_narrative(full_text, fy)
        narrative_rows.extend(snips)
        print(f"    FY{fy} 10-K: {len(snips)} DDG-narrative snippets")

    # Write segment CSV (long-form)
    fields = sorted({k for r in segment_rows for k in r.keys()})
    front = ["fy_book", "fy_in_note", "accn"]
    fields = front + [f for f in fields if f not in front]
    with open(OUT / "hii_ingalls_segment.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for r in segment_rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"\nWrote {OUT/'hii_ingalls_segment.csv'} ({len(segment_rows)} rows)")

    # Reconciled per FY (most recent vintage wins)
    most_recent = {}
    for r in segment_rows:
        fy = r["fy_in_note"]
        if fy not in most_recent or r["fy_book"] > most_recent[fy]["fy_book"]:
            most_recent[fy] = r
    with open(OUT / "hii_ingalls_segment_reconciled.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for fy in sorted(most_recent):
            w.writerow({k: most_recent[fy].get(k, "") for k in fields})
    print(f"Wrote {OUT/'hii_ingalls_segment_reconciled.csv'} ({len(most_recent)} rows)")

    # Narrative CSV
    with open(OUT / "hii_ingalls_program_narrative.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=["fy_book", "keyword", "has_dollar", "snippet"])
        w.writeheader()
        for r in narrative_rows:
            w.writerow(r)
    print(f"Wrote {OUT/'hii_ingalls_program_narrative.csv'} ({len(narrative_rows)} rows)")

    # Print Ingalls per-FY revenue + OI for at-a-glance view
    print("\nIngalls segment per-FY (reconciled, most recent vintage):")
    print(f"  {'FY':>4}  {'Rev $M':>9}  {'OpInc $M':>9}  {'Margin':>7}  {'Product $M':>10}  {'Service $M':>10}")
    for fy in sorted(most_recent):
        r = most_recent[fy]
        rev = r.get("ingalls_total_rev_$M", 0) or 0
        oi  = r.get("ingalls_op_income_$M", 0) or 0
        prod = r.get("ingalls_product_rev_$M", 0) or 0
        svc  = r.get("ingalls_service_rev_$M", 0) or 0
        margin = 100*oi/rev if rev else 0
        print(f"  {fy:>4}  {rev:>9,}  {oi:>9,}  {margin:>6.1f}%  {prod:>10,}  {svc:>10,}")

    print("\nDONE")


if __name__ == "__main__":
    main()
