"""data_production_schedule - the "Production Schedule" tab (DDG, data group).

Hull -> yard -> FY build schedule + hull-count support. The former Production
section of the composite Budget tab, now its own tab. The in-window hull count is
consumed by TAM Build (per-hull views).

Promoted accessors (Python counts; base-free):
  hull_count, in_window_hull_count
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, build_table, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_TITLE_SHEET,
    S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._bind import EXTRACTED
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "data"
_TAB = "DDG Production Schedule"
_NCOLS = 6
_WINDOW_FYS = range(2022, 2028)


def _make_production_schedule():
    _PROD_HEADERS = ["Ship", "Shipbuilder", "FY", "Contract award",
                     "Start construction", "Delivery"]

    def _prod_load():
        out = []
        with (EXTRACTED / "scn_li_production_schedule.csv").open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                out.append({"ship": (r.get("Ship") or "").strip(),
                            "yard": (r.get("Shipbuilder") or "").strip(),
                            "fy": (r.get("FY") or "").strip(),
                            "award": (r.get("Contract Award") or "").strip(),
                            "start": (r.get("Start Construction") or "").strip(),
                            "delivery": (r.get("Delivery Date") or "").strip()})
        return out

    _PROD = _prod_load()

    def _yard_counts():
        counts = {}
        for r in _PROD:
            y = r["yard"] or "(unspecified)"
            counts[y] = counts.get(y, 0) + 1
        return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)

    def hull_count() -> int:
        return len(_PROD)

    def in_window_hull_count() -> int:
        return sum(1 for r in _PROD if r["fy"].isdigit() and int(r["fy"]) in _WINDOW_FYS)

    tables: list[ExcelTable] = []
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Hull schedule (native table)
    c.banner("§1 - Hull schedule (hull -> yard -> FY)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    prod_hdr = c.at()
    data_rows = [[r["ship"], r["yard"], r["fy"], r["award"], r["start"], r["delivery"]] for r in _PROD]
    blk, nxt = build_table(prod_hdr, headers=_PROD_HEADERS, data_rows=data_rows,
                           header_style=S_HEADER_LEFT, col_styles=S_DEFAULT, start_col=1, outline_level=1)
    c.feed(blk, nxt)
    tables.append(ExcelTable(name="tbl_ddg_production",
                             ref=f"B{prod_hdr}:{col_letter(len(_PROD_HEADERS))}{prod_hdr + len(_PROD)}",
                             headers=_PROD_HEADERS))
    c.blank(2)

    # §2 Hull count by yard
    c.banner("§2 - Hull count by yard", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    yb_hdr = c.at()
    sum_rows = [[y, str(cnt), "", "", "", ""] for y, cnt in _yard_counts()]
    blk2, ye = build_table(yb_hdr, headers=["Yard", "Hulls", "", "", "", ""], data_rows=sum_rows,
                           header_style=S_HEADER_LEFT, col_styles=S_DEFAULT, start_col=1, outline_level=1)
    c.feed(blk2, ye)
    c.blank(2)

    # §3 Model window
    c.banner("§3 - Model window", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Hulls in schedule (all FY)", hull_count()],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["In-window hulls (award FY22-27)", in_window_hull_count()],
            styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.write(["FY2026 award hulls (DDG 147, DDG 149): funded by OBBBA Sec. 20002(17) "
             "mandatory appropriation."],
            styles=[S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[26, 18, 8, 20, 20, 16],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=tables)

    return SheetEntry(_TAB, _GROUP, render), hull_count, in_window_hull_count


(PRODUCTION_SCHEDULE, hull_count, in_window_hull_count) = _make_production_schedule()
