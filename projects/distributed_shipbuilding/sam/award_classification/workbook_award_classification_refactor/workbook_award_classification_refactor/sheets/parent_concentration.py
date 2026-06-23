"""parent_concentration - capability-domain concentration at UEI vs ultimate-parent grain (live).

Companion to Domain Concentration (which treats each subawardee UEI as an independent firm).
This sheet shows the SAME (program x domain) concentration at two grains side by side: the
operating-entity (UEI) grain and the strategic ULTIMATE-PARENT grain - a domain can look
contestable across operating entities yet become materially more concentrated after related
operating entities are collapsed to their ultimate parent.

Every cell is a LIVE formula over the three program-vendor sheets, exactly like Domain
Concentration. The UEI grain reads the per-UEI Subaward $M directly (each row is one firm). The
parent grain reads three hidden per-row helpers the program-vendor factory carries (Parent Key /
Parent Domain $ / Parent Domain Rows): they collapse each UEI to its standardized ultimate parent
and pre-aggregate that parent's positive FY2026$ within the row's domain, which is what lets the
parent Top-1 / HHI / effective-firm / distinct-parent measures be plain MAXIFS / SUMIFS
instead of a baked CSV. Concentration ratios use POSITIVE spend (consistent with Domain
Concentration). `summary` group.
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
from workbook_award_classification_refactor.sheets._tabs import TAB_PARENT_CONC
from workbook_award_classification_refactor.sheets._taxonomy import DOMAINS
from workbook_award_classification_refactor.sheets.ddg_program_vendors import ddg_pv_cols
from workbook_award_classification_refactor.sheets.virginia_program_vendors import virginia_pv_cols
from workbook_award_classification_refactor.sheets.columbia_program_vendors import columbia_pv_cols

_GROUP = "summary"

# (display name, cols accessor). Virginia / Columbia / DDG, mirroring Domain Concentration.
PROGRAMS = [
    ("Virginia", virginia_pv_cols),
    ("Columbia", columbia_pv_cols),
    ("DDG-51", ddg_pv_cols),
]

# B label + 4 UEI-grain + 4 parent-grain metrics + 2 diagnostic deltas.
_HEADERS = ["", "UEI Top-1 %", "UEI HHI", "UEI Eff Firms", "UEI Suppliers",
            "Parent Top-1 %", "Parent HHI", "Parent Eff Firms", "Parent Firms",
            "HHI uplift", "Firm reduction"]
_NCOLS = len(_HEADERS)
_COLS = [40, 12, 9, 13, 13, 13, 9, 13, 12, 11, 13]

INTRO = "Capability-domain concentration at supplier UEI and ultimate-parent grain."
CAVEAT = ("UEI grain treats each operating entity as a firm; parent grain collapses entities to "
          "their standardized ultimate parent, so a UEI-contestable domain can still be a "
          "parent-level duopoly. Top-1 share and HHI use positive FY2026$ spend; effective firms "
          "= 1/HHI. HHI uplift and firm reduction show what changes after parent collapse. Read "
          "alongside Domain Concentration (the UEI-grain size + contestability view).")

_BODY_STY = [S_DEFAULT, S_PCT, S_NUM, S_NUM, S_INT, S_PCT, S_NUM, S_NUM, S_INT,
             S_NUM, S_INT]


def _domain_row(code: str, name: str, cols):
    """One (program x domain) row: UEI-grain + parent-grain concentration, all live."""
    M = cols("Subaward $M")                              # per-UEI lifetime FY2026$
    D = cols("Capability Domain Archetype (D)")           # resolved D code, per UEI
    PD = cols("Parent Domain $")                          # parent's positive $ within the row's domain
    SQ = cols("UEI Positive $ Squared")                   # positive UEI $^2, else 0
    PN = cols("Parent HHI Numerator")                     # positive UEI $ x parent-domain total
    PW = cols("Parent Firm Weight")                       # positive row weight = 1/parent-domain rows
    pos = f'SUMIFS({M},{D},"{code}",{M},">0")'            # positive domain total (shared denominator)
    u_top1 = f'_xlfn.MAXIFS({M},{D},"{code}",{M},">0")'   # largest single UEI
    p_top1 = f'_xlfn.MAXIFS({PD},{D},"{code}",{M},">0")'  # largest single parent (max of parent totals)
    return [
        f"{code}  {name}",
        f'=IFERROR({u_top1}/{pos},"")',                                          # C UEI Top-1 %
        f'=IFERROR(SUMIFS({SQ},{D},"{code}")/{pos}^2,"")',                       # D UEI HHI
        lambda r: f'=IFERROR(1/D{r},"")',                                         # E UEI Eff firms
        f'=COUNTIFS({D},"{code}",{M},">0")',                                      # F UEI Suppliers
        f'=IFERROR({p_top1}/{pos},"")',                                           # G Parent Top-1 %
        # Parent HHI numerator already equals sum(parent total^2) when summed by domain.
        f'=IFERROR(SUMIFS({PN},{D},"{code}")/{pos}^2,"")',                       # H Parent HHI
        lambda r: f'=IFERROR(1/H{r},"")',                                         # I Parent Eff firms
        # Each parent's positive rows carry weights summing to exactly one.
        lambda r: f'=IF(F{r}=0,"",SUMIFS({PW},{D},"{code}"))',                   # J Parent Firms
        lambda r: f'=IF(OR(D{r}="",H{r}=""),"",H{r}-D{r})',                    # K HHI uplift
        lambda r: f'=IF(OR(F{r}="",J{r}=""),"",F{r}-J{r})',                    # L firm reduction
    ]


def _make_parent_concentration():
    # Build eagerly at import (the make_flat_sheet shape) so each program block's first/last
    # data rows are captured DURING the real row walk and are available to parent_conc_range
    # before the Executive Summary renders. render() just wraps the already-built rows. This
    # sheet emits NO total row (unlike Domain Concentration) - the captured anchors track that
    # for free, so the load-bearing +4-vs-+5 stride difference simply disappears.
    c = RowCursor(2)
    c.banner(TAB_PARENT_CONC, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write([INTRO], styles=[S_ITALIC])
    c.write([CAVEAT], styles=[S_ITALIC])
    c.blank(2)

    _last_domain = len(DOMAINS) - 1
    for i, (prog, cols) in enumerate(PROGRAMS, start=1):
        c.banner(f"§{i} - {prog}: UEI vs parent concentration",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.write(_HEADERS,
                styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (_NCOLS - 1))
        for j, (code, name, _defn) in enumerate(DOMAINS):
            # Tag the block's first + last data row as the cursor writes them; the accessor
            # reads these captured anchors instead of a hand-counted base row + stride.
            c.write(_domain_row(code, name, cols), styles=_BODY_STY, outline_level=1,
                    mark=(f"{prog}:first" if j == 0
                          else f"{prog}:last" if j == _last_domain else None))
        c.blank(2)

    anchors = dict(c.marks)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_PARENT_CONC, _GROUP, render), anchors


# Build at import; `_ANCHORS` holds each program block's captured first/last data row.
PARENT_CONCENTRATION, _ANCHORS = _make_parent_concentration()


def parent_conc_range(program: str, header: str) -> str:
    """Absolute data range for one program block / visible header on Parent Concentration.

    Row bounds come from the anchors the RowCursor captured while writing each program block
    (see _make_parent_concentration), so the range tracks the rows the sheet actually emitted
    - there is no hand-counted base/stride to drift if a caveat / blank row changes. Still
    positional A1, no named ranges; only the column letter derives from _HEADERS.
    """
    if header not in _HEADERS:
        raise KeyError(header)
    first = _ANCHORS[f"{program}:first"]   # KeyError on an unknown program
    last = _ANCHORS[f"{program}:last"]
    assert last == first + len(DOMAINS) - 1, (program, first, last)
    letter = col_letter(_HEADERS.index(header) + 1)
    return f"'{TAB_PARENT_CONC}'!${letter}${first}:${letter}${last}"
