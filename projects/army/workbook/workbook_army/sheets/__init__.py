"""Sheet registry - one module per rendered sheet.

Tab order = the SHEETS order below, grouped into contiguous blocks in
workbook_core.groups.SHEET_GROUPS order (summary -> guide -> inputs -> model -> data
-> outputs -> validation -> sources -> chartdata); package_workbook() asserts that
invariant at build. Producers are listed before their consumers within the model block.

Scaffold status: seeded with a single placeholder summary sheet so the pipeline
builds a valid .xlsx on first run. Replace it with real sheet modules.

To add a sheet:
  1. Copy workbook_core/sheet_base_template.py to workbook_army/sheets/<name>.py.
  2. Set the metadata + INTENT/LAYOUT, build _build_rows().
  3. Import the module here and add <name>.SPEC to SHEETS, in tab order.
"""
from . import (
    # summary
    summary_overview,
    # data (faithful raw contract pulls; the leaves the recompete radar keys on)
    data_contract_awards,
    data_award_actions,
    data_subawards,
    data_pipeline_events,
    # model (live-formula screens over the data leaves; calendar imports from the radar)
    model_recompete_radar,
    model_recompete_calendar,
)


SHEETS = [
    # Summary
    summary_overview.OVERVIEW,
    # Model (live-formula screens; must precede the data block per groups order)
    model_recompete_radar.RECOMPETE_RADAR,
    model_recompete_calendar.RECOMPETE_CALENDAR,
    # Data (raw contract evidence - one filterable native table per source pull)
    data_contract_awards.CONTRACT_AWARDS,
    data_award_actions.AWARD_ACTIONS,
    data_subawards.SUBAWARDS,
    data_pipeline_events.PIPELINE_EVENTS,
]
