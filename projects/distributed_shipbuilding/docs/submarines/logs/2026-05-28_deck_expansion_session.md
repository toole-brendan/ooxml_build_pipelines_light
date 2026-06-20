# 2026-05-28 — Deck expansion session: 6 → 11 slides + embedded chart workbooks

## Scope

Executed [2026-05-28_deck_expansion_plan.md](../2026-05-28_deck_expansion_plan.md)
and its OOXML
[companion](../2026-05-28_deck_expansion_ooxml_companion.md). Expanded the
methodology side deck from 6 slides to 11, added Executive Answer at
slot 2 plus four findings slides between Methodology and
Meaning-and-Limits, and rewired `deck_submarines/charts.py` to emit per-chart
embedded `.xlsx` workbooks so PowerPoint's "Edit Data" button works
on every chart in the deck. Final state: 11-slide deck builds clean,
2 native charts with embedded mini-Excel workbooks, all parts pass
ZIP + XML integrity checks.

Workbook companion changes: 5 new accessor functions, 37 new DeckData
figure rows across 5 new sections (DD-S2 / S7 / S8 / S9 / S10), 3
new reconciliation checks (CHK-13 / 14 / 15). No new sheets.

---

## 1. Workbook accessors (Phase 1)

Small, surgical additions to two producer sheets — no analytical
changes:

- `top_vendors.py`:
  - `top_n_dollars_cell(n)` — `Top_Vendors!E{row}` for rank N (1-50)
  - `top_n_name_cell(n)` — `Top_Vendors!D{row}` for rank N
  - `dollars_range(start, end)` — `Top_Vendors!E{r1}:E{r2}` for SUM aggregation
- `dod_pop.py`:
  - `other_us_pct_cell()` — Other US % aggregate cell
  - `foreign_pct_cell()` — Foreign % aggregate cell

Rebuild confirmed `sub.xlsx` byte count unchanged at 43,966 bytes
(accessors are pure functions, no rendered side effects).

## 2. DeckData expansion (Phase 2)

Appended 5 new section banners + 37 figure rows under row 49,
keeping every existing DeckData row stable (no consumer breakage):

| Section | Rows | Purpose |
|---|---:|---|
| DD-S2 (Executive Answer) | 8 | 6 republishes from DD-S5 + 2 derived (FY27 Va+Col Low/High sums) |
| DD-S7 (Annual Modeled Pool) | 12 | Va + Col Out_Mid per FY FY22-FY27 |
| DD-S8 (Visibility Gap) | 5 | Window-matched FY22-FY26 throughout |
| DD-S9 (Geography) | 7 | Includes derived unparsed residual (DD-S9-07) |
| DD-S10 (Supplier Concentration) | 5 | Top-N concentration ladder |

The contract pattern "one slide reads one DeckData section" — every
figure a slide displays republishes through that slide's own DD-Sx
block. Slide 8 doesn't reach into DD-S5 even though six of DD-S8's
five cells could in principle resolve from existing DD-S5
republishes; the contract trades a small amount of formula
duplication for slide-level decoupling.

### Window-alignment fix on DD-S8-05

The plan's critique #2 — and the most analytically important
addition — is **DD-S8-05**, the window-matched FY22-FY26 floor cell.
Previously the Visibility Gap bridge would have subtracted DD-S5-02
($6.14B cum FY16-FY26) from DD-S8-03 ($24.5B cum FY22-FY26),
mixing windows. DD-S8-05 forces the bridge into one window
(FY22-FY26 for both terms), so the visible $19.9B unseen layer is
math-honest. DD-S8-04 reads DD-S8-03 − DD-S8-05 (not DD-S5-02).

### Forward refs within DeckData

DD-S8-04 references DD-S8-03 and DD-S8-05 — its own neighbors.
Excel resolves cross-cell refs at load time, not at write time, so
forward refs within a sheet are fine. Same shape used on DD-S9-07
(reads DD-S9-01/02/05/06). The build script doesn't care about
declaration order.

DeckData sheet grew from 15,982 → 32,879 bytes (~doubled — consistent
with 5 banner sections + 37 data rows on a 35-row sheet).

## 3. Reconciliation checks (Phase 3)

Three new CHK rows; sheet grew from 7,087 → 8,433 bytes:

- **CHK-13** — DD-S2-01 (FY27 Mid republish) == DD-S5-01 (canonical).
  Catches a regression where DD-S2-01 gets hardcoded instead of
  reading `=DeckData!D29`. Tolerance $1M.
- **CHK-14** — DD-S8-03 (cum modeled Mid FY22-26 Va+Col) ==
  SUM(Funnel out_mid FY22-26 Va) + SUM(Col). Locks the Visibility
  Gap bridge's left-hand card against drift. Tolerance $1M.
- **CHK-15** — DD-S10-04 (top-50 share republish) ==
  SUM(Top_Vendors!E6:E55) / Subaward_Annual!O8. Same expression
  CHK-10 validates on Top_Vendors itself, but on the DeckData copy.
  Distinct because a stale hardcoded DeckData republish would not
  be caught by CHK-10. Tolerance 0.0001.

Needed a new import in `checks.py`: `derived_cell as _dd` from
`deckdata`, plus `cumulative_metric_range` from `funnel`. No
circular-import risk — deckdata doesn't import from checks.

Final workbook: 14 sheets, 15 checks, **46,108 bytes**, ZIP + XML
clean.

## 4. charts.py rewrite for embedded workbooks (Phase 4)

The high-uncertainty technical work in this PR. The plan's
companion doc had the full mechanics; I followed it but deviated
slightly on the `chart_rels` API (see below).

### What changed

`make_clustered_bar_chart` now returns a `dict`:

```python
{
    "chart_xml":  str,    # ppt/charts/chartN.xml body
    "embed_xlsx": bytes,  # complete .xlsx zip
    "chart_rels": str,    # template; lib.py fills {chart_num}
}
```

`_build_series` learned an `embed_data: bool` flag:

- **`True` (default)** — emits `<c:strRef>` / `<c:numRef>` with parallel
  `<c:strCache>` / `<c:numCache>` blocks. Cell-formula references
  point at `Sheet1!$A$2:$A$N` (categories) and `Sheet1!$B$2:$B$N` /
  `Sheet1!$C$2:$C$N` / ... (one column per series). Series-name tx
  uses real cell refs (`Sheet1!$B$1`) instead of fake formulas
  (`Series1`).
- **`False`** — legacy behavior, emits `<c:strLit>` / `<c:numLit>` inline
  literals. Edit Data stays disabled. Kept for backward compat;
  the slide-side surface is identical (`embed_data` defaults to `True`).

A new `<c:externalData r:id="rId1"><c:autoUpdate val="0"/></c:externalData>`
element appears at the end of `<c:chartSpace>` after `</c:chart>` (the
ordering matters per cheat sheet §27 gotcha).

### Inner xlsx generator

Five static OOXML parts as module-level constants
(`_EMBED_CONTENT_TYPES`, `_EMBED_ROOT_RELS`, `_EMBED_WORKBOOK`,
`_EMBED_WORKBOOK_RELS`, `_EMBED_STYLES`) plus one dynamic part
(`_build_sheet1`). All packed into a `zipfile.ZipFile(io.BytesIO(),
"w", ZIP_DEFLATED)` and returned as bytes.

Sheet1 layout:
- Column A: category labels (inline strings)
- Column B/C/...: per-series values, one column per series
- Row 1: header (`cat_header` in A; series names in B+)
- Rows 2 onward: one row per category

Blank handling: None / NaN values render as empty cells in the
sheet (`<c r="C2"/>` with no `<v>` child) and are also omitted from
the chart cache (`<c:pt idx="i">` only emitted for non-blank
values). The chart's `<c:dispBlanksAs val="gap"/>` already maps
those to visual gaps. The plan recommended passing 0 for sparse
Columbia FYs over None — slide 7 follows that recommendation since
0-height columns read visually as "no bar" and editors opening
Edit Data can adjust them in place.

### chart_rels API deviation

The plan asked `make_clustered_bar_chart` to return a complete
`chart_rels` XML string. Problem: each chart's rels file must point
at `../embeddings/Microsoft_Excel_Worksheet{global_chart_num}.xlsx`
— but the chart-generator function doesn't know the global chart
number (it's only assigned in `lib.py::build()`). Solution: return
a **template string** with `{chart_num}` Python format-placeholder;
`lib.py` calls `chart_rels.format(chart_num=global_chart_num)` when
it writes the part. Keeps responsibilities clean (charts.py owns
chart-XML mechanics, lib.py owns deck-wide numbering).

### lib.py build-loop changes

The CHARTS iteration now accepts either a dict (new shape) or a
bare XML string (backward compat). When a chart provides
`embed_xlsx`:

- Writes `ppt/charts/_rels/chart{N}.xml.rels` (chart_rels formatted)
- Writes `ppt/embeddings/Microsoft_Excel_Worksheet{N}.xlsx`
- Bumps `embedded_xlsx_count`

`_content_types_xml` takes a new `num_embedded_xlsx` param and
emits one `<Override>` entry per embedded workbook. The chart's
own rels file is matched by the existing
`<Default Extension="rels" .../>` line; no Override needed for it.

### De-risking smoke test

Per the plan, ran a standalone test of `make_clustered_bar_chart`
before writing any production chart slide. Confirmed:
- Returns the three-key dict with both bytes (embed_xlsx) and strings (chart_xml, chart_rels template)
- `chart_xml` parses; contains `<c:strRef>`, `<c:numRef>`, `<c:externalData>`, correct cell ranges (`Sheet1!$A$2:$A$7`, `Sheet1!$B$2:$B$7`, `Sheet1!$C$2:$C$7`)
- `embed_xlsx` is a valid zip with the 6 expected files; each XML part parses
- Sparse cells (Columbia FY22 / FY23 / FY25 if None-valued) render as empty cells in `sheet1.xml`

Also confirmed the existing 6-slide deck (no CHARTS exposed by any
slide) still builds clean with zero chart / embed parts produced —
the embedded-workbook code path is genuinely opt-in per slide.

## 5. Five new slide modules (Phases 5-9)

Built in plan-recommended order: chartless slides first (2, 8, 9),
then chart slides (7, 10) once the embedded-workbook plumbing was
verified. Each module follows the locked-chrome conventions in
`body_template.py`; helpers stay slide-local per the rule.

### Slide 2 — `executive_answer.py` (~21 KB rendered)

Left hero tile (BLUE_5 anchor, 1.5pt border) carrying "$9.45B" at
54pt headline size, a smaller caption, a BLUE_4 formula strip, and
three scenario pills (BLUE_2 / BLUE_4 / BLUE_2 — Mid is focal).
Right 2x2 KPI grid: FFATA-visible floor / Lag-adjusted floor /
Observed coverage / Outside-yard lens.

Card 4 ("Outside-yard lens") carries two numbers stacked in one
value cell ("75.5% and 63.5%") rather than splitting into a fifth
card. Caption uses semicolon as separator ("outside EB yard;
outside team yards"), not slash, per the prose rule.

The hero number is the only place in the deck where a single
number gets headline-size treatment. Used `size=5400` (54pt) — 60pt
felt heavy in the 4.65M-EMU hero tile.

### Slide 8 — `visibility_gap.py` (~21 KB rendered)

Two bar gauges at top (Observed 19%, Lag-adjusted 22%) — each is a
GRAY_1 track with a BLUE_4 fill segment whose cx is the track cx
times the pct, plus a big % value to the right of the fill. The
two gauges share track width so the difference reads visually.

Middle bridge band: three BLUE_1 cards with `mathMinus` and
`mathEqual` operator AutoShapes between them, vendored from
`methodology.py`. All three values are window-matched FY22-FY26.
The vertical position of each 300k-EMU operator is centered inside
the 1M-EMU card height via `(card_h - op_h) // 2`.

Right callout panel: inline-glyph bullet list (5 items) explaining
what sits in the unseen layer. Used the multi-paragraph
`_multiline_textbox` helper (one `<a:p>` per line) rather than
PowerPoint-canonical `<a:buChar char="•"/>` because the marauder
N81 slides established the inline-glyph pattern and the visual
result is identical with simpler layout plumbing.

### Slide 9 — `geography.py` (~17 KB rendered)

Stacked horizontal bar made entirely of layered `<p:sp>`
rectangles — no chart library. 5 segments left to right:

| Segment | Pct | Fill | Text color |
|---|---:|---|---|
| EB | 24.5% | BLUE_5 | WHITE |
| HII | 12.1% | BLUE_4 | WHITE |
| Other US | 55.2% | BLUE_2 | DK |
| Foreign | 0.0% | (omitted from bar) | — |
| Unparsed | 8.3% | GRAY_1 | DK |

The Foreign segment renders below the 100k-EMU degeneracy threshold
(its `cx = 7.4M × 0.000 = 0`), so a build-time guard skips it
entirely. The caption strip under the bar names it explicitly:
"Foreign 0.0% omitted from bar; segment widths under 100k EMU
collapse."

Border-sharing handled by suppressing internal segment borders
(`border_color=None` on each rect) and painting a single 1.5pt
black outer frame on top (no-fill rect with `border_w=19_050`). No
doubled internal seams.

Right column: two stacked KPI cards (outside EB 75.5%, outside
team 63.5%). Middle: caveat band naming the parser miss
(METHODOLOGY §6, ~$1.6B affected, CHK-12 tolerance ±10pt).

### Slide 7 — `annual_modeled_pool.py` (~12 KB rendered + 6 KB chart + 2 KB embed)

First chart slide. Native clustered column chart via
`make_clustered_bar_chart(horizontal=False, ...)` with two series
(Va BLUE_4, Col BLUE_2) across 6 FYs.

Values pulled at module-import time from
`cost_funnel_per_class.csv` (verified via direct CSV read at plan
time): Va `Out_Mid` = [2854.97, 3057.27, 5442.46, 3195.93, 1882.08,
5333.59], Col `Out_Mid` = [0, 0, 3813.65, 0, 4295.86, 4112.24].
Columbia's sparse FYs (FY22, FY23, FY25) are passed as `0.0` not
`None` per the plan's recommendation; the footer caption explains
("Columbia procurement timing creates sparse fiscal-year columns;
blanks are not zero-demand years").

Chart kwargs: `value_axis_format='"$"#,##0,"M"'`,
`value_label_format='"$"#,##0"M"'`, `show_legend=True`,
`legend_pos="b"`, `show_gridlines=True`, `gap_width=120`,
`bar_overlap=-20`.

Right panel: three BLUE_1 cards (FY27 midpoint $9.45B, Va BC
$8.89B, Col BC $6.85B) plus an italic GRAY_4 caption (no border)
giving the band-logic prose. Card heights tuned to 920k cy so
three cards + an italic caption fit in the 4.2M cy panel.

### Slide 10 — `supplier_concentration.py` (~14 KB rendered + 6 KB chart + 2 KB embed)

Second chart slide. Horizontal bar chart with per-bar colors
(top-1 BLUE_5, ranks 2-5 BLUE_4, ranks 6-10 BLUE_2) to visualize
the top-5 concentration cliff.

Top-10 vendor names + dollars read from
`sam_subaward_top_parents.csv` at module-import time, MIB-filtered
the same way the workbook's `top_vendors.py` filters. Display
names abbreviated (e.g. "NORTHROP GRUMMAN SYSTEMS CORPORATION" →
"Northrop Grumman Systems Corp.") via a `_VENDOR_DISPLAY` dict
that lives in the slide module — display-only abbreviations; the
workbook keeps the legal names.

Categories reversed so rank 1 lands at the TOP of the horizontal
chart (otherwise NGSC ends up at the bottom and the visual
hierarchy fights the ranking story).

Right column: concentration ladder. Open ledger (no outer
container) with a header + 1.5pt black bottom rule + 4 rows
separated by 0.75pt GRAY_2 hairlines. Layered text boxes only — no
native `a:tbl` (decorative ranking, not data). Hairlines drawn as
9_525-EMU-tall filled rectangles.

## 6. lib.py reorder (Phase 10)

Three changes:
- `N_SLIDES_OUT = 11`
- Added 5 imports for the new slide modules
- Reordered `slide_module_renders` to the final 11-slot sequence:
  cover · executive_answer · framing · scope · cost_funnel ·
  methodology · annual_modeled_pool · visibility_gap · geography ·
  supplier_concentration · meaning_limits

`SLIDE_RELS` rebuild loop, `presentation_xml`, `presentation_rels_xml`,
`_content_types_xml`, `app.xml` are all already adaptive to
`N_SLIDES_OUT` — no manual edits needed beyond the count bump.

## 7. slide_topics.md sync (Phase 11)

Rewrote `sub_pptx/slide_topics.md` to match the 11-slide deck.
Added a DeckData contract table at the bottom mapping each slide
to its DD-Sx section, row count, and any notes (e.g. slide 11
reads DD-S6-* under the legacy section numbering).

---

## Final state

### Workbook

```
sub_workbook/sub.xlsx — 46,108 bytes
  14 sheets, 15 reconciliation checks
  DeckData: 99 figure IDs across 10 sections
    DD-S3 (9) + DD-S4 (8) + DD-S5 (8) + DD-S6 (9)  [original]
    DD-S2 (8) + DD-S7 (12) + DD-S8 (5) + DD-S9 (7) + DD-S10 (5)  [new]
  Checks: CHK-01..15 all in spec
```

### Deck

```
sub_pptx/sub.pptx
  Slides:   11
  Charts:   2 (chart1.xml + chart2.xml — both with embedded workbooks)
  Embeds:   3 (Worksheet1.xlsx + Worksheet2.xlsx + legacy oleObject1.bin)
  All XML parts parse; both inner xlsx zips test clean
```

| Slot | Slide | Bytes | Chart? |
|---:|---|---:|:---:|
| 1 | Cover | 965 | |
| 2 | **Executive Answer** | 20,959 | |
| 3 | Framing | 25,372 | |
| 4 | Scope and Definitions | 38,816 | |
| 5 | Cost Funnel | 34,528 | |
| 6 | Methodology | 23,939 | |
| 7 | **Annual Modeled Pool** | 11,965 | ✓ |
| 8 | **Visibility Gap** | 20,918 | |
| 9 | **Geography** | 17,110 | |
| 10 | **Supplier Concentration** | 13,511 | ✓ |
| 11 | Meaning and Limits | 37,014 | |

## Architectural notes

### Workbook and pptx are NOT connected

Mid-session the user asked whether the workbook (`sub.xlsx`) and
the pptx are being linked. They are not — and won't be. The
relationship between them is one of **manually maintained
correspondence**, validated internally by CHK rules in the
workbook. The slide modules hardcode values in their Python
source; an analyst keeps those values in sync with DeckData by
hand.

The **embedded mini-Excel workbooks per chart** (the Phase 4 work)
are separate from this. Each chart's embed is a fully
self-contained snapshot of that chart's data, packed inside the
.pptx zip at `ppt/embeddings/Microsoft_Excel_Worksheet{N}.xlsx`.
PowerPoint opens it via "Edit Data" exactly like any other native
chart. No external link to `sub_workbook/sub.xlsx`.

The deck remains a standalone deliverable — it ships with all the
data it needs to render and be edited. The workbook is the
analytical source of truth for the analyst, not for the deck at
runtime.

### CHARTS dict shape — backward compat

`lib.py::build()` accepts either form in a slide's `CHARTS` list:

```python
# Old shape (literal data, no embed):
CHARTS: list[str] = [chart_xml_string]

# New shape (default for make_clustered_bar_chart):
CHARTS: list[dict] = [{
    "chart_xml":  str,
    "embed_xlsx": bytes,    # or None
    "chart_rels": str,      # or None — template with {chart_num}
}]
```

Detection is `isinstance(chart, dict)`. Allowed for a smooth
incremental migration; the existing 6 slides exposed no CHARTS at
all, so no migration was actually needed in this PR, but the
escape hatch exists for future ad-hoc literal charts.

### Chart-rels template pattern

Because charts.py emits chart_rels but doesn't know the global
chart number, the rels XML carries a `{chart_num}` Python
format-placeholder:

```xml
<Relationship Id="rId1"
  Type="...relationships/package"
  Target="../embeddings/Microsoft_Excel_Worksheet{chart_num}.xlsx"/>
```

`lib.py::build()` calls `chart_rels.format(chart_num=N)` at write
time. Trivial mechanism; keeps charts.py decoupled from deck-wide
chart numbering.

### Inner-xlsx encoding choices

- **Inline strings, not sharedStrings.** Categories + series names
  go in cells as `<c r="A2" t="inlineStr"><is><t>...</t></is></c>`.
  Saves one OOXML part (no sharedStrings.xml) at the cost of
  duplicating string content on rare repeats. Top-10 vendor names
  are all unique so the trade-off is free in this deck.
- **No custom number formats in the embed.** `xl/styles.xml` is
  minimal — single default font, no numFmts. The chart's
  `c:formatCode` (e.g. `"$"#,##0"M"`) lives in the chart's cache,
  not in the embedded xlsx. Edit Data still shows formatted values
  because the chart cache controls display.
- **`autoUpdate="0"` on externalData.** "Don't refetch the embed
  every time the slide opens." The chart cache is authoritative
  for display; the embed is the source of truth for editing.
  Keeps PowerPoint from flickering on first open.

---

## Open follow-ups

1. **Wire the workbook → slide values for slides 7 and 10.** Right
   now both chart slides hardcode their numbers in module source
   (matching what DeckData publishes). The plan deferred the
   workbook-read step to a separate workstream. If wired, the slide
   modules would open `sub.xlsx`, look up figure IDs via
   `derived_cell('DD-S7-01')` etc., and bake the live values into
   the chart data at build time. Adds an openpyxl dependency or a
   stdlib xlsx reader.

2. **Verify "Edit Data" actually opens in PowerPoint.** The
   workbook structure passes static validation (ZIP, XML, all 6
   parts of each inner xlsx) but PowerPoint sometimes flags
   "repaired records" for issues static analysis misses. Need a
   visual check: open `sub.pptx`, right-click chart on slide 7 or
   10, choose Edit Data, confirm the mini-Excel pane opens with
   the correct values, edit a cell, save, confirm the chart
   updates. **Did not validate this session — user has the file
   open in PowerPoint, file lock blocked an inspection round at
   the end.**

3. **Cumulative-vs-annual mismatch on slide 4 band 3.** Still a
   labeling decision from the prior session. The Visibility Gap
   slide (8) sidesteps this by window-matching to FY22-FY26
   throughout; the Cost Funnel slide (4) does not yet.

4. **DD-S5-03 (floor coverage % FY22-FY26) was already redefined**
   in the prior fix-pack session; DD-S2-06 and DD-S8-01 just
   republish that figure. The lag-adjusted parallel DD-S5-08 is
   what DD-S2-06 and DD-S8-02 republish. No new analytical work.

5. **Long vendor-name overflow on slide 10.** Used display-only
   abbreviations in `_VENDOR_DISPLAY` dict. The longest still
   shown is "Curtiss-Wright Electro-Mechanical" (35 chars). If
   the chart's category axis cramps in PowerPoint, drop
   `cat_label_size_pt` from 9 to 8 or further abbreviate (e.g.
   "Curtiss-Wright EMC").

6. **No native a:tbl in any new slide.** The plan's recommendation
   to use native tables only for actual tabular data was honored:
   slide 5's lens ledger (built in the prior session) is the only
   native `a:tbl`. Slides 7 and 10 use layered text-box ladders
   instead. Slide 4 (Scope) still uses native `a:tbl` from the
   prior session.

7. **CHK-13/14/15 tolerance vintage tracking.** All three are
   formula-equality checks. CHK-13 ($1M tolerance) gives room for
   the 1-cent rounding floats Excel sometimes produces in chained
   ref formulas. CHK-15 (0.0001 percent equality) is tighter
   because top-50 share is a ratio. Worth periodically checking
   whether observed deltas drift past these tolerances if upstream
   data shifts.

---

## Reference files

- [logs/2026-05-28_workbook_review_fixpack.md](2026-05-28_workbook_review_fixpack.md) — DeckData figure-ID contract, CHK conventions, lag-adjusted floor cells
- [logs/2026-05-28_methodology_deck_session_2.md](2026-05-28_methodology_deck_session_2.md) — §12 conventions (color role table, locked title format, slide-local helpers rule), native a:tbl ghost-column pattern, GFE-prime list resolution
- [logs/2026-05-28_methodology_deck_session.md](2026-05-28_methodology_deck_session.md) — `_operator()` helper origin (`methodology.py:181-200`), `mathMinus` / `mathEqual` prstGeom AutoShapes
- [logs/2026-05-28_workbook_session.md](2026-05-28_workbook_session.md) — workbook architecture, ID-based accessor pattern, sparse-data formula patterns
- [../2026-05-28_deck_expansion_plan.md](../2026-05-28_deck_expansion_plan.md) — the plan document this session executed
- [../2026-05-28_deck_expansion_ooxml_companion.md](../2026-05-28_deck_expansion_ooxml_companion.md) — OOXML snippets and embedded-xlsx mechanics
- `sub_pptx/ooxml_cheat_sheet_pptx.md` §20-23 (chart architecture), §27 (gotchas — chartSpace element ordering)
- `sub_workbook/extracted/cost_funnel_per_class.csv` — Slide 7 source data (per-class per-FY P-5c Basic Construction)
- `sub_workbook/extracted/sam_subaward_top_parents.csv` — Slide 10 source data (top vendors, MIB-excluded)
- `sub_workbook/extracted/nc_scope_summary.json` — `excluded_mib_ueis` filter set for slide 10
