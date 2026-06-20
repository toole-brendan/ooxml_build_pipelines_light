Source Index
Tab color: 1F3A5F (navy)  ·  group: Sources
Module: sources_source_index.py

Purpose
The provenance map: which extracted datasets feed which tabs, and which model
areas consume them. The dataset inventory + model lineage. A source table (the
context-note exception), so it keeps short context notes.

Reads
- none (standalone inventory; rows are literal dataset records)

Feeds
- none (producer accessor dataset_row_cell is internal hygiene only)
- Native table: tbl_ddg_source_index

On the sheet
§1  Extracted datasets and their consuming tabs
    - Native table (tbl_ddg_source_index), columns: Dataset (extracted/), Rows,
      Key fields, Consumed by (tab), Retrieval, Note.
    - One row per extracted dataset (scn_li_* budget CSVs, dod_announcement_pop /
      dod_action_pop_by_worktype, nc_records_long / nc_annual_by_piid / by_vendor,
      nc_lifetime_vendors, entity_naics_lookup, fpds_annual_by_prime, fpds_raw_v2/,
      nc_scope_summary + _discovered_piids, cost_funnel_summary, sam_subaward_*,
      exec_quotes_outsourcing, edgar_research/), each naming the tab(s) that consume it
      (SCN Budget, Production Schedule, AP Bridge / TAM Build, POP Corpus, SAM Build /
      Entity Master, Vendors, Location Master, FPDS Primes, Scope Exclusions, References).

§2  Consumers by model area
    - Roll-up table (Model area, Primary datasets) grouping the datasets by area:
      Budget, POP, Suppliers, SAM, Validation, References - prose, no formulas.

Notes
- Native cell notes: none.
- Note column: §1.
