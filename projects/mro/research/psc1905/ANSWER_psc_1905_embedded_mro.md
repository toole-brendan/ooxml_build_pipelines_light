# Answer: PSC 1905 Embedded MRO = $1,904M (FY2025, Navy + USCG)

Companion to [OPEN_QUESTION_psc_1905_embedded_mro.md](OPEN_QUESTION_psc_1905_embedded_mro.md). This document closes the loop: what question we were trying to answer, how we answered it, what number we locked, and what the answer changes about our market-sizing picture.

## TL;DR

- **FY2025 PSC 1905 embedded MRO = $1,904M** (Central, classifier-locked). Bounds: $1,553M - $2,057M.
- Supergroup breakdown: **Submarines $1,255M, Aircraft Carriers $337M, Surface Combatants $119M, Unclassified-vessel $193M.**
- The number is **code-reproducible** from `build_script_slim/psc_1905_classifier.py`, backed by two orthogonal signals (description keywords + USAspending TAS evidence), and wired into the Reconciliation sheet of `08APR2028_MRO_Spend_v4.5.xlsx` as the workbook-scope defined name `PSC1905_MRO_EMBEDDED`.
- **Impact on TAM:** adds $1,255M to the Submarine MRO slice (2.5x uplift) and $337M to the Aircraft Carrier MRO slice (1.8x uplift) of the existing $7,067M Services MRO TAM.

---

## 1. The question

PSC 1905 is the federal Product Service Code for "Combat Ships and Landing Vessels" - i.e., the shipbuilding PSC. FY2025 Navy + USCG obligations on PSC 1905 total **$38,053M across 201 PIIDs**. On its face, this is all newbuild: Columbia SSBN construction, Virginia SSN construction, CVN-80/81, DDG-51 Flight III, Constellation FFG, and so on.

**But a non-trivial slice is actually MRO.** NAVSEA's Supervisor of Shipbuilding, Conversion, and Repair (SUPSHIP) administers *both* construction AND major overhaul work at the same builder yards - Electric Boat, HII Newport News, HII Ingalls - under one PSC set. So an Engineered Overhaul of a Los Angeles-class submarine at Newport News gets coded PSC 1905 (shipbuilding), not J998 (non-nuclear ship repair), even though it is unambiguously depot maintenance work.

The question this work answers:

> For FY2025 PSC 1905 obligations ($38,053M Navy + USCG), what dollar amount is actually MRO / depot work bundled under the shipbuilding PSC - and how does that split across submarines vs. aircraft carriers vs. other platforms?

## 2. Why this matters for the project

Our core deliverable is a defensible U.S. Navy + Coast Guard MRO TAM/SAM. The current workbook's **Services MRO TAM is $7,067M** (post-exclusion, FY25), built bottom-up from 68 J/K/N/M/H/L services PSCs. That $7.07B explicitly does NOT include any PSC 1905 dollars because PSC 1905 is classified as newbuild and sits on the Product Procurement side.

If we don't account for the embedded MRO in PSC 1905, we **structurally undercount** the addressable market for submarine and carrier maintenance:

| Platform | Services TAM (current) | + PSC 1905 Embedded MRO (this work) | Complete FPDS picture |
|---|---:|---:|---:|
| Submarines | ~$838M | +$1,255M | ~$2,093M (**2.5x uplift**) |
| Aircraft Carriers | ~$422M | +$337M | ~$759M (**1.8x uplift**) |

Undercounting submarine MRO by a factor of 2.5x is a material error for any investor or strategic read of the market. The embedded $1.9B of PSC 1905 MRO is **the single largest source of systematic undercounting** in the prior TAM methodology.

This is independent of the **public naval shipyard labor** undercount (Portsmouth / Puget Sound / Pearl Harbor, funded through NWCF reimbursement, ~$3-4B outside FPDS entirely). That's a separate issue partially addressed via Budget Anchors in the Reconciliation sheet (named range `PUBLIC_SHIPYARD_NWCF`).

## 3. Methodology - how we got to a single defensible number

The prior spec (`domnann/docs/methodology/psc_1905_mro_share.md`) produced a **range** of $1.5 - 2.0B using a 3-tier heuristic cascade (keywords + POP length + newbuild hull override). That range had ~$150-200M residual uncertainty on its Central point, which is too wide for a headline deck number.

This work tightens the answer in two ways:

1. **Reproduces the keyword cascade as versioned code** (not an ad-hoc one-off analysis), so it can be re-run deterministically and audited per-PIID.
2. **Adds a Tier 0 TAS signal** from USAspending that moves $235M of previously-ambiguous dollars into the MRO-confirmed bucket using independent evidence (federal appropriation source).

### 3.1 Classifier cascade (six tiers)

Implemented in `build_script_slim/psc_1905_classifier.py`. Order matters: first rule that fires wins.

**Tier 0 - TAS-confirmed (new in this work):**
If USAspending `/awards/funding/` shows any non-SCN federal account on this PIID (OMN `017-1804`, OPN `017-1810`, RDT&E-DW `097-0400`, `097-0300`, or Marine Corps Procurement `017-1109`) AND the keyword cascade did not tag the PIID as Newbuild -> **MRO (TAS-confirmed)**.

*Why this is a definitive signal:* O&M dollars are legally restricted by the Antideficiency Act to operations and maintenance - they cannot fund new construction. If a PSC 1905 award received OMN obligations in FY25, that portion of the contract is unambiguously MRO work. The same logic applies to OPN (modernization/depot) and RDT&E (sustainment research like Trident MK7).

**Tier 1 - Newbuild keyword or newbuild hull name -> Newbuild (keyword or hull).** Overrides everything below. Keywords: `detail design`, `DD&C`, `long lead time material`, `advance procurement`, `lead yard services`, `nuclear components`, `drawing updates`, `balance testing`, `propulsion plant`, `fabrication`, `first article`, `class design`, `supplier development`, `industrial base`, `capex`, `capital expenditure`, `WLR`, `WLIC`. Newbuild hulls: LHA 8/9, CVN 80/81, DDG 126-133, SSN 810-815, SSBN 826-828 (Columbia), LPD 30-33, FFG 62-65, T-AO 209-211.

**Tier 2 - Strong MRO keyword -> MRO (strong).** Keywords: `engineered overhaul`, `RCOH`, `DSRA`, `selected restricted availability`, `extended drydocking`, `EDSRA`, `depot maintenance`, `inactivation`, `post shakedown`, `DPIA`, `CNO availability`, `drydock`, `restricted availability`, `seam split repair`, `hull treatment`, `PIA`, `PSA`, `availability`.

**Tier 3 - Soft MRO keyword + POP <= 3 years -> MRO (probable).** Soft keywords: `overhaul`, `maintenance`, `repair`, `emergent`, `modernization`, `growth work`, `condition report`, `labor support`, `midlife`.

**Tier 4 - POP <= 2 years, no keyword -> MRO (POP-only).**

**Tier 5 - POP >= 4 years, no keyword -> Newbuild (POP-only).**

**Tier 6 - Remainder -> Unclassified.**

### 3.2 Data inputs

All inputs are symlinked into `branmut/data_pull/output/` from the `domnann/` working copy (which was built earlier on a different machine):

| File | Source | Records | Purpose |
|---|---|---:|---|
| `fpds/navy_awards_master.json` | domnann FPDS pipeline | 20,468 (194 are PSC 1905) | PIID, description, POP, hull, recipient |
| `fpds/cg_awards_master.json` | domnann FPDS pipeline | 4,746 (7 are PSC 1905) | same, USCG scope |
| `usaspending/approp_attribution.json` | USAspending service-PSC aggregator | 9,755 | NOT USED - covers only services PSCs, zero PSC 1905 overlap |
| `psc_1905_funding_agg.json` | this work (from USAspending /awards/funding/) | 70 (PIID, federal_account) rows across 57 PIIDs | Tier 0 TAS signal |

### 3.3 What Path 1 (TAS pass) actually delivered vs. what the plan predicted

The original plan in `OPEN_QUESTION_psc_1905_embedded_mro.md` hoped Path 1 would classify 60-80% of PSC 1905 dollars cleanly via Treasury Account Symbol (TAS) mapping to specific budget line items (SCN LI 2086 RCOH = MRO, SCN LI 1045 Columbia = Newbuild, etc.).

**What we actually got:** USAspending's `/awards/funding/` endpoint returned transaction-level TAS for only ~$105M net of the $38,053M total - about **0.3% coverage**. The missing 99.7% is SCN (017-1611), where USAspending carries award-level imputed obligations but does NOT populate `transaction_obligated_amount` on individual rows. The `usa_client.py` filter drops those rows because both obligated and outlay fields are null.

The 70 rows we did get were all for OMN/OPN/RDTE/Procurement-MC/Procurement-DW accounts - each of which is a definitive MRO signal when it appears on a PSC 1905 award. So Path 1 was highly valuable on a per-PIID basis even though dollar coverage was thin. It moved 31 PIIDs from ambiguous buckets (Unclassified / POP-only / probable) into `MRO (TAS-confirmed)`, accounting for $235M of classification upgrades. The biggest single moves:

| $M | PIID | Description | Signal |
|---:|---|---|---|
| 54.1 | N0002423C2324 | DDG 1000 BYMP EXECUTION (PMS 500 OPN) | OMN + OPN funding, previously Unclassified |
| 38.0 | N0002423C4300 | Electric Boat NEW ENGLAND MAINTENANCE AND MANPOWER INITIATIVE | OMN funding, previously Unclassified |
| 36.5 | N0002423C4307 | Electric Boat NUCLEAR REGIONAL MAINTENANCE DEPARTMENT | OMN funding, previously Unclassified |
| 26.0 | N6279325F0003 | HII COMPREHENSIVE INCOMPLETE WORK LIST | OMN funding, previously Unclassified |
| 10.0 | N5005424F6003 | HII Fleet Support labor on USS Ford weapons elevator | OMN funding, previously MRO (probable) |

### 3.4 What we did NOT do (and why)

- **Per-mod LLM classification** (Path 2 in the open question). The `navy_awards_master.json` and `cg_awards_master.json` files store PIID-level rollups, not `mods[]` arrays - per-mod descriptions aren't preserved downstream of the domnann pipeline. Getting them would require re-hitting USAspending `/transactions/` for ~1,000-2,000 mods across the 201 PIIDs. We decided the marginal precision gain wasn't worth the additional complexity once the Central number was stable: after Tier 0, the remaining $190M of ambiguous dollars ($153M MRO POP-only + $37M Unclassified) is spread across mostly sub-$10M per-PIID items whose classification won't swing the headline by more than ~$50M.
- **Per-PIID manual review.** Would pin down the residual to an exact number but is not scalable and would contradict the "reproducible from code" goal.

## 4. Results

### 4.1 Bucket distribution (201 PSC 1905 PIIDs, FY2025 $38,053M)

| Bucket | N | $M | % |
|---|---:|---:|---:|
| Newbuild (keyword or hull) | 20 | 23,451 | 61.6 |
| Newbuild (POP-only) | 60 | 12,508 | 32.9 |
| MRO (strong) | 13 | 1,553 | 4.1 |
| **MRO (TAS-confirmed) [new]** | **31** | **235** | **0.6** |
| MRO (probable) | 28 | 116 | 0.3 |
| MRO (POP-only) | 43 | 153 | 0.4 |
| Unclassified | 6 | 37 | 0.1 |
| **Total** | **201** | **38,053** | **100.0** |

### 4.2 Embedded MRO bounds

| Bound | Method | $M |
|---|---|---:|
| Conservative | MRO (strong) only | 1,553 |
| **Central (locked)** | **strong + TAS-confirmed + probable** | **1,904** |
| Upper | + MRO (POP-only) | 2,057 |

### 4.3 Supergroup breakdown (Central basis)

| Vessel supergroup | PSC 1905 total $M | Embedded MRO $M | MRO share |
|---|---:|---:|---:|
| Submarines | 24,279 | 1,255 | 5.2% |
| Aircraft Carriers | 1,431 | 337 | 23.6% |
| Unclassified-vessel | 3,471 | 193 | 5.6% |
| Surface Combatants | 5,653 | 119 | 2.1% |
| Amphibious Warfare Ships | 1,644 | 0 | 0.0% |
| Combatant Crafts | 957 | 0 | 0.0% |
| Multi-class | 534 | 0 | 0.0% |
| Unmanned Maritime Platforms | 83 | 0 | 0.0% |

Submarines and aircraft carriers are where the overwhelming bulk of embedded MRO lives - expected, since RCOH and submarine engineered overhauls are the work types that get bundled under the shipbuilding PSC at SUPSHIP-administered yards. Surface combatants, amphibs, and crafts are predominantly newbuild in PSC 1905 (DDG-51 Flight III, FFG-62, LHA 8/9, LPD 30-33).

### 4.4 Validation - top MRO-character PIIDs

The two anchors cited in the methodology doc both correctly classify:

| $M | PIID | Recipient | Description | Classification |
|---:|---|---|---|---|
| 831 | N0002412C2115 | Electric Boat | Fleet Directed Work: Special Hull Treatment (SHT) Seam Split Repairs | MRO (strong) ✓ |
| 424 | N0002418C4314 | HII Newport News | USS Boise (SSN 764) Engineered Overhaul Execution | MRO (strong) ✓ |
| 97 | N0002425C2127 | HII | CVN 68 Inactivation AP Emergent | MRO (strong) ✓ |
| 54 | N0002423C2324 | HII | DDG 1000 BYMP Execution | MRO (TAS-confirmed) ✓ |
| 45 | N5005424FP009 | Metro Machine | USS Eisenhower (CVN 69) FY25 PIA | MRO (strong) ✓ |

Known newbuild controls all classify as Newbuild: Columbia-class ($6.8B across 4 PIIDs), Virginia-class SSN ($17.5B across 13 PIIDs), CVN-80/81 ($2.0B), DDG-51 Flight III + DDG-1000 at BIW and HII ($2.4B). No false positives found in spot-check of top-12 Tier 0 upgrades.

## 5. Impact on the TAM story

### 5.1 Services MRO TAM (current build, pre-PSC 1905)

Unchanged: **$7,067M** FY25 Services MRO TAM across the 68 services PSCs (J/K/N/M/H/L families). This number came from the existing Services sheet methodology and does NOT move.

### 5.2 Reconciled TAM picture including embedded PSC 1905

The deck's "S22 Scope Reconciliation" slide (per `PLAN_deck_revisions.md`) needs to treat PSC 1905 MRO as **inside** the reconciled TAM rather than "adjacent":

| TAM component | Value | Source |
|---|---:|---|
| Services MRO TAM (FY25) | $7,067M | Services sheet, 68 PSCs |
| Embedded PSC 1905 MRO (FY25) | **$1,904M** | This work, `PSC1905_MRO_EMBEDDED` |
| **Reconciled FPDS-visible MRO TAM** | **$8,971M** | Sum of above |

Public naval shipyard NWCF labor (~$7.5B, named range `PUBLIC_SHIPYARD_NWCF`) sits outside FPDS entirely and is a separate reconciliation anchor - not part of the addressable contract market, but critical context for any "total Navy MRO activity" framing.

### 5.3 Deck edits this unblocks

From `PLAN_deck_revisions.md` Step 3:
- **S04 TAM Sizing Approach** - replace $7,067M headline with $8,971M reconciled total.
- **S08 TAM Composition** - denominator shifts from $7,067M to $8,971M; work-segment % shares recalculate; decide whether to add a 6th Marimekko category "Embedded Submarine/Carrier MRO" or footnote the uplift.
- **S11 Marauder-Like Platform TAM** - Submarine + Aircraft Carrier totals grow by ~$1.6B combined (Subs +$1,255M, Carriers +$337M).
- **S22 Scope Reconciliation** - rewrite the PSC 1905 callout from "$1.5-2.0B heuristic range adjacent to TAM" to "$1,904M inside reconciled TAM". Remove "Not double-counted" language.
- **S23 TAM Framing matrix** - Total row increases from $7,067M to $8,971M.

All of the above are deferred to a future session because `deck_script/slide_copy.yaml` + `manifest.json` sources aren't present in `branmut/` - only the built `PA_MRO_Deck_v1.18.pptx` binary.

## 6. Residual uncertainty and caveats

### 6.1 What's still ambiguous

$190M still sits in non-MRO-confirmed buckets:

- **MRO (POP-only) $153M** - 43 PIIDs with short POPs and no MRO keyword. Mostly small (<$10M each) Virginia-class component procurements, LCAC parts, and "OPW - LOT 1/2 CRITICAL SYSTEMS ENGINEERING" entries. Could be MRO (ancillary support for in-service work) or Newbuild (short-POP procurement tasks within the construction envelope).
- **Unclassified $37M** - 6 PIIDs with neither keyword signal nor POP signal. All sub-$10M.

If the true MRO share of these ambiguous dollars is 50%, the Central point moves by ~$95M. That would bring the number to ~$1,999M - still inside the bounds and not materially different for deck purposes.

### 6.2 Known caveats in the classifier

- The $831M Electric Boat Special Hull Treatment Seam Split Repairs line may include some newbuild-program component (hull treatment material for Virginia-class hulls under construction). Classified as MRO based on "repairs" language in the description; full disaggregation would need mod-level review.
- Administrative modifications on newbuild base contracts (e.g., CVN-68 inactivation admin mods) are classified as MRO on the assumption they reallocate funding within an MRO base contract. If they are funding new scope on a newbuild contract, they would still typically be MRO.
- The `industrial base` and `capex` / `capital expenditure` newbuild keywords catch CAPEX incentive PIIDs that award the contractor money to invest in shipbuilding facilities. The $191M BIW CAPEX Incentive PIID classifies as Newbuild (not MRO), which matches the methodology doc's treatment.

### 6.3 What would further narrow the number

1. **Per-mod classification via USAspending `/transactions/`** + Claude LLM. Estimated gain: narrow residual from $190M to ~$50-100M, moving headline by ~$25-50M.
2. **Human review of the 49 residual-bucket PIIDs.** Same precision gain, ~2-3 hours of expert time.
3. **Direct SUPSHIP contract-file access** (not available externally).

None of these are pursued in the current session because the Central point is stable enough for the deck, and additional precision would not change the headline materially.

## 7. How to reproduce

```bash
cd /Users/brendantoole/projects2/branmut

# 1. Re-pull TAS data from USAspending (optional, cached on disk)
python3 -m build_script_slim.pull_psc_1905_funding

# 2. Run the classifier (reads the master JSONs + funding_agg)
python3 -m build_script_slim.psc_1905_classifier

# 3. Rebuild the workbook (reads psc_1905_summary.json)
python3 -m build_script_slim.build_from_data
```

Output artifacts:

- `build_script_slim/output/psc_1905_classified.csv` - per-PIID classification with evidence strings
- `build_script_slim/output/psc_1905_summary.json` - bounds + supergroup rollup (consumed by `reconciliation.py`)
- `build_script_slim/output/psc_1905_funding_agg.json` - USAspending TAS rollup per (PIID, federal_account)
- `build_script_slim/output/08APR2028_MRO_Spend_v4.5.xlsx` - workbook with `PSC1905_MRO_EMBEDDED = $1,904M` on the Reconciliation sheet

Cache (for resumability):

- `data_pull/output/usaspending/funding_psc_1905/*.json` - one file per PIID, raw `/awards/funding/` response

## 8. Critical files

| File | Role |
|---|---|
| `build_script_slim/psc_1905_classifier.py` | 6-tier cascade, headline number |
| `build_script_slim/pull_psc_1905_funding.py` | USAspending fetcher with sequential progress |
| `build_script_slim/vendor/usa_client.py` | USAspending client (symlink into domnann) |
| `build_script_slim/sheets/reconciliation.py` | Wires `PSC1905_MRO_EMBEDDED` named range |
| `data_pull/output/fpds/navy_awards_master.json` | Navy PIIDs (symlink to domnann) |
| `data_pull/output/fpds/cg_awards_master.json` | USCG PIIDs (symlink to domnann) |
| `build_script_slim/output/psc_1905_summary.json` | Classifier output read by workbook builder |

## 9. Related reading

- [OPEN_QUESTION_psc_1905_embedded_mro.md](OPEN_QUESTION_psc_1905_embedded_mro.md) - original problem statement and proposed paths
- [PLAN_deck_revisions.md](PLAN_deck_revisions.md) - Step 2 of this plan is the work documented here; Steps 3-5 (deck edits) remain open
- `domnann/docs/methodology/psc_1905_mro_share.md` - source methodology for the 3-tier keyword cascade

---

*Generated: 2026-04-22. Locked number: $1,904M. Re-run the classifier to refresh if upstream JSONs change.*
