# 2026-06-04 — z_ChartData reshaped to think-cell paste blocks (both workbooks) + paste styles ported to core

## Scope

Follow-up to the chart-conversion plan (`docs/chart_conversion_spec.md`, still mid-implementation
in the slide modules — **left untouched**). Rewrote the **z_ChartData** tab in **both** workbooks
so each block is a **think-cell embedded-datasheet paste range**: category / step labels **across
the top row**, values in the row(s) beneath (a small matrix for multi-series charts), styled as a
**pale-yellow copy-paste rectangle with a thin black perimeter**, ordered by deck slide and titled
with the chart type. Reference / gold standard: the Sea Range Telemetry workbook
(`~/Downloads/new/workbook_srt/sheets/z_chartdata.py`).

The faithful SRT look required **paste-range cell styles that did not exist in this repo's
`workbook_core/styles.py`** — so this session includes an **authorized, additive locked-core
change** (user signed off). Everything else is sheet-module work.

User decisions carried in (via AskUserQuestion):
- **Port the paste styles to core** (additive) rather than approximate.
- **Clean paste rectangles only** — drop the old annotation columns (Treatment / Note / % share /
  cumulative-vs-annual / Source / Bucket / Country).
- **Follow the conversion-spec TARGET chart types** (the eventual think-cell forms), not the
  pre-conversion types. (Moot in practice — the slide modules are already converted to match.)

Workspace is not under git / no backup; the safety net is a green `build_workbook.py` for both decks
+ DDG `validate_workbook.py` + an XML-parse sweep, run after each change.

---

## 1. Core — paste styles ported into `workbook_core/styles.py` (additive, no index moved)

A sheet can only reference existing style indices, so the pale-yellow/bordered paste look had to be
defined centrally. Appended (the styles.xml builder is list-driven on `count=len(...)`, so append =
done):
- palette `C_FILL_PASTE = "FFFACD"`; **1 fill** (pale yellow, id 5).
- **7 borders** (ids 3-9): TL / T / TR / BL / BR / L / R via a new `_thin()` helper (bottom edge
  reuses the existing bottom-thin id 1; interior reuses id 0).
- **2 number formats**: `166 = "$"#,##0"M"`, `167 = "$"0.0"B"` (percent reuses existing `165`).
- **20 cellXfs + `S_PASTE_*` constants** (ids 23-42): 3 header (TL/T/TR, bold-center), 2 label
  (L/BL, plain-left), 15 value = {BL, B, BR, R, interior} × {`_M` $M / `_B` $B / `_P` %}.

Verified: existing `S_*` indices unchanged (`S_DEFAULT`=0 … `S_HEADER_CENTER`=22); CELL_XFS 23→43,
FILLS 5→6, BORDERS 3→10, NUM_FMTS 2→4; `build_styles_xml()` parses; both workbooks still build green
with the styles present but (pre-rewrite) unreferenced. Values are **black-on-yellow** (not the green
link font) — a paste range, not a model cell.

## 2. The paste-block emitter (`_paste_block`, one copy per sheet module — not core)

Self-contained helper in each `chartdata_z_chart_data.py` (mirrors SRT's local helper; keeps the
shared `_layout.py` RowCursor untouched). Given `header` (corner + across-the-top labels) and `rows`
(`(row_label, [values])`), it emits a section banner, one blank, the header row, the data row(s),
then two blanks — styling every cell by its position in the rectangle (TL/T/TR header, L/INT/R
middle, BL/B/BR bottom) and unit (`_M`/`_B`/`_P`). A value is a formula (`=…`), the waterfall marker
`"e"`, or a numeric literal.

**think-cell waterfall convention:** computed subtotals/totals are the literal text `"e"` (think-cell
draws a calculated bar from prior steps; a numeric subtotal would double-count). **Units** match each
deck chart's displayed magnitude: `$B` blocks divide the model's `$M` producers by 1000; avg-annual
blocks divide a cumulative producer by `n_years`. All values stay **live producer links** (the one
exception: DDG §9 FFATA bands have no model producer → CSV-summed numeric inputs).

## 3. DDG z_ChartData — 9 blocks (deck slide order)

§1 Cost funnel (waterfall, 2×5) · §2 MYP POP distribution (stacked col, 6×2) · §3 MYP outside-yards
split (stacked col, 2×3) · §4 Annual TAM build (waterfall, 2×6) · §5 TAM by FY (stacked col, 3×7) ·
§6 Work-type allocation (ranked col, 2×9) · §7 SAM scenarios (ranked col, 2×6) · §8 Supplier
landscape (bar, 10×2, names down) · §9 FFATA visibility gap (column, 2×5). `executive_summary` chart
removed (KPI board) → no block. Cost-funnel "Less other" = `-(total − GFE − basic)` so it reconciles.

## 4. Submarines z_ChartData — 9 blocks (deck slide order)

§1 Basic Construction (stacked col, 3×7, $B) · §2 Annual cadence (clustered col, 3×7, $B) · §3
Coefficient evidence (ranked col, 2×4, %) · §4 AP/LLTM bridge (waterfall, 2×6, $B) · §5 Work-type
bucket TAM (ranked col, 2×8) · §6 SAM scenarios (ranked col, 2×6) · §7 Visible suppliers (bar, 10×2)
· §8 SIB exclusion (waterfall, 2×5, additive: BlueForge+TMG+IALR→`"e"`) · §9 Coefficient sensitivity
(appendix ranked col, 2×4, %; same ladder as §3). **AP-bridge removal cells are already signed
negative** on the AP Bridge tab, so they link straight through (no extra negation) — unlike DDG's
cost-funnel, which negates positive SCN cells.

## 5. Specs

Rewrote both `workbook/sheet_specs/chartdata_z_chart_data.md` to the paste-layout shape: new purpose
(labels-across / values-below, paste-range styling, `"e"` convention, unit handling), the §1-§9 block
map with chart type + rectangle dims, the trimmed Reads, and the new core-style dependency.

---

## Verification

| Check | DDG | Submarines |
|---|---|---|
| `build_workbook.py` | green — 24 tabs | green — 20 tabs |
| `validate_workbook.py` | 55 parts, **0 xml errors**, 24 sheets, **0 error-literal cells** | (no validator) |
| all XML parts well-formed | — | 36/36 parse, 0 errors |
| paste-styled cells in z_ChartData | 123 (styles 23-42) | 130 (styles 23-42) |
| `"e"` waterfall markers | 3 (cost funnel end; TAM build subtotal + end) | 2 (AP bridge end; SIB end) |
| unit styles exercised | `_M`, `_P` | `_M`, `_B`, `_P` |
| layout spot-check | §1 header across (TL/T/TR) + values below (B/BR) + `"e"`; §5 FY matrix header across | — |
| core indices unmoved | `S_DEFAULT`=0 … `S_HEADER_CENTER`=22 unchanged | (shared core) |

## Files touched

- **Core (authorized, additive):** `workbook_core/styles.py` (paste fill / borders / num-formats /
  cellXfs / `S_PASTE_*` constants).
- **DDG:** `workbook_ddg/sheets/chartdata_z_chart_data.py` (full rewrite),
  `workbook/sheet_specs/chartdata_z_chart_data.md`.
- **Subs:** `workbook_submarines/sheets/chartdata_z_chart_data.py` (full rewrite),
  `workbook/sheet_specs/chartdata_z_chart_data.md`.
- **Rebuilt:** `projects/ddg/…_vS.xlsx`, `projects/submarines/…_vS.xlsx`.
- **Not touched:** any slide module (chart conversion still in flight), other `workbook_core/*`, the
  decks, the SRT reference in `~/Downloads/new` (read-only), README.

## Open items / follow-ups

- **Number formats mirror the deck units, not SRT's.** DDG `$M` blocks use zero-decimal `"$"#,##0"M"`
  and the `$B` blocks use one-decimal `"$"0.0"B"` to match each deck chart's display; SRT used a
  single one-decimal `$M`. think-cell re-formats on paste anyway, so this is cosmetic.
- **Mirror, not a live feed.** Regenerate the affected block whenever a deck's rendered chart set
  changes. If the conversion plan alters a chart type/category list, re-sync the matching block.
- **MYP distribution** is a single 100%-stacked column; the spec's earlier "drop %-stacked" note was
  not enforced (the module still renders `mode="percent"`). The paste data (5 shares) is identical
  either way; flagged only so the block and chart stay in step if that mode changes.
- **Audit gates** (QA Reconciliation / Number Audit "0 FAIL") are runtime Excel formulas, not
  evaluated headless; this session changed no model formula/value, and DDG validate shows 0
  error-literal cells. Confirm in Excel for final sign-off.
- **`sheet_guide.md` not amended.** If "z_ChartData blocks are think-cell paste ranges (labels across,
  `"e"` for waterfall totals, S_PASTE_* styling)" should become a documented house rule, that's a
  locked-core guide edit — raise separately.
