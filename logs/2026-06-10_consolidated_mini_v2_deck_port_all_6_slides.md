# 2026-06-10 — Consolidated mini-v2 deck port (v2.0 slides 1–6 → deck_mini_v2)

## Goal

Port ALL 6 slides of `projects/consolidated/20260605_Defense Demand Drivers New
Construction_v2.0.pptx` 1:1, faithfully, into a NEW pipeline at
`projects/consolidated/deck_mini_v2/`, repeating the same-day deck_mini port
methodology (`docs/faithful_deck_port_methodology.md`). Output:
`projects/consolidated/20260610_New Construction Methodology Mini_v2.pptx`.

Final state: **6 slides, 5 native chart parts, build green on the FIRST
build**, all six renders visually verified against the source side-by-side,
and all validation greps zero (`<a:fld>` / `r:id`/`r:embed` / `stCxn|endCxn` /
`lumOff` / think-cell residue across `_chart_xml/`; built pptx re-checked via
zip dump: no live fields, no dangling rels, externalData stripped from every
chart part).

## The source (what v2.0 is)

The v2.0 deck is the cleaned, restated successor of the vDraft the deck_mini
port covered — same pipeline-baked chrome idiom (`Breadcrumb`, `PrelimChip`,
`Title`, `StepLabel`, …), draft chips/highlights removed, numbers reflecting
the same-day restates (DDG $6.4B portfolio TAM, subs $18.1B, per-class
penetration strips) — PLUS two new working placeholder slides:

| build # | module | content | parts |
|---|---|---|---|
| 1 | `outsourced_bc_walk` | total-ship-spend → outsourced-BC walk, DDG + sub | chart1+chart2, tables 14,50 |
| 2 | `worktype_by_program` | work-type split, ~$18.1B sub vs ~$6.4B DDG pools | chart3, table 6 |
| 3 | `outsourced_bc_annual_tam` | annual TAM FY22–31 + Va/Col/DDG penetration strips | chart4, table 154 |
| 4 | `penetration_outlook_placeholder` | gray placeholder box (intended line chart spec) | shapes only |
| 5 | `worktype_by_fy` | work-type mix stacked bars per class | chart5 |
| 6 | `contracts_outlook_placeholder` | gray placeholder OVER a templated contracts table + budget-alignment legend chips | table 13 |

All six on `slideLayout4` (Light Blank); theme byte-identical to
`infra/template`; layout4 differs only by the hidden think-cell "Do not
remove" tag shape (cosmetic) — the layout map is the identity, exactly as in
the deck_mini port.

## How (same playbook, zero fix passes, ~15 min)

- Tooling copied verbatim from `deck_mini/_qa/` (`dump_slide.py`,
  `extract_chart.py`) — all cleaning rules pre-paid.
- The charts are the same vintage as the vDraft's: REAL native `<c:chart>`
  parts whose only relationship is `<c:externalData>` → embedded .xlsb. Strip
  it, bundle verbatim via `CHARTS=[{"chart_xml": ...}]`, place with
  `graphic_frame()` at the source frame xfrm. No chartSpace-level `spPr`
  exists on any of them (same as vDraft — regroup-safe, proven by deck_mini's
  renders).
- Transcribe EVERYTHING, no `--keepout` — chrome included.
- `_qa/regen_charts.sh` records every extraction arg; module body pattern is
  `_TABLES + graphic_frame(s) + _SHAPES`.
- Slide 6 z-order note: the contracts table and legend chips sit UNDER the
  gray placeholder box in the source; emitting `_TABLES + _SHAPES` preserves
  that (the placeholder is last among the transcribed shapes). Verified in the
  render (box covers the table) and in the built XML (table + "Recompete
  Date" strings present in slide6.xml).

## Pipeline layout (mirrors deck_mini exactly)

```
projects/consolidated/deck_mini_v2/
  build_deck.py
  deck_mini_v2/
    __init__.py  lib.py             # OUT = 20260610_New Construction Methodology Mini_v2.pptx
    slides/
      __init__.py                   # SLIDE_RENDERS, 6 modules in deck order
      outsourced_bc_walk.py  worktype_by_program.py  outsourced_bc_annual_tam.py
      penetration_outlook_placeholder.py  worktype_by_fy.py  contracts_outlook_placeholder.py
      _chart_xml/                   # 16 files: slide0N.xml / _tables.xml / _chartK.xml
  _qa/
    dump_slide.py extract_chart.py  # verbatim from deck_mini/_qa
    render.sh regen_charts.sh
    src_xml/  src_png/src-{1..6}.png  png/
```

## Resume / regenerate

```bash
cd projects/consolidated/deck_mini_v2
/usr/bin/python3 build_deck.py        # green = "wrote … 6 slides, 5 charts"
bash _qa/regen_charts.sh              # rebuild every _chart_xml/ data file
rm -f _qa/png/*.pdf && bash _qa/render.sh
# compare _qa/png/slide-N.png vs _qa/src_png/src-N.png   (1:1, same numbering)
```

## Cross-references

- Same-day predecessor port: `logs/2026-06-10_consolidated_mini_deck_port_slides2-5.md`
  (deck_mini; explains why this playbook is fast).
- Methodology: `docs/faithful_deck_port_methodology.md`.
- MRO port logs: `logs/2026-06-08_mro_deck_native_port.md`,
  `logs/2026-06-08_mro_deck_static_thinkcell_charts_and_completion.md`.
