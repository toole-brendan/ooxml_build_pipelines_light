# 2026-06-04 — Workbook banner-fill widths + visible-text LLM-ism scrub (both decks)

## Scope

Acted on an in-depth styling assessment of both workbooks (`workbook_core` guidance vs
the per-tab sheet modules). Two problem classes, fixed across **29 sheet modules** (18
submarines + 11 DDG). **No `workbook_core` changes; no formula/value/row edits** — only
banner `n_cols`, two DDG `cols` lengths, one total-row width, and visible-text strings.
Both workbooks build green throughout; workspace is not under git, so each workbook was
rebuilt after editing as the safety net.

The diagnosis split cleanly: **DDG was largely clean; submarines was the offender** on
both axes — exactly the user's read.

---

## 1. Banner fills running too long / too short

`banner_row(n_cols=N, with_gutter=True)` fills columns B..N, so a full-content-width
banner needs `N == len(cols)`. The guide treats banners as chrome spanning the full
content width (explicit for the title banner; the `banner_row` docstring and every
snippet use `len(COLS)`).

**Root divergence:** DDG sets one `_NCOLS = len(cols)` and reuses it for every banner
(clean right edge). Submarines sized each section banner to *its own block*
(`n_cols=2/3/4/7…`), giving a ragged right edge on nearly every multi-width sheet. Fix =
make every banner full content width.

Measured from emitted XML (render → count title-styled cells per row vs content width).
After the fix **every sheet has `declared == banner_max == data_max`** (44/44).

Fixes:
- **Submarines (9 sheets ragged):** `model_tam_build` (§3 group 3→7), `model_sam_build`
  (all → 7), `data_ap_bridge` (§4/§5 3→14), `data_entity_master` (§3/§4/§5 3→9),
  `inputs_assumptions` (§4/§5/§6 → 7), `data_scn_budget` (ship sections 7→8),
  `outputs_figure_register` (6→7), `sources_references` (§2 8→9).
- **DDG (1 sheet ragged):** `model_sam_build` `_NCOLS` 5→8 (title + §1–§4 were stuck at
  the 5-wide scenario block while §5 annual + cols were 8; the **title banner itself
  violated the explicit full-width rule**).

**Two real bugs (not just aesthetics):**
- **subs `model_sam_build`** — §8 annual block (`n_cols = 2 + len(_SCEN_KEYS) = 7`) wrote
  into **column 7, which `cols=[…6 widths…]` never declared**. Added the 7th width and a
  module `_NCOLS = 2 + len(_SCEN_KEYS)` used by every banner.
- **subs `validation_sensitivity`** — §2b used `n_cols=4` on a **2-column sheet**, painting
  fill two columns past all data. → `n_cols=2`.

**Over-provisioned columns (DDG, gray bar overran empty cols):**
- `validation_scope_exclusions` — declared 6, real data reaches col D. Trimmed
  `cols` 6→3, `_NCOLS` 6→3, the subtotal `total_row` `n_cols` 4→3.
- `guide_methodology` — declared 6, data reaches col F. Trimmed `cols` 6→5, `_NCOLS` 6→5.

Total-row `n_cols` were **left at block width** everywhere else (a subtotal divider spans
its table, not the sheet — correct, and distinct from the banner-fill rule).

## 2. Visible-text LLM-isms

Scrubbed against the guide's "Human workbook standard" (no self-reference, short
noun-phrase banners, no meta/role labels). All categories now grep-clean.

- **Self-referential headers:** subs `guide_methodology` glossary header
  `"Workbook treatment"` → `"Treatment"`; DDG `sources_references`
  `"Workbook methodology + spec (internal)"` → `"Methodology + model spec (internal)"`.
- **"§1 - At a glance:" tic** (submarines opened **14/20** sheets with it; DDG 2): dropped
  the prefix on all 16, e.g. `§1 - At a glance: headline TAM` → `§1 - Headline TAM`. (Two
  leftover hits are source code comments, not emitted text — retitled for tidiness.)
- **Meta-instructions / imperative directives:** `NEVER present the 87%`,
  `DO NOT HEADLINE`, `never hardcoded`, `ALWAYS travel…`, `(editable on Inputs)`,
  `(linked from Inputs/Assumptions/TAM Build)`, `(not a formula)` → removed or reworded to
  lower-case declarative analyst voice (the substantive MYP-artifact caveat is kept once,
  in the existing native notes, not shouted across banners and cells).
- **Build-process leakage:** subs `model_tam_build` §3e
  `(reproduce the v4 worked example; drift guard)` → `§3e - Anchor regression`; subs
  `sources_source_index` `(… superseded by Phase-3)` / `SUPERSEDES v5 …` / version-tag
  labels → declarative + clean doc titles (real file paths kept in the path column); DDG
  `(Phase 3)` / `(the Phase-2 gate…)` → dropped.
- **Formulas in banners → noun phrases:** `§5a - TAM by FY ($M) = BC_base x BC_coeff + …`
  → `§5a - TAM by FY ($M)`; `§6 - Scenario SAM = SUMPRODUCT(…)` → `§6 - Scenario SAM`;
  `§4 - TAM bridge (TAM = …)` → `§4 - TAM bridge`; `§2 - TAM-base derivation (CY AP x …)` →
  `§2 - TAM-base derivation`; the two `Annual SAM by fiscal year (… x …)` glosses on both
  decks → trimmed to match.

Legitimate analyst parentheticals were **kept** (e.g. `($M, FY22-27)`, `(not
supplier-addressable)`, `(appendix)`, `(1 = include)`, `(top N by $)`); only meta /
formula / provenance / tic content was removed. Methodology *body* prose that states the
model's formulas was kept (it is a methodology sheet).

---

## Verification

| Check | Result |
|---|---|
| DDG `build_workbook.py` | green — 24 tabs, 11 native tables, 6 note parts |
| DDG `validate_workbook.py` | 70 parts, **0 xml errors**, 24 sheets, **0 error-literal cells** |
| Submarines `build_workbook.py` | green — 20 tabs, 10 native tables, 8 note parts |
| Banner span audit (render-truth) | **44/44 sheets `declared == banner_max == data_max`**; 0 too-short / too-long / ragged |
| `At a glance` in emitted text | 0 (2 residual are source comments) |
| `Workbook treatment` / `Workbook methodology` | 0 |
| `NEVER/DO NOT/ALWAYS/never present/never hardcoded/editable on Inputs` | 0 |
| `Phase-N` / `SUPERSEDES` / `drift guard` / `reproduce the v4` in emitted text | 0 |
| Formula-equation banners (`= SUMPRODUCT`, `= BC_base`, `TAM = …`) | 0 |

## Files touched

- **Submarines (18):** `model_tam_build`, `model_sam_build`, `data_ap_bridge`,
  `data_entity_master`, `inputs_assumptions`, `data_scn_budget`, `outputs_figure_register`,
  `validation_sensitivity`, `sources_references`, `guide_methodology`,
  `sources_source_index`, `data_location_master`, `data_pop_corpus`,
  `validation_qa_reconciliation`, `validation_number_audit`, `validation_sib_excluded`,
  `data_worktype_evidence`, `validation_pop_source_audit`.
- **DDG (11):** `model_sam_build`, `model_tam_build`, `guide_methodology`,
  `validation_scope_exclusions`, `chartdata_z_chart_data`, `outputs_figure_register`,
  `summary_executive_summary`, `validation_sensitivity`, `validation_qa_reconciliation`,
  `sources_references`, `data_ap_bridge`.
- No `workbook_core`, README, or build-script changes.

## Open items / follow-ups

- **Core hardening (not done — would be a `workbook_core` change, needs sign-off):**
  the guide only *implies* section banners are full-width (explicit only for the title) —
  worth stating outright; and a `sheet_probe` lint for `banner span == content width`
  would catch this whole class mechanically going forward. Offered, not applied.
- **Left as legitimate analyst voice:** the longer-but-real descriptive parentheticals on
  some banners (e.g. DDG SAM Build §2a). Trim further only if a terser house form is wanted.
- **Stale tab-name reference spotted, out of scope:** subs `sources_source_index` data
  note `"… (SCN Annual)"` still uses the pre-rename tab name (now `SCN Budget`). Not an
  LLM-ism; flag if a correctness sweep is wanted.
- **Audit gates** (QA Reconciliation / Number Audit "0 FAIL") are runtime Excel formulas —
  not evaluated here; this session changed no formula/value, and DDG validate shows 0
  error-literal cells, so they should be unaffected. Confirm in Excel for final sign-off.
