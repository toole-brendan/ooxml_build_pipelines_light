#!/usr/bin/env python3
"""
Extract Exhibit P-10 (Advance Procurement Requirements Analysis) detail from
all 6 SCN budget books for Columbia (LI 1045) and Virginia (LI 2013).

Captures per-category, per-FY AP dollar amounts. Categories differ between classes:

  Columbia P-10 structure (~13 categories):
    PLANS (1), BASIC CONSTRUCTION (3) - SHIPBUILDER PROCURED LLTM,
    BASIC CONSTRUCTION (4) - MISSILE TUBE ..., BASIC CONSTRUCTION (5) - ADVANCE CONSTRUCTION,
    BASIC CONSTRUCTION (6) - EOQ ..., BASIC CONSTRUCTION (7) - SHIPYARD MANUFACTURED ...,
    NUCLEAR PROPULSION PLANT EQUIPMENT (8), HM&E (9),
    ORDNANCE SWS SHIPBOARD SYSTEMS (10) - LLTM,
    ORDNANCE SWS SHIPBOARD SYSTEMS (11) - ECONOMIC ...,
    ORDNANCE SWS SHIPBOARD SYSTEMS (12) - CONTINUOUS,
    ELECTRONICS (13), Electronics EOQ (14)

  Virginia P-10 structure (3 top-level + sub-items):
    Advance Procurement (with sub-items: Nuclear Propulsion Plant, Electronics,
      Non-Nuclear Propulsion / Propulsor, Long Lead-Time CFE One Year AP, ...Two Year AP)
    Economic Order of Quantity (with per-future-hull EOQ sub-items)
    Plans (with: Supplier Development - SIB, Nuclear Shipbuilder Productivity Enhancements)
    Total Advance Procurement/Obligation Authority (grand total)

Outputs:
  extracted/scn_p10_ap_long.csv   — long form: vintage, pb_year, li, class,
                                    category, fy, value_$M
  extracted/scn_p10_ap_reconciled.csv — best per (li, class, category, fy)
  extracted/scn_p10_ap_buckets.csv — grouped into deck-narrative buckets

Deck-narrative buckets:
  - Nuclear plant LLTM  (BPMI / Naval Reactors)
  - Electronics LLTM   (combat systems / sonar)
  - Propulsor LLTM     (non-nuclear propulsion / shaft / propulsor)
  - Shipbuilder-procured LLTM (CFE / BC(3) / BC(5) / BC(7))
  - Missile compartment LLTM (Col only; BC(4))
  - EOQ                (Economic Order Quantity; multi-year savings)
  - HM&E LLTM          (Col only)
  - Ordnance LLTM      (Col only; ORDNANCE SWS)
  - Plans / SIB        (workforce / Submarine Industrial Base)
"""
import csv
import os
import re
from collections import defaultdict

BOOKS_DIR = "/Users/brendantoole/projects2/submarine_outsourced_work/budget_books"
OUT = "/Users/brendantoole/projects2/submarine_outsourced_work/extracted"

LINE_ITEMS = {
    "1045": "Columbia",
    "2013": "Virginia",
}


def parse_value(v):
    if v is None:
        return None
    s = str(v).strip()
    if not s or s in ("-", "--"):
        return None
    s = s.replace(",", "").replace("$", "")
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def detect_vintage(path):
    m = re.search(r"FY(\d{2})", os.path.basename(path))
    return f"FY{m.group(1)}" if m else "unknown"


def detect_pb_year(path):
    with open(path) as f:
        head = "".join(f.readline() for _ in range(40))
    m = re.search(r"Fiscal Year \(FY\) (\d{4}) Budget Estimates", head)
    return int(m.group(1)) if m else None


def find_p10_pages(lines, li):
    """Find all (start, end) line index ranges for P-10 page-1 sections
    associated with this LI. P-10 page 1 contains the per-FY values we want."""
    # P-10 page 1 header pattern
    p10_pattern = re.compile(
        r"Exhibit P-10, Advance Procurement Requirements Analysis \(page 1"
    )
    li_pattern = re.compile(rf"\b{li}\s*/\s*(COLUMBIA|Virginia) Class Submarine")

    # Find all P-10 page-1 markers, then check the following ~5 lines for
    # this LI's identifier.
    sections = []
    p10_starts = [i for i, ln in enumerate(lines) if p10_pattern.search(ln)]
    for idx, start in enumerate(p10_starts):
        # Look ahead 5 lines for LI marker
        block = "\n".join(lines[start:start + 6])
        if li_pattern.search(block):
            # End at next P-10 marker OR next "Exhibit P-" OR LI footer
            end = p10_starts[idx + 1] if idx + 1 < len(p10_starts) else min(start + 800, len(lines))
            sections.append((start, end))
    return sections


def parse_fy_header(lines, section_start, section_end):
    """Find the FY header row in a P-10 section. Returns list of FYs (int) in column order."""
    for i in range(section_start, min(section_start + 20, section_end)):
        ln = lines[i]
        fy_matches = re.findall(r"FY\s*(\d{4})", ln)
        if len(fy_matches) >= 3:
            return [int(fy) for fy in fy_matches]
    return None


# Category detection patterns
# Match section headers like "PLANS (1)", "BASIC CONSTRUCTION (3) - SHIPBUILDER PROCURED LLTM"
COL_CATEGORY_PATTERNS = [
    r"^\s*PLANS \(\d+\)\s*$",
    r"^\s*BASIC CONSTRUCTION \(\d+\)( - .*)?\s*$",
    r"^\s*NUCLEAR PROPULSION PLANT EQUIPMENT \(\d+\)\s*$",
    r"^\s*HM&E \(\d+\)\s*$",
    r"^\s*ORDNANCE.*\(\d+\)( - .*)?\s*$",
    r"^\s*ELECTRONICS \(\d+\)\s*$",
    r"^\s*Electronics EOQ \(\d+\)\s*$",
]

# Virginia uses different top-level headers
VA_TOP_LEVEL_HEADERS = [
    r"^\s*Advance Procurement\s*$",
    r"^\s*Economic Order of Quantity\s*$",
    r"^\s*Plans\s*$",
]

# Total: line — collect these as canonical per-category per-FY totals.
TOTAL_LINE_RE = re.compile(r"^\s*Total:\s*(.+?)\s{2,}([\d,.()\-\s]+)\s*$")
GRAND_TOTAL_RE = re.compile(r"^\s*Total Advance Procurement/Obligation Authority\s+([\d,.()\-\s]+)\s*$")
# Va sub-item rows look like: "                  (4)         1,273.090   1,336.590  ..."
# The label is on the line BEFORE this (possibly with leadtime text trailing).
# Examples of labels:
#   "Nuclear Propulsion Plant Equipment                                                    30-72         Various"
#   "Long Lead-Time CFE One Year AP                                                        24-58         Various"
# We strip the trailing leadtime/required columns from the label.
VA_SUBITEM_RE = re.compile(r"^\s*\((\d+)\)\s+([\d,.()\-\s]+)\s*$")

# Known Va sub-item labels (used to validate label-from-prior-line)
VA_KNOWN_SUBITEM_LABELS = {
    "Nuclear Propulsion Plant Equipment": "Nuclear Propulsion Plant Equipment LLTM",
    "Electronics Equipment": "Electronics Equipment LLTM",
    "NON-Nuclear Propulsion Plant Equipment - Propulsor": "Non-Nuclear Propulsion / Propulsor LLTM",
    "Long Lead-Time CFE One Year AP": "Long Lead-Time CFE One Year AP",
    "Long Lead-Time CFE Two Year AP": "Long Lead-Time CFE Two Year AP",
    "Supplier Development - Submarine Industrial Base": "Plans: Supplier Development - SIB",
    "Nuclear Shipbuilder Productivity Enhancements": "Plans: Nuclear Shipbuilder Productivity Enhancements",
}


def clean_va_label(raw_label):
    """Strip trailing 'NN-NN  Various' (Production Leadtime + When Required) columns
    from a Va sub-item label line, returning just the descriptive label."""
    # Remove trailing patterns like '30-72   Various' or '24-58   Various'
    cleaned = re.sub(r"\s+\d+-\d+\s+\w+\s*$", "", raw_label).strip()
    return cleaned


def parse_section(lines, section_start, section_end, vintage, pb_year, li, cls):
    """Extract per-category per-FY values from one P-10 section. Returns list of dicts."""
    out = []
    fys = parse_fy_header(lines, section_start, section_end)
    if not fys:
        return out

    n_fy_cols = len(fys)

    for i in range(section_start, section_end):
        ln = lines[i]
        # Stop if we hit the next major exhibit
        if "Exhibit P-" in ln and "Exhibit P-10, Advance Procurement Requirements Analysis (page 1" not in ln:
            if i > section_start + 5:
                break

        # Match Total: <category>  <values...> (single-line case)
        m = TOTAL_LINE_RE.match(ln)
        if m:
            cat_label = m.group(1).strip()
            value_str = m.group(2).strip()
            # Parse values into n_fy_cols tokens
            tokens = re.split(r"\s{2,}", value_str)
            tokens = [t for t in tokens if t.strip()]
            if len(tokens) > n_fy_cols:
                tokens = tokens[:n_fy_cols]
            for fy, tok in zip(fys, tokens):
                val = parse_value(tok)
                if val is not None:
                    out.append({
                        "vintage": vintage,
                        "pb_year": pb_year,
                        "li": li,
                        "class": cls,
                        "category": cat_label,
                        "is_total": "yes",
                        "fy": fy,
                        "value_$M": val,
                    })
            continue

        # Multi-line Total: header — when category name is too long, it wraps.
        # Line N:   "Total: BASIC CONSTRUCTION (6) - EOQ IN SUPPORT OF MULTI-"
        # Line N+1: "                              489.266    376.645   ..."  (values)
        # Line N+2: "PROGRAM PROCUREMENT"                                     (label continuation)
        m_multi = re.match(r"^\s*Total:\s*(.+?)\s*$", ln)
        if m_multi and "Total:" in ln and i + 1 < section_end:
            partial_label = m_multi.group(1).strip()
            next_line = lines[i + 1].strip()
            # Check if next line is values-only (numbers + dashes only)
            if re.match(r"^[\d,.()\-\s]+$", next_line) and re.search(r"\d", next_line):
                # Try to read the continuation line (i+2) for the rest of label
                cont = lines[i + 2].strip() if i + 2 < section_end else ""
                # Don't merge if cont looks like start of another section
                # (e.g., a new category header all-caps with a number)
                if cont and not re.match(r"^[A-Z][A-Z &]+\(\d+\)", cont):
                    full_label = partial_label.rstrip("-").strip() + " " + cont
                    full_label = re.sub(r"\s+", " ", full_label)
                else:
                    full_label = partial_label
                tokens = re.split(r"\s{2,}", next_line)
                tokens = [t for t in tokens if t.strip()]
                if len(tokens) > n_fy_cols:
                    tokens = tokens[:n_fy_cols]
                for fy, tok in zip(fys, tokens):
                    val = parse_value(tok)
                    if val is not None:
                        out.append({
                            "vintage": vintage,
                            "pb_year": pb_year,
                            "li": li,
                            "class": cls,
                            "category": full_label,
                            "is_total": "yes",
                            "fy": fy,
                            "value_$M": val,
                        })
                continue

        # Match grand total (Va only)
        m = GRAND_TOTAL_RE.match(ln)
        if m:
            value_str = m.group(1).strip()
            tokens = re.split(r"\s{2,}", value_str)
            tokens = [t for t in tokens if t.strip()]
            if len(tokens) > n_fy_cols:
                tokens = tokens[:n_fy_cols]
            for fy, tok in zip(fys, tokens):
                val = parse_value(tok)
                if val is not None:
                    out.append({
                        "vintage": vintage,
                        "pb_year": pb_year,
                        "li": li,
                        "class": cls,
                        "category": "TOTAL: Advance Procurement / Obligation Authority",
                        "is_total": "grand",
                        "fy": fy,
                        "value_$M": val,
                    })
            continue

        # Va sub-item: Two patterns:
        #   A: "    (N)    val1   val2   ..." — values inline; label is on the
        #      NEXT line below.
        #   B: "    (N)" alone — values are on the next line; label is on the
        #      line AFTER that.
        if cls == "Virginia":
            value_str = None
            label_line_idx = None
            m = VA_SUBITEM_RE.match(ln)
            if m:
                # Pattern A: (N) with inline values
                inline = m.group(2).strip()
                if re.search(r"\d", inline):
                    value_str = inline
                    label_line_idx = i + 1
            if value_str is None and re.match(r"^\s*\(\d+\)\s*$", ln):
                # Pattern B: (N) alone — peek at next line for values
                if i + 1 < section_end:
                    next_line = lines[i + 1].strip()
                    if re.match(r"^[\d,.()\-\s]+$", next_line) and re.search(r"\d", next_line):
                        value_str = next_line
                        label_line_idx = i + 2
            if value_str and label_line_idx is not None and label_line_idx < section_end:
                tokens = re.split(r"\s{2,}", value_str)
                tokens = [t for t in tokens if t.strip()]
                if len(tokens) < 2:
                    pass
                else:
                    if len(tokens) > n_fy_cols:
                        tokens = tokens[:n_fy_cols]
                    label_line = lines[label_line_idx].strip()
                    cleaned = clean_va_label(label_line)
                    label = VA_KNOWN_SUBITEM_LABELS.get(cleaned)
                    if label is None:
                        # Some labels have an "(NNNN SSNs)" parenthetical suffix
                        cleaned2 = re.sub(r"\s*\(\d+ SSNs\)\s*$", "", cleaned).strip()
                        label = VA_KNOWN_SUBITEM_LABELS.get(cleaned2)
                    if label is not None:
                        for fy, tok in zip(fys, tokens):
                            val = parse_value(tok)
                            if val is not None:
                                out.append({
                                    "vintage": vintage,
                                    "pb_year": pb_year,
                                    "li": li,
                                    "class": cls,
                                    "category": label,
                                    "is_total": "subitem",
                                    "fy": fy,
                                    "value_$M": val,
                                })
                        continue

    return out


def extract_book(path):
    vintage = detect_vintage(path)
    pb_year = detect_pb_year(path)
    if pb_year is None:
        pb_year = 2000 + int(vintage[2:])
    with open(path) as f:
        lines = f.read().splitlines()

    rows = []
    for li, cls in LINE_ITEMS.items():
        sections = find_p10_pages(lines, li)
        for sec_start, sec_end in sections:
            rows.extend(parse_section(lines, sec_start, sec_end, vintage, pb_year, li, cls))
    return rows


# Bucket mapping — group raw category labels into deck-narrative buckets
def map_to_bucket(raw_cat):
    rc = raw_cat.upper()
    # Va sub-items first (explicit labels)
    if "LONG LEAD-TIME CFE" in rc:
        return "Shipbuilder-procured LLTM (CFE)"
    if "NON-NUCLEAR PROPULSION" in rc or "PROPULSOR" in rc:
        return "Propulsor LLTM"
    if "PLANS: SUPPLIER DEVELOPMENT" in rc or "PLANS: NUCLEAR SHIPBUILDER" in rc:
        return "Plans / SIB"
    if "ECONOMIC ORDER OF QUANTITY" in rc or "ECONOMIC ORDER QUANTITY" in rc:
        return "EOQ"
    # Col categories
    if "PLANS" in rc and "(1)" in rc:
        return "Plans / SIB"
    if rc.strip() == "PLANS":  # Va top-level
        return "Plans / SIB"
    if "SHIPBUILDER PROCURED" in rc or "SHIPYARD MANUFACTURED" in rc:
        return "Shipbuilder-procured LLTM"
    if "ADVANCE CONSTRUCTION" in rc:
        return "Shipbuilder-procured LLTM"
    if "MISSILE TUBE" in rc:
        return "Missile compartment LLTM"
    if "EOQ" in rc and "ELECTRONIC" not in rc and "ORDNANCE" not in rc:
        return "EOQ"
    if "NUCLEAR PROPULSION" in rc:
        return "Nuclear plant LLTM"
    if "HM&E" in rc:
        return "HM&E LLTM"
    if "ORDNANCE" in rc:
        return "Ordnance LLTM"
    if "ELECTRONIC" in rc:
        return "Electronics LLTM"
    if rc.strip() == "ADVANCE PROCUREMENT":  # Va top-level
        return "Advance Procurement (Va sub-total)"
    if "OBLIGATION AUTHORITY" in rc:
        return "Grand Total"
    return f"Other: {raw_cat}"


def reconcile_best_vintage(vintage_vals, fy):
    if not vintage_vals:
        return None, None
    settled = {pb: v for pb, v in vintage_vals.items() if pb >= fy + 2}
    if settled:
        best_pb = max(settled.keys())
    else:
        best_pb = max(vintage_vals.keys())
    return vintage_vals[best_pb], best_pb


def main():
    book_files = sorted(
        f for f in os.listdir(BOOKS_DIR)
        if f.startswith("SCN_Book_FY") and f.endswith(".txt")
    )

    all_rows = []
    for fname in book_files:
        path = os.path.join(BOOKS_DIR, fname)
        rows = extract_book(path)
        print(f"  {fname}: {len(rows)} P-10 rows")
        all_rows.extend(rows)

    # Write long form
    long_path = os.path.join(OUT, "scn_p10_ap_long.csv")
    with open(long_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "vintage", "pb_year", "li", "class", "category", "is_total", "fy", "value_$M"
        ])
        w.writeheader()
        for r in all_rows:
            r2 = dict(r)
            r2["value_$M"] = f"{r['value_$M']:.3f}"
            w.writerow(r2)
    print(f"Wrote {long_path}  ({len(all_rows)} rows)")

    # Reconcile across vintages: (li, category, fy) -> best_value, best_pb
    idx = defaultdict(dict)
    for r in all_rows:
        key = (r["li"], r["category"], r["fy"])
        idx[key][r["pb_year"]] = r["value_$M"]

    rec_path = os.path.join(OUT, "scn_p10_ap_reconciled.csv")
    with open(rec_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["LI", "Class", "Category", "Bucket", "FY", "Best Value $M",
                    "Source PB", "All Vintages"])
        for (li, cat, fy), vintages in sorted(idx.items()):
            best_val, best_pb = reconcile_best_vintage(vintages, fy)
            all_v = ", ".join(f"PB{pb}={v:.3f}" for pb, v in sorted(vintages.items()))
            cls = LINE_ITEMS[li]
            w.writerow([li, cls, cat, map_to_bucket(cat), fy,
                        f"{best_val:.3f}", f"PB{best_pb}", all_v])
    print(f"Wrote {rec_path}")

    # Buckets summary: per (li, bucket, fy) — sum the right rows per class.
    # Col rows have is_total='yes' for "Total: <CATEGORY>" lines — use those.
    # Va rows have is_total='subitem' for the sub-items (the per-label rows) AND
    # is_total='yes' for "Total: Advance Procurement / EOQ / Plans" parents.
    # For Va we want to use the SUB-ITEMS for granular buckets, but fall back to
    # the parent Total for EOQ and Plans (which don't have sub-items captured).
    bucket_idx = defaultdict(lambda: defaultdict(dict))  # (li, bucket, fy) -> {pb: value}
    for r in all_rows:
        cls = r["class"]
        if r["is_total"] == "grand":
            continue
        bucket = map_to_bucket(r["category"])
        if bucket == "Grand Total":
            continue
        # Va: skip the parent "Advance Procurement" total (it would double-count
        # the sub-items we already capture).
        if cls == "Virginia" and bucket == "Advance Procurement (Va sub-total)":
            continue
        # Col: keep is_total='yes' rows only.
        # Va: keep is_total='subitem' rows + is_total='yes' rows that aren't the
        # "Advance Procurement" parent (i.e., Va EOQ + Va Plans totals are kept).
        if cls == "Columbia" and r["is_total"] != "yes":
            continue
        if cls == "Virginia" and r["is_total"] not in ("subitem", "yes"):
            continue
        bk_key = (r["li"], bucket, r["fy"])
        if r["pb_year"] not in bucket_idx[bk_key]:
            bucket_idx[bk_key][r["pb_year"]] = 0.0
        bucket_idx[bk_key][r["pb_year"]] += r["value_$M"]

    buckets_path = os.path.join(OUT, "scn_p10_ap_buckets.csv")
    with open(buckets_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["LI", "Class", "Bucket", "FY", "Best Value $M", "Source PB"])
        for (li, bucket, fy), vintages in sorted(bucket_idx.items()):
            best_val, best_pb = reconcile_best_vintage(vintages, fy)
            cls = LINE_ITEMS[li]
            w.writerow([li, cls, bucket, fy, f"{best_val:.3f}", f"PB{best_pb}"])
    print(f"Wrote {buckets_path}")


if __name__ == "__main__":
    main()
