"""model_recompete_calendar - the forward, date-ordered recompete calendar (live).

A focused projection of the Recompete Radar that foregrounds the LIVE targets: one row
per actionable vehicle (a lineage chain TAIL - superseded vehicles are folded out),
ordered FORWARD-by-decision-FY then an OVERDUE section. Where the radar is the full
$-ranked inventory, this is the "what's coming up and when" calendar.

Provenance contract (same as the radar): every displayed number is either a LIVE
in-sheet formula (BLACK) or an honest hardcoded input (BLUE) - none are baked-in-Python
values masquerading as derived. The family roll-ups (Decision date, Potential end,
Obligated $M) are the SAME live formulas the radar uses, imported from
_radar_formulas.family_formulas, so the two sheets can never disagree. Decision FY,
Notice-by, Months to decision, Tenure and Option yrs left are in-sheet date math, and
Open notice (PSC) is a live COUNTIFS over Pipeline Events - all re-clock off the single
Recompete Radar As-of cell (_tabs.AS_OF_CELL).

Decision date = the family's latest current-PoP end (the forced exercise/recompete
point); Notice-by = decision - 90 days (a planning lead estimate, NOT a contract term).
The one value a formula cannot reach is incumbent tenure across the PREDECESSOR chain:
the chain walk is multi-hop, so its root start date is surfaced as a BLUE input
("Incumbent since") and Tenure = (As-of - Incumbent since) stays a black formula. Row
ORDER (forward-by-decision then overdue) and the forward/overdue split are legitimate
build-time concerns; only the rendered cells are formulas. Built via _make_calendar().
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DATE, S_DATE_INPUT, S_DEFAULT, S_INT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._cuts import date_serial
from workbook_army.sheets._text_input import S_TEXT_INPUT
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_RECOMPETE_CALENDAR, AS_OF_CELL
from workbook_army.sheets._radar_formulas import family_formulas
from workbook_army.sheets.data_pipeline_events import pipeline_cols
from workbook_army.sheets.model_recompete_radar import (
    load_families, _MIN_OBLIG, _AS_OF,
)

_GROUP = "model"
_TAB = TAB_RECOMPETE_CALENDAR
_NOTICE_LEAD_DAYS = 90          # planning lead: notice-by = decision - this (days)

_HEADERS = [
    "Decision FY", "Phase", "Decision date", "Notice-by (est)",
    "Months to decision", "Family (vehicle PIID)", "Incumbent", "Incumbent since",
    "Tenure (yrs)", "PSC", "Obligated $M", "Potential end",
    "Option yrs left", "Open notice (PSC)", "Confidence", "Pursuit access", "Notes",
]
_NCOLS = len(_HEADERS)
_COLS = [9, 10, 13, 13, 13, 22, 34, 13, 10, 8, 12, 13, 12, 14, 14, 14, 28]
assert len(_COLS) == _NCOLS, (len(_COLS), _NCOLS)
_CENTER = {"Months to decision", "Tenure (yrs)", "Obligated $M", "Potential end",
           "Option yrs left"}
_CL = {h: col_letter(i + 1) for i, h in enumerate(_HEADERS)}


def _make_calendar():
    attrs, pred_of, succ_of = load_families()
    asof_ser = date_serial(_AS_OF)          # build-time only: the forward/overdue split

    def root_start(key):
        """Chain-root start serial: walk the predecessor lineage back to its root.

        Surfaced as a BLUE input ("Incumbent since") because the multi-hop walk is not
        expressible as a single Excel formula; Tenure then derives from it live.
        """
        cur = key
        while cur in pred_of:
            cur = pred_of[cur]
        return attrs[cur]["start"]           # serial, or None if the root has no start

    # actionable = chain tails (exclude superseded) above the floor, with a decision date.
    # Sort + split are build-time (legitimate); the rendered cells below are all formulas.
    tails = [a for a in attrs.values()
             if a["total"] >= _MIN_OBLIG and a["key"] not in succ_of
             and a["end"] is not None]
    forward = sorted((a for a in tails if a["end"] >= asof_ser), key=lambda a: a["end"])
    overdue = sorted((a for a in tails if a["end"] < asof_ser),
                     key=lambda a: a["end"], reverse=True)
    ordered = [("Forward", a) for a in forward] + [("Overdue", a) for a in overdue]

    # ---- live formulas (black) ----
    fam = lambda r: f"${_CL['Family (vehicle PIID)']}{r}"
    F = family_formulas(fam, AS_OF_CELL)            # shared roll-ups (same as the radar)
    decision_f, potend_f, obl_f = F["cur_end"], F["pot_end"], F["obl"]

    DD, IS = _CL["Decision date"], _CL["Incumbent since"]
    PE, PSCc = _CL["Potential end"], _CL["PSC"]
    PL_PSC, PL_DEADLINE = pipeline_cols("psc_code"), pipeline_cols("response_deadline")

    # Decision FY = DoD fiscal year of the (live) decision date; FY rolls Oct 1.
    fy_f = lambda r: (
        f'=IF(${DD}{r}="","","FY"&TEXT(MOD(IF(MONTH(${DD}{r})>=10,'
        f'YEAR(${DD}{r})+1,YEAR(${DD}{r})),100),"00"))')
    notice_f = lambda r: f'=IF(${DD}{r}="","",${DD}{r}-{_NOTICE_LEAD_DAYS})'
    months_f = lambda r: f'=IF(${DD}{r}="","",ROUND((${DD}{r}-{AS_OF_CELL})/30.44,0))'
    tenure_f = lambda r: (f'=IF(${IS}{r}="","",'
                          f'ROUND(({AS_OF_CELL}-${IS}{r})/365.25,1))')
    # Option years remaining = (potential - current end) / 365, floored at 0; no
    # potential-end data (blank) -> 0, matching the radar's option-headroom convention.
    optyrs_f = lambda r: (f'=IF(OR(${PE}{r}="",${DD}{r}=""),0,'
                          f'MAX(0,ROUND((${PE}{r}-${DD}{r})/365,0)))')
    # Open notice (PSC) = count of OPEN Pipeline Events notices (deadline >= As-of) that
    # share this vehicle's PSC - a weak same-product signal, rendered "Y (n)" / "".
    notice_psc_f = lambda r: (
        f'=IF(${PSCc}{r}="","",'
        f'IF(COUNTIFS({PL_PSC},${PSCc}{r},{PL_DEADLINE},">="&{AS_OF_CELL})>0,'
        f'"Y ("&COUNTIFS({PL_PSC},${PSCc}{r},{PL_DEADLINE},">="&{AS_OF_CELL})&")",""))')

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Forward recompete calendar - actionable watercraft vehicles (lineage chain "
             "tails) ordered by decision FY then an Overdue section. Every number is a "
             "LIVE formula over the data leaves or an honest blue input; Decision date = "
             "the vehicle's latest current-PoP end, Notice-by = decision - 90d (planning "
             "estimate), and the expiry / tenure clock re-clocks off the Recompete Radar "
             "As-of date. Confidence / Pursuit access / Notes are ANALYST inputs, blank."],
            styles=[S_ITALIC])
    c.blank(2)

    c.banner("§1 - Recompete calendar (forward, then overdue)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    styles = [S_DEFAULT,        # Decision FY        - derived FY text (off decision date)
              S_DEFAULT,        # Phase              - build-time section label (Forward/Overdue)
              S_DATE,           # Decision date      - MAXIFS current PoP end
              S_DATE,           # Notice-by (est)    - decision - 90d
              S_INT,            # Months to decision - live vs As-of
              S_DEFAULT,        # Family (PIID)      - family key (text)
              S_DEFAULT,        # Incumbent          - text
              S_DATE_INPUT,     # Incumbent since    - BLUE chain-root start input
              S_NUM,            # Tenure (yrs)       - (As-of - Incumbent since)/365.25
              S_DEFAULT,        # PSC                - text
              S_NUM,            # Obligated $M       - SUMIFS over Award Actions
              S_DATE,           # Potential end      - MAXIFS potential PoP end
              S_INT,            # Option yrs left    - (potential - current)/365
              S_DEFAULT,        # Open notice (PSC)  - COUNTIFS over Pipeline Events
              S_TEXT_INPUT, S_TEXT_INPUT, S_TEXT_INPUT]   # analyst inputs (blank)
    assert len(styles) == _NCOLS, (len(styles), _NCOLS)

    for phase, a in ordered:
        c.write([fy_f, phase, decision_f, notice_f, months_f,
                 a["key"], a["incumbent"], root_start(a["key"]), tenure_f, a["psc"],
                 obl_f, potend_f, optyrs_f, notice_psc_f, None, None, None],
                styles=styles, outline_level=1)
    last = hdr + len(ordered)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"

    c.blank(2)
    c.write([f"{len(forward)} forward vehicles (decision date >= As-of) + {len(overdue)} "
             "overdue (expired, no detected successor - validate before treating as a live "
             "recompete). Provenance: Decision date / Potential end = MAXIFS of the "
             "family's current / potential PoP end on Contract Awards; Obligated $M = "
             "SUMIFS over Award Actions - the SAME live formulas the Recompete Radar uses. "
             "Incumbent since (blue) is the build-time chain-root start of the predecessor "
             "lineage (the one value a formula can't walk), so Tenure = (As-of - Incumbent "
             "since) stays formula-driven. Superseded vehicles (a live same-incumbent "
             "follow-on exists) are NOT shown - see Lineage status on the Recompete Radar. "
             "Open notice (PSC) = an OPEN SAM notice shares this vehicle's PSC (a weak, "
             "same-product signal; the open pipeline is mostly USACE civil-works, so most "
             "rows are blank)."],
            styles=[S_DEFAULT])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="RecompeteCalendar", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render)


RECOMPETE_CALENDAR = _make_calendar()
