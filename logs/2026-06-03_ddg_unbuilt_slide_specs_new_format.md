# 2026-06-03 — DDG unbuilt slide specs migrated to the new SlideSpec format

## Scope

Converted the **five DDG slide specs that have no slide module yet** from their old
ALL-CAPS wireframe template into the standardized **SlideSpec** format authored earlier
today (`docs/spec_format/SPEC_FORMAT.md`). The five are the deck backlog (slides 12–16):
`sam_scenarios`, `supplier_landscape`, `ffata_visibility_gap`, `market_direction`,
`implications`. Each original `.md` was **overwritten in place** with a new-format YAML
spec; the original narrative content was carried forward into the new structure (chiefly
the `reserve` density bank).

This is a **spec-authoring** task only: no `deck_core` changes, no slide modules built,
no deck rebuild (specs are not on any build path). Workspace is not under git, so the
safety net was a read-only engine/research pass + a structural verification sweep.

## 0. Decisions carried in from the user

- **Author fresh from the originals** — do **not** lean on the existing worked example
  `docs/spec_format/example_ddg_sam_scenarios.md` (unknown effort behind it). The example
  was left untouched as a format reference; the new `slide_specs/sam_scenarios.md` is an
  independent rebuild (own region layout, richer tie-outs, 10 reserve chips).
- **Read all of `deck_core/`** first — it is exactly what the future build agent reads, so
  the specs speak the engine's real vocabulary.
- **Mine the DDG mirrors for commentary** — `projects/ddg/research/wiki` (organized) and the
  finished workbook `projects/ddg/workbook/workbook_ddg` — for accurate, citable detail.
- **Do not touch the submarines specs** (a parallel agent is mid-migration; WIP).
- Earlier in-session answers: **rebuild `sam_scenarios` fresh** (not adopt the example),
  **convert all five at once**, **overwrite in place**.

## 1. Engine read (grounding the vocabulary)

Read every `deck_core/` file so token/factory/region references are real, not guessed:
`style.py` (palette + type scale + insets + the BODY box + locked-chrome geometry),
`primitives.py` (`text_box` / `house_table` / `table` / `picture` / `connector` + the
breadcrumb/title/prelim/sources chrome builders), `charts.py`
(`bar_chart`/`column_chart`/`line_chart`/`waterfall_chart`/`marimekko_chart` + `graphic_frame`),
`text_metrics.py` (`estimate_row_heights`), `slide_base_template.py` (the
`_SECTION`/`_TOPIC`/`_TAKEAWAY`/`_SOURCES` + `LAYOUT`/`CHARTS`/`IMAGES` symbols),
`slide_guide.md`, `slide_snippets.md`.

## 2. Research fan-out (read-only)

Four parallel subagents mined the DDG wiki + workbook, one per slide cluster, returning
exact numbers with **internal tie-outs**, **real external citations**, supplier caveats,
and density-bank facts. Headline result: **every figure in the originals ties out exactly**
to the workbook (replayed over the source CSVs with default knobs). Key findings folded in:

- **Numbers confirmed:** the 5 scenario values (broad $327.3M/yr … HM&E $88.5M/yr, with
  cumulatives + % of TAM), portfolio TAM ~$573M/yr (~$3.44B; BC ~$365M + AP/LLTM ~$208M),
  per-hull ~$265M across 13 hulls, residual ~42.9%; the 10 parent-level supplier values; the
  CD10 gap band ($2,728.6M visible / $11,311.4 / $13,573.7 / $16,159.2M; 20.1% midpoint).
- **Build caveats discovered and encoded as guardrails:**
  - `supplier_landscape` must source the **Vendors tab** (parent-level
    `nc_lifetime_vendors.csv`), **not** `z_ChartData CD09` — CD09 is bucket-split, dollars
    are per-(vendor,bucket) exposure, and it drops GFE/prime-named firms. Duplicate filer
    UEIs (Major Tool, Rolls-Royce) need consolidation; "foreign" = incorporation, not work
    location; Arctic Slope / Advanced Sciences are services, not components.
  - `ffata_visibility_gap` 20.1% (cumulative cost-funnel) and ~15% (recent-rate
    segment-revenue) are **different bases — never on one axis**; visible flow is ~93%
    Ingalls / ~7% BIW (a filing-behavior artifact; Ingalls reports ~6× denser; BIW's FY23-27
    master shows zero filings).
  - `market_direction` `CD11_OUTSOURCING_INDEX` is a **qualitative shape-table, not a numeric
    index** (never fabricate one); GD's "supply chain is the gating item" was said in an
    **Electric Boat / submarine** context, not BIW/DDG; HII's doubled/+30%/23-vendor figures
    are enterprise-wide (Ingalls + Newport News), not DDG-only; HII FY24 Q3 call was
    **Oct 31 2024** (the wiki's "November" is wrong).
  - `implications` confidence/qualification/priority are **deck judgment**, not
    workbook-computed (SD12 literally says "set in deck").

## 3. Per-slide conversion

All five carry the full required schema (`meta`, `chrome`, `story`, `regions`,
`element_inventory`, `charts`, `tables`, `commentary` incl. **mandatory `reserve`**, `qa`),
the closed BODY-relative region grammar, an `element_inventory` spine, and exact real
citations in `chrome.sources` + `source_line_exact`.

| Spec (slide) | Exhibits | Notes |
|---|---|---|
| `sam_scenarios` (s12) | `bar_chart` (5 ranked scenarios) + `house_table` inclusion matrix (7×5) | required-if-present on BOTH chart and table |
| `supplier_landscape` (s13) | `bar_chart` (10 parent-level suppliers) + no-fill caveat rail; `tables: []` | Vendors-tab sourcing guardrail; CD09 warning |
| `ffata_visibility_gap` (s14) | `bar_chart` (visible vs low/mid/high band) + explanation rail + pointer-callout annotation; `tables: []` | 20.1% vs ~15% basis warning; BIW/Ingalls asymmetry |
| `market_direction` (s15) | **No chart** (`charts: []`) — evidence-timeline `house_table` (Period/Source/Signal/Implication) + interpretation rail | qualitative; GD-context + enterprise-vs-DDG caveats |
| `implications` (s16) | **No chart** (`charts: []`) — scorecard `house_table` (dark skin) + no-fill where-to-play/sizing note | confidence = deck judgment; no bubble chart |

Content mapping held throughout: `PURPOSE`→`story.objective`; `KEY VALUES`/chart contracts
→`charts`/`tables` + `data_and_calculations` (verbatim numbers, nothing invented);
`FOOTER SOURCE LINE`→`chrome.sources` + `source_line_exact`; `OBJECT PLACEMENT` %s→the
region grammar; `COMMENTARY NOTES` + `RESEARCH CONTEXT` + research findings→ample
`reserve.context` + 8–10 region-tagged `approved_extra_points`; `QA CHECKS`→`qa.guardrails`
+ the standard `engine_checks` battery.

## 4. House-style fix

Normalized em-dashes (` — ` → `, `) in the 12 `approved_extra_points` **chip `body:`** lines
across the five files — those chips are drop-in slide copy, so they must follow the
no-em-dash rule. Internal `reserve.context` prose and YAML comments keep their em-dashes
(never rendered).

## Verification

| Check | Result |
|---|---|
| Files present / size | 5 specs, 256–309 lines each (matches example depth) |
| Required blocks present (`meta`…`qa`) | all 5 |
| `reserve` present (body-slide mandatory) | all 5 |
| `module_name` == filename (1:1) | all 5 |
| Tokens referenced vs `style.py` exports | all real (`BLUE_*`, `GRAY_*`, `DK`, `CHART_TITLE_10PT`, `LABEL_9PT`, `FINEPRINT_8_5PT`, `DENSE_BODY_10PT`, `INSETS_NONE/MESSAGE`); `GAP`/`NOTE_H`/`TITLE_BAND_H` are the format's region-grammar constants |
| Factories referenced | only `bar_chart`, `house_table`, `text_box` — all in `deck_core` |
| `chart_index: 0 -> rId2` | correct on the 3 chart slides; `charts: []` on the 2 table-only slides |
| Table column_widths / aligns / row cell counts | consistent (matrix 6 cols; timeline 4; scorecard 6) |
| Numbers vs workbook | every value ties out (research replay); no invented figures |
| Em-dashes in rendered-candidate fields | 0 after normalization |

## Files touched

- **Overwritten (new format):** `projects/ddg/deck/slide_specs/{sam_scenarios, supplier_landscape,
  ffata_visibility_gap, market_direction, implications}.md`
- **Not changed:** `deck_core/*` (read-only), the workbook + research (read-only),
  `docs/spec_format/*` (the example/standard left as-is), the other ~16 DDG specs (already
  built modules — out of scope), all submarines files.

## Open items / follow-ups

- **Specs still describe unbuilt slides.** Building the five `deck_ddg/slides/*.py` modules
  from these specs and wiring them into `slides/__init__.py` (slide order 12–16, before the
  appendix) is the next pass.
- **`example_ddg_sam_scenarios.md` now diverges** from the fresh `slide_specs/sam_scenarios.md`
  (independent layout, richer tie-outs, 10 chips). Both are valid; the example remains a
  format demonstration in `docs/spec_format/`. Reconcile only if a single canonical
  `sam_scenarios` spec is wanted.
- **Other DDG specs (~16) remain in the old format** — migrating the already-built ones is a
  separate, lower-priority pass.
- **Two long title findings** (`implications`, `sam_scenarios`) fit 2 lines at 20pt but are
  near the limit — flagged in each spec's `known_caveats`; the build agent should confirm
  against `slide_probe` once the module exists.
- **`ffata_visibility_gap` pointer-callout** needs `tip_x`/`tip_y` set in EMU after a probe
  pass (noted in the spec); it is classified as a chart annotation, not the editorial callout.
