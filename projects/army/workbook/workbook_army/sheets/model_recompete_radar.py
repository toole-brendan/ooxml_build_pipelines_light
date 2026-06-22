"""model_recompete_radar - the Timing & Incumbent Screen (live-formula contract screen).

A contract/incumbent SCREEN (renamed from "Recompete Radar"): a sound landscape of who
holds what and when each vehicle's authority lapses - NOT yet an opportunity forecast.
One row per watercraft contract FAMILY (vehicle): task orders collapse into their parent
IDV (family key = parent_idv_piid, else the standalone piid). Analytic columns are LIVE
Excel formulas (SUMIFS / COUNTIFS / MAXIFS / date math) over the data-leaf sheets and an
editable As-of cell, so the roll-ups recompute as the leaves change.

Data spine (the integrity refactor): the build-time family selection, reconciliation and
lineage now come from the CANONICAL contract_families.csv + the analyst lineage_edges.csv
(both produced by research/contracts/aggregate_contracts.py), NOT from a private compute
here. That fixes three reviewed defects:
  * Obligation reconciliation - a SINGLE selected measure (per-mod action sum when its
    coverage of the award-reported obligation is complete, else award-level with an
    explicit fallback flag) drives BOTH the materiality floor and the ranking; the radar
    then shows Award-reported $M, Recon. $M (actions) and their Coverage side by side so a
    partial/negative reconstruction can never masquerade as a vehicle's lifetime value.
  * Parent-IDV hydration - orphan IDVs were hydrated into Contract Awards (synthesized
    rows from the SAM Contract Awards API), so the live MAXIFS resolves Parent/vehicle end.
  * Lineage as evidence, not verdict - a predecessor is only SUPPRESSED ("Superseded")
    when an analyst marks the successor edge Confirmed/Probable in lineage_edges.csv; an
    unreviewed expired vehicle reads "Expired - successor unresolved", never a definitive
    overdue/superseded call. Candidate predecessor/successor PIIDs are still shown.

Customer segment (Army operational vs USACE civil works vs MRO vs RDT&E vs peripheral)
is carried from the canonical table so the radar never reports them as one market.

The soft analyst judgments (recompete Window override / Confidence / Pursuit access /
program / capability_node / Notes) are read from the DURABLE analyst/recompete_reviews.csv
(keyed by family_key) and rendered BLUE, so they survive a rebuild.

Built at import via _make_radar() into a standalone single-table screen.
"""
from __future__ import annotations

import csv
from collections import defaultdict

from workbook_core.primitives import col_letter, worksheet, cf_rule
from workbook_core.styles import (
    S_BOLD, S_DATE_INPUT, S_DATE_LINK, S_DEFAULT, S_INT, S_LINK_NUM, S_NUM, S_LINK_PCT,
    S_TITLE_SECTION, S_TITLE_SHEET,
    DXF_IMMINENT, DXF_COVERAGE, DXF_INMARKET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._cuts import load_table, date_serial
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_TIMING_SCREEN, AS_OF_ROW
from workbook_army.sheets._radar_formulas import family_formulas
from workbook_army.sheets.data_contract_families import families_cols
from workbook_army.sheets.model_market_size import market_size_cols
from workbook_army.sheets.input_recompete_reviews import recompete_reviews_cols
from workbook_army.sheets._analyst import load_analyst_table, value as a_value, ANALYST_DIR
from workbook_army.sheets import config as CFG

_GROUP = "model"
_TAB = TAB_TIMING_SCREEN
_AS_OF = CFG.AS_OF               # default as-of; editable in-sheet (re-clocks all math)
_MIN_OBLIG = CFG.MIN_OBLIG       # materiality floor (single selected measure per family)
_GAP_CAP_DAYS = CFG.GAP_CAP_DAYS
_OVERLAP_DAYS = CFG.OVERLAP_DAYS

# Watercraft-relevance sets - used ONLY by the no-canonical-CSV fallback path.
_WC_PSC, _WC_NAICS = CFG.WC_PSC, CFG.WC_NAICS
_WC_PRIMES, _WC_DESC = CFG.WC_PRIMES, CFG.WC_DESC

# The NARROW primary screen (audit #5): the decision-grade columns only. Cohort structure,
# the four end-date lenses, reconciliation, lineage candidates, action counts and anomaly
# detail move to the companion Timing Detail sheet; the per-family analyst judgment lives on
# the Recompete Reviews input tab (linked here). Selected $M / Coverage / Decision date are
# green links into Contract Families; Confidence / Pursuit access link Recompete Reviews.
_HEADERS = [
    "Family (vehicle PIID)", "Incumbent", "Customer segment", "Saronic tier",
    "Selected $M", "Coverage", "Decision date", "Months to decision", "Decision window",
    "Date confidence", "In-market notice", "Opportunity", "Saronic priority score",
    "Confidence", "Pursuit access",
]
_NCOLS = len(_HEADERS)
_COLS = [22, 30, 26, 20, 12, 10, 15, 13, 14, 13, 13, 28, 14, 13, 14]
assert len(_COLS) == _NCOLS, (len(_COLS), _NCOLS)
_CENTER = {"Selected $M", "Coverage", "Decision date", "Months to decision",
           "Saronic priority score"}
_STYLE = {
    "Selected $M": S_LINK_NUM, "Coverage": S_LINK_PCT, "Decision date": S_DATE_LINK,
    "Months to decision": S_INT, "Saronic priority score": S_LINK_PCT,
}
# within-row column letters (gutter mode: header i -> col_letter(i+1))
_CL = {h: col_letter(i + 1) for i, h in enumerate(_HEADERS)}


def _serial(s):
    return date_serial(s) if s else None


def _toint(s, default=1):
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return default


def _tier_rank(label):
    """Saronic-first sort rank from a tier label (Core=0, Adjacent=1, Peripheral=2). Keyed
    on the first word so it survives the parenthetical drift; unknown -> last."""
    return CFG.SARONIC_TIER_RANK.get(label.split()[0], 3) if label else 3


# ---- canonical load (preferred) -------------------------------------------
def load_families():
    """Watercraft family attributes + predecessor<->successor lineage maps, from the
    canonical contract_families.csv + analyst lineage_edges.csv. Shared by the RADAR and
    the CALENDAR so the two never disagree. Returns (attrs, pred_of, succ_of) where
    pred_of/succ_of are the CONFIRMED/Probable edges only (the suppression set); each
    family also carries cand_pred/cand_succ (strongest candidate, any disposition).
    Falls back to a compute over contract_awards if the canonical table is absent."""
    try:
        headers, rows = load_table("contract_families")
    except Exception:
        rows = None
    if not rows:
        return _load_families_legacy()

    ix = {h: i for i, h in enumerate(headers)}

    def g(row, c):
        j = ix.get(c)
        return row[j] if (j is not None and j < len(row)) else ""

    def fnum(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return 0.0

    attrs = {}
    for row in rows:
        if g(row, "is_watercraft") != "Y":
            continue
        key = g(row, "family_key")
        attrs[key] = {
            "key": key, "total": fnum(g(row, "selected_measure")),
            "award_oblig": fnum(g(row, "award_reported_obligation")),
            "action_sum": fnum(g(row, "reconstructed_action_sum")),
            "coverage_status": g(row, "coverage_status"),
            "materiality_basis": g(row, "materiality_basis"),
            "reason": g(row, "relevance_basis"), "incumbent": g(row, "incumbent"),
            "uei": g(row, "recipient_uei"), "psc": g(row, "psc_code"),
            "naics": g(row, "naics_code"), "comp": g(row, "extent_competed"),
            "segment": g(row, "customer_segment"),
            "saronic_tier": g(row, "saronic_tier"),
            "vehicle_type": g(row, "vehicle_type"),
            "agreement_type": g(row, "agreement_type"),
            "award_structure": g(row, "single_or_multiple_award"),
            "cohort_id": g(row, "cohort_id"), "cohort_role": g(row, "cohort_role"),
            "cohort_size": _toint(g(row, "cohort_size")),
            "start": _serial(g(row, "pop_start_date")),
            "end": _serial(g(row, "pop_current_end_date")),
            "pot": _serial(g(row, "pop_potential_end_date")),
            "ordering_end": _serial(g(row, "ordering_period_end")),
            # The classified recompete date + its split-out child follow-on lens (serials for
            # the build-time sort / Calendar; the sheets render them as live INDEX/MATCH).
            "decision_date": _serial(g(row, "effective_decision_date")),
            "date_basis": g(row, "date_basis"),
            "date_confidence": g(row, "date_confidence"),
            "latest_to": _serial(g(row, "latest_task_order_end")),
            "date_anomaly": g(row, "date_anomaly"),
            "hydrated": g(row, "hydrated"),
            "cand_pred": None, "cand_succ": None,
        }
    pred_of, succ_of = _load_lineage_edges(attrs)
    return attrs, pred_of, succ_of


def _load_lineage_edges(attrs):
    """Read analyst/lineage_edges.csv: set cand_pred/cand_succ (strongest candidate, any
    disposition) on attrs, and return CONFIRMED/Probable-only pred_of/succ_of (the set
    that SUPPRESSES a predecessor). No file -> no suppression (nothing 'Superseded')."""
    pred_of, succ_of = {}, {}
    path = ANALYST_DIR / "lineage_edges.csv"
    if not path.exists():
        return pred_of, succ_of
    best_succ, best_pred = {}, {}            # key -> (other_key, score)
    with open(path, newline="") as f:
        for e in csv.DictReader(f):
            pk, sk = e.get("predecessor_family"), e.get("successor_family")
            if pk not in attrs or sk not in attrs:
                continue
            try:
                score = float(e.get("evidence_score") or 0)
            except ValueError:
                score = 0.0
            if pk not in best_succ or score > best_succ[pk][1]:
                best_succ[pk] = (sk, score)
            if sk not in best_pred or score > best_pred[sk][1]:
                best_pred[sk] = (pk, score)
            if (e.get("analyst_disposition") or "").strip() in ("Confirmed", "Probable"):
                succ_of[pk] = sk
                pred_of[sk] = pk
    for pk, (sk, _) in best_succ.items():
        attrs[pk]["cand_succ"] = sk
    for sk, (pk, _) in best_pred.items():
        attrs[sk]["cand_pred"] = pk
    return pred_of, succ_of


# ---- legacy fallback (only when contract_families.csv is absent) -----------
def _wc_reason(g, row):
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


def _build_lineage(attrs):
    """Same-incumbent (UEI)+PSC temporal chaining; used only by the fallback path to
    populate candidate maps (no analyst dispositions exist without the canonical pull)."""
    groups = defaultdict(list)
    for a in attrs.values():
        if a["uei"] and a["psc"] and a["start"] is not None and a["end"] is not None:
            groups[(a["uei"], a["psc"])].append(a)
    succ = {}
    for members in groups.values():
        members.sort(key=lambda a: (a["start"], a["end"]))
        for i, A in enumerate(members):
            best, best_gap = None, None
            for B in members[i + 1:]:
                gap = B["start"] - A["end"]
                if -_OVERLAP_DAYS <= gap <= _GAP_CAP_DAYS:
                    if best_gap is None or abs(gap) < abs(best_gap):
                        best, best_gap = B, gap
            if best is not None and (A["key"] not in succ
                                     or abs(best_gap) < abs(succ[A["key"]][1])):
                succ[A["key"]] = (best["key"], best_gap)
    pred = {}
    for a_key, (b_key, gap) in succ.items():
        if b_key not in pred or abs(gap) < abs(pred[b_key][1]):
            pred[b_key] = (a_key, gap)
    return ({k: v[0] for k, v in pred.items()}, {k: v[0] for k, v in succ.items()})


def _load_families_legacy():
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
        key = g(row, "parent_idv_piid") or g(row, "piid")
        if key:
            fams[key].append(row)
    attrs = {}
    for key, frows in fams.items():
        reason = next((r for r in (_wc_reason(g, x)
                       for x in sorted(frows, key=oblig, reverse=True)) if r), None)
        if reason is None:
            continue
        dom = max(frows, key=oblig)
        starts = [s for s in (_serial(g(x, "pop_start_date")) for x in frows) if s is not None]
        ends = [e for e in (_serial(g(x, "pop_current_end_date")) for x in frows) if e is not None]
        pots = [p for p in (_serial(g(x, "pop_potential_end_date")) for x in frows) if p is not None]
        tot = sum(oblig(x) for x in frows)
        attrs[key] = {
            "key": key, "total": tot, "award_oblig": tot, "action_sum": 0.0,
            "coverage_status": "(no canonical table)", "materiality_basis": "award",
            "reason": reason, "incumbent": g(dom, "recipient_name"),
            "uei": (g(dom, "recipient_uei") or "").strip(), "psc": g(dom, "psc_code"),
            "naics": g(dom, "naics_code"),
            "comp": g(dom, "extent_competed_description") or g(dom, "extent_competed"),
            "segment": "", "saronic_tier": "", "vehicle_type": "",
            "agreement_type": "", "award_structure": "",
            "cohort_id": "", "cohort_role": "Standalone", "cohort_size": 1,
            "start": min(starts) if starts else None,
            "end": max(ends) if ends else None,
            "pot": max(pots) if pots else None, "ordering_end": None,
            # No canonical timing without the family table: degrade the decision date to the
            # latest current end (the old conflated behaviour) and flag it Low confidence.
            "decision_date": max(ends) if ends else None,
            "date_basis": "(no canonical table)", "date_confidence": "Low",
            "latest_to": max(ends) if ends else None, "date_anomaly": "",
            "hydrated": "",
            "cand_pred": None, "cand_succ": None,
        }
    cand_pred, cand_succ = _build_lineage(attrs)
    for k, v in cand_succ.items():
        attrs[k]["cand_succ"] = v
    for k, v in cand_pred.items():
        attrs[k]["cand_pred"] = v
    return attrs, {}, {}            # no confirmed suppression without analyst review


def _screened():
    """Select the screened watercraft families and rank them Saronic-FIRST: tier, then the
    live commercial-priority score, then historical $ as the tie-break. Computed ONCE and
    shared by both the primary screen and the Timing Detail sheet, so a reader can cross-
    reference row N between them. Returns (sorted_selected, succ_of)."""
    attrs, pred_of, succ_of = load_families()
    attribution = load_analyst_table("award_opportunity_attribution", "family_key")
    opps = load_analyst_table("opportunities", "opportunity_id")
    sr = load_analyst_table("saronic_relevance", "opportunity_id")
    ma = load_analyst_table("market_assumptions", "opportunity_id")

    def _favg(oid):
        vals = []
        for col in ("mission_fit", "platform_fit", "autonomy_c2_fit"):
            raw = (a_value(sr, oid, col) or "").strip()
            if raw:
                try:
                    vals.append(float(raw))
                except ValueError:
                    pass
        return sum(vals) / len(vals) if vals else 0.0     # Excel AVERAGE: skip blanks

    def _num(table, oid, col):
        try:
            return float((a_value(table, oid, col) or "").strip())
        except ValueError:
            return 0.0

    def priority_of(family_key):
        """(score, opportunity_name) for a family: the Market-Size Saronic-priority composite
        (mean fit x timing x pursuit x win), looked up through its attributed opportunity.
        Build-time REPLICA of the live INDEX/MATCH formula, so the sort matches the sheet."""
        oid = (a_value(attribution, family_key, "opportunity_id") or "").strip()
        if not oid:
            return 0.0, ""
        name = a_value(opps, oid, "name") or oid
        score = (_favg(oid) * _num(ma, oid, "timing_conf")
                 * _num(ma, oid, "pursuit_access") * _num(ma, oid, "win_prob"))
        return round(score, 6), name

    selected = [a for a in attrs.values() if a["total"] >= _MIN_OBLIG]
    for a in selected:
        a["priority_score"], a["opp_name"] = priority_of(a["key"])
    selected.sort(key=lambda d: (_tier_rank(d["saronic_tier"]),
                                 -d["priority_score"], -d["total"]))
    return selected, succ_of


# Computed once at import; model_timing_detail imports these so the two sheets share order.
SCREENED, SUCC_OF = _screened()


def family_link_builder(fam):
    """An INDEX/MATCH-by-family-key link builder into Contract Families (shared by the screen
    + Timing Detail). _link(header) -> fn(row) -> a green-link formula resolving that family's
    value, blank-safe; _link_millions(header) divides a raw-$ leaf by 1e6."""
    fam_key = families_cols("family_key")

    def _link(header):
        rng = families_cols(header)

        def f(r):
            idx = f"INDEX({rng},MATCH({fam(r)},{fam_key},0))"
            return f'=IF({idx}="","",{idx})'      # blank source -> blank, not 1899-12-30
        return f

    def _link_millions(header):
        rng = families_cols(header)

        def f(r):
            idx = f"INDEX({rng},MATCH({fam(r)},{fam_key},0))"
            return f'=IF({idx}="","",{idx}/1000000)'
        return f

    return _link, _link_millions


def _make_screen():
    selected, succ_of = SCREENED, SUCC_OF

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["One row per watercraft contract family: incumbent, decision timing and Saronic "
             "priority. A screen, not a forecast."], styles=[S_ITALIC])
    c.blank(2)
    asof_row = c.write(["As-of date", date_serial(_AS_OF),
                        "edit to re-clock every timing column (row order is fixed at build)"],
                       styles=[S_BOLD, S_DATE_INPUT, S_ITALIC])
    assert asof_row == AS_OF_ROW, (asof_row, AS_OF_ROW)  # keeps _tabs.AS_OF_CELL valid
    ASOF = f"'{_TAB}'!$C${asof_row}"
    c.blank(2)

    FB = _CL["Family (vehicle PIID)"]
    DD, MO, OPP = _CL["Decision date"], _CL["Months to decision"], _CL["Opportunity"]
    fam = lambda r: f"${FB}{r}"
    inmkt_f = family_formulas(fam, ASOF)["inmkt"]

    # Selected $M / Coverage / Decision date are green links into the Contract Families leaf.
    _link, _link_millions = family_link_builder(fam)
    selected_f = _link_millions("selected_measure")
    coverage_f = _link("coverage_ratio")
    decision_f = _link("effective_decision_date")

    # Saronic priority score: live lookup of the family's opportunity composite on Market
    # Size, keyed by the Opportunity cell. Blank when unattributed (honest "not scored").
    MS_OPP, MS_PRIO = market_size_cols("Opportunity"), market_size_cols("Saronic priority")
    prio_link_f = lambda r: (f'=IF(${OPP}{r}="","",'
                             f'IFERROR(INDEX({MS_PRIO},MATCH(${OPP}{r},{MS_OPP},0)),""))')

    # Confidence / Pursuit access link the Recompete Reviews input tab by family key (black
    # derived text - the editable cells live there, not on this screen).
    RR_KEY = recompete_reviews_cols("family_key")

    def rev_link(col):
        rng = recompete_reviews_cols(col)
        return lambda r: f'=IFERROR(INDEX({rng},MATCH({fam(r)},{RR_KEY},0)),"")'

    conf_f, pursuit_f = rev_link("confidence"), rev_link("pursuit_access")

    months_f = lambda r: f'=IF(${DD}{r}="","",ROUND((${DD}{r}-{ASOF})/30.44,0))'
    window_f = lambda r: (
        f'=IF(${DD}{r}="","n/a",IF(${DD}{r}<{ASOF},"Expired",'
        f'IF(${MO}{r}<=12,"0-12 mo",IF(${MO}{r}<=24,"12-24 mo",'
        f'IF(${MO}{r}<=36,"24-36 mo","36+ mo")))))')

    c.banner("§1 - Contract timing & incumbent screen", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    f = hdr + 1
    styles = [_STYLE.get(h, S_DEFAULT) for h in _HEADERS]
    assert len(styles) == _NCOLS, (len(styles), _NCOLS)
    for d in selected:
        c.write([d["key"], d["incumbent"], d["segment"], d["saronic_tier"],
                 selected_f, coverage_f, decision_f, months_f, window_f,
                 d["date_confidence"], inmkt_f, d["opp_name"], prio_link_f,
                 conf_f, pursuit_f],
                styles=styles, outline_level=1)
    last = hdr + len(selected)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"

    SEL = _CL["Selected $M"]
    total_vals = [None] * _NCOLS
    total_vals[0] = f"Total - {len(selected)} vehicles screened"
    total_vals[_HEADERS.index("Selected $M")] = f"=SUBTOTAL(109,{SEL}{f}:{SEL}{last})"
    total_sty = [S_DEFAULT] * _NCOLS
    total_sty[0] = S_BOLD
    total_sty[_HEADERS.index("Selected $M")] = S_NUM
    c.total(total_vals, styles=total_sty, n_cols=_NCOLS)

    c.blank(2)
    c.write(["Selected $M, Coverage and Decision date link Contract Families; Months and "
             "Decision window re-clock off As-of."], styles=[S_DEFAULT])
    c.write(["Cohort, end-date lenses, reconciliation, lineage and anomalies: Timing Detail. "
             "Per-family reviews: Recompete Reviews."], styles=[S_DEFAULT])
    c.write(["Historical obligations, not TAM/SAM."], styles=[S_ITALIC])

    # Conditional formatting: imminent decision, incomplete coverage, confirmed in-market.
    CV, IM = _CL["Coverage"], _CL["In-market notice"]
    cfmt = [
        cf_rule(f"${MO}${f}:${MO}${last}", DXF_IMMINENT,
                f'AND(${MO}{f}<>"",${MO}{f}>=0,${MO}{f}<=12)', priority=1),
        cf_rule(f"${CV}${f}:${CV}${last}", DXF_COVERAGE,
                f'AND(${CV}{f}<>"",${CV}{f}<1)', priority=2),
        cf_rule(f"${IM}${f}:${IM}${last}", DXF_INMARKET, f'${IM}{f}="Y"', priority=3),
    ]

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, conditional_formatting=cfmt)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="TimingIncumbentScreen", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render)


RECOMPETE_RADAR = _make_screen()
