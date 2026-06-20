# PSC 1905 Embedded MRO Share -- FY2025 Navy + USCG

**Headline:** ~$1.5-2.0B of the $38.1B FY2025 PSC 1905 Navy + USCG
obligations is MRO-character work bundled under the shipbuilding PSC,
not new construction. Midpoint estimate: **~$1.7B (4.4% of PSC 1905)**.

**Purpose:** Quantifies the "est. $X" placeholder in Slide 3 (Scope
Reconciliation) bottom-left cell and RHS callout card #3 of
`deck/MRO_DECK_v1.5_RECONCILIATION_SPEC.md`. Backs the load-bearing
claim that the $7.1B Services MRO TAM is a floor, not a ceiling, on
submarine and carrier MRO activity visible in FPDS.

## Starting number

| Metric | Value |
|---|---|
| PSC 1905 rows, Navy + USCG, FY2025-active | 201 |
| FY2025 obligation sum | $38,053M |
| Total obligation (all years) | $191,536M |
| Base and all options | $247,545M |

Source: `data_pull/output/fpds/navy_awards_master.json` +
`cg_awards_master.json`, filter `psc_code == '1905'` and
`fy2025_obligation != 0`.

## Classification method

Each PIID was tagged using a three-tier cascade:

1. **Strong MRO keyword** in description and no newbuild keyword ->
   `MRO (strong)`. Keywords: `engineered overhaul`, `RCOH`, `DSRA`,
   `selected restricted availability`, `extended drydocking`, `EDSRA`,
   `depot maintenance`, `inactivation`, `post shakedown`, `DPIA`,
   `CNO availability`, `drydock`, `restricted availability`,
   `seam split repair`, `hull treatment`, `PIA`, `PSA`,
   `availability`.

2. **Newbuild keyword or newbuild hull name** -> `Newbuild`. Keywords:
   `detail design`, `DD&C`, `long lead time material`, `advance
   procurement`, `lead yard services`, `nuclear components`,
   `drawing updates`, `balance testing`, `propulsion plant`,
   `fabrication`, `first article`, `class design`, `supplier
   development`, `industrial base`, `CAPEX incentive`, `WLR`, `WLIC`.
   Newbuild hulls: LHA 8/9, CVN 80/81, DDG 126-133, SSN 810-815,
   SSBN 826-828 (Columbia), LPD 30-33, FFG 62-65, T-AO 209-211,
   ESB / EPF variants.

3. **Soft MRO keyword + POP <= 3 years** and no newbuild signal ->
   `MRO (probable)`. Soft keywords: `overhaul`, `maintenance`,
   `repair`, `emergent`, `modernization`, `growth work`, `condition
   report`, `labor support`, `midlife`.

4. **POP <= 2 years** with no keyword -> `MRO (POP-only)`.

5. **POP >= 4 years** with no keyword -> `Newbuild (POP-only)`.

6. Remainder -> `Unclassified`.

Newbuild-hull and newbuild-keyword signals override all MRO signals.
Rationale: a contract whose description mentions LHA 9 or "DD&C" is
fundamentally newbuild work even if the contract also includes
incidental condition-report or growth-work line items.

## Results

| Bucket | N rows | FY2025 $M | % of PSC 1905 |
|---|---:|---:|---:|
| Newbuild (keyword or hull) | 21 | 25,963 | 68.2% |
| Newbuild (POP-only) | 58 | 9,959 | 26.2% |
| MRO (strong) | 15 | 1,565 | 4.1% |
| MRO (POP-only) | 76 | 288 | 0.8% |
| Unclassified | 14 | 182 | 0.5% |
| MRO (probable) | 17 | 95 | 0.3% |
| **Total** | **201** | **38,053** | **100.0%** |

**Embedded MRO bounds:**

| Bound | Method | $M |
|---|---|---:|
| Conservative | MRO (strong) only | $1,565M |
| Central | MRO (strong) + MRO (probable) | $1,660M |
| Upper | + MRO (POP-only) | $1,949M |

**Cited in deck:** ~$1.5-2.0B (range), midpoint ~$1.7B.

## MRO share by vessel_supergroup

| Vessel supergroup | PSC 1905 total $M | Embedded MRO $M | MRO share |
|---|---:|---:|---:|
| Submarines | 24,279 | 1,255 | 5.2% |
| Aircraft Carriers | 1,431 | 319 | 22.3% |
| Surface Combatants | 5,653 | 48 | 0.8% |
| Amphibious Warfare Ships | 1,644 | 0 | 0.0% |
| unclassified | 3,471 | 39 | 1.1% |
| Combatant Crafts | 957 | 0 | 0.0% |
| Multi-class | 534 | 0 | 0.0% |
| Unmanned Maritime Platforms | 83 | 0 | 0.0% |

**Key read:** submarine and carrier PSC 1905 contracts are where the
bulk of the embedded MRO lives. Surface combatants and amphibs in PSC
1905 are predominantly newbuild (DDG-51 Flight III, FFG-62
Constellation, DDG-1000, LHA 8/9, LPD 30-33).

## Top MRO-character PIIDs (verification)

| $M | Recipient | Vessel | Description |
|---:|---|---|---|
| 831 | Electric Boat | Submarines | FLEET DIRECTED WORK: SPECIAL HULL TREATMENT (SHT) SEAM SPLIT REPAIRS |
| 424 | HII | Submarines | USS BOISE (SSN 764) ENGINEERED OVERHAUL EXECUTION |
| 97 | HII | Aircraft Carriers | CVN 68 INACTIVATION AP EMERGENT |
| 60 | HII | Aircraft Carriers | Administrative mod on CVN 68 inactivation contract |
| 45 | Metro Machine | Aircraft Carriers | USS EISENHOWER (CVN 69) FY25 PIA |
| 28 | HII | Aircraft Carriers | CVN 68 CLASS INACTIVATION PLANNING |
| 25 | BAE Jacksonville | Surface Combatants | LCS 25 POST SHAKEDOWN AVAILABILITY |
| 23 | BAE Norfolk | Surface Combatants | PSA FOR HARVEY BARNUM JR. (DDG 124) |
| 13 | HII | Aircraft Carriers | Admin mod on CVN inactivation contract |
| 11 | HII Fleet Support | Aircraft Carriers | ELEVATOR SUPPORT UNIT to support CVN 74 |

**Read:** the top two items ($831M EB Seam Split Repairs, $424M Boise
Engineered Overhaul) account for $1,255M of the $1,565M strong-MRO
total. Both are private-yard submarine depot work at Newport News and
Groton that is coded as shipbuilding rather than as J998 / J999
because the contracting office (NAVSEA's Supervisor of Shipbuilding,
Conversion, and Repair) administers both construction and major
overhaul work at the shipbuilder-yards under a single set of PSC
codes.

## What this means for the deck

1. **Slide 3 bottom-left cell**: replace "est. $X of nuclear
   engineered overhauls and depot work bundled as shipbuilding" with
   "est. ~$1.5-2.0B of engineered overhauls and depot work bundled
   as shipbuilding (mostly nuclear; see methodology doc)".

2. **Slide 3 RHS callout card (bottom-left explanation)**: cite the
   Boise EOH ($424M) and the EB Seam Split Repairs ($831M) as the
   two largest examples.

3. **Floor-vs-ceiling argument**: The Services TAM has $838M for
   Submarines and $422M for Aircraft Carriers. Adding the
   PSC-1905-embedded MRO gives a more complete contracting-market
   picture: Submarines ~$2.1B, Aircraft Carriers ~$0.7B. Even this
   remains a floor on total nuclear MRO because public-yard NWCF
   labor (Portsmouth, Puget Sound, Pearl Harbor) is outside FPDS
   entirely (see Slide 3 top-right cell).

4. **Methodology defensibility**: this analysis is itself evidence
   for the v1.5 awards-first framing. PSC-level classification alone
   (the only cut available to a budget-first methodology) would miss
   all of this -- PSC 1905 would have been tagged as "newbuild" in
   full, and the MRO TAM would have lost the entire $1.5-2.0B.
   Recovering it required PIID-level description parsing + POP-length
   + vendor-pattern analysis, which is only possible on awards data.

## Caveats

1. The $831M EB Special Hull Treatment line could have a
   newbuild-program component (hull treatment material procurement
   for Virginia-class hulls under construction). Examining the
   contract modification history in depth would be needed to
   disaggregate. For now classified as MRO based on "repairs"
   language in the description.

2. The $60M and $13M "administrative modifications" on CVN-68
   inactivation contracts are classified as MRO on the assumption
   that they reallocate funding within an MRO base contract. If
   they are funding new scope, they would still be MRO.

3. Borderline cases in the MRO (POP-only) bucket (Birdon WLIC/WLR,
   HII Fleet Support labor support) were reviewed and moved to
   Newbuild (Birdon) or kept as Probable MRO (HII Fleet Support)
   based on the strongest signal in the description. Further
   disambiguation would require reading each contract; impact on
   headline is < $100M.

## Reproducibility

Script: ad-hoc Python analysis over `navy_awards_master.json` +
`cg_awards_master.json`. Result: `$1,565M - $1,949M` range with
central estimate `$1,660M`. To rerun: filter master files to
`psc_code == '1905'` and apply the three-tier cascade above.

Generated: 2026-04-20 (walk-in build session for v1.5 deck).
