"""Sheet registry - ONE module per rendered sheet (one file = one tab).

Tab order = the order of SHEETS below. Each sheet module exposes a single
tables.SheetEntry; each declares its group (see workbook_core.groups), and the
blocks below keep each group contiguous and in groups.SHEET_GROUPS order
(summary -> guide -> inputs -> model -> data -> outputs -> validation -> sources
-> chartdata). package_workbook() asserts that invariant at build time.

Module files are named ``<group>_<tab-slug>.py`` (the spec files in
workbook/sheet_specs/ match 1:1). ``taxonomy`` is a shared NON-sheet helper
(bucket vocabulary + classify()), imported by the sheet modules that need it; it
is not registered here.

To add a sheet: create a new module exposing a SheetEntry, import it, and place
its entry in its group's block below.
"""
from . import (
    # summary (the reader-facing answer page)
    summary_executive_summary,
    # guide & scope
    guide_methodology,
    # inputs & levers (the single edit surface)
    inputs_assumptions,
    # model (TAM/SAM)
    model_tam_build,
    model_sam_build,
    model_outlook,
    # source data
    data_deflators,
    data_scn_budget,
    data_obbba_funding,
    data_ap_bridge,
    data_fydp_outyears,
    data_pop_corpus,
    data_entity_master,
    data_location_master,
    data_worktype_evidence,
    data_worktype_by_fy,
    # outputs (deck contract)
    outputs_figure_register,
    # validation
    validation_sib_excluded,
    validation_sensitivity,
    # validation_number_audit,       # unregistered (kept as module; fed the removed Exec Summary audit status)
    # validation_qa_reconciliation,  # unregistered (kept as module; fed the removed Exec Summary audit status)
    validation_pop_source_audit,
    # sources
    sources_source_index,
    sources_references,
    # chart data (deck loader; sorts last, own group/color)
    chartdata_z_chart_data,
)


SHEETS = [
    # --- Summary ---
    summary_executive_summary.EXECUTIVE_SUMMARY,
    # --- Guide & scope ---
    guide_methodology.METHODOLOGY,
    # --- Inputs & levers ---
    inputs_assumptions.ASSUMPTIONS,
    # --- Model (TAM/SAM) ---
    model_tam_build.TAM_BUILD,
    model_sam_build.SAM_BUILD,
    model_outlook.OUTLOOK,
    # --- Source data ---
    data_deflators.DEFLATORS,
    data_scn_budget.SCN_BUDGET,
    data_obbba_funding.OBBBA_FUNDING,
    data_ap_bridge.AP_BRIDGE,
    data_fydp_outyears.FYDP_OUTYEARS,
    data_pop_corpus.POP_CORPUS,
    data_entity_master.ENTITY_MASTER,
    data_location_master.LOCATION_MASTER,
    data_worktype_evidence.WORKTYPE_EVIDENCE,
    data_worktype_by_fy.WORKTYPE_BY_FY,
    # --- Outputs ---
    outputs_figure_register.FIGURE_REGISTER,
    # --- Validation ---
    validation_sib_excluded.SIB_EXCLUDED,
    validation_sensitivity.SENSITIVITY,
    # validation_number_audit.NUMBER_AUDIT,            # unregistered (kept as module)
    # validation_qa_reconciliation.QA_RECONCILIATION,  # unregistered (kept as module)
    validation_pop_source_audit.POP_SOURCE_AUDIT,
    # --- Sources ---
    sources_source_index.SOURCE_INDEX,
    sources_references.REFERENCES,
    # --- Chart data (deck loader; sorts last) ---
    chartdata_z_chart_data.CHART_DATA,
]
