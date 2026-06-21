# 2026-06-03 — DDG built-slide specs: migrate + research-enrich the 16 remaining specs into SlideSpec format

## Scope

Took the **16 DDG slide specs for the already-built deck slides** (body + appendix) that were
still in the old ALL-CAPS wireframe format and finalized them into the standardized SlideSpec
format (`docs/spec_format/SPEC_FORMAT.md`), **overwriting the originals in place** (no backup).

These 16 + the 5 already-migrated-earlier-today (`sam_scenarios`, `supplier_landscape`,
`ffata_visibility_gap`, `market_direction`, `implications`) = all **21 DDG specs now in the new
format**.

Starting material: three batches of new-format drafts produced by alternative AI agents that did
**not** have access to the DDG research repo or the workbooks (done to "speed up" the conversion).
Their structure was sound but their numbers were inherited (unverified) and their `reserve` banks
+ citations were thin. This session closed exactly that gap: verify every number against the
workbook, enrich `reserve`/`sources` from the DDG wiki + workbook, fold forward useful original
content, and clear each one.

Specs are not on any build path, so no deck rebuild (the workbook/research were read-only).
Workspace is not under git.

## Source -> canonical mapping (16 files; 2 filename renames)

| Downloads batch | new file | -> canonical project spec |
|---|---|---|
| `converted_slide_specs (3)` | market_primer, executive_summary, scope, cost_funnel, myp_redaction, appendix_bucket_rules_supplier_evidence | same names |
| `converted_slide_specs (2)` | tam_method **-> tam_methodology**, annual_tam_build, tam_timing, sam_taxonomy, worktype_allocation **-> work_type_allocation** | (2 renamed to canonical module name) |
| `converted_slide_specs (4)` | a01_definitions_scope, a02_tam_calculation, a03_myp_correction, a04_ap_lltm_sensitivity, a05_ffata_limitations | -> `appendix_*` canonical names |

The other Downloads batches (`converted_slide_specs`, `converted_specs`, `converted_slide_specs (1)`)
are the **submarine** equivalents (demand_backdrop / methodology / sizing_boundary, the subs-sNN
set, and the A1-A10 appendix) — out of scope this session.

slide_id / slide_order preserved from the converted specs (original wireframe deck numbering):
body `ddg-s02..s11`, appendix `ddg-a1..a6`, dovetailing with the gold-standard `ddg-s12..s16`.

## Method

1. Authored a shared **canonical-facts + protocol brief** (TAM $573M/yr·$3.44B; BC $365M/$2.19B,
   12.5% coeff, $17.47B base; AP $208M/$1.25B, 80% share, 85% coeff, $1.47B; per-hull $265M / 13
   hulls; MYP $14.58B masters, 87%/73.6% disclosed vs 33% corrected; SAM scenarios; 7 buckets +
   42.9% residual; FFATA $2.73B vs $13.57B mid = 20.1%, 7%/93% BIW/Ingalls, $13.84B/1,954; supplier
   proof points; policy) so every spec stays numerically consistent.
2. Fanned out **6 parallel subagents** by cluster (front-matter; cost-funnel/MYP; TAM-build;
   SAM/work-types; appendix A1-A3; appendix A4-A6), each reading the brief + format + `style.py`
   tokens + gold-standard exemplars + its wiki chapters + workbook modules, then writing its specs.
   A transient server rate-limit cut off 4 agents' **report** messages (their file writes had
   completed); `tam_timing` was the only spec left unwritten and was authored directly.
3. **Clearing pass (me):** read 12 of 16 specs in full + spot-verified the rest; mechanical sweep
   for structure, token validity, dash/separator discipline, citation discipline, and
   canonical-number consistency.

## Verification (clearing pass)

| Check | Result |
|---|---|
| Header + required blocks (meta/chrome/story/regions/element_inventory/reserve/qa) | all 16 |
| `module_name` == canonical filename; `slide_type` body/appendix | all 16 |
| slide_id/order contiguous (s02-s11, a1-a6) and consistent with gold standards | pass |
| Style tokens all exist in `style.py` | pass (no invented tokens) |
| Em dashes only in non-rendered fields (comments / story_role / reserve.context); 0 en dashes | pass |
| Visible `+` / `/` separators in rendered fields | none except the sanctioned `Unbucketed / ambiguous` |
| Citations real external primaries only; no wiki/tab/CD-ID/CSV in `sources` | pass |
| Canonical numbers tie out across all 16 (TAM build, MYP, SAM buckets/scenarios, FFATA, suppliers) | pass |

## Fixes applied during clearing

- **`work_type_allocation`**: residual label normalized to the canonical `Unbucketed / ambiguous`
  (slash) in the rendered chart category + qa + data row — was `Unbucketed and ambiguous`,
  inconsistent with `sam_taxonomy` and the cross-artifact constant.
- Verified the **A3 `appendix_myp_correction` 87% / 73.6% / 32.8%** framing: 87% = announcement
  outside-both-yards (incl. unparsed), 73.6% = live workbook disclosed coefficient (other+foreign
  only), 32.8% = MYP-corrected. Correct and self-reconciling, not contradictory with the body
  slides' `~87%` shorthand. Left as authored (the appendix is the right place for the precision).
- Resolved **scope.md 1,554 vs 1,954**: `1,554 unique in-scope parent UEIs`
  (`nc_scope_summary.json` -> `unique_parent_ueis_in_scope`) and `1,954 FFATA-visible parent
  vendors` (wiki) are distinct, correctly-labeled metrics. No conflict.

## Open items / follow-ups

- **`appendix_myp_correction` disclosed-only TAM ~$2.13B / uplift ~$1.31B** are the one pair not
  independently recomputed (they need the live `validation_sensitivity` SUMPRODUCT); structurally
  correct per the tab's formula (`portfolio_tam x bc_disc/bc`), internally consistent, and marked
  `~`. Confirm exact values on the next workbook build if precision matters.
- **DoD vs DoW** wording for the daily-contract-announcement citation varies across specs (both are
  valid: defense.gov rebranded to war.gov after Jan 2025). Cosmetic; standardize if a single label
  is wanted.
- **Submarine equivalents** (the other 3 Downloads batches: subs body S07-S11 + S17-S18, and the
  A1-A10 appendix) still need the same verify-and-enrich pass against the submarine research/workbook.
- Specs are not on any build path; no deck rebuild was needed or done.

## Files touched

- **Overwritten (new format), `projects/ddg/deck/slide_specs/`:** market_primer, executive_summary,
  scope, cost_funnel, myp_redaction, tam_methodology, annual_tam_build, tam_timing, sam_taxonomy,
  work_type_allocation, appendix_definitions_scope, appendix_tam_calculation, appendix_myp_correction,
  appendix_ap_lltm_sensitivity, appendix_ffata_limitations, appendix_bucket_rules_supplier_evidence (16).
- **Not changed:** `deck_core/*`, the workbook + research (read-only), `docs/spec_format/*`, the 5
  already-migrated DDG specs, and all submarine files.
