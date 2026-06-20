"""Non-Public-NSY Bridge

INTENT
    Two clearly-separated reconciliations, kept apart so the $9.5B funding cross-check
    and the $7.1B contestable SAM base are never confused:

      §1 Reconciliation cross-check - the budget-anchored MRO funding pot (~$16,996M)
         less Public NSY intramural labor (~$7,485M) leaves ~$9,511M of non-public-NSY
         funding, which sits within ~6% (~$540M) of the $8,971M Reconciled FPDS-visible
         MRO TAM. A funding-side check, NOT a market size, NOT "TAM".

      §2 SAM addressability entry point (disclosure) - the Broad Addressable /
         private-contestable SAM base = Reconciled TAM less captive SUPSHIP complex-OH
         and FMS (~$7,135M), computed over the TAM-atom scope_class. Captive/FMS
         contestability is a SAM question (see SAM Build), surfaced here only so the two
         numbers are visible side by side.

    Pure links/derivations - no recompute of producer figures. A bare =accessor() pull
    is green (S_LINK_NUM); a scaled / summed / netted value is derived (black S_NUM).

LAYOUT
    row 2 : title
    B..C  : Step, $M
    §1 non-public-NSY reconciliation cross-check · §2 Broad Addressable (SAM entry)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_LABEL_INDENT_1,
    S_NUM, S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets.model_tam_bridge import topdown_total_cell, bottomup_total_cell
from workbook_mro.sheets.model_op5_navy_topdown import op5_public_nsy_cell
from workbook_mro.sheets.data_tam_atoms import amount_range, axis_tag_range
from workbook_mro.sheets import taxonomy_mro as tx

_GROUP = "model"
_TAB = "Non-Public-NSY Bridge"
_NCOLS = 2                       # B..C: Step, $M
_COLS = [52, 16]
_HEADERS = ["Step", "$M"]
_HSTYLE = [S_HEADER_LEFT, S_HEADER_CENTER]

# Atom-scope ranges for the §2 Broad Addressable computation (same construction as
# SAM Build's broad_addressable scenario: constrain scope_class = Addressable).
_AMT = amount_range()
_SCOPE = axis_tag_range("scope_class")
_ADDR = tx.SCOPE_ADDRESSABLE


def _make():
    P: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    def _step(key, label, val, style, *, indent=False):
        r = c.write([label, val],
                    styles=[S_LABEL_INDENT_1 if indent else S_DEFAULT, style],
                    outline_level=1)
        P[key] = r
        return r

    # §1 Reconciliation cross-check (funding side; not a market size)
    c.banner("§1 - Non-public-NSY reconciliation cross-check", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(_HEADERS, styles=_HSTYLE, outline_level=1)
    _step("pot", "Budget-anchored MRO funding pot (top-down)",
          f"={topdown_total_cell()}", S_LINK_NUM)
    _step("nsy", "less Public NSY (intramural federal labor)",
          f"=-{op5_public_nsy_cell()}/1000", S_NUM, indent=True)
    P["crosscheck"] = c.total(
        ["Non-public-NSY funding cross-check", f"=C{P['pot']}+C{P['nsy']}"],
        styles=[S_BOLD, S_NUM], n_cols=_NCOLS, outline_level=1)
    _step("tam", "Reconciled FPDS-visible MRO TAM (bottom-up)",
          f"={bottomup_total_cell()}", S_LINK_NUM)
    P["delta"] = c.total(
        ["Delta (cross-check - TAM)", f"=C{P['crosscheck']}-C{P['tam']}"],
        styles=[S_BOLD, S_NUM], n_cols=_NCOLS, outline_level=1)
    c.blank(2)

    # §2 SAM addressability entry point (the contestable base; lives in SAM)
    c.banner("§2 - Broad Addressable (SAM addressability entry point)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(_HEADERS, styles=_HSTYLE, outline_level=1)
    _step("broadtam", "Broad TAM (TAM atoms total)", f"=SUM({_AMT})", S_NUM)
    _step("lesscap", "less captive SUPSHIP complex OH + FMS (a SAM question)",
          f'=-SUMPRODUCT({_AMT},({_SCOPE}<>"{_ADDR}"))', S_NUM, indent=True)
    P["broadaddr"] = c.total(
        ["Broad Addressable / private-contestable SAM base (see SAM Build)",
         f'=SUMPRODUCT({_AMT},({_SCOPE}="{_ADDR}"))'],
        styles=[S_BOLD, S_NUM], n_cols=_NCOLS, outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    # accessors (consumed by Executive Summary + Figure Register)
    def budget_pot_cell() -> str: return f"'{_TAB}'!C{P['pot']}"
    def nonpublic_nsy_crosscheck_cell() -> str: return f"'{_TAB}'!C{P['crosscheck']}"
    def crosscheck_delta_cell() -> str: return f"'{_TAB}'!C{P['delta']}"
    def broad_addressable_entry_cell() -> str: return f"'{_TAB}'!C{P['broadaddr']}"

    accessors = dict(budget_pot_cell=budget_pot_cell,
                     nonpublic_nsy_crosscheck_cell=nonpublic_nsy_crosscheck_cell,
                     crosscheck_delta_cell=crosscheck_delta_cell,
                     broad_addressable_entry_cell=broad_addressable_entry_cell)
    return SheetEntry(_TAB, _GROUP, render), accessors


PRIVATE_ADDRESSABLE, _ACC = _make()

budget_pot_cell = _ACC["budget_pot_cell"]
nonpublic_nsy_crosscheck_cell = _ACC["nonpublic_nsy_crosscheck_cell"]
crosscheck_delta_cell = _ACC["crosscheck_delta_cell"]
broad_addressable_entry_cell = _ACC["broad_addressable_entry_cell"]
