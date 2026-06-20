"""data_location_master - the "Location Master" tab (DDG, data group; one module = one sheet).

Location evidence and the domestic / foreign split. The former Locations section of
the composite Suppliers tab, now its own tab. Location is a HINT only - the
award-action scope controls. No major downstream accessors.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, build_table
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.lib import EXTRACTED
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "Location Master"
_NCOLS = 4


def _make_locations():
    def _f(x) -> float:
        try:
            return float(str(x).replace(",", "").strip())
        except (TypeError, ValueError):
            return 0.0

    _PRIME_SITES = [
        ["ME", "Maine", "GD Bath Iron Works (BIW)", "final-assembly yard"],
        ["MS", "Mississippi", "HII Ingalls Shipbuilding", "final-assembly yard"],
    ]

    def _foreign_split():
        dom = frn = 0.0
        with (EXTRACTED / "nc_lifetime_vendors.csv").open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                amt = _f(r.get("amount_M_lifetime"))
                flag = (r.get("foreign") or "").strip().lower()
                if flag in ("true", "yes", "y", "1", "t"):
                    frn += amt
                else:
                    dom += amt
        return dom, frn

    _DOM, _FRN = _foreign_split()
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Prime sites
    c.banner("§1 - Prime sites", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    blk, nxt = build_table(c.at(), headers=["State", "Name", "Prime-controlled site", "Role"],
                           data_rows=_PRIME_SITES, header_style=S_HEADER_LEFT, col_styles=S_DEFAULT,
                           start_col=1, outline_level=1)
    c.feed(blk, nxt)
    c.blank(2)

    # §2 Location principle
    c.banner("§2 - Location principle", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Vendor location is context, not a scope test; scope is set per award action."],
            styles=[S_DEFAULT], outline_level=1)
    c.write(["BIW (Maine) + Ingalls (Mississippi) are prime-controlled final-assembly sites; work there is not addressable."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 Domestic / foreign split (formula-driven)
    c.banner("§3 - Domestic / foreign split (foreign / FMS is excluded scope)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Origin", "$M lifetime", "% of total", ""],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    r_dom = c.at()
    r_total = r_dom + 2
    c.write(["Domestic (US)", round(_DOM, 1), f"=C{r_dom}/C{r_total}", ""],
            styles=[S_DEFAULT, S_NUM_INPUT, S_PCT, S_DEFAULT], outline_level=1)
    r_frn = c.write(["Foreign", round(_FRN, 1), f"=C{r_dom + 1}/C{r_total}", ""],
                    styles=[S_DEFAULT, S_NUM_INPUT, S_PCT, S_DEFAULT], outline_level=1)
    c.total(["Total", f"=SUM(C{r_dom}:C{r_frn})", f"=SUM(D{r_dom}:D{r_frn})", ""],
            styles=[S_BOLD, S_NUM, S_PCT, S_DEFAULT], n_cols=4)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[18, 18, 14, 30],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


LOCATION_MASTER = _make_locations()
