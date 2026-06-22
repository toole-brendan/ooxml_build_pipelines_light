"""executive_summary - the front-door dashboard tab.

The first sheet: orients a cold reader and carries the headline numbers, all as LIVE
formulas off the three program-vendor sheets (so they never drift). Four blocks:

  - Purpose + scope (static intro).
  - §1 Scope & how to read these figures (the denominator caveat - what is and isn't
    counted, and why submarine shares are NOT total-boat-construction shares).
  - §2 Program totals (live per-program roll-up: UEIs, $M FY2026$, transactions, span,
    foreign share).
  - §3 / §4 Capability Domain and Primary Output mix by fiscal year - one matrix each,
    the three programs side by side (FY2022-FY2025), body = each archetype's % of that
    program-FY's reported first-tier subaward $ (constant FY2026$); the bottom row gives
    the absolute $M so a reader sees mix and magnitude together.

Cells reference the program-vendor sheets' per-FY and archetype columns via their
promoted cols accessors (ddg_pv_cols / virginia_pv_cols / columbia_pv_cols), the same
way those sheets reference the tx leaf. Carries no native table (a legend/dashboard).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_TITLE_SHEET, S_TITLE_SECTION, S_NUM, S_PCT, S_INT, S_DATE,
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
    "data (about $98M visible against tens of billions - see HII Co-Build Workshare).",
    "Read a domain's mix with its supplier concentration (Domain Concentration).",
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
        ], styles=[S_DEFAULT, S_INT, S_NUM, S_INT, S_DATE, S_DATE, S_PCT],
            outline_level=1)
    c.write(['"Foreign-maj. UEIs %" = share of subawardee UEIs whose record-majority place of '
             "performance is foreign (an entity-count ratio), not a share of dollars."],
            styles=[S_ITALIC], outline_level=1)


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
        c.write(vals, styles=sty, outline_level=1)
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
        c.write(vals, styles=sty, outline_level=1)
    tvals, tsty = ["Total $M (FY26$)"], [S_BOLD]
    for _lbl, fyh in FYS:
        tvals.append(f"=SUM({swbs_rollup_cols(fyh)})")
        tsty.append(S_NUM)
    c.total(tvals, styles=tsty, n_cols=n)
    sm = swbs_rollup_cols("Subaward $M")
    c.write(["SWBS coverage (HII-Ingalls DDG $ mapped)",
             f'=IFERROR(1-SUMIFS({sm},{grp},"U00")/SUM({sm}),"")'],
            styles=[S_ITALIC, S_PCT], outline_level=1)


def _make_exec_summary():
    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.banner(TAB_EXEC_SUMMARY, n_cols=_NCOLS, style=S_TITLE_SHEET)
        c.write([INTRO], styles=[S_ITALIC])
        c.blank(2)

        c.banner("§1 - Scope & how to read these figures",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        for line in CAVEATS:
            c.write([line], styles=[S_DEFAULT], outline_level=1)
        c.blank(2)

        c.banner("§2 - Program totals (lifetime, constant FY2026$)",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        _headline(c)
        c.blank(2)

        c.banner("§3 - Capability Domain mix by fiscal year",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.write(["Each cell = that domain's share of the program's reported first-tier subaward $ "
                 "for the fiscal year (constant FY2026$); columns sum to 100%. Window: FY2022-FY2025 "
                 "(pre-FY22 and partial FY26 are excluded from this mix; lifetime totals are in §2)."],
                styles=[S_ITALIC], outline_level=1)
        _matrix(c, "Capability Domain Archetype (D)", DOMAINS)
        c.blank(2)

        c.banner("§4 - Primary Output mix by fiscal year",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.write(["Each cell = that output's share of the program's reported first-tier subaward $ "
                 "for the fiscal year (constant FY2026$); columns sum to 100%. Window: FY2022-FY2025 "
                 "(pre-FY22 and partial FY26 are excluded from this mix; lifetime totals are in §2)."],
                styles=[S_ITALIC], outline_level=1)
        _matrix(c, "Primary Output Archetype (P)", OUTPUTS)
        c.blank(2)

        c.banner("§5 - DDG SWBS mix by FY",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.write(["DDG-51 HII-Ingalls only (the SWBS-eligible builder), transaction-grain. Each cell = "
                 "that ship-system group's share of HII-Ingalls DDG reported subaward $ for the fiscal "
                 "year (constant FY2026$); columns sum to 100% incl. U00 unmapped. Denominator differs "
                 "from §3/§4, which include GD-BIW."],
                styles=[S_ITALIC], outline_level=1)
        _swbs_matrix(c)

        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_EXEC_SUMMARY, _GROUP, render)


EXECUTIVE_SUMMARY = _make_exec_summary()
