POP Corpus
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_pop_corpus.py

Purpose
The gated award place-of-performance corpus that the BC supplier coefficient is
measured over (gated, non-GFE, confirmed actions, incl. MYP masters). The two
reconstructed MYP master rows lead the table (linked from Assumptions), followed by the
gated disclosed-announcement actions.

Source
extracted/dod_announcement_pop.csv  - DoD contract-announcement place-of-performance.
   Only actions flagged is_ddg_new_construction_tam (the gate) are kept; GFE/Excl = 1
   when program_refined starts "ddg_gfe_"; $ converted to $M; the four POP-site percents
   (BIW / Ingalls / Other US / Foreign) converted from percent to fraction; rows sorted
   by $ descending. Two MYP master rows are prepended ahead of the disclosed rows.

Reads
- Assumptions   MYP master $ (redacted) per yard [myp_master_cell], reconstructed POP %
           per yard x class [myp_pop_cell] - the two leading master rows link here
           (BIW = N00024-23-C-2305, Ingalls = N00024-23-C-2307)

Feeds
- TAM Build (the SUMPRODUCT operands behind every BC supplier coefficient), POP Source Audit
- Native table: tbl_ddg_pop_parse
- Promoted accessors: gate_range, gfe_excl_range, confirmed_range, stream_range,
  scope_class_range, program_range, pop_dollar_range, myp_master_range, pct_range
  (biw/ingalls/other/foreign), pop_first_data_row, pop_last_data_row, pop_row_cell,
  gated_row_cell, n_gated, n_myp_masters

On the sheet
§1  POP corpus (gated award place-of-performance)
    - Native table tbl_ddg_pop_parse, columns: Date, PIID, Prime, Program, Work Type,
      Scope Class, Stream, Gate, GFE/Excl, Confirmed, MYP master, $M, BIW %, Ingalls %,
      Other US %, Foreign %.
    - Master rows (myp_master = 1) carry green links: $M <- Assumptions myp_master_cell(yard);
      BIW/Ingalls/Other/Foreign % <- Assumptions myp_pop_cell(yard, class). Scope Class =
      INCLUDE_BC, Stream = BC, Gate = Confirmed = 1, GFE/Excl = 0.
    - Disclosed rows (myp_master = 0) are CSV input values; Scope Class = EXCLUDE_GFE
      when GFE/Excl = 1 (program starts ddg_gfe_) else INCLUDE_BC; Stream = BC for all
      gated DDG work; Confirmed defaults to 1.
    - The Gate / GFE-excl / Confirmed / $ / POP-% / MYP-master columns are exposed as
      ranges for the TAM Build coefficient SUMPRODUCTs.

§2  Field guide
    - Static field-meaning table: Gate (1 = DDG new-construction TAM action), GFE/Excl
      (1 = ddg_gfe_* dropped from the coefficient), Confirmed (1 = manual-review
      confirmed, default 1), MYP master (1 = reconstructed $-redacted master, linked from
      Assumptions), Scope Class (INCLUDE_BC / EXCLUDE_GFE action-level arbiter), Stream (BC).

Notes
- Native cell notes: none.
- Note column: none.
