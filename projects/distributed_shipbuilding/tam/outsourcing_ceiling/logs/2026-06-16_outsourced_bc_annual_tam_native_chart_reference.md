# 2026-06-16 — Outsourced-BC Annual TAM: verbatim port → self-contained native-chart reference

Converted deck_primary slide 3 (`outsourced_bc_annual_tam`, the annual outsourced-BC
TAM stacked-column slide) from an opaque verbatim OOXML port into an **agent-editable
native-chart reference**, built in three stages, verified visually identical at every
step, then **flattened into one self-contained module**. The `.xlsb` was preserved
byte-for-byte throughout (explicit user requirement).

Methodology saved to memory: `port-to-editable-staging.md`. Related precedent from
earlier this session (gso flow-chart hybrid): `flow_charts_graph.py` in
`projects/gso_JM_reference/deck_gso_JM/`.

## Final state (deck_primary/deck_primary/slides/)
- **`outsourced_bc_annual_tam_ref.py`** — the live, self-contained reference (registered slide 3).
- `outsourced_bc_annual_tam.py` — original verbatim port, **kept on disk, unregistered** (archived comparator).
- Deleted (superseded staging twins): `…_chart_ref.py`, `…_layers.py`, `…_data.py`.
- New `_chart_xml/` assets from the overlay split: `slide03_{chrome,forecasted_chip,forecast_framing,fy_labels,value_labels,dollar_callouts,legend,penetration}.xml` (the ref reads 7; penetration is generated, its file kept as the template source). Originals `slide03.xml` / `slide03_chart4.{xml,xlsb}` / `slide03_tables.xml` untouched.
- Side bundle at projects3 root: `outsourced_bc_annual_tam_port/` (the module + its 4 loaded assets, copied for handoff; no generator).

Build:  `cd projects/distributed_shipbuilding/deck_primary && python3 build_deck.py`  → `…/20260610_Distributed Shipbuilding New Construction_vS.pptx` (12 slides, 6 charts)
Validate: schema-check every slide part against `infra/ooxml_reference/schema/pml.xsd` with lxml (catches "repair on open" that build-green and minidom miss).

## What the port did, and the problem
Thin verbatim assembler: `_body() = slide03_tables.xml + graphic_frame(rId2) + slide03.xml`,
with the native chart (`slide03_chart4.xml`) bundled via `editable_bundled_chart()` + its
`.xlsb`. Faithful but opaque — the 146 KB `slide03.xml` overlay (174 shapes) and the chart
data hid every semantic editing handle.

## Stages (each a twin, registered after its predecessor, then verified)

### Stage 1 — native-chart-first + semantic mirror (`…_chart_ref.py`)
Render path unchanged → **byte-identical** to the port. Added a descriptive mirror above it,
extracted from `chart4.xml`'s cache: `CHART_NODE`, `CHART_STYLE` (stacked col, gap 0, overlap
100, y 0–15/major 5, hidden cat labels), `PROGRAMS`, `CHART_SERIES` (2 stacked rows: outsourced
over retained), and **`CHART_POINTS`** — 27 real points on a stride-4 FY grid (+0 ddg51, +1
virginia, +2 columbia, +3 spacer), `total_label`/`penetration` derived. Principle: never
decompose a real `<c:chart>` into shapes.

### Stage 2 — split the overlay into 8 named layers (`…_layers.py`)
Byte-exact scan of the 174 overlay shapes, classified by `cNvPr` name + text into 8 groups
(chrome 5 · forecasted_chip 1 · forecast_framing 80 · fy_labels 10 · value_labels 32 ·
dollar_callouts 4 · legend 18 · penetration 24), written to per-group files, emitted in paint
order. **Proved visually identical**, not byte-identical: (a) shape multiset == original, and
(b) of 454 reordered pairs, **0 had overlapping bboxes** → regrouping only swaps spatially
disjoint shapes, so nothing moves on screen. forecast_framing (think-cell geometry) flagged
pinned-forever.

### Stage 3 — data-driven penetration layer (`…_data.py`)
Regenerated only the penetration layer. Every shape type had exactly **one** style template;
lifted each verbatim (placeholders for id/off/text only), drove the % ovals from
`CHART_POINTS[i].penetration` ("n/a" falls out where a program has no point in an actual year),
with the ranges/labels/notes as their own small data. **Verified zero drift**: regenerated
`{name,x,y,text}` set == the export's (24 shapes), and no `"11%"`-style literal remains in the
module. `.xlsb` reused unchanged.

## Flatten + cleanup
Collapsed `chart_ref → layers → data` (which imported each other) into one self-contained
**`outsourced_bc_annual_tam_ref.py`** — sections ① chart + mirror, ② 8 named layers, ③
penetration generator — with no intra-family imports. Verified `ref.render() == data.render()`
(modulo shape ids). Swapped it into slide 3, unregistered the chain, deleted the three staging
twins (confirmed nothing else imported them), kept the verbatim port. Rebuilt: 12 slides,
schema ALL VALID.

## Key decisions / gotchas
- **`.xlsb` is chart-only** — Stage 3 touches overlay shapes, never the chart part, so "Edit Data" is unaffected. Binary `.xlsb` authoring is deliberately never attempted.
- **One FY2025 ddg oval** is nudged ~0.012 in left in the export; preserved exactly via `PEN_X_OVERRIDE` rather than forced onto the clean column grid.
- Earlier in the session, a separate gso experiment hit a **"repair on open"** because a computed connector used `<p:cxnSp>` + `<a:custGeom>`; custom geometry belongs in `<p:sp>`. Captured in `pptx-repair-invalid-enums.md` along with the lxml/`pml.xsd` validation harness now used here.
