# doc_core — snippets

Copy-from recipes. Each page module stays self-contained: import the builders it
needs from `docx_core.*` and return a `PageModuleSpec` from `render()`.

## 1. Module skeleton (page module)

```python
from docx_core.primitives import heading, paragraph, run, bullets
from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PAGE_PORTRAIT
from docx_core.style_ids import R_STRONG, P_SOURCE

PAGE_TITLE = "Market scope"

def render() -> PageModuleSpec:
    body = [
        heading(1, "Reachable market is narrower than total visible spend"),
        paragraph([run("Finding: ", style=R_STRONG),
                   run("three gating constraints limit near-term capture.")]),
        *bullets([
            "Primary records cover only directly visible activity.",
            "Indirect activity is recovered through a secondary lens.",
        ]),
        paragraph("Sources: FPDS extracts; budget exhibits", style=P_SOURCE),
    ]
    return PageModuleSpec(body=body, page_setup=PAGE_PORTRAIT, title=PAGE_TITLE)
```

## 2. Rich paragraph (mixed runs)

```python
from docx_core.primitives import paragraph, run
from docx_core.style_ids import R_STRONG, R_EMPH

paragraph([
    run("Addressable base: ", style=R_STRONG),
    run("$1.8B "),
    run("(FY2026 run-rate)", style=R_EMPH),
])
```

## 3. Rule table with caption + source

```python
from docx_core.primitives import table_block, paragraph
from docx_core.style_ids import P_SOURCE

blocks = [
    *table_block(
        ["Lens", "Coverage", "Use in model"],
        [["Primary", "Directly observed", "Lower bound"],
         ["Secondary", "Qualified proxy", "Sensitivity range"]],
        caption_text="Table 1. Evidence bridge by source lens",
    ),
    paragraph("Sources: primary records; secondary program documents", style=P_SOURCE),
]
```

Use `dark_header=True` for the one primary table; pass `col_widths_twips=[...]`
(twips; 1 in = 1440) to fix column widths.

## 4. Lists

```python
from docx_core.primitives import bullets, numbered, outline_item

*bullets(["First point.", "Second point."]),
*numbered(["First step.", "Second step."]),
outline_item("Market", level=0),
outline_item("Defense", level=1),
```

## 5. Landscape page module (wide table / diagram)

```python
from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PAGE_LANDSCAPE

def render() -> PageModuleSpec:
    return PageModuleSpec(title="Wide table", page_setup=PAGE_LANDSCAPE, body=[
        # ...wide table or canvas...
    ])
```

## 6. Structured blocks (registers, forms, definitions)

```python
from docx_core.primitives import heading
from docx_core.specs import PageModuleSpec
from docx_core.structured_blocks import (
    card_block, field_block, checklist_block, definition_list,
)

def render() -> PageModuleSpec:
    body = [
        heading(1, "Build register"),
        *card_block("Ingest",
                    ["Pulls the source extracts nightly.", "Owner: data team."]),
        *field_block("Purpose",
                     "Allocate portfolio TAM across work-type buckets."),
        *checklist_block(
            ["Bucket TAM total == portfolio TAM by construction.",
             "No placeholder cells remain."],
            label="Checks"),
        *definition_list([
            ("TAM", "total addressable supplier opportunity"),
            ("SAM", "scenario subset of TAM, no capture haircut")]),
    ]
    return PageModuleSpec(body=body, title="Build register")
```

## 7. Wireframes

```python
from docx_core.wireframes import (
    ascii_block, wire_table, wire_cell, canvas, CanvasBox, CanvasLine,
)
from docx_core.style import BLUE_1, BLUE_2

# Layer A - ASCII (fastest logic sketch)
ascii_block(
    "+----------------+        +----------------+\n"
    "| Source system  | -----> | Normalization  |\n"
    "+----------------+        +----------------+"
)

# Layer B - table-grid (stable, editable boxes/lanes)
wire_table(
    [
        [wire_cell("Input", fill=BLUE_1), wire_cell("Transform", fill=BLUE_1),
         wire_cell("Output", fill=BLUE_1)],
        [wire_cell("CSV / API"), wire_cell("Rules + QA"), wire_cell("Workbook + deck")],
    ],
    col_widths_twips=[3000, 3000, 3000],
)

# Layer C - DrawingML canvas (free-positioned boxes + arrows; inches map 1:1)
canvas([
    CanvasBox(0.0, 0.0, 2.0, 0.8, text="Ingest", fill=BLUE_1),
    CanvasBox(3.0, 0.0, 2.0, 0.8, text="Transform", fill=BLUE_2),
    CanvasLine(2.0, 0.4, 1.0, 0.0, arrow=True),   # arrow Ingest -> Transform
], w_in=5.0, h_in=0.8)
```

Reach for ASCII first, table-grid for stable diagrams, and DrawingML `canvas`
only when the page needs polished free positioning.

## 8. Slide mock (wireframing a pptx slide)

A page that reproduces a real 16:9 slide (13.333 × 7.5 in) with all its planned
copy, then annotates the layout and objects below it on the same page.

```python
from docx_core.specs import PageModuleSpec
from docx_core.page_setup import PAGE_SLIDE_16x9_TALL
from docx_core.wireframes import slide_canvas, slide_frame, CanvasBox
from docx_core.style import BLUE_1, BLUE_5, WHITE

PAGE_TITLE = "Worktype mix - slide mock"

def render() -> PageModuleSpec:
    # The slide region: 16:9, drawn at the page's usable width (inches map 1:1).
    slide = slide_canvas([
        CanvasBox(0.0, 0.0, 12.5, 0.9,
                  text="Worktype mix | Outsourced scope concentrates in three lanes.",
                  fill=BLUE_5, text_color=WHITE, align="left", text_size_pt=13),
        CanvasBox(0.0, 1.1, 7.6, 5.7, text="[ stacked column: worktype $ by yard ]"),
        CanvasBox(7.8, 1.1, 4.7, 5.7, fill=BLUE_1, align="left",
                  text="Three lanes hold ~70% of outsourced $.\n"
                       "- piping and structural lead\n"
                       "- coatings rises post-FY26"),
    ], ratio="16:9", w_in=12.5)

    return PageModuleSpec(
        page_setup=PAGE_SLIDE_16x9_TALL, title=PAGE_TITLE,
        body=slide_frame(
            slide,
            layout=[
                "Title band across the top (dark fill, white text).",
                "Body split Pattern A: exhibit left (~7.6in), commentary right (~4.7in).",
            ],
            objects=[
                "Title: topic | finding.",
                "Exhibit: stacked column, worktype $ by yard.",
                "Commentary card: bold finding + two evidence bullets.",
            ],
        ),
    )
```

Every planned word lives in the slide region; `layout` / `objects` stay
high-level. Pair with `PAGE_SLIDE_16x9_TALL` (or `PAGE_SLIDE_16x9` for a
full-bleed slide page with no annotation).
