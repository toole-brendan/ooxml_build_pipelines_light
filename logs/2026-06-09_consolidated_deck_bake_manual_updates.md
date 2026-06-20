# 2026-06-09 — Consolidated deck: bake manual PowerPoint edits back into the slide modules

## Problem

The built deck `projects/consolidated/20260605_Distributed Shipbuilding Consolidated_vS.pptx`
is generated from the Python slide modules in
`projects/consolidated/deck/deck_consolidated/slides/`. The user separately opened that deck
in PowerPoint (with think-cell installed), made a round of manual edits, and saved it as
`~/Downloads/20260605_Defense Demand Drivers New Construction_v1.0.pptx` ("the manual file").
Goal: bake those manual edits back into the **source modules** so a rebuild reproduces the
manual file's content — **without** carrying over the think-cell OLE/`.xlsb` chart re-encoding;
the deck keeps using editable native charts styled to look like think-cell.

### What actually changed (built → manual), established by diffing both PPTX packages

Method: unzip both, extract every `<a:t>`, run a `Counter`-based multiset diff per slide
(ignoring `&apos;`→`'` and run-splitting noise). Slide map (build order): built **16
(Where to Play)** and **17 (Entry Wedge)** were deleted, shifting the appendix from built
18–23 → manual 16–21 (manual deck = 21 slides vs built 23).

Real edits, by type:
1. **Slide deletions** — Where to Play + Entry Wedge.
2. **Number rounding** — a "cleaner numbers" pass ($B→1 decimal, headline %→whole). The
   manual pass was *internally inconsistent* (left `$3.88B` in the s09 headline + s12 body,
   `$10.29B`/`$3.31B` on s09, `$13.57B` on s14, etc.).
3. **Title/text/divider edits** — appendix H1s → "Methodology (1/5)…(5/5)" (eyebrow unchanged);
   two divider subtitles; sentence trims (s09 "scope removal", roadmap "No SOM…" dropped,
   s14 classifier "Residual is unclassified award spend"); s02 bottom focal callout removed;
   s13 do-not-sum strip reworded to a small right-column "Note:" box.
4. **Chart restyle to think-cell** — plain-number labels (drop `$`/`B`/`M`), totals floated
   above each stacked column, tighter axes (e.g. 0–6 step 0.5).
5. **Rename build output** to "Defense Demand Drivers New Construction" (cover slide text
   unchanged in the manual file).

Noise correctly ignored: the image "swap" `virginia_construction.jpg`→`image6.jpg` is
byte-identical (same md5, 1100×394 — PowerPoint just renamed it); the `tags/`/`.xlsb`/
`oleObject*.bin`/chart1–6 explosion is think-cell re-encoding of the native charts.

## Decisions (user-approved, via AskUserQuestion)

- **Charts:** full think-cell match (plain-number labels + totals-above-column + tight axes).
- **Rounding:** harmonize **deck-wide** — round every occurrence consistently, including the
  spots the manual pass missed (not a literal 1:1 with the manual file).
- **Deletions:** remove from the registry **and** move the two module files to `deck/archived/`.
- **Rename:** change the build output filename.

Key enabling facts (no `deck_core` engine changes were needed):
- The chart engine already supports plain number formats and `value_axis_min/max/major_unit`.
- The **totals-above-stack** look is already in this deck (`s02` floats 14pt `_total_label`
  text boxes above each column with `show_value_labels=False`). MRO `topdown_detail.py:120`
  documents the same "column total = overlay" technique, and `column_chart` exposes
  `plot_layout={"x","y","w","h"}` (`<c:manualLayout layoutTarget="inner">`) which pins the
  inner bar rectangle → **deterministic** per-bar overlay positions.

## Changes (`projects/consolidated/deck/`)

### Structural
- `deck_consolidated/slides/__init__.py` — dropped the `s15_body_where_to_play_scorecard` /
  `s16_body_entry_wedge_thesis` imports + their `SLIDE_RENDERS` tuples (now 21 slides).
- `git mv` both modules → `deck/archived/`.
- `deck_consolidated/lib.py` — `OUT` filename →
  `20260605_Defense Demand Drivers New Construction_v1.0.pptx`.

### Rounding (harmonized deck-wide; $M figures and `~32.8%` kept exact)
- String/label edits across **s02, s05, s08, s09, s10, s11, s12, s13, s14**. Underlying chart
  **data floats** (e.g. `3.31`, `0.573`, `1.225`) stay precise — only label *display format*
  changed. Verified zero stragglers via
  `grep -rnoE '\$(3\.88|3\.28|…)B'` and `'(12\.5|35\.0|51\.8|48\.5)%'` (only intentional
  `~32.8%` remains). Note: s08 (`$3.88B` headline) and s14 (`~$2.73B/~$13.57B/~$5.46B`) were
  rounded **beyond** the manual file, per the harmonize decision.

### Title / text / divider
- `divider_sizing_opportunity.py` / `divider_evidence_implications.py` — new subtitles.
- Five `appendix_*.py` — H1 `_TOPIC` → "Methodology (N/5)" (breadcrumb `_BREADCRUMB_TOPIC`
  left descriptive); plus "retained budget base", "Residual is unclassified award spend",
  and the roadmap guardrail "No SOM…" sentence dropped.
- `s02_…py` — deleted the bottom `_CALLOUT` focal strip (+ its constant).
- `s13_…py` — caveat reworded ("Note: Scenarios are overlapping cuts of one TAM.") and the
  full-width bottom strip narrowed to a right-column note (`_COMM_X`/`_COMM_W`).

### Native chart restyle to think-cell (format + overlays, no engine change)
- **s11** (stacked col): labels/axis → plain `0.0`, `value_axis_min/max/major_unit=0/6/0.5`,
  `plot_layout` pinned, six `_stack_totals` overlay labels (1.9/2.4/5.8/2.5/4.8/5.9) floated
  just above each bar via the pinned-plot math.
- **s12** (ranked stacked col, $M): labels/axis → plain `#,##0`, axis 0/1400/200, `plot_layout`
  pinned, eight `_stack_totals` overlays (1,263/662/590/334/192/151/93/596).
- **s13** (clustered single-series): labels/axis → plain `0.0`, axis 0/3.5/0.5 (labels already
  sit above each column).
- **s02** (TAM-stack vs SAM): segment labels turned **on** (plain), SAM series `hide_labels`
  so only its overlaid total shows; totals → "3.9"/"3.3" repositioned **per-bar** via a pinned
  `plot_layout` + `_total_box_y()` (was a fixed band that floated the SAM total too high);
  axis 0/4/0.5.
- **s05** (shape funnel): program chips → per-funnel italic titles
  ("DDG-51 / Submarines, FY2022–FY2027 portfolio cumulative, nominal then-year $B"); shared
  units caption dropped; value axis/ticks/gridlines/tick-labels removed (kept the baseline);
  bar value labels → plain whole numbers (30/10/2/17, 84/17/10/57) above every bar incl. the
  endpoint; step labels shortened ("Less other non-BC", "Basic Construction").

## Verification

- **Build:** `cd projects/consolidated/deck && python3 build_deck.py` → "21 slides, 4 charts",
  renamed `.pptx` written, no errors. `ast.parse` clean on all slide modules.
- **Text parity** (rebuilt vs manual, multiset `<a:t>` diff, 1:1 over 21 slides): every delta
  is either (a) the intentional harmonization superset (s2 `$23.28B/$19.70B`, s5 `$10.29B`,
  s8 `$3.88B`, s9 `$3.88B/$3.31B/35.0%/$56.65B`, s12 `$2.52B/$3.88B`, s15 `$2.73B/$13.57B/
  $5.46B`) or (b) benign representation (native-chart category/segment labels live in the
  chart part vs think-cell slide text; PowerPoint run-merging; leading-space indent runs).
  **No unexpected content differences.**
- **Visual** (`soffice`→pdf→`pdftoppm`, compared to `/tmp/manual_png/`): s11/s12 totals land
  just above each bar; s02 per-bar totals fixed (3.3 now hugs the SAM bar); s05 reads as a
  clean think-cell waterfall; s13 plain labels + right-column Note; appendix H1s read
  "Methodology (N/5)".

## Notes / gotchas for next time

- **Totals over a native stacked column** aren't a chart element — overlay text boxes, and
  pin the plot with `plot_layout` (`layoutTarget="inner"`) so positions are deterministic:
  `cx_i = px + pw*(2i+1)/(2n)`, `y_top_i = py + ph*(1 − total/axis_max)`. Leave ~8–10% inner-
  plot **top margin** as headroom so the tallest bar's total still fits inside the frame.
- The build deck's native charts already round via number-format strings, so most "chart
  label" diffs against a think-cell file are representation noise, **not** data changes — don't
  chase them. Real chart edits here were format precision + axis bounds + the overlays.
- Harmonize-everywhere was the right call: the manual file's own rounding was inconsistent;
  matching it literally would have shipped `$3.88B` next to `$3.9B` on the same deck.
- The appendix "(1/5)…(5/5)" labels are the user's explicit page-of-5 indicator (not an
  internal M-step code), so they override the usual `no-m-series-codes-in-visible-slide-copy`
  habit — apply only to the H1, keep the descriptive breadcrumb eyebrow.

## Follow-up (2026-06-09, second pass) — remaining chart-parity gaps vs the Downloads reference

Reference of record is `~/Downloads/20260605_Defense Demand Drivers New Construction_v1.0.pptx`
(541 KB, think-cell, 21 slides). Diffed its chart parts against the build; three gaps remained.
The native-chart exemplar to copy idioms from is `projects/mro/deck`.

### 1. Slide 05 was still shapes, not a chart (`s05_body_scope_cost_funnel.py`)
The two cost funnels were hand-drawn rectangles + a manual baseline (no value axis). The
reference builds them as **native stacked-column charts** (chart2 DDG, chart3 sub): an
invisible `_Base` spacer series lifts the floating removal bars, one visible series carries the
heights, and per-point fills color the bars. Rebuilt s05 to match:
- `CHARTS = [_funnel_chart(_DDG), _funnel_chart(_SUB)]` → the builder numbers them chart2/chart3
  (charts are assigned by slide order; CHARTS[0]→rId2, CHARTS[1]→rId3 per slide). Result is now
  **6 charts**, same chart→slide map as the reference (s2=1, s5=2+3, s11=4, s12=5, s13=6).
- Exact reference floats: DDG spacer `[0, 19.646671, 17.470983, 0]` / visible
  `[29.936605, 10.289934, 2.175688, 17.470983]`; sub spacer `[0, 66.927049, 56.646727, 0]` /
  visible `[83.790155, 16.863106, 10.280322, 56.646727]`. `spacer[i]+visible[i]` = the running
  total (bar top) at category i.
- Fills via `data_point_colors` = **accent5 (AFC2CC) start, accent4 (89A2B0) removals, accent2
  (1D4D68) Basic-Construction end** — exactly the reference dPt scheme (was grays + BLUE_4).
  Note start≠end color, so the engine's `waterfall_chart()` (single `total_color`) can't express
  it; built it directly with `column_chart(mode="stacked")` + a no-fill spacer.
- Value axis **0–30 step 5 / 0–90 step 10**, dark-navy spine (`axis_line_color="162029"`), no
  gridlines. Native value + category labels OFF; both are slide overlays (the reference's catAx
  is `tickLblPos="none"` and the 4 category names live as slide text boxes).
- Overlays pinned to the chart's `plot_layout` inner plot: 4 value labels (start/end float above
  the full bar, removals centered in their floating segment), 4 category labels below the
  baseline, and 3 **dashed dark-navy** running-total connector rules. The reference connectors are
  `lgDash`, w=3175 (0.25pt), color tx1 — not solid black; matched with `connector(..., color=
  "162029", width=3175, dashed=True)`.

### 2. Slide 11 stacked segment order was inverted (`s11_body_annual_cadence.py`)
Reference chart4 stacks **Submarine (accent2 navy) as the base, DDG (accent1 gray) as the upper
cap**; the build had DDG on the bottom. Swapped the two series dicts (colors stay bound to each
program). The manual `chart_key` keeps its DDG-then-Submarine reading order — legend order is
independent of the bottom-up stack order.

### 3. Slide 12 colors + axis diverged (`s12_body_work_type_allocation.py`)
The build used an all-blue 3-accent progression (sub accent2 / DDG accent3 / residual accent4);
the reference (chart5) uses a **consistent program palette**: sub accent2 navy, **DDG accent1
gray** (same as s11), residual its own **accent3 (486D82)** mid-slate. Repainted DDG→accent1,
residual→accent3, updated the key, and set the value axis to **max 1300 / major 100** (was
1400/200). The earlier "all-blue for 3+ segments, gray reserved for 1-v-1" rule was the build
author's convention, not the reference's — parity wins, and it makes DDG read gray on both s11
and s12.

### Verification
- `python3 build_deck.py` → "21 slides, **6 charts**", no errors; `ast.parse` clean on the 3 modules.
- Chart→slide rels now mirror the reference exactly (s5 carries chart2+chart3).
- Visual (`soffice`→pdf→`pdftoppm`): s05 reads as two native think-cell waterfalls (axis, accent5/
  accent4/accent2 bars, totals-above / removals-inside, dashed navy connectors); s11 now navy-base/
  gray-cap; s12 residual is mid-slate with a 0–1300 axis. Segment order matches the reference on
  every stacked chart (s02/s11/s12 all sub-on-bottom).

### Gotchas
- **Native waterfall with differently-colored endpoints** can't use `waterfall_chart()` (one
  `total_color` for both start and end). Use `column_chart(mode="stacked")` with a `no_fill`
  spacer series + a visible series carrying `data_point_colors`; `spacer[i]+visible[i]` is the bar
  top, so connector levels = `tops[1:]` and removal-label centers = `spacer[i]+visible[i]/2`.
- **Two charts on one slide**: export `CHARTS=[a, b]` and emit two `graphic_frame`s with `rId2`/
  `rId3`; global chart numbers follow slide order, so inserting s05's pair shifted s11/12/13 from
  chart2/3/4 to chart4/5/6 — which is exactly the reference numbering, no manual renumber needed.
- think-cell fills are **theme `schemeClr accentN`**, not srgb — `CHART_ACCENT_N` in `style.py`
  maps 1:1 to theme accentN (accent1 79838F … accent5 AFC2CC), so match by accent index, not hex.

## Follow-up (2026-06-09, third pass) — chart label/legend/divider parity vs the reference

The native charts were styled "think-cell-ish" but several label/legend mechanics were off
versus the reference (`~/Downloads/…v1.0.pptx`). Fixed across **s02, s05, s11, s12, s13** so the
numbers, dividers, and legends read like the source. The reference charts are think-cell exports
(verbatim XML in MRO's `_chart_xml`); the consolidated deck rebuilds them natively, so these
mechanics have to be reproduced, not inherited.

### What the reference actually does (measured off chart1-6 + slide2/5/11/12 XML)
- **All in-chart numbers are 10pt, NON-bold** (`sz=1000`, no `b`), theme font `+mn-lt` (= Arial
  here). Totals above a column read apart from in-bar segments by **position, not weight** — same
  size, same regular weight. (Build had 8pt **bold** segment labels — the engine hard-coded
  `b="1"` — plus bold 9/8.5/14pt overlay totals.)
- **No segment dividers / bar borders**: every series `spPr` line is `<a:ln><a:noFill/></a:ln>`
  on chart1/4/5/6. (Build forced white 0.75pt dividers via `seg_line_color="FFFFFF"`.)
- **Thin-segment chips**: a cap too thin to hold its in-bar label (s11 FY2022 DDG `0.2`; s12 every
  DDG cap except Machining `225`) drops its native label and shows the number on a **chip filled
  with the segment's own accent** (gray accent1 here, white text) — NOT a white chip. This is the
  exact MRO recipe (`topdown_detail.py`: the 1% USCG sliver, chip filled accent6). In the
  reference these are encoded as deleted dLbls (`ser1` is missing the suppressed idxs).
- **Legends are 12pt** overlay rows (the native legend is off), swatch rect `179388×133350`,
  centered over open plot space — s11 bottom-center, s12 top-center over the short right bars, s02
  bottom-left. (Build used the 8.5pt `chart_key` side-key pinned bottom-left.)

### Engine changes (`deck_core/charts.py`, backward-compatible — MRO unaffected)
- `value_label_bold: bool = True` param on `_bars` (threads to `_build_series`); set **False** on
  the consolidated charts for the regular-weight think-cell look. Default True preserves every
  other deck (incl. MRO's 8pt-bold engine charts).
- Per-series `hide_label_points: list[int]` option → emits `<c:dLbl><c:idx/><c:delete val="1"/>`
  for just those points (vs `hide_labels`, which kills the whole series). Lets a single thin cap
  drop its label while its siblings keep theirs. The per-point dLbl block now handles deletes
  **and** color overrides, in ascending idx order (CT_DLbls requirement).
- `seg_line_color=None` already emitted a no-fill outline — just hadn't been used on these charts.

### Legend helper (`deck_core/chart_key.py`)
- New `chart_legend(sp_id, entries, *, cy, x_center|x, label_size=BODY_12PT)` — 12pt row,
  rectangular `179388×133350` swatches, centered on `x_center` or pinned at `x`, vertically
  centered on `cy`. `chart_key` (the quiet 8.5pt side-key) is left intact for other decks.

### Per-slide
- **s11**: `seg_line_color=None`; DDG `hide_label_points=[0]` + a `_chips()` overlay (accent1 fill,
  white `0.2`, chip top at the bar top so it reads at the cap); labels 10pt non-bold; stack-total
  overlays 10pt non-bold; `chart_legend` bottom-center (DDG, Submarine). Extracted `_SUB_VALS`/
  `_DDG_VALS`/`_DDG_CHIP_PTS` so the chart, totals, and chips share one source of truth via a
  `_plot_geom()` helper.
- **s12**: same; DDG `hide_label_points=[0,1,2,4,5,6]` (all caps but Machining 225) + six chips;
  `chart_legend` top-center (Submarine, DDG, Residual).
- **s02**: `seg_line_color=None`; labels + `_total_label` overlays 10pt non-bold; `chart_legend`
  12pt bottom-left. (DDG stays accent3 here — the reference colors DDG slate on s02 but gray on
  s11/s12; the program palette is per-slide in the source, not deck-wide.)
- **s05**: value-label overlays already moved to 10pt non-bold in the second pass; bars are
  borderless (`seg_line_color=None`) already.
- **s13**: `seg_line_color=None` (borderless bars); labels 10pt non-bold.

### Gotchas
- The engine **hard-coded data-label bold** (`b="1"`) — any "make chart labels regular" task needs
  the new `value_label_bold=False`, not just a size change.
- A too-thin segment's label can't just be shrunk — reproduce the think-cell **chip**:
  `hide_label_points` on that point + an accent-filled `text_box` whose top sits at the bar top.
  Filling the chip with the **segment's own color** (not white) is what the reference does.
- MRO "doesn't have this problem" because its charts are **verbatim think-cell XML** (`_chart_xml`),
  so font/size/weight/label-positions/chips come for free. Native rebuilds must reproduce each.

### Sizing tweak (same day, after a look) — user found 10pt + the chips a touch big
- On-chart numbers dropped **10pt → 9pt** (`LABEL_9PT`) deck-wide (s02/s05/s11/s12/s13 labels,
  stack-total overlays, chip text). Slightly under the reference's 10pt, per the user's eye.
- Chips shrunk to hug the 9pt number: `300_000×150_000 → 215_000×112_000`, `overlap 24k → 10k`.
- **s02 legend was obscuring the category-axis labels** — it sat in the key band right under the
  bars (`_KEY_Y`, ~5.12M). Moved down to `cy=5_700_000` (the open band above SOURCES_Y 5.93M),
  matching the reference, which also drops its legend near the slide bottom.
