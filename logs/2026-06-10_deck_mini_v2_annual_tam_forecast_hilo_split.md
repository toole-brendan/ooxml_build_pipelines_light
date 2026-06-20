# 2026-06-10 — deck_mini_v2 slide 3 (Annual TAM): forecast bars split to low / high / retained

## Goal

Rework the bundled native chart on deck_mini_v2 slide 3 ("Outsourced Basic
Construction (Annual TAM)", chart4) so the FY28–31 forecast bars show the
outsourced range explicitly: implied LOW at the bottom, the low→high
INCREMENT stacked on it in a different fill, and the unfilled "retained"
segment on top — with retained being the SAME series per vessel in both the
actual (FY22–27) and forecast eras, while the outsourced segments stay
era-distinct per vessel. Plus (user iterations): both range bounds readable
as numbers, legend updated, and all dark chart numbers in true black.

## What the source chart was (decoded, byte-level)

`slide03_chart4.xml`: stacked barChart, gapWidth 0, overlap 100, valAx fixed
0–12, plotArea manualLayout. 39 implicit category slots = [DDG-51, Virginia,
Columbia, spacer] × 10 FYs (no trailing spacer; Columbia FY22/23/25 blank).
Only TWO series, styled entirely by per-point dPt overrides:

- row 1 "outsourced" (`Sheet1!$A$1:$AM$1`): actual-era bars in accent4 (DDG)
  / accent3 (Va) / accent2 (Col); **forecast bars cached at the HIGH end of
  the range** (e.g. Va FY28 3.317 = low 2.5515 + 0.7654) in BEBEBE
  (DDG/Va) / A1A1A1 (Col).
- row 2 "retained" (`$A$2:$AM$2`): white/noFill, stacks every column to FYDP
  gross (Va28: 3.317 + 7.517 = 10.833).

Everything else — dashed retained-box outlines (lgDash Va/Col, sysDot DDG),
bar-top gross totals, the small DDG "0.5"/"0.7", FY labels, both legend chip
groups, penetration strips — is transcribed CHROME in `slide03.xml`,
positioned to this exact bar geometry. The backing workbook was the original
2-row source `.xlsb` (reattached same-day via `editable_bundled_chart`).

## The re-split: 2 → 12 series, bar geometry untouched

Four series per class, mirroring workbook §4
(`workbook_consolidated/sheets/z_chart_data_outsourced_bc.py:222-227`,
`_*_OUTYEAR_LO_B` / `_*_OUTYEAR_HI_B` — HI asserted equal to the chart's own
forecast caches):

| series (×3 classes) | slots | fill |
|---|---|---|
| `X outsourced` | FY22–27 actuals | the class accent (was dPt overrides) |
| `X outsourced low` | FY28–31 | the era gray (BEBEBE; A1A1A1 Col) |
| `X outsourced high` | FY28–31 increment = HI−LO | pattFill ltUpDiag 486D82 on white |
| `X retained spend` | ALL 10 FYs, one series | FFFFFF (noFill dPt quirks unified) |

low + increment == old cached high and retained is reused verbatim, so every
column total — and all bar geometry under the fixed axis — is unchanged; the
chrome stays aligned with zero edits to positions. Series get literal names
(`<c:tx><c:v>`), refs `Sheet1!$A$N:$AM$N` rows 1–12.

## Labels (took 4 iterations — the learnings matter)

1. ~~"lo–hi" range string as a rich-text dLbl on the low segment~~ — wrong
   color inheritance, 7-char strings overflow the ~0.30in bars, collide.
2. ~~Same + segment-gray chip (dLbl spPr fill) moved onto the hatch~~ — the
   chrome dashed boxes paint AFTER the chart, so they cut THROUGH in-chart
   chips; chip covers the hatch/boundary so segment heights unreadable.
3. ~~Chips as chrome shapes painted last~~ — fixes dash-through but the wide
   strings still collide with neighbor-column retained labels; the stagger
   constraint window goes empty for some FYs. Dead end: WIDE labels cannot
   live anywhere in this packed cluster layout.
4. **FINAL: two SHORT numbers per forecast bar, no chips needed** (each
   ≤3 chars fits inside one bar width — zero spill, zero collisions):
   - LOW: numeric in-bar label centered in the gray low segment (source's
     label slot reused).
   - HIGH: the cumulative high (e.g. "3.3") as a LITERAL think-cell-style
     label (`<c:tx><c:rich>` override, showVal off, cloned c16:uniqueId
     stripped) floated via manualLayout c:y to ~0.45 value-units ABOVE the
     hatch top — inside the empty interior of the dashed retained box, where
     no boundary is covered and no dash crosses. Offset math: delta =
     (hi−lo)/2 + 0.45 units; chart-area fraction = plot-h/12 per unit.
   - The increment segment itself carries no numeric (it would mislead).
   - Bar reads bottom-up: low → hatch → high → retained → gross (chrome).
5. **All dark numbers true black** `srgbClr 000000` (user request): the
   source's dark labels were theme tx2 (gray-navy) and the forecast gray
   bars had bg1 WHITE labels; both promoted to black, matching the chrome
   totals (already 000000). The 21 white-on-dark-accent labels kept white.

## Legend (chrome, also derived)

Forecast legend group (x > 9.5in, 2 cols × 3 rows): the right column's three
per-class "retained spend" chips are REDUNDANT once retained is one series
per class across both eras (the actual-era group already chips it) →
replaced by ONE hatched chip "Outsourced upper range" on the middle row
(Rectangle 1001 refilled with the hatch + the borderless gray-chip ln;
rows 1/3 swatches + texts deleted). Actual-era group untouched.

## Mechanics — everything derived, regen-safe

- **`_qa/make_chart4_hilo.py`** (new, deterministic): reads the VERBATIM
  `slide03_chart4.xml` + `slide03.xml` and derives:
  - `slide03_chart4_hilo.xml` — the 12-series chart (only the two `<c:ser>`
    blocks replaced; every other byte identical). Harvested per-point dLbl
    entries are reassigned by slot to the new owning series.
  - `slide03_chart4_hilo.xlsx` — row-oriented 12×39 backing workbook
    (series N → Sheet1 row N+1, slots → cols A..AM), zip members cribbed
    from `deck_core.charts` constants. Replaces the 2-row `.xlsb`, which
    cannot back the 12-series refs.
  - `slide03_hilo.xml` — legend-patched chrome.
  - Asserts: workbook LO/HI reconcile with the chart caches (1e-9), every
    source point consumed exactly once, per-column totals unchanged, label
    census (13 actual + 12 low + 12 high + 27 retained = 64).
- **`outsourced_bc_annual_tam.py`**: loads the `_hilo` triplet;
  `CHARTS = [editable_bundled_chart(_CHART, _XLSX, embed_ext="xlsx")]`.
- **`_qa/regen_charts.sh`**: runs `make_chart4_hilo.py` after re-extraction,
  so a regen reproduces the derived assets instead of orphaning them.

## Verification

- Build green (6 slides, 5 charts). Built pptx: chart4 = 12 series with
  correct names/refs/fills, 64 dLbls, all c16:uniqueId unique, zero tx2
  left in labels; `externalData rId1` → `chart4.xml.rels` →
  `Microsoft_Excel_Worksheet4.xlsx` (Content-Types Override present; the
  other 4 charts keep their `.xlsb` — mixed embed types in one package,
  exercising the same-day lib.py generalization). Zero dangling rel targets.
- Render diff vs the verbatim-port render confined exactly to the forecast
  bars + forecast legend region; FY22–27 bars, retained boxes, totals, and
  the rest of the slide pixel-identical.
- soffice renders with no repair; forecast bars visually verified: gray low
  with black number, hatched increment, floating black high number, dashed
  retained box intact above.

## Caveats

- The 12 floating high labels are LITERAL text (think-cell idiom): editing
  data via Edit Data will not update them — `make_chart4_hilo.py` is the
  source of truth.
- Workbook §4's annex "lo–hi" strings round the same way (`:.1f`), so the
  chart bounds tie to the side-table strings exactly.
- deck_mini (the predecessor) still has the old single-high-segment chart;
  the same generator approach would port over if ever wanted.

## Resume

```bash
cd projects/consolidated/deck_mini_v2
/usr/bin/python3 _qa/make_chart4_hilo.py   # re-derive chart + xlsx + chrome
/usr/bin/python3 build_deck.py             # green = "6 slides, 5 charts"
rm -f _qa/png/*.pdf && bash _qa/render.sh  # compare _qa/png/slide-3.png
```

## Cross-references

- Same-day port + editable-xlsb logs:
  `logs/2026-06-10_consolidated_mini_v2_deck_port_all_6_slides.md`,
  `logs/2026-06-10_deck_mini_v2_charts_editable_xlsb_reattach.md`.
- §4 data source / think-cell layout rationale:
  `logs/2026-06-10_front_row_text_polish_and_chartdata_thinkcell_layout.md`.
- Label-chip idiom: `deck_core/slide_snippets.md` charts > Recipes > F
  (why chips exist; here superseded by short two-number labels).
