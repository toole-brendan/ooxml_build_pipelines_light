# 2026-06-21 — GFE vs Basic Construction: investigation + "no change" decision

Follow-on to `2026-06-20_master_tam_consolidation.md`. A question came up after the
master-TAM consolidation: **submarines fold propulsion into GFE, DDG does not** — is
that an inconsistency that needs fixing? Investigated it end-to-end and concluded
**no change needed: the methodology is already consistent.** This log records the
reasoning so it isn't re-litigated.

## The original concern
- Submarine GFE (`gfe_sum_$M`) = **Propulsion (BPMI nuclear reactor) + Electronics + Ordnance**.
- DDG GFE (`gfe_elec_ord_$M`) = **Electronics + Ordnance only** — the DDG funnel-build
  script even calls it "a LOWER BOUND on GFE" because the LM2500 propulsion is folded
  into HM&E, not broken out.
- Surface read: "DDG under-counts GFE / the two GFE columns aren't comparable."

## What the investigation found

1. **LM2500 is CFE, not GFE.** GFE = *government*-furnished (the Navy buys it and ships
   it to the yard): DDG Electronics (Aegis/SPY-6/SEWIP) + Ordnance (Mk41 VLS / guns).
   The LM2500 is bought by the *shipyard* (contractor-furnished) → it is **not** GFE.
   The `gfe_elec_ord_$M` naming was deliberate and correct. (For subs, propulsion =
   nuclear reactor = genuinely government-furnished/BPMI, so it correctly sits in GFE.)

2. **GFE is NOT inside Basic Construction in the budget.** The SCN P-5c "Cost Category"
   lines are **siblings**, not nested. Verified against
   `virginia_columbia_research/extracted/scn_p5c_per_fy_reconciled.csv` (Virginia FY2024):
   `BC 9,070.8 + Plan 207.2 + Propulsion 1,121.5 + Electronics 562.4 + HM&E 144.2 +
   Ordnance 0 + Other 70.5 + ChgOrd 185.1 + TechIns 16.0 = 11,377.6 = Total Ship
   Estimate (delta 0.0)`. So Basic Construction is its own line — the prime-shipyard's
   construction-contract base — *parallel* to the GFE lines, not containing them.

3. **TAM is built on Basic Construction ONLY.** For both programs:
   `TAM = Basic Construction × place-of-performance supplier coefficient` (+ small
   additive streams: DDG AP/LLTM = P-10 Ship-Construction-EOQ base × ~100%, ~$174M/yr;
   OBBBA mandatory BC base × BC coeff). The BC base is literally
   `scn_cell(li, fy, 'basic')`; the coefficient is the announced/measured share of the
   construction contract's place-of-performance landing away from the prime/co-prime
   yards (subs: Block V 34% / Build I 22%; DDG: MYP-corrected ~25.3%).

4. **Therefore the GFE columns never enter the TAM math.** `gfe_sum_$M` /
   `gfe_elec_ord_$M` are reporting-only (the GFE% display on SCN Budget and the ceiling
   cost base). Whether the LM2500 is labeled GFE or not has **zero effect on the TAM
   number**, because TAM = BC × coeff and neither program's GFE line was ever in BC.

## Decision
- **No change.** The methodology is consistent: both programs use the same base
  (Basic Construction) and the same coefficient mechanism; the GFE-labeling difference
  is immaterial to TAM.
- Created an audit note (`GFE_TREATMENT_DISCREPANCY.md`) mid-investigation, then
  **deleted it** — it implied a problem where there isn't one and caused more confusion
  than it resolved.

## One thing noted but deliberately NOT acted on
The DDG LM2500/HM&E is contractor-furnished and therefore *supplier-addressable*, yet
it sits in HM&E ("other non-BC") and is excluded from the DDG BC/TAM base. Subs
correctly exclude propulsion (GFE reactor, non-addressable). So DDG's TAM is
**conservative** on yard-bought propulsion/HM&E. If anyone ever wants DDG TAM to
include yard-bought HM&E/propulsion, the lever is the **BC-base scope** (add HM&E to
the addressable base) — NOT the GFE label. That is a deliberate scope choice, not an
inconsistency, so it's parked here rather than changed.

## Cross-refs
- `tam/logs/2026-06-20_master_tam_consolidation.md` (the consolidation this follows)
- Cost-funnel definitions: `*/research/scripts/build_cost_funnel.py`
- TAM engine: `master/workbook_master_tam/sheets/{submarines,ddg}/model_tam_build.py`
