"""model_recompete_radar - the Army watercraft recompete radar (live-formula screen).

One row per watercraft contract FAMILY (vehicle): task orders collapse into their
parent IDV (family key = parent_idv_piid, else the standalone piid). The analytic
columns are LIVE Excel formulas (SUMIFS / COUNTIFS / MAXIFS / date math) keyed on the
data-leaf sheets via their cols() accessors and on an editable As-of date cell - so
the obligation roll-ups recompute as the leaves change and the whole expiry clock
re-clocks when you edit one cell.

Methodology is the army's own contracts handoff spec (NOT the shipbuilding cadence
model): a recompete WINDOW (not a single date), the parent-vehicle expiry tracked
distinctly from the latest task-order end, and the soft judgment - recompete window
override, a Confirmed/Strong/Inferred/Speculative confidence, a SEPARATE pursuit-access
rating - left BLANK for the analyst, alongside the program / capability_node bridges.

Scope (build-time, deterministic + documented):
  - Watercraft-relevant: a family qualifies if ANY of its awards matches PSC 1905 /
    1915 / 1925 / 1930 / 1935 / 1940 / 1945 / 1990 / 2090, NAICS 336611 / 336612, a
    ship/boat/vessel/dredge/barge descriptor, or a known watercraft prime. NOTE: the
    discovery universe was already NAICS/PSC-scoped to watercraft, so this flag is
    near-saturating (it only drops a handful of off-scope families).
  - Materiality floor: only families with >= $MIN_OBLIG lifetime obligations are
    shown - the real focusing lever, since the median family is a ~$65k micro-buy.
    Lower MIN_OBLIG to widen the radar; everything still lives on Contract Awards.

Built at import via _make_radar() into a standalone single-table screen.
"""
from __future__ import annotations

from collections import defaultdict

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DATE, S_DATE_INPUT, S_DEFAULT, S_INT, S_NUM,
    S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._cuts import load_table, date_serial
from workbook_army.sheets._text_input import S_TEXT_INPUT
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_RECOMPETE_RADAR
from workbook_army.sheets.data_contract_awards import awards_cols
from workbook_army.sheets.data_award_actions import actions_cols
from workbook_army.sheets.data_pipeline_events import pipeline_cols

_GROUP = "model"
_TAB = TAB_RECOMPETE_RADAR
_AS_OF = "2026-06-20"            # default as-of; editable in-sheet (re-clocks all math)
_MIN_OBLIG = 1_000_000.0        # materiality floor (lifetime obligations per family)

# Deterministic watercraft-relevance rule (documented in the docstring + caption).
_WC_PSC = {"1905", "1915", "1925", "1930", "1935", "1940", "1945", "1990", "2090"}
_WC_NAICS = {"336611", "336612"}
_WC_PRIMES = ["VIGOR", "BIRDON", "BAY SHIP", "COLONNA", "CONRAD",
              "EASTERN SHIPBUILDING", "THOMA-SEA", "METAL TRADES"]
_WC_DESC = ["SHIP BUILD", "SHIP REPAIR", "BOAT", "VESSEL", "WATERCRAFT", "DREDG",
            "BARGE", "LANDING CRAFT", "TUG", "PONTOON", "LIGHTER", "MARINE"]

_HEADERS = [
    "Family (vehicle PIID)", "Incumbent", "Relevance basis", "PSC", "NAICS",
    "Last competition", "Vehicle type", "Task orders", "Obligated $M", "Actions",
    "Current end", "Potential end", "Parent/vehicle end", "Months to current end",
    "Option headroom (mo)", "Recompete window", "In-market notice",
    "Window (analyst)", "Confidence", "Pursuit access", "program", "capability_node",
    "Notes",
]
_NCOLS = len(_HEADERS)
_COLS = [22, 34, 20, 8, 11, 26, 14, 11, 12, 10, 14, 14, 14, 12, 12, 16, 12,
         16, 14, 14, 14, 16, 30]
assert len(_COLS) == _NCOLS, (len(_COLS), _NCOLS)
_CENTER = {"Task orders", "Obligated $M", "Actions", "Current end", "Potential end",
           "Parent/vehicle end", "Months to current end", "Option headroom (mo)"}
# within-row column letters (gutter mode: header i -> col_letter(i+1))
_CL = {h: col_letter(i + 1) for i, h in enumerate(_HEADERS)}


def _wc_reason(g, row):
    """Short relevance basis for an award, or None if not watercraft-relevant."""
    psc = (g(row, "psc_code") or "").strip()
    naics = (g(row, "naics_code") or "").strip()
    name = (g(row, "recipient_name") or "").upper()
    nd = (g(row, "naics_description") or "").upper()
    pd = (g(row, "psc_description") or "").upper()
    if psc in _WC_PSC:
        return f"PSC {psc}"
    if naics in _WC_NAICS:
        return f"NAICS {naics}"
    for p in _WC_PRIMES:
        if p in name:
            return f"prime: {p.title()}"
    for t in _WC_DESC:
        if t in nd or t in pd:
            return f"desc: {t.lower()}"
    return None


def _make_radar():
    headers, rows = load_table("contract_awards")
    ix = {h: i for i, h in enumerate(headers)}
    def g(row, c):
        j = ix[c]
        return row[j] if j < len(row) else ""
    def oblig(row):
        v = (g(row, "obligation_amount") or "").strip()
        return float(v) if v else 0.0

    fams = defaultdict(list)
    for row in rows:
        piid = g(row, "piid")
        key = g(row, "parent_idv_piid") or piid
        if key:
            fams[key].append(row)

    # select watercraft-relevant families above the materiality floor; sort by $ desc
    selected = []
    for key, frows in fams.items():
        reason = next((r for r in (_wc_reason(g, x)
                       for x in sorted(frows, key=oblig, reverse=True)) if r), None)
        if reason is None:
            continue
        total = sum(oblig(x) for x in frows)
        if total < _MIN_OBLIG:
            continue
        dom = max(frows, key=oblig)
        selected.append({
            "key": key, "total": total, "reason": reason,
            "incumbent": g(dom, "recipient_name"),
            "psc": g(dom, "psc_code"), "naics": g(dom, "naics_code"),
            "comp": g(dom, "extent_competed_description") or g(dom, "extent_competed"),
        })
    selected.sort(key=lambda d: -d["total"])

    # ---- leaf ranges (live-formula keys) ----
    AMT = actions_cols("amount")
    A_PIID = actions_cols("piid")
    A_PARENT = actions_cols("parent_idv_piid")
    AW_PIID = awards_cols("piid")
    AW_PARENT = awards_cols("parent_idv_piid")
    AW_CUR = awards_cols("pop_current_end_date")
    AW_POT = awards_cols("pop_potential_end_date")
    PL_AWARDNO = pipeline_cols("award_number")

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Army watercraft contract families coming up for re-award - a live screen "
             "over the Contract Awards / Award Actions / Pipeline Events leaves. "
             "Window (analyst), Confidence, Pursuit access and the program / "
             "capability_node bridges are ANALYST inputs, left blank."],
            styles=[S_ITALIC])
    c.blank(2)
    asof_row = c.write(["As-of date", date_serial(_AS_OF),
                        "(edit to re-clock every expiry column)"],
                       styles=[S_BOLD, S_DATE_INPUT, S_ITALIC])
    ASOF = f"'{_TAB}'!$C${asof_row}"
    c.blank(2)

    FB, CE, PE, MO = (_CL["Family (vehicle PIID)"], _CL["Current end"],
                      _CL["Potential end"], _CL["Months to current end"])
    fam = lambda r: f"${FB}{r}"

    def eff_end(rng):
        def f(r):
            m = (f"MAX(_xlfn.MAXIFS({rng},{AW_PIID},{fam(r)}),"
                 f"_xlfn.MAXIFS({rng},{AW_PARENT},{fam(r)}))")
            return f'=IF({m}=0,"",{m})'
        return f
    cur_end_f, pot_end_f = eff_end(AW_CUR), eff_end(AW_POT)
    def parent_end_f(r):
        m = f"_xlfn.MAXIFS({AW_CUR},{AW_PIID},{fam(r)})"
        return f'=IF({m}=0,"",{m})'

    vtype_f = lambda r: f'=IF(COUNTIFS({AW_PARENT},{fam(r)})>0,"IDV vehicle","Standalone")'
    tos_f = lambda r: f'=COUNTIFS({AW_PARENT},{fam(r)})'
    obl_f = lambda r: (f'=(SUMIFS({AMT},{A_PARENT},{fam(r)})'
                       f'+SUMIFS({AMT},{A_PIID},{fam(r)}))/1000000')
    acts_f = lambda r: f'=COUNTIFS({A_PARENT},{fam(r)})+COUNTIFS({A_PIID},{fam(r)})'
    months_f = lambda r: f'=IF(${CE}{r}="","",ROUND((${CE}{r}-{ASOF})/30.44,0))'
    head_f = lambda r: (f'=IF(OR(${CE}{r}="",${PE}{r}=""),"",'
                        f'ROUND((${PE}{r}-${CE}{r})/30.44,0))')
    window_f = lambda r: (
        f'=IF(${CE}{r}="","n/a",IF(${CE}{r}<{ASOF},"Expired",'
        f'IF(${MO}{r}<=12,"0-12 mo",IF(${MO}{r}<=24,"12-24 mo",'
        f'IF(${MO}{r}<=36,"24-36 mo","36+ mo")))))')
    inmkt_f = lambda r: f'=IF(COUNTIFS({PL_AWARDNO},{fam(r)})>0,"Y","")'

    c.banner("§1 - Watercraft recompete radar", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    f = hdr + 1
    styles = ([S_DEFAULT] * 7 + [S_INT, S_NUM, S_INT] + [S_DATE] * 3
              + [S_INT, S_INT] + [S_DEFAULT, S_DEFAULT] + [S_TEXT_INPUT] * 6)
    for d in selected:
        c.write([d["key"], d["incumbent"], d["reason"], d["psc"], d["naics"],
                 d["comp"], vtype_f, tos_f, obl_f, acts_f,
                 cur_end_f, pot_end_f, parent_end_f, months_f, head_f,
                 window_f, inmkt_f, None, None, None, None, None, None],
                styles=styles, outline_level=1)
    last = hdr + len(selected)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"

    J = _CL["Obligated $M"]
    total_vals = [None] * _NCOLS
    total_vals[0] = f"Total - {len(selected)} vehicles"
    total_vals[_HEADERS.index("Obligated $M")] = f"=SUBTOTAL(109,{J}{f}:{J}{last})"
    total_sty = [S_DEFAULT] * _NCOLS
    total_sty[0] = S_BOLD
    total_sty[_HEADERS.index("Obligated $M")] = S_NUM
    c.total(total_vals, styles=total_sty, n_cols=_NCOLS)

    c.blank(2)
    c.write(["Recompete window keys off the family's latest current PoP end vs the "
             "As-of date; Option headroom = months from current to potential (option) "
             "end. Parent/vehicle end is the IDV ordering-period (or standalone) "
             "expiry, tracked distinctly from the task-order ends folded into Current "
             "end. Scope: watercraft-relevant families (PSC 19xx / NAICS 33661x / "
             "vessel-dredge descriptors / known primes) with >= $1.0M lifetime "
             "obligations. In-market notice = a Pipeline Events notice references this "
             "vehicle (sparse until Stage 5 runs full)."],
            styles=[S_DEFAULT])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="RecompeteRadar", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render)


RECOMPETE_RADAR = _make_radar()
