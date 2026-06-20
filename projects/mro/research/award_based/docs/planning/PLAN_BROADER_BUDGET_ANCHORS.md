# Plan: Broader Top-Down Budget Anchors for MRO Reconciliation

**Status**: partially implemented. TAS / appropriation-color pull
completed 2026-04-18 (see `sessions/SESSION_2026-04-18_v_tas_funding_pull.md`).
Workbook integration still pending.

**Motivation**: the current `Budget Anchors` sheet + Services Budget
Reconciliation block uses OMN cost element 928 "Ship Maintenance By
Contract" (summed across BA-1 Ship Ops SAGs = $2.4B) as the top-down
anchor for the FPDS-captured $7.4B Services TAM. Real FY2025
obligations on MRO PSCs are funded by **multiple appropriations**, not
just OMN CE 928. This plan broadens the anchor to reflect how MRO-PSC
contract work is actually sourced across the federal appropriation
stack.

The FPDS $7.4B is correct. What is incorrect is the current narrative
that OMN CE 928 ($2.4B) is "the" top-down comparison -- in reality, a
set of appropriations feeds MRO-PSC obligations, and the right
top-down number for a comparison is the sum of their contract-directed
slices.

---

## Bottom-up measurement (new, 2026-04-18)

Rather than infer the appropriation mix from budget-book line items,
the session (v) TAS pull measures it directly by joining every MRO-PSC
FY25 obligation to its Treasury Account Symbol via USAspending
`/api/v2/awards/funding/`. Measured breakdown across 9,282 MRO PIIDs
(98.4% of FY25 $ directly cached + PSC-bucket imputed for the tail):

| Federal Account | FY25 $M | % | Appropriation |
|---|---:|---:|---|
| 017-1804 | $2,794M | **37.7%** | OMN (Operation & Maintenance, Navy) |
| 017-1810 | $2,639M | **35.6%** | OPN (Other Procurement, Navy) |
| 097-0400 | $804M | 10.9% | RDT&E, Defense-Wide |
| 097-0100 | $185M | 2.5% | O&M, Defense-Wide |
| 057-3400 | $163M | 2.2% | OMAF (O&M, Air Force) |
| 097-0300 | $111M | 1.5% | Procurement, Defense-Wide |
| 070-0610 | $111M | 1.5% | USCG OE |
| 017-1319 | $92M | 1.2% | APN (Aircraft Procurement, Navy) |
| 021-2020 | $80M | 1.1% | OMA (O&M, Army) |
| 070-0613 | $76M | 1.0% | USCG AC&I |
| 017-1611 | $40M | 0.5% | **SCN** |
| 017-1507 | $36M | 0.5% | WPN |
| ... | ... | ... | 24 more accounts |
| **Total** | **$7,406M** | 100% | |

**Artifact**: `data_pull/output/usaspending/approp_rollup_imputed.json`.

Per-PSC-bucket ratios (used for imputation on uncached awards, and
useful on their own):

| PSC Bucket | FY25 $M | Dominant appropriations |
|---|---:|---|
| J998/J999 Depot Ship Repair | ~$4,900M | OPN 70% + OMN 27% |
| J-series Equip Maint | ~$1,800M | OMN 38% + RDT&E-DW 32% + OPN 9% |
| K-series Equip Mod | ~$400M | OMAF 22% + OMN 14% + Proc-DW 14% + OPN 10% |
| N-series Install | ~$150M | OMN 68% + OPN 11% + O&M-DW 9% |
| M2 Husbanding | ~$50M | OMN 89% + USCG 11% |
| L-series Tech Rep | ~$40M | OMN 97% + RDT&E-DW 3% |

Key takeaways:
- **J998/J999 depot work is OPN-dominant, not OMN-dominant**. 70% is
  routed through OPN (modernization install funding), not OMN CE 928.
- **SCN spillover on MRO PSCs is tiny** ($40M). The plan's earlier
  $200-500M estimate was 5-7x too high.
- **Defense-Wide RDT&E** ($804M) is the third-largest appropriation,
  almost entirely driven by J-series equipment sustainment (Draper MK7
  Trident, SMDC/SSP work).

---

## Blockers resolved (session v)

### ORATA vs OMN CE 928 overlap - INSIDE CE 928, not additive

`sources/OMN_Book.txt` line 5608 lists ORATA ($990M FY25) as a
WORKLOAD category in the OP-5 Performance Criteria table for SAG
1B4B. Line 6698 lists CE 928 Ship Maintenance By Contract ($2,228M
FY25) as a COST-ELEMENT category for the same SAG. Both tables sum
to the same $11,764M SAG total - they are two views of the same
dollars. Line 5518 narrative confirms ORATA is outsourced contract
workload, so inside CE 928.

**Conclusion**: ORATA cannot be added as a separate additive anchor.
Plan's proposed $990M ORATA row is dropped.

### SCN spillover onto MRO PSCs - $66M measured, not $200-500M

Measured two ways, consistent:
- Contracting-office filter (`SUP OF SHIPBUILDING CONV AND R` +
  `SUP OF SHIPBUILDING GROTON` on MRO PSCs): $66M across 26 rows.
- TAS filter (017-1611 on MRO PSCs): $40M.

Composition: Post-Delivery Availability / Post-Shakedown Availability
on newbuild LPD 29, DDG 128, LCS 36/38. Warranty-style work on
recently-delivered ships, not RCOH modernization bundles.

**Conclusion**: treat as ~$40-66M memo row, not a primary anchor.

### NDSF data source - not needed, already captured

NDSF is primarily a strategic-sealift PROCUREMENT fund in declining
use (ESD/ESB procurement has shifted to SCN BLI 3039 per
SCN_Book.txt line 13818). NOT an MSC operating fund. MSC operations
and maintenance are already captured:
- Operations = OMN SAG 1B1B Navy Transportation (`OMN_1B1B_TOTAL_FY25`).
- Maintenance = OMN SAG 1B4B Ship Maintenance MSC section
  (`OMN_1B4B_TOTAL_FY25`), line 5637 of OMN_Book.

**Conclusion**: drop NDSF section from the plan.

---

## Revised proposed structure for Budget Anchors sheet

Keep the existing 4 sections (OMN Ship Ops BA-1 / SCN Capital Ships /
USCG ISVS / NWCF Memo) unchanged. Add one new top section:

### New section: **FY2025 MRO-PSC TAS Attribution (bottom-up measured)**

A rolling summary of the TAS-attributed breakdown above, with named
cells for the top appropriations so the Services sheet can reference
them directly:

- `MRO_TAS_OMN_FY25` = $2,794M
- `MRO_TAS_OPN_FY25` = $2,639M
- `MRO_TAS_RDTE_DW_FY25` = $804M
- `MRO_TAS_SCN_FY25` = $40M
- `MRO_TAS_USCG_FY25` = $187M (sum of 070-* accounts)
- `MRO_TAS_DEFENSE_WIDE_FY25` = $1,100M (sum of 097-* accounts)
- `MRO_TAS_OTHER_FY25` = remainder
- `MRO_TAS_TOTAL_FY25` = $7,406M (= FPDS Services TAM)

These values refresh whenever the TAS pull is re-run against current
Awards; the plan's earlier structural additions (ORATA / NDSF / OPN
BA-8 detail / SCN spillover) are either dropped or demoted to memo
rows.

### Optional smaller additions (lower-priority)

- OMN non-BA-1 CE 928 (1C1C + 1C3C + 1C7C): ~$38M. Tiny; skip unless
  completeness required.
- OPN BA-8 line 9020 Spares and Repair Parts total: ~$883M as a
  top-down cross-check on OPN's contribution, but note that the $2.64B
  total OPN on MRO PSCs spans many more BAs than just 9020.
- USCG OE Depot Level Maintenance earmark ($70M FY25 from
  `data_v2.xlsx` row 3351): already aligns with the measured $187M
  USCG total.

---

## Revised Services sheet reconciliation block

Current: FPDS $7.1B vs OMN CE 928 $2.4B -> $4.7B "implied gap"
attributed narratively to appropriation-color + vintage mixing.

**Revised**: replace the "implied gap" with a **per-appropriation
breakdown** showing where each FY25 MRO $ lands. The "gap" disappears
by construction once all appropriations are captured:

```
FY25 FPDS Services MRO TAM:                  $7.4B
  of which funded by OMN (017-1804):         $2.8B (38%)
  of which funded by OPN (017-1810):         $2.6B (36%)
  of which funded by RDT&E Defense-Wide:     $0.8B (11%)
  of which funded by Defense-Wide other:     $0.3B ( 4%)
  of which funded by OMAF, OMA, other Navy:  $0.5B ( 7%)
  of which funded by USCG:                   $0.2B ( 3%)
  of which funded by SCN, WPN, APN:          $0.2B ( 2%)
```

The narrative shifts from "there's a $4.7B unexplained gap" to "here
is the exact appropriation mix funding $7.4B MRO, which matches FPDS
by construction."

---

## Implementation phases

### Phase 1: TAS pull (DONE 2026-04-18)

- `data_pull/usa_client.py` -> `get_award_funding()` method (DONE)
- `data_pull/enrich_funding_accounts.py` -> orchestrator (DONE)
- `data_pull/classify_approp_colors.py` -> classifier (DONE)
- Cache: `data_pull/output/usaspending/funding/` (3,730 awards)
- Output: `approp_rollup_imputed.json` (DONE)

### Phase 2: Budget Anchors sheet addition (TODO)

Add a new `SECTIONS` entry in `sheets/budget_anchors.py` at the top of
the sheet (before OMN Ship Ops BA-1). Rows: 7-8 per-appropriation
rows, each with an FY25 $M cell (value from the rollup JSON) and
a defined name. Load values by reading `approp_rollup_imputed.json` at
build time.

### Phase 3: Services sheet reconciliation rewrite (TODO)

Replace `_write_mro_budget_reconciliation` to use the per-appropriation
breakdown. Drop the "Implied gap" row in favor of a tie-out row showing
FPDS TAM = sum of per-appropriation attributions.

### Phase 4: Methodology doc update (PARTIAL)

`docs/methodology/METHODOLOGY_MRO_BUDGET_RECONCILIATION.md` updated
2026-04-18 with TAS findings. Further narrative refinement pending
workbook integration.

### Phase 5: Deck update (TODO)

`deck/SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md` callout rewrite. New callout:
"FY25 Services MRO $7.4B sources mostly from Navy OPN + OMN (73%
combined), with Defense-Wide RDT&E as the surprise third anchor at
11%. SCN and CE 928-only framings understate the real appropriation
stack."

### Phase 6: Completing TAS coverage (LOW PRIORITY)

- 5,552 MRO PIIDs uncached (long tail, $118M / 1.6% of $). At
  USAspending's ~1 req/s effective rate under sustained load, ~75 min
  additional pull. Not worth it unless 100% direct-classified coverage
  is needed (imputation fills the gap adequately).
- ~15,336 newbuild / other PSC PIIDs never attempted. Would let the
  same methodology reconcile Product Procurement ($ heavy at
  SCN-backed HII NNS submarine + carrier programs). ~3 hours; probably
  worthwhile for a full top-down vs bottom-up story.

---

## Open questions (resolved)

1. **SCN spillover measurement** - resolved: $40-66M via both the
   SUP OF SHIPBUILDING contracting-office filter and TAS 017-1611.
2. **ORATA treatment** - resolved: inside OMN CE 928, not additive.
3. **NDSF data source** - resolved: not needed (MSC ops+maintenance
   already in OMN 1B1B+1B4B).
4. **Timing vs TAM framing decision** - independent. The TAM framing
   question (Frame A contracting activity vs Frame B revenue earned)
   can be decided separately; this plan's appropriation breakdown
   works for either frame, just applied to the chosen denominator.

---

## Related docs

- `sessions/SESSION_2026-04-18_v_tas_funding_pull.md` -- full log of
  the TAS pull, blocker resolution, and findings
- `docs/methodology/METHODOLOGY_MRO_BUDGET_RECONCILIATION.md` -- now
  references the measured appropriation breakdown
- `docs/methodology/METHODOLOGY_TAM_FRAMING.md` -- parallel open
  question about what $7.4B represents (contracting activity vs
  revenue earned)
- `docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md` -- same
  appropriation-color-mixing dynamic on the SCN side
- `sheets/budget_anchors.py` -- file to extend with TAS attribution
  section
- `sheets/services.py` -- file to rewrite the reconciliation block in
- `data_pull/output/usaspending/approp_rollup_imputed.json` --
  source data for the Budget Anchors TAS section
