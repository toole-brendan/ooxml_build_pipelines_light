# 2026-06-26 — Refresh deck_primary slide modules to the updated TAM + SAM workbooks

Pipeline: `projects/distributed_shipbuilding/deck_primary/`
Output:   `…/deck_primary/20260610_Distributed Shipbuilding New Construction_vS.pptx`
Build:    `cd deck_primary && python3 build_deck.py`  → `(8 slides, 5 charts)`
Sources:  TAM `tam/master/workbook_master_tam` · SAM `sam/sam_awards_data/workbook_award_classification_refactor`

## Why

Both upstream workbooks changed materially since the deck was last built:
- **TAM**: FY2028–31 outyear outsourcing-growth assumption → 30% HII outsourcing-hours growth,
  compound-ramped to full effect at FY2031, with a **DDG-51 BIW carve-out** (only HII's 55% share
  grows). Lowers DDG-51 outyear BC-TAM vs. the deck's stale (pre-carve-out) values.
- **SAM**: work-type classification **completely replaced** — the 7 NAICS-4 buckets are gone, now
  two published archetype axes (Capability Domain D0–D11, Primary Output P0–P6) + a DDG SWBS
  dimension; scope narrowed to hull-builder-only (GDEB subs; GD-BIW + HII-Ingalls DDG).

## Outcome (nothing committed; changes staged)

Deck still builds green `(8 slides, 5 charts)`. All slide rIds + chart rels resolve both
directions; all 8 modules `py_compile` clean. No PNG pass — **eyeball owed** (below). Source-of-
truth numbers were re-verified by **recalcing both workbooks headless** via soffice
(`OOXMLRecalcMode=0`, per memory `workbook-recalc-verification`) and reading the computed sheets.

| Slide | Module | Change |
|---|---|---|
| 8 | `data_reference` | 7 NAICS buckets → **two-axis taxonomy** (D0–D11 + P0–P6, side-by-side tables, defs from `_taxonomy.py`); in-scope PIIDs → hull-builder scope (`prime_contract_scope.csv`: Va 6 / Col **1** / DDG 13); award sample's out-of-scope Scot Forge row swapped to its in-scope record under N0002417C2117; title/sources/docstring updated. Pure `table()` text edit. |
| 3 | `outsourced_bc_annual_tam_ref` | **DDG-51 FY2028–31** bars re-pointed to the new compound-ramp + BIW carve-out high values (577.4 / 613.7 / 980.9 / 1051.5 $M, FY26$); each bar's **total held constant** (only the outsourced/retained split + penetration mirror move; total labels 3.9/4.0/6.1/6.3 unchanged). Patched `slide03_chart4.xml` numCache (idx 24/28/32/36, both series) + `CHART_POINTS`. Va/Col already tie to workbook high (Va within ~$2M, left). |
| 2 | `worktype_by_program` | **Rebuilt**: bundled think-cell chart → native `column_chart(stacked)` with **12 Capability Domains** + right legend. Values = SAM domain share (recalced Domain Concentration) × program TAM cumulative; column totals preserved exactly (**6.42 / 4.51 / 13.64 $B**). Neutral title. Old overlay (`slide02.xml`) + 7-stage NAICS ledger (`slide02_tables.xml`) retired. |
| 5 | `worktype_by_fy` | **Rebuilt**: → native `column_chart(percent)`, **12 program-year bars** (DDG-51/Va/Col × FY22–25) × 12 domains, right legend. Values = net subaward $M per (program, FY, domain) from recalced Supplier-Year Activity; each bar normalized to 100%. Neutral title. Old overlay (`slide05.xml`, incl. $-total + penetration strip) retired. |
| 1 | `outsourced_bc_walk` | **Verify-only, no change.** Walk is FY22–27 cumulative; outyear TAM change doesn't touch it. Endpoints re-confirmed against recalced TAM: Va 13,636.3 + Col 4,507.1 = **$18.1B sub pool**; DDG **$6.4B**. |
| 4, 6, 7 | placeholders / methodology Qs | Untouched (out of scope for the data refresh). |

## Decisions taken (user-confirmed)
- Slides 2 & 5 show **all 12 domains** (not condensed) and use **neutral/descriptive titles**.
- Slide 5 uses the **aligned FY22–25** cut for all three programs (12 bars). NB: an earlier
  "DDG-51 has $0 in FY22–25" read was a **label bug** ("DDG" vs "DDG-51" across SAM sheets) — DDG-51
  does have FY22–25 data; corrected before building.

## Mechanism notes
- `column_chart()` returns the same `{chart_xml, embed_xlsx, chart_rels}` dict the build wires like
  `editable_bundled_chart`; its embedded `.xlsx` is **in sync** (factory-built). For slide 3, only
  the bundled `slide03_chart4.xml` numCache was patched — its `.xlsb` stays verbatim (render reads
  the cache; "Edit Data" shows stale source — documented, accepted).
- Bundled-chart series/category **labels live in the overlay** (`slideNN.xml`), not the chart XML —
  why slides 2/5 were re-authored with primitive chrome + native legend rather than hand-patched.

## Eyeball owed (no PNG run — standing preference, memory `awards-deck-visual-qa`)
- **Slide 8**: two side-by-side D/P tables + award sample must fit above the sources line; Columbia
  shows a single in-scope PIID (intentional, annotated). Check row-wrap / vertical fit.
- **Slide 2**: 12-domain right legend + 3 stacked bars — legend fit / readability.
- **Slide 5**: 12 program-year bars + right legend, percent-stacked — bar/label density; the
  per-bar **$ total + penetration-% annotations were dropped** (can be re-added as an overlay).
- **Slide 3**: DDG-51 outyear bars shifted ~1–2px (split only) — a glance.

## For the next agent
- Slides 2/5 dropped the old methodology ledger / penetration strip; if wanted, re-author them to
  the new D/P method (not the retired NAICS one).
- SAM sheets are inconsistent on the DDG program label (**"DDG"** in Supplier-Year Activity vs
  **"DDG-51"** in Where to Play) — match carefully when aggregating.
- Recalced workbooks (scratch): TAM/SAM `…/scratchpad/{tam,sam}_recalc/*.xlsx`.
