"""executive_summary - the front-door dashboard tab.

The first sheet: orients a cold reader and carries the headline numbers, all as LIVE
formulas off the model / summary sheets (so they never drift). Seven blocks:

  - Purpose + scope (static intro).
  - §1 Scope & how to read these figures (the denominator caveat - what is and isn't
    counted, and why submarine shares are NOT total-boat-construction shares).
  - §2 Program totals (live per-program roll-up: UEIs, $M FY2026$, transactions, span,
    foreign share).
  - §3 Supplier-concentration headlines: the most concentrated material domain per program,
    parent-collapse threshold crossings, and the share of dollars in highly concentrated domains.
  - §4 Vendor-activity headlines: recurring-core vs one-time tail, multi-program reach and duration.
  - §5 / §6 Capability Domain and Primary Output mix by fiscal year - one matrix each,
    the three programs side by side (FY2022-FY2025), body = each archetype's % of that
    program-FY's reported first-tier subaward $ (constant FY2026$); the bottom row gives
    the absolute $M so a reader sees mix and magnitude together.
  - §7 DDG SWBS mix by FY (HII-Ingalls only).

Cells reference the program-vendor sheets' per-FY and archetype columns via their
promoted cols accessors (ddg_pv_cols / virginia_pv_cols / columbia_pv_cols), the same
way those sheets reference the tx leaf. Carries no native table (a legend/dashboard).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_PCT, S_INT, S_DATE,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_classification_refactor.sheets._layout import RowCursor
from workbook_award_classification_refactor.sheets._italic import S_ITALIC
from workbook_award_classification_refactor.sheets._tabs import TAB_EXEC_SUMMARY
from workbook_award_classification_refactor.sheets._taxonomy import (
    DOMAINS, OUTPUTS, SWBS_GROUPS,
)
from workbook_award_classification_refactor.sheets.ddg_program_vendors import ddg_pv_cols
from workbook_award_classification_refactor.sheets.virginia_program_vendors import (
    virginia_pv_cols,
)
from workbook_award_classification_refactor.sheets.columbia_program_vendors import (
    columbia_pv_cols,
)
from workbook_award_classification_refactor.sheets.ddg_swbs_rollup import swbs_rollup_cols
from workbook_award_classification_refactor.sheets.domain_concentration import domain_conc_range
from workbook_award_classification_refactor.sheets.subaward_activity import (
    subaward_activity_profile_cell, subaward_activity_rollup_range,
)

_GROUP = "summary"

# Programs, side by side, in the user's order. (display name, cols accessor)
PROGRAMS = [
    ("Virginia", virginia_pv_cols),
    ("Columbia", columbia_pv_cols),
    ("DDG-51", ddg_pv_cols),
]
# (column label, the per-FY header on the program-vendor sheet)
FYS = [("FY22", "FY22 $M"), ("FY23", "FY23 $M"),
       ("FY24", "FY24 $M"), ("FY25", "FY25 $M")]

# B label + 3 programs x 4 FY = 13 content columns (gutter A added by worksheet()).
_NCOLS = 1 + len(PROGRAMS) * len(FYS)
_COLS = [44] + [10] * (_NCOLS - 1)

INTRO = ("Reported hull-builder first-tier subawards for DDG-51, Virginia and Columbia; "
         "constant FY2026$.")

CAVEATS = [
    "Reported first-tier subawards under the hull-construction primes (GDEB for Virginia and "
    "Columbia, Bath Iron Works and Ingalls for DDG-51); constant FY2026$ (Green Book Procurement "
    "deflator). GFE and MIB / BlueForge accounts are excluded.",
    "Submarine shares are percentages of GDEB-reported subcontracted scope, not of total boat "
    "construction; the HII-Newport News co-build workshare is largely outside the reported subaward "
    "data (about $98M visible against tens of billions - see Market Bridge).",
    "Read a domain's mix with both operating-entity and ultimate-parent concentration "
    "(Domain Concentration, including its Parent columns).",
]


def _headline(c: RowCursor) -> None:
    """§2 - one live row per program."""
    c.write(["Program", "Subawardee UEIs", "Subaward $M (FY26$)", "Transactions",
             "Earliest", "Latest", "Foreign-maj. UEIs %"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 6)
    for name, cols in PROGRAMS:
        uei = cols("Subawardee UEI")
        pop = cols("Predominant Place of Performance (by records)")
        c.write([
            name,
            f"=COUNTA({uei})",
            f'=SUM({cols("Subaward $M")})',
            f'=SUM({cols("Published Subaward Records")})',
            f'=MIN({cols("First Subaward")})',
            f'=MAX({cols("Last Subaward")})',
            f'=IFERROR(COUNTIF({pop},"Foreign")/COUNTA({uei}),"")',
        ], styles=[S_DEFAULT, S_INT, S_NUM, S_INT, S_DATE, S_DATE, S_PCT])
    c.write(['"Foreign-maj. UEIs %" = share of subawardee UEIs whose record-majority place of '
             "performance is foreign (an entity-count ratio), not a share of dollars."],
            styles=[S_ITALIC])


def _concentration_headlines(c: RowCursor) -> None:
    """Answer-first concentration cut. 'Material' means at least 5% of program net $."""
    headers = [
        "Most concentrated material domain / Top-1 firm", "Domain share", "UEI Top-1",
        "Parent Top-1", "Highly-conc. $ share", "Parent threshold crossings", "Status",
    ]
    c.write(headers, styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(headers) - 1))
    for name, _cols in PROGRAMS:
        labels = domain_conc_range(name, "")
        share = domain_conc_range(name, "Share")
        dollar = domain_conc_range(name, "$M (FY26$)")
        firms = domain_conc_range(name, "Top-1 firm")
        top1 = domain_conc_range(name, "Top-1 share")
        contest = domain_conc_range(name, "Contestability")
        ptop1 = domain_conc_range(name, "Parent Top-1 %")
        max_material = f'_xlfn.MAXIFS({top1},{share},">=0.05")'
        match = f'MATCH(1,INDEX(({top1}={max_material})*({share}>=0.05),0),0)'
        c.write([
            f'=IFERROR("{name}: "&INDEX({labels},{match})&" - "&INDEX({firms},{match}),"{name}")',
            f'=IFERROR(INDEX({share},{match}),"")',
            f'=IFERROR({max_material},"")',
            f'=IFERROR(INDEX({ptop1},{match}),"")',
            f'=IF(COUNTIF({contest},"Check")>0,"",IFERROR('
            f'SUMIFS({dollar},{contest},"Highly concentrated")/SUM({dollar}),""))',
            f'=COUNTIFS({ptop1},">=0.6",{top1},"<0.6",{share},">=0.05")',
            f'=IF(COUNTIF({contest},"Check")>0,"CHECK","OK")',
        ], styles=[S_DEFAULT, S_PCT, S_PCT, S_PCT, S_PCT, S_INT, S_BOLD])
    c.write([
        "Material-domain screen = at least 5% of program net reported subaward $. "
        "Concentration ratios use positive spend; 'Highly-concentrated $ share' uses net domain $. "
        "Threshold crossings count material domains whose parent Top-1 is at least 60% while the "
        "largest operating UEI remains below 60%.",
    ], styles=[S_ITALIC])


def _activity_headlines(c: RowCursor) -> None:
    """Portfolio-wide supplier recurrence / persistence takeaways, live off Subaward Activity."""
    uei = subaward_activity_rollup_range("Subawardee UEI")
    net = subaward_activity_rollup_range("Net Subaward $M")
    programs = subaward_activity_rollup_range("Distinct Programs")
    duration = subaward_activity_rollup_range("Duration Tier")
    reports = subaward_activity_rollup_range("Reports")
    distinct = subaward_activity_rollup_range("Distinct Subaward Numbers")
    neg = subaward_activity_rollup_range("Neg. Adjustments")

    c.write(["Cohort", "% of vendors", "% of portfolio $"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    for label in ("High / sustained activity", "Single / one-time"):
        c.write([
            label,
            f'={subaward_activity_profile_cell(label, "% of Vendors")}',
            f'={subaward_activity_profile_cell(label, "% of Portfolio $")}',
        ], styles=[S_DEFAULT, S_PCT, S_PCT])
    c.write([
        "Multi-program suppliers",
        f'=IFERROR(COUNTIF({programs},">1")/COUNTA({uei}),"")',
        f'=IFERROR(SUMIFS({net},{programs},">1")/SUM({net}),"")',
    ], styles=[S_DEFAULT, S_PCT, S_PCT])
    c.write([
        "Long-duration activity (>=6 years)",
        f'=IFERROR(COUNTIF({duration},3)/COUNTA({uei}),"")',
        f'=IFERROR(SUMIFS({net},{duration},3)/SUM({net}),"")',
    ], styles=[S_DEFAULT, S_PCT, S_PCT])
    c.write(["Reports per distinct subaward number",
             f'=IFERROR(SUM({reports})/SUM({distinct}),"")'],
            styles=[S_ITALIC, S_NUM])
    c.write(["Negative adjustment rows / reports",
             f'=IFERROR(SUM({neg})/SUM({reports}),"")'],
            styles=[S_ITALIC, S_PCT])
    c.write([
        "Activity tiers are analyst-defined reporting-pattern descriptors. Duration is first-to-last "
        "reported action and therefore a lower bound; see Subaward Activity for the breadth x duration "
        "matrix, vendor detail and block continuity.",
    ], styles=[S_ITALIC])


def _matrix(c: RowCursor, axis_header: str, codes: list[tuple[str, str, str]]) -> None:
    """A mix-by-FY matrix: archetype rows x (program x FY) columns. Body cells = the
    archetype's share of that program-FY's reported subaward $; bottom row = the $M total
    that is the share denominator. `codes` = (code, name, definition) tuples."""
    # group header (program name at each block's first column) + FY sub-header
    grp, gsty = [""], [S_DEFAULT]
    fy, fsty = [""], [S_DEFAULT]
    for name, _cols in PROGRAMS:
        grp += [name] + [""] * (len(FYS) - 1)
        gsty += [S_BOLD] + [S_DEFAULT] * (len(FYS) - 1)
        fy += [lbl for lbl, _h in FYS]
        fsty += [S_HEADER_CENTER] * len(FYS)
    c.write(grp, styles=gsty)
    c.write(fy, styles=fsty)
    # body: one row per archetype code
    for code, name, _defn in codes:
        vals, sty = [f"{code}  {name}"], [S_DEFAULT]
        for _name, cols in PROGRAMS:
            axis = cols(axis_header)
            for _lbl, fyh in FYS:
                fyr = cols(fyh)
                vals.append(f'=IFERROR(SUMIFS({fyr},{axis},"{code}")/SUM({fyr}),"")')
                sty.append(S_PCT)
        c.write(vals, styles=sty)
    # total $M (FY2026$) row - the per-program-FY denominator, as a bordered divider
    tvals, tsty = ["Total $M (FY26$)"], [S_BOLD]
    for _name, cols in PROGRAMS:
        for _lbl, fyh in FYS:
            tvals.append(f"=SUM({cols(fyh)})")
            tsty.append(S_NUM)
    c.total(tvals, styles=tsty, n_cols=_NCOLS)


def _swbs_matrix(c: RowCursor) -> None:
    """§5 - DDG SWBS mix by FY: one DDG block (subs carry no SWBS). Rows = SWBS major
    groups (+U00); cells = the group's share of HII-Ingalls DDG reported subaward $ for the
    FY, off the per-subsystem roll-up rolled to major group. Columns sum to 100% incl. U00."""
    n = 1 + len(FYS)   # B label + FY22..FY25
    grp = swbs_rollup_cols("SWBS Major Group")
    c.write([""] + [lbl for lbl, _h in FYS],
            styles=[S_DEFAULT] + [S_HEADER_CENTER] * len(FYS))
    for code, name, _ex in SWBS_GROUPS:
        vals, sty = [f"{code}  {name}"], [S_DEFAULT]
        for _lbl, fyh in FYS:
            fyr = swbs_rollup_cols(fyh)
            vals.append(f'=IFERROR(SUMIFS({fyr},{grp},"{code}")/SUM({fyr}),"")')
            sty.append(S_PCT)
        c.write(vals, styles=sty)
    tvals, tsty = ["Total $M (FY26$)"], [S_BOLD]
    for _lbl, fyh in FYS:
        tvals.append(f"=SUM({swbs_rollup_cols(fyh)})")
        tsty.append(S_NUM)
    c.total(tvals, styles=tsty, n_cols=n)
    sm = swbs_rollup_cols("Subaward $M")
    c.write(["SWBS coverage (HII-Ingalls DDG $ mapped)",
             f'=IFERROR(1-SUMIFS({sm},{grp},"U00")/SUM({sm}),"")'],
            styles=[S_ITALIC, S_PCT])


def _make_exec_summary():
    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.title(TAB_EXEC_SUMMARY, _NCOLS)
        c.caption(INTRO)
        c.blank(2)

        c.section("§1 - Scope & how to read these figures", _NCOLS)
        for line in CAVEATS:
            c.write([line], styles=[S_DEFAULT])
        c.blank(2)

        c.section("§2 - Program totals (lifetime, constant FY2026$)", _NCOLS)
        _headline(c)
        c.blank(2)

        c.section("§3 - Supplier concentration headlines", _NCOLS)
        _concentration_headlines(c)
        c.blank(2)

        c.section("§4 - Supplier activity & recurrence headlines", _NCOLS)
        _activity_headlines(c)
        c.blank(2)

        c.section("§5 - Capability Domain mix by fiscal year", _NCOLS)
        c.write(["Each cell = that domain's share of the program's reported first-tier subaward $ "
                 "for the fiscal year (constant FY2026$); columns sum to 100%. Window: FY2022-FY2025 "
                 "(pre-FY22 and partial FY26 are excluded from this mix; lifetime totals are in §2)."],
                styles=[S_ITALIC])
        _matrix(c, "Capability Domain Archetype (D)", DOMAINS)
        c.blank(2)

        c.section("§6 - Primary Output mix by fiscal year", _NCOLS)
        c.write(["Each cell = that output's share of the program's reported first-tier subaward $ "
                 "for the fiscal year (constant FY2026$); columns sum to 100%. Window: FY2022-FY2025 "
                 "(pre-FY22 and partial FY26 are excluded from this mix; lifetime totals are in §2)."],
                styles=[S_ITALIC])
        _matrix(c, "Primary Output Archetype (P)", OUTPUTS)
        c.blank(2)

        c.section("§7 - DDG SWBS mix by FY", _NCOLS)
        c.write(["DDG-51 HII-Ingalls only (the SWBS-eligible builder), transaction-grain. Each cell = "
                 "that ship-system group's share of HII-Ingalls DDG reported subaward $ for the fiscal "
                 "year (constant FY2026$); columns sum to 100% incl. U00 unmapped. Denominator differs "
                 "from §5/§6, which include GD-BIW."],
                styles=[S_ITALIC])
        _swbs_matrix(c)

        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_EXEC_SUMMARY, _GROUP, render)


EXECUTIVE_SUMMARY = _make_exec_summary()
