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
    S_DATE, S_DATE_INPUT, S_DATE_LINK, S_DEFAULT, S_INT, S_INT_INPUT, S_LINK_NUM, S_NUM,
    S_LINK_PCT,
    S_TITLE_SECTION, S_TITLE_SHEET,
    DXF_ANOMALY, DXF_IMMINENT, DXF_COVERAGE, DXF_INMARKET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._cuts import date_serial
from workbook_army.sheets._text_input import S_TEXT_INPUT
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_RESEARCH_QUEUE, AS_OF_CELL
from workbook_army.sheets._radar_formulas import family_formulas
from workbook_army.sheets._analyst import load_analyst_table, value as a_value
from workbook_army.sheets.data_pipeline_events import pipeline_cols
from workbook_army.sheets.data_contract_families import families_cols
from workbook_army.sheets import config as CFG
from workbook_army.sheets.model_recompete_radar import (
    load_families, _MIN_OBLIG, _AS_OF, _tier_rank,
)

_GROUP = "model"
_TAB = TAB_RESEARCH_QUEUE
_NOTICE_LEAD_DAYS = CFG.NOTICE_LEAD_DAYS    # notice-by = decision - this (solicitation lead)
_CAPTURE_LEAD_DAYS = CFG.CAPTURE_LEAD_DAYS  # capture-start = decision - this (18 mo BD lead)

# "Scope" (leftmost, prominent) splits the actionable capture work from the expired-lineage
# backlog so the queue is a BD instrument, not one undifferentiated list (audit #3): filter
# Scope = Active for the capture queue. The money block carries THREE measures - the Selected
# measure (what drives materiality/ranking), the Award-reported lens, and the per-mod Recon.
# (actions) - so award-fallback rows aren't misread (audit #2; the old single "Obligated $M"
# always showed the reconstructed action sum, misleading for ~41 award-basis rows).
_HEADERS = [
    "Scope",
    "Phase", "Decision FY", "Decision date", "Date confidence", "Anomaly flag",
    "Months to decision", "Capture-start (est)", "Notice-by (est)",
    "Planned RFI", "Planned solicitation", "Planned award",
    "Capture lead override (days)", "Milestone source",
    "Family (vehicle PIID)", "Incumbent", "Customer segment", "Saronic tier",
    "Incumbent since", "Tenure (yrs)", "PSC",
    "Selected $M", "Award-reported $M", "Recon. $M (actions)", "Coverage", "Materiality basis",
    "Potential end", "Option yrs left",
    "Related activity (PSC)", "In-market (confirmed)",
    "Confidence", "Pursuit access", "Notes",
]
_NCOLS = len(_HEADERS)
_COLS = [14,
         20, 9, 13, 13, 32,
         13, 15, 14,
         13, 16, 13,
         16, 16,
         22, 34, 30, 26,
         13, 10, 8,
         12, 15, 16, 10, 16,
         13, 12,
         18, 16,
         14, 14, 28]
assert len(_COLS) == _NCOLS, (len(_COLS), _NCOLS)
_CENTER = {"Decision date", "Months to decision", "Capture-start (est)", "Notice-by (est)",
           "Capture lead override (days)", "Tenure (yrs)",
           "Selected $M", "Award-reported $M", "Recon. $M (actions)", "Coverage",
           "Potential end", "Option yrs left"}
_CL = {h: col_letter(i + 1) for i, h in enumerate(_HEADERS)}

# Per-column render style: green for the cross-sheet links (decision date, coverage), blue
# for the analyst inputs, black for the live date/number math, default black text elsewhere
# (Phase / FY formulas + baked classified facts: confidence, anomaly, tier, materiality).
_STYLE = {
    "Decision date": S_DATE_LINK, "Coverage": S_LINK_PCT,
    "Months to decision": S_INT, "Option yrs left": S_INT,
    "Capture-start (est)": S_DATE, "Notice-by (est)": S_DATE, "Potential end": S_DATE,
    "Planned RFI": S_DATE_INPUT, "Planned solicitation": S_DATE_INPUT,
    "Planned award": S_DATE_INPUT, "Incumbent since": S_DATE_INPUT,
    "Capture lead override (days)": S_INT_INPUT, "Milestone source": S_TEXT_INPUT,
    "Tenure (yrs)": S_NUM,
    # money block: Selected $M is a green cross-sheet link; Award-reported / Recon. are live
    # in-sheet SUMIFS (black), matching the Screen.
    "Selected $M": S_LINK_NUM, "Award-reported $M": S_NUM, "Recon. $M (actions)": S_NUM,
    "Confidence": S_TEXT_INPUT, "Pursuit access": S_TEXT_INPUT, "Notes": S_TEXT_INPUT,
}


def _make_calendar():
    attrs, pred_of, succ_of = load_families()
    reviews = load_analyst_table("recompete_reviews", "family_key")
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

    def _msdate(key, col):
        v = (a_value(reviews, key, col) or "").strip()
        return date_serial(v) if v else None

    def _msint(key, col):
        v = (a_value(reviews, key, col) or "").strip()
        try:
            return int(float(v))
        except ValueError:
            return None

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
    potend_f, obl_f, obl_award_f, inmkt_f = F["pot_end"], F["obl"], F["obl_award"], F["inmkt"]

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
    PE, PSCc, CLO = _CL["Potential end"], _CL["PSC"], _CL["Capture lead override (days)"]
    PL_PSC, PL_DEADLINE = pipeline_cols("psc_code"), pipeline_cols("response_deadline")

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
    c.write(["Saronic-first recompete RESEARCH QUEUE - actionable watercraft vehicles "
             "(lineage chain tails) ordered by Saronic tier (Core -> Adjacent -> Peripheral) "
             "then decision date, with an expired/overdue section last. SCOPE (col B) splits "
             "the actionable capture work from the expired-lineage backlog - filter Scope = "
             "Active for the capture queue. Decision date is the CLASSIFIED recompete date "
             "(IDV ordering-period end, NOT the conflated latest task-order end), a live link "
             "off Contract Families; Capture-start = decision - 18 mo (the BD lead - 90-day "
             "Notice-by is far too late to start), and the whole clock re-clocks off the As-of "
             "cell. MONEY: Selected $M is the measure that drives materiality/ranking; "
             "Award-reported $M and Recon. $M (actions) are the two reconciliation lenses, so "
             "award-fallback rows are not misread. Date confidence / Anomaly flag temper each "
             "row. ROW ORDER is STATIC (build-time) though Scope/Phase re-clock live - re-run "
             "the build to re-sort. Planned RFI/solicitation/award, capture override, "
             "Confidence / Pursuit access / Notes are ANALYST inputs "
             "(analyst/recompete_reviews.csv)."],
            styles=[S_ITALIC])
    c.blank(2)

    c.banner("§1 - Research queue (Saronic-first; forward, then expired-unresolved)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    styles = [_STYLE.get(h, S_DEFAULT) for h in _HEADERS]
    assert len(styles) == _NCOLS, (len(styles), _NCOLS)

    for a in ordered:
        k = a["key"]
        c.write([scope_f, phase_f, fy_f, decision_f, a["date_confidence"], a["date_anomaly"],
                 months_f, capture_f, notice_f,
                 _msdate(k, "planned_rfi_date"), _msdate(k, "planned_solicitation_date"),
                 _msdate(k, "planned_award_date"), _msint(k, "capture_lead_override_days"),
                 a_value(reviews, k, "milestone_source"),
                 k, a["incumbent"], a["segment"], a["saronic_tier"],
                 root_start(k), tenure_f, a["psc"],
                 selected_f, obl_award_f, obl_f, coverage_f, a["materiality_basis"],
                 potend_f, optyrs_f,
                 related_psc_f, inmkt_f,
                 a_value(reviews, k, "confidence"), a_value(reviews, k, "pursuit_access"),
                 a_value(reviews, k, "notes")],
                styles=styles, outline_level=1)
    last = hdr + len(ordered)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"

    c.blank(2)
    c.write([f"{len(forward)} forward vehicles (decision date >= As-of) + {len(overdue)} "
             "expired-unresolved (expired with NO analyst-confirmed successor - validate "
             "before treating as a live recompete). These counts are AS OF THE BUILD As-of; "
             "the Scope and Phase columns re-clock live when you change the As-of cell, but "
             "these totals (and the physical row order) only update on the next build. Ordered "
             "SARONIC-FIRST: Saronic tier, then decision date; USACE/peripheral sort last and "
             "can be hidden via the table AutoFilter. TIMING: Decision date = the CLASSIFIED "
             "effective recompete date (Contract Families!effective_decision_date - the IDV "
             "ordering-period end, with Date confidence / Anomaly flag carrying its caveats), "
             "NOT the conflated latest task-order end. Capture-start = decision - 18 mo "
             "(override per row); Notice-by = decision - 90 d. Option yrs left = (potential - "
             "decision)/365, 'unknown' when no potential end is on record. PROVENANCE: "
             "Potential end / Recon. $M (actions) are the SAME live MAXIFS / SUMIFS the Timing "
             "& Incumbent Screen uses; Coverage links "
             "the Screen's reconstruction ratio. Incumbent since (blue) is the chain-root "
             "start so Tenure stays formula-driven. SIGNALS: Related activity (PSC) is an "
             "OPEN notice sharing this vehicle's PSC - RELATED activity, not a confirmed "
             "link; In-market = a CONFIRMED notice<->family link on Notice Links. ONLY "
             "analyst-confirmed superseded vehicles fold out (see Lineage status + "
             "analyst/lineage_edges.csv on the Screen)."],
            styles=[S_DEFAULT])

    # Conditional formatting over the data block (hdr+1..last): imminent decisions,
    # anomalous dates, incomplete coverage, confirmed in-market (audit: presentation).
    f0 = hdr + 1
    MOc, ANc = _CL["Months to decision"], _CL["Anomaly flag"]
    CVc, IMc = _CL["Coverage"], _CL["In-market (confirmed)"]
    cfmt = [
        cf_rule(f"${ANc}${f0}:${ANc}${last}", DXF_ANOMALY, f'${ANc}{f0}<>""', priority=1),
        cf_rule(f"${MOc}${f0}:${MOc}${last}", DXF_IMMINENT,
                f'AND(${MOc}{f0}<>"",${MOc}{f0}>=0,${MOc}{f0}<=12)', priority=2),
        cf_rule(f"${CVc}${f0}:${CVc}${last}", DXF_COVERAGE,
                f'AND(${CVc}{f0}<>"",${CVc}{f0}<1)', priority=3),
        cf_rule(f"${IMc}${f0}:${IMc}${last}", DXF_INMARKET, f'${IMc}{f0}="Y"', priority=4),
    ]

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, conditional_formatting=cfmt)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="RecompeteResearchQueue", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render)


RECOMPETE_CALENDAR = _make_calendar()
