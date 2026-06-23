"""executive_summary - the front-door dashboard tab.

The first sheet: orients a cold reader and carries the headline numbers, all as LIVE
formulas off the model / summary sheets (so they never drift). Answer-first order - market
scale, then where the dollars sit, then accessibility:

  - Purpose + scope (static intro).
  - §1 Scope & how to read these figures (the denominator caveat - what is and isn't counted,
    and why submarine shares are NOT total-boat-construction shares).
  - §2 Observed SAM by program and fiscal year (per-program $ by FY, lifetime memo, FY2025 reach).
  - §3 Capability Domain mix by fiscal year (one matrix, the three programs side by side).
  - §4 FY2025 where-to-play scorecard (per program x domain: size, parent concentration,
    incumbency, retention, entry and the Observed Structure read - all read off Where to Play).
  - §5 Supplier continuity by program and fiscal year (incumbent $ share + retention by FY,
    program grain, off Supplier-Year Activity).
  - §6 Primary Output mix by fiscal year (one matrix).
  - §7 DDG SWBS mix by FY (HII-Ingalls only).

Cells reference the program-vendor per-FY / archetype columns, the Where to Play scorecard and
the Supplier-Year Activity model via their promoted cols accessors, the same way those sheets
reference the transaction leaf. Carries no native table (a legend/dashboard).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_PCT, S_INT,
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
from workbook_award_classification_refactor.sheets.where_to_play import where_to_play_cols
from workbook_award_classification_refactor.sheets.supplier_year_activity import (
    supplier_year_cols,
)

_GROUP = "summary"

# Programs, side by side, in the user's order. (display name, cols accessor)
PROGRAMS = [
    ("Virginia", virginia_pv_cols),
    ("Columbia", columbia_pv_cols),
    ("DDG-51", ddg_pv_cols),
]
# Display label -> internal program key (the Supplier-Year Activity / spine key; DDG-51 -> DDG).
_PROGRAM_KEY = {"Virginia": "Virginia", "Columbia": "Columbia", "DDG-51": "DDG"}
# (column label, the per-FY header on the program-vendor sheet)
FYS = [("FY22", "FY22 $M"), ("FY23", "FY23 $M"),
       ("FY24", "FY24 $M"), ("FY25", "FY25 $M")]
FY_NUMS = [2022, 2023, 2024, 2025]

# B label + 3 programs x 4 FY = 13 content columns (gutter A added by worksheet()).
_NCOLS = 1 + len(PROGRAMS) * len(FYS)
_COLS = [44] + [10] * (_NCOLS - 1)

# Supplier-Year Activity ranges (program-grain continuity + FY reach).
_SY_PROG = supplier_year_cols("Program")
_SY_FY = supplier_year_cols("Federal FY")
_SY_POS = supplier_year_cols("Positive Supplier $M")
_SY_STATUS = supplier_year_cols("Activity Status")

# Where to Play lookup columns (the FY2025 scorecard reads its rows by Axis / Program / FY / code).
_W_AXIS = where_to_play_cols("Axis")
_W_CODE = where_to_play_cols("Archetype Code")
_W_PROGRAM = where_to_play_cols("Program")
_W_FY = where_to_play_cols("Federal FY")

INTRO = ("Reported hull-builder first-tier subawards for DDG-51, Virginia and Columbia; "
         "constant FY2026$.")

CAVEATS = [
    "Reported first-tier subawards under the hull-construction primes (GDEB for Virginia and "
    "Columbia, Bath Iron Works and Ingalls for DDG-51); constant FY2026$ (Green Book Procurement "
    "deflator). GFE and MIB / BlueForge accounts are excluded.",
    "Submarine shares are percentages of GDEB-reported subcontracted scope, not of total boat "
    "construction; the HII-Newport News co-build workshare is largely outside the reported subaward "
    "data (about $98M visible against tens of billions - see Market Bridge).",
    "Size, concentration and supplier continuity are read at one program x archetype x fiscal-year "
    "grain (Where to Play). Domain Concentration keeps the lifetime structural view, with both "
    "operating-entity and ultimate-parent concentration.",
]


def _program_fy_totals(c: RowCursor) -> None:
    """§2 - per-program $ by fiscal year, with a lifetime memo and FY2025 reach."""
    total_fy25 = "+".join(f"SUM({cols('FY25 $M')})" for _n, cols in PROGRAMS)
    c.write(["Program", "FY22 $M", "FY23 $M", "FY24 $M", "FY25 $M",
             "Lifetime $M", "FY25 active UEIs", "FY25 share"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 7)
    for name, cols in PROGRAMS:
        key = _PROGRAM_KEY[name]
        c.write([
            name,
            f"=SUM({cols('FY22 $M')})",
            f"=SUM({cols('FY23 $M')})",
            f"=SUM({cols('FY24 $M')})",
            f"=SUM({cols('FY25 $M')})",
            f"=SUM({cols('Subaward $M')})",
            f'=COUNTIFS({_SY_PROG},"{key}",{_SY_FY},2025,{_SY_POS},">0")',
            lambda r: f'=IFERROR(F{r}/({total_fy25}),"")',
        ], styles=[S_DEFAULT, S_NUM, S_NUM, S_NUM, S_NUM, S_NUM, S_INT, S_PCT])
    c.write(["FY columns are constant FY2026$ reported first-tier subaward $; lifetime is all years. "
             "FY25 active UEIs = distinct suppliers with positive FY2025 spend; FY25 share = the "
             "program's FY2025 dollars over the three-program FY2025 total."],
            styles=[S_ITALIC])


def _wtp(metric: str, program_disp: str, code: str) -> str:
    """One FY2025 Where to Play cell, by axis D / program display label / archetype code."""
    vals = where_to_play_cols(metric)
    match = (f'MATCH(1,INDEX(({_W_AXIS}="D")*({_W_PROGRAM}="{program_disp}")'
             f'*({_W_FY}=2025)*({_W_CODE}="{code}"),0),0)')
    return f'=IFERROR(INDEX({vals},{match}),"")'


def _fy25_domain_scorecard(c: RowCursor) -> None:
    """§4 - one row per program x capability domain, FY2025, read off Where to Play."""
    c.write(["Domain (FY2025)", "$M (FY26$)", "Program share", "Active UEIs", "Parent Top-1",
             "Parent HHI", "Incumbent $", "Retention", "First-observed $", "Observed structure"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 9)
    for disp, _cols in PROGRAMS:
        c.write([disp], styles=[S_BOLD])
        for code, name, _defn in DOMAINS:
            c.write([
                f"{code}  {name}",
                _wtp("Net Subaward $M", disp, code),
                _wtp("Program Share", disp, code),
                _wtp("Active Suppliers", disp, code),
                _wtp("Parent Top-1", disp, code),
                _wtp("Parent HHI", disp, code),
                _wtp("Incumbent $ %", disp, code),
                _wtp("Retention %", disp, code),
                _wtp("First-observed $ %", disp, code),
                _wtp("Observed Structure", disp, code),
            ], styles=[S_DEFAULT, S_NUM, S_PCT, S_INT, S_PCT, S_NUM,
                       S_PCT, S_PCT, S_PCT, S_DEFAULT])
    c.write(["Parent Top-1 / Parent HHI / Incumbent $ / Retention / First-observed $ use positive "
             "spend at the ultimate-parent grain. Observed Structure is an analyst-defined screen on "
             "parent concentration and incumbency (Thin observation below three suppliers), not proof "
             "of contestability - see Methodology. Full annual detail is on Where to Play."],
            styles=[S_ITALIC])


def _continuity_incumbent(key: str, fy: int) -> str:
    cont = f'SUMIFS({_SY_POS},{_SY_PROG},"{key}",{_SY_FY},{fy},{_SY_STATUS},"Continued")'
    tot = f'SUMIFS({_SY_POS},{_SY_PROG},"{key}",{_SY_FY},{fy})'
    return f'=IFERROR({cont}/{tot},"")'


def _continuity_retention(key: str, fy: int) -> str:
    cont = (f'COUNTIFS({_SY_PROG},"{key}",{_SY_FY},{fy},'
            f'{_SY_STATUS},"Continued",{_SY_POS},">0")')
    prior = f'COUNTIFS({_SY_PROG},"{key}",{_SY_FY},{fy - 1},{_SY_POS},">0")'
    return f'=IFERROR({cont}/{prior},"")'


def _program_fy_continuity(c: RowCursor) -> None:
    """§5 - program-grain supplier continuity across the FY window (off Supplier-Year Activity)."""
    c.write(["Continuity (program x FY)", "FY22", "FY23", "FY24", "FY25"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 4)
    c.write(["Incumbent $ share (dollars to suppliers active the prior FY)"], styles=[S_BOLD])
    for name, _cols in PROGRAMS:
        key = _PROGRAM_KEY[name]
        c.write([name] + [_continuity_incumbent(key, fy) for fy in FY_NUMS],
                styles=[S_DEFAULT] + [S_PCT] * 4)
    c.write(["Retention (prior-FY suppliers still active this FY)"], styles=[S_BOLD])
    for name, _cols in PROGRAMS:
        key = _PROGRAM_KEY[name]
        c.write([name] + [_continuity_retention(key, fy) for fy in FY_NUMS],
                styles=[S_DEFAULT] + [S_PCT] * 4)
    c.write(["Incumbent = positive-spend suppliers active in the prior fiscal year too. Retention = "
             "the prior year's active suppliers still active this year. Both pool all archetypes; "
             "the archetype detail is on Where to Play."],
            styles=[S_ITALIC])


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
    """§7 - DDG SWBS mix by FY: one DDG block (subs carry no SWBS). Rows = SWBS major
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

        c.section("§2 - Observed SAM by program and fiscal year", _NCOLS)
        _program_fy_totals(c)
        c.blank(2)

        c.section("§3 - Capability Domain mix by fiscal year", _NCOLS)
        c.write(["Each cell = that domain's share of the program's reported first-tier subaward $ "
                 "for the fiscal year (constant FY2026$); columns sum to 100%. Window: FY2022-FY2025 "
                 "(pre-FY22 and partial FY26 are excluded from this mix; lifetime totals are in §2)."],
                styles=[S_ITALIC])
        _matrix(c, "Capability Domain Archetype (D)", DOMAINS)
        c.blank(2)

        c.section("§4 - FY2025 where-to-play scorecard", _NCOLS)
        c.write(["The answer page: FY2025 size and accessibility per program x capability domain, "
                 "read off Where to Play. Read size (left) with parent concentration and incumbency "
                 "(right) - a large share that is one embedded parent is not an open field."],
                styles=[S_ITALIC])
        _fy25_domain_scorecard(c)
        c.blank(2)

        c.section("§5 - Supplier continuity by program and fiscal year", _NCOLS)
        c.write(["Whether FY2025 looks like the prior years: incumbent dollar share and supplier "
                 "retention by program and fiscal year, pooled across archetypes."],
                styles=[S_ITALIC])
        _program_fy_continuity(c)
        c.blank(2)

        c.section("§6 - Primary Output mix by fiscal year", _NCOLS)
        c.write(["Each cell = that output's share of the program's reported first-tier subaward $ "
                 "for the fiscal year (constant FY2026$); columns sum to 100%. Window: FY2022-FY2025 "
                 "(pre-FY22 and partial FY26 are excluded from this mix; lifetime totals are in §2)."],
                styles=[S_ITALIC])
        _matrix(c, "Primary Output Archetype (P)", OUTPUTS)
        c.blank(2)

        c.section("§7 - DDG SWBS mix by fiscal year", _NCOLS)
        c.write(["DDG-51 HII-Ingalls only (the SWBS-eligible builder), transaction-grain. Each cell = "
                 "that ship-system group's share of HII-Ingalls DDG reported subaward $ for the fiscal "
                 "year (constant FY2026$); columns sum to 100% incl. U00 unmapped. Denominator differs "
                 "from §3/§6, which include GD-BIW."],
                styles=[S_ITALIC])
        _swbs_matrix(c)

        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_EXEC_SUMMARY, _GROUP, render)


EXECUTIVE_SUMMARY = _make_exec_summary()
