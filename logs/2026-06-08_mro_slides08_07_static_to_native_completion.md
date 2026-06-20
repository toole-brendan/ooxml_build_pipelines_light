# 2026-06-08 — MRO deck: slides 8 + 7 static→native charts (conversion project COMPLETE)

Continuation of `logs/2026-06-08_mro_slide06_static_to_native_chart.md` (slides 6 + 13). This session
converted the last two static think-cell chart exhibits — **slide 8** (single stacked column) and
**slide 7** (6×6 marimekko) — to real native `<c:chart>` parts that look identical. With these, **all
MRO chart exhibits are now native** (slides 6, 7, 8, 9, 13); no static think-cell chart exhibits
remain. No engine (`deck_core/charts.py`) behavior changes were needed — both slides reuse params the
slide-6/13 work already added. Repo: `projects3/ooxml_build_pipelines_light`; deck at
`projects/mro/deck/`; output `projects/mro/20260607_Defense Drivers MRO_vS.pptx`.

## Slide 8 "Top-Down Composition" — native single stacked column (`topdown_detail.py`)
Same single-fat-column shape as slide 6, so a direct repeat of that pattern. The right-side rollup
table (`slide08_table.xml`) stays transcribed VERBATIM; only the left static chart was swapped. Build
went 4 charts (was 3).

**Faithfulness facts (from `_chart_xml/slide08.xml`).** Six segments bottom→top in **pure accent
order accent1..6** (no accent5/6 swap, unlike slide 6): Public NSY 44% / 1B4B Private avails 25% /
OPN LI 1000 14% / SCN LI 2086 RCOH 9% / MSC M&R 7% / USCG ISVS 1% (= $16,996M total). In-bar label
colors: white forced (`label_color="FFFFFF"`) on accent1–4 (same accent4-is-borderline-bright reason
as slide 6), auto-black on the light accent5/6 tops. Bar geometry is the **same x/width as slide 6**
(L 6.51% / W 29.64%), so it reuses slide 6's `graphic_frame`
(x=465138,y=1660000,cx=3946525,cy=4180000); `plot_layout` recomputed to slide 8's exact bar/axis EMU
= `{0.0833, 0.0187, 0.9155, 0.9441}` (pins all four edges within ~1 EMU: left 793750, right 4406900,
100%-line 1738313, 0%-line 5684838). Value axis 0–100% / 5% ticks; dark-navy axis lines; no
gridlines/native legend. Category label "Total FY2025" from catAx. Overlays: the $16,996M total + the
6-entry vertical legend (USCG ISVS→Public NSY, transcribed y-positions).

**The 1% chip (caught in review by the user).** The 1% USCG ISVS sliver is too thin to hold an in-bar
label, so the source bumps "1%" **above** the bar onto a small rectangle **filled with the segment's
own accent6** (the source label shape carries `<a:solidFill><a:schemeClr val="accent6"/>`; the
44/25/14/9/7% labels are all `noFill` — check the source label-shape fills to see which need this). A
native centered label can't do this, so: set `hide_labels:True` on the accent6 series (verified
`USCG ISVS dLbls=False`, the other five keep theirs) and **overlay the chip** as a `text_box`
(fill=`CHART_ACCENT_6`, `line_color="none"` to beat the house auto-border, at the source x/y
2513013/1697038 — which is coincidentally where the suppressed native label would have centered).
Chip text is `bold` to match the engine's other in-bar labels (the whole slide's native labels render
bold non-italic vs the source's italic — a pre-existing slide-6 tradeoff, applied consistently).

chart verified: native 6-series stacked `barChart` + manualLayout + max/min/majorUnit + embedded
editable workbook; render matches `src-08.png` (colors/order, white dividers, 5% axis, in-bar label
colors, the 1% chip, $16,996M, category label, legend, geometry). Round-trips soffice, no Repair.

## Slide 7 "TAM Composition" — native 6×6 MARIMEKKO via POSITIONAL series (`tam_composition.py`)
6 segments × 6 hull columns. **This one needed a new technique** — NOT a direct repeat of slide 13 —
because the source **size-sorts each column's segments** (largest at the bottom), so the columns do
not share one segment order (Surface Combatants has Depot/grey at the bottom; Submarines has
Nuclear/navy at the bottom 60%). A by-segment native percentStacked (one series per segment, the
slide-13 approach) forces ONE global order and would visibly reshuffle several columns. Build went 5
charts.

**Positional-series fix.** Instead of one series per segment, build one series per **stack layer**
(Layer 1 = bottom band, Layer 2 = 2nd band, …) and color each *bin* individually with
`data_point_colors`. Layer 1 sits at the bottom of every column but carries each column's own bottom
segment + its accent, so every column keeps its exact source bottom→top order while the chart stays
native + Edit-Data-backed. Empty top layers (columns with <6 segments) get value 0 / a dummy color.
Built with `column_chart(mode="percent", categories=[""]*200, series=<6 positional layers>, …)` (not
`marimekko_chart`, which only emits by-segment series). Bin allocation (∝ width, largest-remainder) is
replicated in-module as `_alloc_bins` (mirrors `charts._allocate_bins`) because it's also needed for
the vertical dividers.

**Why this also keeps the overlay verbatim.** Because the native cells now land in the *exact* source
order/proportions, the source's in-cell %s, the tiny-segment leader chips (small accent squares +
their `1%/2%/0%` labels, at non-column x's), the legend, the $M + vessel headers, and the "Segment
composition by hull" rail title all overlay correctly — kept verbatim by the same filter idiom as
slide 13 (`_overlay()` drops only the colored cells `x∈_COL_X & accent`, the source value-axis labels
`%-text & x<900000`, and the axis lines `cxnSp & x∈{839788 ticks, 868363 baseline, 873125 spine}`).
Seamless render (`seg_line_color=None`) + overlaid white dividers (5 vertical between columns at bin
boundaries, 22 horizontal between segments at cumulative source heights). Caption / commentary rail /
footer stay deck_core primitives (never part of the extracted exhibit — confirmed `slide07.xml` has
no caption/commentary/footer text).

**Data facts.** Widths ∝ FY2025 $M at ≈790 EMU/$M (2239/1441/2093/769/759/1667). Segment→accent (from
the legend, NOT stack position): 1 Depot / 2 Nuclear&Complex / 3 HM&E / 4 Combat / 5 Electronics / 6
Port. Per-column stacks bottom→top (accent, EMU height), transcribed from the source cells:
- Surface Combatants:       (1,2871788)(3,192088)(4,192088)(2,190500)(6,138113)
- Amphibious Warfare Ships: (1,3346450)(3,192088)(6,46038)
- Submarines:               (2,2149475)(4,762000)(3,319088)(5,276225)(1,71438)(6,6350)
- Combat Logistics Ships:   (1,2986088)(6,409575)(3,188913)
- Aircraft Carriers:        (1,1720850)(2,1592263)(6,160338)(3,95250)(5,15875)
- Other:                    (1,1277938)(3,1060450)(6,430213)(2,415925)(5,358775)(4,41275)

Plot rect pinned x 873125..7956551, y(100%) 2047875 → y(0%) 5632451 via `_FRAME`
{430000,1860000,7740000,3900000} + `_PL` {0.057251,0.048173,0.915171,0.919122}.

chart verified: native `percentStacked`, 6 series, **1200 `<c:dPt>` per-bin color overrides (all
seamless `<a:ln><a:noFill/></a:ln>`)**, manualLayout + max/min/majorUnit, 200 blank bins, embedded
editable workbook; ~302KB (the 1200 dPt — the cost of per-bin coloring; drop `total_bins` to ~120 to
roughly halve it if leaner is ever wanted). Round-trips soffice, no Repair. Render matches `src-07.png`
tightly (widths, per-column order, colors, dividers, in-cell %s, leader chips, legend, headers).

## Documentation (so future agents reuse the techniques)
- `deck_core/slide_snippets.md` → `## charts > ### Recipes`:
  - **Recipe E2 — per-column-sorted marimekko (POSITIONAL series)** (slide 7 technique).
  - **Recipe F — thin-segment label chip** (slide 8 technique).
- `deck_core/charts.py` — extended the `hide_labels` docstring to note its second use (suppress a
  too-thin segment's label to overlay a chip), cross-referencing recipe F. Docstring-only.
- Memory `mro-deck-native-port.md` — marked slides 7+8 done, recorded the positional + chip
  techniques, set status "ALL MRO chart exhibits now native".
- These doc edits are markdown/docstring-only — no behavior change.

## Verify / regenerate
```bash
cd /Users/brendantoole/projects3/ooxml_build_pipelines_light
/usr/bin/python3 projects/mro/deck/build_deck.py            # green: 15 slides, 5 charts
OUT=projects/mro/deck/_qa/png
PPTX="projects/mro/20260607_Defense Drivers MRO_vS.pptx"
soffice --headless --convert-to pdf --outdir "$OUT" "$PPTX"
pdftoppm -png -r 220 -f 7 -l 8 "$OUT/20260607_Defense Drivers MRO_vS.pdf" "$OUT/built"
# source at 300dpi for diff: pdftoppm -png -r 300 -f 7 -l 7 _qa/src_png/…v3.3.pdf …
```
Regression: all decks rebuild green — **mro 5** / consolidated 4 / ddg 9 / subs 9 / sea_range 0. The
engine was untouched (both slides reuse opt-in params), so nothing else moved.

## Status: conversion project COMPLETE
All five MRO chart exhibits are native: slide 6 (stacked column), slide 7 (6×6 positional marimekko),
slide 8 (stacked column + 1% chip), slide 9 (bundled funnel, already native), slide 13 (5-col
marimekko). Every other static `_chart_xml/*.xml` read is a diagram / funnel / bridge / table with no
chart equivalent (verified: zero accent-fills + zero %-labels on slides 4/5/10/11/12/14/15).
