# 2026-06-08 — Consolidated deck: native charts restyled to the MRO static think-cell look

Restyled the four native `column_chart()` slides in `deck_consolidated` (s02, s11, s12,
s13) to mirror the MRO static think-cell exhibits — **while keeping them native and
editable** (not flattened to shapes). The work split into a small, backward-compatible
extension to the shared chart engine plus per-module styling. Reusable how-to lives in
`docs/faithful_deck_port_methodology.md`; this is the consolidated-side application.

## The think-cell signature being mirrored (verified from MRO `_chart_xml/slide06.xml`)
- `accent1–6` Saronic gray-blue fills (not the BLUE program ramp)
- **0.75pt white (`bg1`) segment dividers** (`<a:ln w="9525"> FFFFFF`)
- **0.75pt dark-navy (`tx1`=`162029`) axis line** on cat + val axes
- **8pt** labels; **no** native legend, **no** gridlines

## 1. Engine change — `deck_core/charts.py` (backward-compatible, byte-identical defaults)
Added optional params, defaults = the historical behavior, so MRO/DDG/submarines charts
are untouched unless they opt in:
- `_build_series`: `seg_line_color="000000"`, `seg_line_width=6350` — replaced the two
  hardcoded `<a:ln w="6350">…000000…` borders (series-level + per-point `c:dPt`). **No
  `cap` attr** on the segment border so the default string is byte-for-byte the old one
  (cap is irrelevant on a closed rectangle outline).
- `_bars`: same `seg_line_*` (forwarded to `_build_series`) plus `axis_line_color=None`,
  `axis_line_width=9525`. When `axis_line_color` is set, injects a `<c:spPr><a:ln>` into
  **both** `catAx` and `valAx`, in the CT_CatAx/CT_ValAx slot after `<c:tickLblPos>` and
  before `<c:txPr>` (else PowerPoint repairs).
- `column_chart` needed no change (it `**kwargs`-forwards to `_bars`).

Regression proof: MRO uses **no** generated charts (its 1 chart is bundled static XML),
so it's definitionally unaffected. DDG (9 charts) + submarines (9 charts) never pass the
new params — confirmed all 9+9 retain the old black 0.5pt border, 0 injected axis lines,
no white segment borders. All three decks rebuild green.

## 2. Palette — `deck_core/style.py`, CHARTS ONLY
Added `CHART_ACCENT_1..6` (+ `CHART_ACCENT_SCALE`/`CHART_ACCENT_TEXT`/`chart_accent_pair()`)
= the theme accent hexes (`79838F/1D4D68/486D82/89A2B0/AFC2CC/D8E3EB`). **Named and
commented "CHARTS ONLY"** at the user's explicit instruction — do not use for shapes,
tables, text, or chrome (the general palette stays BLUE_*/GRAY_*). The name itself flags
misuse.

## 3. Color mapping = positional progression, gray-reserved rule
Studied the actual MRO progression (parsed `_chart_xml/slide06.xml`/`slide08.xml`): stacked
segments step through the theme accents **in index order, bottom→top, same sequence per
column**. Then the user refined it: `CHART_ACCENT_1` (79838F) is the **gray** accent and
`CHART_ACCENT_2..6` are the **blues**, so —
- a **1-v-1 (two-series) chart uses accent1 (gray) + accent2 (blue)**;
- a **3+ segment/column chart starts at accent2 and steps through the blues**
  (accent2 → accent3 → accent4 → …).

Colors follow **stack/column position** (series index 0 = bottom = first accent), not
program identity. Final assignment:
- s11 (1-v-1, stacked): DDG=accent1 (gray, base), Submarine=accent2 (blue, upper)
- s12 (3, stacked): Submarine=accent2, DDG=accent3, Residual=accent4 (separate column)
- s02 (3, stacked): Submarine=accent2, DDG=accent3, Broad-SAM=accent4 (comparison column)
- s13 (5 cols, clustered): accent2→accent6 across Broad, HM&E, Electrical, Metal, Modular

Consequence (flagged): a program's color **varies across charts** (color by position, not
identity) — faithful think-cell behavior; each chart's color key disambiguates. Stack
ORDER unchanged; only fills. In-bar label readability handled by the engine's auto
white/black flip (`_label_color_on`). (Two earlier maps this session — program-consistent,
then raw accent1→N — were superseded by this gray-reserved rule.)

## 4. Per-module (`deck_consolidated/slides/`)
- All four: series → accent map; `seg_line_color="FFFFFF", seg_line_width=9_525,
  axis_line_color="162029"`; `show_gridlines=False`, `show_legend=False`;
  `value_label_size_pt=8, cat_label_size_pt=8`. (s13's 14pt KPI labels → 8pt; renders fine.)
- s02 keeps its 14pt overlay total labels and its **BLUE_* hero/support cards** (cards are
  not charts → stay on the deck palette). Result: s02's submarine support card (BLUE_4
  `3D5972`) is a slightly different blue than the chart's submarine segment (accent2
  `1D4D68`) — a deliberate consequence of "accents = charts only"; reads coherent.

## 5. Manual color key — `deck_core/chart_key.py` (promoted from the consolidated deck)
`chart_key(sp_id, x, y, h, [(label, fill), …])` emits a horizontal row of [filled-rect
swatch + 8.5pt label] — replaces the dropped native legend on s02/s11/s12 (s13 keeps its
own composition legend + per-point category labels). Labels use `wrap="none"` (never wrap)
and a 1.25× width-safety factor for spacing (the 0.50 avg-char model under-measured
capital-heavy labels like "DDG"/"Submarine" → first render wrapped; fixed). Each chart's
`graphic_frame` cy shrinks by ~210k EMU to seat the key in the old footprint.

## 6. QA harness — new `projects/consolidated/deck/_qa/render.sh`
Modeled on MRO's (soffice→PDF→`pdftoppm -r 96`→`_qa/png/slide-N.png`). Consolidated is
greenfield (no `src_png`), so the style target is MRO's rendered `slide-06/07/08.png`.

## Verify / regenerate
```bash
cd projects/consolidated/deck && /usr/bin/python3 build_deck.py     # green: 23 slides, 4 charts
rm -f _qa/png/*.pdf _qa/png/*.png && bash _qa/render.sh             # all 23 -> _qa/png/slide-NN.png
```
Visually confirmed slides 2/11/12/13: accent fills, white dividers, dark cat+val axes,
8pt labels, no gridlines/legend, key reads on single lines. Charts remain editable
(`ppt/charts/chartN.xml` + `ppt/embeddings/…xlsx` present). Deck round-trips through
soffice (586KB PDF) — no Repair.

## 7. deck_core reusables (so future charts get the look without boilerplate)
Promoted/added to deck_core (all surgical, additive):
- `deck_core/chart_key.py` — `chart_key()` moved here from the consolidated deck (it only
  depended on deck_core). Kept out of `primitives.py` to preserve that module's
  minimal/self-contained charter (chart_key needs `text_metrics`).
- `deck_core/charts.py` — **`THINKCELL_BARS`** kwargs dict (the 7 look params). Spread it;
  verified byte-identical to passing them explicitly. + a 3-line docstring pointer.
- `deck_core/style.py` — **`chart_accent_seq(n)`** encodes the gray-reserved rule (n==2 →
  accent1+accent2; n≥3 → accent2…); verified to reproduce s11/s02/s12/s13's fills.
- `deck_core/slide_snippets.md` — one pointer line in the charts section.

Future chart = `column_chart(mode=..., categories=..., series=[{...,"color":c} for c in
chart_accent_seq(n)], **THINKCELL_BARS, value_axis_format=..., gap_width=...)` + a
`chart_key(...)` where the legend used to sit. The consolidated modules still pass the 7
kwargs explicitly (not retro-fitted to the preset; the preset is the go-forward shortcut).

## Files
- `deck_core/charts.py` (seg/axis params + `THINKCELL_BARS`), `deck_core/style.py`
  (`CHART_ACCENT_*` + `chart_accent_seq`), new `deck_core/chart_key.py`,
  `deck_core/slide_snippets.md` (pointer)
- `deck_consolidated/slides/{s02_body_executive_answer,s11_body_annual_cadence,
  s12_body_work_type_allocation,s13_body_sam_scenario_menu}.py`
- new `projects/consolidated/deck/_qa/render.sh`
