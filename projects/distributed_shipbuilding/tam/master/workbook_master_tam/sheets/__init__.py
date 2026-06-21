"""Master TAM sheet registry - tabs grouped by FUNCTION, program as the inner axis.

This is a TAM workbook (the SAM model and its supporting machinery were removed):
no SAM Build, scenarios, worktype shares, or subaward/supplier/geography evidence
tabs; no deck-contract tabs (figure register / chart data).

The engine (package_workbook) asserts that every sheet declares a group, that
each group forms ONE contiguous run, and that the runs follow groups.SHEET_GROUPS
order (summary -> guide -> inputs -> model -> data -> validation -> sources).
Because a per-program SHEETS list would repeat every group, we interleave the
former workbooks group by group here.

Each former workbook lives under its own sub-package (submarines/ ddg/ ceiling/)
with its tab names prefixed for uniqueness ("Sub ..."/"DDG ..."/"Ceiling ...").
Deflators is shared once; the Portfolio Summary is the cross-program answer page.
"""
from workbook_master_tam.sheets.portfolio import portfolio_summary as p_summary
from workbook_master_tam.sheets.submarines import (
    summary_executive_summary as s_summary,
    guide_methodology as s_guide,
    inputs_assumptions as s_inputs,
    model_tam_build as s_tam,
    model_outlook as s_outlook,
    data_deflators as s_deflators,
    data_scn_budget as s_scn,
    data_obbba_funding as s_obbba,
    data_ap_bridge as s_ap,
    data_fydp_outyears as s_fydp,
    data_pop_corpus as s_pop,
    validation_sib_excluded as s_sib,
    validation_sensitivity as s_sens,
    validation_pop_source_audit as s_pop_audit,
    sources_source_index as s_srcidx,
    sources_references as s_refs,
)
from workbook_master_tam.sheets.ddg import (
    summary_executive_summary as d_summary,
    guide_methodology as d_guide,
    inputs_assumptions as d_inputs,
    model_tam_build as d_tam,
    model_outlook as d_outlook,
    data_scn_budget as d_scn,
    data_obbba_funding as d_obbba,
    data_production_schedule as d_prodsched,
    data_ap_bridge as d_ap,
    data_fydp_outyears as d_fydp,
    data_pop_corpus as d_pop,
    validation_sensitivity as d_sens,
    validation_scope_exclusions as d_scope,
    validation_pop_source_audit as d_pop_audit,
    sources_source_index as d_srcidx,
    sources_references as d_refs,
)
from workbook_master_tam.sheets.ceiling import (
    summary_overview as c_overview,
    inputs_assumptions as c_inputs,
    model_ceiling as c_ceiling,
    model_bridge as c_bridge,
    model_headroom as c_headroom,
    data_cost_base as c_costbase,
    validation_sensitivity as c_sens,
    validation_tie_outs as c_tieouts,
    sources_source_index as c_sources,
)


SHEETS = [
    # ===================== SUMMARY =====================
    p_summary.PORTFOLIO_SUMMARY,   # cross-program answer page (Va | Col | DDG | Total)
    s_summary.EXECUTIVE_SUMMARY,
    d_summary.EXECUTIVE_SUMMARY,
    c_overview.OVERVIEW,
    # ===================== GUIDE & SCOPE =====================
    s_guide.METHODOLOGY,
    d_guide.METHODOLOGY,
    # ===================== INPUTS & LEVERS =====================
    s_inputs.ASSUMPTIONS,
    d_inputs.ASSUMPTIONS,
    c_inputs.ASSUMPTIONS,
    # ===================== MODEL =====================
    s_tam.TAM_BUILD,
    s_outlook.OUTLOOK,
    d_tam.TAM_BUILD,
    d_outlook.OUTLOOK,
    c_ceiling.CEILING_MODEL,
    c_bridge.CONVERSION_BRIDGE,
    c_headroom.HEADROOM,
    # ===================== SOURCE DATA =====================
    s_deflators.DEFLATORS,   # shared across all programs (DoD Green Book deflators)
    s_scn.SCN_BUDGET,
    s_obbba.OBBBA_FUNDING,
    s_ap.AP_BRIDGE,
    s_fydp.FYDP_OUTYEARS,
    s_pop.POP_CORPUS,
    d_scn.SCN_BUDGET,
    d_obbba.OBBBA_FUNDING,
    d_prodsched.PRODUCTION_SCHEDULE,
    d_ap.AP_BRIDGE,
    d_fydp.FYDP_OUTYEARS,
    d_pop.POP_CORPUS,
    c_costbase.COST_BASE,
    # ===================== VALIDATION =====================
    s_sib.SIB_EXCLUDED,
    s_sens.SENSITIVITY,
    s_pop_audit.POP_SOURCE_AUDIT,
    d_sens.SENSITIVITY,
    d_scope.SCOPE_EXCLUSIONS,
    d_pop_audit.POP_SOURCE_AUDIT,
    c_sens.SENSITIVITY,
    c_tieouts.TIE_OUTS,
    # ===================== SOURCES =====================
    s_srcidx.SOURCE_INDEX,
    s_refs.REFERENCES,
    d_srcidx.SOURCE_INDEX,
    d_refs.REFERENCES,
    c_sources.SOURCES,
]
