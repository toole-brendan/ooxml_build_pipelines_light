References
Tab color: 1F3A5F (navy)  ·  group: Sources
Module: sources_references.py

Purpose
Industry-baseline primary-source claims and executive make/buy commentary behind the
model and the deck's source lines, as two native tables plus a citation-completeness
rollup. Leaf module (loads its CSVs); long quote text is held in the cell, not sized
into the workbook.

Source
extracted/industry_baseline_citations.csv - primary-source claims (claim_id, label,
  value, unit, source_id/date/title/url, quoted_text); value coerced to int/float when
  numeric, else kept as text.
extracted/exec_commentary_makebuy.csv - executive quotes (quote_id, date, speaker, role,
  company_or_org, topic, quote_or_statement, source_url_or_doc).

Reads
- none (standalone leaf; loads its own CSVs, links no sibling sheet)

Feeds
- none (reference content; not consumed by another tab)
- Native tables: tbl_sub_references_claims (§1), tbl_sub_references_exec (§2)

On the sheet
§1  Industry-baseline primary-source claims (anchors the 50/60/65% band)
    - tbl_sub_references_claims, one row per CSV claim (Claim ID, Label, Value, Unit,
      Source ID, Date, Source title, Source URL, Quoted text). Numeric Value cells use the
      input number style; non-numeric values fall back to text.

§2  Executive commentary on make/buy (strategy signal, not sizing)
    - tbl_sub_references_exec, one row per CSV quote (Quote ID, Date, Speaker, Role,
      Company, Topic, Quote, Source URL). Editorial signal, not a sizing input.

§3  Citation completeness
    - Rollup table (Citation family, Count, Missing URL count, Notes):
        - Primary-source claims  = len(industry CSV); missing = rows with blank source_url
        - Executive commentary   = len(exec CSV); missing = rows with blank source_url
        - Budget exhibits        = 3, missing 0 (see Source Index)
        - Methodology documents  = 4, missing 0 (see Source Index)

Notes
- Native cell notes: none.
- Note column: §3.
