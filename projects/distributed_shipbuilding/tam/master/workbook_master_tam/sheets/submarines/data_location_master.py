"""data_location_master - the "Location Master" tab (one module = one sheet).

Subaward geography: top states (native table), country distribution, and the
prime-controlled-state flags. Geography is a HINT only - the award-action scope
controls the TAM treatment, not where the $ lands. Prime-controlled states (where a
final-assembly yard or major prime site sits): CT/RI = Electric Boat
(Groton/Quonset); VA = HII-Newport News; MS = HII-Ingalls. Subaward $ landing in a
prime-controlled state is distributed-view, not necessarily addressable. Leaf module
(loads its own CSVs, no cross-sheet dependency).
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, build_table, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_NUM, S_NUM_INPUT, S_PCT_INPUT, S_HEADER_LEFT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._bind import EXTRACTED
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "data"
_TAB = "Sub Location Master"
_PRIME_STATES = {"CT": "EB (Groton)", "RI": "EB (Quonset)",
                 "VA": "HII-NNS (Newport News)", "MS": "HII-Ingalls"}
_N_STATES = 15
_BASE = 13                                       # title(2) + blank + §1 at-a-glance(4-10) + 2 blanks


def _f(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def _load_states():
    out = []
    with (EXTRACTED / "nc_geo_by_state.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            out.append({"state": (r.get("state") or "").strip(), "name": (r.get("state_name") or "").strip(),
                        "amt": _f(r.get("amount_M")), "pct": _f(r.get("pct_of_us_total"))})
    out.sort(key=lambda r: r["amt"], reverse=True)
    return out


def _load_countries():
    out = []
    with (EXTRACTED / "nc_geo_by_country.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            out.append({"code": (r.get("country_code") or "").strip(), "name": (r.get("country") or "").strip(),
                        "amt": _f(r.get("amount_M")), "pct": _f(r.get("pct_of_total"))})
    out.sort(key=lambda r: r["amt"], reverse=True)
    return out


_STATES_ALL = _load_states()
_COUNTRIES = _load_countries()
_STATES = _STATES_ALL[:_N_STATES]


def _build_location_master(tab: str, base: int):
    _STATE_HEADERS = ["State", "Name", "$M", "% of US", "Prime-controlled site"]
    c = RowCursor(base)

    # §2 Top states (native table)
    c.banner(f"§2 - Top {_N_STATES} states by subaward $ ($M lifetime)", n_cols=5,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    state_header_row = c.at()
    state_rows = [[s["state"], s["name"], s["amt"], s["pct"], _PRIME_STATES.get(s["state"], "")]
                  for s in _STATES]
    blk, nr = build_table(state_header_row, headers=_STATE_HEADERS, data_rows=state_rows,
                          header_style=S_HEADER_LEFT,
                          col_styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_PCT_INPUT, S_DEFAULT],
                          start_col=1, outline_level=1)
    c.feed(blk, nr)
    state_last = nr - 1
    c.blank(2)

    # §3 Country distribution
    c.banner("§3 - Country distribution (foreign / FMS is excluded scope)", n_cols=5,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    ctry_rows = [[c2["code"], c2["name"], c2["amt"], c2["pct"]] for c2 in _COUNTRIES]
    blk2, nr2 = build_table(c.at(), headers=["Code", "Country", "$M", "% of total"],
                            data_rows=ctry_rows, header_style=S_HEADER_LEFT,
                            col_styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_PCT_INPUT],
                            start_col=1, outline_level=1)
    c.feed(blk2, nr2)
    c.blank(2)

    # §4 Prime-controlled state flags
    c.banner("§4 - Prime-controlled state flags", n_cols=5,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["State", "Site"], styles=S_HEADER_LEFT)
    for st, site in _PRIME_STATES.items():
        c.write([st, site], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    table = ExcelTable(name="tbl_sub_location_states",
                       ref=f"B{state_header_row}:{col_letter(len(_STATE_HEADERS))}{state_last}",
                       headers=_STATE_HEADERS)
    return c.rows, c.at(), [table]


# ── Layout pass ──────────────────────────────────────────────────────────────
_rows, _after, _tables = _build_location_master(_TAB, _BASE)

_US_TOTAL = sum(s["amt"] for s in _STATES_ALL)
_FOREIGN_TOTAL = sum(c["amt"] for c in _COUNTRIES if c["code"].upper() not in {"US", "USA"})
_TOP_STATE = _STATES_ALL[0] if _STATES_ALL else {"name": "-", "amt": 0.0}
_PRIME_TOTAL = sum(s["amt"] for s in _STATES_ALL if s["state"] in _PRIME_STATES)


def _render_location_master() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner("Location Master", n_cols=5, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Subaward geography (hint only)", n_cols=5, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=S_HEADER_LEFT)
    c.write(["US subaward $M", _US_TOTAL],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Foreign subaward $M", _FOREIGN_TOTAL],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Top state by $M", _TOP_STATE["name"]],
            styles=[S_DEFAULT, S_DEFAULT])
    c.write(["Prime-controlled-state $M", _PRIME_TOTAL],
            styles=[S_DEFAULT, S_NUM])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)

    ws = worksheet(c.rows, cols=[34, 30, 12, 12, 26],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, tables=_tables)


LOCATION_MASTER = SheetEntry(_TAB, _GROUP, _render_location_master)
