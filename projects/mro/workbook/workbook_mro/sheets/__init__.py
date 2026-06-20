"""Sheet registry - one module per rendered sheet.

Tab order = the SHEETS order below, grouped into contiguous blocks in
workbook_core.groups.SHEET_GROUPS order (summary -> guide -> inputs -> model -> data
-> outputs -> validation -> sources -> chartdata); package_workbook() asserts that
invariant at build. Producers are listed before their consumers within the model block.
"""
from . import (
    # summary
    summary_executive_summary,
    # guide
    guide_methodology,
    # inputs
    inputs_assumptions,
    inputs_scenarios,
    # model (producers first)
    model_reconciliation,
    model_services,
    model_depot_ship_repair,
    model_op5_navy_topdown,
    model_msc_scn_uscg_topdown,
    model_tam_bridge,
    model_private_addressable,
    model_sam_build,
    # data
    data_awards,
    data_j998_j999,
    data_psc_1905_classified,
    data_tam_atoms,
    # outputs
    outputs_figure_register,
    # validation
    validation_verification_answers,
    validation_scope_reconciliation,
    # sources
    sources_source_index,
    sources_references,
    # chartdata (sorts last)
    chartdata_output,
)


SHEETS = [
    # Summary
    summary_executive_summary.EXECUTIVE_SUMMARY,
    # Guide & scope
    guide_methodology.METHODOLOGY,
    # Inputs & levers
    inputs_assumptions.ASSUMPTIONS,
    inputs_scenarios.SCENARIOS_ENTRY,
    # Model (TAM/SAM)
    model_reconciliation.RECONCILIATION,
    model_services.SERVICES,
    model_depot_ship_repair.DEPOT_SHIP_REPAIR,
    model_op5_navy_topdown.OP5_NAVY_TOPDOWN,
    model_msc_scn_uscg_topdown.MSC_SCN_USCG_TOPDOWN,
    model_tam_bridge.TAM_BRIDGE,
    model_private_addressable.PRIVATE_ADDRESSABLE,
    model_sam_build.SAM_BUILD,
    # Source data
    data_awards.AWARDS,
    data_j998_j999.J998_J999,
    data_psc_1905_classified.PSC_1905_CLASSIFIED,
    data_tam_atoms.TAM_ATOMS,
    # Outputs (deck contract)
    outputs_figure_register.FIGURE_REGISTER,
    # Validation
    validation_verification_answers.VERIFICATION_ANSWERS,
    validation_scope_reconciliation.SCOPE_RECONCILIATION,
    # Sources
    sources_source_index.SOURCE_INDEX,
    sources_references.REFERENCES,
    # Chart data (deck loader; sorts last)
    chartdata_output.OUTPUT,
]
