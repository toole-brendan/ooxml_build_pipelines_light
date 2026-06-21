# 2026-06-08 — MRO deck: slide 6 "Work Segments" static-shape → real native chart

Converted the first of the MRO deck's fake (static-shape) think-cell exhibits into a **real
native `<c:chart>`** that looks identical. Scope was deliberately **one chart** (user: "focus on
just doing 1 at a time"). This is the inverse of the consolidated restyle
(`logs/2026-06-08_consolidated_charts_thinkcell_restyle.md`): there, native charts were styled to
look like the MRO static exhibits; here, an MRO static exhibit becomes native.

## What slide 6 was vs is
- **Was:** `work_segments.py` pasted `_chart_xml/slide06.xml` verbatim — accent `<p:sp>` rectangles
  (the column segments), `<p:cxnSp>` axis lines, and frozen `<a:r>` % labels. Looked like a chart;
  wasn't one.
- **Is:** a native `column_chart(mode="stacked")` — single category, 6 one-value series — placed by
  `graphic_frame(rId="rId2")`, with the embedded `.xlsx` (editable). Caption, right-side
  `house_table`, and footer are unchanged. The `$8,971M` column total (which a native stacked chart
  can't draw) and the 6-entry vertical legend stay as overlay shapes.

## Faithfulness facts (verified from `_chart_xml/slide06.xml` + theme1.xml)
- Theme "Saronic" resolves `accent1..6` = `79838F/1D4D68/486D82/89A2B0/AFC2CC/D8E3EB`, `tx1=162029`,
  `bg1=FFFFFF` — **identical to `deck_core.style.CHART_ACCENT_1..6`**, so native fills match exactly.
- Segments bottom→top: `accent1,2,3,4,6,5` at `53/21/10/7/5/4 %` — note the deliberate **accent5/6
  swap** on the top two segments (preserved).
- In-bar % labels: white on accent1–4, black on the two light tops. The engine's auto white/black
  flip would wrongly blacken the 7% (accent4 is borderline-bright), so `label_color="FFFFFF"` is
  forced on the first four series; the light two use the auto-black.
- Color↔name (from the legend, NOT positional): accent1=Depot, 2=Nuclear, 3=HM&E, 4=Combat,
  5=Electronics, 6=Port. (First pass mislabeled the 7/5/4% series in the hidden embedded data;
  corrected.)
- Value axis 0–100% in **5% ticks**; dark-navy axis lines; no gridlines; no native legend.
- Bar geometry pinned to the source: measured source bar = L 6.5% / R 36.1% / width 29.6% of slide;
  native build now L 6.8% / R 36.1% / width 29.3% (within ~0.3%).

## Engine changes — `deck_core/charts.py` `_bars` (all additive, defaults = byte-identical)
Same backward-compatible pattern as the earlier `seg_line_*` / `axis_line_*` additions; verified the
default path emits the old bare `<c:scaling><c:orientation val="minMax"/></c:scaling>` and
`<c:layout/>` with no new elements.
1. `value_axis_min` / `value_axis_max` / `value_axis_major_unit` (default None) → emit `<c:max>`/
   `<c:min>` inside `<c:scaling>` (order: orientation, max, min) and `<c:majorUnit>` after
   `<c:crossBetween>`. Slide 6 uses 0 / 100 / 5 for the dense 5% axis.
2. `plot_layout` (default None) → a `{"x","y","w","h"}` (frame fractions) manualLayout with
   `layoutTarget="inner"` (same structure slide 9's bundled chart uses), pinning the inner
   plot/bars rectangle. Slide 6 uses `{0.0833, 0.0138, 0.9155, 0.9491}` + `gap_width=0` so the
   single fat column lands at the source bar's exact x/width.

## Module — `projects/mro/deck/deck_mro/slides/work_segments.py`
- Dropped the `slide06.xml` read (and the now-unused `pathlib` import). Added `_SEG` (the 6
  segments), the `column_chart(...)` + `CHARTS=[_CHART]`, a `_legend()` builder over `_LEG` (6
  swatch `text_box`es with the 0.75pt white border + 8pt labels, transcribed y-positions), and the
  `$8,971M` overlay. `_chart_xml/slide06.xml` left in place (unused; keeps the extraction tooling /
  source-of-truth intact).

## Verify / regenerate
```bash
cd /Users/brendantoole/projects3/ooxml_build_pipelines_light
/usr/bin/python3 projects/mro/deck/build_deck.py            # green: 15 slides, 2 charts
OUT=projects/mro/deck/_qa/png
soffice --headless --convert-to pdf --outdir "$OUT" "projects/mro/20260607_Defense Drivers MRO_vS.pptx"
pdftoppm -png -r 220 -f 6 -l 6 "$OUT/20260607_Defense Drivers MRO_vS.pdf" "$OUT/built-slide"
```
Confirmed vs `_qa/src_png/src-06.png`: segments/colors/order, white dividers, 5% axis, in-bar label
colors, `$8,971M`, category label, the 6-entry legend, and bar width/position all match. chart1.xml
is a native 6-series stacked `barChart` with manualLayout + max/min/majorUnit + embedded workbook +
rels; `[Content_Types]` has the chart+xml and spreadsheet overrides; deck round-trips soffice with
no Repair. Regression: consolidated (4 charts) / ddg (9) / submarines (9) / sea_range (0) all rebuild
green — they never pass the new params, and defaults are byte-identical.

> Note: `projects/mro/deck/_qa/render.sh` has a **stale** `PPTX=` path (an old filename); rendered
> directly against the real output (`…Defense Drivers MRO_vS.pptx`) instead. Pre-existing; not fixed.

## Slide 13 "Marauder-Like Fleet MRO" — native MARIMEKKO (done same session)
Converted the second exhibit: the work-segment × hull **marimekko** (`fleet_mro.py`) → a native
`marimekko_chart` (first use of that engine fn anywhere). 5 hull columns (T-AO/T-AKE/ESB/T-EPF/WPC),
widths ∝ FY2025 $M (384/208/60/59/35), each percent-stacked to 100% over 3 segments bottom→top:
**Depot (accent1) / Port & Technical (accent3) / HM&E (accent2)** (mapping from the source legend,
not stack position). Values + widths transcribed as the source cell EMU heights/widths so
proportions are exact.

**The pinstripe problem + fix.** `marimekko_chart` fakes variable width via many thin equal bins
(here `total_bins=200`, percentStacked, gap 0). With white cell borders (`seg_line_color="FFFFFF"`)
each bin gets an outline → ~50 white vertical pinstripes per column (graph-paper look). Verified by
render. Fix: render the chart **seamless** (`seg_line_color=None`) and **overlay** the white dividers
— 4 vertical (between columns, at `label_meta[i].x1_frac`) + 9 horizontal (between segments, at the
cumulative-% boundaries), computed from the same pinned plot rect so they land exactly on the native
bin/segment edges. (`gap_width=0` already makes same-color bins within a column abut into a solid block.)

**Two more additive engine changes** (`deck_core/charts.py`, both safe — defaults unchanged):
- `seg_line_color=None` → emits `<a:ln><a:noFill/></a:ln>` (borderless bars). Default `"000000"`
  unaffected.
- cat-axis `majorTickMark` tied to `show_cat_labels`: when labels are hidden (only the marimekko
  does this) the tick marks are dropped too — else the native cat axis prints a tick **per bin**
  (200 ticks along the bottom). Normal charts keep `"out"`.

**Module pattern** (`fleet_mro.py`): native chart pinned via `graphic_frame` + `plot_layout`
(value axis 0–100% / 5% ticks via `value_axis_min/max/major_unit=0/1/0.05`, `value_axis_format="0%"`,
dark axis spine); computed `_dividers()`; and **`_overlay()`** which keeps the source slide13.xml
shapes verbatim *except* the colored cells and the source's own value axis (filtered by x-coord), so
the legend / $M + hull headers / in-cell %s / right-side callouts / axis title / footer / tiny-segment
"2%" leader chips are all reproduced for free. chart3.xml verified: `percentStacked`, seamless,
~200 bins, embedded `Worksheet3.xlsx` (+rels) = editable; deck round-trips soffice, no Repair;
render matches the static target tightly. All chart decks (mro 3 / consolidated 4 / ddg 9 / subs 9)
rebuild green — the new params are opt-in.

## Slide 8 "Top-Down Composition" — native single stacked column (done same session)
Converted the third exhibit: the budget-source split (`topdown_detail.py`) — the same single-fat-
column shape as slide 6, so a direct repeat of that pattern. **No engine change** (reuses the
`value_axis_min/max/major_unit` + `plot_layout` params slide 6 already added). The right-side rollup
table (`slide08_table.xml`) stays transcribed VERBATIM; only the left static chart was swapped.

**Faithfulness facts (from `_chart_xml/slide08.xml`).** Six segments bottom→top in **pure accent
order accent1..6** (no accent5/6 swap, unlike slide 6): Public NSY 44% / 1B4B Private avails 25% /
OPN LI 1000 14% / SCN LI 2086 RCOH 9% / MSC M&R 7% / USCG ISVS 1% (= $16,996M total). In-bar label
colors: white on accent1–4 (forced `label_color="FFFFFF"` on the first four, same accent4-is-
borderline-bright reason as slide 6), auto-black on the light accent5/6 tops. Bar geometry is the
**same x/width as slide 6** (L 6.51% / W 29.64%), so it reuses slide 6's `graphic_frame`
(x=465138,y=1660000,cx=3946525,cy=4180000); `plot_layout` recomputed to slide 8's exact bar/axis
EMU = `{0.0833, 0.0187, 0.9155, 0.9441}` (pins all four edges within ~1 EMU: left 793750, right
4406900, 100%-line 1738313, 0%-line 5684838). Value axis 0–100% / 5% ticks; dark-navy axis lines;
no gridlines/native legend. Category label "Total FY2025" comes from catAx. Overlays: the $16,996M
total + the 6-entry vertical legend (USCG ISVS→Public NSY, transcribed y-positions).

**The 1% chip (caught in review).** The 1% USCG ISVS sliver is too thin to hold an in-bar label, so
the source bumps "1%" **above** the bar onto a small rectangle **filled with the segment's own
accent6** (the source label shape carries `<a:solidFill><a:schemeClr val="accent6"/>`; the
44/25/14/9/7% labels are all `noFill`). A native centered label can't do this, so: set
`hide_labels:True` on the accent6 series (verified `USCG ISVS dLbls=False`, the other five keep
theirs) and **overlay the chip** as a `text_box` (fill=`CHART_ACCENT_6`, `line_color="none"` to
beat the house auto-border, at the source x/y 2513013/1697038 — which is coincidentally where the
suppressed native label would have centered). Chip text is bold to match the engine's other in-bar
labels (the whole slide's native labels render bold non-italic vs the source's italic — same
pre-existing slide-6 tradeoff).

chart2.xml verified: native 6-series stacked `barChart` + manualLayout + max/min/majorUnit +
embedded `Worksheet2.xlsx` (+rels, editable); render matches `src-08.png` (colors/order, white
dividers, 5% axis, in-bar label colors, the 1% chip, $16,996M, category label, legend, bar
width/position). Deck round-trips soffice, no Repair. All decks rebuild green (mro 4 / consolidated
4 / ddg 9 / subs 9 / sea_range 0).

## Slide 7 "TAM Composition" — native 6×6 MARIMEKKO via POSITIONAL series (done same session)
Converted the last exhibit: the work-segment × vessel-type marimekko (`tam_composition.py`), 6
segments × 6 hull columns. **This one needed a new technique** — it is NOT a direct repeat of slide
13, because the source **size-sorts each column's segments** (largest at the bottom), so the columns
do not share one segment order (Surface Combatants has Depot/grey at the bottom; Submarines has
Nuclear/navy at the bottom 60%). A by-segment native percentStacked (one series per segment, the
slide-13 approach) forces ONE global order and would visibly reshuffle several columns.

**Positional-series fix.** Instead of one series per segment, build one series per **stack layer**
(Layer 1 = bottom band, Layer 2 = 2nd band, …) and color each *bin* individually with
`data_point_colors`. Layer 1 sits at the bottom of every column but carries each column's own bottom
segment + its accent, so every column keeps its exact source bottom→top order while the chart stays
native + Edit-Data-backed. Empty top layers (columns with <6 segments) get value 0 / a dummy color.
Built with `column_chart(mode="percent", categories=[""]*200, series=<6 positional layers>, …)` (not
`marimekko_chart`, which only emits by-segment series). Bin allocation (∝ width, largest-remainder)
is replicated in-module as `_alloc_bins` (mirrors `charts._allocate_bins`) because it's also needed
for the vertical dividers.

**Why this also keeps the overlay verbatim.** Because the native cells now land in the *exact* source
order/proportions, the source's in-cell %s, the tiny-segment leader chips (small accent squares +
their `1%/2%/0%` labels, at non-column x's), the legend, the $M + vessel headers, and the "Segment
composition by hull" rail title all overlay correctly — kept verbatim by the same filter idiom as
slide 13 (`_overlay()` drops only the colored cells `x∈_COL_X & accent`, the source value-axis labels
`%-text & x<900000`, and the axis lines `cxnSp & x∈{839788 ticks,868363 baseline,873125 spine}`).
Seamless render (`seg_line_color=None`) + overlaid white dividers (5 vertical between columns at bin
boundaries, 22 horizontal between segments at cumulative source heights). Caption / commentary rail /
footer stay deck_core primitives (never part of the extracted exhibit).

Data facts: widths ∝ FY2025 $M at ≈790 EMU/$M (2239/1441/2093/769/759/1667). Segment→accent: 1 Depot
/ 2 Nuclear&Complex / 3 HM&E / 4 Combat / 5 Electronics / 6 Port. Plot rect pinned x 873125..7956551,
y(100%) 2047875 → y(0%) 5632451 via `_FRAME`+`_PL`. chart (chart for slide7) verified: native
`percentStacked`, 6 series, **1200 `<c:dPt>` per-bin color overrides (all seamless)**, manualLayout +
max/min/majorUnit, 200 blank bins, embedded editable workbook; ~302KB (the 1200 dPt) but round-trips
soffice with no Repair. Render matches `src-07.png` tightly (widths, per-column order, colors,
dividers, in-cell %s, leader chips, legend, headers). All decks rebuild green (mro 5 / consolidated 4
/ ddg 9 / subs 9 / sea_range 0).

## Status: ALL MRO chart exhibits are now native
Slides 6 (single stacked column), 7 (6×6 positional marimekko), 8 (single stacked column), 9 (bundled
funnel chart, already native), 13 (5-col marimekko). No static think-cell chart exhibits remain; every
other static `_chart_xml/*.xml` read is a diagram / funnel / bridge / table (no chart equivalent).
