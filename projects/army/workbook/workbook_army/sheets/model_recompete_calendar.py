"""model_recompete_calendar - the Recompete Research Queue (Saronic-first, live).

A prioritized research/BD QUEUE projected from the Timing & Incumbent Screen: one row per
actionable vehicle (a lineage chain TAIL - analyst-confirmed superseded vehicles fold out),
ordered SARONIC-FIRST (Core -> Adjacent -> Peripheral) and within a tier by the recompete
decision date, with an Overdue/expired section last. Where the Screen is the full $-ranked
inventory, this is the "what to chase, in what order, by when" queue.

Provenance contract (same as the Screen): every displayed number is either a LIVE in-sheet
formula (BLACK), a cross-sheet LINK (GREEN), or an honest hardcoded input (BLUE) - none are
baked-in-Python values masquerading as derived. Decision date is the CLASSIFIED effective
recompete date on the Contract Families leaf (the IDV ordering-period end, NOT the conflated
latest task-order end), surfaced as a live INDEX/MATCH link; Decision FY, Phase, Months to
decision, Capture-start, Notice-by, Tenure and Option yrs left are in-sheet date math, and
Related activity (PSC) / In-market are live COUNTIFS - all re-clock off the single As-of cell
(_tabs.AS_OF_CELL).

STATIC-SORT LIMITATION (honest): rows are ordered at BUILD time (tier, then decision date).
The Phase column re-clocks LIVE off As-of, but the physical row ORDER does not - re-run the
build to re-sort after a big As-of change. The one value a formula cannot reach is incumbent
tenure across the PREDECESSOR chain (a multi-hop walk), so its root start is a BLUE input
("Incumbent since") and Tenure = (As-of - Incumbent since) stays a black formula. The planned
RFI / solicitation / award / capture-override milestones are durable analyst inputs. Built
via _make_calendar().
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet, cf_rule
from workbook_core.styles import (
    S_DATE, S_DATE_INPUT, S_DATE_LINK, S_DEFAULT, S_INT, S_LINK_NUM, S_NUM, S_LINK_PCT,
    S_TITLE_SECTION, S_TITLE_SHEET,
    DXF_IMMINENT, DXF_COVERAGE, DXF_INMARKET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._cuts import date_serial
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_RESEARCH_QUEUE, AS_OF_CELL
from workbook_army.sheets._radar_formulas import family_formulas
from workbook_army.sheets.data_pipeline_events import pipeline_cols
from workbook_army.sheets.data_contract_families import families_cols
from workbook_army.sheets.input_recompete_reviews import recompete_reviews_cols
from workbook_army.sheets import config as CFG
from workbook_army.sheets.model_recompete_radar import (
    load_families, _MIN_OBLIG, _AS_OF, _tier_rank,
)

_GROUP = "model"
_TAB = TAB_RESEARCH_QUEUE
_NOTICE_LEAD_DAYS = CFG.NOTICE_LEAD_DAYS    # notice-by = decision - this (solicitation lead)
_CAPTURE_LEAD_DAYS = CFG.CAPTURE_LEAD_DAYS  # capture-start = decision - this (18 mo BD lead)

# "Scope" (leftmost) splits the actionable capture work from the expired-lineage backlog
# (audit #3): filter Scope = Active for the capture queue. The narrowed queue keeps the
# capture-oriented fields (audit #5); the planned milestones + capture override are linked
# from the Recompete Reviews input tab, and the reconciliation lenses / anomaly live on
# Timing Detail. Selected $M is the materiality measure that drives ranking.
_HEADERS = [
    "Scope",
    "Phase", "Decision FY", "Decision date", "Date confidence",
    "Months to decision", "Capture-start (est)", "Notice-by (est)", "Capture lead (days)",
    "Family (vehicle PIID)", "Incumbent", "Customer segment", "Saronic tier",
    "Incumbent since", "Tenure (yrs)", "PSC",
    "Selected $M", "Coverage",
    "Potential end", "Option yrs left",
    "Related activity (PSC)", "In-market (confirmed)",
    "Confidence", "Pursuit access", "Notes",
]
_NCOLS = len(_HEADERS)
_COLS = [14,
         20, 9, 13, 13,
         13, 15, 14, 14,
         22, 34, 30, 26,
         13, 10, 8,
         12, 10,
         13, 12,
         18, 16,
         14, 14, 28]
assert len(_COLS) == _NCOLS, (len(_COLS), _NCOLS)
_CENTER = {"Decision date", "Months to decision", "Capture-start (est)", "Notice-by (est)",
           "Capture lead (days)", "Tenure (yrs)",
           "Selected $M", "Coverage", "Potential end", "Option yrs left"}
_CL = {h: col_letter(i + 1) for i, h in enumerate(_HEADERS)}

# Per-column render style: green cross-sheet links (Selected $M, Coverage, Decision date),
# black live date/number math, default black text elsewhere. Confidence / Pursuit access /
# Notes / Capture lead are black links into Recompete Reviews. Incumbent since is the one
# blue input - a build-baked chain-root start the multi-hop walk can't express in a formula.
_STYLE = {
    "Decision date": S_DATE_LINK, "Coverage": S_LINK_PCT, "Selected $M": S_LINK_NUM,
    "Months to decision": S_INT, "Option yrs left": S_INT, "Capture lead (days)": S_INT,
    "Capture-start (est)": S_DATE, "Notice-by (est)": S_DATE, "Potential end": S_DATE,
    "Incumbent since": S_DATE_INPUT, "Tenure (yrs)": S_NUM,
}


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

    # actionable = families above the floor with a DECISION date, EXCLUDING only those an
    # analyst CONFIRMED as superseded (succ_of). An expired vehicle with merely a *candidate*
    # successor still shows - flagged unresolved, not hidden. Order is SARONIC-FIRST (tier),
    # then by decision date, forward section then overdue. Static at build time (see header).
    tails = [a for a in attrs.values()
             if a["total"] >= _MIN_OBLIG and a["key"] not in succ_of
             and a["decision_date"] is not None]
    forward = sorted((a for a in tails if a["decision_date"] >= asof_ser),
                     key=lambda a: (_tier_rank(a["saronic_tier"]), a["decision_date"]))
    overdue = sorted((a for a in tails if a["decision_date"] < asof_ser),
                     key=lambda a: (_tier_rank(a["saronic_tier"]), -a["decision_date"]))
    ordered = forward + overdue

    # ---- live formulas (black) + cross-sheet links (green) ----
    fam = lambda r: f"${_CL['Family (vehicle PIID)']}{r}"
    F = family_formulas(fam, AS_OF_CELL)            # shared roll-ups (same as the Screen)
    potend_f, inmkt_f = F["pot_end"], F["inmkt"]

    # Decision date + Coverage are CLASSIFIED values on the Contract Families leaf, surfaced
    # as live green INDEX/MATCH links; every As-of clock below re-points to the decision cell.
    FAM_KEY = families_cols("family_key")

    def _fam_link(header):
        rng = families_cols(header)

        def f(r):
            idx = f"INDEX({rng},MATCH({fam(r)},{FAM_KEY},0))"
            return f'=IF({idx}="","",{idx})'      # blank source -> blank, not 1899-12-30
        return f

    def _fam_link_millions(header):
        rng = families_cols(header)

        def f(r):
            idx = f"INDEX({rng},MATCH({fam(r)},{FAM_KEY},0))"
            return f'=IF({idx}="","",{idx}/1000000)'   # raw-$ leaf -> $M; blank stays blank
        return f

    decision_f = _fam_link("effective_decision_date")
    coverage_f = _fam_link("coverage_ratio")
    selected_f = _fam_link_millions("selected_measure")   # the measure that drives materiality

    DD, IS = _CL["Decision date"], _CL["Incumbent since"]
    PE, PSCc, CLO = _CL["Potential end"], _CL["PSC"], _CL["Capture lead (days)"]
    PL_PSC, PL_DEADLINE = pipeline_cols("psc_code"), pipeline_cols("response_deadline")

    # Confidence / Pursuit access / Notes / Capture lead link the Recompete Reviews input tab
    # by family key (black derived; the editable cells live on that inputs tab). Capture lead
    # then feeds Capture-start, so an override re-clocks live.
    RR_KEY = recompete_reviews_cols("family_key")

    def rev_link(col):
        rng = recompete_reviews_cols(col)
        return lambda r: f'=IFERROR(INDEX({rng},MATCH({fam(r)},{RR_KEY},0)),"")'

    conf_f, pursuit_f, notes_f = (rev_link("confidence"), rev_link("pursuit_access"),
                                  rev_link("notes"))
    clo_f = rev_link("capture_lead_override_days")

    # Decision FY = DoD fiscal year of the (live) decision date; FY rolls Oct 1.
    fy_f = lambda r: (
        f'=IF(${DD}{r}="","","FY"&TEXT(MOD(IF(MONTH(${DD}{r})>=10,'
        f'YEAR(${DD}{r})+1,YEAR(${DD}{r})),100),"00"))')
    # Scope splits actionable capture (forward) from the expired-lineage backlog (audit #3),
    # keyed on the SAME live decision-date vs As-of test as Phase, so it re-clocks live.
    # Filter Scope = Active for the capture queue. (Superseded vehicles already fold out.)
    scope_f = lambda r: (
        f'=IF(${DD}{r}="","",IF(${DD}{r}<{AS_OF_CELL},"Expired-lineage","Active"))')
    # Phase re-clocks LIVE off As-of (the row ORDER is static - see the header note).
    phase_f = lambda r: (
        f'=IF(${DD}{r}="","",IF(${DD}{r}<{AS_OF_CELL},"Expired - unresolved",'
        f'IF((${DD}{r}-{AS_OF_CELL})<=365,"Imminent (<=12 mo)",'
        f'IF((${DD}{r}-{AS_OF_CELL})<=1095,"Forward (1-3 yr)","Long-range (3+ yr)"))))')
    notice_f = lambda r: f'=IF(${DD}{r}="","",${DD}{r}-{_NOTICE_LEAD_DAYS})'
    # Capture-start = decision - 18 mo (the BD/teaming lead; 90 days is far too late to BEGIN
    # capture of a complex autonomous-vessel buy). Per-row override honored when filled.
    capture_f = lambda r: (f'=IF(${DD}{r}="","",${DD}{r}-'
                           f'IF(${CLO}{r}="",{_CAPTURE_LEAD_DAYS},${CLO}{r}))')
    months_f = lambda r: f'=IF(${DD}{r}="","",ROUND((${DD}{r}-{AS_OF_CELL})/30.44,0))'
    tenure_f = lambda r: (f'=IF(${IS}{r}="","",'
                          f'ROUND(({AS_OF_CELL}-${IS}{r})/365.25,1))')
    # Option years remaining = (potential - decision) / 365, floored at 0. Blank decision ->
    # blank; no potential-end on record -> "unknown" (NOT 0, which would read as "no options").
    optyrs_f = lambda r: (f'=IF(${DD}{r}="","",IF(${PE}{r}="","unknown",'
                          f'MAX(0,ROUND((${PE}{r}-${DD}{r})/365,0))))')
    # Related activity (PSC) = count of OPEN Pipeline Events notices (deadline >= As-of) that
    # share this vehicle's PSC - RELATED market activity, NOT a confirmed link (21 of 22 such
    # signals are two PSC-1935 notices). The confirmed signal is In-market, next column.
    related_psc_f = lambda r: (
        f'=IF(${PSCc}{r}="","",'
        f'IF(COUNTIFS({PL_PSC},${PSCc}{r},{PL_DEADLINE},">="&{AS_OF_CELL})>0,'
        f'"Y ("&COUNTIFS({PL_PSC},${PSCc}{r},{PL_DEADLINE},">="&{AS_OF_CELL})&")",""))')

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Saronic-first capture queue: actionable watercraft vehicles by decision date. "
             "Filter Scope = Active for the capture work."], styles=[S_ITALIC])
    c.blank(2)

    c.banner("§1 - Research queue", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    styles = [_STYLE.get(h, S_DEFAULT) for h in _HEADERS]
    assert len(styles) == _NCOLS, (len(styles), _NCOLS)

    for a in ordered:
        c.write([scope_f, phase_f, fy_f, decision_f, a["date_confidence"],
                 months_f, capture_f, notice_f, clo_f,
                 a["key"], a["incumbent"], a["segment"], a["saronic_tier"],
                 root_start(a["key"]), tenure_f, a["psc"],
                 selected_f, coverage_f,
                 potend_f, optyrs_f,
                 related_psc_f, inmkt_f,
                 conf_f, pursuit_f, notes_f],
                styles=styles, outline_level=1)
    last = hdr + len(ordered)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"

    c.blank(2)
    c.write([f"{len(forward)} forward + {len(overdue)} expired-unresolved. Counts and row "
             "order are fixed at build (Scope / Phase re-clock live) - re-run to re-sort."],
            styles=[S_DEFAULT])
    c.write(["Decision date / Selected $M / Coverage link Contract Families; Capture-start = "
             "decision - 18 mo. Reconciliation + anomaly: Timing Detail. Reviews: Recompete "
             "Reviews."], styles=[S_DEFAULT])

    # Conditional formatting: imminent decision, incomplete coverage, confirmed in-market.
    f0 = hdr + 1
    MOc, CVc, IMc = (_CL["Months to decision"], _CL["Coverage"],
                     _CL["In-market (confirmed)"])
    cfmt = [
        cf_rule(f"${MOc}${f0}:${MOc}${last}", DXF_IMMINENT,
                f'AND(${MOc}{f0}<>"",${MOc}{f0}>=0,${MOc}{f0}<=12)', priority=1),
        cf_rule(f"${CVc}${f0}:${CVc}${last}", DXF_COVERAGE,
                f'AND(${CVc}{f0}<>"",${CVc}{f0}<1)', priority=2),
        cf_rule(f"${IMc}${f0}:${IMc}${last}", DXF_INMARKET, f'${IMc}{f0}="Y"', priority=3),
    ]

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, conditional_formatting=cfmt)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="RecompeteResearchQueue", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render)


RECOMPETE_CALENDAR = _make_calendar()
