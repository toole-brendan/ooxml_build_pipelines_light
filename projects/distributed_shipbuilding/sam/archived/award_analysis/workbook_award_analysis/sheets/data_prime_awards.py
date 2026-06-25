"""data_prime_awards - the "Prime Awards" sheet.

Per in-scope PIID: the prime (shipbuilder) contract's base award date, last
action date, action count and block label, from wb_prime_calendar.csv (parsed
from the FPDS pulls, filtered to the in-scope PIID). Context for the Re-buy
timing indicator, which keys each lane's PIID to its prime/block dates.

This is an OVERLAY, not the re-buy clock. The empirical test
(research/extracted/jumpball_prime_clustering.csv) shows supplier re-sourcing
does not track prime award dates - so subaward cadence/turnover leads and this
calendar is context. Two honesty flags travel on every row: PIIDs the FPDS
pulls did not reach show Coverage = no, and a base award at/near the pull's
SIGNED_DATE floor (2018-01-01 subs / 2017-10-01 DDG) shows Base date =
window-floored - it is the earliest pulled action, not the true base award.

Built at import via _make_prime_calendar() into a standalone single-table sheet
(its own title banner, §1 section table, column widths and autofilter).

Promoted accessor (module-level):
  prime_cols() - absolute PIID + base-award-date column ranges.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DATE_INPUT, S_DEFAULT, S_INT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import date_serial, load
from workbook_award_analysis.sheets._widths import (
    W_PIID, W_CLASS, W_BUILDER, W_LABEL, W_DATE, W_COUNT, W_STATUS,
    header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_PRIME_AWARDS

_GROUP = "data"
_TAB = TAB_PRIME_AWARDS
_BANNER = "§1 - Prime awards"

_HEADERS = ["PIID", "Class", "Builder", "Block", "Base award",
            "Last action", "Prime actions", "Action type",
            "Base date", "Coverage"]
_DATE_HDRS = {"Base award", "Last action"}
_NCOLS = len(_HEADERS)
_COLS = [W_PIID, W_CLASS, W_BUILDER, W_LABEL, W_DATE, W_DATE,
         W_COUNT, W_STATUS, W_STATUS, W_CLASS]
_PIID_COL = col_letter(1)            # B
_BASE_COL = col_letter(5)            # F (Prime base award)


def _make_prime_calendar():
    """Build the Prime Awards sheet: a row-2 title banner + the §1 section
    table. Returns (SheetEntry, prime_cols)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_prime_calendar")
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()

    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, _DATE_HDRS))
    f = hdr + 1
    for row in rows:
        floored = row[i["base_is_window_floored"]] == "yes"
        covered = row[i["covered"]] == "yes"
        c.write([row[i["piid"]], row[i["vessel_class"]], row[i["builder"]],
                 row[i["block_label"]],
                 date_serial(row[i["prime_base_award_date"]]),
                 date_serial(row[i["prime_last_action_date"]]),
                 row[i["n_prime_actions"]], row[i["base_action_type"]],
                 "window-floored" if floored else ("actual" if covered else ""),
                 row[i["covered"]]],
                styles=[S_DEFAULT] * 4 + [S_DATE_INPUT] * 2 + [S_INT]
                       + [S_DEFAULT] * 3,
                outline_level=1)
    l = hdr + len(rows)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{l}"
    c.blank(2)
    c.write(["Coverage no = outside FPDS pull; window-floored = earliest "
             "pulled action."],
            styles=[S_DEFAULT])

    def prime_cols() -> dict:
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${f}:${col}${l}"
        return {"piid": rng(_PIID_COL), "base": rng(_BASE_COL)}

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="PrimeAwards", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render), prime_cols


(PRIME_AWARDS, prime_cols) = _make_prime_calendar()
