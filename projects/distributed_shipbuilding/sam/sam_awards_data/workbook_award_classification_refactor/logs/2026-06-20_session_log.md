# 2026-06-20 - Session log (award_classification_refactor)

Narrative log for the whole session. Two deep pieces of work got their own topic logs and are
only summarized here:
- `2026-06-20_hull_builder_only_scope_standardization.md`
- `2026-06-20_archetype_mece_revision.md` (incl. the D9 functional-domain push addendum)

Build stayed green the whole way (12 sheets, 10 native tables, 6 note parts, 0 XML errors,
0 error-literal cells, no repair). All dollar figures nominal unless noted.

---

## How the session started vs. where it went

Started by picking up the prior handoff
(`2026-06-20_naics_crosswalk_sheet_and_override_first_archetype_wiring.md`), whose only open item
was **§8 - Phase 4, constant-FY2026 dollars**. That turned out NOT to be the work that got done:
investigating it surfaced a blocker, and the user then re-scoped toward data-quality questions
(comparability of the archetype cuts) that became the real session.

## Thread 1 - Constant-FY2026 dollars (investigated, then PUT ON HOLD)

- The handoff assumed `workbook_core.deflators` could just be reused. It can't: that series is
  **FY2022-2031**, but the subaward data runs **CY2013-2026** - **53% of the dollars ($6.94B of
  $13.17B) are pre-2022** with no factor. No historical series exists anywhere in the repo.
- Fix path identified: back-extend from the **FY2025 Green Book Table 5-4 Procurement column**
  (the same source/edition as the existing values; user has the PDF at `~/Downloads/fy25_Green_
  Book.pdf`), kept project-local (not mutating shared `workbook_core`).
- User answered the two pending decisions (FY price-year basis; Green Book back-extend) **but then
  reconsidered whether the standardization is even needed**. **Status: ON HOLD** - nothing built.
  If resumed: FY basis, project-local back-extended series, per-tx constant-$ column ->
  `Subaward $M (2026)` via SUMIFS; watch the CY->FY caption migration.

## Thread 2 - Are the archetype % breakdowns comparable? (the real session)

Trigger: the user suspected the D/P shares were distorted by the raw-pull filters, and flagged the
DDG-vs-submarine propulsion asymmetry. Investigation findings:

1. **`role`/`bucket` are NOT raw data** (verified): the FSRS record has no such field. They are a
   derived overlay = a 169-row hand registry (`vendor_evidence_registry.csv`, itself largely
   NAICS/SAM-based, **0 source URLs**, ~13-15% UEI coverage though ~75-85% of dollars) + a
   mechanical `classify(name, naics4)` fallback. **Decided NOT to use the overlay as the scope
   lever** - the reliable lever is the raw **prime group** (`bgroup`).
2. **The two programs used different cost-funnel denominators** (submarine wiki ch01): DDG pulled
   hull-builders only (Basic Construction); submarines pulled BC **+ the GFE primes** (BPMI
   reactor, LM, BAE, RR). So GFE/nuclear was IN for subs, OUT for DDG - the opposite of the
   initial Bechtel hypothesis, and the real cause of the non-comparable shares.
3. **HII-NNS is invisible in the subaward stream** (the "Newport News gap"): ~50% Virginia /
   ~22% Columbia construction flows through GDEB as vendor of record - only ~$98M shows on
   Virginia, **$0 on Columbia**. Not fixable from this data; understates submarine D1/P5.

## What got built (the three approved increments)

1. **Hull-builder-only standardization** (Thread 2 -> fix). Filter to the hull-construction prime
   (subs = GDEB; DDG already its two builders) in the 3 corpus-derived build scripts, NOT in
   shared `_corpus`. Columbia -$674M (BPMI), Virginia -$6.5M, DDG unchanged; workbook ~$13.17B ->
   ~$12.49B. Detail: hull-builder topic log.
2. **Archetype MECE revision** (D axis). D failed to place 36% of NAICS (vs P's 14%); D0 was three
   things mashed together ($3.03B). Added **D11 Services**, resolved the **D2/D3 electric-power
   crack** (re-adjudicated the $2B NG entity: Virginia->D2, Columbia->D6), reframed **D9** as an
   application-agnostic material/process fallback, tightened D8/D10 catch-alls, kept ordnance in
   D6 (decided), left P axis alone. **D0 collapsed 24% -> ~7%.** Detail: MECE topic log.
3. **D9 functional-domain push** (user-approved Tier A + 2 mis-bins). 7 firm-level overrides
   (Scot Forge/Erie/AmTank/Ranor -> D2, Goodrich -> D1, D.W. Clark -> D4, Industrial Corrosion ->
   D11). D9 $1,446M -> $926M. Detail: MECE topic log addendum.

## Artifacts produced this session

- Rebuilt `projects/research_shared/award_classification_refactor.xlsx` (reopen in Excel to
  refresh cached D/P; all live formulas).
- **`projects/research_shared/DOMAIN_SHARE_CONCENTRATION_CAVEAT.md`** - standalone caveat: several
  D shares are 1-2 contracts deep (Virginia D2 40% is 72% one NG contract; Columbia D6 24.5%;
  etc.). Read before quoting any domain %.
- New script `scripts/apply_mece_remap.py` (auditable crosswalk remap).
- Backups: `extracted/naics6_archetype_map.pre_mece.csv`, `extracted/*_archetype_results.pre_d9mece.csv`.
- Two topic logs (above).

## Memories written

- `hull-builder-only-scope` (project) - the workbook is a ~$12.49B hull-builder subset of the
  $13.1B canonical `_corpus`; filter in 3 build scripts, not `_corpus`; HII-NNS gap caveat.
- `audit-before-applying-overrides` (feedback) - for per-firm classification changes, audit +
  recommend first and WAIT for approval before writing (user interrupted a read-only audit to
  say so).
- Updated `canonical-corpus-source` to cross-link the hull-builder subset.

## Open / next

- **Constant-FY2026 dollars** - on hold (Thread 1).
- **D9 Tier B** (Ellwood Forge, Lehigh Heavy Forge, Seemann bow domes - app likely, exact part
  unconfirmed) left as D9; push later if desired.
- **D0 residual** ($277M/$319M/$286M per program) is genuine-indeterminate generic codes (336611
  shipbuilding $1.2B, 332999 misc-fab-metal $0.5B) - firm-level overrides only.
- **Verify-before-publish** (from the caveat doc): BAE Land & Armaments showing in Virginia D2
  ($333M) looks mis-attributed; DRS Naval Power split across two UEIs in Columbia D2.
- Whether to flip the propulsor fabricators (American Tank, Ranor) from D2 to D1 (structural) -
  offered, not done.
