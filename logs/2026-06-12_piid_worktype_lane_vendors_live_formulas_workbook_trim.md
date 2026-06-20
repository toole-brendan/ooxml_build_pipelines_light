# 2026-06-12 (later session) — PIID x Work Type tab, flow fixes, live % formulas, workbook trim

## Goal

Five asks in sequence on the Award Analysis workbook
(`20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`,
pipeline `projects/consolidated/workbook_award_analysis/`):
(1) does it cover subaward counts / timing / vendor-repeat / vendor-overlap
by work type per PIID — it covered none, so add them; (2) structural +
sheet-to-sheet flow review and fixes; (3) trim: delete the directory section,
Data Notes and Source Index tabs, hide Tie-Outs; (4) **"FIX THE % VALUES"** —
no hardcoded percentages; pull the underlying data in and make them live
formulas; (5) count cells must not render with a ".0" decimal — integer
formats for record/vendor counts.

## 1. PIID x Work Type tab (the four coverage asks)

- New extract `wb_piid_worktype.csv`: one row per (program, piid, work_type)
  supplier lane — per-FY record counts (≤FY12 + FY13–26), first/last award,
  n_vendors, repeat_award_share, shared_vendor_pct, dollars_total. 132 lanes
  (61 subs across 10 PIIDs / 71 ddg across 11). User-confirmed definitions:
  **Repeat % = repeat-award share** (lane records to vendors with >1 record in
  the lane); **Shared % = per-PIID shared vendor %** (lane vendors also on the
  same work type on ≥1 other same-program PIID). Extraction asserts lane
  counts tie to wb_annual_worktype per (program, work_type, FY column) exactly.
- New sheet `data_piid_worktype.py`, tab `PIID x Work Type` (ASCII x), after
  By PIID. Zero-record PIIDs have no lanes (basis note points at By PIID).
- Headline lane: Columbia piping on N0002417C2117 — 77 vendors,
  repeat 99.5%, shared 87%.

## 2. Flow audit + fixes (user asked "does it build sheet to sheet, any redundancy?")

- Verdict: tab order correct (each data tab adds one dimension, reuses earlier
  vocabulary); the cut overlaps are deliberate roll-ups that power Tie-Outs,
  nothing removable. Three real defects, all fixed:
- **Count-basis inconsistency**: By PIID "Records" was ALL-roles (data_status
  basis) while the lanes are supplier-only — N0002418C2307 reads 2,612 vs
  2,358 with no explanation. By PIID now carries both columns ("Records (all
  roles)" + "Supplier records", `n_records_supplier` added to wb_annual_piid)
  with an on-sheet basis note.
- **$ thread dead-ended**: lanes were counts-only → blue "$M (full hist)"
  lane column added (extraction `dollars_total`), program total live-summed.
- **Overview didn't orient**: gained §1 "Corpus shape at a glance" — supplier
  $M / records as green links to the By Work Type producer cells; vendor
  counts (924 subs / 487 ddg), PIIDs with records ("10 of 15" / "11 of 24"),
  first/last subaward (2013–2025 subs / 2001–2026 ddg) as S_DEFAULT metadata
  computed at build time from the loaded extracts.
- Tie-Outs grew to **6 dollar legs** (+ lane $M) and **5 count legs**
  (Overview supplier records, By Work Type, By PIID supplier records,
  PIID x Work Type, By Vendor SUMIF), counts checked with exact equality.
  Engine canon respected: no frozen panes (locked out), no hyperlinks
  (green links are the house navigation idiom).

## 3. Trim (user direction)

- Overview "§2 - What's in this workbook" directory **deleted** (added in §2
  work above, removed same session); role grids renumbered §2/§3.
- **Data Notes and Source Index tabs deleted** — modules removed from the
  registry and the files deleted (`guide_data_notes.py`,
  `sources_source_index.py`). Key definitions survive as on-tab basis notes
  on By PIID / PIID x Work Type. NOTE: not a git repo — the deleted notes
  content lives only in this conversation + older builds.
- **Tie-Outs built hidden.** workbook_core had no visibility support → added
  additively: `SheetEntry.hidden: bool = False` (tables.py),
  `build_workbook_xml(..., hidden=[...])` emits `state="hidden"`, packager
  collects flags + guards ≥1 visible sheet (lib.py). Other pipelines
  unaffected (defaulted field / optional param).

## 4. Live % formulas (the loud one)

- User: hardcoded %s unacceptable — pull data in if needed. Root issue: Repeat
  % / Shared % need vendor×lane detail that was on no sheet.
- New extract `wb_vendor_lane.csv` (2,897 rows): one row per (program, piid,
  work_type, vendor) with n_records + dollars. New tab **Lane Vendors**
  (`data_vendor_lane.py`, after PIID x Work Type) — native table `VendorLane`,
  blue Records/$M, plus a LIVE per-row "PIIDs w/ work type" column
  (`=COUNTIFS` over the table itself: same program + work type + vendor UEI =
  the vendor's distinct-PIID footprint, rows being unique per PIID), live
  SUMIF program totals below.
- PIID x Work Type **Vendors / Repeat % / Shared % are now black live
  formulas** keyed on each row's own PIID (B) + Work Type (C) cells:
  Vendors `=COUNTIFS(lane)`; Repeat `=SUMIFS(rec,lane,rec,">1")/SUMIFS(rec,lane)`;
  Shared `=COUNTIFS(lane,np,">1")/COUNTIFS(lane)` — ranges promoted by
  `vl_cols()` from data_vendor_lane. The CSV's n_vendors/repeat/shared columns
  remain script-side reconciliation only.
- **Verified by simulation**: re-computed the exact COUNTIFS/SUMIFS semantics
  in Python from wb_vendor_lane.csv → 132/132 lanes match the script-side
  values; Excel recalcs on open (engine sets fullCalcOnLoad/forceFullCalc).
- Memory written: `derived-metrics-live-formulas` (never hardcode derived
  metrics; pull inputs in as a sheet and derive live).

## 5. Integer formats for count cells

- User: counts shouldn't render "1,527.0". The engine had only the universal
  1-decimal numFmt 164 → added **numFmt 168** (`#,##0;-#,##0;"-"`, zero as
  dash) + six styles to `workbook_core/styles.py`: `S_INT` / `S_INT_INPUT` /
  `S_LINK_INT` + the three `*_TOTAL` bordered variants, wired into
  `BORDER_TOP_FOR`. Append-only — other pipelines untouched.
- Swapped onto every count cell in all three color roles: Overview Records
  column + Total-reported records + §1 records links; By Work Type count
  grids + totals; By PIID both record columns + totals; PIID x Work Type FY
  count grid, row/program count totals, Vendors COUNTIFS; Lane Vendors
  Records + PIID-footprint + records SUMIF; By Vendor Records + records
  SUMIF; Tie-Outs §2 legs. Dollars / percentages unchanged (decimal is
  meaningful there) — By Vendor now intentionally mixes integer Records with
  decimal $ columns. Verified with a 25-point openpyxl format audit (INT vs
  DEC + font color per cell, all pass).

## Lessons / mechanics worth keeping

- Cross-sheet COUNTIFS criteria must match CELL TEXT exactly — both sheets
  render work type via the same `BUCKET_NAME` display map, and lane formulas
  reference the row's own B/C cells as criteria, so the match is structural.
- `total_row()` RAISES on a style missing from `styles.BORDER_TOP_FOR` — any
  new base numeric style needs its top-bordered `*_TOTAL` variant + map entry
  in the same change, or builds break at the first total row carrying it.
- One SHEETS item = one tab in the packager, so per-sheet flags (hidden) ride
  as a parallel list collected via `getattr(item, "hidden", False)` — works
  for SheetEntry and legacy module items alike.
- Overview can import producer accessors from data sheets (no cycle — data
  sheets only import _cuts/core); registry order ≠ import order.
- PIIDs are unique across programs, so lane formulas need no program
  criterion; the Lane Vendors footprint column does (it's per-program).

## State / open items

- Final shape: **8 tabs** — Overview, By Work Type, By Vessel, By PIID,
  PIID x Work Type, Lane Vendors, By Vendor, Tie-Outs (hidden). 7 extracts.
  Build: 0 xml errors, 0 error literals, 2 native tables. User visually
  verifies (no PNG renders, per standing rule).
- Regeneration flow unchanged: `extract_workbook_cuts.py` →
  `build_workbook.py` (→ `validate_workbook.py`).
- Carried from earlier 06-12 log: Phase F deck fill still gated on memo
  review (basis choice open); workbook-side entity_naics_lookup.csv copies
  still unsynced (282 lookups); FY2025–26 will grow with FFATA lag — re-pull
  → re-extract → rebuild.

## Files

New: `projects/consolidated/workbook_award_analysis/workbook_award_analysis/sheets/{data_piid_worktype,data_vendor_lane}.py`,
`projects/consolidated/workbook_award_analysis/extracted/{wb_piid_worktype,wb_vendor_lane}.csv`,
repo memory `derived-metrics-live-formulas`.
Modified: `projects/consolidated/research/scripts/extract_workbook_cuts.py`
(lane/vendor-lane aggregation, n_records_supplier + dollars_total columns,
3 new recon assertions), sheets `{__init__,summary_overview,data_by_worktype,data_by_piid,data_by_vendor,validation_tie_outs}.py`,
`workbook_core/{tables,lib}.py` (hidden-sheet support, additive),
`workbook_core/styles.py` (numFmt 168 + S_INT/S_INT_INPUT/S_LINK_INT +
*_TOTAL variants + BORDER_TOP_FOR entries, additive),
`projects/consolidated/20260612_Distributed Shipbuilding Award Analysis_vS.xlsx` (rebuilt).
Deleted: sheets `{guide_data_notes,sources_source_index}.py` (tabs Data Notes,
Source Index).
