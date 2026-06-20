#!/usr/bin/env python3
"""
Extract Columbia (LI 1045) and Virginia (LI 2013) line item structured data from
the FY27 SCN justification book.

Outputs (in extracted/):
  scn_li_resource_summary.csv     P-1 line-item resource summary (Prior Years / FY25 actual /
                                  FY26 estimate / FY27 base / FY27 OOC / FY27 total / FY28-31 /
                                  To Complete / Total)
  scn_li_cost_categories.csv      P-5c Ship Cost Analysis — cost-category breakdown per ship hull,
                                  per FY (Plan / Basic Construction / Change Orders / Electronics /
                                  Propulsion / HM&E / Ordnance / Other / Total Ship Estimate)
  scn_li_production_schedule.csv  P-27 ship production schedule — hull, shipbuilder, FY of
                                  authorization, contract award date, start of construction,
                                  delivery date
  scn_li_text_sections.md         Full prose sections (Description, MISSION, notes about
                                  Contracts/MIB) per line item for follow-up reading

This is a parser for layout-preserved pdftotext output. It is line-grep-based — not a fully
robust PDF parser. Spot-check the CSVs against the PDF before relying on numbers.
"""
import csv
import os
import re
import sys
from collections import defaultdict

SRC = "/Users/brendantoole/projects2/submarine_outsourced_work/budget_books/SCN_Book_FY27.txt"
OUT = "/Users/brendantoole/projects2/submarine_outsourced_work/extracted"
os.makedirs(OUT, exist_ok=True)

# Each line item is a contiguous range of pages in the SCN book.
# Identified by the "P-1 Line #N" footer that repeats on every page.
LINE_ITEMS = [
    {"li": 1045, "title": "COLUMBIA Class Submarine", "p1_line": 1,
     "appropriation": "1611N", "ba": "01", "bsa": "1",
     "ba_name": "Fleet Ballistic Missile Ships"},
    {"li": 1045, "title": "COLUMBIA Class Submarine, Advance Procurement", "p1_line": 2,
     "appropriation": "1611N", "ba": "01", "bsa": "1",
     "ba_name": "Fleet Ballistic Missile Ships"},
    {"li": 2013, "title": "Virginia Class Submarine", "p1_line": 6,
     "appropriation": "1611N", "ba": "02", "bsa": "1",
     "ba_name": "Other Warships"},
    {"li": 2013, "title": "Virginia Class Submarine, Advance Procurement", "p1_line": 7,
     "appropriation": "1611N", "ba": "02", "bsa": "1",
     "ba_name": "Other Warships"},
]


def load_text():
    with open(SRC) as f:
        return f.read()


def find_p1_line_pages(text, p1_line):
    """Find page-marker lines like 'P-1 Line #1' and return (start_line_idx, end_line_idx)
    in the file for the entire contiguous block. Multiple P-1 lines exist; each block is
    a range of consecutive lines that share the marker."""
    lines = text.splitlines()
    marker = re.compile(rf"\bP-1 Line #{p1_line}\b")
    matched = [i for i, ln in enumerate(lines) if marker.search(ln)]
    if not matched:
        return None, None
    # The block extends from the first page where this marker appears,
    # going backwards to the previous page boundary, through the last page where it appears
    # forwards to the next page boundary. Approximate with the matched-line range, plus
    # some context.
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

    # Locate the "Resource Summary" header line + the following numeric rows
    out_rows = []
    found_header = False
    # Iterate per-line within the block
    block_lines = block.splitlines()
    for i, ln in enumerate(block_lines):
        if "Resource Summary" in ln and ("Prior" in block_lines[i - 1] or "Prior" in ln):
            found_header = True
            continue
        # The numeric rows tend to look like:
        # "Procurement Quantity (Units in Each)                              2          -                   1               1         -                   1               1                1               1               1              4            12"
        # "Gross/Weapon System Cost ($ in Millions)              26,810.410          0.000      10,744.317       ..."
        if found_header:
            # Stop conditions
            if "(The following Resource Summary rows" in ln:
                continue
            if "Description:" in ln or "Major Electronics" in ln or "MISSION:" in ln:
                break
            # Try to match: row_label + 11ish numeric tokens (commas allowed)
            # The label can have a "$ in Millions" or similar suffix
            m = re.match(r"^\s*([A-Za-z][A-Za-z0-9 ()\$/&,'.\-+]+?)\s{2,}([0-9,*().\-\s]+?)\s*$", ln)
            if m:
                label = m.group(1).strip()
                nums_str = m.group(2).strip()
                # Split by 2+ whitespace
                tokens = re.split(r"\s{2,}", nums_str)
                # Reduce labels we don't care about — but keep them; later filtering.
                out_rows.append({
                    "li": li,
                    "p1_line": p1_line,
                    "row_label": label,
                    "raw_values": tokens,
                })
    return out_rows


def extract_p5c_ship_cost(text, li, p1_line):
    """Extract P-5c Ship Cost Analysis tables — one per page, each shows a single ship
    (or up to 4 hulls per table) with cost categories."""
    lines = text.splitlines()
    block_rows = []
    marker = re.compile(rf"\bP-1 Line #{p1_line}\b")
    in_p5c = False
    fy_headers = []
    for i, ln in enumerate(lines):
        if not marker.search(ln) and "Exhibit P-5c" not in ln:
            # only relevant if we're already in a P-5c context for this line item
            pass
        if "Exhibit P-5c" in ln:
            # Check next ~5 lines for our LI marker (page header is right after Exhibit line).
            # Don't require P-1 Line marker — it's in the page footer, beyond our window.
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
        # End of section
        if "Remarks:" in ln or "Exhibit P-" in ln:
            in_p5c = False
            continue
        # FY header row(s)
        fy_matches = re.findall(r"FY\s*(\d{4})", ln)
        if fy_matches and len(fy_matches) >= 2:
            fy_headers = fy_matches
            continue
        # Cost category row: label + 2 OR 4 OR 8 numeric pairs (Qty, $M)
        m = re.match(r"^\s*([A-Za-z][A-Za-z0-9 ,()/&\-\.]+?)(?:\s*\(†\))?\s{2,}(.+?)\s*$", ln)
        if m:
            label = m.group(1).strip()
            # Skip noise lines
            if label.lower().startswith(("page", "navy", "appropriation", "1611n", "less ",
                                          "net p-1", "li ", "ba ", "bsa ", "id code", "cost categories",
                                          "remarks", "exhibit", "fy ", "(†)")):
                continue
            tokens = re.split(r"\s{2,}", m.group(2).strip())
            # Only keep if the token list looks numeric
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
    start of construction, delivery date."""
    lines = text.splitlines()
    marker = re.compile(rf"\bP-1 Line #{p1_line}\b")
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
            r"^\s*(SS[BNG]N?\s*\d+|SSN[\s\-]?\d+)\s+(.+?)\s+(\d{4})\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s+([A-Z][a-z]{2,3}\s*\d{4}|TBD|N/A)\s*$",
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
        # Pattern B (footnoted): ship name alone on its own line, followed by indented "(n)
        # shipbuilder ..." row with the same fields.
        m1 = re.match(r"^\s*(SS[BNG]N?\s*\d+|SSN[\s\-]?\d+)\s*$", ln)
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


def main():
    text = load_text()

    # Resource summaries
    rs_rows = []
    for item in LINE_ITEMS:
        rs_rows.extend(extract_resource_summary(text, item["li"], item["p1_line"]))
    if rs_rows:
        # Find the max number of value columns across all rows
        max_cols = max(len(r["raw_values"]) for r in rs_rows)
        # Column labels per FY27 SCN P-40: Prior Years, FY 2025, FY 2026, FY 2027 Base,
        # FY 2027 OOC, FY 2027 Total, FY 2028, FY 2029, FY 2030, FY 2031, To Complete, Total
        # = 12 columns. If a row has fewer values, the rightmost cols get blank.
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
        print(f"Wrote scn_li_resource_summary.csv ({len(rs_rows)} rows)")

    # P-5c cost categories
    p5_rows = []
    for item in LINE_ITEMS:
        if "Advance Procurement" in item["title"]:
            continue  # AP lines don't have P-5c
        p5_rows.extend(extract_p5c_ship_cost(text, item["li"], item["p1_line"]))
    if p5_rows:
        max_cols = max(len(r["raw_values"]) for r in p5_rows)
        with open(os.path.join(OUT, "scn_li_cost_categories.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["LI", "P-1 Line", "Cost Category", "FY Headers"] +
                       [f"v{i}" for i in range(max_cols)])
            for r in p5_rows:
                w.writerow(
                    [r["li"], r["p1_line"], r["cost_category"], "|".join(r["fy_columns"])] +
                    r["raw_values"] + [""] * (max_cols - len(r["raw_values"]))
                )
        print(f"Wrote scn_li_cost_categories.csv ({len(p5_rows)} rows)")

    # P-27 production schedule
    p27_rows = []
    for item in LINE_ITEMS:
        if "Advance Procurement" in item["title"]:
            continue
        p27_rows.extend(extract_p27_schedule(text, item["li"], item["p1_line"]))
    if p27_rows:
        with open(os.path.join(OUT, "scn_li_production_schedule.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["LI", "P-1 Line", "Ship", "Shipbuilder", "FY", "Contract Award",
                        "Start Construction", "Delivery Date"])
            for r in p27_rows:
                w.writerow([r["li"], r["p1_line"], r["ship"], r["shipbuilder"],
                            r["fiscal_year"], r["contract_award"],
                            r["start_construction"], r["delivery_date"]])
        print(f"Wrote scn_li_production_schedule.csv ({len(p27_rows)} rows)")


if __name__ == "__main__":
    main()
