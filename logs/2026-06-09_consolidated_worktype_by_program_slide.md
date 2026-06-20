# 2026-06-09 — Consolidated deck: work-type-by-program slide (manager's "Slide 3") + z_ChartData §15

## Problem / goal

Manager's third front-row slide for the consolidated deck: re-cut the work-type chart
from one-bar-per-work-type (s12, which STAYS in the deck) to **one stacked column per
program (DDG-51, Submarines)**, segmented by the 7 work-type buckets with each
program's residual riding the stack as a **hatched cap**, and the right panel carrying
a **condensed M4 classifier methodology** (the classification-ledger table) so the
slide self-contains the method instead of pointing at the appendix. His mock's values
(480/800, the 100s) were placeholders; real numbers are the per-program SAM bucket
allocations in the two program workbooks. Two mock errors fixed, not reproduced:
"Submarins" → "Submarines"; "Cuml. 5-yr." → the basis is 6 FYs (cumulative
FY2022–FY2027, carried in the exhibit header, not the title).

User decisions (AskUserQuestion): slide goes after s03 (s12 kept, nothing deleted);
right panel = condensed ledger table (not the flow); workbook change = a NEW block in
the consolidated workbook only; DDG segments = leader labels beside the bar.

## Data (recalc-verified, cumulative FY2022–FY2027 constant FY2026 $M, OBBBA on)

Rebuilt both program workbooks (no code changes needed — SAM Build already exposes
`bucket_tam_cell` / `unbucketed_tam_cell` / `portfolio_tam_cell`), recalc'd via
headless LibreOffice, read SAM Build §3b (DDG) / §5a (subs):

| Bucket (slide order) | DDG-51 | Submarines |
|---|---|---|
| Electrical and power | 227.42 | 7,889.07 |
| Piping, valves, and pumps | 209.27 | 4,051.07 |
| Structural fabrication and pre-outfit | 218.54 | 3,579.55 |
| Machining | 1,552.60 | 699.58 |
| Coatings and insulation | 101.90 | 1,134.78 |
| Castings and forgings | 66.84 | 906.27 |
| HVAC and ventilation | 245.84 | 364.97 |
| Residual (unbucketed) | 1,328.87 | 2,586.89 |
| **Total** | **3,951.28** | **21,212.17** |

Identities tie exactly: buckets + unbucketed = portfolio TAM per program; totals = the
s03 walk endpoints (3.951280 / 21.212173 $B, z_ChartData §11); sub bucketed total =
broad SAM 18,625.29; all SAM Build §9 checks OK; 0 error cells. Note: the per-program
residual sum (~$3,916M cum) differs slightly from the §8 combined residual (653/yr →
~$3,913M implied) because §8 derives residual as combined TAM − broad-SAM-scenario;
the per-program unbucketed values are the honest split and were used as-is.

## Changes

### `projects/consolidated/workbook/workbook_consolidated/sheets/z_chart_data.py`
- NEW block **"§15 - Outsourced BC by work type (per program, stacked column)"**
  appended after §14 (the same-day §11–§14 appends set the convention: append with
  sequential numbers, never renumber). Header `["", "DDG-51", "Submarines"]`; 8 rows =
  `_WORKTYPE_HDR` (reused) zipped with new `_DDG_WT_BY_PROG_B` / `_SUB_WT_BY_PROG_B`
  exact floats (cumulative $B); docstring map line added "(slide 4)". §8 untouched
  (s12 still feeds from it).
- Build + validate: 0 xml errors, 0 error-literal cells.

### NEW `projects/consolidated/deck/deck_consolidated/slides/s03b_body_worktype_by_program.py`
Sibling idioms copied from s03 (chrome, `_zone_header` exhibit-header + rule,
`_plot_geom` overlay math, `a:pattFill` hatch) and s12 (`_stack_totals` float math).
- **Chrome**: breadcrumb "Executive Summary / Supplier TAM and SAM"; title
  "Outsourced Basic Construction Spend by Work Type | Electrical power leads the
  ~$21.2B submarine pool; machining leads the ~$4.0B DDG-51 pool." (user-picked from
  five options; ≤2 lines); exhibit header "($B, cumulative FY2022–FY2027, FY2026 $)";
  right zone header "Methodology"; prelim chip; 4-part sources line.
- **Chart** (native `column_chart(mode="stacked")`, chart4): categories
  ["DDG-51", "Submarines"]; 8 series base→top = 7 buckets (accent2/3/4/5/6, accent1,
  DK) + Residual `pattern={"prst": "ltUpDiag", "fg": CHART_ACCENT_1, "bg": WHITE}`;
  white 0.75pt dividers, dark-navy axis, axis 0–24 $B with tick labels OFF
  (`show_value_axis_labels=False` — every segment annotated directly), native cat
  labels 10pt, `gap_width=65`, labels '0.0' 9pt non-bold. **Plot pinned right-of-center
  (`plot_layout x=0.30 w=0.62`)** so the chart zone's left strip holds the key and the
  DDG ladder.
- **Label scheme** (the bars are 5.4:1, far from the mock's equal placeholders):
  - Series thin on BOTH bars (Machining, Castings, HVAC) → `hide_labels=True`;
    every other series → `hide_label_points=[0]` (kill only the DDG point).
  - **DDG**: all 8 values on an even-pitch ladder (160k EMU) up from the plot bottom,
    left of the bar, with two-piece elbow leaders (60k tick at the true segment center
    + slant to the label). Strict per-segment y collapses — the three base segments'
    centers sit ~32k EMU apart; the monotonic k→k ladder cannot cross.
  - **Sub**: in-bar labels where ≥ ~150k EMU tall (7.9/4.1/3.6/1.1/2.6); machining
    0.7 / castings 0.9 / HVAC 0.4 leader-labeled right, castings↔HVAC spread to a
    150k min pitch about their mean.
  - Program totals "4.0" / "21.2" float above each bar, 9pt bold.
- **Vertical 8-entry key** top-left (bucket order; matches the manager's mock). The
  Residual swatch is a **hand-built `<p:sp>` with `a:pattFill`** (`_hatch_swatch`) —
  `text_box`/`chart_key` are solid-fill-only.
- **Methodology panel**: the appendix classification ledger
  (`appendix_sam_classification_field_audit`) condensed to 2 columns (Stage | Rule
  applied), 7 rows, 8.5pt, row fills mirroring the appendix highlights (BLUE_1
  entity/output, GRAY_1 role filter, GRAY_2 residual), heights via
  `estimate_row_heights`; two findings beneath (s12 `_commentary` idiom): "The
  classifier is entity-first and role-first." / "Residual is unclassified award
  spend." with evidence bullets.

### `slides/__init__.py`
Import + tuple inserted directly after s03. The parallel session's
`s11a_body_outsourced_bc_annual_tam` (manager's slide 2, outlook) landed mid-flight
next to s11 — first registry edit attempt failed on the mtime check, re-read, merged
around it.

## Copy decisions (target_copy.txt / slide_guide.md)

- **Title rule is mechanical, not just style**: `slide_guide.md:60` — the title box is
  noAutofit 20pt and BODY_Y clears exactly a 2-line "Topic | Finding."; a 3-line title
  collides with the body. First draft (~183 chars) rendered 3 lines and touched the
  exhibit header; budget is ~150 chars total (s03 = 146, s12 = 126). Five options
  offered; user picked the program-mix contrast with dollars (147 chars). The
  dollar-basis tail lives in the exhibit header, s03-style, not the title.
- **No em dashes** in rendered text (`target_copy.txt:161`): two slipped into the
  first draft (ledger row 1, findings bullet) — swapped for parens/colon. s03's ledger
  has the same drift ("add none — supplier long-lead…"), left alone.
- **User vetoed "denominator"** in visible copy. Replaced at each level's own term:
  ledger row 6 (classifier level) → "Keep unresolved dollars in the **addressable
  base**; residual dilutes named shares." (rows 4/7 already say "addressable base");
  finding (allocation level) → "Unresolved dollars stay **in TAM but outside SAM**:
  the hatched cap on each program's stack." (s12 precedent: "stays in TAM while
  remaining outside broad SAM"). The manager's own snip says "Keep unresolved $ in
  denominator" — meaning kept, word dropped.

## Verification

- Program workbooks: build + soffice recalc, 0 error cells, §9 checks OK, identity
  ties above. Consolidated workbook: build + validate, 0/0.
- Deck: `python3 build_deck.py` → **24 slides, 10 charts** (+1/+1 over the 23/9
  baseline after s11a landed). `xmllint --noout` clean on slide4.xml + chart4.xml;
  one `pattFill` in each (bar series + key swatch).
- Visual (`soffice`→pdf→`pdftoppm`, slide 4): hatch renders in both residual caps and
  the key swatch; DDG ladder reads bottom-up 0.2/0.2/0.2/1.6/0.1/0.1/0.2/1.3 with a
  clean non-crossing leader fan; sub leaders hit machining/castings/HVAC centers;
  totals clear the plot top; ledger rows unclipped, findings fit with slack; title on
  2 lines. Slides 3 (s03) and 15 (s12) unchanged.

## Gotchas / notes for next time

- **Concurrent sessions are live in this repo** — the registry changed between read
  and edit (s11a), and z_ChartData had grown §11–§14 since the morning pass. Re-read
  every file immediately before editing; `ls -lat` first.
- **3-line titles physically collide with the body** (BODY_Y clears exactly 2 noAutofit
  20pt lines). Check char count (~≤150 incl. topic) before building.
- **`hide_labels` vs `hide_label_points`**: with per-program series, `hide_labels`
  kills BOTH programs' labels — only correct when the segment is thin on both bars;
  otherwise `hide_label_points=[idx]` surgically kills one category's point.
- **A hatched legend swatch needs raw `<p:sp>` XML** with `a:pattFill`; `text_box`
  and `chart_key` swatches are solid-fill-only.
- **Leader ladders beat true-y labels** when stacked segments are thinner than a 9pt
  line (~137k EMU): even pitch anchored at the plot bottom + k→k elbows is collision-
  free by monotonicity; reserve the strip by pinning the plot right-of-center
  (`plot_layout`), not by shrinking the chart frame.
- **Per-program residual ≠ the §8 combined residual** (~$2.7M cum delta): §8 derives
  it from the broad-SAM scenario, the per-program split from each workbook's
  unbucketed row. Use the per-program values for per-program exhibits.
- z_ChartData convention confirmed: **append new blocks with sequential § numbers**
  (letter suffix like §11b only for a companion memo of the same exhibit); never
  renumber existing blocks.
