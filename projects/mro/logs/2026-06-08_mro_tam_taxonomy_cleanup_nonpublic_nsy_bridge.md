# 2026-06-08 — MRO TAM/SAM terminology cleanup + Private-Addressable convergence-bug fix

## Problem

The MRO model + deck over-loaded the word **"TAM"** for five different quantities, and the
workbook `Private Addressable` sheet had a real formula bug: bottom-up "private-addressable"
started from the **services-only** universe ($7,067M, no PSC 1905) then **subtracted** captive
PSC 1905 OH ($1,903M) + FMS ($100M) → a bad **$5,064M**, giving a **−$2,944M** "convergence
gap" against its top-down ($8,008M). Meanwhile the deck slide 11 claimed convergence within
~6% (~$540M), and SAM Build already disclosed the contradiction (QA-6: Broad Addressable −
Private Addressable = **$2,071M**, "methodologies differ").

Root cause: captive-SUPSHIP / FMS *contestability* exclusions were applied at a TAM-adjacent
layer. The deck slide 11 ("addressability is a SAM question") and the atom engine already
handle them **in SAM** — SAM Build's `Broad Addressable` = TAM − captive − FMS = **$7,135M**
is the correct private-contestable base. The buggy sheet was the lone outlier.

## Decision (user-approved)

Captive/FMS live in **SAM only**. Exactly one number is "TAM" = **Reconciled FPDS-visible MRO
TAM** (~$8,971M). Slide 11 headlines a **non-public-NSY reconciliation cross-check**, not
"private-addressable TAM". Target hierarchy (all verified against the rebuilt xlsx):

| | $M | called "TAM"? |
|---|---:|---|
| Budget-anchored MRO funding pot (top-down, **WPN excluded**) | 16,996 | no |
| Non-public-NSY funding cross-check (pot − Public NSY 7,485) | 9,511 | no |
| **Reconciled FPDS-visible MRO TAM** (services 7,067 + embedded 1,904) | **8,971** | **yes (only)** |
| Broad Addressable / private-contestable SAM base (TAM − captive − FMS) | 7,135 | no (SAM rung) |
| Selected SAM (Core Depot) | 4,781 | no |

Cross-check delta 9,511 − 8,971 = **~$540M (~6%)** — ties to the deck's already-correct
`slide10_table.xml` bridge (16,996 / 8,971 / +8,025).

## Workbook changes (`projects/mro/workbook/workbook_mro/sheets/`)

- **`model_tam_bridge.py`** — WPN dropped from the summed total → a memo row below the line
  (top-down 17,496 → **16,996**); bottom-up grand total switched from services-only
  (`navy+cg`) to `reconciled_mro_tam_cell()` (**8,971**); gap → **8,025**; "Top-down minus
  Public NSY" drop-through → **9,511**. Now ties to deck slide 10.
- **`model_private_addressable.py` → repurposed to "Non-Public-NSY Bridge"** (kept the module
  filename + `PRIVATE_ADDRESSABLE` symbol; only `_TAB` + accessors changed). Two blocks:
  §1 cross-check (pot 16,996 − Public NSY 7,485 = 9,511 vs TAM 8,971, Δ 540); §2 SAM entry
  (Broad TAM `SUM(amount_range)` − captive+FMS = Broad Addressable **7,135**, via
  `SUMPRODUCT(amount, scope_class="Addressable")` over `data_tam_atoms` ranges — acyclic).
  New accessors `budget_pot_cell / nonpublic_nsy_crosscheck_cell / crosscheck_delta_cell /
  broad_addressable_entry_cell`; deleted the captive `sumifs_psc1905` / WPN / FMS / old top-down.
- **`model_sam_build.py`** — dropped QA-6 + its `addressable_bottomup_cell` import (decouples
  the `private_addressable → sam_build` edge; QA-3 already bounds Broad Addressable ≤ TAM).
- **`summary_executive_summary.py`** — removed the two §1 "Private-addressable TAM" rows;
  rewrote §3 → "Non-public-NSY cross-check" (pot / cross-check / TAM / Δ) via the new accessors.
- **`outputs_figure_register.py`** — S06 "Budget-anchored MRO funding pot"; S07 repointed to
  the cross-check (kept 3 rows → DO-id count stable).
- **`guide_methodology.py`** — §2c rewritten into the non-public-NSY bridge line + the Broad
  Addressable (SAM-entry) line (the old `= TAM − Public NSY − captive − FMS` was wrong: Public
  NSY isn't in the TAM, it's in the pot); §1 defs, §3 flow, §5 evidence tabs (captive/FMS →
  SAM Build).
- **`chartdata_output.py`** §13 header "Private-Addressable MRO TAM" → "Non-public-NSY MRO
  funding" (text-only; the cell already computed 9,511).
- **`qa/tie_out.py`** `_ENGINE_TABS` "Private Addressable" → "Non-Public-NSY Bridge"
  (mandatory). Plus `sources_source_index.py`, `inputs_assumptions.py`, `taxonomy_mro.py`
  docstrings/labels.

## Deck changes (`projects/mro/deck/deck_mro/slides/` + `_chart_xml/`)

Full `.py` + frozen-XML edits: slide 3 definitions table (TAM = reconciled FPDS-visible;
SAM = TAM-atom subset with Broad Addressable ~$7.1B rung); slide 4 takeaway + `slide04.xml`
(65-PSC = $7.1B, +$1.9B embedded → $9.0B "Reconciled MRO TAM"); slides 6/7 captions
("Reconciled FPDS-visible MRO TAM"); slide 8 caption ("Budget-Anchored MRO Funding"); slide 9
takeaway + `slide09.xml` (residual/scope/axis → "non-public-NSY funding"); slide 10
`slide10_table.xml` explanation ("non-public-NSY TD"); slide 11 title "Non-Public-NSY
Cross-Check" + `slide11.xml` ("Non-public-NSY TD: $9,511M"), keeping the "addressability is a
SAM question" note.

## Verification (all green)

- Pre-change baseline required a **rebuild first** (the on-disk xlsx the user saved was stale
  vs current source); after rebuild, `compare` was green.
- `build_workbook.py` (22 sheets, sheet 11 = Non-Public-NSY Bridge, 9 native tables);
  `verify_crosstab.py` OK (4,290).
- `compare --invariant-a warn`: **Invariant B 86/86 (zero producer drift)**; Invariant-A
  deltas localized to TAM Bridge / Non-Public-NSY Bridge / SAM Build only (removed old
  −2944/−1903×2/−100×2/500×2/1239.85/1480.31; added 16996×2/9511×2/8025/8971×3/540/7135/−1836).
  Small 26/26.87/123.57 are greedy-multiset tol-collateral, not foreign-sheet changes.
- `regen-baseline` → REGEN OK (Invariant B self-asserts before write; 6331-value multiset);
  final `compare` → TIE-OUT OK (B+A).
- `build_deck.py` (15 slides, 5 charts); rendered slides 3/4/6/7/8/9/10/11 via soffice→pdftoppm
  — all labels/numbers correct, no overflow.

## Notes / not done

- `fms_estimate_cell` (Assumptions) is now consumed nowhere (kept as a reference plug to avoid
  row shifts; FMS exclusion now lives on atom scope_class).
- `qa/*/probe/08_Private_Addressable.json` etc. are stale standalone diagnostic dumps (no gate
  reads them) — left as-is.
- Output: `projects/mro/20260607_Defense Drivers MRO_vS.{xlsx,pptx}`.
