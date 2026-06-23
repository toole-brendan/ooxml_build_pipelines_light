"""domain_concentration - the "where to play" contestability view (live).

Turns the documented Capability-Domain concentration caveat into an analytical axis:
for each program x capability domain, the domain's SIZE (reported first-tier subaward
$, FY2026$) paired with its CONCENTRATION - so a large share that is really one or two
contracts (a "fortress") is never misread as a broad, contestable supplier field.

All cells are LIVE formulas over the three program-vendor sheets' entity-grain rows
(one row per subawardee UEI), via their promoted cols accessors:
  - Domain $M / Share      = SUMIFS over Subaward $M keyed on the resolved D code.
  - Suppliers              = COUNTIFS of UEIs with that D and $>0.
  - Top-1 $M / firm / share= the domain's largest positive vendor total (_xlfn.MAXIFS with
                             $>0), the firm holding it (a DOMAIN-CONSTRAINED INDEX/MATCH on
                             that amount, so a tied $ in another domain can't mis-name it),
                             and that amount over the domain total.
  - HHI                    = SUMIFS of a hidden per-UEI positive-$-squared helper divided by
                             positive-domain-total^2 (Herfindahl, share-of-domain; 0..1).
                             Negative adjustment balances do not enter either side of the ratio.
                             Eff. # firms = 1/HHI.
  - Contestability         = a live label off Top-1 share + HHI + effective # firms.

Scope inherited from the program-vendor sheets: GDEB-reported first-tier subcontracted
scope, hull-builder-only; the HII-Newport News co-build workshare is FFATA-invisible and
excluded (see Executive Summary S1 and the HII Co-Build sheet). Submarine shares are
"% of reported subcontracted scope," NOT "% of total boat construction." `model` group.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_TITLE_SHEET, S_TITLE_SECTION, S_NUM, S_PCT, S_INT,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_classification_refactor.sheets._layout import RowCursor
from workbook_award_classification_refactor.sheets._italic import S_ITALIC
from workbook_award_classification_refactor.sheets._tabs import TAB_DOMAIN_CONC
from workbook_award_classification_refactor.sheets._taxonomy import DOMAINS
from workbook_award_classification_refactor.sheets.ddg_program_vendors import ddg_pv_cols
from workbook_award_classification_refactor.sheets.virginia_program_vendors import virginia_pv_cols
from workbook_award_classification_refactor.sheets.columbia_program_vendors import columbia_pv_cols

_GROUP = "summary"

# (display name, cols accessor). DDG last (its co-build hole does not apply; subs do).
PROGRAMS = [
    ("Virginia", virginia_pv_cols),
    ("Columbia", columbia_pv_cols),
    ("DDG-51", ddg_pv_cols),
]

# B label + 9 metric columns. Top-1 $M (G) is the helper the firm-name match keys on -
# kept beside Top-1 firm / Top-1 share so the dollar, holder, and share read together.
_HEADERS = ["", "$M (FY26$)", "Share", "Suppliers", "Top-1 firm",
            "Top-1 $M", "Top-1 share", "HHI", "Eff. # firms", "Contestability"]
_NCOLS = len(_HEADERS)
_COLS = [40, 12, 8, 10, 26, 12, 11, 8, 12, 15]

INTRO = "Capability-domain size and supplier concentration by program."
CAVEAT = ("Scope: GDEB-reported first-tier subcontracted scope, hull-builder only; the HII-Newport "
          "News co-build workshare is excluded (see HII Co-Build). Submarine shares are share of "
          "reported subcontracted scope, not of total boat construction. Concentration uses positive "
          "spend; size and share use net spend. Highly concentrated: Top-1 at least 60% or HHI at "
          "least 0.40; concentrated: effective firms at most 3; otherwise contestable. HHI = sum of "
          "squared within-domain shares; effective firms = 1/HHI. Operating-entity (UEI) grain; for "
          "ultimate-parent grain see Parent Concentration.")


def _domain_row(code: str, name: str, cols):
    """One (program x domain) row: size + concentration, all live."""
    D = cols("Capability Domain Archetype (D)")
    M = cols("Subaward $M")
    SQ = cols("UEI Positive $ Squared")
    NM = cols("Subawardee Vendor Name")
    dollar = f'SUMIFS({M},{D},"{code}")'                       # net domain total (size / share)
    pos = f'SUMIFS({M},{D},"{code}",{M},">0")'                 # positive-spend total (HHI denom)
    top1 = f'_xlfn.MAXIFS({M},{D},"{code}",{M},">0")'          # largest positive vendor total
    return [
        f"{code}  {name}",
        f"={dollar}",                                                       # C $M (net)
        f'=IFERROR({dollar}/SUM({M}),"")',                                  # D share
        f'=COUNTIFS({D},"{code}",{M},">0")',                               # E suppliers
        # F top-1 firm: DOMAIN-CONSTRAINED match on the Top-1 $M helper (col G) via an
        # INDEX-coerced boolean array (MATCH(1,INDEX((D=code)*(M=G),0),0), no CSE) - so an
        # equal amount in another domain can never return the wrong firm name.
        lambda r: f'=IFERROR(INDEX({NM},MATCH(1,INDEX(({D}="{code}")*({M}=G{r}),0),0)),"")',
        f'={top1}',                                                         # G top-1 $M (helper)
        # H top-1 share: over POSITIVE domain spend (the {pos} denominator), consistent with HHI
        # below - net dollars stay the size/share denominator (col D), concentration ratios use
        # positive dollars (reviewer finding #6).
        lambda r: f'=IFERROR(G{r}/{pos},"")',
        # I HHI: the row-level square helper is zero for nonpositive spend, so this is
        # a plain SUMIFS rather than a cross-sheet array expression.
        f'=IFERROR(SUMIFS({SQ},{D},"{code}")/{pos}^2,"")',                 # I HHI
        lambda r: f'=IFERROR(1/I{r},"")',                                   # J eff # firms
        # Never classify an error / unavailable concentration metric as a real result.
        lambda r: (f'=IF(E{r}=0,"",IF(NOT(AND(ISNUMBER(H{r}),ISNUMBER(I{r}),'  # K
                   f'ISNUMBER(J{r}))),"Check",IF(OR(H{r}>=0.6,I{r}>=0.4),'
                   f'"Highly concentrated",IF(J{r}<=3,"Concentrated","Contestable"))))'),
    ]


_BODY_STY = [S_DEFAULT, S_NUM, S_PCT, S_INT, S_DEFAULT, S_NUM, S_PCT, S_NUM,
             S_NUM, S_BOLD]


def _make_domain_concentration():
    # Build eagerly at import (the make_flat_sheet shape) so each program block's first/last
    # data rows are captured DURING the real row walk and are available to domain_conc_range
    # before the Executive Summary renders - it calls the accessor inside its own render(),
    # which runs earlier in SHEETS order. render() just wraps the already-built rows.
    c = RowCursor(2)
    c.banner(TAB_DOMAIN_CONC, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write([INTRO], styles=[S_ITALIC])
    c.write([CAVEAT], styles=[S_ITALIC])
    c.blank(2)

    _last_domain = len(DOMAINS) - 1
    for i, (prog, cols) in enumerate(PROGRAMS, start=1):
        M = cols("Subaward $M")
        D = cols("Capability Domain Archetype (D)")
        c.banner(f"§{i} - {prog}: capability-domain concentration",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.write(_HEADERS,
                styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (_NCOLS - 1))
        for j, (code, name, _defn) in enumerate(DOMAINS):
            # Tag the block's first + last data row as the cursor writes them; the accessor
            # reads these captured anchors instead of a hand-counted base row + stride.
            c.write(_domain_row(code, name, cols), styles=_BODY_STY, outline_level=1,
                    mark=(f"{prog}:first" if j == 0
                          else f"{prog}:last" if j == _last_domain else None))
        c.total([f"{prog} total", f"=SUM({M})", "=1",
                 f'=COUNTIFS({M},">0")', "", "", "", "", "", ""],
                styles=[S_BOLD, S_NUM, S_PCT, S_INT, S_DEFAULT, S_DEFAULT,
                        S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT],
                n_cols=_NCOLS)
        c.blank(2)

    anchors = dict(c.marks)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_DOMAIN_CONC, _GROUP, render), anchors


# Build at import; `_ANCHORS` holds each program block's captured first/last data row.
DOMAIN_CONCENTRATION, _ANCHORS = _make_domain_concentration()


def domain_conc_range(program: str, header: str) -> str:
    """Absolute data range for one program block / visible header on Domain Concentration.

    Row bounds come from the anchors the RowCursor captured while writing each program block
    (see _make_domain_concentration), so the range tracks the rows the sheet actually emitted
    - there is no hand-counted base/stride to drift if a caveat / blank / total row changes.
    Still positional A1, no named ranges; only the column letter derives from _HEADERS.
    """
    if header not in _HEADERS:
        raise KeyError(header)
    first = _ANCHORS[f"{program}:first"]   # KeyError on an unknown program
    last = _ANCHORS[f"{program}:last"]
    assert last == first + len(DOMAINS) - 1, (program, first, last)
    letter = col_letter(_HEADERS.index(header) + 1)   # gutter A -> first content col B
    return f"'{TAB_DOMAIN_CONC}'!${letter}${first}:${letter}${last}"
