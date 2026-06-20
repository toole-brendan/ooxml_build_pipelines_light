# 2026-06-16 — GS&O style-guide deck: faithful port + surgical style-system reconciliation

## Goal

Two linked deliverables off a single source file,
`/Users/brendantoole/projects3/20260615_GS&O_Strategy Materials Style Guide.pptx`
(5 slides). The deck is itself a **style guide**: each slide is a worked example
of one exhibit archetype (bridge charts, bar charts, tables, flow charts),
annotated with floating purple `JM:` reviewer directives (initials JM).

1. **Faithful 1:1 port** of the 5 slides into a new native `deck_core` pipeline
   (`docs/faithful_deck_port_methodology.md`), filtering the `JM:` callouts out of
   the render and into a markdown reference at the new pipeline's root.
2. **Surgical reconciliation** of the `JM:` directives against the shared house
   style (`deck_core/slide_guide.md`, `target_copy.txt`, `deck_core/primitives.py`)
   — permissive additions only, never new mandates (primary slide authors are AI
   agents; the engine is a reference, not a straitjacket).

Output deck: `projects/gso_JM_reference/20260615_GSO_Strategy Materials Style Guide_vS.pptx`.

---

## Layout & structure

New pipeline lives under a new `projects/gso_JM_reference/` (so the structure
mirrors the other engagements one level under `projects/`):

```
projects/gso_JM_reference/
├── 20260615_GSO_Strategy Materials Style Guide_vS.pptx   ← output (5 slides, 4 charts)
└── deck_gso_JM/
    ├── JM_style_notes.md            ← the 41 JM directives, verbatim (deliverable 1's filter output / deliverable 2's input)
    ├── build_deck.py
    ├── deck_gso_JM/                 ← package: __init__.py (sys.path), lib.py (bindings), slides/
    │   └── slides/  bridge_charts_1 · bridge_charts_2 · bar_charts · tables · flow_charts
    │                (+ _chart_xml/ extracted data, images/ copied media)
    └── _qa/   src_xml · src_png · png · dump_slide.py · extract_chart.py · extract_pics.py · regen_charts.sh · render.sh
```

`deck_gso_JM/__init__.py` puts the build dir + workspace root (parents[4]) on
sys.path, exactly like `deck_mini_v2`; depths match (`gso_JM_reference` is one
level under `projects/`, same as `distributed_shipbuilding`). `lib.py` binds OUT
+ `infra/template` + `infra/assets` + a per-deck `slides/images/` dir.

---

## Gating facts (verified before any module was written)

- **All 5 source slides use `slideLayout13` = "Light Blank"** → maps to
  `infra/template` `slideLayout4` ("Light Blank"). `LAYOUT = "slideLayout4"` on
  every module. (Matched by layout *name*, per methodology §4.)
- **Theme is byte-identical to `infra/template`** — same brand template family as
  the shipbuilding/MRO decks (dk1=162029, accents 79838F/1D4D68/486D82/89A2B0/
  AFC2CC/D8E3EB, …). So `extract_chart.py`'s `_THEME` map is valid as-is and plain
  `schemeClr` refs resolve to the same hexes. No per-deck color resolution needed.
- **4 native `<c:chart>` parts** (chart1–4) + **4 `.xlsb`** + 6 OLE blobs. The
  charts are real native charts (the OLE/think-cell frames are the "do not delete"
  blobs, dropped). chart→xlsb (from `charts/_rels`): chart1←Worksheet.xlsb,
  chart2←Worksheet1, chart3←Worksheet2, chart4←Worksheet3.

---

## Per-slide port (final deck order = source order)

| # | module | archetype | charts | table | real pics |
|---|---|---|---|---|---|
| 1 | `bridge_charts_1` | Bridge Charts (1/2) — newbuild price-reduction levers | chart1 (rId2) | 331 | US-flag wordmark image6.png (rId3) |
| 2 | `bridge_charts_2` | Bridge Charts (2/2) — MR product-tanker opex comps | chart2 (rId2), chart3 (rId3) | — | OSG/Hafnia/Scorpio/Torm logos image7–10 (rId4–7) |
| 3 | `bar_charts` | Bar Charts — SCF legally-mandated demand | chart4 (rId2) | 11 | — (only the OLE-EMF, dropped) |
| 4 | `tables` | Tables — opex categories driving cost differential | — | 155 | 4 shadowed source images image11–14 (rId2–5) |
| 5 | `flow_charts` | Flow Charts — SCF subsidy / penalty flow | — | — | China flag image15 (rId2) + US flag image6 ×3 (rId3–5) |

Each module is a thin verbatim read (the `deck_mini_v2/outsourced_bc_walk` pattern):
`slide(_body())` where `_body()` concatenates the extracted `_chart_xml/slideNN.xml`
(chrome + overlays + callouts + connectors, JM callouts removed), `slideNN_tables.xml`
(verbatim `<a:tbl>`), `slideNN_pics.xml` (verbatim `<p:pic>` with remapped embeds),
and `graphic_frame(rId=…)` placements for the native charts. `CHARTS =
[editable_bundled_chart(chart_xml, xlsb)]` re-adds `<c:externalData>` + the .xlsb so
"Edit Data" works; `IMAGES = [{"rId","file"}]` wires the picture rels.

---

## Tooling

- `_qa/dump_slide.py`, `_qa/extract_chart.py` — copied verbatim from `deck_mini_v2`.
- **NEW `_qa/extract_pics.py`** — extracts named top-level `<p:pic>` shapes verbatim
  (strips `extLst`, remaps each `blip r:embed` to a controlled slide rId, renumbers
  the cNvPr id +offset). Preserves drop-shadows / geometry that `deck_core.picture()`
  (a plain rect blipFill) would flatten. Pair with the module's `IMAGES` manifest.
- `_qa/regen_charts.sh` — records the exact extraction args per slide; deterministic
  rebuild. **Keepout lists = JM-callout ids + real-pic ids.**

**Gotcha worth remembering:** `extract_chart.py` chart-mode keeps `pic` shapes
(`pic` ∈ `SHAPE_TAGS`), so a slide's real pics get transcribed *with their source
`r:embed`* — dangling, since we renumber. Fix: `--keepout` the pic ids in the
chart-shape pass too, so pics come *only* from `extract_pics` with remapped embeds.
The first regen run flagged exactly this (dangling-ref counts 1/4/4/4 == the pic
counts on slides 1/2/4/5); adding the pic ids to keepout zeroed them.

JM-callout keepout ids (also the index in `JM_style_notes.md`): s1 9,10,11,12,13,
14,17,19,21,22,30,31,32,35 · s2 9,11,12,13,14,15,16,18,19,20 · s3 3,7,9 · s4 8,9,
10,11,12,13,14,15,16,17 · s5 3,5,8,11.

---

## QA / done-ness

- **Build green:** `wrote …_vS.pptx (5 slides, 4 charts)`.
- **All 5 slides visually verified** against `_qa/src_png/` (rendered via `render.sh`):
  bridge bars + lever table + flag (1), dual column charts + circled data rows +
  4 operator logos (2), stacked column + SHIPS Act table + focal callout + dashed
  leaders (3), opex table + shadowed source images + MSC callout (4), full
  bottom-to-top SCF flow with flags + labeled connectors (5). All purple `JM:`
  callouts gone.
- **Built-package integrity (zip dump):** 0 live `<a:fld>`, 0 `JM:` residue, 0
  think-cell residue, 0 `stCxn`/`endCxn` glue, 0 `schemeClr+lumOff`; every slide's
  rels resolve (no dangling r:id/embed); all 4 charts carry re-added
  `<c:externalData>` pointing at a real `.xlsb` embedding. Round-trips through
  soffice without repair (OPC content-type guard passed; jpeg/png/emf all declared
  defaults).
- Same media file across multiple rIds is fine (slide 5's US flag image6.png ×3):
  media is keyed by filename in the parts dict, so one part, three rels.

---

## Surgical style-system reconciliation (deliverable 2)

The house style is stated in **two parallel files** — `deck_core/slide_guide.md`
and `target_copy.txt` (workspace root, the cited "source of truth") — so a
consistent edit touches both. All edits are **permissive** ("acceptable
alternative", "typically"), never a new mandate. No code defaults changed → the
existing shipbuilding/MRO decks are untouched.

| Item | Change | Spots |
|---|---|---|
| Connector width | "…**typically ¼–½ pt** for flow/leader/divider lines, stepping to 1 pt for emphasis; non-black needs a legend." (code default left at 1pt) | `slide_guide.md:198`, `target_copy.txt:121` |
| Table interior borders | appended "a light **½ pt `GRAY_5`** rule between body rows is an acceptable alternative where row separation aids reading" (additive; "avoid *heavy* interior grids / no verticals" kept) | `slide_guide.md:145`, `target_copy.txt:76` |
| `Note:`/`Summary:` ban | **scoped** to body/commentary/exhibit text; **footnote line exempted** (it does carry Note/Source labels). The real fix — the guide already self-contradicted, since its own `Sources:` line is a role label and MRO footers use `Note: … Source: …` | `slide_guide.md:246`, `target_copy.txt:170` |
| Sources line | dropped the `(1) …; (2) …` parenthetical numbering → semicolon-separated, pipe to combine a Note + Sources line, superscript-tie notes (not sources), hyperlink sources. (`target_copy.txt` never had the numbering; `sources_line()` takes a raw string and enforces nothing) | `slide_guide.md:318`, `primitives.py:905` docstring |
| Number hygiene (new line) | currency + magnitude + **dollar basis** (real → base year `$M, real 2025`; nominal → `$M, nominal`, in the units caption), `- -` for an explicit zero, round-at-half | `slide_guide.md:239` |

The number-hygiene example was refined after a first pass: JM's literal example
`'25E` carried an incidental **E (estimate)** marker unrelated to real-vs-nominal,
so the generic `$M, real 2025` / `$M, nominal` replaced it (the source deck's own
unit captions read `$M, '25E, …`).

**Deliberately left as reference, NOT pushed into the shared guide** (mandating
them would constrain agent creativity): circled data rows, on-bar segment-value
labels, largest-segment-at-bottom ordering, hashed upper-bound ranges, logo
parity, image drop-shadows, 1pt dashed content separators, hyperlinked sources.
These live verbatim in `deck_gso_JM/JM_style_notes.md`.

---

## Resume / extend

- Rebuild data: `cd projects/gso_JM_reference/deck_gso_JM/_qa && bash regen_charts.sh`,
  then `cd .. && python build_deck.py`, then `bash _qa/render.sh`.
- `deck_gso_JM/slides/__init__.py` `SLIDE_RENDERS` is the order/progress source of truth.
- The port is COMPLETE (5/5 slides, build green, visually verified, integrity clean)
  and the style reconciliation is applied. No open items.
