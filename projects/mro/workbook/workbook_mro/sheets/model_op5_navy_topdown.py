"""OP-5 Navy Top-Down - 1B4B Ship Maintenance by availability category.

Private (contract-executable) availability categories + public naval shipyards, from the
Navy OP-5 exhibit (OMN_Book). Exposes the 18 OP5_* anchors (all in the FY25-Current
column G) as closure accessors. Per-row line refs are TEXT (Source column).

The §3 cross-check `OP-5 grand total - OMN 1B4B total` reads the Reconciliation 1B4B
anchor through its `omn_cell('1B4B_TOTAL')` accessor (a one-directional import; no cycle).
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
# §3 cross-check reads the Reconciliation 1B4B anchor via its accessor (no defined
# names). One-directional import (Reconciliation never imports OP-5), so no cycle.
from workbook_mro.sheets.model_reconciliation import omn_cell

_GROUP = "model"
_TAB = "OP-5 Navy Top-Down"
_NCOLS = 8                      # B..I: Code, Category, Side, FY24 PB, FY24 Act, FY25 Cur, FY26 PB, Source
_FY25 = "G"                     # FY25 Current $K column (the named column)
_COLS = [10, 46, 12, 12, 12, 12, 12, 12]
_HEADERS = ["Code", "Availability Category", "Side", "FY24 PB $K", "FY24 Actual $K",
            "FY25 Current $K", "FY26 PB $K", "Source"]

# (code, category, fy24_pb, fy24_actual, fy25_current, fy26_pb, source_line)
_PRIVATE = [
    ("OH", "Overhauls", 329274, 348149, 250497, 250312, "L5600"),
    ("SRA", "Selected Restricted Availability", 717140, 558575, 384455, 305424, "L5601"),
    ("SIA", "Surface Incremental Availability", 95837, 89442, 63660, 104367, "L5602"),
    ("PIA", "Planned Incremental Availability", 99893, 70962, 322052, 349822, "L5603"),
    ("PMA", "Planned Maintenance Availability", 0, 0, 0, 0, "L5604"),
    ("CIA", "Carrier Incremental Availability", 28204, 9000, 16251, 44947, "L5605"),
    ("SCO", "Service Craft Overhauls", 21554, 16873, 22924, 0, "L5606"),
    ("ERATA", "Emergent Repair", 118950, 238559, 136225, 139467, "L5607"),
    ("ORATA", "Miscellaneous RA/TA", 973522, 902149, 990461, 1070896, "L5608"),
    ("CM", "Continuous Maintenance (CMAV)", 696548, 792788, 662899, 650869, "L5609"),
    ("IL", "Non-depot / Intermediate Maintenance", 1497600, 1517398, 1429333, 1525270, "L5610"),
]
_PUBLIC = [
    ("NNSY", "Norfolk Naval Shipyard", 1635116, 1702115, 1789606, 1775132, "L5614"),
    ("PNSY", "Portsmouth Naval Shipyard", 1191581, 1317076, 1468055, 1401503, "L5615"),
    ("PSNSY", "Puget Sound Naval Shipyard", 2521756, 2544027, 2741203, 2944801, "L5616"),
    ("PHNSY", "Pearl Harbor Naval Shipyard", 1237273, 1394013, 1485973, 1656378, "L5617"),
]


def _make():
    P: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    def _header():
        c.write(_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_LEFT] +
                [S_HEADER_CENTER] * 4 + [S_HEADER_LEFT])

    def _datarow(code, name, side, pb, act, cur, fy26, src):
        r = c.write([code, name, side, pb, act, cur, fy26, src],
                    styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_NUM_INPUT,
                            S_NUM_INPUT, S_NUM_INPUT, S_DEFAULT], outline_level=1)
        P[code] = r
        return r

    # §1 Private (contract-executable) availability categories
    c.banner("§1 - Private availability categories", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _header()
    for code, name, pb, act, cur, fy26, src in _PRIVATE:
        _datarow(code, name, "private", pb, act, cur, fy26, src)
    P["priv_sub"] = c.total(
        ["", "Private subtotal (FY25 Current)", "", None, None,
         f"=SUM({_FY25}{P['OH']}:{_FY25}{P['IL']})", None, ""],
        styles=[S_BOLD, S_BOLD, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_NUM, S_DEFAULT],
        n_cols=_NCOLS, outline_level=1)
    c.blank(2)

    # §2 Public naval shipyards (federal civilian workforce)
    c.banner("§2 - Public naval shipyards", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _header()
    for code, name, pb, act, cur, fy26, src in _PUBLIC:
        _datarow(code, name, "public_nsy", pb, act, cur, fy26, src)
    P["pub_sub"] = c.total(
        ["", "Public NSY subtotal (FY25 Current)", "", None, None,
         f"=SUM({_FY25}{P['NNSY']}:{_FY25}{P['PHNSY']})", None, ""],
        styles=[S_BOLD, S_BOLD, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_NUM, S_DEFAULT],
        n_cols=_NCOLS, outline_level=1)
    c.blank(2)

    # §3 Grand total & cross-checks
    c.banner("§3 - Grand total & cross-checks", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    P["grand"] = c.total(
        ["", "OP-5 Grand Total FY25 Current ($K)", "", None, None,
         f"={_FY25}{P['priv_sub']}+{_FY25}{P['pub_sub']}", None, ""],
        styles=[S_BOLD, S_BOLD, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_NUM, S_DEFAULT],
        n_cols=_NCOLS, outline_level=1)
    P["src_total"] = c.write(
        ["", "Source TOTAL row (OMN_Book.txt line 5618)", "", None, None, 11763594, None, "L5618"],
        styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_NUM_INPUT, S_NUM_INPUT,
                S_NUM_INPUT, S_DEFAULT], outline_level=1)
    c.write(["", "Delta vs source TOTAL (must be 0)", "", None, None,
             f"={_FY25}{P['grand']}-{_FY25}{P['src_total']}", None, ""],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_NUM, S_DEFAULT],
            outline_level=1)
    c.write(["", "Delta vs OMN 1B4B total (must be 0)", "", None, None,
             f"={_FY25}{P['grand']}-{omn_cell('1B4B_TOTAL')}", None, ""],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_NUM, S_DEFAULT],
            outline_level=1)

    # accessors (FY25 Current -> col G)
    def _g(key): return f"'{_TAB}'!{_FY25}{P[key]}"

    def op5_cell(code):
        if code not in P:
            raise ValueError(f"OP-5: unknown code {code!r}")
        return _g(code)

    def op5_private_cell(): return _g("priv_sub")
    def op5_public_nsy_cell(): return _g("pub_sub")
    def op5_total_cell(): return _g("grand")

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    accessors = dict(op5_cell=op5_cell, op5_private_cell=op5_private_cell,
                     op5_public_nsy_cell=op5_public_nsy_cell, op5_total_cell=op5_total_cell)
    return SheetEntry(_TAB, _GROUP, render), accessors


OP5_NAVY_TOPDOWN, _ACC = _make()

op5_cell = _ACC["op5_cell"]
op5_private_cell = _ACC["op5_private_cell"]
op5_public_nsy_cell = _ACC["op5_public_nsy_cell"]
op5_total_cell = _ACC["op5_total_cell"]
