# 2026-06-08 — MRO deck: static think-cell charts, slides 8–15 completion, QA fixes

Session that (1) reversed the "leave think-cell charts blank" decision to **reproduce
them statically by transcription**, (2) completed the v3.3 → `deck_mro` port (slides
8–15), and (3) fixed three slides flagged in user QA (4, 5, 11). Continues
`2026-06-08_mro_deck_native_port.md` (slides 1–7); the reusable how-to lives in
`docs/faithful_deck_port_methodology.md`. Output deck:
`projects/mro/20260607_Navy USCG Vessel MRO Market Sizing_vS.pptx`.

Final state: **15 slides, build green, 1 native chart**; whole deck round-trips through
soffice without repair; 0 live `<a:fld>` / dangling `r:id` / connector glue / unresolved
`lumOff` across all `_chart_xml/` data. Memory: `mro-deck-native-port`.

---

## 1. The pivot — think-cell charts reproduced STATICALLY (was: leave blank)

The previous decision was to leave think-cell chart areas blank and reproduce only the
surrounding text. The user asked instead to **re-create the think-cell charts statically**.

Key realisation: **think-cell emits its chart as ordinary native shapes** right next to
the opaque OLE blob (`graphicFrame` named `think-cell data - do not delete`). The bar
segments are plain `<p:sp>` rectangles with `fill=scheme:accentN`; the axes are
`<p:cxnSp>` connectors; every data / axis / legend label is a "Text Placeholder" whose
text lives in an `<a:fld>` field. So you do **not** rebuild the chart from data — you
**transcribe the shapes think-cell already drew**, drop the OLE, and freeze the fields.
Pixel-faithful, fully static, no think-cell dependency.

The dumper (`dump_slide.py`) shows these label placeholders with *empty* text, because it
only reads `<a:r>` runs and the labels are in `<a:fld>` — that empty-text cluster of
`Text Placeholder 25` + `accentN` rects + `prst=line` connectors is the tell.

## 2. Tooling — `_qa/extract_chart.py`

Turns a slide's think-cell chart (and, in `--tables` mode, a dense native table) into
cleaned, fully static OOXML the module reads from `deck_mro/slides/_chart_xml/slideNN.xml`.
Balanced top-level `spTree` scan (handles nested `grpSp`), no XML parse that would mangle
namespace prefixes.

```bash
# chart mode: bar/axis/label shapes; drops OLE + the keep-out (chrome/table/caption/footer)
python extract_chart.py N --keepout 2,5,6,7,9,67 --offset 300 > .../_chart_xml/slideNN.xml
# table mode: a dense source <a:tbl>, verbatim + cleaned
python extract_chart.py N --tables 7        --offset 300 > .../_chart_xml/slideNN_table.xml
```

**Cleaning pipeline (final order):**
1. strip `<a:extLst>` (creationId / hiddenFill / dsbld cellmeta), `<p:extLst>` modId,
   `<p:custDataLst>` tags, inherited `<a:lstStyle>`.
2. **freeze `<a:fld>` → `<a:r>`** — the field's `type="datetime…"` is bogus and holds the
   cached label text; PowerPoint may *refresh* it to today's date and destroy the label,
   so it's rewritten to a static run (rPr + cached `<a:t>`). Verify `live <a:fld>=0`.
3. **strip connector glue** `<a:stCxn>`/`<a:endCxn>` — they anchor a `<p:cxnSp>` to shapes
   by id, which our id-renumber breaks; stripping makes the connector render from its own
   `xfrm` (off/ext/rot/flip), exact.
4. **resolve `schemeClr`+`lumMod`/`lumOff` → literal `<a:srgbClr>`** via an HLS transform.
   A *plain* `schemeClr` is kept (theme is byte-identical to `infra/template`), but a
   `schemeClr` carrying lum modifiers is baked to hex because **soffice mis-renders
   `schemeClr`+`lumOff`** (darkens instead of lightening). See §5 slide 4.
5. **strip hyperlinks** `<a:hlinkClick>`/`<a:hlinkHover>` — they reference a slide rel by
   `r:id` we don't carry; the run's rPr fill keeps the visible color.
6. **renumber `cNvPr id += offset`** (default +300) so chart ids don't collide with chrome
   (breadcrumb=2, title=3, prelim=4, sources=9999) or the module's own primitive ids.

The tool asserts `r:id/embed=0` and `live <a:fld>=0` and validates the result parses.
`_qa/regen_charts.sh` records every slide's exact `--keepout`/`--tables` args, so all
`_chart_xml/` files rebuild deterministically after a tool change.

**Module wiring** (data files are package data, NOT OPC parts — `build_pptx` won't bundle
them):
```python
_XML = Path(__file__).parent / "_chart_xml"
_CHART = (_XML / "slideNN.xml").read_text(encoding="utf-8")
...
return caption + _TABLE + footer + _CHART   # _CHART last so labels paint over bars
```

## 3. Slides 6 & 7 retrofitted; 8–15 completed

| # | Module | Pattern |
|---|---|---|
| 6 | `work_segments` | retrofit chart-blank → **static stacked bar** (49 shapes) + existing coverage table |
| 7 | `tam_composition` | retrofit → **static Marimekko** (124 shapes) + commentary rail |
| 8 | `topdown_detail` | static stacked bar + **verbatim 20-row rollup `<a:tbl>`** (see §4) |
| 9 | `topdown_funnel` | **native pptx chart** bundled verbatim (see §4) + transcribed neck connectors / labels / commentary |
| 10 | `reconciliation_bridge` | verbatim bridge `<a:tbl>` + 7 transcribed oval row-markers |
| 11 | `private_addressable` | all dual-narrative tiles / connectors / convergence callout transcribed |
| 12 | `fleet_structure` | verbatim tier-roster `<a:tbl>` + callout/caption; **DISCUSS dropped** |
| 13 | `fleet_mro` | **static Marimekko** (93 shapes) + commentary; DISCUSS dropped |
| 14 | `sam_sizing` | **Blank layout** (`slideLayout5`) — chrome transcribed with funnel shapes + verbatim Note/Detail table; DISCUSS dropped |
| 15 | `contract_vehicles` | verbatim 5-vehicle `<a:tbl>` + callout/caption; DISCUSS dropped |

Each registered in `deck_mro/slides/__init__.py` and visually diffed against its
`src_png/src-NN.png`. DISCUSS analyst review-stickies on 12–15 dropped via `--keepout`.
Slide-14 special case: it sits on the "Blank" layout (no breadcrumb/title placeholders),
so its chrome is transcribed verbatim with the body rather than rebuilt from builders.

## 4. Two patterns worth naming

**Verbatim dense table (`--tables`).** deck_core `table()`/`house_table()` hardcode cell
`marT/marB=45720` + 115% line spacing — fine for a few rows, but a ~20-row source table
(slide 8) overflows the slide. Fix: transcribe the native `<a:tbl>` verbatim; the cleaner
swaps the source's custom `tableStyleId` for the built-in **No-Style-No-Grid** GUID
(`{2D5ABB26-0587-4C30-8999-92F81FD0307C}`) so it keeps only its explicit per-cell fills /
borders (incl. the `bg1`+`lumMod50` grey total row) with no fallback grid, and needs no
`tableStyles.xml` entry. Used on slides 8, 10, 12, 14, 15 (and 4, 5 in the fix pass).

**Native chart part (slide 9).** The funnel is a real `<c:chart>` part (`chart1.xml`), not
think-cell shapes — `extract_chart` can't help. Bundle the source chart verbatim: strip
`<c:externalData>` (it renders from its cached `<c:numCache>` values, no embedded workbook
needed), set module `CHARTS=[{"chart_xml": <text>}]`, place with
`graphic_frame(rId="rId2", ...)`. Theme is identical so `schemeClr` refs resolve. Build
prints "1 charts" when wired. The funnel-neck connectors + stage labels + commentary are
transcribed separately.

## 5. QA fix pass — slides 4, 5, 11

User flagged: slide 4 wrong box fills + text overflow; slide 5 table needed work; slide 11
connectors. (Slides 4 & 5 were the earlier hand-built primitive versions.)

- **Slide 4 (Bottom-Up Methodology) — wrong fills.** The source boxes are `schemeClr tx1`
  with `lumMod`/`lumOff` modifiers (one theme color → a light/medium/dark navy ramp). The
  dumper only shows `scheme:tx1`, so the hand-built module flattened them all to dark `DK`;
  and soffice itself mis-renders `schemeClr`+`lumOff` (darkens). **Fix:** added the
  `schemeClr`+lum → `srgbClr` HLS bake to `extract_chart` (ramp resolves to
  `E2E9EF / B6C8D8 / 3D5972`), and rebuilt slide 4 by **verbatim transcription** (grid
  table id 14 via `--tables`; the 9 boxes + straight arrows + bent elbows + footer via
  `--keepout 2,4,5`).
- **Slide 4 — text overflow.** The hand-built boxes were mis-sized so two captions spilled
  below; the verbatim boxes are correctly sized, so the overflow is gone.
- **Slide 4 — elbow glue.** The source `bentConnector3` elbows carry `stCxn id="9"` /
  `endCxn id="27"` glue that id-renumbering breaks → added the **stCxn/endCxn strip** to
  `extract_chart` (also fixed 1 leftover glue ref on slide 14's transcribed annot).
- **Slide 5 (Vessel Taxonomy).** Rebuilt by **verbatim transcription** of the native table
  (id 3 via `--tables` — exact row heights, category fills, in-cell rotated
  Definition/Classifications labels) + MSC bubble / exhibit label / source line via
  `--keepout 2,4,7`. The source-line citations carried `<a:hlinkClick>` rels → added the
  **hyperlink strip** to `extract_chart` (rPr fill keeps the text color, no dangling rel).
- **Slide 11 (Private-Addressable).** Connectors are **byte-identical to the source** (short
  centred vertical stubs in the tile gaps, no glue) — already faithful; high-res diff is
  identical. User confirmed: **keep faithful (as source)**. No change.

After the tool changes, `regen_charts.sh` regenerated all `_chart_xml/` files. **Render
cache gotcha:** `render.sh` reuses a stale PDF — `rm _qa/png/*.pdf` before re-rendering
after a rebuild (this masked the slide-4 fix on first look).

## 6. Resume / regenerate

```bash
cd projects/mro/deck
/usr/bin/python3 build_deck.py                 # green = "wrote … 15 slides, 1 charts"
bash _qa/regen_charts.sh                        # rebuild every _chart_xml/ data file
rm -f _qa/png/*.pdf && _qa/render.sh            # fresh render of all 15 -> _qa/png/slide-NN.png
```

Data files: `deck_mro/slides/_chart_xml/slideNN.xml` (transcribed shapes),
`…_table.xml` (verbatim tables), `slide09_chart1.xml` (bundled native chart, externalData
stripped). Validation greps (all should be 0): `<a:fld`, `r:id=`/`r:embed=`,
`stCxn|endCxn`, `lumOff` across `_chart_xml/*.xml`.

## 7. Cross-references

- Reusable methodology (deck-agnostic): `docs/faithful_deck_port_methodology.md`
  (§7 = static think-cell + `extract_chart` cleaning rules; §2c = the tool).
- Slides 1–7 native-port log: `logs/2026-06-08_mro_deck_native_port.md`.
- Memory: `mro-deck-native-port`.
