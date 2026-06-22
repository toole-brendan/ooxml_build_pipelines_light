"""model_market_size - the Gross Funded -> Addressable -> Serviceable -> Weighted bridge.

Turns the funded demand spine into a Saronic-addressable market, opportunity by opportunity,
as LIVE formulas:

  Gross Funded $M      = the FY27-31 forward spine of the opportunity's budget line
                         (live SUMIFS over Budget Facts: request_total + outyears, PB2027).
  Addressable $M       = Gross x Addressable %        (what the requirement can buy from us)
  Saronic-Serviceable  = Addressable x Saronic fit %  (what our portfolio actually serves)
  Weighted Pursuit $M  = Serviceable x timing x pursuit-access x win-prob   (risk-adjusted)

The Gross + all products are BLACK live formulas; the % / probability knobs are BLUE inputs
read from the DURABLE analyst/market_assumptions.csv (fractions 0-1) so editing one cell
re-sizes the market. The seeded assumptions are ILLUSTRATIVE (source=seed) - replace them in
the analyst pass. These measures are kept SEPARATE (never summed together) and are NOT to be
added to historical contract obligations (a different lens).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_NUM, S_PCT, S_LINK_PCT,
    S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_MARKET_SIZE
from workbook_army.sheets._analyst import load_analyst_table, value as a_value
from workbook_army.sheets.input_market_assumptions import market_assumptions_cols
from workbook_army.sheets.data_budget_facts import budget_facts_cols

_GROUP = "model"
_TAB = TAB_MARKET_SIZE
_VINTAGE = "2027"

# The relevance cluster (Mission/Platform/Autonomy fit + Saronic priority) ranks each
# opportunity on COMMERCIAL fit, not historical contract $ (review #6). The fits are blue
# analyst inputs (analyst/saronic_relevance.csv); Saronic priority is a live 0-1 composite
# (mean fit x timing x pursuit x win - the same product mechanics as Weighted pursuit) that
# the Timing & Incumbent Screen looks up per family via its attributed opportunity.
_HEADERS = ["Opportunity", "Segment", "Primary line", "Gross funded $M (FY27-31)",
            "Addressable %", "Addressable $M", "Saronic fit %", "Serviceable $M",
            "Timing conf", "Pursuit access", "Win prob", "Weighted pursuit $M",
            "Mission fit", "Platform fit", "Autonomy/C2 fit", "Saronic priority"]
_NCOLS = len(_HEADERS)
_COLS = [40, 26, 18, 16, 12, 14, 12, 14, 11, 13, 10, 16, 11, 11, 14, 13]
assert len(_COLS) == _NCOLS, (len(_COLS), _NCOLS)
_CENTER = {h for h in _HEADERS[3:]}
_CL = {h: col_letter(i + 1) for i, h in enumerate(_HEADERS)}


def _make_market_size():
    opps = load_analyst_table("opportunities", "opportunity_id")
    ma = load_analyst_table("market_assumptions", "opportunity_id")

    FL = budget_facts_cols("line_item_id")
    FB = budget_facts_cols("source_book_fy")
    FM = budget_facts_cols("measure")
    FR = budget_facts_cols("column_role")
    FA = budget_facts_cols("amount")

    def gross(line, measure):
        base = (f'SUMIFS({FA},{FL},"{line}",{FB},"{_VINTAGE}",{FM},"{measure}",'
                f'{FR},"request_total")')
        out = (f'SUMIFS({FA},{FL},"{line}",{FB},"{_VINTAGE}",{FM},"{measure}",'
               f'{FR},"outyear")')
        return f"={base}+{out}"

    GR, AP, AD = _CL["Gross funded $M (FY27-31)"], _CL["Addressable %"], _CL["Addressable $M"]
    FP, SV = _CL["Saronic fit %"], _CL["Serviceable $M"]
    TC, PA, WP, WT = (_CL["Timing conf"], _CL["Pursuit access"], _CL["Win prob"],
                      _CL["Weighted pursuit $M"])
    MF, PF, AF = _CL["Mission fit"], _CL["Platform fit"], _CL["Autonomy/C2 fit"]
    addr_f = lambda r: f"={GR}{r}*{AP}{r}"
    serv_f = lambda r: f"={AD}{r}*{FP}{r}"
    wt_f = lambda r: f"={SV}{r}*{TC}{r}*{PA}{r}*{WP}{r}"
    # Saronic priority: 0-1 commercial-relevance index = mean(mission, platform, autonomy
    # fit) x timing x pursuit x win - the same product chain as Weighted pursuit, but on the
    # fit knobs instead of $. The Timing Screen looks this up per family by opportunity.
    prio_f = lambda r: (f"=AVERAGE({MF}{r},{PF}{r},{AF}{r})*{TC}{r}*{PA}{r}*{WP}{r}")

    # The eight % / fit knobs are GREEN cross-sheet links into the Market Assumptions input
    # tab (INDEX/MATCH on the opportunity name): the editable cells live there, so this MODEL
    # sheet carries no blue inputs. $ products are black live formulas; Saronic priority is a
    # live composite (S_PCT).
    OPP = _CL["Opportunity"]
    MA_OPP = market_assumptions_cols("opportunity")

    def knob(col):
        rng = market_assumptions_cols(col)
        return lambda r: f'=IFERROR(INDEX({rng},MATCH(${OPP}{r},{MA_OPP},0)),"")'

    k_addr, k_fit = knob("addressable_pct"), knob("saronic_fit_pct")
    k_tc, k_pa, k_wp = knob("timing_conf"), knob("pursuit_access"), knob("win_prob")
    k_mf, k_pf, k_af = knob("mission_fit"), knob("platform_fit"), knob("autonomy_c2_fit")

    styles = [S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM, S_LINK_PCT, S_NUM, S_LINK_PCT,
              S_NUM, S_LINK_PCT, S_LINK_PCT, S_LINK_PCT, S_NUM,
              S_LINK_PCT, S_LINK_PCT, S_LINK_PCT, S_PCT]
    assert len(styles) == _NCOLS, (len(styles), _NCOLS)

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["FY27-31 funded demand x addressability x Saronic fit x timing x access x win, "
             "per opportunity. Knobs on Market Assumptions."],
            styles=[S_ITALIC])
    c.blank(2)

    c.banner("§1 - Market-size bridge (per opportunity)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    first = hdr + 1
    for oid, mrow in ma.items():
        line = (mrow.get("primary_line_item") or "").strip()
        measure = (mrow.get("measure") or "").strip()
        name = a_value(opps, oid, "name") or oid
        seg = a_value(opps, oid, "customer_segment") or ""
        c.write([name, seg, line, gross(line, measure),
                 k_addr, addr_f, k_fit, serv_f,
                 k_tc, k_pa, k_wp, wt_f,
                 k_mf, k_pf, k_af, prio_f],
                styles=styles, outline_level=1)
    last = hdr + len(ma)

    def cols(header: str) -> str:
        col = col_letter(_HEADERS.index(header) + 1)   # +1 for the gutter (A)
        return f"'{_TAB}'!${col}${first}:${col}${last}"

    total_vals = [None] * _NCOLS
    total_vals[0] = f"TOTAL - {len(ma)} opportunities"
    for h in ("Gross funded $M (FY27-31)", "Addressable $M", "Serviceable $M",
              "Weighted pursuit $M"):
        cl = _CL[h]
        total_vals[_HEADERS.index(h)] = f"=SUM({cl}{first}:{cl}{last})"
    total_sty = [S_DEFAULT] * _NCOLS
    total_sty[0] = S_BOLD
    for h in ("Gross funded $M (FY27-31)", "Addressable $M", "Serviceable $M",
              "Weighted pursuit $M"):
        total_sty[_HEADERS.index(h)] = S_NUM
    tr = c.total(total_vals, styles=total_sty, n_cols=_NCOLS)
    refs = {k: f"'{_TAB}'!${_CL[h]}${tr}" for k, h in (
        ("gross", "Gross funded $M (FY27-31)"), ("addressable", "Addressable $M"),
        ("serviceable", "Serviceable $M"), ("weighted", "Weighted pursuit $M"))}

    c.blank(2)
    c.banner("§2 - Method & caveats", n_cols=_NCOLS, style=S_TITLE_SECTION)
    c.blank()
    for _line in [
        "Bridge: Gross funded -> Addressable -> Serviceable (SAM) -> Weighted pursuit (SOM).",
        "Gross funded = FY27-31 forward spine - the same numbers as Budget Market.",
        "Knobs live on Market Assumptions; seed illustrations until sourced, not validated.",
        "A separate lens from historical obligations - never summed with them.",
    ]:
        c.write([_line], styles=[S_DEFAULT])

    def render() -> WorksheetSpec:
        # Styled range (not a native table): the three principal rows + total are a fixed
        # bridge, not a filterable list; the header underline + total border carry the look.
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render), refs, cols


MARKET_SIZE, TOTAL_REFS, market_size_cols = _make_market_size()
