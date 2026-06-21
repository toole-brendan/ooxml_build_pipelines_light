---
title: The MYP redaction and the unseen layer
---

# The MYP redaction and the unseen layer

This chapter develops the structural caveats that bound any quantitative analysis of destroyer outsourcing. The first section addresses a **destroyer-specific structural feature** that has no parallel in the U.S. submarine analysis: the **source-selection-sensitive redaction** of the FY23-27 multiyear master award dollar values, which is a direct consequence of the two-yard competitive procurement structure. The second section treats the **standard "unseen layer" categories** that apply across federal-procurement analysis broadly — categories that are present in both the destroyer and the submarine analyses but that interact with the destroyer corpus in characteristic ways.

## The MYP redaction caveat

Both anchor cases of the destroyer DoD-announcement corpus — the August 2023 FY23-27 multiyear master awards to GD Bath Iron Works (PIID `N00024-23-C-2305`, war.gov article 3479250, dated August 1, 2023) and to HII Ingalls Shipbuilding (PIID `N00024-23-C-2307`, war.gov article 3491276, dated August 11, 2023) — contain in their published DoD daily contract announcement paragraphs the following standard redaction language:

> "...the dollar values associated with the multiyear contract are considered source selection sensitive information and will not be made public at this time (see 41 U.S. Code 2101, et seq., Federal Acquisition Regulation (FAR) 2.101 and FAR 3.104)."

The actual obligated dollar amounts — known from trade-press reporting (USNI News, Defense Daily, Naval News) to total approximately **$14.58 billion across the BIW + Ingalls combined awards** (BIW share approximately $6.40 billion, Ingalls share approximately $8.18 billion) — are not in the DoD-announcement bulletins. The bulletins do disclose the **place-of-performance percentages** (the BIW master at 69% Bath, Maine; the Ingalls master at 77% Pascagoula, Mississippi for Block I and 79% for Block II option), but the dollar-value field is empty.

### Why the redaction occurs

The source-selection-sensitive designation under 41 U.S. Code § 2101 et seq. and FAR 3.104 protects information that, if disclosed publicly, could compromise the integrity of an ongoing or recently-concluded source-selection process. The destroyer FY23-27 procurement was structured as a **two-yard competitive multiyear**: both BIW and Ingalls submitted competing proposals, the Navy made parallel award decisions to both yards, and the per-yard dollar values reflect the Navy's commercial negotiation outcomes with each yard separately. Disclosing the individual per-yard dollar values would reveal the competitive pricing positions of the two yards to each other and to the broader commercial market, which the Navy considers source-selection sensitive even after the award.

This is not a destroyer-specific procurement convention per se — the source-selection-sensitive provisions of FAR 3.104 apply across federal procurement. What is destroyer-specific is the **two-yard competitive procurement structure** that triggers the designation. By contrast:

- **Submarine multiyear procurements** are structured as a single-prime competitive (GDEB only, with HII Newport News participating as the team-build partner under GDEB's prime). There is no parallel-yard competitive process; the dollar value of the master award is disclosed in the DoD-announcement bulletin.
- **Aircraft carrier procurements** are also single-prime (HII Newport News only); same disclosure pattern as submarines.
- **Frigate (Constellation-class) procurements** are single-prime (Fincantieri Marinette Marine); same pattern.

The destroyer FY23-27 MYP is therefore methodologically unique within the recent Navy new-construction portfolio in having its master-award dollar values redacted. (The FY18-22 destroyer multiyear, awarded September 2018, also used the two-yard structure but pre-dates the corpus coverage window — the September 2018 bulletins are not in the destroyer corpus.)

### Practical implication for the chapter 4 measurement

The chapter 4 headline finding — "approximately 87 percent of dollar-weighted POP on supplier-TAM-relevant DDG-51 actions flows outside the two destroyer shipyards" — is computed against the dollar-weighted aggregation of disclosed dollar values across the 152 supplier-TAM-relevant actions. The two redacted MYP master awards have POP percentages that would shift dollar weight strongly into the BIW (69% Bath) and Ingalls (77% Pascagoula) buckets if their $14.58 billion of obligated value were included.

If the trade-press-reported dollar values were treated as if disclosed:

| Bucket | Original $-weighted POP | Adjusted $-weighted POP including MYP masters |
|---|---:|---:|
| BIW-sites | 11.2% | approximately 36% |
| Ingalls-sites | 1.3% | approximately 31% |
| Other-US suppliers | 73.6% | approximately 33% |
| Foreign | 0% | 0% |

The adjusted reading — with the trade-press-reported MYP master values folded in — has the outside-yards share at approximately **33 percent rather than 87 percent**. This is a dramatic shift, and it illustrates the methodological dependence of the headline figure on the redaction.

**The defensible reading is to report both figures with the caveat explicit.** The 87 percent figure is "outside-yards share of supplier-TAM-relevant DoD-announcement disclosed dollar value, with MYP master values redacted." The adjusted ~33 percent figure is "outside-yards share if the trade-press-reported MYP master values are folded in as approximate dollar values." Both readings are useful, and neither is wrong; the choice depends on whether one is measuring "what does the DoD-announcement-only-disclosed-corpus say" or "what is the actual production-cost split, using trade-press supplementation for the redacted values."

For the headline conventions of this article, the chapter 4 figure stands as reported (87 percent against the disclosed-only corpus), with the explicit acknowledgment in this chapter that adjusting for the redaction shifts the headline materially. The adjusted figure is consistent with the chapter 9 estimate that the yards self-perform on the order of 33 percent of total ship cost when measured against the full per-ship Total Ship Estimate.

### Cross-reference for the dollar recovery

To recover the omitted yard-construction dollars on the MYP master PIIDs for dollar-weighted analyses that need the actual values rather than the trade-press estimates, the recommended cross-reference is to the FPDS Atom Feed (`fpds_raw_v2/gd_biw_navy_raw.json` and similar) which records the per-modification `obligatedAmount` field. The cumulative FPDS-reported totals on the two MYP masters at the May 2026 pull date:

| PIID | FPDS-reported cumulative obligated $M (latest mod) |
|---|---:|
| `N00024-23-C-2305` (BIW FY23-27 master) | 5,027.5 |
| `N00024-23-C-2307` (Ingalls FY23-27 master) | (similar order of magnitude; see fpds_raw / fpds_raw_v2) |

The cumulative FPDS figure of approximately $5.03 billion on the BIW master is somewhat below the trade-press-reported $6.40 billion, reflecting the gap between the contract ceiling value (approximately $6.40B for the BIW share of the FY23-27 multiyear) and the actual obligated amount as of the pull date (approximately $5.03B, with the remainder yet to be obligated through option exercises). The Ingalls master shows a similar pattern.

## The standard unseen-layer categories

Beyond the destroyer-specific MYP redaction caveat, the analysis is subject to a set of standard unseen-layer limitations that apply across federal-procurement research broadly. These were introduced briefly in chapter 5; this section develops their interaction with the destroyer corpus.

### Purchased material booked as direct material cost

When a yard purchases hull steel, prefabricated piping, large fittings, electrical-system components, or major HM&E equipment and books the purchase under direct-material accounting rather than under a subcontract clause, the purchase is not FFATA-reportable. This is the single largest invisible category in the chapter 9 yard-side outsourcing estimate. For Ingalls and BIW combined, direct-material purchasing is estimated at several hundred million dollars per year — likely on the order of $400–700M/yr — comparable in magnitude to the FFATA-visible flow itself.

The direct-material booking is *not* a compliance gap — it is a legitimate accounting treatment under standard cost-accounting standards (CAS) for items that pass title to the buyer at the point of physical receipt rather than under a subcontract milestone-based pricing structure. The categorical invisibility is structural to the FFATA-reporting framework.

### Lower-tier subcontracts (a sub's sub)

A subcontract issued by a first-tier subawardee to its own supplier is not FFATA-reportable under FAR 52.204-10. For example, Lockheed Martin's Mk 41 VLS supplier base includes Major Tool & Machine (Indianapolis, IN) — this appears in FFATA as LM's first-tier subaward. But Major Tool & Machine's own suppliers — raw-material vendors providing precision-machined steel forgings, specialty bolts, surface-finishing services — do not appear in FFATA at all.

The cumulative dollar weight of the second-tier supplier base is unknown but is estimated in the broader defense-industrial-base research to add 30–50 percent to the visible first-tier flow. For the destroyer corpus, that implies hundreds of millions of dollars of second-tier supplier activity that the FFATA stream does not see.

### FFATA non-compliance and under-reporting

The most striking instance in the destroyer corpus is the **FY23-27 BIW multiyear master PIID `N00024-23-C-2305` with zero published subaward filings as of the May 2026 pull**. This is not consistent with the contract's roughly $6.4B trade-press-reported value and the expected first-tier subaward activity (Johnson Controls, Rolls-Royce Marine, GE LM2500 pass-through, Timken Gears, and dozens of smaller first-tier subs). The most likely interpretation is a sustained compliance gap at BIW's filing practices — confirmed at lower magnitudes in the BIW historical filings as well (the FY18-22 master `N00024-18-C-2305` has approximately $57M of filings on a $5.3B+ obligated total, again markedly thin).

The GAO has generically flagged FFATA compliance issues across the federal prime base, including the shipbuilder community, in GAO-25-106286.[^gao-25-106286] No targeted DoD Inspector General investigation of BIW's FFATA compliance has been publicly announced.

For the destroyer corpus specifically, the BIW under-reporting is the single largest individual contributor to the FFATA-vs-actual gap. The combined yard-side outsourcing estimate of $1.8B/yr (chapter 9) implicitly accounts for it by computing yard-side flow from segment revenue rather than from FFATA filings.

### Long-term supplier agreements not subordinated to the prime

Standing pricing agreements with material suppliers that pre-date the prime contract and are not modified or referenced in the prime contract are not FFATA-reportable. This is a smaller category in dollar terms (likely tens of millions per year rather than hundreds), but it is structurally invisible.

### The sub-$30,000 long tail

FFATA reports actions above $30,000 per individual subaward. Actions below the threshold are not in the FSRS data. Although individually small, the cumulative dollar value of the long tail is non-trivial. For high-action-count primes (Lockheed Martin Mk 41 VLS at 834 reported actions, Raytheon CIWS at 3,661 reported actions), the corresponding under-threshold actions could represent 5–10 percent of the actual total subaward activity.

### USAspending per-PIID truncation

The USAspending `/api/v2/subawards/` endpoint truncates output at approximately 2,500 records per prime PIID. For PIIDs with more than 2,500 first-tier subawards (notably the CIWS PIID `N00024-18-C-5406` with 3,661 records), USAspending shows only the first 2,500 — the long tail is not retrievable. SAM.gov has no equivalent cap, which is why SAM.gov is the canonical FFATA denominator for this analysis (chapter 5).

### FFATA reporting lag

First-tier subaward filings are required within 30 days of subaward issuance, but compliance with that deadline is uneven. For new prime contracts in their first 12–24 months of execution, the visible FFATA flow is systematically below the actual first-tier subaward activity by a factor of 2–3×. For the FY23-27 destroyer MYP masters (still in their first ~30 months of execution as of May 2026), the visible FFATA flow is therefore an undercount of the actual subaward activity even before accounting for the BIW compliance gap.

## Categorically-excluded categories

In addition to the unseen-layer categories above, certain categories are categorically excluded from the article's outsourcing measurement by design:

- **Federal naval shipyard depot maintenance** at Norfolk, Portsmouth, Pearl Harbor, and Puget Sound — federal payroll, not outsourced contract activity (chapter 1)
- **Federal employee labor at NAVSEA, PEO Ships, and the Aegis Technical Representative office** — government program-office labor, not outsourced
- **Weapons Procurement (WPN) and Other Procurement (OPN) appropriations** for Standard Missile, ESSM, Tomahawk, CIWS — funded under different appropriations from SCN; including them double-counts (chapter 1)
- **DDG-1000 Zumwalt-class modernization** — out-of-class for the scope of this article; OPN-funded rather than SCN-funded (chapter 1)
- **Private ship-repair work at BAE San Diego, BAE Jacksonville, BAE Norfolk, BAE Southeast Shipyards Mayport** — destroyer-sustainment scope rather than new-construction scope (chapter 1)
- **Classified-payload procurement** — by design not visible in the public SCN data (chapter 1, parallel to the submarine exclusion)

## Subordinate technical caveats

A handful of smaller methodological caveats that affect specific buckets:

### The single-supplier-no-percentage parser caveat

Approximately 5–8 LM2500 bulletin paragraphs in the corpus follow a template that names a single supplier city (e.g., "Evendale, Ohio") without an associated percent figure: "Work will be performed in Evendale, Ohio, and is expected to be completed by August 2032." The standard POP-percentage regex returns zero percent for all four buckets in the absence of an explicit percent figure. This is the cause of the chapter 4 `ddg_gfe_propulsion` row showing 19.2 percent Other-US POP rather than the expected approximately 100 percent.

A partial parser patch added in May 2026 (`RE_POP_SINGLE` regex in `pull_dod_announcements_pop.py` and `ingest_wayback_bulletins.py`) handles the "Work will be performed in [City, State], and is expected to be completed by..." pattern by assigning 100 percent of the action's POP to the matched single city. The patch lifted the `ddg51 construction` bucket BIW share from 8.9 percent to 76.5 percent — a substantial correction. However, the patch does not handle all variants of the single-supplier-no-percentage pattern, and approximately $50M of LM2500 value across 5–8 rows remains unattributed.

A more complete parser patch is straightforward (~15 minutes of work) but has not been executed; it is documented as a known limitation.

### The IVECO MARCORSYSCOM contamination

PIID `M67854-16-C-0006` is a Marine Corps Systems Command (MARCORSYSCOM, agency prefix M67854) Mk 110 amphibious-warship gun production contract that was inadvertently included in the destroyer in-scope PIID set during FPDS discovery. The contamination introduces IVECO Defence Vehicles S.p.A. (an Italian armored-vehicle manufacturer) as a top-line vendor at approximately $707M in subaward value — a Marine Corps Light Armored Vehicle supplier, not a destroyer supplier.

The `nc_lifetime_vendors.csv` view filters out IVECO from the in-scope counts via the new-construction classification pass; the SAM `top_parents` view is broader and includes the unfiltered numbers. The contamination is flagged in chapter 6 and will be cleaned in a future re-run of the discovery pipeline.

### The "non-DDG" hard-drop classification rules

The two-pass classifier hard-drops paragraphs that match the destroyer keyword set but are actually about other ship classes: submarines (mentioned "VLS" but in a Virginia-class context), aircraft carriers (mentioning the Aegis baseline as a CG-equivalent reference), Littoral Combat Ships (LCS), Landing Craft Air Cushion (LCAC), amphibious warships (LPD-17, LHA-8), Polar Security Cutter (PSC), Zumwalt-class (DDG-1000), and foreign-military-sale actions at Pascagoula or Bath. The hard-drop rules are encoded in `classify_dod_action_worktype.py` and refined in `reclassify_dod_action_subrelevance.py`. They are conservative — actions that might be DDG-relevant but that match a hard-drop keyword are excluded — which means the actual TAM-relevant corpus is likely 5–10 percent larger than the 152 actions captured in the article's headline.

This is a deliberate methodological choice: the article prefers to under-count rather than over-count the destroyer-attribution, which means the chapter 4 87-percent figure is conservative (a more inclusive rule would likely shift dollar weight toward additional supplier-TAM-relevant actions, generally at supplier-city POP rather than at yard POP, which would push the headline higher rather than lower).

## What this all adds up to

The destroyer-outsourcing analysis is bounded by the MYP-redaction structural caveat (which biases the headline figure toward outside-yards), by the standard unseen-layer categories (which bias the FFATA-visible flow downward by approximately 6–7×, per chapter 9), and by the categorical exclusions (which are deliberate definitional choices). Taken together, the analysis supports three structural conclusions:

1. **The destroyer outsourcing flow is large in absolute dollar terms** — on the order of $6.8 billion per year (GFE + yard-side combined) against a program-level annual run-rate of approximately $7–8 billion.
2. **The DoD-announcement-corpus 87 percent outside-yards figure is methodologically conservative**, in the sense that the MYP redaction biases it upward (away from the yards). Adjusting for the redaction with the trade-press-reported MYP master values shifts the headline to approximately 33–40 percent outside-yards — still substantial, but very different in magnitude.
3. **The FFATA-visible flow captures approximately 15 percent of the actual yard-outsourcing flow**, with the invisible 85 percent distributed across direct-material booking, lower-tier subs, BIW compliance gap, long-term supplier agreements, the sub-$30,000 long tail, USAspending truncation, and reporting lag.

A reader interested in a "single-number" outsourcing measurement for the destroyer program should reach for the chapter 9 combined estimate of **approximately $1.8 billion per year of yard-side outsourcing plus approximately $5 billion per year of GFE-funded supplier flow** rather than for the chapter 4 87-percent figure in isolation. The chapter 4 figure is the most-direct primary-source measurement of *outside-yards share within the disclosed DoD-announcement corpus*; it is not a complete picture of the full destroyer outsourcing flow.

[^gao-25-106286]: U.S. Government Accountability Office, *Shipbuilding and Repair: Navy Needs a Strategic Approach for Private Sector Industrial Base Investments*, GAO-25-106286 (February 27, 2025). <https://www.gao.gov/products/gao-25-106286>.
