"""sources_references - the "References" tab (one module = one sheet).

Primary-source citations + executive commentary, as two native tables, plus a
citation-completeness rollup. Leaf module (loads its CSVs; table names unchanged
from the former source_sheets). A sources sheet: source columns may run wider, but
long quote text is held in the cell, not sized into the workbook.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM_INPUT, S_TITLE_SHEET,
    S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.lib import EXTRACTED
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "sources"
_TAB = "References"

_REF_S1_HEADERS = ["Claim ID", "Label", "Value", "Unit", "Source ID", "Date",
                   "Source title", "Source URL", "Quoted text"]
_REF_S2_HEADERS = ["Quote ID", "Date", "Speaker", "Role", "Company", "Topic",
                   "Quote", "Source URL"]
_S1_HDR_STYLES = ([S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT]
                  + [S_HEADER_LEFT] * 5)


def _ref_load_industry() -> list[dict]:
    out = []
    with (EXTRACTED / "industry_baseline_citations.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            out.append({
                "claim_id": r["claim_id"], "label": r["claim_label"],
                "value": r["value"], "unit": r["unit"],
                "source_id": r["source_id"], "source_date": r["source_date"],
                "source_title": r.get("source_title", ""),
                "source_url": r.get("source_url", ""),
                "quoted_text": r.get("quoted_text", ""),
            })
    return out


def _ref_load_exec() -> list[dict]:
    out = []
    with (EXTRACTED / "exec_commentary_makebuy.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            out.append({
                "quote_id": r["quote_id"], "date": r["date"],
                "speaker": r["speaker"], "role": r["role"],
                "company": r["company_or_org"], "topic": r["topic"],
                "quote": r.get("quote_or_statement", ""),
                "source_url": r.get("source_url_or_doc", ""),
            })
    return out


def _ref_coerce_value(v: str):
    try:
        if "." in v or "e" in v.lower():
            return float(v)
        return int(v)
    except (ValueError, AttributeError):
        return v


_INDUSTRY = _ref_load_industry()
_EXEC = _ref_load_exec()


def _render_references() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner("References", n_cols=9, style=S_TITLE_SHEET)
    c.blank()

    # §1 Primary-source claims
    c.banner("§1 - Industry-baseline primary-source claims (anchors the 50/60/65% band)", n_cols=9,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    s1_header = c.write(_REF_S1_HEADERS, styles=_S1_HDR_STYLES)
    s1_first = c.at()
    for cl in _INDUSTRY:
        v = _ref_coerce_value(cl["value"])
        v_style = S_NUM_INPUT if isinstance(v, (int, float)) else S_DEFAULT
        c.write([cl["claim_id"], cl["label"], v, cl["unit"], cl["source_id"],
                 cl["source_date"], cl["source_title"], cl["source_url"], cl["quoted_text"]],
                styles=[S_DEFAULT, S_DEFAULT, v_style, S_DEFAULT, S_DEFAULT,
                        S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    s1_last = c.at() - 1
    c.blank(2)

    # §2 Executive commentary
    c.banner("§2 - Executive commentary on make/buy (strategy signal, not sizing)", n_cols=9,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    s2_header = c.write(_REF_S2_HEADERS, styles=S_HEADER_LEFT)
    s2_first = c.at()
    for q in _EXEC:
        c.write([q["quote_id"], q["date"], q["speaker"], q["role"], q["company"],
                 q["topic"], q["quote"], q["source_url"]], styles=[S_DEFAULT] * 8, outline_level=1)
    s2_last = c.at() - 1
    c.blank(2)

    # §3 Citation completeness
    _claims_missing = sum(1 for c2 in _INDUSTRY if not (c2["source_url"] or "").strip())
    _exec_missing = sum(1 for q in _EXEC if not (q["source_url"] or "").strip())
    c.banner("§3 - Citation completeness", n_cols=9, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Citation family", "Count", "Missing URL count", "Notes"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    for rec in [
        ["Primary-source claims", len(_INDUSTRY), _claims_missing, "industry-baseline anchors"],
        ["Executive commentary", len(_EXEC), _exec_missing, "strategy signal, not sizing"],
        ["Budget exhibits", 5, 0, "see Source Index"],
        ["Methodology documents", 4, 0, "see Source Index"],
    ]:
        c.write(rec, styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)

    ws = worksheet(c.rows, cols=[34, 36, 18, 12, 18, 14, 40, 42, 44],
                   tab_color=group_color(_GROUP), with_gutter=True)
    tables = [
        ExcelTable(name="tbl_sub_references_claims",
                   ref=f"B{s1_header}:{col_letter(len(_REF_S1_HEADERS))}{s1_last}", headers=_REF_S1_HEADERS),
        ExcelTable(name="tbl_sub_references_exec",
                   ref=f"B{s2_header}:{col_letter(len(_REF_S2_HEADERS))}{s2_last}", headers=_REF_S2_HEADERS),
    ]
    return WorksheetSpec(ws, tables=tables)


REFERENCES = SheetEntry(_TAB, _GROUP, _render_references)
