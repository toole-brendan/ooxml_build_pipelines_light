# 2026-06-10 — Consolidated mini-deck port (vDraft slides 2–5 → deck_mini)

## Goal

Port slides 2–5 of `projects/consolidated/20260605_Defense Demand Drivers New
Construction_vDraft.pptx` **1:1, faithfully** into a NEW mini deck pipeline at
`projects/consolidated/deck_mini/`, following the MRO v3.3 port methodology
(`docs/faithful_deck_port_methodology.md`). Output:
`projects/consolidated/20260610_New Construction Methodology Mini_vS.pptx`.

Final state: **4 slides, 5 native chart parts, build green on the FIRST build**,
all four renders visually verified against the source side-by-side, and all
validation greps zero (`<a:fld>` / `r:id`/`r:embed` / `stCxn|endCxn` / `lumOff` /
think-cell residue across `_chart_xml/`). User QA: "looks great."

The four slides (all `slideLayout4` Light Blank, all chart-led):

| build # | vDraft # | module | content |
|---|---|---|---|
| 1 | 2 | `outsourced_bc_walk` | total-ship-spend → outsourced-BC walk, DDG + sub side by side, step/rationale ledger |
| 2 | 3 | `worktype_by_program` | work-type split, ~$21.2B submarine vs ~$4.0B DDG pools, methodology ledger |
| 3 | 4 | `outsourced_bc_annual_tam` | annual TAM FY22–FY31, pre/post-OBBBA, dense annotation layer |
| 4 | 5 | `worktype_by_fy` | FY-pair work-type stacked bars, full-width, shared legend |

## Why this went fast (~30 minutes, zero fix passes) — the load-bearing reasons

This was the *third* application of the faithful-port playbook, and everything
that made the MRO port slow had already been paid for once and written down:

**1. The methodology was already a document, not tribal knowledge.**
`docs/faithful_deck_port_methodology.md` prescribes the exact sequence — unzip
source → `dump_slide.py` per slide → layout map by NAME not number → theme
diff → transcribe at exact EMU → build → render → compare. No step had to be
re-derived; the doc was read first and followed literally.

**2. The tooling was battle-hardened and copied verbatim.** `dump_slide.py` and
`extract_chart.py` came straight from `projects/mro/deck/_qa/` with **every
cleaning rule already built in** from the MRO fix passes: the `<a:fld>`→`<a:r>`
freeze (bogus datetime fields), `stCxn`/`endCxn` connector-glue strip,
`schemeClr`+`lumMod`/`lumOff`→hex HLS bake (the soffice mis-render), hyperlink
strip, custData/creationId/lstStyle strip, and the `cNvPr id += offset`
renumber with self-validation (asserts parse-clean, `r:id=0`, `live fld=0`).
Each of those rules cost a debugging session in June's MRO port; here they all
ran correctly on the first invocation of every extraction.

**3. The source deck turned out to be OUR OWN pipeline's output, hand-edited.**
The first `dump_slide.py 2` showed pipeline-idiom shape names (`Breadcrumb`,
`PrelimChip`, `Title`, `StepLabel`, `StepRationaleLedger`) — the vDraft is a
baked `deck_consolidated` build (the fr1–fr4 front-row slides) that an analyst
then edited by hand: pasted think-cell charts over the native ones, added red
P1–P4 priority chips, purple "double check" wedge callouts, yellow highlight
runs in titles/sources, and reworded takeaways. Consequences that removed whole
phases of work:
- **Layout mapping was the identity.** The source's slideLayouts ARE the curated
  6-layout set; slides 2–5 all sit on `slideLayout4` (Light Blank) in both
  source and `infra/template` (the only layout diff was a hidden think-cell
  "Do not remove" tag shape — cosmetic).
- **Theme was byte-identical** (`diff` of theme1.xml), so plain `schemeClr`
  refs in the transcribed shapes and bundled charts resolve identically — no
  color resolution table needed.
- The geometry was already pipeline-clean EMU, so nothing fought the grid.

**4. One strategy decision did most of the work: transcribe EVERYTHING, no
keepout.** The MRO port rebuilt chrome with deck_core builders and transcribed
only bodies. Here the manual edits live IN the chrome — the title and sources
carry `<a:highlight>` yellow runs the builders can't emit, and the P-chips /
purple callouts are free-floating draft shapes. So each module is maximally
verbatim: `extract_chart.py N --offset 300` with **no `--keepout` at all**
(all sp/cxnSp transcribed, chrome included), `--tables` for the dense ledgers,
and the chart parts bundled (below). Builder-vs-source fidelity questions never
arose because nothing was rebuilt.

**5. The think-cell charts here are REAL native `<c:chart>` parts — so the MRO
slide-9 pattern applied directly.** Unlike the MRO v3.3 source (where think-cell
emitted its charts as loose `<p:sp>` shapes that had to be transcribed and
frozen), this think-cell vintage pasted genuine `chart1.xml`–`chart5.xml`
barChart parts whose ONLY relationship is the `<c:externalData>` link to an
embedded .xlsb. Strip that one element and each chart is fully self-contained
(renders from its cached `<c:numCache>` values). So every chart is bundled
verbatim via the module's `CHARTS=[{"chart_xml": ...}]` and placed with
`graphic_frame()` at the source frame's exact xfrm (rId2 first chart, rId3
second — slide 2 carries two). The OLE blobs ("think-cell data - do not
delete"), tagN.xml custData, and the image1.emf preview all fall away because
`extract_chart` skips graphicFrames and strips `custDataLst`.

**6. One z-order check before committing, instead of a render-debug loop.**
The modules emit `tables + chart frames + shapes` rather than the source's
interleaved order. That regroup is only safe because the chartSpace `spPr` is
`<a:noFill/>` (checked up front) — charts can't paint over the white
annualized-callout boxes that sit inside their frames, and the transcribed
shape layer (incl. the white divider connector and label patches that must
paint OVER the bars) comes last. Verified once, then trusted; the renders
confirmed it.

**7. Deterministic extraction from the start.** `_qa/regen_charts.sh` records
every slide's exact extraction args plus the chart externalData-strip step, so
all 12 `_chart_xml/` data files rebuild with one command — the same discipline
the MRO port adopted only after its tool-change fix pass forced a full regen.

## Pipeline layout (mirrors deck_mro / deck_consolidated)

```
projects/consolidated/deck_mini/
  build_deck.py                  # launcher
  deck_mini/
    __init__.py                  # sys.path shim (deck_mini + workspace-root deck_core)
    lib.py                       # bindings: OUT, infra/template + infra/assets, docProps
    slides/
      __init__.py                # SLIDE_RENDERS registry (4 modules, deck order)
      outsourced_bc_walk.py      # vDraft 2 (2 charts, 2 tables)
      worktype_by_program.py     # vDraft 3 (1 chart, 1 table)
      outsourced_bc_annual_tam.py# vDraft 4 (1 chart, 1 table)
      worktype_by_fy.py          # vDraft 5 (1 chart, no tables)
      _chart_xml/                # package data, NOT OPC parts (12 files)
        slide0N.xml              # transcribed shapes (chrome + annotations)
        slide0N_tables.xml       # verbatim <a:tbl> ledgers (No-Style-No-Grid GUID swap)
        slide0N_chartK.xml       # native chart parts, externalData stripped
  _qa/
    dump_slide.py extract_chart.py   # copied verbatim from mro/deck/_qa
    render.sh regen_charts.sh        # adapted paths; regen records all args
    src_xml/                         # vDraft unzipped (source of truth)
    src_png/src-0{2..5}.png          # source renders (96dpi) for side-by-side QA
    png/                             # built-deck renders
```

Module pattern (all four identical in shape):

```python
LAYOUT = "slideLayout4"
_SHAPES = (_XML / "slide02.xml").read_text(...)        # everything incl. chrome
_TABLES = (_XML / "slide02_tables.xml").read_text(...)
CHARTS = [{"chart_xml": _CHART_DDG}, {"chart_xml": _CHART_SUB}]
def _body():
    return _TABLES + graphic_frame(..., rId="rId2") + graphic_frame(..., rId="rId3") + _SHAPES
```

## Content decisions

Pure faithful port — **everything kept verbatim**, including the draft
artifacts: red P1–P4 priority chips, yellow `<a:highlight>` runs ("(something
about annualized avg. FY22–FY27", "AP/LLTM source…"), and the purple
"Double check based on MYP adjustments" wedge callouts. These are analyst
working notes in a vDraft; stripping them is a one-line `--keepout` /
`.replace()` change per slide if a clean deliverable version is wanted later.

## Resume / regenerate

```bash
cd projects/consolidated/deck_mini
/usr/bin/python3 build_deck.py        # green = "wrote … 4 slides, 5 charts"
bash _qa/regen_charts.sh              # rebuild every _chart_xml/ data file
bash _qa/render.sh                    # -> _qa/png/slide-N.png (rm _qa/png/*.pdf first after a rebuild)
# compare _qa/png/slide-N.png vs _qa/src_png/src-0(N+1).png
```

Validation greps (all 0): `<a:fld`, `r:id=|r:embed=`, `stCxn|endCxn`, `lumOff`,
`think-cell` across `deck_mini/slides/_chart_xml/*.xml`.

## Cross-references

- Methodology: `docs/faithful_deck_port_methodology.md` (§7 static charts /
  extract_chart rules; the native-chart-part path used here is §7's footnote
  pattern, proven on MRO slide 9).
- MRO port logs: `logs/2026-06-08_mro_deck_native_port.md`,
  `logs/2026-06-08_mro_deck_static_thinkcell_charts_and_completion.md`.
- The vDraft's ancestor modules: `projects/consolidated/deck/deck_consolidated/
  slides/fr{1..4}_*.py` (native-chart originals these slides were hand-edited from).
- Memory: `consolidated-mini-deck-port`.
