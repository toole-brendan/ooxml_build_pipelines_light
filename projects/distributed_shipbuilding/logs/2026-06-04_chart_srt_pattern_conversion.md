# 2026-06-04 — Chart conversion: DDG + submarine decks adopt the Sea Range Telemetry chart pattern

## Scope

Converted the chart layer of **both decks** (`projects/ddg/deck`, `projects/submarines/deck`)
to the visual grammar of the *Sea Range Telemetry* (SRT) market-sizing deck (a think-cell deck
at `~/projects2/sea_range_telemetry/`): **vertical column family only, waterfall as the
signature for build-ups/derivations, horizontal bars reserved for supplier-name rankings**, and
the **SRT bar fill palette** (raw hex, per user direction — not the deck's `style.py` ramp).

Driven by `docs/chart_conversion_spec.md` (written first, then applied). **Content work only** —
slide modules + one slide spec; **no `deck_core` / `style.py` changes** (every target type was
already exposed by `column_chart` / `waterfall_chart`). Workspace is not under git / no backup,
so each deck was rebuilt green as the safety net.

User decisions carried in: **(a)** shorten long category labels to fit vertical columns;
**(b)** `sib_exclusion` → waterfall (not the table its spec described); **colors = the SRT
chart bars' exact hex**, inlined in the modules.

---

## The SRT bar palette (inlined hex)

Hero navy `#1D4D68` (the one focal color) · blue ramp `#486D82 → #89A2B0 → #AFC2CC → #D8E3EB`
· neutral blue-gray `#79838F` · grays `#A1A1A1 / #BEBEBE / #DBDBDB` (de-emphasis, waterfall
connectors). Ranked columns use `_SRT_RAMP = ["1D4D68","486D82","89A2B0","AFC2CC","D8E3EB"]`
(+ `BEBEBE`/`DBDBDB` tail for 7-8 cats). `gap_width=80`, `value_label_size_pt=10` on converted
columns; gridlines kept.

## DDG — 9 modules touched (10 charts → 9)

| Module | Change |
|---|---|
| `cost_funnel` | ranked bar → **decreasing waterfall** ($5,492M total ship → −GFE 1,807 → −other 363 → $3,322M Basic Construction); total navy, excluded steps gray |
| `ffata_visibility_gap` | clustered bar → **single-series column**; visible-flow bar hero navy, 3 outsourcing estimates neutral; labels shortened; wedge callout re-aimed at leftmost column |
| `work_type_allocation` | ranked bar → **ranked column**; residual gray, top named bucket hero navy + ramp; labels shortened |
| `sam_scenarios` | ranked bar → **ranked column**; SRT ramp; labels shortened |
| `myp_redaction` (×2) | both flipped to **vertical**: distribution = 100%-stacked column (Other-US supplier hero), comparison = stacked column (corrected navy / artifact gray); comparison labels shortened |
| `tam_timing` | recolor stacked column — AP/LLTM spike hero navy, BC stream mid blue |
| `annual_tam_build` | recolor waterfall to SRT palette |
| `supplier_landscape` | **kept horizontal** (10 supplier names); recolor only |
| `executive_summary` | **chart removed** (its slide-spec already had `charts: []`); `_chart_title` + frame deleted |

## Submarines — 9 modules touched (9 charts → 9)

| Module | Change |
|---|---|
| `sib_exclusion` | ranked bar → **additive exclusion waterfall** (BlueForge → +TMG → +IALR → Total excluded); steps/total gray-neutral (excluded ≠ hero TAM) — **decision (b)** |
| `bucket_tam` | ranked bar → **ranked column**; SRT ramp + gray tail; labels shortened |
| `sam_scenarios` | ranked bar → **ranked column**; SRT ramp; labels shortened |
| `coefficient_evidence` | ranked bar → **ranked column** (applied coeff hero, evidence views neutral); labels shortened; 2 bar-annotations repositioned above their columns |
| `appendix_coefficient_sensitivity` | ranked bar → **ranked column**; same color logic; labels shortened (caption already below chart) |
| `basic_construction` | recolor stacked column — Virginia hero navy, Columbia slate |
| `annual_cadence` | recolor clustered column — Broad SAM (addressable) hero navy, TAM neutral |
| `ap_and_lltm` | recolor waterfall to SRT palette |
| `visible_suppliers` | **kept horizontal** (10 supplier names); recolor only |

---

## Verification

| Check | DDG | Submarines |
|---|---|---|
| `build_deck.py` | green — **25 slides, 9 charts** | green — **27 slides, 9 charts** |
| emitted chart orientation | 8 `barDir=col` + 1 `bar` (suppliers) | 8 `barDir=col` + 1 `bar` (suppliers) |
| waterfalls (col/stacked, 4-series) | 2 (`annual_tam_build`, `cost_funnel`) | 2 (`ap_and_lltm`, `sib_exclusion`) |
| hero navy `#1D4D68` present | 8/9 charts (sib intentionally gray-only) | n/a |
| residual `bar_chart` callers | only `supplier_landscape` (intended) | only `visible_suppliers` (intended) |
| dangling `bar_chart` imports | none | none |
| `sib_exclusion.md` spec | — | re-authored to waterfall; **YAML parses** |

## Files touched

- **DDG slide modules (9):** `cost_funnel`, `ffata_visibility_gap`, `work_type_allocation`,
  `sam_scenarios`, `myp_redaction`, `tam_timing`, `annual_tam_build`, `supplier_landscape`,
  `executive_summary`.
- **Submarine slide modules (9):** `sib_exclusion`, `bucket_tam`, `sam_scenarios`,
  `coefficient_evidence`, `appendix_coefficient_sensitivity`, `basic_construction`,
  `annual_cadence`, `ap_and_lltm`, `visible_suppliers`.
- **Specs:** `submarines/.../slide_specs/sib_exclusion.md` (charts:[] → waterfall; ledger table
  marked superseded). `docs/chart_conversion_spec.md` (added §7 as-built).
- **Rebuilt:** both `.pptx` outputs. **Not touched:** `deck_core/*`, `style.py`, README,
  workbooks, all other slide specs.

## Open items / follow-ups

- **Visual review in PowerPoint (orientation flips moved hand-tuned geometry):**
  `ffata_visibility_gap` wedge-callout tip; `coefficient_evidence` two bar-annotation captions;
  `myp_redaction` distribution (single 100%-stacked column in a wide-short frame — chunky).
  Builds are green and XML valid; only on-slide positioning is unverified (no renderer here).
- **Spec reconciliation (NOT done — 15 specs):** every `slide_specs/*.md` carries a full
  `charts:` mirror (factory / categories / colors / params). 15 still describe the *old* chart
  (`bar_chart`, old labels, `BLUE_*`). Mechanical mirror pass needed; only `sib_exclusion.md`
  reconciled here (it contradicted decision b). A parallel per-file pass would close this.
- **Unused `style.py` imports** left in several converted modules (the old `BLUE_*`/`GRAY_*`
  chart-color tokens). Harmless at runtime; a cleanup pass could prune them.
- **`#1D4D68` etc. are inlined hex** per user direction (bypasses `style.py` tokens). Making
  them named tokens would be a `style.py` (core) change — deferred, needs sign-off.
- **Audit gates / values unchanged:** no data values were altered (only chart type, color,
  labels, and `executive_summary` chart removal).
