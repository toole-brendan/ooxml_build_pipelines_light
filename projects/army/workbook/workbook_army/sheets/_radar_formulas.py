"""_radar_formulas - the shared live-formula library for the recompete sheets.

The Recompete RADAR and the Recompete CALENDAR surface the SAME family-keyed roll-ups
(latest current-PoP end, potential end, parent/vehicle end, lifetime obligations, the
task-order + action counts, the open-notice signal) as LIVE Excel formulas over the
Contract Awards / Award Actions / Pipeline Events leaves. Defining the builders ONCE
here is what guarantees the two sheets can never disagree on a number - the same way
they already share load_families() for the lineage. (The within-row date math -
months-to-end, option headroom, the recompete-window bucket - stays in each sheet,
since it keys on that sheet's own column letters.)

family_formulas(fam, asof) takes:
  - fam:  a callable row -> the family-key cell reference on the CALLING sheet, e.g.
          lambda r: f"$G{r}". The column letter differs per sheet, so the caller owns it.
  - asof: the As-of date cell reference (cross-sheet AS_OF_CELL, or the radar's own C6,
          which is the identical string).
and returns a dict of row -> formula-string builders. Every leaf range resolves from
the leaf's own cols() accessor, so each formula is traceable to a data-sheet cell.
"""
from __future__ import annotations

from workbook_army.sheets.data_contract_awards import awards_cols
from workbook_army.sheets.data_award_actions import actions_cols
from workbook_army.sheets.data_pipeline_events import pipeline_cols


def family_formulas(fam, asof):
    """Family-keyed live-formula builders for one sheet (see module docstring)."""
    AMT = actions_cols("amount")
    A_PIID = actions_cols("piid")
    A_PARENT = actions_cols("parent_idv_piid")
    AW_PIID = awards_cols("piid")
    AW_PARENT = awards_cols("parent_idv_piid")
    AW_CUR = awards_cols("pop_current_end_date")
    AW_POT = awards_cols("pop_potential_end_date")
    PL_AWARDNO = pipeline_cols("award_number")
    PL_DEADLINE = pipeline_cols("response_deadline")

    def eff_end(rng):
        # Family end = MAX of the per-PIID and per-parent MAXIFS, so a task order folds
        # into its parent IDV; 0 (no matching rows) renders blank, not 1899-12-30.
        def f(r):
            m = (f"MAX(_xlfn.MAXIFS({rng},{AW_PIID},{fam(r)}),"
                 f"_xlfn.MAXIFS({rng},{AW_PARENT},{fam(r)}))")
            return f'=IF({m}=0,"",{m})'
        return f

    def parent_end_f(r):
        m = f"_xlfn.MAXIFS({AW_CUR},{AW_PIID},{fam(r)})"
        return f'=IF({m}=0,"",{m})'

    return {
        "cur_end": eff_end(AW_CUR),
        "pot_end": eff_end(AW_POT),
        "parent_end": parent_end_f,
        "vtype": lambda r: f'=IF(COUNTIFS({AW_PARENT},{fam(r)})>0,"IDV vehicle","Standalone")',
        "tos": lambda r: f'=COUNTIFS({AW_PARENT},{fam(r)})',
        "obl": lambda r: (f'=(SUMIFS({AMT},{A_PARENT},{fam(r)})'
                          f'+SUMIFS({AMT},{A_PIID},{fam(r)}))/1000000'),
        "acts": lambda r: f'=COUNTIFS({A_PARENT},{fam(r)})+COUNTIFS({A_PIID},{fam(r)})',
        "inmkt": lambda r: (f'=IF(COUNTIFS({PL_AWARDNO},{fam(r)},'
                            f'{PL_DEADLINE},">="&{asof})>0,"Y","")'),
    }
