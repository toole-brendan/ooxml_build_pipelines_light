Source Index
Tab color: 1F3A5F (navy)  ·  group: Sources
Module: sources_source_index.py

Purpose
The data / budget / methodology source inventory, as three native tables, plus a short
refresh-control block; records what each source feeds. Leaf module (static content);
columns may run a little wider than a model block.

Reads
- none (standalone leaf; static inventory, links no sibling sheet)

Feeds
- none (reference content; not consumed by another tab)
- Native tables: tbl_sub_source_index_data (§1), tbl_sub_source_index_budget (§2),
  tbl_sub_source_index_docs (§3)

On the sheet
(All sections share the header Source / Retrieved / Location / Note-what-it-feeds.)

§1  Data sources (extracted)
    - Static rows for the extracted/ corpus, e.g. dod_announcement_pop.csv (658-row POP
      corpus; feeds POP Corpus TAM gate + per-class split),
      dod_action_pop_by_worktype.csv (POP shares by program x work_type),
      entity_naics_lookup.csv (150 subaward vendors; Entity Master), nc_records_long.csv
      (9,267 FFATA subaward records), subaward_top_recipients.csv, nc_geo_by_state/country
      (Location Master hints), nc_scope_summary.json (SIB exclusion total $4,251.8M + PIID roster).

§2  Budget exhibits (SCN P-5c / P-10 / TOA)
    - Static rows: SCN P-5c Basic Construction (scn_p5c_*.csv; BC stream base -> SCN Budget),
      SCN P-10 Advance Procurement (scn_p10_ap_*.csv; AP/LLTM gross, NOT additive -> AP Bridge),
      SCN per-FY actual TOA (scn_per_fy_actual_toa.csv; reconciliation reference).

§3  Methodology + reference docs
    - Static rows: METHODOLOGY (POP / subaward / budget), implementation_plan.md (v5;
      two-stream TAM + scenario SAM spec), sub_phase3_BPMI_reconciliation.md (SUPERSEDES v5
      on sub AP/LLTM additivity - confirms additive base = $0), deck_specs.md (slide plan).

§4  Refresh control
    - Static block (Area, Last refreshed, Source path, Notes): POP corpus (2026-05,
      extracted/dod_announcement_pop.csv, re-pull on new DoD announcements), Subaward vendors
      (2026-05, extracted/entity_naics_lookup.csv, USAspending + SAM.gov), Budget exhibits
      (FY22-27 PB, budget_books/, annual PB cycle).

Notes
- Native cell notes: none.
- Note column: §4.
