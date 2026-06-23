"""subaward_activity - historical supplier activity intensity on new-construction subawards.

This sheet characterizes the HISTORICAL ACTIVITY INTENSITY of the third-party suppliers: one-off /
brief makers vs broad, long-running vendors. It is a DESCRIPTIVE intensity measure, not a measure
of annual supplier retention or incumbency - those are reported at the Program x Archetype x FY
grain on Where to Play. Intensity is TWO INDEPENDENT AXES, so a single report count misleads. Both
axes are shown as their own 0-3 tier column, and the composite profile is just the more intense of
the two - nothing claims a mechanism a single axis can't establish:

  - BREADTH   = distinct subaward NUMBERS (one scope or many separate buys). Deduped: ~16.5% of
                subaward numbers are refiled, so raw report rows overstate breadth ~1.3x.
                Breadth Tier: 1 ->0   2-3 ->1   4-9 ->2   10+ ->3
  - DURATION  = first->last reported-action span in years. FFATA carries no period-of-
                performance field, so span is a reporting-based LOWER BOUND, not contractual
                PoP. Action Span / PoP = span / prime PoP says whether a vendor tracks the
                whole build or just a slice.
                Duration Tier: 0 ->0   <2yr->1   2 to <6yr->2   >=6yr->3

    Observed Activity Profile = CHOOSE(max(breadth tier, duration tier))
        = Single / one-time | Limited | Established | High / sustained activity

Layout (answer-first; sections numbered in the order they appear top-to-bottom; two of them are
native sortable tables):
  §1  Activity intensity  - counts & $ by profile (the punchline)          [styled block, live]
  §1b Breadth x Duration  - 4x4 vendor-count matrix (the two axes)         [styled block, live]
  §2  Vendor rollup       - one row per UEI, recurrence across all PIIDs    [NATIVE TABLE, live]
  §3  Engagement detail   - one row per UEI x prime PIID                    [NATIVE TABLE, live]
  §4  Activity by block   - first-observed / reactivated / continued by MYP [styled block, live]

The two row spines + their distinct-counts are materialized by
scripts/build_subaward_activity.py (a distinct-count has no clean/performant live-Excel form
at this row count). EVERYTHING else is a live aggregate over the three transaction leaves. §3
(engagement) is keyed on UEI + Prime PIID against the row's OWN program leaf only (PIIDs are
program-disjoint, so the other two leaves contribute exactly 0); §2 (vendor) is keyed on UEI
alone and stays 3-way additive (a UEI can span programs). §4 splits each block's vendors into
first-observed (never in any earlier block of the program's chain), reactivated (in an earlier
block but not the immediate predecessor), and continued-from-prior - all fully live over §3, with
the block chronology supplied as input via _BLOCK_PRED.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_INT, S_NUM, S_PCT, S_LINK_INT, S_DATE_LINK,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_classification_refactor.sheets._layout import RowCursor
from workbook_award_classification_refactor.sheets._italic import S_ITALIC
from workbook_award_classification_refactor.sheets._text_input import S_TEXT_INPUT
from workbook_award_classification_refactor.sheets._tabs import TAB_SUBAWARD_ACTIVITY
from workbook_award_classification_refactor.sheets._fiscal import TX_REAL
from workbook_award_classification_refactor.sheets._cuts import load_table, as_int
from workbook_award_classification_refactor.sheets._widths import header_styles
from workbook_award_classification_refactor.sheets.ddg_subaward_transactions import ddg_tx_cols
from workbook_award_classification_refactor.sheets.virginia_subaward_transactions import virginia_tx_cols
from workbook_award_classification_refactor.sheets.columbia_subaward_transactions import columbia_tx_cols
from workbook_award_classification_refactor.sheets.prime_awards import prime_awards_cols

_GROUP = "summary"
_TXS = (ddg_tx_cols, virginia_tx_cols, columbia_tx_cols)
# Program label (as materialized in the §3 spine) -> its single transaction leaf accessor.
PROG_TX = {"DDG": ddg_tx_cols, "Virginia": virginia_tx_cols, "Columbia": columbia_tx_cols}

# ---------------------------------------------------------------------------------------
# Shared column grid (content starts at column B = col_letter(1)). §2 and §3 share the first
# eleven columns (B-K) identically, so the two native tables read consistently and the grid
# widths fit both; L/M are repurposed per table; §3 extends to Q.
#   B UEI | C Vendor | D Distinct subawards | E Breadth Tier | F Span | G Duration Tier
#   H Observed Activity Profile | I Net $M | J Reports | K Negative Adjustments
#   L(=§2 Distinct PIIDs / §3 Program) | M(=§2 Distinct Programs / §3 PIID)
#   N Block/MYP | O Action Span / PoP | P First | Q Last
# ---------------------------------------------------------------------------------------
B_UEI, B_VEND, B_DSUB, B_BTIER, B_SPAN, B_DTIER, B_PROFILE, B_NET, B_REP, B_CORR = \
    "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"
B1_PROG, B1_PIID, B1_BLK, B1_COV, B1_FIRST, B1_LAST = "L", "M", "N", "O", "P", "Q"
B2_PIIDS, B2_PROGS = "L", "M"
_NCOLS = 16                      # B..Q - banners span the full width

# B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q
# D widened to 20 for the "Distinct Subaward Numbers" / "PIID-Subaward Pairs" headings.
_WIDTHS = [14, 31, 20, 12, 18, 12, 26, 15, 10, 14, 14, 22, 24, 14, 14, 14]
assert len(_WIDTHS) == _NCOLS

_PROFILE_LABELS = ("Single / one-time", "Limited", "Established", "High / sustained activity")

# Block chronology (HAND JUDGMENT - flag for review, like prime_awards' BLOCK_MYP). Predecessor
# = the immediately prior block WITHIN the same program; cross-program has no "prior" and the
# first block of each program is absent here (no predecessor -> New = all, Returning = 0).
_BLOCK_PRED = {
    "DDG FY13-17 MYP": "DDG FY11 (single-ship)",
    "DDG FY18-22 MYP": "DDG FY13-17 MYP",
    "DDG FY23-27 MYP": "DDG FY18-22 MYP",
    "Virginia LYS (cross-block)": "Virginia Block IV (LLTM)",
    "Virginia Block V (LLTM)": "Virginia LYS (cross-block)",
    "Virginia Block VI (LLTM)": "Virginia Block V (LLTM)",
}


def _earlier_blocks(blk: str) -> list[str]:
    """All strictly-earlier block labels in blk's program chain, walking the single immediate-
    predecessor map _BLOCK_PRED back to the program's first block. Baseline blocks (absent from
    _BLOCK_PRED) return []. The visited-set guard is belt-and-suspenders against a malformed map."""
    out, seen, cur = [], set(), _BLOCK_PRED.get(blk)
    while cur and cur not in seen:
        out.append(cur)
        seen.add(cur)
        cur = _BLOCK_PRED.get(cur)
    return out

# Prime Awards lookup ranges (authoritative prime PoP + the hand-set Block/MYP), by PIID.
_PA_PIID = prime_awards_cols("Prime PIID")
_PA_BLK = prime_awards_cols("Block / MYP")
_PA_START = prime_awards_cols("PoP Start")
_PA_END = prime_awards_cols("PoP Current End")


# --- live-formula builders --------------------------------------------------------------

def _k1(txc, r: int) -> str:
    """One program leaf's `uei_range,$UEI, piid_range,$PIID` for the §3 (UEI x PIID) grain."""
    return (f"{txc('Subawardee UEI')},${B_UEI}{r},"
            f"{txc('Prime PIID')},${B1_PIID}{r}")


def _k2(txc, r: int) -> str:
    """One program leaf's `uei_range,$UEI` for the §2 (UEI-only) rollup grain."""
    return f"{txc('Subawardee UEI')},${B_UEI}{r}"


def _sum3(template) -> str:
    """`=( leafA + leafB + leafC )` for a per-leaf formula fragment (3-way additive)."""
    return "=" + "+".join(template(t) for t in _TXS)


def _multi_leaf_span(keyed, r: int) -> str:
    """first->last span (years) when the key can match MORE THAN ONE program leaf (the §2 UEI
    grain - 383 vendors span >1 program). last = MAX of the per-leaf MAXIFS (a non-matching
    leaf's 0 can't beat a real serial). first = MIN of the per-leaf MINIFS with a non-matching
    leaf's 0 lifted to a sentinel (the §3 'MAX drops the zero' trick is WRONG here - it returns
    the LATEST per-program minimum, not the global earliest). Single-program vendors reduce to
    the same answer."""
    def _min(t): return f"_xlfn.MINIFS({t('Subaward Date')},{keyed(t, r)})"
    first = "MIN(" + ",".join(f"IF({_min(t)}=0,1E9,{_min(t)})" for t in _TXS) + ")"
    last = "MAX(" + ",".join(f"_xlfn.MAXIFS({t('Subaward Date')},{keyed(t, r)})" for t in _TXS) + ")"
    return f"=({last}-{first})/365.25"


def _breadth_tier(dsub_cell: str) -> str:
    """0-3 tier from distinct subaward numbers: 1 ->0   2-3 ->1   4-9 ->2   10+ ->3."""
    return f"IF({dsub_cell}>=10,3,IF({dsub_cell}>=4,2,IF({dsub_cell}>=2,1,0)))"


def _duration_tier(span_cell: str) -> str:
    """0-3 tier from the activity span (years): 0 ->0   <2 ->1   2 to <6 ->2   >=6 ->3."""
    return f"IF({span_cell}>=6,3,IF({span_cell}>=2,2,IF({span_cell}>0,1,0)))"


def _profile_formula(btier_cell: str, dtier_cell: str) -> str:
    """Observed Activity Profile = the label for the more intense of the two visible tiers."""
    labels = ",".join(f'"{lab}"' for lab in _PROFILE_LABELS)
    return f"=CHOOSE(MAX({btier_cell},{dtier_cell})+1,{labels})"


# shared tier / profile cells (same column letters D/E/F/G/H in §2 and §3) -----------------
def _f_btier(r):   return "=" + _breadth_tier(f"${B_DSUB}{r}")
def _f_dtier(r):   return "=" + _duration_tier(f"${B_SPAN}{r}")
def _f_profile(r): return _profile_formula(f"${B_BTIER}{r}", f"${B_DTIER}{r}")


# §3 (engagement) live cells - keyed on the row's OWN program leaf (single-leaf, PIID-disjoint)
def _e_reports(txc): return lambda r: f"=COUNTIFS({_k1(txc, r)})"
def _e_corr(txc):    return lambda r: f'=COUNTIFS({_k1(txc, r)},{txc("Subaward Amount $")},"<0")'
def _e_net(txc):     return lambda r: f"=SUMIFS({txc(TX_REAL)},{_k1(txc, r)})/1000000"
def _e_first(txc):   return lambda r: f"=_xlfn.MINIFS({txc('Subaward Date')},{_k1(txc, r)})"
def _e_last(txc):    return lambda r: f"=_xlfn.MAXIFS({txc('Subaward Date')},{_k1(txc, r)})"
def _e_span(r):      return f"=(${B1_LAST}{r}-${B1_FIRST}{r})/365.25"


def _e_block(r):
    return f'=IFERROR(INDEX({_PA_BLK},MATCH(${B1_PIID}{r},{_PA_PIID},0)),"-")'


def _e_cov(r):
    m = f"MATCH(${B1_PIID}{r},{_PA_PIID},0)"
    span_days = f"(${B1_LAST}{r}-${B1_FIRST}{r})"
    pop_days = f"(INDEX({_PA_END},{m})-INDEX({_PA_START},{m}))"
    return f'=IFERROR({span_days}/{pop_days},"")'


# §2 (vendor) live cells - 3-way additive (a UEI can span programs) -----------------------
def _f2_reports(r): return _sum3(lambda t: f"COUNTIFS({_k2(t, r)})")
def _f2_corr(r):    return _sum3(lambda t: f'COUNTIFS({_k2(t, r)},{t("Subaward Amount $")},"<0")')
def _f2_net(r):     return "=(" + "+".join(f"SUMIFS({t(TX_REAL)},{_k2(t, r)})" for t in _TXS) + ")/1000000"
def _f2_span(r):    return _multi_leaf_span(_k2, r)


# --- headers ----------------------------------------------------------------------------
# §3 engagement (native table, B..Q)
_ENG_HEADERS = ["Subawardee UEI", "Subawardee Vendor Name", "PIID-Subaward Pairs",
                "Breadth Tier", "Activity Span (Yrs)", "Duration Tier",
                "Observed Activity Profile", "Net Subaward $M", "Reports",
                "Neg. Adjustments", "Program", "Prime PIID", "Block / MYP",
                "Span / Prime PoP", "First Action", "Last Action"]
_ENG_CENTER = {"PIID-Subaward Pairs", "Breadth Tier", "Activity Span (Yrs)",
               "Duration Tier", "Net Subaward $M", "Reports", "Neg. Adjustments",
               "Span / Prime PoP", "First Action", "Last Action"}
_ENG_STYLES = [S_TEXT_INPUT, S_DEFAULT, S_INT, S_INT, S_NUM, S_INT, S_DEFAULT, S_NUM,
               S_LINK_INT, S_LINK_INT, S_DEFAULT, S_TEXT_INPUT, S_DEFAULT, S_PCT,
               S_DATE_LINK, S_DATE_LINK]

# §2 vendor rollup (native table, B..M)
_ROLL_HEADERS = ["Subawardee UEI", "Subawardee Vendor Name", "Distinct Subaward Numbers",
                 "Breadth Tier", "Portfolio Span (Yrs)", "Duration Tier",
                 "Observed Activity Profile", "Net Subaward $M", "Reports",
                 "Neg. Adjustments", "Distinct PIIDs", "Distinct Programs"]
_ROLL_CENTER = {"Distinct Subaward Numbers", "Breadth Tier", "Portfolio Span (Yrs)",
                "Duration Tier", "Net Subaward $M", "Reports", "Neg. Adjustments",
                "Distinct PIIDs", "Distinct Programs"}
_ROLL_STYLES = [S_TEXT_INPUT, S_DEFAULT, S_INT, S_INT, S_NUM, S_INT, S_DEFAULT, S_NUM,
                S_LINK_INT, S_LINK_INT, S_INT, S_INT]

# §1 activity profile summary (styled block, starts at column C)
_TYPE_HEADERS = ["Observed Activity Profile", "# Vendors", "% of Vendors", "Net Subaward $M",
                 "% of Portfolio $", "Avg Span (Yrs)"]
_TYPE_CENTER = {"# Vendors", "% of Vendors", "Net Subaward $M", "% of Portfolio $",
                "Avg Span (Yrs)"}
_TYPE_STYLES = [S_DEFAULT, S_INT, S_PCT, S_NUM, S_PCT, S_NUM]

# §1b breadth x duration matrix (styled block, starts at column C; counts vendors over §2)
_MTX_HEADERS = ["Breadth \\ Duration", "Dur 0 (none)", "Dur 1 (<2y)", "Dur 2 (2-<6y)",
                "Dur 3 (>=6y)", "All"]
_MTX_CENTER = {"Dur 0 (none)", "Dur 1 (<2y)", "Dur 2 (2-<6y)", "Dur 3 (>=6y)", "All"}
_MTX_ROWS = ["Breadth 0 (1 sub)", "Breadth 1 (2-3)", "Breadth 2 (4-9)", "Breadth 3 (10+)"]
_MTX_STYLES = [S_DEFAULT, S_INT, S_INT, S_INT, S_INT, S_INT]

# §4 activity by block (styled block, starts at column C) - first-observed / reactivated / continued
_BLK_HEADERS = ["Block / MYP", "Compared with", "# Vendors", "First observed", "Reactivated",
                "Continued from prior", "Continuation %", "Prior-block retention", "# Engagements",
                "PIID-Subaward Pairs", "Net Subaward $M", "$ to continued", "Continued $ %",
                "% of Portfolio $"]
_BLK_CENTER = {"# Vendors", "First observed", "Reactivated", "Continued from prior",
               "Continuation %", "Prior-block retention", "# Engagements", "PIID-Subaward Pairs",
               "Net Subaward $M", "$ to continued", "Continued $ %", "% of Portfolio $"}
_BLK_STYLES = [S_DEFAULT, S_DEFAULT, S_INT, S_INT, S_INT, S_INT, S_PCT, S_PCT, S_INT, S_INT,
               S_NUM, S_NUM, S_PCT, S_PCT]

INTRO = (
    "Historical supplier breadth and observed duration on reported "
    "new-construction subawards."
)
CAV1 = (
    "Profile = the higher of breadth tier and duration tier; "
    "it is not an annual retention measure."
)
CAV2 = (
    "Activity span is report-date based; FFATA does not provide "
    "contractual period of performance."
)
MTX_CAP = (
    "Breadth tiers use distinct subawards; duration tiers use observed action span."
)
BLK_CAP = (
    "Later blocks are right-censored. Reactivated means seen earlier, "
    "but not in the immediately prior block."
)


def _block_order() -> list[str]:
    """Distinct Block/MYP labels in Prime-Awards (program, PIID) order."""
    headers, rows = load_table("prime_awards")
    j = headers.index("Block / MYP")
    seen, out = set(), []
    for r in rows:
        b = r[j] if j < len(r) else ""
        if b and b not in seen:
            seen.add(b)
            out.append(b)
    return out


def _make_subaward_activity() -> tuple[SheetEntry, dict]:
    act_h, act_rows = load_table("subaward_activity")
    roll_h, roll_rows = load_table("subaward_vendor_rollup")
    blocks = _block_order()
    ai = {h: i for i, h in enumerate(act_h)}
    ri = {h: i for i, h in enumerate(roll_h)}
    n_types, n_blocks, n_mtx = len(_PROFILE_LABELS), len(blocks), len(_MTX_ROWS)
    n_roll, n_act = len(roll_rows), len(act_rows)

    # --- Pass 1: compute every section's rows up front, so cross-section formulas (§1->§2,
    # §4->§3) can reference real ranges before the rows are emitted. `rr` tracks the NEXT free
    # row, mirroring RowCursor exactly (one +1 per emitted row, +n per blank(n)). Physical
    # order top-to-bottom: §1 profile, §2 rollup, §3 engagement, §4 block. ------------------
    rr = 2                      # next free row
    rr += 1                     # title banner (row 2)
    rr += 1                     # intro
    rr += 1                     # caveat 1
    rr += 1                     # caveat 2
    rr += 2                     # blank(2)
    type_banner = rr; rr += 1
    type_header = rr; rr += 1
    type_first = rr; rr += n_types
    type_last = type_first + n_types - 1
    type_total = rr; rr += 1
    rr += 2
    mtx_banner = rr; rr += 1
    mtx_cap = rr; rr += 1
    mtx_header = rr; rr += 1
    mtx_first = rr; rr += n_mtx
    mtx_last = mtx_first + n_mtx - 1
    mtx_total = rr; rr += 1
    rr += 2
    roll_banner = rr; rr += 1
    roll_header = rr; rr += 1
    roll_first = rr; rr += n_roll
    roll_last = roll_first + n_roll - 1
    rr += 2
    eng_banner = rr; rr += 1
    eng_header = rr; rr += 1
    eng_first = rr; rr += n_act
    eng_last = eng_first + n_act - 1
    rr += 2
    blk_banner = rr; rr += 1
    blk_caption = rr; rr += 1
    blk_header = rr; rr += 1
    blk_first = rr; rr += n_blocks
    blk_last = blk_first + n_blocks - 1
    blk_total = rr; rr += 1

    # §2 rollup ranges used by §1 profile summary (absolute, same sheet)
    RP_PROFILE = f"${B_PROFILE}${roll_first}:${B_PROFILE}${roll_last}"
    RP_UEI = f"${B_UEI}${roll_first}:${B_UEI}${roll_last}"
    RP_NET = f"${B_NET}${roll_first}:${B_NET}${roll_last}"
    RP_SPAN = f"${B_SPAN}${roll_first}:${B_SPAN}${roll_last}"
    RP_BTIER = f"${B_BTIER}${roll_first}:${B_BTIER}${roll_last}"   # §2 col E (breadth tier)
    RP_DTIER = f"${B_DTIER}${roll_first}:${B_DTIER}${roll_last}"   # §2 col G (duration tier)
    # §3 engagement ranges used by §4 block
    RE_BLK = f"${B1_BLK}${eng_first}:${B1_BLK}${eng_last}"
    RE_UEI = f"${B_UEI}${eng_first}:${B_UEI}${eng_last}"
    RE_DSUB = f"${B_DSUB}${eng_first}:${B_DSUB}${eng_last}"
    RE_NET = f"${B_NET}${eng_first}:${B_NET}${eng_last}"
    # row of each block (for §4 Retention %'s predecessor lookup)
    block_row = {blk: blk_first + i for i, blk in enumerate(blocks)}

    def render() -> WorksheetSpec:
        c = RowCursor(2)
        assert c.at() == 2
        c.title(TAB_SUBAWARD_ACTIVITY, _NCOLS)
        c.caption(INTRO)
        c.write([CAV1], styles=[S_ITALIC])
        c.write([CAV2], styles=[S_ITALIC])
        c.blank(2)

        # §1 Activity profile (styled block, indented to col C so labels don't clip) ---------
        assert c.at() == type_banner
        c.section("§1 - Historical activity intensity", _NCOLS)
        assert c.at() == type_header
        c.write(_TYPE_HEADERS, styles=header_styles(_TYPE_HEADERS, center_headers=_TYPE_CENTER),
                start_col=2)
        for lab in _PROFILE_LABELS:
            c.write([
                lab,
                f'=COUNTIF({RP_PROFILE},"{lab}")',
                lambda r: f"=D{r}/COUNTA({RP_UEI})",
                f'=SUMIF({RP_PROFILE},"{lab}",{RP_NET})',
                lambda r: f"=F{r}/SUM({RP_NET})",
                f'=IFERROR(AVERAGEIF({RP_PROFILE},"{lab}",{RP_SPAN}),"")',
            ], styles=_TYPE_STYLES, start_col=2)
        assert c.at() == type_total
        c.total(["Total", f"=SUM(D{type_first}:D{type_last})",
                 f"=SUM(E{type_first}:E{type_last})", f"=SUM(F{type_first}:F{type_last})",
                 f"=SUM(G{type_first}:G{type_last})", None],
                styles=[S_BOLD, S_INT, S_PCT, S_NUM, S_PCT, S_NUM], n_cols=6, start_col=2)
        c.blank(2)

        # §1b Breadth x Duration matrix (styled block; vendor counts over §2, b rows x d cols) -
        assert c.at() == mtx_banner
        c.section("§1b - Breadth x Duration matrix (vendor counts by tier)", _NCOLS)
        assert c.at() == mtx_cap
        c.write([MTX_CAP], styles=[S_ITALIC])
        assert c.at() == mtx_header
        c.write(_MTX_HEADERS, styles=header_styles(_MTX_HEADERS, center_headers=_MTX_CENTER),
                start_col=2)
        for b, lab in enumerate(_MTX_ROWS):
            c.write([
                lab,
                *[f"=COUNTIFS({RP_BTIER},{b},{RP_DTIER},{d})" for d in range(4)],
                lambda r: f"=SUM(D{r}:G{r})",
            ], styles=_MTX_STYLES, start_col=2)
        assert c.at() == mtx_total
        c.total(["All", f"=SUM(D{mtx_first}:D{mtx_last})", f"=SUM(E{mtx_first}:E{mtx_last})",
                 f"=SUM(F{mtx_first}:F{mtx_last})", f"=SUM(G{mtx_first}:G{mtx_last})",
                 f"=SUM(H{mtx_first}:H{mtx_last})"],
                styles=[S_BOLD] + _MTX_STYLES[1:], n_cols=6, start_col=2)
        c.blank(2)

        # §2 Vendor rollup (native table) -------------------------------------------------
        assert c.at() == roll_banner
        c.section("§2 - Vendor rollup: recurrence per supplier", _NCOLS)
        assert c.at() == roll_header
        c.write(_ROLL_HEADERS, styles=header_styles(_ROLL_HEADERS, center_headers=_ROLL_CENTER))
        for v in roll_rows:
            c.write([
                v[ri["Subawardee UEI"]],
                v[ri["Subawardee Vendor Name"]],
                as_int(v[ri["Distinct Subaward Numbers"]]),
                _f_btier, _f2_span, _f_dtier, _f_profile,
                _f2_net, _f2_reports, _f2_corr,
                as_int(v[ri["Distinct PIIDs"]]),
                as_int(v[ri["Distinct Programs"]]),
            ], styles=_ROLL_STYLES)
        c.blank(2)

        # §3 Engagement detail (native table) ---------------------------------------------
        assert c.at() == eng_banner
        c.section("§3 - Engagement detail: per supplier x prime contract", _NCOLS)
        assert c.at() == eng_header
        c.write(_ENG_HEADERS, styles=header_styles(_ENG_HEADERS, center_headers=_ENG_CENTER))
        for a in act_rows:
            txc = PROG_TX[a[ai["Program"]]]
            c.write([
                a[ai["Subawardee UEI"]],
                a[ai["Subawardee Vendor Name"]],
                as_int(a[ai["Distinct Subaward Numbers"]]),
                _f_btier, _e_span, _f_dtier, _f_profile,
                _e_net(txc), _e_reports(txc), _e_corr(txc),
                a[ai["Program"]],
                a[ai["Prime PIID"]],
                _e_block, _e_cov, _e_first(txc), _e_last(txc),
            ], styles=_ENG_STYLES)
        c.blank(2)

        # §4 Activity by block / MYP - first-observed / reactivated / continued (live over §3) -
        assert c.at() == blk_banner
        c.section("§4 - Activity by block / MYP: churn vs continuity", _NCOLS)
        assert c.at() == blk_caption
        c.write([BLK_CAP], styles=[S_ITALIC])
        assert c.at() == blk_header
        c.write(_BLK_HEADERS, styles=header_styles(_BLK_HEADERS, center_headers=_BLK_CENTER),
                start_col=2)
        _distinct = f"COUNTIFS({RE_UEI},{RE_UEI},{RE_BLK},{RE_BLK})"
        for blk in blocks:
            pred = _BLOCK_PRED.get(blk, "")
            has_pred = bool(pred)
            earlier = _earlier_blocks(blk)
            in_pred = f'(COUNTIFS({RE_UEI},{RE_UEI},{RE_BLK},"{pred}")>0)'
            # per-UEI "appears in ANY strictly-earlier block" (0/1, constant within a UEI)
            _terms = "+".join(f'COUNTIFS({RE_UEI},{RE_UEI},{RE_BLK},"{lab}")' for lab in earlier)
            in_any = f"(({_terms})>0)" if earlier else "0"
            c.write([
                blk,                                                                  # C Block / MYP
                (pred if has_pred else "-"),                                          # D Compared with
                f'=SUMPRODUCT(({RE_BLK}="{blk}")/{_distinct})',                       # E # Vendors
                ((lambda r: f"=E{r}-G{r}-H{r}") if has_pred                           # F First observed
                    else (lambda r: f"=E{r}")),
                (f'=SUMPRODUCT(({RE_BLK}="{blk}")*{in_any}*(1-{in_pred})/{_distinct})'
                    if has_pred else "-"),                                            # G Reactivated
                (f'=SUMPRODUCT(({RE_BLK}="{blk}")*{in_pred}/{_distinct})'
                    if has_pred else "-"),                                            # H Continued from prior
                ((lambda r: f"=H{r}/E{r}") if has_pred else "-"),                     # I Continuation %
                ((lambda r, pr=block_row[pred]: f"=H{r}/E{pr}")                       # J Prior-block retention
                    if has_pred else "-"),
                f'=COUNTIF({RE_BLK},"{blk}")',                                        # K # Engagements
                f'=SUMIF({RE_BLK},"{blk}",{RE_DSUB})',                                # L PIID-Subaward Pairs
                f'=SUMIF({RE_BLK},"{blk}",{RE_NET})',                                 # M Net Subaward $M
                (f'=SUMPRODUCT(({RE_BLK}="{blk}")*{in_pred}*{RE_NET})'
                    if has_pred else "-"),                                            # N $ to continued
                ((lambda r: f"=N{r}/M{r}") if has_pred else "-"),                     # O Continued $ %
                (lambda r: f"=M{r}/SUM({RE_NET})"),                                   # P % of Portfolio $
            ], styles=_BLK_STYLES, start_col=2)
        assert c.at() == blk_total
        c.total(["Sum of block observations", None,
                 f"=SUM(E{blk_first}:E{blk_last})", f"=SUM(F{blk_first}:F{blk_last})",
                 f"=SUM(G{blk_first}:G{blk_last})", f"=SUM(H{blk_first}:H{blk_last})",
                 None, None,
                 f"=SUM(K{blk_first}:K{blk_last})", f"=SUM(L{blk_first}:L{blk_last})",
                 f"=SUM(M{blk_first}:M{blk_last})", f"=SUM(N{blk_first}:N{blk_last})",
                 None, f"=SUM(P{blk_first}:P{blk_last})"],
                styles=[S_BOLD] + _BLK_STYLES[1:], n_cols=14, start_col=2)

        ws = worksheet(c.rows, cols=_WIDTHS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        # Two native sortable tables on one worksheet (the packager assigns global table ids
        # and injects both <tablePart>s); §1/§4 are styled blocks, not tables.
        t_roll = ExcelTable(name="SubawardVendorRollup",
                            ref=f"B{roll_header}:{col_letter(len(_ROLL_HEADERS))}{roll_last}",
                            headers=_ROLL_HEADERS)
        t_eng = ExcelTable(name="SubawardActivity",
                           ref=f"B{eng_header}:{col_letter(len(_ENG_HEADERS))}{eng_last}",
                           headers=_ENG_HEADERS)
        return WorksheetSpec(ws, tables=[t_roll, t_eng])

    refs = {
        "type_first": type_first, "type_last": type_last,
        "roll_first": roll_first, "roll_last": roll_last,
        "block_first": blk_first, "block_last": blk_last,
    }
    return SheetEntry(TAB_SUBAWARD_ACTIVITY, _GROUP, render), refs


def _sheet_range(letter: str, first: int, last: int) -> str:
    return f"'{TAB_SUBAWARD_ACTIVITY}'!${letter}${first}:${letter}${last}"


def subaward_activity_rollup_range(header: str) -> str:
    """Absolute §2 vendor-rollup range for a visible table header."""
    if header not in _ROLL_HEADERS:
        raise KeyError(header)
    letter = col_letter(_ROLL_HEADERS.index(header) + 1)   # §2 starts in column B
    return _sheet_range(letter, _ACTIVITY_REFS["roll_first"], _ACTIVITY_REFS["roll_last"])


def subaward_activity_profile_cell(label: str, header: str) -> str:
    """Absolute §1 activity-profile cell by profile label and visible header."""
    if label not in _PROFILE_LABELS:
        raise KeyError(label)
    if header not in _TYPE_HEADERS:
        raise KeyError(header)
    row = _ACTIVITY_REFS["type_first"] + _PROFILE_LABELS.index(label)
    letter = col_letter(_TYPE_HEADERS.index(header) + 2)   # §1 starts in column C
    return f"'{TAB_SUBAWARD_ACTIVITY}'!${letter}${row}"


def subaward_activity_block_range(header: str) -> str:
    """Absolute §4 block-summary range for a visible header."""
    if header not in _BLK_HEADERS:
        raise KeyError(header)
    letter = col_letter(_BLK_HEADERS.index(header) + 2)   # §4 starts in column C
    return _sheet_range(letter, _ACTIVITY_REFS["block_first"], _ACTIVITY_REFS["block_last"])


SUBAWARD_ACTIVITY, _ACTIVITY_REFS = _make_subaward_activity()
