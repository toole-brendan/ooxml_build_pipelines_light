#!/usr/bin/env python3
"""
Extract P-5c Ship Cost Analysis rows (Basic Construction, Plan Costs, etc.)
per ship per FY across ALL SCN book vintages.

Each P-5c table shows 1-4 ships, each tied to an authorization FY. Layout varies
by book vintage but always has:
  - FY column headers (e.g., "FY 2021", or 4 columns spanning the lifecycle)
  - "Cost Categories" header
  - Rows: Plan Costs, Basic Construction/Conversion, Change Orders, Electronics,
    Propulsion Equipment, HM&E, Ordnance, Other Cost, Technology Insertion,
    Total Ship Estimate
  - Each cost row has values per FY column. Quantity column appears only for
    rows that have a per-FY Qty (e.g., Plan Costs in FY27 book), otherwise just $.

Output:
  extracted/scn_p5c_per_fy_long.csv         long-form (vintage, li, fy, cost_category, qty, value_$M)
  extracted/scn_p5c_per_fy_reconciled.csv   per-FY most-revised value per cost category
"""
import csv
import os
import re
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
# .../projects/distributed_shipbuilding/tam/submarines/research/scripts -> .../ooxml_build_pipelines_light
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "..", "..", ".."))
BOOKS_DIR = os.path.join(_REPO, "projects", "distributed_shipbuilding", "tam", "shared", "budget_books")
OUT = os.path.join(_REPO, "projects", "distributed_shipbuilding", "tam", "submarines", "extracted")
os.makedirs(OUT, exist_ok=True)

LINE_ITEMS = [
    {"li": 1045, "title": "COLUMBIA Class Submarine"},
    {"li": 2013, "title": "Virginia Class Submarine"},
]

# Cost categories we want to capture (substring match against row label)
CATEGORIES = [
    "Plan Costs",
    "Basic Construction/Conversion",
    "Change Orders",
    "Electronics",
    "Propulsion Equipment",
    "Hull, Mechanical, and Electrical",
    "Ordnance",
    "Other Cost",
    "Technology Insertion",
    "Total Ship Estimate",
]


def detect_vintage(path):
    m = re.search(r"FY(\d{2})", os.path.basename(path))
    return f"FY{m.group(1)}" if m else "unknown"


def detect_pb_year(path):
    with open(path) as f:
        head = "\n".join([next(f).rstrip() for _ in range(30)])
    m = re.search(r"Fiscal Year \(FY\) (\d{4}) Budget Estimates", head)
    return int(m.group(1)) if m else None


def parse_p5c_table(lines, start_idx, end_idx, li, vintage, pb_year):
    """Parse a single P-5c table starting at `start_idx`.

    Returns list of dicts: {vintage, pb_year, li, fy, cost_category, qty, value_$M}

    Strategy: find the "Cost Categories" header line. Look at the LINES ABOVE it
    for "FY YYYY" column tags. Then for each "Cost Categories" row matching one of
    our target categories, extract the (Qty, Total Cost) pairs by FY column.

    The number of value columns per row varies: rows like "Plan Costs" may have
    (Qty, $) per FY, while rows like "Basic Construction/Conversion" only have $
    per FY (no Qty column). We detect by counting tokens.
    """
    out = []
    header_fys = []
    n_fys = 0
    header_seen = False

    for i in range(start_idx, min(end_idx, len(lines))):
        ln = lines[i]
        if "Cost Categories" in ln and not header_seen:
            # FY tags are on the line(s) above
            above1 = lines[i - 1] if i > 0 else ""
            above2 = lines[i - 2] if i > 1 else ""
            # FY tags may span multiple lines (e.g., "FY 2021" on one, "FY 2024" on next)
            # — pull unique FYs preserving order from above2 → above1
            seen = []
            for src in (above2, above1):
                for fy in re.findall(r"FY\s*(\d{4})", src):
                    if fy not in seen:
                        seen.append(fy)
            header_fys = [int(fy) for fy in seen]
            n_fys = len(header_fys)
            header_seen = True
            continue
        if not header_seen:
            continue
        if "Remarks:" in ln or "Net P-1 Funding" in ln or "Exhibit P-" in ln:
            break
        # Match a cost-category row
        for cat in CATEGORIES:
            if cat in ln:
                # Extract the trailing portion (everything after the category label)
                # Split by 2+ spaces to get tokens
                idx = ln.find(cat) + len(cat)
                # Skip "(†)" markers
                rest = re.sub(r"\(†\)", "", ln[idx:]).strip()
                tokens = re.split(r"\s{2,}", rest) if rest else []
                tokens = [t.replace(",", "").replace("$", "") for t in tokens if t]
                # Each FY column might be (Qty, $) or just ($)
                if n_fys == 0:
                    break
                # Heuristic: if tokens are EXACTLY n_fys, each column is just $ (no Qty).
                # If tokens are 2 * n_fys, alternating (Qty, $).
                # If something else, take the last n_fys as $ values.
                if len(tokens) == 2 * n_fys:
                    pairs = [(tokens[2*j], tokens[2*j+1]) for j in range(n_fys)]
                elif len(tokens) == n_fys:
                    pairs = [(None, tokens[j]) for j in range(n_fys)]
                elif len(tokens) > 2 * n_fys:
                    # Take rightmost 2*n_fys
                    take = tokens[-2*n_fys:]
                    pairs = [(take[2*j], take[2*j+1]) for j in range(n_fys)]
                elif len(tokens) > n_fys:
                    take = tokens[-n_fys:]
                    pairs = [(None, take[j]) for j in range(n_fys)]
                else:
                    # Underflow — pad
                    pairs = [(None, tokens[j] if j < len(tokens) else "-") for j in range(n_fys)]
                for fy, (qty, val) in zip(header_fys, pairs):
                    out.append({
                        "vintage": vintage,
                        "pb_year": pb_year,
                        "li": li,
                        "fy": fy,
                        "cost_category": cat,
                        "qty": qty,
                        "value_$M": val,
                    })
                break
    return out


def extract_book(path):
    vintage = detect_vintage(path)
    pb_year = detect_pb_year(path) or (2000 + int(vintage[2:]))
    with open(path) as f:
        lines = f.read().splitlines()

    all_rows = []
    for item in LINE_ITEMS:
        li = item["li"]
        title = item["title"]
        page_marker = re.compile(rf"\b{li}\s*/\s*{re.escape(title.upper())}", re.IGNORECASE)
        # Find every "Exhibit P-5c" header that belongs to this LI
        for i, ln in enumerate(lines):
            if "Exhibit P-5c" not in ln:
                continue
            # Check next ~8 lines for the LI marker
            window = "\n".join(lines[i:i + 8])
            if not page_marker.search(window):
                continue
            # Parse this table — bounded by the next "Exhibit P-" or "Remarks:" or 100 lines
            end_idx = i + 100
            for j in range(i + 5, min(i + 100, len(lines))):
                if "Exhibit P-" in lines[j] and j > i + 5:
                    end_idx = j
                    break
            rows = parse_p5c_table(lines, i, end_idx, li, vintage, pb_year)
            all_rows.extend(rows)
    return all_rows


def main():
    all_long = []
    book_files = sorted(
        f for f in os.listdir(BOOKS_DIR)
        if f.startswith("SCN_Book_FY") and f.endswith(".txt")
    )
    for fname in book_files:
        path = os.path.join(BOOKS_DIR, fname)
        rows = extract_book(path)
        print(f"  {fname}: {len(rows)} P-5c rows extracted")
        all_long.extend(rows)

    out_long = os.path.join(OUT, "scn_p5c_per_fy_long.csv")
    with open(out_long, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "vintage", "pb_year", "li", "fy", "cost_category", "qty", "value_$M"
        ])
        w.writeheader()
        w.writerows(all_long)
    print(f"Wrote {out_long}  ({len(all_long)} long rows)")

    # Reconcile per (li, fy, cost_category): pick most recent vintage that's
    # actual (pb_year >= fy + 2 preferred; else most recent available).
    idx = defaultdict(dict)  # (li, fy, cat) -> {pb_year: value}
    for r in all_long:
        try:
            fy = int(r["fy"])
        except (TypeError, ValueError):
            continue
        key = (int(r["li"]), fy, r["cost_category"])
        val = r["value_$M"]
        if val in ("-", "", None):
            continue
        idx[key][int(r["pb_year"])] = val

    out_recon = os.path.join(OUT, "scn_p5c_per_fy_reconciled.csv")
    with open(out_recon, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "LI", "FY", "Cost Category", "Best Value $M",
            "Source Vintage (PB Year)", "PB - FY",
            "All Vintages Available",
        ])
        for (li, fy, cat), vintage_vals in sorted(idx.items()):
            settled = {pb: v for pb, v in vintage_vals.items() if pb >= fy + 2}
            if settled:
                best_pb = max(settled.keys())
            else:
                best_pb = max(vintage_vals.keys())
            best_val = vintage_vals[best_pb]
            all_pbs = ", ".join(f"PB{pb}={vintage_vals[pb]}" for pb in sorted(vintage_vals.keys()))
            w.writerow([li, fy, cat, best_val, f"PB{best_pb}", best_pb - fy, all_pbs])
    print(f"Wrote {out_recon}")


if __name__ == "__main__":
    main()
