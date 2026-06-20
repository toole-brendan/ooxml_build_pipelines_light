#!/usr/bin/env python3
"""
Pull General Dynamics 10-K data from EDGAR for FY2021-FY2025 (FY ends Dec 31).

GD CIK = 0000040533. Reports in 4 segments: Aerospace, Marine Systems, Combat
Systems, Technologies. Marine Systems = Electric Boat (subs) + Bath Iron Works
(DDGs) + NASSCO (auxiliaries) — submarine work flows through Marine Systems.

For each FY:
  1. Filing index + MetaLinks.json
  2. Pull Segment Information note (revenue / op income / capex per segment)
  3. Pull Description of Business note (program narrative)
  4. Pull main 10-K HTM for MD&A submarine snippets

Outputs to edgar_research/:
  - gd_10k_files/<FY>/             raw HTML cache per FY
  - gd_marine_systems_segment.csv  long-form Marine Systems financials
  - gd_marine_systems_segment_reconciled.csv  most-recent-vintage per FY
  - gd_program_narrative.csv       sub-program snippets (Columbia / Virginia / Electric Boat)

Mirror of pull_hii_10k_research.py — same access pattern, same EDGAR conventions.
"""
import csv
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/submarine_outsourced_work")
OUT = REPO / "edgar_research"
CACHE = OUT / "gd_10k_files"
CACHE.mkdir(parents=True, exist_ok=True)

USER_AGENT = "submarine-research toole.brendan@gmail.com"

# Accession numbers per fiscal year (verified via EDGAR submissions API 2026-05-24)
TEN_K_FILINGS = [
    (2021, "0000040533-22-000007"),
    (2022, "0000040533-23-000014"),
    (2023, "0000040533-24-000007"),
    (2024, "0000040533-25-000008"),
    (2025, "0000040533-26-000006"),
]

BASE_ARCHIVE = "https://www.sec.gov/Archives/edgar/data/40533"


def fetch(url, out_path):
    out_path = Path(out_path)
    if out_path.exists() and out_path.stat().st_size > 1000:
        return True
    out_path.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["curl", "-sS", "--max-time", "60", "-A", USER_AGENT, url, "-o", str(out_path)],
        capture_output=True, text=True, timeout=90,
    )
    if r.returncode != 0:
        print(f"  curl rc={r.returncode}: {r.stderr[:200]}", flush=True)
        return False
    return out_path.exists() and out_path.stat().st_size > 0


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


def pull_filing(fy, accn):
    accn_nd = accn.replace("-", "")
    base = f"{BASE_ARCHIVE}/{accn_nd}"
    fy_dir = CACHE / str(fy)
    fy_dir.mkdir(exist_ok=True)
    if not fetch(f"{base}/index.json", fy_dir / "index.json"):
        return None
    if not fetch(f"{base}/MetaLinks.json", fy_dir / "MetaLinks.json"):
        return None
    metalinks = json.load(open(fy_dir / "MetaLinks.json"))
    instance = list(metalinks["instance"].keys())[0]
    reports = metalinks["instance"][instance]["report"]
    primary_doc = instance

    # GD note names from MetaLinks short-name field
    wanted = {
        "Segment Information",
        "Segment Information (Tables)",
        "Description of the Business",
        "Description of Business",
        "Revenue",
        "Backlog",
        "Marine Systems",
    }
    targets = {}
    for rid, rdata in reports.items():
        short = (rdata.get("shortName") or "").strip()
        if short in wanted and short not in targets:
            targets[short] = rid
    for short, rid in targets.items():
        fetch(f"{base}/{rid}.htm", fy_dir / f"{rid}.htm")
    fetch(f"{base}/{primary_doc}", fy_dir / "10k_main.htm")
    return {"fy": fy, "accn": accn, "primary_doc": primary_doc, "targets": targets, "dir": fy_dir}


def numify(s):
    if s is None:
        return None
    s = str(s).replace(",", "").replace("$", "").strip()
    if s in ("—", "-", ""):
        return 0
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return None


def parse_segment_table(seg_text):
    """Extract Marine Systems numbers from GD's combined-row segment tables.

    GD's segment note has two adjacent tables. Each row holds 3 metrics × 3 years
    side-by-side (9 numbers per segment row).

    Table 1 (financial performance):
        Header: "Revenue ... Other Segment Items ... Operating Earnings"
                "Year Ended December 31 YYYY YYYY YYYY YYYY YYYY YYYY YYYY YYYY YYYY"
        Marine Systems  16,723 14,343 12,461  (15,546) (13,408) (11,587)  1,177 935 874
                        ^^^ revenue Y3 Y2 Y1   ^^^ other items costs       ^^^ op income

        (FY21 book variant has no "Other Segment Items" column — only Revenue + OI
        + something positive in cols 7-9. Detect via paren sign in cols 4-6.)

    Table 2 (investment / assets):
        Header in different orders across vintages (Identifiable Assets, Capex, D&A).
        We grab the SECOND Marine Systems row with 9 numbers, parse the most
        plausibly-capex column heuristically: a column where Marine Systems is
        in the 300-700 range is capex (assets are larger 5,000-7,000; D&A is
        200-300). This is fragile across vintages but matches FY22-FY25.

    Returns {fy_in_note: rec}.
    """
    out = {}

    # Find all year-triplet headers
    year_headers = list(re.finditer(
        r"Year Ended December 31,?\s+(\d{4})\s+(\d{4})\s+(\d{4})",
        seg_text,
    ))
    if not year_headers:
        return out
    years = [int(year_headers[0].group(i)) for i in (1, 2, 3)]

    # Find Marine Systems rows with at least 9 numbers (segment tables)
    rx_9num = (
        r"Marine Systems\s+"
        + r"\$?\s*\(?([\d,]+)\)?\s+\$?\s*\(?([\d,]+)\)?\s+\$?\s*\(?([\d,]+)\)?\s+"  # cols 1-3
        + r"\$?\s*(\(?[\d,]+\)?|—)\s+\$?\s*(\(?[\d,]+\)?|—)\s+\$?\s*(\(?[\d,]+\)?|—)\s+"  # cols 4-6
        + r"\$?\s*\(?([\d,]+)\)?\s+\$?\s*\(?([\d,]+)\)?\s+\$?\s*\(?([\d,]+)\)?"  # cols 7-9
    )
    ms_rows = list(re.finditer(rx_9num, seg_text))
    if not ms_rows:
        return out

    def parse_num(s):
        if s in (None, "—", "-"):
            return 0
        neg = s.startswith("(") and s.endswith(")")
        return -numify(s.strip("()")) if neg else numify(s.strip("()"))

    # --- Table 1: revenue (cols 1-3), maybe OSI (cols 4-6), OI (cols 7-9) ---
    t1 = ms_rows[0]
    rev = [parse_num(t1.group(i)) for i in (1, 2, 3)]
    mid = [parse_num(t1.group(i)) for i in (4, 5, 6)]
    last = [parse_num(t1.group(i)) for i in (7, 8, 9)]
    # If mid values are negative, this is the FY22+ "Other Segment Items" format
    # and OI is in cols 7-9. If mid is positive, FY21 format has OI in cols 4-6.
    if mid and mid[0] is not None and mid[0] < 0:
        oi = last
        osi = mid
    else:
        oi = mid
        osi = None

    # --- Table 2: investment metrics. Identify capex by magnitude (300-700 range
    # for Marine Systems in FY22-FY25). ---
    capex = [None, None, None]
    da = [None, None, None]
    assets = [None, None, None]
    if len(ms_rows) >= 2:
        t2 = ms_rows[1]
        cols = [[parse_num(t2.group(j*3+i+1)) for i in range(3)] for j in range(3)]
        # Heuristic: assets >> capex >> D&A; assets > 1000, D&A < 400, capex 200-700
        for col_triplet in cols:
            v = col_triplet[0]
            if v is None:
                continue
            if v > 1500:
                assets = col_triplet
            elif v < 350:
                da = col_triplet
            else:
                capex = col_triplet

    for col_idx, fy in enumerate(years):
        rec = {"fy_in_note": fy}
        rec["marine_systems_rev_$M"] = rev[col_idx]
        rec["marine_systems_op_income_$M"] = oi[col_idx]
        if osi:
            rec["marine_systems_other_segment_items_$M"] = osi[col_idx]
        rec["marine_systems_capex_$M"] = capex[col_idx]
        rec["marine_systems_da_$M"] = da[col_idx]
        rec["marine_systems_identifiable_assets_$M"] = assets[col_idx]
        out[fy] = rec
    return out


KEYWORDS = [
    ("Columbia",       r"\bColumbia\b"),
    ("Virginia",       r"\bVirginia\b"),
    ("Block IV",       r"\bBlock\s+IV\b"),
    ("Block V",        r"\bBlock\s+V\b"),
    ("Block VI",       r"\bBlock\s+VI\b"),
    ("SSN",            r"\bSSN[- ]?\d+\b"),
    ("SSBN",           r"\bSSBN[- ]?\d+\b"),
    ("Electric Boat",  r"\bElectric Boat\b"),
    ("Quonset Point",  r"\bQuonset Point\b"),
    ("Groton",         r"\bGroton\b"),
    ("submarine",      r"\bsubmarine[s]?\b"),
    ("supply chain",   r"\bsupply chain\b"),
    ("supplier",       r"\bsupplier[s]?\b"),
    ("outsourc",       r"\boutsourc(?:e|ed|ing)\b"),
    ("subcontract",    r"\bsubcontract(?:or|s|ed|ing)?\b"),
    ("material cost",  r"\b(?:material|purchased material)\b"),
    ("backlog",        r"\bbacklog\b"),
]


def extract_program_narrative(full_text, fy):
    snippets = []
    seen = set()
    for label, pat in KEYWORDS:
        for m in re.finditer(pat, full_text, re.IGNORECASE):
            start = max(0, m.start() - 200)
            end = min(len(full_text), m.end() + 400)
            ctx = full_text[start:end]
            ctx = re.sub(r"^[^.]*\.\s*", "", ctx, count=1)
            m2 = re.search(r"\.[A-Z]", ctx)
            if m2:
                ctx = ctx[: m2.start() + 1]
            ctx = ctx.strip()
            if len(ctx) < 50 or len(ctx) > 900:
                continue
            key = ctx[:120]
            if key in seen:
                continue
            seen.add(key)
            has_dollar = bool(re.search(r"\$\s*[\d,\.]+\s*(billion|million|B|M)", ctx, re.I))
            has_count = bool(re.search(r"\b\d+\s+(submarine|ship|boat|carrier)s?\b", ctx, re.I))
            # Sub-relevance score: only keep snippets that mention sub OR have a $ near sub-keyword
            sub_relevant = bool(re.search(r"submarine|Columbia|Virginia|Block\s+I?V|SSN|SSBN|Electric Boat|Groton|Quonset", ctx, re.I))
            if (has_dollar or has_count) and sub_relevant:
                snippets.append({
                    "fy_book": fy,
                    "keyword": label,
                    "has_dollar": "Y" if has_dollar else "",
                    "snippet": ctx,
                })
    return snippets


def main():
    print("=== GD 10-K research pull ===\n")
    filings = []
    for fy, accn in TEN_K_FILINGS:
        print(f"[FY{fy}] accn={accn}")
        info = pull_filing(fy, accn)
        if info:
            filings.append(info)
            print(f"  notes found: {list(info['targets'].keys())}")
        else:
            print(f"  FAILED to fetch")

    # Parse Segment Information notes
    seg_rows = []
    for f in filings:
        seg_rid = f["targets"].get("Segment Information") or f["targets"].get("Segment Information (Tables)")
        if not seg_rid:
            print(f"FY{f['fy']}: no Segment Information note found")
            continue
        seg_text = html_to_text(f["dir"] / f"{seg_rid}.htm")
        parsed = parse_segment_table(seg_text)
        for fy_in_note, rec in sorted(parsed.items()):
            rec["fy_book"] = f["fy"]
            rec["accn"] = f["accn"]
            seg_rows.append(rec)
            print(f"  FY{f['fy']} book reports FY{fy_in_note}: Marine Systems rev=${rec.get('marine_systems_rev_$M','?'):,} "
                  f"OpInc=${rec.get('marine_systems_op_income_$M','?')}")

    fields = sorted({k for r in seg_rows for k in r.keys()})
    front = ["fy_book", "fy_in_note", "accn"]
    fields = front + [f for f in fields if f not in front]
    seg_path = OUT / "gd_marine_systems_segment.csv"
    with open(seg_path, "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for r in seg_rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"\nWrote {seg_path} ({len(seg_rows)} rows)")

    # Reconciled most-recent vintage per FY
    most_recent = {}
    for r in seg_rows:
        fy = r["fy_in_note"]
        if fy not in most_recent or r["fy_book"] > most_recent[fy]["fy_book"]:
            most_recent[fy] = r
    recon_path = OUT / "gd_marine_systems_segment_reconciled.csv"
    with open(recon_path, "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=fields)
        w.writeheader()
        for fy in sorted(most_recent):
            w.writerow({k: most_recent[fy].get(k, "") for k in fields})
    print(f"Wrote {recon_path} ({len(most_recent)} rows)")

    # Program narrative snippets
    narr_rows = []
    for f in filings:
        full_text = html_to_text(f["dir"] / "10k_main.htm")
        snips = extract_program_narrative(full_text, f["fy"])
        narr_rows.extend(snips)
        print(f"  FY{f['fy']} 10-K: {len(snips)} sub-relevant program snippets with $ or boat-count")

    narr_path = OUT / "gd_program_narrative.csv"
    with open(narr_path, "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=["fy_book", "keyword", "has_dollar", "snippet"])
        w.writeheader()
        for r in narr_rows:
            w.writerow(r)
    print(f"Wrote {narr_path} ({len(narr_rows)} rows)")

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
