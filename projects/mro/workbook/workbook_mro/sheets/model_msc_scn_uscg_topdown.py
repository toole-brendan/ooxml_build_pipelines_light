"""MSC / SCN / USCG / OPN LI 1000 top-down maintenance anchors (non-1B4B).

Budget-exhibit input cells for four streams - MSC M&R, SCN CVN RCOH (LI 2086), USCG
ISVS, and OPN LI 1000 - each a small banded input block from the FY25 exhibits.

LAYOUT: B..G = Code, Category, FY24 $K, FY25 $K, FY26 $K, Source; FY25 in col E,
FY26 in col F. Exposes the per-stream anchor cells as closure accessors.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM_INPUT, S_NUM, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor

_GROUP = "model"
_TAB = "MSC SCN USCG Top-Down"
_NCOLS = 6                      # B..G: Code, Category, FY24, FY25, FY26, Source
_FY25 = "E"                     # FY25 $K column
_FY26 = "F"                     # FY26 $K column
_COLS = [12, 44, 12, 12, 12, 12]
_HEADERS = ["Code", "Category", "FY24 $K", "FY25 $K", "FY26 $K", "Source"]


def _make():
    P: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    def _header():
        c.write(_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER,
                                  S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])

    def _row(key, code, cat, fy24, fy25, fy26, src, *, total=False):
        vals = [code, cat, fy24, fy25, fy26, src]
        if total:
            # Subtotal/total bar: c.total() upgrades base styles to the bordered
            # variants so the divider runs continuously across the whole row.
            r = c.total(vals,
                        styles=[S_BOLD, S_BOLD, S_NUM, S_NUM, S_NUM, S_DEFAULT],
                        n_cols=_NCOLS, outline_level=1)
        else:
            r = c.write(vals,
                        styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_NUM_INPUT, S_NUM_INPUT,
                                S_DEFAULT], outline_level=1)
        if key:
            P[key] = r
        return r

    # §1 - Military Sealift Command (MSC) M&R
    c.banner("§1 - Military Sealift Command (MSC) M&R", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _header()
    _row("msc_1b1b", "FY25_1B1B", "FY25 MSC M&R anchor (1B1B transfer-out to 1B4B)",
         None, 1239846, None, "L4467")
    _row("msc_mta", "MTA", "Mid-Term Availability", 0, 0, 341925, "L5648")
    _row("msc_roh", "ROH", "Regular Overhaul", 0, 0, 666329, "L5649")
    _row("msc_other", "OTHER", "Other MSC Related Maintenance and Repair",
         0, 0, 575746, "L5650")
    _row("msc_total", "", "MSC Table IV FY26 Total (post-transfer to 1B4B)",
         None, None, f"={_FY26}{P['msc_mta']}+{_FY26}{P['msc_roh']}+{_FY26}{P['msc_other']}",
         "L5651", total=True)
    c.blank(2)

    # §2 - SCN CVN refueling overhauls (LI 2086)
    c.banner("§2 - SCN CVN refueling overhauls (LI 2086)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _header()
    _row("cvn74", "CVN74", "CVN 74 STENNIS RCOH", 530868, 1480314, 483100, "L6880")
    _row("cvn75", "CVN75", "CVN 75 TRUMAN RCOH", 0, 0, 1779011, "L6880")
    _row("li2086", "LI_2086", "LI 2086 Total CVN RCOH (both hulls)", None,
         f"={_FY25}{P['cvn74']}+{_FY25}{P['cvn75']}",
         f"={_FY26}{P['cvn74']}+{_FY26}{P['cvn75']}", "L6880", total=True)
    c.blank(2)

    # §3 - USCG maintenance
    c.banner("§3 - USCG maintenance", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _header()
    _row("isvs_total", "ISVS_TOTAL", "In-Service Vessel Sustainment (PPA total)",
         120000, 120000, 152000, "L128")
    _row("isvs_47mlb", "ISVS_47MLB", "47-Foot Motor Lifeboat SLEP", 43000, 43000, 45000,
         "L2378")
    _row("isvs_wmec", "ISVS_WMEC", "270-Foot Medium Endurance Cutter (WMEC) SLEP",
         46200, 46200, 76000, "L2420")
    _row("isvs_healy", "ISVS_HEALY", "CGC Healy SLEP", 13000, 13000, 11000, "L2420")
    _row("os_memo", "OS_SURFACE_AIR_SHORE", "Surface, Air, and Shore Operations (O&S, memo)",
         3125281, 3172908, 3425335, "L124")
    c.blank(2)

    # §4 - OPN LI 1000 ship maintenance (private contracted)
    c.banner("§4 - OPN LI 1000 ship maintenance (private contracted)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _header()
    _row("li1000", "LI1000", "Ship Maintenance, Repair and Modernization (private)",
         2839179, 2392190, 2392620, "L21287")

    # accessors (FY25 -> col E, FY26 -> col F)
    def _e(key): return f"'{_TAB}'!{_FY25}{P[key]}"
    def _f(key): return f"'{_TAB}'!{_FY26}{P[key]}"

    def msc_mr_fy25_transfer_cell(): return _e("msc_1b1b")
    def msc_mr_fy26_mta_cell(): return _f("msc_mta")
    def msc_mr_fy26_roh_cell(): return _f("msc_roh")
    def msc_mr_fy26_other_cell(): return _f("msc_other")
    def msc_mr_fy26_total_cell(): return _f("msc_total")

    def scn_cvn74_rcoh_cell(fy): return {2025: _e, 2026: _f}[fy]("cvn74")
    def scn_cvn75_rcoh_fy26_cell(): return _f("cvn75")

    def scn_cvn_rcoh_li2086_cell(fy):
        if fy not in (2025, 2026):
            raise ValueError(f"LI 2086 RCOH: fy must be 2025/2026, got {fy}")
        return (_e if fy == 2025 else _f)("li2086")

    def uscg_isvs_floor_cell(): return _e("isvs_total")
    def uscg_os_memo_fy25_cell(): return _e("os_memo")

    def opn_li1000_cell(fy):
        if fy not in (2025, 2026):
            raise ValueError(f"OPN LI 1000: fy must be 2025/2026, got {fy}")
        return (_e if fy == 2025 else _f)("li1000")

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    accessors = dict(
        msc_mr_fy25_transfer_cell=msc_mr_fy25_transfer_cell,
        msc_mr_fy26_mta_cell=msc_mr_fy26_mta_cell,
        msc_mr_fy26_roh_cell=msc_mr_fy26_roh_cell,
        msc_mr_fy26_other_cell=msc_mr_fy26_other_cell,
        msc_mr_fy26_total_cell=msc_mr_fy26_total_cell,
        scn_cvn74_rcoh_cell=scn_cvn74_rcoh_cell,
        scn_cvn75_rcoh_fy26_cell=scn_cvn75_rcoh_fy26_cell,
        scn_cvn_rcoh_li2086_cell=scn_cvn_rcoh_li2086_cell,
        uscg_isvs_floor_cell=uscg_isvs_floor_cell,
        uscg_os_memo_fy25_cell=uscg_os_memo_fy25_cell,
        opn_li1000_cell=opn_li1000_cell,
    )
    return SheetEntry(_TAB, _GROUP, render), accessors


MSC_SCN_USCG_TOPDOWN, _ACC = _make()

msc_mr_fy25_transfer_cell = _ACC["msc_mr_fy25_transfer_cell"]
msc_mr_fy26_mta_cell = _ACC["msc_mr_fy26_mta_cell"]
msc_mr_fy26_roh_cell = _ACC["msc_mr_fy26_roh_cell"]
msc_mr_fy26_other_cell = _ACC["msc_mr_fy26_other_cell"]
msc_mr_fy26_total_cell = _ACC["msc_mr_fy26_total_cell"]
scn_cvn74_rcoh_cell = _ACC["scn_cvn74_rcoh_cell"]
scn_cvn75_rcoh_fy26_cell = _ACC["scn_cvn75_rcoh_fy26_cell"]
scn_cvn_rcoh_li2086_cell = _ACC["scn_cvn_rcoh_li2086_cell"]
uscg_isvs_floor_cell = _ACC["uscg_isvs_floor_cell"]
uscg_os_memo_fy25_cell = _ACC["uscg_os_memo_fy25_cell"]
opn_li1000_cell = _ACC["opn_li1000_cell"]
