"""Sheet registry - one module per rendered sheet.

Tab order = the SHEETS order below, grouped into contiguous blocks in
workbook_core.groups.SHEET_GROUPS order (summary -> guide -> inputs -> model -> data
-> outputs -> validation -> sources -> chartdata); package_workbook() asserts that
invariant at build. Producers are listed before their consumers within the model block.

Decision-first reading order: Overview (the bridge) -> Scope -> Customer Map -> the model
sheets (Budget Market + Market Size lead; then the recompete timing screens) -> the raw
data leaves -> QA + Data Freshness -> Source Log.

To add a sheet:
  1. Copy workbook_core/sheet_base_template.py to workbook_army/sheets/<name>.py (or use
     make_flat_sheet for a raw leaf).
  2. Build it; import the module here and add its SheetEntry to SHEETS, in tab order.
"""
from . import (
    # summary
    summary_overview,
    # guide
    scope_assumptions,
    # inputs (editable knobs + analyst reference)
    input_market_assumptions,
    input_recompete_reviews,
    data_customer_map,
    # model (live-formula screens; must precede the data block per groups order)
    model_budget_market,
    model_market_size,
    model_recompete_radar,
    model_recompete_calendar,
    # data (faithful raw contract pulls)
    data_contract_awards,
    data_award_actions,
    data_subawards,
    data_pipeline_events,
    data_notice_links,
    # data (faithful budget funding evidence)
    data_budget_facts,
    data_p5_cost_elements,
    data_oma_notes,
    # data (canonical per-family fact table)
    data_contract_families,
    # validation
    qa_reconciliation,
    data_source_clocks,
    # sources
    data_source_log,
)


SHEETS = [
    # Summary
    summary_overview.OVERVIEW,
    # Guide
    scope_assumptions.SCOPE_ASSUMPTIONS,
    # Inputs (editable knobs first, then the analyst reference graph)
    input_market_assumptions.MARKET_ASSUMPTIONS,
    input_recompete_reviews.RECOMPETE_REVIEWS,
    data_customer_map.CUSTOMER_MAP,
    # Model (decision models first, then the recompete timing screens)
    model_budget_market.BUDGET_MARKET,
    model_market_size.MARKET_SIZE,
    model_recompete_radar.RECOMPETE_RADAR,
    model_recompete_calendar.RECOMPETE_CALENDAR,
    # Data (raw contract evidence)
    data_contract_awards.CONTRACT_AWARDS,
    data_award_actions.AWARD_ACTIONS,
    data_subawards.SUBAWARDS,
    data_pipeline_events.PIPELINE_EVENTS,
    data_notice_links.NOTICE_LINKS,
    # Data (raw budget funding evidence)
    data_budget_facts.BUDGET_FACTS,
    data_p5_cost_elements.P5_COST_ELEMENTS,
    data_oma_notes.OMA_NOTES,
    # Data (canonical per-family fact table)
    data_contract_families.CONTRACT_FAMILIES,
    # Validation
    qa_reconciliation.QA_RECONCILIATION,
    data_source_clocks.DATA_FRESHNESS,
    # Sources
    data_source_log.SOURCE_LOG,
]
