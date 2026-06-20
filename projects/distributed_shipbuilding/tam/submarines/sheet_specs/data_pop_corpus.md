POP Corpus
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_pop_corpus.py

Purpose
The 658-row place-of-performance corpus as a native Excel table behind a compact
at-a-glance rollup; the source of the per-stream POP coefficients (consumed by TAM Build)
and the confirmation audit (POP Source Audit). Each row carries the Gate / GFE-Excl /
Confirmed / Stream flags and the EB / HII / Other-US / Foreign POP % split.

Source
extracted/dod_announcement_pop.csv - one row per parsed announcement action
(action_date, piid, program_refined, work_type_primary, amount_usd, pop_*_site_pct).
Rows sorted $M descending.

Reads
- none (leaf module; loads its CSV and derives every flag in-sheet, no cross-sheet
  dependency)
- Classification knobs (Python, at load): gate = (is_sub_new_construction_tam in
  {yes/y/true/1}); gfe_excl = 1 if program in {sub_gfe_electronics, sub_gfe_components,
  bpmi_nuclear}; stream = AP_LLTM if work_type in {lltm_early_mfg, advance_procurement}
  else BC; scope_class in {EXCLUDE_GFE_NUCLEAR, EXCLUDE_GFE, INCLUDE_AP_LLTM, INCLUDE_BC,
  EXCLUDE_REVIEW}; confirmed = 1 for every row.

Feeds
- POP Source Audit (reads the ranges + gated-row register), TAM Build (per-stream POP
  coefficients), Sensitivity
- Producer accessors (the SUMPRODUCT operands, names unchanged from the former
  corpus_sheets): gate_range, gfe_excl_range, confirmed_range, stream_range,
  scope_class_range, program_range, pop_dollar_range, pct_range(which) for
  eb/hii/other/foreign; plus pop_row_cell(i,key), gated_row_cell(rank,key), n_gated()
- Excel table: tbl_sub_pop_parse

On the sheet
§1  At a glance: gated POP corpus
    - Same-sheet summary over the corpus ranges:
        Rows in corpus      = n_rows (count of parsed actions)
        Gated TAM actions   = SUMPRODUCT(gate_range)   (is_sub_new_construction_tam = 1)
        Gated TAM corpus $M = SUMPRODUCT(gate_range x pop_dollar_range)  ($-weighted pool)
        In-scope non-GFE $M = SUMPRODUCT(gate_range x (1 - gfe_excl_range) x dollar)
                              (the coefficient corpus)
        Confirmed in-scope $M = SUMPRODUCT(gate x (1 - gfe_excl) x confirmed x dollar)
                              (see POP Source Audit)

§2  POP corpus (658-row place-of-performance gate)
    - The native table tbl_sub_pop_parse, one row per CSV action, columns: Date, PIID,
      Program, Work Type, Scope Class, Stream, Gate, GFE/Excl, Confirmed, $M, EB %, HII %,
      Other US %, Foreign %. amount_usd is divided by 1e6 to $M; each POP % is divided by
      100 to a fraction. These columns are the ranges every coefficient SUMPRODUCT (here,
      POP Source Audit, TAM Build, Sensitivity) runs over.

Notes
- Native cell notes: none.
- Note column: none.
