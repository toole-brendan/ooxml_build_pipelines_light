# 2026-06-10 — deck_mini_v2 charts made editable (reattach source .xlsb)

## Problem

The deck_mini / deck_mini_v2 faithful ports bundle each source think-cell chart
as a verbatim `<c:chart>` part but **strip `<c:externalData>`** at extraction
time, so the charts render from their cached `<c:numCache>` values yet have **no
backing workbook** — PowerPoint greys out "Edit Data". (Contrast the MRO native
charts on slides 6/7/8/13, which are re-authored via `column_chart()` and so
emit a generated `.xlsx`; MRO slide 9 is bundled-and-stripped like these.)

Goal: make deck_mini_v2's 5 charts editable **without re-authoring** — i.e. keep
the chart XML byte-for-byte, just restore the Edit-Data backing. User asked
specifically for the embedded workbook to be the **binary `.xlsb`** the source
actually carried (most faithful — zero data reconstruction).

## What the source had (verified)

- `_qa/src_xml/ppt/charts/chart{1..5}.xml` → each `<c:externalData r:id="rId1">`
  → `_rels/chartK.xml.rels` → `../embeddings/Microsoft_Excel_Binary_Worksheet*.xlsb`.
- The 5 `.xlsb` are clean, self-contained OPC zips (`xl/workbook.bin`,
  `sheet1.bin`, `styles.bin`; **no** think-cell linkage — the think-cell OLE
  blobs are the separate `oleObject*.bin` parts we don't bundle).
- All chart `<c:f>` refs are `Sheet1!$A$N:$X$N` single-row numeric ranges that
  already match the `.xlsb` layout. So reattaching the original workbook +
  re-adding externalData reproduces the source's exact editable state.
- The 5 bundled `_chart_xml/slide0N_chartK.xml` were confirmed to pair with the
  right source chart (hence the right `.xlsb`) by matching first-row numCache
  values — `slide01_chart1↔chart1↔Worksheet.xlsb`, …, `slide05_chart5↔chart5↔
  Worksheet4.xlsb`. All 5 consistent.

## Changes

### 1. `deck_core/charts.py` — new `editable_bundled_chart(chart_xml, embed_bytes, *, embed_ext="xlsb")`
Returns the CHARTS dict the build loop wires. It:
- re-inserts `<c:externalData r:id="rId1"><c:autoUpdate val="0"/></c:externalData>`
  right before `</c:chartSpace>` **iff** absent (these parts end
  `</c:chart></c:chartSpace>` with no spPr/txPr/printSettings/userShapes after
  the chart, so that slot is schema-valid);
- sets `embed_xlsx`=the source workbook bytes, plus a matching `chart_rels`
  (rId1 → the embed), `embed_filename` template, and `embed_content_type`.
- `_BUNDLED_EMBED_SPECS`: `xlsb` → `Microsoft_Excel_BinaryWorksheet{chart_num}.xlsb`
  + `application/vnd.ms-excel.sheet.binary.macroEnabled.12`; `xlsx` → the native
  convention. The chart caches and every other byte are untouched → render is
  identical; only Edit-Data is restored.

### 2. `deck_core/lib.py` — pipeline embed handling generalized (additive)
Previously the chart loop hardcoded `Microsoft_Excel_Worksheet{N}.xlsx` +
`spreadsheetml.sheet` for every embed. Now a chart dict may carry
`embed_filename` (template, `{chart_num}`) and `embed_content_type`; both
**default to the old `.xlsx` values**, so native charts (ddg/subs/consolidated)
are byte-identical. `_content_types_xml` now takes a list of
`(PartName, content-type)` embeds instead of `embedded_xlsx_nums` and emits one
Override per embed with its own type. `embed_xlsx` (the payload field name) is
unchanged for back-compat.

### 3. deck_mini_v2 modules + assets
- Copied the 5 source `.xlsb` into `deck_mini_v2/slides/_chart_xml/` as
  `slide0N_chartK.xlsb` (1:1 with the chart XML).
- `outsourced_bc_walk` / `worktype_by_program` / `outsourced_bc_annual_tam` /
  `worktype_by_fy`: `CHARTS = [editable_bundled_chart(_CHART, _XLSB), …]` (the
  walk passes two). Docstrings updated (no longer "externalData stripped").

## Verification

- Build green: **6 slides, 5 charts**. Built pptx: 5 `.xlsb` embeddings
  (`Microsoft_Excel_BinaryWorksheet{1..5}.xlsb`), each a valid workbook; every
  `chart{i}` has `externalData r:id=rId1` → `chartI.xml.rels rId1` → its `.xlsb`;
  Content_Types declares all 5 binary; slide→chart rels intact.
- **Strict OPC check**: every part has a content type, zero dangling rel
  targets (`.bin` covered by the pre-existing oleObject Default; `.xlsb` via
  Override). Clean for real PowerPoint, not just soffice.
- soffice round-trips with no Repair; slides 1 & 3 renders are **pixel-identical**
  to `src_png/` (charts unchanged).
- **Regression**: mro (15/5), ddg (25/9), submarines (27/9), consolidated (25/13),
  deck_mini (4/5) all rebuild green; ddg's native embeds remain 9× `.xlsx` with
  the `spreadsheetml.sheet` type → default path untouched.

## Follow-up available (not done)

`deck_mini` (the predecessor `…_vS.pptx`) has the SAME stripped-chart charts and
the SAME 5 source `.xlsb` available — applying `editable_bundled_chart` there is
the identical one-line-per-module change if a consistent editable mini deck is
wanted.

## Resume

```bash
cd projects/consolidated/deck_mini_v2 && /usr/bin/python3 build_deck.py   # 6 slides, 5 charts
# verify embeds/rels/externalData + strict OPC: see the inline python in this session
```

## Cross-references
- Port logs: `logs/2026-06-10_consolidated_mini_v2_deck_port_all_6_slides.md`,
  `logs/2026-06-10_consolidated_mini_deck_port_slides2-5.md`.
- The stripped-bundle pattern this fixes: `docs/faithful_deck_port_methodology.md`
  §7 footnote (MRO slide 9); native editable charts: the consolidated restyle log
  `logs/2026-06-08_consolidated_charts_thinkcell_restyle.md`.
