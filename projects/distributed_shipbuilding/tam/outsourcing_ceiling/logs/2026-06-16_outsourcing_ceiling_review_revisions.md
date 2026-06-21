# 2026-06-16 — Outsourcing Ceiling: two review cycles → workbook + doc revisions

Workbook pipeline: `projects/distributed_shipbuilding/workbook_outsourcing_ceiling/`
Workbook launcher: `workbook_outsourcing_ceiling/build_workbook.py`
Workbook output:   `projects/distributed_shipbuilding/20260615_Distributed Shipbuilding Outsourcing Ceiling_vS.xlsx`
Data generator:    `workbook_outsourcing_ceiling/build_ceiling_base.py` (writes `extracted/wb_cost_base.csv` + `wb_anchors.csv`)
Doc page module:   `doc/doc_outsourced_ceiling/pages/ceiling_methodology_explainer.py`
Updated-module snapshot: `/Users/brendantoole/projects3/updated_outsourcing_ceiling/` (sheet modules copied with `updated_` prefix)
Build: `cd projects/distributed_shipbuilding/workbook_outsourcing_ceiling && python3.12 build_workbook.py`

Prior logs: `2026-06-15_outsourcing_ceiling_workbook.md` (original build), `2026-06-16_outsourcing_ceiling_doc_explainer.md` (the doc).

## Goal

Assess two external review passes on the workbook + methodology doc and implement
the meritorious fixes. The work was driven by the reviews, not a fresh spec; each
critique was verified against the actual files before acting (several were
overstated, misattributed, or constrained by unverifiable sources — noted below).

## Round 1 — first review (interpretive + sourcing fixes)

Assessed as strong/accurate; implemented the valid subset, declined the overreaches.

- **Summary p=1 vs active case.** Relabeled "Outsourcing ceiling %" →
  "Structural ceiling % (p=1 upper bound)" and added a live-linked active-case row
  (later renamed — see round 3). The "blends three concepts" framing was overstated:
  the Conversion Bridge already exposed p=0 / active-p / p=1 + a full Sensitivity
  sweep; the real gap was only Summary surfacing.
- **L-rebase derivation** on Assumptions: 40% of total ship cost ÷ portfolio
  BC/Total (live link to Cost Base, ≈65.2%) ⇒ implied L-of-BC upper bound (≈61.4%)
  ⇒ selected 50%/45%. Ledger entry for L re-tagged "Verified + judgment".
- **DDG-51 POP anchor (A7).** Added a dedicated anchor for the off-team ~13%;
  removed the parenthetical that had been buried in Columbia's A6. **Caveat:** both
  `war.gov` and `defense.gov` return HTTP 403 to automated fetches, so the review's
  specific "BIW 31% / Ingalls 23% other-locations" figures could NOT be verified —
  did not encode them. A7 states 13% as the production-weighted off-team blend and
  defines it as narrower than gross place-of-performance (no fabricated numbers).
- **p=1 tie-out.** Added "Ceiling % = Bridge p=1 case" to the hidden Tie-Outs sheet.
- **Scaffolding leak removed.** Dropped the Sources `_FRAME` line referencing the
  "×1.30 intent uplift … deck_mini_v2 (future wiring)".
- **Column widths** widened on Assumptions/Bridge/Headroom/Summary/Sources (no wrap —
  row height is locked at 10pt; `_widths.py` house rule is size-to-content).
- **Doc (kept plain-language register):** made p=1-vs-working-case explicit in
  "From hours to dollars"; "already outsourced" → announced place-of-performance
  wording; "reactor work" → "nuclear integration and test work".
- **Declined:** the workbook "LLM-ism" rewrite (workbook prose was already
  analyst-native; flagged phrases were in the doc), the DDG "headroom too high"
  argument (leans on non-comparable POP definitions), and the doc memo-restructure.

Verified via LibreOffice recompute: headline intact (portfolio core 23.9% / ceiling
76.1% / $56,418M / 3.0×), active case 50.5%, all Tie-Outs OK incl. the new p=1 check.

## Round 2 — copy to updated_ folder, then delete prose sections

- Copied all sheet modules to `/Users/brendantoole/projects3/updated_outsourcing_ceiling/`
  with an `updated_` filename prefix (originals left intact).
- **Deleted the LLM-ism prose sections** (the user's call after seeing them): every
  bottom-of-sheet "§Reading" (summary, model_ceiling, model_bridge, model_headroom)
  and the Sources "§Frame" (+ its `_FRAME` data + docstring). Kept the §1 content,
  the Assumptions settings/anchors, and the Sources §2 sourced-vs-assumed ledger
  (structured provenance, not narrative).
- **Grouping / order / tab color:** compared with `submarines/workbook/workbook_submarines`
  and `ddg/workbook/workbook_ddg`. The ceiling workbook **already** matches the
  shared `workbook_core/groups.py` logic (private `_GROUP` + `group_color()`,
  canonical summary→inputs→model→data→validation→sources order, `<group>_<slug>.py`
  names, contiguity enforced by `package_workbook`). Verified the built tab colors
  match the reference scheme on all 9 sheets — nothing to rewire. Did NOT add the
  reference's guide/outputs/chartdata groups (no such content here; groups.py says
  don't add unused groups).

## Round 3 — second review (presentation polish)

Assessed; most items valid presentation polish, a couple re-litigated settled
decisions or were data-constrained. Implemented the user-selected set:

- **#1 Sources clipping.** Dropped the visible URL column; each `source_url` is now a
  compact **auto-fit native Excel note** on the Source cell (per user: notes, not a
  Notes column; `ExcelNote` width/height left None → form-fitting, capped 220pt).
  Source column widened (cols `[44,10,34,80,6]`).
- **#2 Bridge portfolio + tie-out.** Labor-only (p=0) and material-incl (p=1) rows now
  compute Portfolio as dollar-weighted `SUMPRODUCT(shares, BC)/ΣBC`. Tie-Outs gained
  a **Portfolio** column across all five checks (added `pop_range()` on Assumptions
  and `bc_base_range()` on Ceiling Model; portfolio POP% = dollar-weighted SUMPRODUCT,
  portfolio FFATA = sum of the three classes; All-OK gate now spans C:F).
- **#3 (targeted).** Removed "TAM"/"bridge knob" from the visible Sources ledger cell;
  renamed Summary's active row → "Selected pass-through case % (p=50%)". (Hover-note
  uses of "TAM" left alone — reviewer agreed notes are fine.)
- **#4.** Sources ledger POP status "Verified" → "Sourced + derived".
- **#5/#6.** Duplicated the POP note onto the Virginia/Columbia/DDG-51 cells (was only
  on Virginia) and clarified the DDG-51 13% as a production-weighted blend
  (BIW ~20% off-Bath + Ingalls ~9% off-Pascagoula) — qualitative, no fabricated weights.
- **#7.** Removed the unused `header_styles` import in `model_ceiling.py`; scrubbed
  `_CREATOR`/`_APP` in `lib.py` (they had named `build_workbook.py` / the package).
- **Skipped (user):** the methodology DOCX tone pass — it deliberately keeps the
  plain-language explainer register, so "breakthrough / the answer people want /
  punchline" etc. remain by design, not oversight. No `updated_`-prefixed DOCX exists.
- **Durability fix (not requested, but important):** `build_ceiling_base.py`
  *generates* `wb_anchors.csv`, and its `ANCHORS` list still had the old A6 (with the
  DDG parenthetical) and no A7 — so a data rebuild would silently revert the round-1
  CSV edits. Ported the A6 fix + A7 into the generator (did NOT run it, so
  `wb_cost_base.csv` cost data is untouched); CSV and generator now agree.

## Verification

- Rounds 1 & 2: LibreOffice recompute confirmed all tie-outs OK and the headline
  values; built `.docx` confirmed the doc wording changes.
- Round 3: workbook **builds green** — 9 sheets, 0 XML errors, 0 error-literal cells,
  2 native tables, 2 note parts (Assumptions + the new Sources URL notes). The
  LibreOffice formula recompute for round 3 was **skipped at the user's request**;
  the new portfolio/POP formulas are the same dollar-weighting pattern already
  verified and are algebraically entailed (portfolio p=1 == portfolio ceiling), but
  the round-3 OK/FAIL evaluation has not been re-run.

## State / notes

- Stand-alone reader-facing deliverables; nothing wired into a live model. Rebuild
  with the launcher after edits; rerun `build_ceiling_base.py` only on a cost-funnel
  refresh (it now also carries A7 / the cleaned A6).
- `updated_outsourcing_ceiling/` holds the 12 sheet-module copies, re-synced after
  each round. It also contains `updated_20260615_…_vS.xlsx` (a copy of the built
  workbook) that I did **not** create and left untouched — confirm whether to refresh
  or remove it.
- The `updated_` copies import `workbook_outsourcing_ceiling.sheets.*` (the live
  package), so they are a labeled snapshot, not an independently buildable package.
