# 2026-06-04 — Workbook deck-loader standardization: one wide-block "Chart Data" sheet per workbook, Slide Data removed

## Scope

Standardized the two workbooks' deck-loader sheets (`projects/{ddg,submarines}/workbook/
workbook_*/sheets/`) onto a single, shared shape. The two `z_ChartData` tabs had diverged
into two different data models, and submarines additionally carried a separate `Slide Data`
tab. Collapsed both to **one wide-block "Chart Data" sheet per workbook**, restricted to the
charts that actually render, with values kept as live producer-cell links.

This session was preceded by a read-only investigation (see §0) that established the
deciding fact: **the deck loader is consumed by nothing** — so these sheets could be
reshaped with zero build risk. No `workbook_core` changes; no formula/value edits to any
model/data sheet. Workspace is not under git; the safety net was a green `build_workbook.py`
(both decks) plus `validate_workbook.py` (DDG) after each change.

Decisions carried in from the user:
- Collapse to **one sheet** ("Chart Data" / `z_ChartData`), **DDG's wide-block shape**
  (categories down col B, series across) — the literal layout of a chart.
- **Delete Slide Data** (submarines only); **drop the manifest**.
- **One block = one chart that actually renders**; drop shape-table / non-chart exhibits.
- **Keep source-linking** (every value an `=` link to a producer cell).
- Proceed with the **current** rendered chart set ("assuming same charts, we can always
  update later") rather than waiting for a finalized list.

---

## 0. Investigation — is the deck loader used? (no)

Every `xlsx`/`workbook` reference in the deck code is the **self-contained mini-workbook
embedded inside each native chart** (PowerPoint's "Edit Data"); `deck_core/charts.py` states
it outright ("no link to sub_workbook/sub.xlsx"). Confirmed:
- No deck code imports `csv`/`openpyxl`/`load_workbook` or reads the produced `.xlsx`.
- Nothing references `z_ChartData`, `tbl_deck_chart_data`, `tbl_deck_slide_data`, or the
  manifest. Deck charts hardcode their numbers as Python literals in the slide modules.

Also found the decks had **grown since the last logs**: the S12-S16 SAM/supplier section is
now built and registered in both, so the real chart counts are higher than the 7/5 noted
earlier (~10 DDG modules / 9 subs modules carrying `CHARTS`). Used each deck's
`slides/__init__.py` registry + the `CHARTS`/chart-factory usage as the source of truth for
"which charts actually render."

## 1. DDG Chart Data — trim to chart-backing blocks, drop the manifest

`projects/ddg/workbook/workbook_ddg/sheets/chartdata_z_chart_data.py`:
- Removed the 3 **non-chart** blocks: `CD01` (KPI tiles), `CD11` (exec-quote shape-table),
  `SD12` (implications scorecard) — and the `_load_quotes` CSV loader they needed.
- Removed the `tbl_ddg_chart_manifest` native table, `_MANIFEST_HEADERS`, and the two-pass
  splice; render is now a **single pass** (sheet title -> §1 banner -> blocks).
- Kept **CD02-CD10** (9 wide blocks, one per rendered chart), still source-linked. CD10
  FFATA gap stays CSV-fed (`cost_funnel_summary.csv`) — it has no model producer.
- Pruned now-dead imports (`col_letter`, `ExcelTable`, `avg_annual_tam_cell`); the sheet now
  carries **no native table** (`WorksheetSpec(ws)`).

Block -> chart map: CD02 executive_summary (stacked bar), CD03 cost_funnel, CD04 myp_redaction
(its two charts share one block), CD05 annual_tam_build (waterfall), CD06 tam_timing,
CD07 work_type_allocation, CD08 sam_scenarios, CD09 supplier_landscape, CD10 ffata_visibility_gap.

## 2. Submarines Chart Data — long table -> DDG wide blocks (and made it a leaf)

`projects/submarines/workbook/workbook_submarines/sheets/chartdata_z_chart_data.py`:
- **Kept `_build_specs` (the producer links) and just changed the render**: pivot each
  CD_* block's `(category, series, value)` rows into a wide block (categories down col B,
  series across), preserving first-seen order. Lowest-risk path — links are unchanged and
  still pass `assert_links()`.
- Dropped **CD_A6** (SAM bucket crosswalk — a table, not a chart) and the §1 at-a-glance
  rollup. Result: **10 wide blocks**, one per rendered chart (CD_07-11, CD_13-16, CD_A5).
- Simplified the spec tuple to `(cid, cat, series, kind, payload, unit)` (dropped the
  long-table-only `slide`/`label`/`role`/source columns); added a `_BLOCK_META` map of
  per-block title + category-column header.
- Removed `chart_audit_links()` / `_producer_tab` / `_FIRST_DATA` / `_VALUE_COL`, making the
  sheet a **pure leaf** like DDG.

## 3. Number Audit — drop the §4 chart tie-out (subs)

`validation_number_audit.py` (subs) imported `chart_audit_links` and built a §4 "Chart Data
tie-out" (chart value vs producer). Since every chart value is `=<producer ref>`, the tie-out
was **tautological** (delta always 0) and only coupled the audit to the chart-data layout.
Removed the import + the §4 section. DDG's Number Audit never had this — so this aligns subs
to DDG. No row-count assert depended on §4; build stays green.

## 4. Delete the Slide Data sheet (subs)

`outputs_slide_data.py` held only non-chart exhibits (KPI cards, timeline, bullet steps,
taxonomy tags, scorecard) and was consumed by nothing. Deleted the module, its spec
(`sheet_specs/outputs_slide_data.md`), and the 2 registry lines in `sheets/__init__.py`. The
`outputs` group stays contiguous (now just Figure Register). Subs drops 21 -> **20 tabs**.

## 5. Specs

Rewrote both `sheet_specs/chartdata_z_chart_data.md` to the new wide-block / real-charts-only
/ no-manifest / leaf shape (block -> rendered-chart map, source-linking rule, the removed
exhibits, and the known minor divergences). Deleted the subs `outputs_slide_data.md` spec.

---

## Verification

| Check | DDG | Submarines |
|---|---|---|
| `build_workbook.py` | green — 24 tabs | green — 20 tabs (was 21) |
| native tables | 11 (was 12; manifest dropped) | 10 (was 12; both loader tables dropped) |
| `validate_workbook.py` | 70 parts, **0 xml errors, 0 error-literal cells** | (no validator) |
| rendered z_ChartData | CD02-CD10 present; CD01/CD11/SD12 + manifest gone; CD10 CSV-fed; all else `=` links | 10 wide blocks; CD_13 derived `=bucket_tam/n_years` works; CD_15 vendor-name categories render as col-B formulas; CD_A5 two-unit series fills each measure's own column |
| dead-reference sweep | clean (`chart_audit_links` / `tbl_ddg_chart_manifest` / `tbl_deck_slide_data` / `outputs_slide_data` / `SLIDE_DATA` / `_load_quotes`) | clean |

## Files touched

- **DDG:** `workbook_ddg/sheets/chartdata_z_chart_data.py`, `sheet_specs/chartdata_z_chart_data.md`.
- **Subs:** `workbook_submarines/sheets/chartdata_z_chart_data.py`,
  `workbook_submarines/sheets/validation_number_audit.py`, `sheets/__init__.py`,
  `sheet_specs/chartdata_z_chart_data.md`; **deleted** `sheets/outputs_slide_data.py` +
  `sheet_specs/outputs_slide_data.md`.
- No `workbook_core`, no model/data sheet, no README, no build-script changes.

## Open items / follow-ups

- **Mirror, not a live feed.** Both sheets are hand-maintained mirrors of the deck charts;
  regenerate the affected blocks whenever the deck's **rendered chart set changes** (the
  reason the user said "assuming same charts, update later").
- **Block-vs-literal-chart divergences (DDG), left for a later pass:** CD03 lists the full
  SCN funnel where the chart collapses to 3 bars; CD04 backs both `myp_redaction` charts in
  one block; CD09 lists top-12 where the chart shows top-10. Noted in the DDG spec.
- **Column harmonization.** DDG blocks still carry annotation columns (Note / Display label /
  Treatment) the leaner subs blocks omit; harmonize if pixel-identical blocks are wanted.
- **Audit gates** (QA Reconciliation / Number Audit "0 FAIL") are runtime Excel formulas —
  not evaluated here; this session changed no formula/value, and DDG validate shows 0
  error-literal cells, so they should be unaffected. Confirm in Excel for final sign-off.
