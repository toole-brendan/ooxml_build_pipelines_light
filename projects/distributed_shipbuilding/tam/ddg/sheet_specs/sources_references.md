References
Tab color: 1F3A5F (navy)  ·  group: Sources
Module: sources_references.py

Purpose
Primary-source pulls and policy/industry citations behind the model and the
deck's source lines. The source / citation registry. A source table (the
context-note exception), so it keeps short context notes.

Reads
- none (standalone citation registry; rows are literal source records)

Feeds
- none (producer accessor source_ref_cell is internal hygiene only)
- Native tables: tbl_ddg_references_primary, tbl_ddg_references_citations

On the sheet
§1  Primary sources & data pulls
    - Native table (tbl_ddg_references_primary), columns: Source ID, Document / dataset,
      Type, Date, Location / reference, Context note.
    - SRC-01..SRC-14: the budget books (P-5c/P-10/P-40), the extracted SCN cost-category
      and production-schedule CSVs, DoD announcement POP (with redacted MYP master $),
      FPDS de-capped prime pulls, SAM.gov FSRS subawards, vendor/NAICS enrichment, the
      scope-summary JSON, cost-funnel CSV, EDGAR segment filings, and the exec-quote CSV.
    - Context notes name the downstream consumer (e.g. "Feeds TAM Build", FFATA ~15%
      floor, ~35% NAICS lookup-fail) - prose, no formulas.

§2  Policy & industry citations
    - Native table (tbl_ddg_references_citations), same columns.
    - CITE-01..CITE-05: the MYP master totals (BIW 2305 ~$6.40B + Ingalls 2307 ~$8.18B,
      reconstructing the ~$14.58B redacted masters; outside-yards 87% -> ~33%), the CRS
      DDG-51 program report, GAO shipbuilding assessments, the Navy 30-Year Shipbuilding
      Plan, and the internal methodology/spec docs.

Notes
- Native cell notes: none.
- Note column: none.
