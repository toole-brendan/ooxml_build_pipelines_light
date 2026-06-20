#!/usr/bin/env python3
"""
Multi-vintage SCN line-item extractor.

Iterates over all SCN_Book_FY*.txt files in budget_books/. For each book, auto-detects
the FY columns from the P-40 Resource Summary header line and extracts Columbia
(LI 1045) + Virginia (LI 2013) line items into a long-form CSV:

  vintage, li_number, li_title, p1_section, row_label, fy_label, value

`p1_section` distinguishes the base line item from the Advance Procurement (AP) line.

`fy_label` is one of: 'Prior Years', 'FY 2020', 'FY 2021', ..., 'FY 2030',
                     'FY 2027 Base', 'FY 2027 OCO', 'FY 2027 Total', 'To Complete', 'Total'

`vintage` is the book's PB year (e.g., 'FY22', 'FY27').

Output:
  extracted/scn_li_per_fy_long.csv     long-form per-book per-row-per-FY data
  extracted/scn_per_fy_actual_toa.csv  reconciled per-FY actual TOA picked from
                                        the most-recent book that shows it as actual
  extracted/scn_per_book_columns.csv   diagnostic: each book's detected column schema
"""
import csv
import os
import re
import sys
from collections import defaultdict

BOOKS_DIR = "/Users/brendantoole/projects2/submarine_outsourced_work/budget_books"
OUT = "/Users/brendantoole/projects2/submarine_outsourced_work/extracted"
os.makedirs(OUT, exist_ok=True)

# Line items to extract (LI number is stable across years; P-1 line # drifts)
LINE_ITEMS = [
    {"li": 1045, "title": "COLUMBIA Class Submarine"},
    {"li": 2013, "title": "Virginia Class Submarine"},
]


def detect_vintage(path):
    """Return the PB year (string like 'FY22') from filename or file content."""
    m = re.search(r"FY(\d{2})", os.path.basename(path))
    if m:
        return f"FY{m.group(1)}"
    return "unknown"


def detect_pb_year(path):
    """Read first ~30 lines to find 'Fiscal Year (FY) YYYY Budget Estimates'."""
    with open(path) as f:
        head = "\n".join([next(f).rstrip() for _ in range(30) if f])
    m = re.search(r"Fiscal Year \(FY\) (\d{4}) Budget Estimates", head)
    return int(m.group(1)) if m else None


def parse_p40_header(lines, start_idx, look_ahead=10):
    """Find the FY label header line for the Resource Summary table.

    Returns a list of column labels in order, e.g.
    ['Prior Years', 'FY 2025', 'FY 2026', 'FY 2027 Base', 'FY 2027 OOC',
     'FY 2027 Total', 'FY 2028', 'FY 2029', 'FY 2030', 'FY 2031',
     'To Complete', 'Total']

    The headers can span 2 lines (one with "Prior Years FY YYYY ... Total",
    one with "Base OOC Total" below the request year). We normalize."""
    # Look for a line containing two or more "FY YYYY" patterns
    for j in range(start_idx, min(start_idx + look_ahead, len(lines))):
        ln = lines[j]
        fy_matches = re.findall(r"FY\s*(\d{4})", ln)
        if len(fy_matches) >= 2 and ("Prior" in ln or "Years" in ln):
            # Now split the header line into tokens by 2+ spaces
            # The header structure is something like:
            #   "Resource Summary  Prior Years   FY 2020   FY 2021     Base     OCO     Total ..."
            # The "Base / OCO / Total" sub-headers may be on the line BELOW
            next_line = lines[j + 1] if j + 1 < len(lines) else ""
            # Build label list manually based on the FY matches and known structure
            labels = ["Prior Years"]
            for fy in fy_matches:
                labels.append(f"FY {fy}")
            # Find the request year (usually FY-of-book year). It has Base/OCO/Total sub-cols.
            # The number of value columns in data rows tells us which FY has sub-cols.
            # Heuristic: if the header has "Base" or "OCO" or "OOC" tokens after an FY,
            # split that FY into 3 sub-columns.
            # For simpler logic: assume the SECOND FY listed (index 2 in labels) is the request year.
            # Actually we need to figure this out from book-vintage:
            return labels, "needs_split"
    return None, None


def parse_resource_summary_table(lines, start_idx, end_idx, li, vintage,
                                  pb_year, p1_section):
    """Extract Resource Summary rows from a P-40 table. Returns list of dicts."""
    out = []
    header_labels = None
    header_idx = None
    n_value_cols = None

    for i in range(start_idx, end_idx):
        ln = lines[i]
        # Only parse the FIRST "Resource Summary" header — later occurrences
        # (e.g., "(The following Resource Summary rows are informational...)")
        # would silently clobber the real header with empty FY list.
        if "Resource Summary" in ln and header_labels is None:
            # Header. The header spans up to 2 lines:
            #   line above: "Prior Years   FY 2027   FY 2027   FY 2027 ..."
            #   this line:  "Resource Summary   Years   FY 2025   FY 2026   Base   OOC   Total ..."
            # Merge both lines' FY tags + Base/OCO/OOC sub-headers, then dedupe.
            # The main "Resource Summary" line has FY tags in column order, EXCEPT
            # the request year which is shown as Base/OCO/Total sub-columns (its FY tag
            # is on the line ABOVE). So the main line's FYs skip the request year,
            # leaving a 2-year gap where the request year belongs.
            main_fys = [int(fy) for fy in re.findall(r"FY\s*(\d{4})", ln)]
            request_fy = pb_year
            # Build labels by walking main_fys, inserting Base/OCO/Total at the gap
            labels = ["Prior Years"]
            inserted_request = False
            for k, fy in enumerate(main_fys):
                if not inserted_request and fy > request_fy:
                    labels.extend([
                        f"FY {request_fy} Base",
                        f"FY {request_fy} OOC",
                        f"FY {request_fy} Total",
                    ])
                    inserted_request = True
                labels.append(f"FY {fy}")
            if not inserted_request:
                # Request year is at the end of the sequence (uncommon — fallback)
                labels.extend([
                    f"FY {request_fy} Base",
                    f"FY {request_fy} OOC",
                    f"FY {request_fy} Total",
                ])
            labels.extend(["To Complete", "Total"])
            header_labels = labels
            header_idx = i
            n_value_cols = len(labels)
            continue
        if header_labels is None:
            continue
        if "(The following Resource Summary rows" in ln:
            continue
        if "Description:" in ln or "Major Electronics" in ln or "MISSION:" in ln:
            break
        # Match value rows
        m = re.match(r"^\s*([A-Za-z][A-Za-z0-9 ()\$/&,'.\-+]+?)\s{2,}([0-9,*().\-\s]+?)\s*$", ln)
        if m:
            label = m.group(1).strip()
            tokens = re.split(r"\s{2,}", m.group(2).strip())
            if len(tokens) > n_value_cols:
                tokens = tokens[:n_value_cols]
            if len(tokens) < n_value_cols:
                # Right-pad
                tokens = tokens + ["-"] * (n_value_cols - len(tokens))
            for col, tok in zip(header_labels, tokens):
                out.append({
                    "vintage": vintage,
                    "pb_year": pb_year,
                    "li": li,
                    "p1_section": p1_section,
                    "row_label": label,
                    "fy_label": col,
                    "value": tok,
                })
    return out, header_labels


def extract_book(path):
    """Extract all line items from one SCN book. Returns (long_rows, columns_detected)."""
    vintage = detect_vintage(path)
    pb_year = detect_pb_year(path)
    if pb_year is None:
        # Fallback: assume from vintage tag
        pb_year = 2000 + int(vintage[2:])
    with open(path) as f:
        lines = f.read().splitlines()

    long_rows = []
    columns_detected = []

    for item in LINE_ITEMS:
        li = item["li"]
        title = item["title"]
        # Find all "... {li} / {title}" page-header lines. Use word boundary before
        # the LI number, NOT a slash — because Virginia's header reads
        # "BSA 1: Other 2013 / Virginia Class Submarine" (BSA name jams against LI #)
        # whereas Columbia reads "Fleet Ballistic Missile Ships / 1045 / COLUMBIA ...".
        page_marker = re.compile(rf"\b{li}\s*/\s*{re.escape(title.upper())}", re.IGNORECASE)
        # Also catch "1611N ... / {li} / {title}, Advance Procurement"
        idxs = [i for i, ln in enumerate(lines) if page_marker.search(ln)]
        if not idxs:
            continue
        # Identify base section vs AP section by scanning page headers
        base_section_idx = None
        ap_section_idx = None
        for i in idxs:
            # Look back ~50 lines for "Exhibit P-40" + the same LI title
            block_start = max(0, i - 60)
            block = "\n".join(lines[block_start:i + 200])
            if f"{li} / {title}, Advance Procurement" in block:
                if ap_section_idx is None or i < ap_section_idx:
                    ap_section_idx = i
            elif f"{li} / {title}" in block:
                if base_section_idx is None or i < base_section_idx:
                    base_section_idx = i

        # For each section, find the FIRST P-40 table and extract resource summary
        for section_name, sec_idx in (("base", base_section_idx), ("ap", ap_section_idx)):
            if sec_idx is None:
                continue
            # The Resource Summary table is within the first ~80 lines after section start
            rows, hdrs = parse_resource_summary_table(
                lines, sec_idx, sec_idx + 80, li, vintage, pb_year, section_name
            )
            long_rows.extend(rows)
            if hdrs:
                columns_detected.append({
                    "vintage": vintage,
                    "pb_year": pb_year,
                    "li": li,
                    "p1_section": section_name,
                    "columns": "|".join(hdrs),
                })

    return long_rows, columns_detected


def main():
    all_long = []
    all_cols = []
    book_files = sorted(
        f for f in os.listdir(BOOKS_DIR)
        if f.startswith("SCN_Book_FY") and f.endswith(".txt")
    )
    for fname in book_files:
        path = os.path.join(BOOKS_DIR, fname)
        rows, cols = extract_book(path)
        print(f"  {fname}: {len(rows)} long rows, {len(cols)} sections detected")
        all_long.extend(rows)
        all_cols.extend(cols)

    # Write long-form
    out_long = os.path.join(OUT, "scn_li_per_fy_long.csv")
    with open(out_long, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "vintage", "pb_year", "li", "p1_section", "row_label", "fy_label", "value"
        ])
        w.writeheader()
        w.writerows(all_long)
    print(f"Wrote {out_long}  ({len(all_long)} long rows)")

    # Write columns diagnostic
    out_cols = os.path.join(OUT, "scn_per_book_columns.csv")
    with open(out_cols, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["vintage", "pb_year", "li", "p1_section", "columns"])
        w.writeheader()
        w.writerows(all_cols)
    print(f"Wrote {out_cols}")

    # Per-FY actual reconciliation
    # Strategy: for each FY in FY20-FY27, find the most recent book that shows it as
    # "FY YYYY" (actual or estimate). The most recent book has the most-revised number.
    # Priority order: most recent vintage's actual > older vintage's actual > estimate.
    # We treat any cell labeled "FY YYYY" (without Base/OOC/Total suffix) as the
    # canonical actual/estimate column. The book that shows the FY closest to
    # its PB year has the most-revised actual (e.g., for FY22 actual, the FY24
    # book is best since it's pre-Total/post-actual).
    canonical_rows = ["Total Obligation Authority ($ in Millions)",
                      "Net Procurement (P-1) ($ in Millions)",
                      "Gross/Weapon System Cost ($ in Millions)",
                      "Procurement Quantity (Units in Each)"]
    target_fys = list(range(2020, 2028))
    # Index data: (li, p1_section, row_label, fy_int) -> {vintage_pb_year: value}
    idx = defaultdict(dict)
    for r in all_long:
        if r["row_label"] not in canonical_rows:
            continue
        # Accept "FY YYYY" (plain outyear) OR "FY YYYY Total" (request year, sum of Base+OCO).
        # Skip "FY YYYY Base" and "FY YYYY OOC" since "Total" already covers them.
        m = re.match(r"^FY (\d{4})(?: Total)?$", r["fy_label"])
        if not m:
            continue
        fy_int = int(m.group(1))
        key = (r["li"], r["p1_section"], r["row_label"], fy_int)
        # Prefer "Total" over plain — but in practice they're equivalent for the
        # same book (Total exists only on request year). Store plain by default;
        # if both exist for same book/FY, the second one overwrites which is fine.
        idx[key][int(r["pb_year"])] = r["value"]

    out_reconcile = os.path.join(OUT, "scn_per_fy_actual_toa.csv")
    with open(out_reconcile, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "LI", "Section", "Row Label", "FY",
            "Best Value", "Source Vintage (PB Year)",
            "FYs ahead/behind PB", "All Vintages Available"
        ])
        for (li, sec, row_label, fy), vintage_vals in sorted(idx.items()):
            # Best vintage = most recent PB year ≥ fy+2 (gives time for actuals to settle).
            # If no such book, take the most recent that has the FY.
            settled = {pb: v for pb, v in vintage_vals.items() if pb >= fy + 2}
            if settled:
                best_pb = max(settled.keys())
                best_val = settled[best_pb]
            else:
                best_pb = max(vintage_vals.keys())
                best_val = vintage_vals[best_pb]
            all_pbs = ", ".join(f"PB{pb}={vintage_vals[pb]}" for pb in sorted(vintage_vals.keys()))
            w.writerow([li, sec, row_label, fy, best_val, f"PB{best_pb}",
                        best_pb - fy, all_pbs])
    print(f"Wrote {out_reconcile}")


if __name__ == "__main__":
    main()
