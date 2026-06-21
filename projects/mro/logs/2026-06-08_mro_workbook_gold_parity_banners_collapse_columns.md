# 2026-06-08 — MRO workbook: gold-parity pass (banner widths, collapse, columns, casing)

## Scope

Seventh 06-08 pass on the MRO workbook sheet modules
(`projects/mro/workbook/workbook_mro/sheets/`). Closed the remaining visual gaps vs the gold
`submarines`/`ddg` workbooks the user flagged: half-wired collapse, "long background fills over
empty columns", Reconciliation §2's blank column B, TAM Bridge's two one-row sections, lowercase
prose, and a redundant Figure Register column. Plan: `~/.claude/plans/wait-there-s-missing-misty-finch.md`.

**Every edit is layout / style / outline / text, or a numeric *relocation within an engine tab*.**
All gates green with **no `regen-baseline`**: `build_workbook.py` → 19 sheets, **0 defined names**,
7 native tables (was 8 — see Reconciliation); `qa/verify_crosstab.py` → OK (4,290); `qa/tie_out.py
compare … --tol 1.0` → **Invariant B (86 figures) + Invariant A (engine multiset) both match**.

## The load-bearing mechanism (collapse)

`banner_row(mark_collapsible=True)` puts the gutter `x` (visual only); the *functional* collapse
is `row(outline_level=N>0)` on the content rows (Excel groups contiguous equal-level runs;
`worksheet()` already emits `<outlinePr summaryBelow="0"/>`). So "collapsible like gold" needs
**both** on every section/sub-section. `model_services.py` had the `x` on sections but **zero**
`outline_level` anywhere → the `x` collapsed nothing. That was the real "missing collapse" bug.

## Changes

- **`_layout.py` (shared RowCursor)** — added opt-in `RowCursor(start, outline_default=N)`.
  When >0, `write()`/`total()` default content rows to that outline level (banners stay 0).
  Backward-compatible (default 0 → no change to other sheets). Used by services + methodology to
  wire whole-section collapse without touching ~30 call sites each.
- **`outputs_figure_register.py`** — deleted the redundant **"Source cell"** column F (`_HEADERS`,
  header styles, data rows, `_COLS`→`[10,8,52,14]`). `value_cell()` unchanged (Value stays col E;
  F was rightmost). Not an engine tab, 0 names → value-neutral.
- **`model_tam_bridge.py`** — folded the two 1-row sections (`§2 Grand totals`, `§3 drop-through`)
  up into `§1`: the `c.total()` TOTAL row + the addressable drop-through row now follow the 8
  bridge rows under the single `§1` banner. `P["total"]` still captured → `topdown_total_cell` /
  `bottomup_total_cell` / `bridge_gap_cell` (Figure Register inputs) unchanged.
- **`model_reconciliation.py`** — **R5 layout** (user choice): kept §1's three columns; reordered
  §2 to **lead with the wide "Line Item" description in column B**, so §2 shares the wide column
  with §1's Anchor → **no empty column B** (the prior C-start fix's regression). `_S2_HEADERS`
  reordered; §2 amounts now E/F/G, FY25 Enacted accessor → **col F**; §1 value stays D. Added
  `mark_collapsible` + `outline_level=1` to §2; converted the 4 appropriation dividers from
  single-cell `c.write(S_TITLE_SUBSECTION)` to full **collapsible subsection banners**. To allow
  that cleanly, **dropped the `BudgetAnchors` ExcelTable** (a native table can't host banner rows
  / outline groups gracefully; nothing referenced the table name — accessors use cell refs).
- **`model_services.py`** (`_NCOLS=32`) — localized every banner to its section width
  (`_crosstab`→`len(axis)+3`; §4/§5/§9/§12→3; §6→4; §7→3; §10/§11→5; §13/§14→`len(_S13_CATS)+3`);
  added `mark_collapsible` to the 9 sub-section banners; `RowCursor(2, outline_default=1)` to wire
  collapse (was entirely absent). Sheet title stays full width.
- **`model_depot_ship_repair.py`** (`_NCOLS=20`) — `_section(title, n_cols)` now parameterized;
  each section passes its real width (matrix sections stay `ncol+2`; §4=20 genuinely wide, the
  rest 5–9). §11 tier sub-section banners got `mark_collapsible` + `n_cols=5`.
- **`guide_methodology.py`** — `outline_default=1` (full-section collapse); added a `_sc()`
  sentence-case helper applied to the descriptive columns (§1 definitions, §2b, §3, §4, §5, §6).
- **`sources_source_index.py`** — sentence-cased 3 "Key fields" values. Left filenames / `v433` /
  `PSC`/`PIID`-leading values as-is.
- **Collapse audit** of the other 11 sheets: every section/sub-section banner already had
  `mark_collapsible`; data rows already at `outline_level=1` (header at 0 = gold pattern). No
  change needed except methodology.

## Why value-neutral

Banner-width / `mark_collapsible` `x` / `outline_level` touch only styled-empty or text cells and
row attributes → no numeric `<c>` → Invariant A (numeric multiset over the 9 engine tabs)
unchanged. Reconciliation §2 *relocates* numeric cells within one engine tab (relocation-proof)
and the producer accessors + `qa/name_map` follow `_NAME_COL` → Invariant B re-validates the 86 at
their new cells (verified: §2 names → col F, §1 → col D). TAM Bridge total relocates within its
engine tab. Figure Register / Methodology / Source Index are non-engine, text-only.

## Verification (all green)

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py        # 19 sheets, 0 defined names, 7 native tables
/usr/bin/python3 qa/verify_crosstab.py    # CROSSTAB VERIFY OK (4,290)
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Defense Drivers MRO_vS.xlsx" --tol 1.0   # B + A match, no regen
```
Empirical (openpyxl on the built xlsx): Services §4 banner fill stops at D (J/AG empty) while the
§2 cross-tab spans to AG; Depot §1 stops at H, §4 matrix spans to U; every section/sub-section
banner has `x` in col A and content rows carry `outlineLevel=1` (Services/Methodology cross-tabs
now collapse). Reconciliation §2 header `B:Line Item … F:FY25 Enacted … H:Source`, col B non-empty,
`OMN_1B4B_TOTAL` = 11,763,594 at F. TAM Bridge has one §1 banner with TOTAL + drop-through. Figure
Register header B:E. Methodology/Source Index prose now capitalized; acronyms (FPDS/OP-5/PSC) left.
AST unused-import check clean on all edited modules.

## Notes / not done
- SRC-10 References still reads "HII **Marine** Technologies (Ingalls)" — actual segment is
  **Mission Technologies**. Flagged, not in this pass.
- Native tables 8→7 (dropped `BudgetAnchors`); no gate on the count; §2 is now a styled range with
  collapsible subsection banners (the gold model-sheet idiom).
