# 2026-06-08 — MRO deck native port (v3.3 → deck_mro slide modules)

## Goal

Port the **15-slide v3.3 MRO deck** (`projects/mro/20260408_Commercial Strategy_Defense
Demand Drivers_MRO_v3.3.pptx`, also at `/Users/brendantoole/projects3/mro/…v3.3.pptx`)
**1:1, faithfully**, into native `deck_mro/slides/` modules built on the shared
`deck_core` engine — the deck analog of the workbook native rewrite. Output:
`projects/mro/20260607_Navy USCG Vessel MRO Market Sizing_vS.pptx`.

The pipeline scaffold (`projects/mro/deck/`) already existed cover-only. This port fills
slides 2–15. **Faithful reproduction means matching the source OOXML** (exact EMU
geometry, fills, fonts, tables, shapes) — NOT re-skinning into the ddg/submarines house
layout. (An earlier attempt invented house-style layouts and was rejected by the user:
"those slides dont look like the slides in v3.3".)

## Locked decisions (user)

- **Naming:** BuildCo → **Saronic** consistently (the brand template IS Saronic). Keep
  "Marauder", and keep the source's "USN / USCG" wording where it appears.
- **DISCUSS boxes** (yellow analyst-question callouts on src slides 12–15): **drop them**.
- **think-cell charts:** ~~leave BLANK~~ **SUPERSEDED 2026-06-08 (user request): reproduce
  them STATICALLY.** think-cell emits the chart as ordinary native shapes (accent-fill
  `<p:sp>` bars, `<p:cxnSp>` axes, `<a:fld>`-label placeholders) next to the OLE blob —
  transcribe those shapes, drop the OLE, and freeze every `<a:fld>`→`<a:r>` (else
  PowerPoint refreshes the bogus `datetime` fields to today's date). Tool:
  `_qa/extract_chart.py` (chart mode + `--tables` verbatim-table mode). See
  methodology §7. Native-pptx chart on src slide 9: treat the same (transcribe its
  shapes if think-cell-style; otherwise decide when reached).

## Workflow + tooling (all under `projects/mro/deck/_qa/`)

- `src_xml/` — the v3.3 pptx unzipped (source of truth).
- `dump_slide.py N` — dumps slide N's shape tree: per-shape id/name/geometry(EMU+inches)/
  prst/fill/line, text runs w/ props, and full table structure (cols, row heights, per-cell
  fill + span + text). **This is the primary tool** — run it per slide before building.
  For run-level detail inside table cells, or connector flips/avLst, use small inline
  python (examples in the transcript).
- `render.sh [first] [last]` — builds nothing; converts the BUILT deck to PDF via soffice
  then per-slide PNG via pdftoppm (96 dpi) into `_qa/png/slide-N.png`. Read those to QA.
- `src_png/src-NN.png` — the rendered SOURCE slides, for side-by-side comparison.
- Build: `cd projects/mro/deck && /usr/bin/python3 build_deck.py` (green = "wrote … N slides").

## Layout mapping (source layout name → infra/template layout number)

`infra/template` is the same Saronic brand template but renumbers to a curated 6-layout set:

| source slide | source layout | use `LAYOUT =` |
|---|---|---|
| 1 cover | Cover 1 | `slideLayout1` |
| 2 overview | 50% Block + Title (dark-left panel) | `slideLayout3` |
| 3–13, 15 | Light Blank | `slideLayout4` |
| 14 | Blank | `slideLayout5` |

The dark-left panel on slide 2 comes FROM `slideLayout3` (don't draw it). Content slides
use `slideLayout4` (provides footer logo + "SARONIC PROPRIETARY AND CONFIDENTIAL" + page #).

## Chrome — deck_core builders reproduce the v3.3 content-slide chrome exactly

Content slides (3–15) use these deck_core builders (verified pixel-faithful vs source):
- `breadcrumb(SECTION, TOPIC)` → "TAM / Definitions" (bold section + " / " + topic, 10pt #44505C)
- `prelim_chip()` → the "Preliminary" yellow box top-right
- `title_placeholder(TOPIC, TAKEAWAY)` → "Topic | Finding." 20pt #162029
- `sources_line(text)` → the bottom source line (pass the source's own "Source: …" string)

The v3.3 titles are ALREADY in "Topic | Finding." form and the headers are already
breadcrumbs — so chrome maps 1:1. Slide 2 (overview) is the exception: no breadcrumb/
prelim/title — it places a light "Overview" title + two header/bulleted-body columns +
yellow note directly (see `overview.py`).

## Reusable reproduction techniques established

- **Concentric rings** (slide 3): `text_box(..., prst="ellipse", fill=BLUE_n, line_color="C0C0C0", line_width=3175)` with empty `[paragraph([])]`, at exact source off/ext. Blue ramp maps EXACTLY: BLUE_1=E2E9EF, BLUE_2=B6C8D8, BLUE_3=6E91B1, BLUE_4=3D5972, BLUE_5=263746. Gray ramp: GRAY_1=F2F2F2, GRAY_3=BFBFBF, GRAY_4=7F7F7F. DK=162029.
- **Greyed table rows** (slide 3 future-effort): `house_table(..., cell_fills={(r,c):GRAY_1}, cell_text_colors={(r,c):GRAY_4})`.
- **Elbow/bent connectors** (slide 4): source think-cell elbows are `bentConnector3 rot="5400000"` with shape-anchored endpoints; reproduce as **raw `<p:cxnSp>`** with the exact `xfrm rot/off/ext`, `prstGeom bentConnector3`, `<a:ln><a:solidFill srgbClr=DK/><a:tailEnd type="triangle"/>` — strip the stCxn/endCxn so it renders statically. Straight arrows = `connector(id,name,x,y,cx,cy,color=BLACK,arrow=True)`.
- **Bulleted bodies w/ levels** (slide 2): `paragraph(runs, bullet=True, mar_l=285750, indent=-228600)` for L0; manual "–  " prefix + `mar_l=461963, indent=-176213` (no bullet) for L1 sub-bullets.
- **Merged tables** (slides 5, 8, etc.): low-level `table()/trow()/tcell()/tcell_rich()` with `grid_span` / `row_span`; the engine synthesizes hMerge/vMerge filler cells — provide only the spanning cell, omit covered cells.

## Generalized methodology

The reusable, deck-agnostic write-up of this whole process — philosophy, the
`dump_slide.py` + `render.sh` tooling (full source embedded), the per-slide loop,
layout-mapping, the shape→primitive cookbook, think-cell-blank rule, color
resolution — lives at **`docs/faithful_deck_port_methodology.md`**. Read that first.

## Static think-cell charts — tool + pattern (2026-06-08)

`_qa/extract_chart.py` turns a slide's think-cell chart into cleaned, fully static
OOXML read by the module from `deck_mro/slides/_chart_xml/slideNN.xml`:
- **chart mode:** `extract_chart.py N --keepout <ids> --offset 300` — emits the
  bar/axis/label shapes; drops the OLE graphicFrame + the keep-out (chrome / table /
  caption / footer) shapes; freezes every `<a:fld>`→`<a:r>`; strips think-cell
  custData / creationId / hiddenFill / dsbld extLst + inherited lstStyle; keeps
  `schemeClr accentN` (source theme == infra/template theme, verified identical);
  renumbers cNvPr id += offset. Asserts `r:id/embed=0` and `live <a:fld>=0`.
- **table mode:** `extract_chart.py N --tables <id> --offset 300` — emits a dense
  source `<a:tbl>` verbatim (swaps tableStyleId → built-in No-Style-No-Grid GUID,
  strips dsbld cellmeta). Use this instead of rebuilding via `table()`/`house_table()`
  when the source table is tall: deck_core hardcodes cell `marT/marB=45720` + 115%
  line spacing, which overflows a ~20-row table.
- Module wiring: `_CHART = (Path(__file__).parent/"_chart_xml"/"slideNN.xml").read_text()`,
  append after the table so labels paint over bars. The `_chart_xml/` dir is package
  data, NOT an OPC part — build_pptx won't bundle it.

Generalized write-up is in `docs/faithful_deck_port_methodology.md` §7.

## Status

**DONE + visually verified (faithful):** slide 1 cover (`cover_mro.py`, pre-existing),
2 overview, 3 definitions, 4 bottom_up_approach, 5 vessel_taxonomy, 6 work_segments
(static stacked bar), 7 tam_composition (static Marimekko, 124 shapes),
8 topdown_detail (static stacked bar + verbatim 20-row rollup `<a:tbl>`),
9 topdown_funnel (**native pptx chart** path: chart1.xml bundled VERBATIM via CHARTS
with `<c:externalData>` stripped + placed by `graphic_frame`; neck connectors / stage
labels / commentary / caption / footer transcribed). Registered in
`deck_mro/slides/__init__.py`. Build green (9 slides, 1 chart). Slides 6 & 7 were
retrofitted from chart-blank to static charts. Remaining: 10–15 (notes below).

### PORT COMPLETE (2026-06-08) — all 15 slides

10 reconciliation_bridge (verbatim bridge `<a:tbl>` + 7 transcribed oval markers),
11 private_addressable (all dual-narrative tiles/connectors/callout transcribed),
12 fleet_structure (verbatim tier-roster table + transcribed callout/caption; DISCUSS
dropped), 13 fleet_mro (static Marimekko, 93 shapes + commentary; DISCUSS dropped),
14 sam_sizing (Blank layout `slideLayout5` — chrome transcribed with the funnel
shapes + verbatim Note/Detail table; DISCUSS dropped), 15 contract_vehicles (verbatim
5-vehicle table + transcribed callout/caption; DISCUSS dropped). All registered;
**build green (15 slides, 1 chart)**; whole deck round-trips through soffice without
repair; `grep` confirms 0 live `<a:fld>`, 0 `r:id`, 0 think-cell/dsbld residue across
all `_chart_xml/*.xml`. DISCUSS review-stickies dropped on 12/13/14/15 via `--keepout`.

### Fix pass (2026-06-08) — slides 4 & 5 rebuilt verbatim; extract_chart hardened

User QA flagged: slide 4 (Bottom-Up Methodology) wrong box fills + text overflow;
slide 5 (Vessel Taxonomy) table needed work; slide 11 connectors. Root causes + fixes:
- **Slide 4 fills:** the source boxes are `schemeClr tx1` with **`lumMod`/`lumOff`**
  modifiers (one theme color → a light/medium/dark navy ramp). The previous hand-built
  module flattened them all to dark `DK`. soffice ALSO mis-renders `schemeClr`+`lumOff`
  (darkens). Fix: `extract_chart` now **bakes `schemeClr`+lum → explicit `srgbClr`** via
  an HLS transform (E2E9EF / B6C8D8 / 3D5972 ramp), and slide 4 is rebuilt by VERBATIM
  transcription (table id 14 grid via `--tables`; the 9 boxes + arrows + elbows + footer
  via `--keepout 2,4,5`). Text overflow gone (verbatim boxes are correctly sized).
- **Slide 4 elbows:** source `bentConnector3` carry `stCxn`/`endCxn` glue (by id) that
  id-renumbering breaks → `extract_chart` now **strips stCxn/endCxn** so connectors
  render from their xfrm. (Also fixed 1 leftover glue ref on slide 14.)
- **Slide 5:** rebuilt by verbatim transcription — table id 3 via `--tables` (exact row
  heights, category fills, in-cell rotated Definition/Classifications labels), MSC bubble
  + exhibit label + source line via `--keepout 2,4,7`. Source-line citations carried
  `<a:hlinkClick>` rels → `extract_chart` now **strips hyperlinks** (rPr fill keeps the
  text color; avoids dangling rels).
- **Slide 11:** connectors are BYTE-IDENTICAL to the source (short centred vertical stubs
  in the tile gaps, no glue) — already faithful; no change needed (flagged to user as a
  source characteristic, not a port bug).

extract_chart cleaning order now: extLst/custData/lstStyle strip → fld→run → stCxn/endCxn
strip → schemeClr+lum resolve → hlink strip → id renumber. `_qa/regen_charts.sh` records
every slide's args and rebuilds all `_chart_xml/` deterministically. Gotcha: `render.sh`
reuses a stale PDF — `rm _qa/png/*.pdf` before re-rendering after a rebuild. Whole deck
re-verified: build green (15 slides, 1 chart), 0 fld / r:id / glue / lumOff residue.

**Native-chart pattern (slide 9, for any `<c:chart>`-backed source object):** the
source funnel is a real chart part, not think-cell shapes — `extract_chart.py` can't
help. Bundle the source `chartK.xml` verbatim: strip `<c:externalData>` (renders from
cached `<c:numCache>` values, no embedded workbook needed), set module
`CHARTS=[{"chart_xml": <text>}]`, and place with `graphic_frame(rId="rId2", ...)`. Theme
is identical so `schemeClr` refs resolve. Build prints "N charts" when wired.

**REMAINING (5–15) — per-slide source notes (from dumps):**
- **5 vessel_taxonomy** — ONE big merged table (8 cols: thin 200497 label col + 7×1666720), 4 rows: spanned header (US Navy gridSpan5 #bg2 / US Coast Guard gridSpan2 #7F7F7F), category row (7 fills: Combatant Ships #223E59, Auxiliary bg2, Combatant Crafts #99B9D8, Unmanned bg2, Support #F2F6FA, Cutters #BFBFBF, Boats #F2F2F2), Definition row, Classifications row (huge per-col hull lists). Thin left col = rotated "Definition"/"Classifications" labels. + a wedgeRectCallout (MSC note, #E2E9EF) + small italic "U.S. Navy and Coast Guard Vessel Taxonomy" label top-left + source line. Hardest slide.
- **6 work_segments** — think-cell stacked bar (LEAVE BLANK) + a Work Segment / Coverage table (6 segments) + title/source. Title: "MRO Work Segments | Depot ship repair at ~53% …". Breadcrumb "TAM / Work Segments".
- **7 tam_composition** — think-cell Mekko (BLANK) + a segment-composition-by-hull commentary table (6 rows). Breadcrumb "TAM / Composition".
- **8 topdown_detail** — rollup TABLE (Category / FY2025 $M / PB26 PDF Source; indented hierarchy, ~18 rows incl. OMN 1B4B, private avails leaves, Public NSY, OPN/MSC/SCN/USCG, $16,996M total) + think-cell stacked bar (BLANK). Breadcrumb "TAM Sizing / Top-Down Detail".
- **9 topdown_funnel** — has the ONE native pptx chart (chart1.xml) — LEAVE BLANK per decision; reproduce the funnel commentary text blocks ($17.0B pool / Public NSY $7.49B / $9.5B residual). Breadcrumb "TAM Sizing / Top-Down Funnel".
- **10 reconciliation_bridge** — 7-component bridge TABLE (Bridge Component / Top-down $M / Bottom-up $M / Gap / Explanation; ~8 rows + total) + numbered markers 1–7. Breadcrumb "TAM Sizing / Reconciliation".
- **11 private_addressable** — dual-narrative cards: Narrative A (Bottom-Up/FPDS) + Narrative B (Top-Down/Budget Anchor) + a convergence strip ("A=$8,971M / B=$9,511M / Delta=$540M (~6%)"). Breadcrumb "TAM Sizing / Private-Addressable".
- **12 fleet_structure** — 3-tier comp-set TABLE (Tier/mission / Hull programs / Role and Marauder fit / FY2025 $M) + hull-inclusion-criteria block. DROP the DISCUSS box. Breadcrumb "SAM / Fleet Structure".
- **13 fleet_mro** — think-cell stacked bar (BLANK) + work-type + hull-concentration commentary blocks. DROP DISCUSS box. Breadcrumb "SAM / Marauder-Like Fleet MRO".
- **14 sam_sizing** — uses `slideLayout5` (Blank). TAM→SAM nested/funnel ($623M) text blocks + a Note/Detail table. DROP DISCUSS box. Breadcrumb "SAM / Sizing".
- **15 contract_vehicles** — dense 5-vehicle TABLE (Vehicle / Qualification requirements / Typical POP/ceiling / Example awardees: MSRA, MAC-MO, SeaPort-NxG, FedMall/GSA, USCG/SFLC) + qualification-paths block. Breadcrumb "SAM / Contract Vehicles".

## Resume

```
cd projects/mro/deck
# per slide N: read source design, then build module
/usr/bin/python3 _qa/dump_slide.py N          # source geometry/text/fills/tables
# … write deck_mro/slides/<name>.py, register in slides/__init__.py …
/usr/bin/python3 build_deck.py                # must stay green
_qa/render.sh N N                             # -> _qa/png/slide-N.png ; compare to _qa/src_png/src-0N.png
```

Memory pointer: `mro-deck-native-port`.
