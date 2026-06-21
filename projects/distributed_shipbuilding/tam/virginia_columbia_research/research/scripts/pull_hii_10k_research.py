#!/usr/bin/env python3
"""
Pull HII 10-K data from EDGAR for FY2021-FY2025 (FY ends Dec 31).

For each FY:
  1. Download filing index, find MetaLinks.json to locate the Segment Information note
  2. Pull the Segment Information note (table of revenue/OpInc per segment)
  3. Pull the Description of Business note (program-level narrative)
  4. Pull the main 10-K HTML and extract submarine/program-mention snippets from MD&A

Outputs to edgar_research/:
  - hii_10k_files/<FY>/  (raw HTML cache per FY)
  - hii_nns_segment.csv       structured Newport News segment financials
  - hii_program_narrative.csv  one row per program-mention snippet (per FY)
  - hii_summary_memo.md        prose writeup of findings + caveats

Notes:
  - SEC requires User-Agent header per Fair Access policy. Set via UA env var.
  - All data is public, no auth.
  - We are NOT modifying the workbook in this script.
"""
import csv
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

REPO = Path("/Users/brendantoole/projects2/submarine_outsourced_work")
OUT = REPO / "edgar_research"
CACHE = OUT / "hii_10k_files"
CACHE.mkdir(parents=True, exist_ok=True)

USER_AGENT = "submarine-research toole.brendan@gmail.com"

# 10-K filings: (fiscal year, accession number)
TEN_K_FILINGS = [
    (2021, "0001501585-22-000007"),
    (2022, "0001501585-23-000010"),
    (2023, "0001501585-24-000007"),
    (2024, "0001501585-25-000006"),
    (2025, "0001501585-26-000006"),
]

BASE_ARCHIVE = "https://www.sec.gov/Archives/edgar/data/1501585"


def fetch(url, out_path):
    """curl with proper User-Agent. Returns True on success."""
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
    """Strip HTML tags, collapse whitespace."""
    class T(HTMLParser):
        def __init__(self): super().__init__(); self.t = []
        def handle_data(self, d): self.t.append(d)

    p = T()
    try:
        p.feed(Path(html_path).read_text(errors="replace"))
    except Exception as e:
        return ""
    return re.sub(r"\s+", " ", " ".join(p.t)).strip()


def pull_filing(fy, accn):
    """Download index + key R-files for a single 10-K."""
    accn_nodash = accn.replace("-", "")
    base = f"{BASE_ARCHIVE}/{accn_nodash}"
    fy_dir = CACHE / str(fy)
    fy_dir.mkdir(exist_ok=True)

    # Filing index (lists all files)
    if not fetch(f"{base}/index.json", fy_dir / "index.json"):
        print(f"  FY{fy}: failed to fetch index")
        return None
    if not fetch(f"{base}/MetaLinks.json", fy_dir / "MetaLinks.json"):
        print(f"  FY{fy}: failed to fetch MetaLinks")
        return None

    # Identify the right R-files for segment / business / revenue notes
    metalinks = json.load(open(fy_dir / "MetaLinks.json"))
    instance = list(metalinks["instance"].keys())[0]
    reports = metalinks["instance"][instance]["report"]
    primary_doc = instance  # e.g. hii-20251231.htm

    targets = {}  # short_name → R-file number
    wanted_short_names = {
        "Segment Information",
        "Description of Business",
        "Revenue",
    }
    for rid, rdata in reports.items():
        short = rdata.get("shortName", "")
        if short in wanted_short_names and short not in targets:
            # rid is already the form "R15" / "R16" / "R9" in metalinks
            targets[short] = rid

    # Pull each target R-file
    for short, r in targets.items():
        fetch(f"{base}/{r}.htm", fy_dir / f"{r}.htm")

    # Also pull the main 10-K HTM (for MD&A / narrative)
    fetch(f"{base}/{primary_doc}", fy_dir / "10k_main.htm")

    return {
        "fy": fy,
        "accn": accn,
        "primary_doc": primary_doc,
        "targets": targets,
        "dir": fy_dir,
    }


def numify(s):
    if s is None:
        return None
    s = str(s).replace(",", "").replace("$", "").strip()
    if s in ("—", "-", ""):
        return 0
    try:
        return int(s)
    except ValueError:
        return None


def parse_segment_table(seg_text):
    """Extract NNS segment numbers from the Segment Information note text.

    HII used TWO formats across FY21-FY25:

    OLD format (FY21/FY22/FY23 books) — single side-by-side table, years as columns:
        Year Ended December 31 ($ in millions) 2022 2021 2020
        Sales and Service Revenues
        Ingalls        $ 2,570 $ 2,528 $ 2,678
        Newport News    5,852   5,663   5,571
        Mission Technologies (or Technical Solutions in FY21 book)
        ...
        Operating Income
        Ingalls        $ 292 $ 281 $ 281
        Newport News    357   352   233
        ...

    NEW format (FY24/FY25 books) — table per year, segments as columns:
        Year Ended December 31, 2025 ($ in millions) Ingalls Newport News ...
        Product sales $ 2,597 $ 5,397 ...
        Service revenues  469  1,109 ...
        Total sales and service revenues 3,078 6,507 ...
        Total segment operating income $ 233 $ 331 ...

    Returns: {fy_in_note: {field: value, ...}}
    """
    out = {}

    # NEW format first
    new_blocks = list(re.finditer(r"Year Ended December 31,\s+(\d{4})", seg_text))
    if new_blocks:
        for i, m in enumerate(new_blocks):
            fy = int(m.group(1))
            block_start = m.end()
            block_end = new_blocks[i + 1].start() if i + 1 < len(new_blocks) else block_start + 3000
            block = seg_text[block_start:block_end]

            m_rev = re.search(
                r"Total sales and service revenues\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*\(?([\d,]+|\—)\)?\s+\$?\s*([\d,]+)",
                block,
            )
            m_oi = re.search(
                r"Total segment operating income\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+|\—)\s+\$?\s*([\d,]+)",
                block,
            )
            m_prod = re.search(
                r"Product sales\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+|\—)\s+\$?\s*([\d,]+)",
                block,
            )
            m_svc = re.search(
                r"Service revenues\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+)\s+\$?\s*([\d,]+|\—)\s+\$?\s*([\d,]+)",
                block,
            )

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

            if "nns_total_rev_$M" in rec:
                out[fy] = rec

    if out:
        return out

    # OLD format — single side-by-side table, years as columns
    # Find "Year Ended December 31 ($ in millions) YYYY YYYY YYYY"
    m_header = re.search(
        r"Year Ended December 31\s*\(\$\s+in\s+millions\)\s+(\d{4})\s+(\d{4})\s+(\d{4})",
        seg_text,
    )
    if not m_header:
        return out
    years = [int(m_header.group(i)) for i in (1, 2, 3)]
    block = seg_text[m_header.end():m_header.end() + 3000]

    # Row patterns: Ingalls/Newport News/(Mission Technologies|Technical Solutions)
    # Numbers may have $ prefix, may have leading negatives in parens
    def find_row(label_pattern, text):
        # Match e.g. "Newport News $ 5,852 $ 5,663 $ 5,571" or "Newport News 5,852 5,663 5,571"
        rx = label_pattern + r"\s+\$?\s*\(?([\d,]+)\)?\s+\$?\s*\(?([\d,]+)\)?\s+\$?\s*\(?([\d,]+)\)?"
        return re.search(rx, text)

    # Sales and Service Revenues block
    sales_block_start = block.find("Sales and Service Revenues")
    if sales_block_start < 0:
        return out
    # Operating income block starts after "Operating Income"
    oi_start = block.find("Operating Income", sales_block_start)
    sales_block = block[sales_block_start:oi_start] if oi_start > 0 else block[sales_block_start:]
    oi_block = block[oi_start:oi_start + 2000] if oi_start > 0 else ""

    nns_rev = find_row(r"Newport News", sales_block)
    ing_rev = find_row(r"Ingalls", sales_block)
    mt_rev = find_row(r"(?:Mission Technologies|Technical Solutions)", sales_block)
    nns_oi = find_row(r"Newport News", oi_block) if oi_block else None
    ing_oi = find_row(r"Ingalls", oi_block) if oi_block else None
    mt_oi = find_row(r"(?:Mission Technologies|Technical Solutions)", oi_block) if oi_block else None

    for col_idx, fy in enumerate(years):
        rec = {"fy_in_note": fy, "format": "old"}
        if nns_rev: rec["nns_total_rev_$M"] = numify(nns_rev.group(col_idx + 1))
        if ing_rev: rec["ingalls_total_rev_$M"] = numify(ing_rev.group(col_idx + 1))
        if mt_rev:  rec["mt_total_rev_$M"] = numify(mt_rev.group(col_idx + 1))
        if nns_oi:  rec["nns_op_income_$M"] = numify(nns_oi.group(col_idx + 1))
        if ing_oi:  rec["ingalls_op_income_$M"] = numify(ing_oi.group(col_idx + 1))
        if mt_oi:   rec["mt_op_income_$M"] = numify(mt_oi.group(col_idx + 1))
        if "nns_total_rev_$M" in rec:
            out[fy] = rec

    return out


KEYWORDS = [
    ("Virginia",       r"\bVirginia\b"),
    ("Columbia",       r"\bColumbia\b"),
    ("Block IV",       r"\bBlock\s+IV\b"),
    ("Block V",        r"\bBlock\s+V\b"),
    ("Block VI",       r"\bBlock\s+VI\b"),
    ("SSN 774",        r"\bSSN\s*774\b"),
    ("SSBN 826",       r"\bSSBN\s*826\b"),
    ("CVN",            r"\bCVN\s*\d+\b"),
    ("RCOH",           r"\bRCOH\b"),
    ("teaming",        r"\bteaming\b"),
    ("Electric Boat",  r"\bElectric Boat\b"),
    ("Backlog",        r"\bbacklog\b"),
    ("award",          r"\bawarded\b"),
]


def extract_program_narrative(full_text, fy):
    """Walk through the full 10-K text. For each keyword, capture sentence-level
    snippets that mention the keyword AND have dollar amounts or contract details.
    """
    snippets = []
    seen = set()  # dedup
    for label, pattern in KEYWORDS:
        for m in re.finditer(pattern, full_text):
            start = max(0, m.start() - 200)
            end = min(len(full_text), m.end() + 400)
            ctx = full_text[start:end]
            # Trim to nearest sentence boundaries
            ctx = re.sub(r"^[^.]*\.\s*", "", ctx, count=1)
            # Truncate at next sentence after end
            m2 = re.search(r"\.[A-Z]", ctx)
            if m2:
                ctx = ctx[: m2.start() + 1]
            ctx = ctx.strip()
            if len(ctx) < 50 or len(ctx) > 800:
                continue
            # Hash for dedup
            key = ctx[:120]
            if key in seen:
                continue
            seen.add(key)
            has_dollar = bool(re.search(r"\$\s*[\d,\.]+\s*(billion|million|B|M)", ctx, re.IGNORECASE))
            has_block_count = bool(re.search(r"\b\d+\s+(submarines|ships|boats|carriers)\b", ctx))
            if has_dollar or has_block_count:
                snippets.append({
                    "fy_book": fy,
                    "keyword": label,
                    "has_dollar": "Y" if has_dollar else "",
                    "snippet": ctx,
                })
    return snippets


def main():
    print(f"=== HII 10-K research pull ===\n")

    # 1) Pull each 10-K filing
    filings = []
    for fy, accn in TEN_K_FILINGS:
        print(f"[FY{fy}] accn={accn}")
        info = pull_filing(fy, accn)
        if info:
            filings.append(info)

    # 2) Parse Segment Information notes
    segment_rows = []
    for f in filings:
        seg_r = f["targets"].get("Segment Information")
        if not seg_r:
            print(f"FY{f['fy']} BOOK — no Segment Information R-file found")
            continue
        seg_text = html_to_text(f["dir"] / f"{seg_r}.htm")
        parsed = parse_segment_table(seg_text)
        for fy_in_note, rec in sorted(parsed.items()):
            rec["fy_book"] = f["fy"]
            rec["accn"] = f["accn"]
            segment_rows.append(rec)
            print(f"  FY{f['fy']} book reports FY{fy_in_note}: "
                  f"NNS rev=${rec.get('nns_total_rev_$M','?'):,} "
                  f"OpInc=${rec.get('nns_op_income_$M','?')}")

    # Write segment CSV (long-form)
    fields = sorted({k for r in segment_rows for k in r.keys()})
    # Put identifier columns first
    front = ["fy_book", "fy_in_note", "accn"]
    fields = front + [f for f in fields if f not in front]
    with open(OUT / "hii_nns_segment.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for r in segment_rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"\nWrote {OUT/'hii_nns_segment.csv'} ({len(segment_rows)} rows)")

    # 3) Reconciled "most recent vintage" NNS revenue per FY
    # (similar to how we reconcile SCN — most-recent 10-K with the FY as actual is authoritative)
    most_recent = {}
    for r in segment_rows:
        fy = r["fy_in_note"]
        if fy not in most_recent or r["fy_book"] > most_recent[fy]["fy_book"]:
            most_recent[fy] = r
    with open(OUT / "hii_nns_segment_reconciled.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for fy in sorted(most_recent):
            w.writerow({k: most_recent[fy].get(k, "") for k in fields})
    print(f"Wrote {OUT/'hii_nns_segment_reconciled.csv'} ({len(most_recent)} rows)")

    # 4) Extract program narrative snippets from main 10-K HTML
    narrative_rows = []
    for f in filings:
        full_text = html_to_text(f["dir"] / "10k_main.htm")
        snips = extract_program_narrative(full_text, f["fy"])
        narrative_rows.extend(snips)
        print(f"  FY{f['fy']} 10-K: {len(snips)} program-narrative snippets with $ or boat-count")

    with open(OUT / "hii_program_narrative.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=["fy_book", "keyword", "has_dollar", "snippet"])
        w.writeheader()
        for r in narrative_rows:
            w.writerow(r)
    print(f"Wrote {OUT/'hii_program_narrative.csv'} ({len(narrative_rows)} rows)")

    print()
    print("=== DONE ===")


if __name__ == "__main__":
    main()
