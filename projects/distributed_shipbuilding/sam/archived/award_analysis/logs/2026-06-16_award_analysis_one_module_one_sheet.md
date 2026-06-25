# 2026-06-16 — Award Analysis workbook: restore 1 module = 1 rendered sheet

Pipeline: `projects/distributed_shipbuilding/workbook_award_analysis/`
  (note the nested package: `workbook_award_analysis/workbook_award_analysis/sheets/`)
Output:   `projects/distributed_shipbuilding/20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`
Build:    `python3.12 build_workbook.py` → `python3.12 validate_workbook.py`
  (run from the outer `workbook_award_analysis/`; system `python3` is 3.9 / no openpyxl)

## Goal

The user prefers the house convention every sibling pipeline follows (ddg /
submarines / mro: *"ONE module per rendered sheet"*), but the 8-tab refactor
(`2026-06-16_award_analysis_8tab_refactor_steps3-6`) had left **more sheet
modules than rendered sheets**. Restore the strict 1:1 mapping **without changing
the rendered workbook**.

## The mismatch (diagnosed, not assumed)

The 8-tab split introduced a **block + aggregator** indirection:
- **13 "block" modules** exposed `render_block(c, tab, banner)` (no `render()`),
  rendering nothing on their own — they emitted rows onto a cursor handed in by an
  aggregator.
- **3 "aggregator" modules** (`data_indicators`, `data_market_views`,
  `data_detail_tables`) wrapped each block into a `SheetEntry` via
  `_section.section_tab()` and re-exported the blocks' accessor functions so
  `summary_overview` / `validation_tie_outs` kept a stable import path.

Net: **16 modules → 13 sheets**, plus `_section.py` existing only as block→aggregator
glue. The other 5 sheets (`summary_overview`, `summary_inputs`, `data_piid_worktype`,
`validation_tie_outs`, `summary_sources`) were already self-contained 1:1.

## Approach — explode each block into a self-contained sheet module

The target shape already existed in `data_piid_worktype.py`: a `_make_xxx()` that
builds the cursor at import, writes both banners, defines `render()` → `WorksheetSpec`,
returns `(SheetEntry, *accessors)`, assigned to module-level names. Converted all 13
blocks to that shape; deleted the 3 aggregators + `_section.py`; repointed consumers.

Per-block transformation (mechanical, body formulas untouched):
- `def render_block(c, tab, banner)` → `def _make_xxx()`; prepend the row-2 title
  banner + blank that `section_tab` used to write (`c.banner(_TAB, n_cols=len(_COLS),
  style=S_TITLE_SHEET)`); `banner`→module `_BANNER`, `tab`→module `_TAB` (the §N
  banner string and the owning-tab name are now module constants).
- return-dict → a `render()` closure returning `WorksheetSpec(ws, tables=[table])`
  + `return SheetEntry(_TAB, _GROUP, render), *accessors`, then a module-level
  `(XXX, *accessors) = _make_xxx()`.
- New imports per block: `worksheet`, `WorksheetSpec`/`SheetEntry`, `group_color`,
  `S_TITLE_SHEET`, and the `TAB_*` constant. Class-A-only cuts (`data_by_worktype`,
  `data_by_vessel`) kept their module-level accessor `def`s and just gained a
  `SheetEntry`.

### Accessor rewiring (consumers now import straight from the owning block)

Every promoted accessor moved to the block that owns its sheet; the Class-B ones
(those closing over the section's own `tab`/rows) became module-level after the
`_make_*` wrap and now close over the block's own `_TAB` (same tab name → identical
cross-sheet refs). Repointed import sites:
- `data_detail_tables` → `data_lane_detail` (`ld_cols`/`ld_date_refs`),
  `data_vendor_lane` (`vl_cols`), `data_lane_vendor_fy`
  (`lvf_cols`/`lvf_total_cell`/`lvf_records_total_cell`), `data_role_detail`
  (`rd_cols`/`role_supplier_*`), `data_prime_calendar` (`prime_cols`).
- `data_market_views` → `data_by_worktype` (`wt_*`), `data_by_vessel`
  (`vessel_total_cell`), `data_by_piid` (`piid_total_cell`/`piid_sup_records_cell`/
  `piid_section_cols`), `data_by_vendor` (`bv_cols`/`vendor_total_cell`/
  `vendor_records_total_cell` — note `bv_cols` is "by **vendor**", not by vessel).
- `data_indicators` → `data_rebuy_timing` (`rb_due_count`),
  `data_concentrated_lanes` (`cl_concentrated_count`), `data_source_concentration`
  (`sc_emerging_count`).

Consumers touched: `summary_overview.py`, `validation_tie_outs.py`,
`data_piid_worktype.py` (+ the cross-block leaf imports in the cut/indicator
blocks). No new import cycles — the dependency direction (leaves ← cuts/indicators
← summary/checks) is unchanged; only the aggregator middleman is removed.

### Registry + deletes

`sheets/__init__.py` rewritten to import all 18 sheet modules and register each
`SheetEntry` directly in the same order, preserving group contiguity
(summary → inputs → model → data → validation → sources, asserted by
`package_workbook`). Docstring updated to "ONE module per rendered sheet". Deleted
`data_indicators.py`, `data_market_views.py`, `data_detail_tables.py`, `_section.py`.
Also refreshed the 13 blocks' module docstrings (dropped the stale "BLOCK
renderer / coordinator does the worksheet() call / re-exported by data_X" text,
which referenced the deleted modules and the retired `render_block` API).

## Result

`sheets/` now holds **18 sheet modules ↔ 18 rendered sheets (1:1)** + 5 underscore
helpers (`_cuts`, `_layout`, `_tabs`, `_taxonomy`, `_widths`) + `__init__.py` —
matching the ddg / submarines / mro convention. Net file change: −4.

## Verification (pure refactor — output proven unchanged)

- Captured a **baseline build before any edit** (`/tmp/wb_baseline`) and a per-part
  sha256 manifest of the unzipped .xlsx.
- Rebuild after the refactor: **18 sheets, 14 native tables, 55 parts, 0 xml errors,
  0 error-literal cells** — identical counts, same tab order, and every per-sheet
  byte size matches the baseline exactly.
- **Structural diff vs baseline: the only part that changed is
  `docProps/core.xml` (the build timestamp). 0 of the `xl/worksheets/*.xml` and
  `xl/tables/*.xml` parts differ** — byte-for-byte identical. So Tie-Outs/Checks
  read exactly as before (per-program $ virginia 4343.6 / columbia 3342.2 /
  ddg 3095.4; records 7725 / 5281 / 5741). Re-diffed after the docstring pass —
  still only core.xml.
- `py_compile` clean on all 13 converted modules; final grep confirms **no residual
  references** to `render_block` / the deleted aggregators / `_section` / `section_tab`.

Final OK/FAIL of Tie-Outs is the user reopening in Excel (caches the recalc), as
before — no headless recalc step.

## Files

- **converted (13)** `sheets/`: `data_lane_detail.py`, `data_vendor_lane.py`,
  `data_lane_vendor_fy.py`, `data_role_detail.py`, `data_prime_calendar.py`,
  `data_rebuy_timing.py`, `data_concentrated_lanes.py`,
  `data_source_concentration.py`, `data_program.py`, `data_by_worktype.py`,
  `data_by_vessel.py`, `data_by_piid.py`, `data_by_vendor.py`
- **edited (consumers/registry)** `sheets/__init__.py`, `summary_overview.py`,
  `validation_tie_outs.py`, `data_piid_worktype.py`
- **deleted (4)** `sheets/data_indicators.py`, `data_market_views.py`,
  `data_detail_tables.py`, `_section.py`
- No `workbook_core/` changes; no research/extract changes.

---

## Follow-up (same session) — group naming + tab-color audit vs the siblings

The user asked whether the sheet **groupings / tab colors** are set up the best
way and to compare the two sibling workbooks (`submarines/workbook`,
`ddg/workbook`).

### Findings

- **Group assignments are correct and sibling-aligned.** The shared taxonomy
  (`workbook_core/groups.py`) defines `model` = "the calc / analysis engine … or a
  set of derived analytical cuts" and `data` = "extracted source evidence". Both
  siblings follow `summary → guide → inputs → model → data → outputs → validation
  → sources → chartdata`, with `data` = leaf CSV tables and `model` = the live
  calc engine (TAM/SAM/Outlook). Award analysis maps cleanly: `data` = the 5
  hardcoded leaf tables; `model` = the 9 derived analytical cuts (Supplier Lanes +
  3 indicators + 5 market views). No sheet is misgrouped. (Skipping
  guide/outputs/chartdata is correct — workbook-only, no deck, methodology in the
  `_20260615.md` docs.)
- **Tab colors are already fully aligned — nothing to change.** Every sheet uses
  `tab_color=group_color(_GROUP)` (verified: **zero hardcoded hex** anywhere in
  `sheets/`), and the siblings call the same `group_color()` from the same shared
  module, so the same group → the same color by construction. Confirmed against the
  built file: Summary `FF6A4C93`, Assumptions `FFB8860B`, the 9 model tabs
  `FF34406B`, the 5 data tabs `FF7B1F3A`, Checks `FF6E6E6E`, Sources `FF1F3A5F` —
  exactly the `SHEET_GROUPS` values (the `FF` is the ARGB alpha the writer adds).
  Adding finer per-tab colors would *break* the shared one-color-per-group
  convention, so it was left as-is.
- **The one real gap was file NAMING.** Siblings name every module
  `<group>_<tab-slug>.py` so the filename reveals the group; here all sheet modules
  carried a `data_` prefix, so the 9 **model** sheets read as if they were source
  data — the likely source of the "which are data vs calc?" confusion. The runtime
  group was right (`_GROUP="model"`); only the filename lied.

### The rename (cosmetic; output proven unchanged)

- Swapped `data_ → model_` on the 9 calc modules, **keeping their slugs** so the
  accessor vocabulary (`pw_`/`rb_`/`cl_`/`sc_`/`wt_`/`bv_`…) stays coherent:
  `model_piid_worktype`, `model_rebuy_timing`, `model_concentrated_lanes`,
  `model_source_concentration`, `model_program`, `model_by_worktype`,
  `model_by_vessel`, `model_by_piid`, `model_by_vendor`.
- Tidied the 2 mis-slugged leaves to match their tabs:
  `data_vendor_lane → data_lane_vendors`, `data_prime_calendar → data_prime_awards`
  — so all 5 data leaves are now tab-aligned (`data_lane_detail`,
  `data_lane_vendors`, `data_lane_vendor_fy`, `data_role_detail`,
  `data_prime_awards`).
- Mechanics: one word-boundary `perl -pi` pass rewrote every module-path /
  import / registry / docstring-first-line reference across `sheets/`, then `mv`'d
  the 11 files. All references are contained in `sheets/` (no `sheet_specs`, build,
  or research code touches them). Deliberately did **not** rename the legacy model
  slugs to full tab-slugs (e.g. `rebuy_timing`→`recompete_timing`) — that would
  cascade into renaming the accessor functions; left as an optional deeper pass.
- **Verified:** rebuild green (18 sheets / 14 tables / 55 parts / 0 errors); the
  structural diff against the **original pre-refactor baseline** still shows only
  `docProps/core.xml` (timestamp) changed — **0 worksheet/table parts differ**.

### `sheets/` now reads by prefix

`summary_*` (2 incl. inputs/sources naming), `model_*` (9 calc cuts, indigo),
`data_*` (5 leaf tables, burgundy), `validation_*` (Checks), plus the 5 `_*`
helpers — so a module's group is obvious from its filename, matching ddg /
submarines.
