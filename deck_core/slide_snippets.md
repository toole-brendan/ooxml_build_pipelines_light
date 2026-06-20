# Slide Snippets — recipes and local-helper patterns

Companion to `slide_base_template.py` + `slide_guide.md`. The template **imports**
the common body builders from `deck_core.primitives` (`run`, `paragraph`,
`text_box`, `house_table`, `connector`) with the design tokens from
`deck_core.style`, and pre-wires the chrome. The low-level table engine
(`table` / `trow` / `tcell`) is **opt-in** — import it only where a merge-heavy
recipe explicitly says to. **This file is not a
second implementation of those builders** — it is a cookbook: how to call them,
when to wrap them in a slide-local `_helper`, and how to drop to raw OOXML for a
one-off visual.

> **Authoring posture**
> - Use the **imported builders** for stable OOXML mechanics — escaping, schema
>   order, insets, the filled-shape border rule, connector vector normalization.
> - Write slide-local `_`-prefixed helpers when they make the slide clearer.
> - Drop to raw `<p:sp>` / `<p:graphicFrame>` / `<p:cxnSp>` when a primitive does
>   not fit — custom geometry, connector attachments, unusual graphic frames, or
>   one-off schema constructs.
> - **These recipes are examples, not validation rules.** Copy and adapt them;
>   follow the style system in `slide_guide.md` (source of truth: `target_copy.txt`).
>   Stay inside `BODY`, on-palette, and sharp-rect except the controlled tags /
>   dots / chevrons.
> - `slide_probe` is a read-only **inspector**: run it to see a slide's geometry,
>   text, fills, borders, tables, charts, and (with `--table-fit`) estimated table
>   row-heights. It does not lint, score, or pass/fail anything.
> - **Example content is intentionally generic.** Labels such as `Category A`,
>   `Segment B`, and `Metric` are placeholders only — substitute the slide's
>   real content and do not treat snippet vocabulary as canonical.

How to use:
- The template already imports the builders and tokens these recipes use, plus
  `_esc` (`from xml.sax.saxutils import escape as _esc`) for raw-OOXML text.
- `p:cNvPr/@id` must be unique within the slide. Chrome uses 2, 3, 4, 9999; use
  10+ for body shapes. Charts: `rId2` = the slide's first chart (`rId1` is the layout).
- Adapt coordinates to `BODY` (`*BODY` unpacks it; index for sub-regions).
- Deeper OOXML mechanics (fills, lines, table cell props, chart data model,
  custom geometry, relationships) live in `deck_core/ooxml_cheat_sheet_pptx.md`.

Contents: [layering](#layering) · [grid](#grid) · [text_box](#text_box) ·
[draft_slot](#draft_slot) · [rich text](#rich-text) ·
[no-fill commentary rail](#no-fill-commentary-rail) · [tables](#tables) ·
[charts](#charts) · [images](#images) · [connectors](#connectors) ·
[visual-refresh vocabulary](#visual-refresh-vocabulary)

---

## layering

OOXML has no z-index — **document order is paint order.** Shapes draw in the
order you concatenate them, so a shape appended *later* sits *on top* of earlier
ones. To place a label, badge, or callout over a filled block (or over a chart /
table frame), append it after the thing it sits on. The template already relies
on this: the breadcrumb is emitted before the Preliminary chip so the chip paints
over the top band; `render()` concatenates `breadcrumb + chip + title + body + sources`.

```python
def _body() -> str:
    panel = text_box(10, "Panel", *BODY, [paragraph([])], fill=BLUE_1, anchor="t")
    tag   = text_box(11, "Tag", BODY_X + 90_000, BODY_Y + 90_000, 1_800_000, 320_000,
                     [paragraph([run("Wedge", size=LABEL_9PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
                     fill=BLUE_5, anchor="ctr")
    return panel + tag   # tag is second -> painted on top of the panel
```

---

## grid

Lay out N equal items across a span with even gaps, instead of hand-typing
coordinates (where misalignment and dead air creep in). `_grid_x` divides a width
into column lefts + a shared item width; `_grid_y` does the same vertically. Both
default to the full `BODY`; pass `start` / `total` to grid a sub-region. (Pure
math — no builder dependency; copy as a local helper.)

```python
GAP = 91_440   # 0.1in; even spacing between gridded items

def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    """N equal columns across `total`. Returns (list-of-x-lefts, shared item_w)."""
    item_w = (total - (n - 1) * gap) // n
    return [start + i * (item_w + gap) for i in range(n)], item_w


def _grid_y(n: int, *, start: int = BODY_Y, total: int = BODY_CY, gap: int = GAP):
    """N equal rows down `total`. Returns (list-of-y-tops, shared item_h)."""
    item_h = (total - (n - 1) * gap) // n
    return [start + i * (item_h + gap) for i in range(n)], item_h
```

```python
# three cards across the full body width
xs, w = _grid_x(3)
cards = "".join(
    text_box(20 + i, f"Card{i}", x, BODY_Y, w, 1_400_000,
             [paragraph([run(label, size=MESSAGE_11PT, color=BLACK, font=FONT)])], fill=BLUE_1, anchor="t")
    for i, (x, label) in enumerate(zip(xs, ["Category A", "Category B", "Category C"]))
)
```

---

## text_box

The workhorse. One sharp rectangle: optional fill, optional border, and a list of
`paragraph()` strings (single line or multi-run / bulleted — see *rich text*).
House rule, **enforced by the builder** (matches `target_copy`: every filled shape
carries a 1pt black border): a *filled* shape gets a 1pt black border (`12_700`)
automatically. Pass `line_width=19_050` (1.5pt) for the one focal / hero / answer /
draft block, an explicit hex only to recolor, or `line_color="none"` to suppress the
border in the rare case you need a borderless fill. An unfilled shape stays
borderless — that is the default for commentary, captions, labels, and chart/table
titles. Text insets are the `insets=` tuple (default `INSETS_DEFAULT`; pass
`INSETS_CARD` for roomier cards). See cheat sheet §11, §13.

```python
# one-liner label (filled -> 1pt black border added automatically)
text_box(10, "Card", *BODY,
         [paragraph([run("Addressable opportunity", size=MESSAGE_11PT, color=BLACK, font=FONT)])],
         fill=BLUE_1, anchor="t")

# dark focal block, white text, 1.5pt border
text_box(11, "Hero", BODY_X, BODY_Y, BODY_CX, 900_000,
         [paragraph([run("~$1.8B per year", size=HERO_32PT, bold=True, color=WHITE, font=FONT)], align="ctr")],
         fill=BLUE_5, line_width=19_050, anchor="ctr")

# transparent label — no fill stays borderless (a plain caption over content)
text_box(12, "Caption", x, y, cx, cy,
         [paragraph([run("aside", size=LABEL_9PT, color=BLACK, font=FONT)])])

# filled support panel — fill gets the default 1pt black border
text_box(13, "Rail", x, y, cx, cy, [paragraph([])], fill=GRAY_1)

# interpretive commentary — no fill, no border (the usual choice for a rail)
text_box(14, "Commentary", x, y, cx, cy,
         [paragraph([run("how to read this exhibit", size=LABEL_9PT, color=BLACK, font=FONT)])],
         fill=None, line_color=None)
```

**Slide-local wrappers** are the right place for a slide-specific motif — name
the intent, compose the primitive, keep it in the module:

```python
def _thesis_band(sp_id: int, y: int, text: str) -> str:
    return text_box(sp_id, "ThesisBand", BODY_X, y, BODY_CX, 520_000,
                    [paragraph([run("Thesis: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                                run(text, size=DENSE_BODY_10PT, color=BLACK, font=FONT)])],
                    fill=GRAY_1, anchor="ctr")   # filled -> default 1pt black border
```

`INSETS_*` presets live in `deck_core.style`: `INSETS_DEFAULT = (91_440, 45_720,
91_440, 45_720)` · `INSETS_CARD` (roomier) · `INSETS_CHIP` (tight). `PAD_X /
PAD_Y / PAD_X_LG / PAD_Y_LG` are the individual values.

---

## draft_slot

A visible "asset goes here" stand-in for an unbuilt chart / table / image, in the
draft visual language (`PRELIM` fill + 1pt black border, italic centered
descriptor). Use it while drafting; replace with the real exhibit later. It is a
plain text box, **not** an OOXML `<p:ph>` placeholder.

```python
def _draft_slot(sp_id: int, x: int, y: int, cx: int, cy: int, label: str) -> str:
    """Draft stand-in for an as-yet-unbuilt asset; PRELIM fill + 1pt border."""
    return text_box(sp_id, "DraftSlot", x, y, cx, cy,
                    [paragraph([run(label, size=BODY_12PT, italic=True, color=BLACK, font=FONT)], align="ctr")],
                    fill=PRELIM, anchor="ctr")   # filled -> default 1pt black border
```

```python
_draft_slot(20, BODY_X, BODY_Y, 5_400_000, 3_000_000, "Chart: metric by scenario")
```

---

## rich text

For multi-run lines (bold label + body) and bullet lists, build runs with `run()`
and paragraphs with `paragraph()`, then hand the list to `text_box(...,
paragraphs)`. `run` size is 1/100 pt and takes point-size tokens (`DENSE_BODY_10PT` = 1000 = 10pt, `BODY_12PT` = 1200 = 12pt); body runs should also pass `font=FONT`. Any attribute left
`None` inherits. `paragraph(bullet=True)` adds a hanging-indent bullet; line and
paragraph spacing are handled for you (they are `<a:pPr>` *children*, never
attributes — a common OOXML trap the builder hides). See cheat sheet §12.

```python
# multi-run line: bold label + body
text_box(30, "UnitCheck", BODY_X, 4_900_000, BODY_CX, 480_000,
         [paragraph([run("UNIT CHECK: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                     run("cumulative value is not annual flow", size=DENSE_BODY_10PT, color=BLACK, font=FONT)])],
         fill=GRAY_1, anchor="ctr")

# bullet list
text_box(31, "Takeaways", BODY_X, BODY_Y, 5_400_000, 2_400_000, anchor="t",
         paragraphs=[
             paragraph([run("Two inputs, one comparison base", size=DENSE_BODY_10PT, color=BLACK, font=FONT)],
                       bullet=True, space_after=600),
             paragraph([run("Embedded activity is not visible in the primary data view", size=DENSE_BODY_10PT, color=BLACK, font=FONT)],
                       bullet=True, space_after=600),
             paragraph([run("Secondary lens recovers the fuller estimate", size=DENSE_BODY_10PT, color=BLACK, font=FONT)],
                       bullet=True),
         ])
```

---

## typography recipes

Point-size tokens make hierarchy visible at the call site. Body runs pass `size=`
and `font=FONT`; only chrome inherits. The full scale is in the `TYPE QUICK REF`
in `slide_base_template.py`.

**Chart / exhibit title** — a no-fill `text_box` above the chart frame, *not* a
native chart title (native titles default to 10pt italic, but an external box
gives better control of spacing, alignment, and hierarchy):

```python
text_box(120, "ChartTitle", x, y, cx, 150_000,
         [paragraph([run("Top categories, cumulative period value, $B",
                         size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
         fill=None, line_color=None, anchor="t", insets=INSETS_NONE)
```

**Connector note** — a quiet italic annotation riding beside a connector in a
tree / flow / system map; no fill, no border:

```python
text_box(121, "ConnectorNote", note_x, note_y, note_w, 120_000,
         [paragraph([run("input funding, not delivery path",
                         size=CONNECTOR_NOTE_8_5PT, italic=True, color=BLACK, font=FONT)],
                    align="ctr")],
         fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
```

**In-shape label prefix + value** — hierarchy *inside* one shape (the move that
makes reference slides read as polished): a small bold prefix, then the value:

```python
text_box(122, "UnitConversionPill", x, y, w, h,
         [paragraph([run("Annualized: ", size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT),
                     run("~$1.25B per year", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
                    align="ctr")],
         fill=BLUE_1, anchor="ctr")
```

---

## no-fill commentary rail

No-fill / no-border interpretation rail for chart notes, legends, and method
commentary — use it when the text explains *how to read* an exhibit rather than
acting as a filled callout, so the chart or axis stays visually dominant. This is
a **recipe**, not a shared primitive: copy it in as a local helper.

```python
def _commentary_rail(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    bullets: list[str | tuple[str, str]],
    *,
    title: str | None = None,
    body_size: int = LABEL_9PT,
) -> str:
    """No-fill / no-border interpretation rail.

    bullets may be either:
      - "flat bullet text"
      - ("Bold lead-in:", "regular explanatory text")
    """
    paras = []

    if title:
        paras.append(
            paragraph(
                [run(title, size=LABEL_9PT, bold=True, italic=True,
                     color=BLACK, font=FONT)],
                space_after=160,
            )
        )

    for i, item in enumerate(bullets):
        space_after = 120 if i < len(bullets) - 1 else 0

        if isinstance(item, tuple):
            lead, body = item
            runs = [
                run(lead + " ", size=DENSE_BODY_10PT, bold=True,
                    color=BLACK, font=FONT),
                run(body, size=body_size, color=BLACK, font=FONT),
            ]
        else:
            runs = [run(item, size=body_size, color=BLACK, font=FONT)]

        paras.append(paragraph(runs, bullet=True, space_after=space_after))

    return text_box(
        sp_id, name, x, y, cx, cy,
        paras,
        fill=None,
        line_color=None,
        anchor="t",
        insets=(137_160, 80_000, 137_160, 80_000),
    )
```

```python
_commentary_rail(
    80, "ChartCommentary",
    BODY_X + 7_800_000, BODY_Y + 400_000, 3_300_000, 1_300_000,
    [
        ("Coverage:", "The observed dataset is partial coverage, not the full scope."),
        ("Mechanic:", "indirect activity can be under-observed."),
        ("Read:", "the title carries the finding; this rail explains the method."),
    ],
    title="How to read this chart",
)
```

---

## tables

Tables are structured evidence, not spreadsheet excerpts: use a native table for
row-column data (exact values, assumptions, scenarios, source comparisons, named
records), and shapes for cards, chips, panels, and commentary.

Native editable table inside a `<p:graphicFrame>` (a graphicFrame uses `<p:xfrm>`,
not `<a:xfrm>`). Two builders, **one cell-inset model** (`45_720`, kept in `tcPr`
only — not duplicated on `bodyPr` — so `text_metrics.estimate_row_heights` agrees
with either):

- **`table()` / `trow()` / `tcell()`** — the low-level engine. Supports
  `gridSpan` / `rowSpan` merges (filler cells are synthesized for you) and
  per-side cell borders, and defaults to the "No Style, No Grid" table style so
  no theme grid lines appear on edit / copy / reset. Reach for it **only** when
  the table has merges or a custom structure `house_table()` doesn't cover.
- **`house_table()`** — the house-standard table and the common case: bold
  header row, cascading bottom borders (1.5pt under the header, 1pt under each
  body row but the last), palette fills, table skins, and per-cell fill / color /
  bold maps. It delegates to the engine above, so the two share one posture and
  one cell-inset model; it is the one place the house table convention lives.
  Import it like any other builder (`from deck_core.primitives import house_table`).

**Which to use:** reach for the low-level `table()` engine **only** for merges,
row/col spans, or an unusual structure `house_table()` doesn't cover. For an
ordinary ledger / matrix / evidence table — the common case — call
`house_table()` and pick a `table_skin` (it defaults to `rule`; `dark` is opt-in
for the one primary table on a page). Do **not** hand-roll dark headers,
`_bottom_border` helpers, or fill maps slide-by-slide.

**Object choice for grids.** Native tables are for row-column data — column
headers, row labels, comparable values across rows or columns. If that is the
content, use `house_table()` (or low-level `table()` for merges), **not** a grid
of `text_box()` shapes. Reserve shape grids for independent cards, chips, badges,
process stages, or panels — objects a reader would not expect to behave as a
PowerPoint table. Code smell: a `_cell()` / `_matrix_cell()` / `_guardrail_cell()`
that returns `text_box()` inside nested row/column loops — if it is tabular, use a
native table; if it is an intentional card grid, name it `_card()` / `_chip()` /
`_panel()`.

**Imported engine — a merged title row** (the engine's reason to exist: `tcell`
takes `grid_span` / `row_span` and the filler cells are synthesized for you). The
low-level `table` / `tcell` / `trow` are opt-in — the template imports only
`house_table`, so add `from deck_core.primitives import table, tcell, trow` for a
merge table. Row heights default to the readability floor (`274_320`); the frame `cy` is the sum of
row heights, and a wrapping row must be sized up with `estimate_row_heights`:

```python
table(40, "Coverage", BODY_X, BODY_Y, 11_282_362, 822_960,   # cy = 3 * 274_320
      col_widths=[5_641_181, 2_820_590, 2_820_591],
      rows=[
          trow([tcell("Coverage by segment", bold=True, grid_span=3, align="ctr")]),
          trow([tcell("Segment", bold=True), tcell("Group A", bold=True), tcell("Group B", bold=True)]),
          trow([tcell("Segment A"), tcell("$1.2B", align="r"), tcell("$0.6B", align="r")]),
      ])
```

**Sizing — read this, it is the #1 table failure.** There is no autofit, and
`<a:tr h>` is only a **minimum** row height: any cell whose text wraps makes that
row grow taller at render time. So a single scalar height gives ragged rows and
the frame `cy` understates the real table — which you can't catch, because you
don't render. **Don't guess.** Size `col_w` to sum to your region (≈`BODY_CX`),
then compute per-row heights from the content and pass the list:

```python
from deck_core.text_metrics import estimate_row_heights
ROW_H = estimate_row_heights(ROWS, COL_W, size_pt=9.5)   # size_pt == cell size / 100
```

Each row is then sized to its tallest cell and the frame `cy` matches the render.
`slide_probe --table-fit <module>` reports the same estimate (authored vs required
row heights and the estimated bottom against `BODY_B`) as informational facts. Keep
cells short / widen columns so nothing wraps and every estimated row lands on the
same floor height for a uniform look.

**`house_table()` — the house-standard table** (imported; the old copy-paste
table recipe was promoted into `deck_core.primitives`, so it is now an import,
not a paste). Base table style `{2D5ABB26-...}` = "No Style, No Grid" so the
explicit per-cell borders are what show. Alignment defaults to **first column
left, the rest centered**; pass `aligns` to override. See cheat sheet §15.

```python
house_table(sp_id, name, x, y, col_w, rows, *,
            row_h=274_320, table_skin="rule",
            header_fill=None, header_color=None,
            body_fill=None, body_color=BLACK,
            aligns=None, anchor="ctr", size=950,           # 950 = 9.5pt
            cell_fills=None, cell_text_colors=None, cell_bold=None)
```

`rows[0]` is the header row; `col_w` is the per-column EMU width (sum = table
width). `table_skin` picks the header treatment in one move — `rule` (default; no
header fill, the 1.5pt header bottom-rule carries it — chart-side evidence /
backup), `dark` (`BLUE_5` + white, the ONE primary table on a page), or `light`
(`GRAY_1` header, dense matrices); an unknown skin raises `ValueError`.
`header_fill` / `header_color` override the skin (pass both). `cell_fills` /
`cell_text_colors` / `cell_bold` take `{(row, col): value}` overrides.
`house_table()` delegates to `table()`, so the cascading bottom borders (1.5pt
under the header, 1pt under each body row but the last), the no-grid style, the
explicit no-fill side borders, and the `45_720` `tcPr` inset are all handled for
you. Size content-fit rows with `estimate_row_heights` and pass the list (see
*Sizing* above) so the frame `cy` matches the render.

```python
from deck_core.text_metrics import estimate_row_heights
_COL_W = [5_641_181, 5_641_181]
_ROWS = [
    ["Category", "Value"],
    ["Category A", "$2,192M"],
    ["Category B", "$1,247M"],
    ["Total", "$3,439M"],
]
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=9.5)   # per-row, content-fit
house_table(40, "ValueTable", BODY_X, BODY_Y, _COL_W, _ROWS, row_h=_ROW_H)
```

---

## charts

Native, editable PowerPoint charts. The factory in `deck_core/charts.py` returns
`{chart_xml, embed_xlsx, chart_rels}`. The slide does just three things:

1. build the chart object,
2. expose it at module scope as `CHARTS = [_CHART]` (lib.py reads this at build),
3. place a `graphic_frame(...)` in `_body()` at `rId2` (first chart on the slide).

**You never touch the embedded workbook.** At build, lib.py writes `embed_xlsx`
into `ppt/embeddings/Microsoft_Excel_WorksheetN.xlsx`, writes the chart part +
its rels, adds the slide→chart relationship, and updates `[Content_Types].xml`.
That xlsx is what makes PowerPoint's "Edit Data" work. Import only what the slide uses:

**Think-cell look (white segment dividers, dark-navy axis, 8pt labels, no native
legend/gridlines):** spread `THINKCELL_BARS` (from `deck_core.charts`) into
`column_chart`/`bar_chart`, color series via `chart_accent_seq(n)`
(`deck_core.style`), and replace the dropped legend with `chart_key(...)`
(`deck_core.chart_key`).

```python
from deck_core.charts import (
    column_chart, bar_chart, line_chart, waterfall_chart, marimekko_chart, graphic_frame,
)
```

### Chart family

- **column_chart** / **bar_chart** — the workhorses. `mode="clustered"` (side by
  side; also a single or ranked series), `"stacked"` (bars sum to their raw
  total), `"percent"` (stack to 100%), `"ranked"` (alias of clustered for one
  pre-sorted series). column = vertical; bar = horizontal (reads top-to-bottom).
- **line_chart** — one line per series, for trends.
- **waterfall_chart** — running-total bridge (native stacked-column workaround).
- **marimekko_chart** — variable-width percent-stacked columns (native; returns
  an extra `label_meta` for overlaid labels).

See cheat sheet §20-23; full arg list in `charts.py` docstrings.

### Chart title convention (house standard — keep it consistent)

Always pass `title=None` to the factory and render the title as a separate
no-fill box above the frame, so every chart shares one 10pt Arial italic
left-aligned title and a clean plot area. Use this local helper:

```python
def _chart_title(text: str, x: int, y: int, cx: int, *, sp_id: int = 60) -> str:
    """House chart/exhibit title: 10pt Arial italic, no fill, no border.

    Prefer this external title box over native chart titles because it gives
    better control of spacing, alignment, and hierarchy. Standard height
    150_000 EMU; place the frame at y + 220_000.
    """
    return text_box(
        sp_id, "ChartTitle", x, y, cx, 150_000,
        [paragraph([
            run(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)
        ], align="l")],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
```

### Recipes

**A — period columns** (`column_chart`, 2 series, $B axis + labels):

```python
_CHART = column_chart(
    mode="clustered",                  # or "stacked" (raw totals) / "percent" (to 100%)
    categories=["P1", "P2", "P3", "P4", "P5", "P6"],
    series=[
        {"name": "Series A", "values": [a1, a2, a3, a4, a5, a6], "color": BLUE_4},
        {"name": "Series B", "values": [b1, b2, b3, b4, b5, b6], "color": BLUE_2},
    ],
    title=None,                        # title via _chart_title above the frame
    show_legend=True, legend_pos="b",
    value_axis_format='"$"0.0"B"',
    show_gridlines=True, major_gridline_color=GRAY_1, major_gridline_width=3_175,  # 0.25pt
    show_value_labels=True, value_label_format='"$"0.0"B"',
    value_label_size_pt=8, cat_label_size_pt=10,
    gap_width=120, cat_header="Period",
)
CHARTS: list[dict] = [_CHART]
```

**B — ranked bars** (`bar_chart`, single series; top-1 / top-5 / rest tints).
bar_chart reads top-to-bottom, so just sort descending:

```python
names  = [...]   # rank 1 .. N, sorted desc
values = [...]
colors = [BLUE_5] + [BLUE_4] * 4 + [BLUE_2] * (len(names) - 5)
_CHART = bar_chart(
    mode="ranked",
    categories=names,
    series=[{"name": "Cumulative value $M", "values": values, "data_point_colors": colors}],
    title=None, show_legend=False,
    value_axis_format='"$"#,##0"M"',
    show_gridlines=True, major_gridline_color=GRAY_1, major_gridline_width=3_175,
    show_value_labels=True, value_label_format='"$"#,##0"M"',
    value_label_size_pt=9, cat_label_size_pt=9,
    gap_width=50, cat_header="Category",
)
CHARTS: list[dict] = [_CHART]
```

**C — line trend** (`line_chart`):

```python
_CHART = line_chart(
    categories=["P1", "P2", "P3", "P4", "P5", "P6"],
    series=[{"name": "Metric", "values": [m1, m2, m3, m4, m5, m6], "color": BLUE_4}],
    title=None, show_legend=False, value_axis_format="#,##0",
)
CHARTS: list[dict] = [_CHART]
```

**D — waterfall** (running-total bridge). Steps are `start` / `delta` /
`subtotal` / `end`; `value=None` on a start/subtotal/end uses the running total:

```python
_CHART = waterfall_chart(
    steps=[
        {"label": "Starting value", "value": 900,  "kind": "start"},
        {"label": "Driver A",       "value": 120,  "kind": "delta"},
        {"label": "Driver B",       "value": 80,   "kind": "delta"},
        {"label": "Driver C",       "value": -45,  "kind": "delta"},
        {"label": "Ending value",   "value": None, "kind": "end"},
    ],
    value_axis_format='"$"#,##0"M"',
)
CHARTS: list[dict] = [_CHART]
```

**E — marimekko** (variable-width percent-stacked columns). Returns
`(chart, label_meta)` — the chart goes in `CHARTS`; `label_meta` drives overlaid
column labels (the axis is blanked, since it can't label variable widths):

```python
_CHART, _MEKKO = marimekko_chart(
    columns=["Segment A", "Segment B", "Segment C"],
    segments=["Group A", "Group B", "Other"],
    values={
        "Segment A": {"Group A": 30, "Group B": 45, "Other": 25},
        "Segment B": {"Group A": 45, "Group B": 35, "Other": 20},
        "Segment C": {"Group A": 20, "Group B": 30, "Other": 50},
    },
    column_widths={"Segment A": 52, "Segment B": 28, "Segment C": 20},
    colors={"Group A": BLUE_5, "Group B": BLUE_4, "Other": GRAY_1},
)
CHARTS: list[dict] = [_CHART]


def _mekko_labels(label_meta, *, chart_x: int, chart_w: int, y: int,
                  h: int = 200_000, base_id: int = 9000) -> str:
    """Overlay one centered label per mekko column, from label_meta."""
    parts = []
    for i, m in enumerate(label_meta):
        x0 = chart_x + int(chart_w * m["x0_frac"])
        cx = int(chart_w * (m["x1_frac"] - m["x0_frac"]))
        if cx < 300_000:            # skip columns too narrow to label
            continue
        parts.append(text_box(base_id + i, f"MekkoLabel{i}", x0, y, cx, h,
                              [paragraph([run(f'{m["label"]}  {m["width_share"]:.0%}',
                                              size=SOURCES_8PT, bold=True, color=BLACK, font=FONT)], align="ctr")],
                              anchor="ctr"))
    return "".join(parts)
```

**E2 — per-column-sorted marimekko (POSITIONAL series).** `marimekko_chart` emits
one series per segment, which forces ONE global bottom→top order for every column.
If your source **size-sorts each column independently** (think-cell's default —
largest segment at the bottom, so different columns have different orders), that
by-segment stack can't reproduce it. Build **positional** series instead: one
series per stack *layer* (Layer 1 = bottom band, Layer 2 = 2nd, …) and color each
bin individually with `data_point_colors`. Layer 1 is at the bottom of every column
but carries each column's own bottom segment + accent, so every column keeps its
source order while staying native + editable. Bypass `marimekko_chart` and call
`column_chart(mode="percent", …)` with your own binning:

```python
_TOTAL_BINS = 200
# per column, BOTTOM->TOP in the source's own order: (accent_hex, value)
_STACKS = {"Surface Combatants": [(A1, 2871788), (A3, 192088), ...],
           "Submarines":         [(A2, 2149475), (A4, 762000), ...],  # different order!
           ...}
_WIDTHS = {col: emu, ...}                       # ∝ the wide-axis measure
_BINS = _alloc_bins([_WIDTHS[c] for c in _COLS], _TOTAL_BINS)   # largest-remainder, local helper
_NPOS = max(len(s) for s in _STACKS.values())
vals = [[] for _ in range(_NPOS)]; cols = [[] for _ in range(_NPOS)]
for col, nb in zip(_COLS, _BINS):
    stack = _STACKS[col]
    for _ in range(nb):
        for k in range(_NPOS):
            v, c = (stack[k][1], stack[k][0]) if k < len(stack) else (0, "FFFFFF")
            vals[k].append(v); cols[k].append(c)
_CHART = column_chart(
    mode="percent", categories=[""] * _TOTAL_BINS,
    series=[{"name": f"Layer {k+1}", "values": vals[k], "data_point_colors": cols[k]}
            for k in range(_NPOS)],
    value_axis_format="0%", value_axis_min=0, value_axis_max=1, value_axis_major_unit=0.05,
    seg_line_color=None, axis_line_color="162029", show_gridlines=False,
    show_legend=False, show_value_labels=False, show_cat_labels=False,
    gap_width=0, plot_layout=_PL,
)
CHARTS: list[dict] = [_CHART]
```

Then overlay white dividers (vertical at the bin boundaries `cum/_TOTAL_BINS`,
horizontal at each column's cumulative source heights) exactly like recipe E /
`fleet_mro.py`. The bottom band being uniform-color across columns means it merges
seamlessly — the vertical dividers are what mark the column edges. Live example:
MRO slide 7 (`projects/mro/deck/deck_mro/slides/tam_composition.py`), a 6×6 mekko;
slide 13 (`fleet_mro.py`) is the simpler by-segment case where one global order
*does* match. Cost: `_NPOS × _TOTAL_BINS` `<c:dPt>` overrides (≈1200 — fine).

**F — thin-segment label chip** (stacked column/bar where one segment is too thin
to hold its native in-bar label). This reproduces think-cell's "outside chip"
treatment: bump the label just outside the bar onto a small rectangle filled with
the *segment's own* accent color (so it stays legible and reads as belonging to
that segment). Two moves: suppress that one series' native label with
`hide_labels: True`, then overlay the chip yourself. Pass `line_color="none"` on
the chip — a filled `text_box` gets a 1pt black house border by default — and use
`bold=True` so it matches the engine's bold value labels (the other in-bar numbers).
Often the suppressed native label's centroid is right where the chip belongs, so
the source label's transcribed x/y double as the chip position.

```python
_SEG = [  # bottom->top; the last (thinnest) segment can't hold an in-bar label
    ("Public NSY", CHART_ACCENT_1, 44, False),
    # ... middle segments ...
    ("USCG ISVS",  CHART_ACCENT_6,  1, True),   # 1% sliver -> chip it
]
_CHART = column_chart(
    mode="stacked",
    categories=["Total"],
    series=[{"name": n, "values": [p], "color": c,
             **({"hide_labels": True} if chip else {})}   # drop only the thin one's label
            for (n, c, p, chip) in _SEG],
    # ... usual think-cell params (dividers, axis, 5% ticks, plot_layout) ...
)
CHARTS: list[dict] = [_CHART]

# overlay the chip where the suppressed label belonged (here, just above the bar top):
chip = text_box(
    104, "OnePctChip", 2_513_013, 1_697_038, 176_213, 122_238,
    [paragraph([run("1%", size=SOURCES_8PT, bold=True, color=BLACK, font=FONT)], align="ctr")],
    fill=CHART_ACCENT_6,     # the segment's own accent ties the chip to its bar
    line_color="none",       # beat the house auto-border on a filled shape
    anchor="ctr", insets=INSETS_NONE,
)
```

Live example: MRO slide 8 (`projects/mro/deck/deck_mro/slides/topdown_detail.py`) —
the 1% USCG ISVS sliver. The source carries the chip as a `solidFill accent6` on the
label shape (the segments that fit are `noFill`), so check the source XML's label
fills to see which segments need this.

### Placement

Title box + frame, with the chart at `rId2` (first chart on the slide; `rId1` is
the layout):

```python
def _body() -> str:
    title = _chart_title("Metric by category, P1 to P6", BODY_X, BODY_Y, BODY_CX)
    frame = graphic_frame(sp_id=51, name="MetricChart",
                          x=BODY_X, y=BODY_Y + 220_000, cx=BODY_CX, cy=3_900_000, rId="rId2")
    return title + frame
```

Two charts on one slide → second is `rId3`, and `CHARTS = [_CHART_A, _CHART_B]`
(rId N+1 maps to CHARTS[N-1]).

---

## images

Images (photos and brand logos) **are** wired by the build. Drop the file into
`infra/assets/media/` (brand chrome) or the deck's `images/` dir — `build_pptx`
copies the bytes into `ppt/media/`. Then declare the file in a module-level
`IMAGES` list and draw it with `picture()`:

```python
from deck_core.primitives import slide, picture   # plus the usual chrome imports

IMAGES = [{"rId": "rId2", "file": "logo_saronic.png"}]   # rId2: this slide has no charts

def _body() -> str:
    return picture(20, "BrandLogo", "rId2", BODY_R - 1_300_000, BODY_Y, 1_200_000, 340_000)
```

`build_pptx` wires the per-slide image relationship automatically (content-types
for png / jpg / jpeg / svg / emf are already declared). **The `rId` in `IMAGES`
and the `r_embed` passed to `picture()` must match.** Image rIds **continue after
chart rIds**: with no charts the first image is `rId2`; with one chart (which takes
`rId2`) the first image is `rId3`; and so on. A declared image whose file is
missing from `ppt/media/`, or an rId that collides with the layout / a chart /
another image, **fails the build with a clear error** — no silent "repair" on open.

If the asset isn't ready yet, a `_draft_slot(...)` placeholder still works as a
stand-in. See cheat sheet §14 for the raw `<p:pic>` mechanics.

---

## connectors

A straight / elbow line between points is a `<p:cxnSp>`. The imported
`connector()` **normalizes signed vectors for you**: a left/up vector (negative
`cx`/`cy`) is converted to a positive `<a:ext>` plus `flipH`/`flipV` with the
offset shifted, so you can pass any signed `cx`/`cy` without tripping a PowerPoint
"repair" on open. `arrow=True` adds a tail arrowhead; `width` is EMU (12700 = 1pt);
`color="none"` makes an invisible line; `prst` selects `line` (default) /
`straightConnector1` / `bentConnector3` / `curvedConnector3`. (To *attach* endpoints
to shapes via `<a:stCxn>` / `<a:endCxn>`, drop to raw OOXML — see cheat sheet §16.)

```python
# free-floating arrow, left to right
connector(60, "Flow", BODY_X, 3_000_000, 2_400_000, 0, arrow=True)

# up-and-left vector — pass it signed; the builder flips + normalizes
connector(61, "Back", BODY_X + 2_400_000, 3_000_000, -2_400_000, -600_000, arrow=True)
```

**Hierarchy + min-arrow guardrail (style guidance).** Pick a weight by role, and
never draw an arrowhead on a connector too short to read (~<0.27in) — widen the
gap, or use a `_chevron`. Define the weights as module constants:

```python
CONNECTOR_HAIRLINE = 9_525      # 0.75pt — secondary guides only
CONNECTOR_NORMAL   = 15_875     # 1.25pt — process arrows
CONNECTOR_STRONG   = 19_050     # 1.5pt  — primary flow
MIN_ARROW_LEN      = 250_000    # ~0.27in — below this, no arrowhead

# e.g. drop the arrowhead automatically on a too-short connector:
arrow = (abs(cx) + abs(cy)) >= MIN_ARROW_LEN
connector(62, "Step", x, y, cx, cy, color=GRAY_4, width=CONNECTOR_NORMAL, arrow=arrow)
```

---

## visual-refresh vocabulary

A second layer of conventions on top of the builders above, to give a deck
**visual hierarchy** instead of one "safe" default everywhere: fewer dark table
headers, disciplined borders, flow that reads, and one line of interpretation per
slide. These are **local-helper recipes** — copy and adapt; they are not promoted
to core. The non-rect ones (`_classification_tag`, `_chevron`, `_step_dot`) are
the **controlled exceptions** to sharp-rect — keep them to tags / dots / flow
transitions, never panels or cards.

### Table skins

`house_table()` takes a `table_skin` argument that sets the header treatment in
one move, so a slide picks an *intent* rather than restating colors. **The
default is `"rule"`** — the dark `BLUE_5` header is opt-in
(`table_skin="dark"`) and reserved for the one primary table on a page. Pass
`header_fill` / `header_color` only to override the skin (pass both, since an
unfilled header needs dark text).

- **rule** (default) — no header fill; the 1.5pt black bottom-rule under the
  header carries it. The right skin for **chart-side legends / evidence / backup
  tables** so they stop reading like separate mini-slides. An unfilled header
  keeps **black** text.
- **dark** — `BLUE_5` header, white text. Reserve for the one primary / answer
  table on a page (use sparingly).
- **light** — `GRAY_1` header; for dense matrices / crosswalks where a dark band
  would dominate.

### Border discipline — one heavy family per slide

Every filled shape carries a 1pt black border (`target_copy`), but don't let the
heavy weight repeat 16 ways. Reserve the **1.5pt** black border for **one object
family per slide** — the hero / answer / output block, draft elements, high-risk
caveats. Everything secondary stays at the default **1pt** black border (filled
support panels) or, better for interpretation, goes **no-fill / no-border**
(commentary rails, captions, labels). A no-fill shape usually carries no border at
all; reach for a thin rule only as a caption / axis / container.

### `_classification_tag` — rounded tag (roundRect, raw OOXML)

A small pill for an exclusion / confidence / classification **tag** (not a panel).
`prstGeom="roundRect"` with a high `adj` reads as a pill — `text_box` can't set the
corner radius, so this is a good place to drop to raw OOXML. This is the one place
sharp rectangles relax; keep it to tags.

```python
def _classification_tag(sp_id, name, x, y, cx, cy, text, *, fill=BLUE_1, color=BLACK,
                        line=BLACK, line_w=12_700, size=850, bold=True, adj=42_000) -> str:
    fill_xml = (f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>')
    line_xml = (f'<a:ln w="{line_w}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
                if line else '<a:ln><a:noFill/></a:ln>')
    b = ' b="1"' if bold else ""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{_esc(name)}"/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst></a:prstGeom>'
            f'{fill_xml}{line_xml}</p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" anchor="ctr" lIns="45720" tIns="9144" '
            f'rIns="45720" bIns="9144"/><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:r>'
            f'<a:rPr lang="en-US" sz="{size}"{b} kern="1200" dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/>'
            f'</a:rPr><a:t>{_esc(text)}</a:t></a:r></a:p></p:txBody></p:sp>')
```

### `_chevron` — flow transition with weight (chevron, raw OOXML)

A right-pointing block arrow between stages — replaces a stubby connector.
`prstGeom="chevron"`. **Caveat:** a chevron's *inscribed* text box is much narrower
than its bounding box (the arrow point + notch are excluded), so even a short word
wraps one character per line. Keep `text` to ~3 characters, or leave it blank and
name the transition with a nearby tag / caption / the table.

```python
def _chevron(sp_id, name, x, y, cx, cy, *, text="", fill=BLUE_3, color=WHITE,
             size=900, bold=True, line=BLACK, line_w=12_700) -> str:
    b = ' b="1"' if bold else ""
    body = ((f'<a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="{size}"{b} kern="1200" dirty="0">'
             f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
             f'<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/>'
             f'</a:rPr><a:t>{_esc(text)}</a:t></a:r></a:p>') if text else '<a:p/>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{_esc(name)}"/>'
            f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="chevron"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
            f'<a:ln w="{line_w}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" anchor="ctr" lIns="68580" tIns="9144" '
            f'rIns="114300" bIns="9144"/><a:lstStyle/>{body}</p:txBody></p:sp>')
```

### `_step_dot` — numbered circle on a shared rail (ellipse, raw OOXML)

For a process / method rail: numbered circles on one thin line with labels
beneath — instead of full boxes joined by tiny arrows. Draw one long `connector`
rail first (behind), then the dots on top (paint order). `active=True` for the
emphasized step.

```python
def _step_dot(base_id, x, y, d, n, label, *, active=False, label_w=None,
              label_h=560_000, label_size=FINEPRINT_8_5PT) -> str:
    fill = BLUE_5 if active else BLUE_1
    cnum = WHITE if active else BLACK
    circle = (f'<p:sp><p:nvSpPr><p:cNvPr id="{base_id}" name="StepDot{n}"/>'
              f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
              f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{d}" cy="{d}"/></a:xfrm>'
              f'<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>'
              f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
              f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{BLACK}"/></a:solidFill></a:ln></p:spPr>'
              f'<p:txBody><a:bodyPr wrap="square" anchor="ctr" lIns="0" tIns="0" rIns="0" bIns="0"/>'
              f'<a:lstStyle/><a:p><a:pPr algn="ctr"/><a:r>'
              f'<a:rPr lang="en-US" sz="1100" b="1" kern="1200" dirty="0">'
              f'<a:solidFill><a:srgbClr val="{cnum}"/></a:solidFill>'
              f'<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/>'
              f'</a:rPr><a:t>{n}</a:t></a:r></a:p></p:txBody></p:sp>')
    lwid = label_w if label_w else d + 600_000
    lx = x + d // 2 - lwid // 2
    label_box = text_box(base_id + 1, f"StepLbl{n}", lx, y + d + 40_000, lwid, label_h,
                         [paragraph([run(label, size=label_size, color=BLACK, font=FONT)], align="ctr")],
                         anchor="t")
    return circle + label_box
```

### `_callout` — the focal "so what" (at most one per slide)

Not a new shape — a *discipline*. When a slide needs a filled focal callout, use at
most one short interpretive line (≤35 words): a bold lead-in plus the point, in a
filled box with the default 1pt black border. Reach for it only after title
findings, direct labels, and a no-fill commentary rail — no-fill commentary doesn't
count against this.

```python
def _callout(sp_id, x, y, cx, cy, text, *, lead="So what:", fill=BLUE_1, color=BLACK,
             size=DENSE_BODY_10PT, anchor="ctr") -> str:
    return text_box(sp_id, "Callout", x, y, cx, cy,
                    [paragraph([run(f"{lead} ", size=size, bold=True, color=color, font=FONT),
                                run(text, size=size, color=color, font=FONT)])],
                    fill=fill, anchor=anchor)   # filled -> default 1pt black border
```

### `_badge` — large emphasis block

A single big number / identity called out beside an exhibit (a coefficient, a
one-line formula). A `text_box` with a strong fill, big bold text, and a 1.5pt
black border — the once-per-slide focal object (the black-outlined family).

```python
def _badge(sp_id, x, y, cx, cy, value, label="", *, fill=BLUE_5, color=WHITE,
           value_size=ANSWER_KPI_24PT, label_size=LABEL_9PT) -> str:
    paras = [paragraph([run(value, size=value_size, bold=True, color=color, font=FONT)], align="ctr")]
    if label:
        paras.append(paragraph([run(label, size=label_size, color=color, font=FONT)], align="ctr"))
    return text_box(sp_id, "Badge", x, y, cx, cy, paras,
                    fill=fill, line_width=19_050, anchor="ctr")
```

### chart annotation overlays — native labels vs manual overlays

Two different things, kept separate:

- **Native chart data labels** (`c:dLbls` / `c:dLbl` in `charts.py`, via
  `show_value_labels` / `label_color` / `label_colors`) are bound to the chart
  data — they move and update with the series. Use these first when the value can
  live cleanly inside or beside the chart.
- **Manual overlays** (below) are ordinary `<p:sp>` shapes placed *on top of* the
  chart frame in the slide shape tree — deterministic, hand-placed, not bound to
  chart data. Use one when a specific bar / column / point needs emphasis or a
  pointer the native labels can't place. Paint order is document order (see
  *layering*), so append the overlay **after** the `graphic_frame`. These are
  slide annotations, not `c:dLbl` labels — name them `ChartValueBadge …` /
  `PointerCallout …` so the probe can classify them, and don't call them
  `DataLabel`.

Both are local-helper recipes (encouraged, not enforced); the probe simply reports
their geometry like any other shape.

### `_chart_value_badge` — oval value bubble over a chart element (ellipse)

A white / `BLUE_1` oval calling out one value on a specific bar or point. Works
through the existing `text_box(prst="ellipse")` — no new mechanics; the filled oval
carries the default 1pt black border.

```python
def _chart_value_badge(sp_id, name, x, y, cx, cy, text, *, fill="FFFFFF",
                       line=BLACK, color=BLACK, size=VALUE_14PT, bold=True) -> str:
    """Manual oval value badge over/near a chart element — a slide annotation,
    not a native c:dLbl. Name it ChartValueBadge* so it reads clearly in the probe."""
    return text_box(sp_id, f"ChartValueBadge {name}", x, y, cx, cy,
                    [paragraph([run(text, size=size, bold=bold, color=color, font=FONT)],
                               align="ctr")],
                    prst="ellipse", tx_box=False, fill=fill, line_color=line,
                    line_width=12_700, anchor="ctr", insets=INSETS_BADGE)
```

### `_pointer_callout` — rectangular callout with a wedge pointer (wedgeRectCallout)

A short focal annotation that points at a chart element. Uses the generic
`geom_adj` handle on `text_box` to aim the wedge tail. `tip_x` / `tip_y` are
absolute slide EMU for the pointer tip; the adj values are signed offsets from
the box centre, in 1/100,000 of the box width / height.

This is a **chart-annotation overlay**, not the page's editorial callout — it does
**not** count against the one-filled-focal-callout budget (`slide_guide.md` →
Callout restraint). Still use it sparingly, and only when it truly points at
something.

```python
def _pointer_callout(sp_id, name, x, y, cx, cy, text, *, tip_x, tip_y,
                     fill=BLUE_1, line=BLACK, color=BLACK, size=DENSE_BODY_10PT,
                     lead=None) -> str:
    """Rectangular wedge callout with a built-in pointer. Name it PointerCallout*
    so it reads clearly in the probe."""
    adj1 = round(((tip_x - (x + cx / 2)) / cx) * 100_000)
    adj2 = round(((tip_y - (y + cy / 2)) / cy) * 100_000)
    runs = []
    if lead:
        runs.append(run(f"{lead} ", size=size, bold=True, color=color, font=FONT))
    runs.append(run(text, size=size, color=color, font=FONT))
    return text_box(sp_id, f"PointerCallout {name}", x, y, cx, cy,
                    [paragraph(runs)],
                    prst="wedgeRectCallout", geom_adj={"adj1": adj1, "adj2": adj2},
                    tx_box=False, fill=fill, line_color=line, line_width=12_700,
                    anchor="ctr", insets=INSETS_MESSAGE)
```

Both sit on top of the chart by paint order (`graphic_frame` is keyword-only):

```python
def _body() -> str:
    chart = graphic_frame(sp_id=50, name="MetricChart", x=BODY_X,
                          y=BODY_Y + 220_000, cx=BODY_CX, cy=3_800_000, rId="rId2")
    badge = _chart_value_badge(80, "SeriesA Pt3",
                               BODY_X + 5_100_000, BODY_Y + 1_420_000,
                               640_000, 340_000, "$42M")
    callout = _pointer_callout(81, "Outlier",
                               BODY_X + 7_250_000, BODY_Y + 420_000,
                               2_600_000, 620_000,
                               "one category drives most of the variance",
                               lead="Read:",
                               tip_x=BODY_X + 6_520_000, tip_y=BODY_Y + 1_820_000)
    return chart + badge + callout   # overlays appended last -> painted on top
```
