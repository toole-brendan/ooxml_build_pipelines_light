# 2026-06-15 — Outsourcing Ceiling workbook (research-agenda items 1 + 2)

Pipeline: `projects/distributed_shipbuilding/workbook_outsourcing_ceiling/`
Output:   `projects/distributed_shipbuilding/20260615_Distributed Shipbuilding Outsourcing Ceiling_vS.xlsx`
Build:    `python3.12 build_ceiling_base.py` → `python3.12 build_workbook.py` → `python3.12 validate_workbook.py`

## Goal

Answer the colleague's open question (`research_agenda_20260611.md` **item 1**:
penetration ceiling; **item 2**: hours→dollars bridge — item 3 became the award-
analysis workbook): **what is the theoretical ceiling on *future* outsourcing $
of new-construction work, if the irreducible prime-yard core is final assembly +
integration + test?** The model's only ceiling today is a flat, unsourced ×1.30
intent uplift; the user wanted it replaced with a structural, sourced one — and
the analysis built into a NEW stand-alone workbook (not award_analysis, which is
descriptive-only over the subaward corpus).

## Feasibility verdict (the discussion that preceded the build)

- **"Final assembly & test" is not a line anywhere.** SCN P-5c stops at a single
  monolithic `Basic Construction/Conversion` line; the L/M split is confirmed
  absent by the DoD FMR (canonical exhibit) and by GD/HII 10-Ks (categories, no
  ratio). The repo already had this as a `NOT FOUND` placeholder (industry claim 26).
- **POP can't be the ceiling** (user's correction): the announced place-of-
  performance off-team share (Va 34% / Col 22%) is *current* outsourcing — using
  it as the ceiling assumes away the growth being sized. POP is repurposed as the
  **floor/basis**; the ceiling needs the irreducible-core anchor.
- So the ceiling is necessarily **parameterized**: budget supplies the BC base;
  one sourced assumption supplies the never-outsourced core. Two new web pulls
  (Perplexity, then primary-source verified) gave the parameters.

## Verified anchors (4 citable + 2 POP; junk discarded)

Captured verbatim and URL-verified this session (saved into `wb_anchors.csv`):
- **A1 — h ≈ 0.50** of submarine construction **labor hours** can leave the prime
  yard. RADM Jon Rucker (PEO Attack Submarines), Defense News 2022-10-21: EB 1.1M
  + NNS 0.9M hrs/yr → 5M = "half the work to build a Virginia submarine". A
  forward capacity-relief **target on an hours basis**, not a make/buy split. The
  2M→5M ramp implies current ~20% → ~50% of hours = **2.5×**, so the ×1.30 ceiling
  is too low.
- **A2 — L ≈ 0.40** shipyard labor share. O'Rourke (CRS), HASC testimony
  2025-03-11: "shipyard labor can account for roughly 40% of a military ship's
  total procurement cost." Denominator = **total procurement incl. GFE**, so
  labor's share of *BC* is higher → defaulted L=0.50 for the nuclear boats.
- **A3 — L cross-check 0.39–0.48.** CBO Shipbuilding Composite Index (Apr 2024):
  shipbuilder labor was almost half of the index 2006–2022, declining 48%→39%.
- **A4 — BC is one regulated line.** DoD FMR 7000.14-R Vol 2B Ch 4, Exhibit P-5
  Ship Cost Element Categories — the labor/material split is not in the budget.
- **A5/A6 — current off-team POP** Va 34% (Block V) / Col 22% (Build I); DDG ~13%
  (BIW 20% / Ingalls 9% blended).
- **Discarded:** youtube/reddit/getvergo/facebook "sources"; the "$1.85B Korea/
  Japan feasibility study" (smells garbled); the labor-only ~20%-of-BC reading
  (right number for "prime-yard labor that relocates," wrong denominator for a
  supplier-opportunity TAM, which counts pass-through material).

## The model

Identity, per class, as a share of Basic Construction:
`core = L·(1−h)` (irreducible prime-yard work) and `ceiling = 1 − core`.
Hours→dollars bridge: `outsourced $ = h·L·BC + p·M·BC`, `M = 1−L` — labor-only
(p=0 ≈ h·L ≈ 25% of BC) up to material-inclusive (p=1 ≈ ceiling). For a supplier
TAM, p is high. Defaults: subs h=0.50/L=0.50; **DDG h=0.55/L=0.45** (analyst
assumption, no reactor → lower core; not the Rucker figure); p=0.50.

**Headline (independently recomputed from the CSV; Excel recalcs on open):**

| | BC $M (FY22-27) | core % | ceiling % | ceiling $M | headroom × |
|---|--:|--:|--:|--:|--:|
| Virginia | 36,277 | 25.0% | 75.0% | 27,208 | 2.2× |
| Columbia | 20,370 | 25.0% | 75.0% | 15,277 | 3.4× |
| DDG-51 | 17,471 | 20.2% | 79.8% | 13,933 | 6.1× |
| **Portfolio** | **74,118** | **23.9%** | **76.1%** | **56,418** | **3.0×** |

The sub-vs-DDG punchline: the nuclear boats carry the higher irreducible core
(25% vs 20%). Lead frame = **POP/distributed** (ceiling vs current off-team work);
make/buy (50/60/65% band) shown as a reference footnote on Headroom (it overstates
contestable headroom — much bought-out material is sole-source-locked).

## Workbook (9 tabs, mirrors the award_analysis pipeline architecture)

summary → inputs → model → data → validation → sources:
- **Summary** (answer page; all green links), **Assumptions** (single edit surface:
  per-class h/L, p, POP, make/buy band — every blue input carries its sourced
  basis as a hover note), **Ceiling Model** (core/ceiling per class+portfolio),
  **Conversion Bridge** (the h·L+p·M walk), **Headroom** (current→ceiling→×, FFATA
  floor + make/buy footnote), **Cost Base** (native table, blue P-5c leaves),
  **Sensitivity** (ceiling=f(L,h) grid + p sweep), **Tie-Outs** (hidden oracle),
  **Sources** (Anchors native table + sourced-vs-assumed ledger + frame).
- Data: `build_ceiling_base.py` unions the subs (`cost_funnel_with_subawards.csv`,
  `gfe_sum_$M`) and DDG (`cost_funnel_summary.csv`, `gfe_elec_ord_$M`) funnels into
  `wb_cost_base.csv` (15 award-year rows, FY22-27) + `wb_anchors.csv` (6 cites).

## Verification

- Build green: **0 xml errors, 0 error-literal cells, 9 sheets, 2 native tables**
  (`CostBase`, `Anchors`; both `autoFilter == ref`), Tie-Outs hidden.
- **Font-color audit:** blue only on Assumptions/Cost Base/Sensitivity inputs;
  every derived cell black; cross-sheet refs green — no hardcoded ratios.
- **Tie-Outs read OK** all three programs: core$+ceiling$=BC$, core%+ceiling%=1,
  ceiling%≥POP%, ceiling$≥FFATA-visible floor.
- Independent recompute from `wb_cost_base.csv` matches the headline above.

## Two post-build tweaks (user)

- Renamed sheet 1 `Overview` → **`Summary`** (pure consumer; nothing links in).
- Added the **`x` gutter collapse-anchor** (`mark_collapsible=True`) to every `§`
  section banner on all 9 sheets (19 markers), and `outline_level=1` to the two
  native-table bodies (Cost Base, Sources §1) that lacked it — matching the
  sibling convention (banner gets the `x`; data rows collapse; header/total stay).

## State / open items

- **Stand-alone only (deliberate).** The ×1.30 intent uplift in
  `submarines|ddg/.../inputs_assumptions.py §9` and
  `deck_mini_v2/.../penetration_outlook.py` is **untouched** — wiring those to
  consume this workbook's ceiling is a future pass (noted on the Sources tab).
- **DDG h/L are analyst assumptions** (no Rucker-equivalent submarine figure);
  the L=40% anchor is "of total procurement," so L-of-BC is judgment (defaulted
  0.50 subs / 0.45 DDG). Sweep them on Sensitivity.
- Basis is **then-year $M** (P-5c as reported), not constant FY2026 like the
  sub/ddg workbooks — ratios are unit-invariant, the $ are illustrative of
  magnitude. Re-run `build_ceiling_base.py` after a cost-funnel refresh.

## Files

New pipeline `projects/distributed_shipbuilding/workbook_outsourcing_ceiling/`:
`build_workbook.py`, `validate_workbook.py`, `build_ceiling_base.py`,
`workbook_outsourcing_ceiling/{__init__,lib}.py`,
`workbook_outsourcing_ceiling/sheets/{__init__,_layout,_widths,summary_overview,
inputs_assumptions,model_ceiling,model_bridge,model_headroom,data_cost_base,
validation_sensitivity,validation_tie_outs,sources_source_index}.py`,
`extracted/{wb_cost_base,wb_anchors}.csv`, and the built `…_vS.xlsx` at the
project root.
