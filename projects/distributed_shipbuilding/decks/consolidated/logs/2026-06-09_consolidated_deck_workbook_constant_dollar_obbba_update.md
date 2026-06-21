# 2026-06-09 — Consolidated deck + chart workbook: constant FY2026 $ + OBBBA restate

## What

Brought the consolidated deliverables (`projects/consolidated`) in line with the two
program workbooks after the same-day deflator conversion and OBBBA Sec. 20002
integrations. Both the think-cell chart workbook
(`workbook_consolidated/sheets/z_chart_data.py`) and the deck slide modules
(`deck_consolidated/slides/`) were hardcoded from pre-deflator, pre-OBBBA outputs
(DDG even pre-deflator nominal: annual TAM summed to 3,438.6).

Source of truth: rebuilt both program workbooks, recalc'd via headless LibreOffice,
read cached values from their z_ChartData / Executive Summary / SCN Budget / Entity
Master tabs.

## New numbers (constant FY2026 $, OBBBA on)

- Combined TAM: $4.2B/yr, $25.2B cum (was $3.9B / $23.3B)
- Combined broad SAM: $3.5B/yr, $21.2B cum (was $3.3B / $19.7B)
- DDG TAM $659M/yr, $4.0B cum; sub TAM $3.5B/yr, $21.2B cum (~84% of combined)
- Residual $653M/yr; modular $408M/yr
- Annual cadence totals: 2.1 / 2.5 / 6.1 / 2.6 / **6.2** / 5.7 — FY2026 is now the
  peak year (OBBBA two DDGs + second Virginia boat + DDG AP/LLTM spike), replacing
  the old "FY2024/FY2027 peaks, FY2026 exception" story
- Work-type combined: 1,353 / 710 / 633 / 375 / 206 / 162 / 102
- Scenario SAM: broad 3.54, HM&E 2.54, electrical 1.35, metal 1.17, modular 0.408
- Unchanged (verified, not assumed): supplier shares (13% / 35%, POP anchors),
  AP/LLTM $208M/yr, visibility evidence ($2.7B / $13.6B / $5.5B), classifier counts

## OBBBA presentation decisions

- DDG folds OBBBA into its BC base, tagged: "BC construction base $21.5B (incl.
  $3.4B OBBBA mandatory, Sec. 20002(17))" — mirrors the DDG workbook.
- Submarine shows a $60.6B base "incl. $2.7B OBBBA mandatory (Sec. 20002(16))" so
  the visible × 35% = $21.2B math holds (the program workbook runs OBBBA as its own
  stream; on the slide the base is combined to keep the 4-card stack).
- z_ChartData §5 carries the OBBBA BC base as its own column (57.888 / 2.677 /
  21.212 / 0.0); §4 DDG bridge base relabeled "(P-5c + OBBBA)".
- Cost funnels (s05, z §2-§3) stay P-5c-scope; card 3 notes the mandatory awards
  are additive and enter at the TAM bridge.
- "(4) FY 2026 Mandatory Funding Allocation Plan, PL 119-21 Sec. 20002" appended to
  sources on s02/s05/s09/s11 and appendix M2/M3.

## Files touched

- Workbook: `z_chart_data.py` (all §§ except §6/§10; docstring basis note).
- Deck: s02, s05, s08 (one $3.9B headline mention), s09, s11, s12, s13,
  appendix_tam_budget_base_scope_gates, appendix_supplier_share_pop_conversion,
  appendix_sam_allocation_scenario_views. Unchanged: cover, dividers, s04, s06,
  s10, s14, appendix roadmap + classifier.
- Axis maxima raised with the data: s02 4.0→4.5, s05 DDG 30→35, s11 6→7 (major
  0.5→1), s12 1300→1500, s13 3.5→4.0. s11 DDG chip points [0] → [0, 5] (FY27 cap
  now too thin at the taller axis).
- s12 per-program ints chosen so stacks sum to the true rounded totals
  (sub machining 116 + DDG 259 = 375; sub 116.6 displayed as 116).

## Verification

- Consolidated workbook: build + validate (0 xml errors, 0 error cells), soffice
  recalc, full-tab dump cross-checked (bridge identities, annual sums, residual).
- Deck: build_deck.py (21 slides, 6 charts) → PDF → PNG QA of s02/s05/s09/s11/
  s12/s13 + appendix 18/19/21: overlay totals track new bar tops, funnel
  connectors land on running totals, M2 ledger clears the AP/LLTM strip with the
  longer row-1 text.

## Notes

- Rounding tension kept deliberately: DDG AP/LLTM cum displays $1.2B (true 1.248)
  although card math "$1.5B × 85%" visually suggests 1.3; matches the workbook.
- Combined broad SAM cum ($21.2B) and sub TAM cum ($21.2B) are coincidentally
  identical at one decimal; they never appear on the same slide today.
- PB28 tripwire (program workbooks) still governs: if a future P-5c vintage folds
  the mandatory ships in, the OBBBA adds must be netted and this deck re-stated.
