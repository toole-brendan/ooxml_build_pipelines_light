"""parent_concentration - capability-domain concentration at UEI vs ultimate-parent grain (live).

Companion to Domain Concentration (which treats each subawardee UEI as an independent firm).
This sheet shows the SAME (program x domain) concentration at two grains side by side: the
operating-entity (UEI) grain and the strategic ULTIMATE-PARENT grain - a domain can look
contestable across operating entities yet be a near-duopoly across parents (e.g. Columbia D2:
Top-1 ~55.5% / HHI ~0.384 at UEI grain vs ~60.4% / ~0.438 parent-collapsed).

Every cell is a LIVE formula over the three program-vendor sheets, exactly like Domain
Concentration. The UEI grain reads the per-UEI Subaward $M directly (each row is one firm). The
parent grain reads three hidden per-row helpers the program-vendor factory carries (Parent Key /
Parent Domain $ / Parent Domain Rows): they collapse each UEI to its standardized ultimate parent
and pre-aggregate that parent's positive FY2026$ within the row's domain, which is what lets the
parent Top-1 / HHI / effective-firm / distinct-parent measures be plain MAXIFS / SUMPRODUCT
instead of a baked CSV. Concentration ratios use POSITIVE spend (consistent with Domain
Concentration). `summary` group.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
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

# B label + 4 UEI-grain + 4 parent-grain metric columns.
_HEADERS = ["", "UEI Top-1 %", "UEI HHI", "UEI Eff Firms", "UEI Suppliers",
            "Parent Top-1 %", "Parent HHI", "Parent Eff Firms", "Parent Firms"]
_NCOLS = len(_HEADERS)
_COLS = [40, 12, 9, 13, 13, 13, 9, 13, 12]

INTRO = "Capability-domain concentration at supplier UEI and ultimate-parent grain."
CAVEAT = ("UEI grain treats each operating entity as a firm; parent grain collapses entities to "
          "their standardized ultimate parent, so a UEI-contestable domain can still be a "
          "parent-level duopoly. Top-1 share and HHI use positive FY2026$ spend; effective firms "
          "= 1/HHI. Read alongside Domain Concentration (the UEI-grain size + contestability view).")

_BODY_STY = [S_DEFAULT, S_PCT, S_NUM, S_NUM, S_INT, S_PCT, S_NUM, S_NUM, S_INT]


def _domain_row(code: str, name: str, cols):
    """One (program x domain) row: UEI-grain + parent-grain concentration, all live."""
    M = cols("Subaward $M")                              # per-UEI lifetime FY2026$
    D = cols("Capability Domain Archetype (D)")           # resolved D code, per UEI
    PD = cols("Parent Domain $")                          # parent's positive $ within the row's domain
    PR = cols("Parent Domain Rows")                       # positive rows sharing parent + domain (>=1)
    pos = f'SUMIFS({M},{D},"{code}",{M},">0")'            # positive domain total (shared denominator)
    u_top1 = f'_xlfn.MAXIFS({M},{D},"{code}",{M},">0")'   # largest single UEI
    p_top1 = f'_xlfn.MAXIFS({PD},{D},"{code}",{M},">0")'  # largest single parent (max of parent totals)
    return [
        f"{code}  {name}",
        f'=IFERROR({u_top1}/{pos},"")',                                          # C UEI Top-1 %
        f'=IFERROR(SUMPRODUCT(--({D}="{code}"),--({M}>0),{M}^2)/{pos}^2,"")',    # D UEI HHI
        lambda r: f'=IFERROR(1/D{r},"")',                                        # E UEI Eff firms
        f'=COUNTIFS({D},"{code}",{M},">0")',                                     # F UEI Suppliers
        f'=IFERROR({p_top1}/{pos},"")',                                          # G Parent Top-1 %
        # Parent HHI: SUMPRODUCT(M_r * parentTotal_r) over in-domain positive rows = sum of
        # squared parent totals (each parent's rows contribute parentTotal^2), over pos^2.
        f'=IFERROR(SUMPRODUCT(--({D}="{code}"),--({M}>0),{M},{PD})/{pos}^2,"")',  # H Parent HHI
        lambda r: f'=IFERROR(1/H{r},"")',                                        # I Parent Eff firms
        # Distinct parents in the domain: each parent's positive rows sum 1/(its row count) -> 1.
        lambda r: (f'=IF(F{r}=0,"",SUMPRODUCT(--({D}="{code}"),--({M}>0),1/{PR}))'),  # J Parent Firms
    ]


def _make_parent_concentration():
    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.banner(TAB_PARENT_CONC, n_cols=_NCOLS, style=S_TITLE_SHEET)
        c.write([INTRO], styles=[S_ITALIC])
        c.write([CAVEAT], styles=[S_ITALIC])
        c.blank(2)

        for i, (prog, cols) in enumerate(PROGRAMS, start=1):
            c.banner(f"§{i} - {prog}: UEI vs parent concentration",
                     n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
            c.write(_HEADERS,
                    styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (_NCOLS - 1))
            for code, name, _defn in DOMAINS:
                c.write(_domain_row(code, name, cols), styles=_BODY_STY,
                        outline_level=1)
            c.blank(2)

        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_PARENT_CONC, _GROUP, render)


PARENT_CONCENTRATION = _make_parent_concentration()
