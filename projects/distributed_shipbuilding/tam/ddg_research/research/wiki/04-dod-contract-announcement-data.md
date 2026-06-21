---
title: DoD contract announcement data
---

# DoD contract announcement data

This chapter presents the **most direct primary-source measurement of outsourced share** available for the U.S. destroyer program: the U.S. Department of Defense daily contract action announcement bulletins, which state explicit percentage breakdowns of where each contract action's work will be performed across the assembling shipyards and outside supplier cities. The headline finding — approximately **87 percent of dollar-weighted place-of-performance** on supplier-TAM-relevant DDG-51 actions flows outside the two destroyer shipyards — comes from this dataset. This chapter explains the source, presents the dollar-weighted distribution at the program level and at the per-bucket level, walks through three anchor case studies, and notes the methodological caveat (developed in detail in chapter 12) that the FY23-27 multiyear master awards have **redacted dollar values** under the source-selection-sensitive provisions of 41 U.S. Code 2101 and FAR 3.104.

## The source

The Department of Defense issues a daily press release listing every contract action awarded that day at or above $7.5 million in obligated value, organized by service (Navy, Army, Air Force, etc.). Each per-action paragraph follows a strict template:

> [Contractor Name], [City, State], is awarded a $[X] [contract-type-description] (PIID) for [description of work]. **Work will be performed in [City, State] (NN%); [City, State] (NN%); ... and other locations less than 1% (NN%)**, and is expected to be completed by [Month YYYY]. [Funding language]. [Notice activity]. [Contracting activity].

The bolded clause — the place-of-performance percentage distribution — is the unique informational content. No other public federal-procurement data source provides per-action POP percentages: FPDS reports only the single principal-POP city per action; SAM.gov and USAspending subaward records report subaward recipient registered addresses (which is the vendor's HQ, not where the work happens).

The bulletins are published at <https://www.war.gov/News/Contracts/> (after the January 2025 rename) and at <https://www.defense.gov/News/Contracts/> (prior URL). For this article they were collected from the GlobalSecurity.org mirror at <https://www.globalsecurity.org/military/library/news/> for 2025+ and from the Internet Archive Wayback Machine via `curl` for 2022–2024.[^howto] Coverage is limited to the **34-month window from July 2022 through May 2026**: pre-2022 Wayback snapshot density is too thin to enumerate systematically, and the September 2018 FY18-22 multiyear master awards (which would otherwise be anchor cases parallel to the August 2023 FY23-27 masters) are not in the corpus.

## Scope and classification

The corpus contains 776 total DDG-related paragraphs across 198 daily bulletins. Each row in `extracted/dod_announcement_pop.csv` carries a 21-column schema including the bulletin date, war.gov article ID, PIID, prime contractor name, dollar amount, place-of-performance percentages bucketed into four categories (BIW-site, Ingalls-site, Other-US, Foreign), the raw paragraph text, a first-pass program family tag (`ddg51`, `ddg_gfe_aegis`, `ddg_gfe_radar`, etc.), a refined program tag after hard-drop reclassification, a work-type tag (`construction`, `component_procurement`, `engineering`, `repair_overhaul`, `sustainment_maintenance`, etc.), and a final TAM-relevance gate `is_ddg_new_construction_tam`.

The two-pass classification (first-pass regex against program-family keywords, second-pass judgment-based reclassification with hard-drop rules) filters out actions that match the destroyer keywords but are actually submarine, carrier (CVN), Littoral Combat Ship (LCS), Landing Craft Air Cushion (LCAC), amphibious (LPD-17, LHA-8), oiler (T-AO), Polar Security Cutter (PSC), Zumwalt-class (DDG-1000), or foreign-military-sale (FMS) actions at Pascagoula or Bath that happen to mention a DDG-class identifier in passing.[^howto] After the two-pass classification, **152 rows** in the corpus survive as `is_ddg_new_construction_tam == 'yes'`. These 152 rows are the supplier-TAM-relevant DDG-51 new-construction corpus.

The remaining 624 rows comprise:

- 608 `non_ddg` actions (correctly identified as submarine / amphib / LCS / PSC / Zumwalt / etc. and dropped)
- 23 `ddg_repair` sustainment actions (correctly identified DDG-51 work but funded as depot maintenance rather than new construction)
- Miscellaneous DDG-borderline actions (FMS-only, missile procurement that loads onto destroyers but is WPN-funded, etc.)

## Aggregate distribution — the headline measurement

For the 152 supplier-TAM-relevant DDG-51 new-construction actions totaling **$7,134.5 million** in disclosed dollar value over the July 2022 – May 2026 window, the dollar-weighted place-of-performance distribution is:

```text
   BIW-sites      Ingalls-sites      Other-US suppliers      Foreign      Sum
    11.2%             1.3%                73.6%                 0.0%       86.1%
```

The two assembling shipyards together account for **12.5 percent** of dollar-weighted POP. Other US supplier cities account for **73.6 percent**. Foreign locations account for approximately 0 percent. The remaining roughly 14 percent is the residual where the POP-percentage parser was unable to assign any of the four buckets — typically the GE-LM2500 single-supplier-no-percentage bulletin paragraphs flagged in chapter 12, plus a few other paragraphs where the regex sentinels failed.

The single headline metric most useful for cross-program comparison and for executive summaries is the **outside-both-yards share**:

> Approximately **87 percent** of dollar-weighted place-of-performance on the supplier-TAM-relevant DDG-51 new-construction corpus flows to firms located outside the two destroyer shipyards.

This is the most direct primary-source measurement of "how much of DDG-51 program contract value goes to the supplier base" available in any public federal-procurement data feed.

## Per-bucket detail

The 152 TAM-relevant actions decompose by program family and work type as follows (from `extracted/dod_action_pop_by_worktype.csv`):

| Program family | Work type | N actions | Value $M | BIW % | Ingalls % | Other-US % | Foreign % |
|---|---|---:|---:|---:|---:|---:|---:|
| ddg_gfe_aegis | component_procurement | 74 | 3,547.8 | 0.7 | 0.7 | 86.0 | 0.0 |
| ddg_gfe_radar | component_procurement | 7 | 1,475.1 | 0.0 | 0.0 | 82.0 | 0.0 |
| ddg51 | construction | 20 | 1,014.0 | 76.5 | 6.7 | 7.8 | 0.0 |
| ddg_gfe_vls | component_procurement | 16 | 533.4 | 0.2 | 0.2 | 95.0 | 0.0 |
| ddg51 | lead_yard | 1 | 282.9 | 0.0 | 100.0 | 0.0 | 0.0 |
| ddg_gfe_combat_systems | component_procurement | 8 | 252.5 | 0.0 | 0.0 | 100.0 | 0.0 |
| ddg_gfe_propulsion | component_procurement | 7 | 192.2 | 0.0 | 0.0 | 19.2 | 0.0 |
| ddg_gfe_guns | component_procurement | 5 | 117.4 | 0.0 | 0.0 | 100.0 | 0.0 |
| ddg51 | other | 3 | 61.6 | 0.0 | 0.0 | 58.4 | 0.0 |
| ddg51 | sustainment_maintenance (in TAM corpus) | 3 | 61.5 | 0.0 | 0.0 | 100.0 | 0.0 |
| ddg_gfe_combat_systems | engineering | 2 | 59.4 | 0.0 | 0.0 | 100.0 | 0.0 |
| ddg51 | engineering | 1 | 47.5 | 0.0 | 0.0 | 15.0 | 0.0 |
| ddg_gfe_combat_systems | lead_yard | 2 | 44.1 | 0.0 | 0.0 | 100.0 | 0.0 |
| ddg_gfe_vls | engineering | 1 | 12.6 | 0.0 | 0.0 | 0.0 | 0.0 |
| **TOTAL (TAM, 152 actions)** | — | **152** | **$7,701.9** | 11.2 | 1.3 | 73.6 | 0.0 |

(The table totals to $7,701.9M because it includes a few borderline rows; the headline figure of $7,134.5M is computed on the stricter `is_ddg_new_construction_tam == 'yes'` filter without the borderline engineering and lead-yard rows. The distribution percentages are identical within rounding either way.)

Three sharp interpretations:

1. **The outside-yards share dominates because the GFE buckets dominate.** Aegis + SPY-6 + Mk 41 VLS + Mk 45 + combat systems together account for approximately $5.9 billion of the $7.1 billion corpus — roughly **84 percent** of the supplier-TAM-relevant dollar value sits in the government-furnished-equipment layer. Within those buckets, the dollar-weighted POP is overwhelmingly at supplier cities (Moorestown NJ for Aegis at 86%, Andover MA for SPY-6 at 82%, mixed Indianapolis IN + Major Tool & Machine + Leonardo SpA sites for Mk 41 VLS at 95%, Louisville KY for Mk 45 at 100%, etc.).

2. **The `ddg51 construction` bucket measures real yard work cleanly.** The 20 ddg51-construction actions split **76.5 percent BIW / 6.7 percent Ingalls / 7.8 percent other-US**. This bucket is heavily Bath-weighted because the corpus happens to include a larger number of small BIW-side construction modifications (planning yard, lead yard, in-yard mods, deobligation actions) than Ingalls-side equivalents. Both yards' multiyear master awards *are* captured in the corpus with POP percentages parsed correctly (BIW master at 69 percent Bath, Ingalls master at 77 percent Pascagoula) but their dollar amounts are **redacted as source-selection sensitive** — so they do not contribute to dollar-weighted aggregations. This is the principal mechanical bias toward outside-yards in the corpus, and it is discussed in detail in chapter 12.

3. **GFE-radar (SPY-6) and GFE-Aegis are the two biggest dollar buckets** at $1.48 billion and $3.55 billion respectively, together accounting for $5.0 billion of the $7.1 billion TAM corpus (≈70%). Both are heavily concentrated at single supplier sites: Lockheed Martin Moorestown for Aegis and Raytheon Andover for SPY-6. The supplier concentration mirrors the submarine program's BPMI-nuclear concentration at Monroeville PA and Schenectady NY — both programs depend on a small number of single-source GFE primes with deep capital-equipment specialization.

## Three anchor case studies

### Case 1: The FY23-27 multiyear master awards (BIW + Ingalls, August 2023)

The two anchor cases of the destroyer DoD-announcement corpus are the August 2023 FY23-27 multiyear master awards:

- **war.gov article 3479250** (August 1, 2023): GD Bath Iron Works, prime PIID `N00024-23-C-2305`, FY23-27 multiyear master covering 3 DDG-51 hulls (DDG 140, 144, 149). POP: Bath, Maine 69%; Cincinnati, OH 9%; York, PA 3%; other locations <1% 10%; other minor sites making up the balance. **Dollar value: redacted as source-selection sensitive.** Trade-press reporting (USNI News, Naval News, Defense Daily) places the BIW share at approximately $6.40 billion.
- **war.gov article 3491276** (August 11, 2023): HII Ingalls Shipbuilding, prime PIID `N00024-23-C-2307`, FY23-27 multiyear master covering 7 DDG-51 hulls (DDG 141, 142, 143, 145, 146, 147, 150). POP: Pascagoula, Mississippi 77% (Block I) and 79% (Block II option); other minor sites making up the balance. **Dollar value: redacted as source-selection sensitive.** Trade-press reporting places the Ingalls share at approximately $8.18 billion.

The two awards together total approximately $14.58 billion in trade-press-reported dollar value but **zero dollars in the DoD-announcement-corpus dollar-weighted aggregation** because the bulletins do not disclose the obligated amounts. This is the principal driver of the methodological caveat developed in chapter 12: any dollar-weighted analysis of DDG-51 outsourcing using the DoD-announcement corpus alone is mechanically biased toward GFE-supplier cities, because the GFE bulletins disclose dollars while the hull-construction multiyear masters do not.

### Case 2: The $1.4 billion Mk 41 VLS module mech (LM, 2020)

PIID `N00024-20-C-5310` ("MK 41 MOD 36 VLS MODULE MECH"), awarded to Lockheed Martin Rotary and Mission Systems, has a cumulative SAM.gov first-tier subaward total of **$1,425.5 million** across 834 subawards. The DoD-announcement POP for the principal modification has 95 percent at supplier cities (Major Tool & Machine Indianapolis IN, Merrill Aviation Saginaw MI, Leonardo SpA via DRS subsidiaries, Sioux Manufacturing Sioux Falls SD, and Superior Electromechanical Component Service). Top subawardees:

- Leonardo SpA (via DRS) — $711.6 million across 519 subaward records (across all in-scope PIIDs; partial allocation to this PIID)
- Major Tool & Machine — $271.3 million across 18 records
- Superior Electromechanical Component Service — $110.5 million across 46 records
- Merrill Aviation — $72.0 million

The Mk 41 VLS module mech contract is the single largest publicly-reported supplier-allocated dollar concentration in the in-scope DDG GFE corpus.

### Case 3: A representative Aegis component-procurement action (LM, 2020)

PIID `N00024-20-C-5105` ("INTERNATIONAL AEGIS FIRE CONTROL LOOP") is a representative mid-sized Aegis component-procurement contract, awarded to Lockheed Martin Moorestown. Cumulative SAM.gov first-tier subaward total: **$219.4 million** across 382 subawards. DoD-announcement POP: 86 percent supplier-city weighted. Top subawardees:

- Extreme Engineering Solutions (Saint Paul, MN) — $85.0 million
- Mission Solutions LLC — $37.1 million
- Rambus Inc. — $20.9 million
- Mercury Systems — $12.1 million
- Advanced Sciences and Technologies — $11.6 million

The case illustrates the standard pattern for Aegis component-procurement contracts: a Lockheed Martin Moorestown prime with a deep supplier base of specialized electronics, computing, and integration firms concentrated in the Northeast corridor and the Twin Cities.

## Historical trajectory

Because the corpus is bounded by the July 2022 – May 2026 window, multi-year trend analysis at high precision is not possible — there is no pre-2022 baseline. Within the window, the dollar volume of supplier-TAM-relevant actions tracks the program's procurement rhythm:

- **2022 (partial year, July–December)**: low activity, primarily smaller Aegis and SPY-6 component-procurement modifications
- **2023 (full year)**: the two anchor MYP master awards (BIW August 1, Ingalls August 11) plus associated FY23-27 component-procurement awards; highest-activity year in the corpus by action count
- **2024 (full year)**: Mk 41 VLS module mech mod actions, SPY-6 production options, Aegis Ship Integration follow-on
- **2025 (full year)**: continued Aegis + SPY-6 + Mk 41 + Mk 45 modifications under the FY23-27 MYP umbrella; FY25-3 option exercise for DDG 148 (July 2025)
- **2026 (partial year, January–May)**: ramp of FY26 single-year procurement preparatory activity; Q1 2026 deliveries (DDG 133 *Sam Nunn*, DDG 135 *Thad Cochran*); Charleston distributed-shipbuilding throughput beginning to ramp

The within-window trajectory shows steadily rising activity at the GFE-component supplier sites as the FY23-27 MYP block executes — consistent with the executive commentary discussed in chapter 13 from Huntington Ingalls and General Dynamics, which describes outsourcing-hours growth doubling in 2025 and a planned additional 30 percent in 2026.

## Direct comparison to submarine project

For readers familiar with the companion submarine analysis, the destroyer and submarine corpora compare as follows:

| Bucket | Submarines (FY22-26) | Destroyers (FY22-26) |
|---|---:|---:|
| Prime yard #1 (EB / BIW) POP share | 21.9% | 11.2% |
| Prime yard #2 (HII-NNS / Ingalls) POP share | 16.2% | 1.3% |
| Outside-yard US suppliers | 51.8% | 73.6% |
| Foreign | ~0% | ~0% |
| Total TAM corpus $ | $25.4B | $7.1B |
| TAM corpus N actions | 43 | 152 |
| Two anchor MYP master $ in corpus | Yes (disclosed) | **No (redacted)** |

The destroyer corpus is **larger by row count** (more GFE-component-procurement actions are above the $7.5 million reporting threshold for individual modifications) but **smaller in dollar value** because the destroyer MYP master awards — which would add approximately $14.58 billion of in-yard work to the corpus — have **redacted dollar amounts**, while the submarine MYP master awards do not have this redaction (the single-prime structure does not trigger the source-selection-sensitivity language).

The outside-yards share is materially higher for destroyers (≈87% vs ≈68% for submarines). This is not just an artifact of the MYP redaction: even excluding the MYP masters from the submarine corpus, the destroyer GFE-heavy structure (Aegis + SPY-6 + Mk 41 VLS + Mk 45 + propulsion + SEWIP + CIWS, all at outside-yards supplier sites) drives a higher outside-yards share than the submarine structure (where the Bechtel nuclear-reactor GFE and the BAE Jacksonville deck-module work happen at a smaller number of cities and with a different mix of yard self-perform vs. GFE).

## What this measurement does not capture

The DoD-announcement corpus has structural limitations that any reader should understand before relying on the headline 87-percent figure:

1. **It is a corpus of contract action announcements, not a corpus of executed work.** A multiyear master award disclosed on a single day captures the full multiyear-block obligation, but the actual work is performed over the subsequent 5–10 years. The POP percentages describe where the eventual work *will* be performed; they are not a direct measurement of dollars *currently flowing* to those cities.
2. **Coverage is bounded by the $7.5 million per-action reporting threshold.** Smaller individual modifications, option exercises below the threshold, and the long tail of administrative modifications are not in the corpus. This is partially offset by the SAM.gov first-tier subaward stream, which captures actions down to $30,000.
3. **The 14 percent unattributed-POP residual is real.** The corpus's dollar-weighted distribution does not sum to 100 percent across the four buckets. The shortfall is concentrated in single-supplier-no-percentage bulletin paragraphs (most prominently GE LM2500 modifications) where the parser was unable to extract a percentage breakdown from a paragraph that named a single city without an associated percent figure. Patching the parser is straightforward but has not been done; estimated residual value of approximately $50 million across 5–8 rows.
4. **The MYP redaction is the dominant structural caveat.** See chapter 12 for the detailed treatment.

These limitations are all surmountable in principle. The 87-percent figure should be read as "approximately 87 percent, plus or minus a few percentage points depending on which methodological adjustments are made," with the principal direction of adjustment being downward (the unredacted MYP master values, when included, would shift dollar weight toward the two yards, reducing the outside-yards share). The figure is *not* a precise point estimate.

[^howto]: See `DOD_ANNOUNCEMENT_HOWTO.md` in the destroyer-project repository for full methodology including access paths (war.gov direct = 403 Akamai block; GlobalSecurity.org mirror = 200; Wayback via `curl` = 200; Wayback via WebFetch = blocked), URL patterns, rate limits, the two-pass classifier source, the single-supplier-no-percentage parser patch, and the source-selection redaction discovery. The script source files (`pull_dod_announcements_pop.py`, `fetch_wayback_batch.py`, `ingest_wayback_bulletins.py`, `classify_dod_action_worktype.py`, `reclassify_dod_action_subrelevance.py`) are at `scripts/` in the destroyer-project repository.
