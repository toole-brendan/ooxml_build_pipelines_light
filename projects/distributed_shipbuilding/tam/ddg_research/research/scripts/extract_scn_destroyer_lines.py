#!/usr/bin/env python3
"""
Extract DDG-51 (LI 2122) line-item structured data from the SCN justification books.

MULTI-VINTAGE (P-5c). The P-5c Ship Cost Analysis cost categories are extracted from
EVERY available SCN book (FY22..FY27) and reconciled per (FY, category) to the most-
recent SETTLED vintage (PB year >= FY + 2), falling back to the most-recent vintage.
This mirrors the submarine pipeline (extract_scn_p5c_multi_vintage.py) and closes the
pre-FY2024 HM&E gap the old single-vintage (FY27-only) extraction left folded into the
"other non-BC" residual. (HM&E is itemized in the FY22/FY23/FY24 books but condensed
out of the FY27 book's FY2016-2023 history block.)

The P-40 resource summary and P-27 production schedule are taken from the LATEST book
(highest PB year) only -- they are forward-looking budget tables, not reconciled actuals,
and the workbook reads them as-is.

SCN page IDs (FY27 book):
  LI 2122 DDG-51 main       — P-1 Line #13  (Volume 1 — pp 213+)
  LI 2122 DDG-51 Adv Procur — P-1 Line #14  (Volume 1 — pp 243+)

DDG 1000 (Zumwalt) is intentionally out of scope — only 3 ships, almost all
construction work complete; remaining $ flows through OPN (CPS install on DDG 1002).

Outputs (in OUT = projects/distributed_shipbuilding/tam/ddg_research/extracted/):
  scn_li_resource_summary.csv     P-40 line-item resource summary (latest book)
  scn_li_cost_categories.csv      P-5c cost categories per FY, multi-vintage reconciled
  scn_li_production_schedule.csv  P-27 ship production schedule (latest book)

Spot-check the CSVs against the PDFs before relying on numbers — this is a line-grep parser.
"""
import csv
import glob
import os
import re
import sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
# .../projects/distributed_shipbuilding/tam/ddg_research/research/scripts -> .../ooxml_build_pipelines_light
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "..", "..", ".."))
BOOKS_DIR = os.path.join(_REPO, "projects", "distributed_shipbuilding", "tam", "shared", "budget_books")
OUT = os.path.join(_REPO, "projects", "distributed_shipbuilding", "tam", "ddg_research", "extracted")
os.makedirs(OUT, exist_ok=True)

# Reconciled cost-category output is constrained to this FY window (matches the prior
# extraction range so downstream cross-FY sums, e.g. the FFATA gap block, are stable).
FY_MIN, FY_MAX = 2016, 2027

# Canonical P-5c cost-category labels the funnel consumes (source label variants are
# normalized via norm_cat). Emitted in this order.
CAT_TOTAL = "Total Ship Estimate"
CAT_PLANS = "Plan Costs"
CAT_BC = "Basic Construction/Conversion"
CAT_CO = "Change Orders"
CAT_ELEC = "Electronics"
CAT_ORD = "Ordnance"
CAT_HME = "Hull, Mechanical, and Electrical"
CAT_OTHER = "Other Cost"
CANON_ORDER = [CAT_PLANS, CAT_BC, CAT_CO, CAT_ELEC, CAT_HME, CAT_ORD, CAT_OTHER, CAT_TOTAL]
CANON_SET = set(CANON_ORDER)

# Each line item is identified by the "P-1 Line #N" footer that repeats on every page.
LINE_ITEMS = [
    {"li": 2122, "title": "DDG-51 Arleigh Burke Class Destroyer", "p1_line": 13,
     "appropriation": "1611N", "ba": "02", "bsa": "1",
     "ba_name": "Other Warships"},
    {"li": 2122, "title": "DDG-51 Arleigh Burke Class Destroyer, Advance Procurement", "p1_line": 14,
     "appropriation": "1611N", "ba": "02", "bsa": "1",
     "ba_name": "Other Warships"},
]


def load_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def detect_pb_year(path):
    """Read the PB (President's Budget) year from the book header, e.g.
    'Fiscal Year (FY) 2027 Budget Estimates' -> 2027."""
    with open(path, encoding="utf-8", errors="replace") as f:
        head = f.read(4000)
    m = re.search(r"Fiscal Year \(FY\) (\d{4}) Budget Estimates", head)
    return int(m.group(1)) if m else None


def parse_value(v):
    """'$1,234.5' / '1,253.175' / '-' / '' -> float or None. Parens => negative."""
    if v is None:
        return None
    s = str(v).strip()
    if not s or s in ("-", "--"):
        return None
    s = s.replace(",", "").replace("$", "").strip()
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def norm_cat(raw):
    """Normalize a source cost-category label to a canonical key (or return it as-is)."""
    r = raw.strip()
    if r.startswith("Hull, Mechanical"):
        return CAT_HME
    if r.startswith("Basic Construction"):
        return CAT_BC
    return r


def melt_row(fy_columns, raw_values):
    """Map a P-5c row's raw value tokens onto its FY columns -> [(fy:int, token:str)].

    Most rows carry one value per FY. 'Plan Costs' carries interleaved (qty, cost) pairs
    (2*N for N FYs); take the cost (odd indices). '-' is a real value slot, not padding.
    """
    cells = [str(c).strip() for c in raw_values]
    last = -1
    for i, c in enumerate(cells):
        if c != "":
            last = i
    vals = cells[: last + 1]
    n = len(fy_columns)
    if n == 0 or not vals:
        return []
    if len(vals) == 2 * n:          # (qty, cost) pairs -> costs
        costs = vals[1::2]
    elif len(vals) == n:            # one value per FY
        costs = vals
    elif len(vals) > n:             # best effort: trailing N are the costs
        costs = vals[-n:]
    else:
        costs = vals + ["-"] * (n - len(vals))
    return [(int(fy), c) for fy, c in zip(fy_columns, costs)]


def reconcile(idx):
    """idx: {(fy, cat) -> {pb_year: value}} -> {(fy, cat) -> (value, pb_year)}.

    Prefer the most-recent SETTLED vintage (pb_year >= fy + 2, i.e. the year has aged
    into a revised/actual), else the most-recent vintage available.
    """
    out = {}
    for (fy, cat), vv in idx.items():
        settled = {pb: v for pb, v in vv.items() if pb >= fy + 2}
        src = settled if settled else vv
        best_pb = max(src)
        out[(fy, cat)] = (src[best_pb], best_pb)
    return out


def find_p1_line_pages(text, p1_line):
    """Find page-marker lines like 'P-1 Line #1' and return (start_line_idx, end_line_idx)
    in the file for the entire contiguous block. Multiple P-1 lines exist; each block is
    a range of consecutive lines that share the marker."""
    lines = text.splitlines()
    marker = re.compile(rf"\bP-1 Line #{p1_line}\b")
    matched = [i for i, ln in enumerate(lines) if marker.search(ln)]
    if not matched:
        return None, None
    return matched[0], matched[-1]


def extract_resource_summary(text, li, p1_line):
    """Find the P-40 Budget Line Item Justification table with columns:
    Prior Years | FY 2025 | FY 2026 | FY 2027 Base | FY 2027 OOC | FY 2027 Total | FY 2028 ... | To Complete | Total

    Pull each Resource Summary row as a labeled dict."""
    lines = text.splitlines()
    start, end = find_p1_line_pages(text, p1_line)
    if start is None:
        return []
    block = "\n".join(lines[max(0, start - 60):end + 5])

    out_rows = []
    found_header = False
    block_lines = block.splitlines()
    for i, ln in enumerate(block_lines):
        if "Resource Summary" in ln and ("Prior" in block_lines[i - 1] or "Prior" in ln):
            found_header = True
            continue
        if found_header:
            if "(The following Resource Summary rows" in ln:
                continue
            if "Description:" in ln or "Major Electronics" in ln or "MISSION:" in ln:
                break
            m = re.match(r"^\s*([A-Za-z][A-Za-z0-9 ()\$/&,'.\-+]+?)\s{2,}([0-9,*().\-\s]+?)\s*$", ln)
            if m:
                label = m.group(1).strip()
                nums_str = m.group(2).strip()
                tokens = re.split(r"\s{2,}", nums_str)
                out_rows.append({
                    "li": li,
                    "p1_line": p1_line,
                    "row_label": label,
                    "raw_values": tokens,
                })
    return out_rows


def extract_p5c_ship_cost(text, li, p1_line):
    """Extract P-5c Ship Cost Analysis tables — one per page, each shows a single ship
    (or up to 8 hulls per table) with cost categories. DDG-51 has many hulls per page."""
    lines = text.splitlines()
    block_rows = []
    in_p5c = False
    fy_headers = []
    for i, ln in enumerate(lines):
        if "Exhibit P-5c" in ln:
            window = "\n".join(lines[i:i + 8])
            if f" {li} / " in window or f"{li} /" in window:
                in_p5c = True
                fy_headers = []
                continue
            else:
                in_p5c = False
                continue
        if not in_p5c:
            continue
        if "Remarks:" in ln or "Exhibit P-" in ln:
            in_p5c = False
            continue
        fy_matches = re.findall(r"FY\s*(\d{4})", ln)
        if fy_matches and len(fy_matches) >= 2:
            fy_headers = fy_matches
            continue
        m = re.match(r"^\s*([A-Za-z][A-Za-z0-9 ,()/&\-\.]+?)(?:\s*\(†\))?\s{2,}(.+?)\s*$", ln)
        if m:
            label = m.group(1).strip()
            if label.lower().startswith(("page", "navy", "appropriation", "1611n", "less ",
                                          "net p-1", "li ", "ba ", "bsa ", "id code", "cost categories",
                                          "remarks", "exhibit", "fy ", "(†)")):
                continue
            tokens = re.split(r"\s{2,}", m.group(2).strip())
            if any(re.match(r"^[\-\$0-9,\.]+$", t) for t in tokens):
                block_rows.append({
                    "li": li,
                    "p1_line": p1_line,
                    "cost_category": label,
                    "fy_columns": fy_headers,
                    "raw_values": tokens,
                })
    return block_rows


def extract_p27_schedule(text, li, p1_line):
    """Extract P-27 ship production schedule — hull, shipbuilder, FY, contract award,
    start of construction, delivery date.

    DDG hull patterns:
      DDG NNN (3 digits, 51+, e.g. DDG 126, DDG 145)
    """
    lines = text.splitlines()
    out = []
    in_p27 = False
    for i, ln in enumerate(lines):
        if "Exhibit P-27" in ln:
            window = "\n".join(lines[i:i + 8])
            if f" {li} / " in window or f"{li} /" in window:
                in_p27 = True
                continue
            else:
                in_p27 = False
                continue
        if not in_p27:
            continue
        if "Exhibit P-" in ln or "Footnotes:" in ln:
            in_p27 = False
            continue
        # Pattern A: ship + shipbuilder + dates all on one line
        m = re.match(
            r"^\s*(DDG\s*\d{2,4})\s+(.+?)\s+(\d{4})\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s*$",
            ln
        )
        if m:
            out.append({
                "li": li,
                "p1_line": p1_line,
                "ship": m.group(1).strip(),
                "shipbuilder": m.group(2).strip(),
                "fiscal_year": m.group(3).strip(),
                "contract_award": m.group(4).strip(),
                "start_construction": m.group(5).strip(),
                "delivery_date": m.group(6).strip(),
            })
            continue
        # Pattern B (footnoted): ship name alone, then indented "(n) shipbuilder ..." row
        m1 = re.match(r"^\s*(DDG\s*\d{2,3})\s*$", ln)
        if m1 and i + 1 < len(lines):
            ship = m1.group(1).strip()
            next_ln = lines[i + 1]
            m2 = re.match(
                r"^\s*(?:\(\d+\))?\s*(.+?)\s+(\d{4})\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s*$",
                next_ln
            )
            if m2:
                out.append({
                    "li": li,
                    "p1_line": p1_line,
                    "ship": ship,
                    "shipbuilder": m2.group(1).strip(),
                    "fiscal_year": m2.group(2).strip(),
                    "contract_award": m2.group(3).strip(),
                    "start_construction": m2.group(4).strip(),
                    "delivery_date": m2.group(5).strip(),
                })
    return out


def write_cost_categories_multi_vintage(books):
    """Extract P-5c cost categories from every book, reconcile per (FY, category) to the
    most-recent settled vintage, and emit one row per category spanning its FYs."""
    # idx[(fy, cat)] = {pb_year: value}; provenance[(fy, cat)] = pb_year chosen.
    idx = defaultdict(dict)
    per_book_diag = []
    for path in books:
        pb = detect_pb_year(path)
        if pb is None:
            print(f"  WARN: no PB year in {os.path.basename(path)}; skipped")
            continue
        text = load_text(path)
        rows = extract_p5c_ship_cost(text, 2122, 13)
        n_cells = 0
        for r in rows:
            cat = norm_cat(r["cost_category"])
            if cat not in CANON_SET:
                continue
            for fy, tok in melt_row(r["fy_columns"], r["raw_values"]):
                if not (FY_MIN <= fy <= FY_MAX):
                    continue
                v = parse_value(tok)
                if v is None:
                    continue
                idx[(fy, cat)][pb] = v
                n_cells += 1
        per_book_diag.append((os.path.basename(path), pb, len(rows), n_cells))

    print("  per-book P-5c extraction (file, PB year, raw rows, in-window cells):")
    for name, pb, nrows, ncells in per_book_diag:
        print(f"    {name:24s} PB{pb}  rows={nrows:3d}  cells={ncells}")

    recon = reconcile(idx)
    percat = defaultdict(dict)            # cat -> {fy: value}
    prov = defaultdict(dict)             # cat -> {fy: pb_year}
    for (fy, cat), (v, pb) in recon.items():
        percat[cat][fy] = v
        prov[cat][fy] = pb

    out_rows = []
    for cat in CANON_ORDER:
        if cat not in percat:
            continue
        fys = sorted(percat[cat])
        vals = [f"{percat[cat][fy]:.3f}" for fy in fys]
        out_rows.append((cat, fys, vals))

    max_cols = max((len(v) for _, _, v in out_rows), default=0)
    path = os.path.join(OUT, "scn_li_cost_categories.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["LI", "P-1 Line", "Cost Category", "FY Headers"] +
                   [f"v{i}" for i in range(max_cols)])
        for cat, fys, vals in out_rows:
            w.writerow(["2122", "13", cat, "|".join(str(fy) for fy in fys)] +
                       vals + [""] * (max_cols - len(vals)))
    print(f"Wrote scn_li_cost_categories.csv ({len(out_rows)} categories, "
          f"reconciled multi-vintage)")

    # Provenance spot-check for the HM&E backfill (the whole point of going multi-vintage).
    hme = percat.get(CAT_HME, {})
    for fy in (2022, 2023):
        if fy in hme:
            print(f"  HM&E FY{fy} = {hme[fy]:.3f}  (from PB{prov[CAT_HME][fy]})")


def write_resource_summary(text):
    rs_rows = []
    for item in LINE_ITEMS:
        rs_rows.extend(extract_resource_summary(text, item["li"], item["p1_line"]))
    if not rs_rows:
        return
    max_cols = max(len(r["raw_values"]) for r in rs_rows)
    col_names = ["Prior Years", "FY 2025", "FY 2026", "FY 2027 Base", "FY 2027 OOC",
                 "FY 2027 Total", "FY 2028", "FY 2029", "FY 2030", "FY 2031",
                 "To Complete", "Total"]
    if max_cols > len(col_names):
        col_names = col_names + [f"col_{i}" for i in range(len(col_names), max_cols)]
    with open(os.path.join(OUT, "scn_li_resource_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["LI", "P-1 Line", "Row Label"] + col_names[:max_cols])
        for r in rs_rows:
            w.writerow(
                [r["li"], r["p1_line"], r["row_label"]] +
                r["raw_values"] + [""] * (max_cols - len(r["raw_values"]))
            )
    print(f"Wrote scn_li_resource_summary.csv ({len(rs_rows)} rows, latest book)")


def write_production_schedule(text):
    p27_rows = []
    for item in LINE_ITEMS:
        if "Advance Procurement" in item["title"]:
            continue
        p27_rows.extend(extract_p27_schedule(text, item["li"], item["p1_line"]))
    if not p27_rows:
        return
    with open(os.path.join(OUT, "scn_li_production_schedule.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["LI", "P-1 Line", "Ship", "Shipbuilder", "FY", "Contract Award",
                    "Start Construction", "Delivery Date"])
        for r in p27_rows:
            w.writerow([r["li"], r["p1_line"], r["ship"], r["shipbuilder"],
                        r["fiscal_year"], r["contract_award"],
                        r["start_construction"], r["delivery_date"]])
    print(f"Wrote scn_li_production_schedule.csv ({len(p27_rows)} rows, latest book)")


def main():
    books = sorted(glob.glob(os.path.join(BOOKS_DIR, "SCN_Book_FY*.txt")))
    if not books:
        sys.exit(f"No SCN books found in {BOOKS_DIR}")
    print(f"Found {len(books)} SCN books in {BOOKS_DIR}")

    # P-5c cost categories: multi-vintage reconciled across all books.
    write_cost_categories_multi_vintage(books)

    # P-40 resource summary + P-27 schedule: latest (highest PB year) book only.
    latest = max(books, key=lambda p: detect_pb_year(p) or 0)
    print(f"Latest book for resource summary / schedule: {os.path.basename(latest)}")
    text_latest = load_text(latest)
    write_resource_summary(text_latest)
    write_production_schedule(text_latest)


if __name__ == "__main__":
    main()
