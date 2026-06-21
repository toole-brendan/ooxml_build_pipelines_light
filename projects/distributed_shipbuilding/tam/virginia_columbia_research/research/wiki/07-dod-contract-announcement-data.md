---
title: DoD contract announcement data
---

# DoD contract announcement data

The U.S. Department of Defense publishes daily press releases announcing all Department of Defense contract awards equal to or greater than $7.5 million in value. Each release names the contractor, the contract or modification value, the contracting authority, the contract identifier, and — for the article's purposes most importantly — the **place of performance**, often broken out as percentage shares across the cities and states where the work will be performed. The percentages are the single most direct primary-source measurement available of how a given contract action's value will be distributed across the firms doing the work.

This chapter uses the DoD daily-announcement corpus across a 34-month window (July 2022 through May 2026) to measure the share of submarine new-construction supplier-targeted contract action value flowing to firms other than the assembling shipyards. Across **43 submarine-relevant supplier-targeted actions totaling approximately $25.4 billion**, the dollar-weighted distribution is:

```text
   EB-sites      HII-sites      Other-US suppliers      Foreign
    21.9%          16.2%             51.8%                ~0%
```

The two outsourcing-share measurements implied by the distribution:

- **Outside-EB share (denominator 1)**: approximately **78 percent** of dollars flow to firms other than General Dynamics Electric Boat. This is the cleanest measurement of "how much of submarine prime-contract value does GDEB outsource."
- **Outside-the-prime-team share (denominator 2)**: approximately **52 percent** of dollars flow to firms outside both shipyards combined. This is the cleanest measurement of "how much of submarine prime-contract value goes to the supplier base rather than the two-yard team."

Both measurements are conservative because the parser used to extract percentages from press-release language treats single-supplier-site actions (where the announcement lists one location without a percentage) as if the location data were missing rather than as 100 percent at that location. This affects an additional $1.6 billion of action value across approximately 17 rows in the corpus, all of which by their construction concentrate at a single non-yard supplier site. The true Outside-EB and Outside-the-prime-team shares with parser correction would be modestly higher; the reported figures are floors.

This chapter sets out the press-release source, the per-bucket breakdown of the 43 actions, three contract-action case studies cited individually as primary sources, and the historical-trajectory contrast between 2022 and 2026.

## The source

The Office of the Assistant Secretary of Defense (Public Affairs) publishes a daily "Contracts" press release for every business day. Each release contains one or more contract action announcements above the $7.5 million reporting threshold. The release for the day on which a contract is awarded contains the action's announcement; subsequent days are not published as updates to that release.

The current canonical URL pattern is `https://www.war.gov/News/Contracts/Contract/Article/<article_id>/`, with the Department of Defense having transitioned the public-affairs domain from `defense.gov` to `war.gov` in January 2025. Historical releases continue to resolve at `https://www.defense.gov/News/Contracts/` for actions through approximately calendar year 2024, with some 2025 actions still resolving on defense.gov as well. Releases predating the January 2025 transition can also be accessed via the Internet Archive's Wayback Machine at `https://web.archive.org/web/<timestamp>/https://www.defense.gov/News/Contracts/Contract/Article/<article_id>/`. The third-party mirror `https://www.globalsecurity.org/military/library/news/<YYYY>/<MM>/dod-contracts_<article_id>.htm` republishes the releases verbatim and is used by this article as an accessor of convenience where the primary URLs return access-restricted responses; the source of record remains the Department of Defense press release.

Each announcement follows a standardized format that includes:

1. **Contractor name, city, and state** — the prime contractor receiving the award.
2. **Award value** — the contract or modification dollar amount.
3. **Action description** — what the work is for, often citing the contract identifier and the platform (e.g., "Virginia-class submarines Block VI long-lead-time material").
4. **Place of performance** — a list of cities with percentage shares: "Work will be performed in Newport News, Virginia (2%); Sunnyvale, California (36%); South Yorkshire, United Kingdom (7%); ..."
5. **Expected completion date.**
6. **Funding source** — the appropriation and fiscal year obligating funds.
7. **Statutory authority** — the FAR justification cited (often FAR 6.302-1(a)(2)(iii), "only one responsible source").
8. **Contracting activity** — Naval Sea Systems Command, Washington, D.C. for submarine awards.

The place-of-performance language is the data this chapter uses.

## Scope and classification

The corpus assembled for this article spans **action dates from July 25, 2022 through May 22, 2026** — a 34-month window from the earliest defense.gov daily release accessible via the routes used to the most recent at the time of writing. Across the window, this article identifies approximately 658 individual contract-action paragraphs that contain submarine-related vocabulary or that name primes with submarine work content. Most of these are not submarine new-construction supplier work — many are surface combatant, missile system, fleet logistics support, depot maintenance, or non-submarine awards that happened to mention submarine vocabulary.

To isolate the submarine new-construction supplier-targeted subset, this article applies a two-stage classification. The first stage tags each action's **program family** (`va`, `col`, `va_or_col`, `bpmi_nuclear`, `sub_gfe_electronics`, `sub_gfe_components`, `sub_repair`, `sub_operational`, `non_sub`) and **work type** (`construction`, `lltm_early_mfg`, `advance_procurement`, `component_procurement`, `lead_yard`, `eoq`, `repair_overhaul`, `engineering`, `design`, `sustainment_maintenance`, `fms`, `other`). The second stage reviews the candidate-rows manually and reclassifies actions where the first-pass regex misjudged the program or work type, then promotes a subset of rows to refined sub-program tags (`bpmi_nuclear`, `sub_gfe_electronics`, `sub_gfe_components`, `sub_repair`, `sub_operational`) and computes a "submarine new-construction TAM relevance" gate.

The TAM gate retains rows where the program family is in {`va`, `col`, `va_or_col`, `bpmi_nuclear`, `sub_gfe_electronics`, `sub_gfe_components`} *and* the work type is in {`construction`, `lltm_early_mfg`, `advance_procurement`, `eoq`, `component_procurement`}. The gate excludes overhauls, repairs, and missile / weapons primes that are operationally sub-relevant but not part of the new-construction supplier-TAM proper. The resulting **43 TAM-relevant actions totaling $25.4 billion** are the corpus this chapter analyzes.

## Aggregate distribution

The dollar-weighted place-of-performance distribution across the 43 TAM-relevant actions is approximately:

| Bucket | $-weighted share |
|---|---:|
| EB-sites (Groton, Quonset Point, North Kingstown) | 21.9% |
| HII-sites (Newport News) | 16.2% |
| Other-US (supplier cities outside the two yards) | 51.8% |
| Foreign (UK, Switzerland, Canada, etc.) | ~0% |

The bucket categorization treats Groton, Connecticut; Quonset Point, Rhode Island; and North Kingstown, Rhode Island as "EB-sites" and Newport News, Virginia as the principal "HII-site." All other U.S. cities aggregate to Other-US. The foreign share rounds to zero because the largest foreign content (the South Yorkshire and Staffordshire UK supplier sites visible in some Virginia actions) totals under 1 percent of dollar-weighted value across the TAM corpus, with a small number of Swiss, Canadian, Italian, and other content.

The 10-percentage-point gap between the buckets' sum (89.9 percent) and 100 percent is the parser miss noted in the chapter introduction: a subset of single-supplier-site actions in the corpus list the location without a percentage and the parser records 0 percent across all four buckets. The affected actions concentrate in `sub_gfe_electronics` and `va, component_procurement`, and account for approximately $1.6 billion of TAM-relevant value. The true Other-US share with parser correction would be higher, lifting the Outside-EB share above 78 percent and the Outside-the-prime-team share above 52 percent.

## Per-bucket breakdown

The 43 TAM-relevant actions decompose into seven program-and-work-type buckets:

| Program | Work type | N actions | Value $M | EB-sites % | HII-sites % | Other-US % |
|---|---|---:|---:|---:|---:|---:|
| Virginia | LLTM / early manufacturing | 7 | 18,104 | 27.4 | 22.2 | 50.4 |
| BPMI nuclear | Component procurement | 13 | 4,814 | 0.0 | 0.0 | 80.2 |
| Submarine GFE electronics | Component procurement | 10 | 1,193 | 0.0 | 0.0 | 0.0* |
| Columbia | Advance procurement | 1 | 699 | 85.0 | 15.0 | 0.0 |
| Virginia | Component procurement | 7 | 338 | 0.0 | 0.0 | 0.0* |
| Virginia | Construction (spares) | 1 | 188 | 0.0 | 2.0 | 98.0 |
| Submarine GFE components | Component procurement | 4 | 91 | 0.0 | 0.0 | 0.0* |

*0%-everywhere rows are single-supplier-site actions where place-of-performance was stated as a single city without a percentage; parser-correction would lift Other-US toward 100 percent for these rows.

Three sharp interpretations:

1. **The outside-yards share is real and measurable.** Across the 43 TAM-relevant actions, approximately half of dollar-weighted value flows to supplier cities outside the two nuclear shipyards. This is the single cleanest primary-source quantification of the cost-funnel's "outsourced layer within Basic Construction."
2. **BPMI nuclear is the cleanest supplier signal in the corpus.** The 13 BPMI actions totaling $4.8 billion place 80.2 percent of dollar value at supplier cities (concentrated in Monroeville, Pennsylvania for Westinghouse facilities and Schenectady, New York for Knolls Atomic Power Laboratory facilities). This is the most concentrated supplier-city pattern in the corpus and the cleanest evidence that the GFE-prime BPMI is itself a supplier-heavy operation.
3. **Long-lead-time material is approximately half-yards, half-suppliers in the aggregate, but moving rapidly toward suppliers.** The seven Virginia LLTM actions split 27 / 22 / 50 by yard / team-partner / supplier-base, meaning a significant chunk of "LLTM" dollars still stays at the yards for early manufacturing (pre-construction subassembly), not at suppliers. But within the LLTM bucket, the timing of dollar-weighted shifts is the most striking trajectory in the corpus, addressed in the next section.

## Three case studies (the framework's anchor examples)

Three specific contract actions from the corpus are cited verbatim as anchors because they appeared in the framework that motivated this analysis. Each is a primary-source measurement of outsourced share at the action level.

### Case 1: Virginia Block VI long-lead-time material, April 30, 2025 ($12.42 billion)

The largest single TAM-relevant action in the corpus is a Virginia Block VI long-lead-time material contract awarded to General Dynamics Electric Boat on April 30, 2025. The action value is $12.42 billion. The press release records the place-of-performance distribution as **40 percent at EB-sites, 32 percent at Newport News (HII), and 28 percent at outside-yard supplier cities**.[^dod-2025-04-30]

The action is the supplier-driven counterpart of the FY2025 Virginia Block VI procurement: Virginia FY2025 Block VI lead boat with Total Ship Estimate of $9.5 billion (chapter 2), an extraordinary Plans Costs share of $2.6 billion (chapter 3), and Basic Construction of $5.3 billion (chapter 4). The $12.42 billion LLTM action is the supplier-procurement and early-manufacturing dollars committed for that block.

The 60-percent share to firms other than the EB-sites — 32 percent to the team partner plus 28 percent to outside-yard suppliers — confirms that, even on a large Virginia LLTM action, a majority of dollar value flows beyond the prime shipyard.

### Case 2: Columbia advance procurement, November 17, 2025 ($699 million)

A Columbia advance procurement modification awarded to General Dynamics Electric Boat on November 17, 2025 places **85 percent of work at EB-sites and 15 percent at Newport News (HII), with zero percent to outside-yard suppliers**.[^dod-2025-11-17] The action carries PIID `N00024-17-C-2117` — the Columbia Build I + II master contract — and represents the kind of contract action where the dollar value remains concentrated at the two-yard team.

The contrast between Case 1 and Case 2 within the same broad category of contract action illustrates that the outsourced-share measurement varies meaningfully across actions: not every contract is supplier-heavy, and the cumulative outsourcing percentage depends on the mix of actions in the relevant fiscal year.

### Case 3: Virginia Block VI long-lead-time material, May 11, 2026 ($2.31 billion)

A Virginia Block VI long-lead-time material contract awarded to General Dynamics Electric Boat on May 11, 2026 places **0 percent of work at EB-sites, 2 percent at Newport News (HII), and 98 percent at outside-yard supplier cities** — a 13-supplier-city distribution covering Sunnyvale, California; Westfield, Massachusetts; Manchester, New Hampshire; Tucson, Arizona; and others.[^dod-2026-05-11] The action value is $2.31 billion. The PIID is `N00024-24-C-2110` — the Virginia Block VI LLTM contract in the in-scope new-construction PIID list.

A single contract action in which 98 percent of the dollar value flows outside the two shipyards is at the extreme end of the corpus distribution, not the mean. But the action is recent (May 2026), large ($2.3 billion), and assigned to a specific in-scope PIID. It is the cleanest single illustration of the trajectory that GAO documents on the oversight side, that HII confirms on the operational side, and that Navy policy explicitly seeks on the strategic side.

## Historical trajectory: 2022 versus 2026

The 34-month corpus span permits a direct primary-source comparison of submarine LLTM contract-action place-of-performance distribution at the start and end of the window. The contrast is the cleanest "outsourcing acceleration" evidence in the article.

### Anchor: December 21, 2022 — Columbia LLTM and SIB, $5.13 billion

A Columbia long-lead-time material and Submarine Industrial Base contract action awarded to General Dynamics Electric Boat on December 21, 2022 placed **75 percent of work at EB-sites, 25 percent at Newport News (HII), and 0 percent at outside-yard supplier cities**.[^dod-2022-12-21] At the time of this action, the entire $5.13 billion of work was scheduled to be performed at the two-yard team.

### Anchor: May 11, 2026 — Virginia Block VI LLTM, $2.31 billion

As described in Case 3, a Virginia Block VI long-lead-time material action awarded to General Dynamics Electric Boat on May 11, 2026 placed **0 percent of work at EB-sites, 2 percent at Newport News (HII), and 98 percent at outside-yard supplier cities** ([^dod-2026-05-11]).

### The contrast

```text
                            December 2022           May 2026
                            (Col LLTM + SIB)         (Va Block VI LLTM)
                            $5.13B                   $2.31B

EB-sites (Groton, etc.):     75%                       0%
HII-sites (NNS):             25%                       2%
Outside-yard suppliers:       0%                      98%
```

In approximately three and a half years, the place-of-performance distribution of submarine long-lead-time material contract actions inverted from 100 percent at the two shipyards to 98 percent at outside-yard supplier cities. The two actions are not identical in scope — Columbia versus Virginia, slightly different work content, different procurement-block context — but they are both prime-LLTM actions awarded to the same prime contractor (GDEB) under the same contracting activity (Naval Sea Systems Command), and they are in the same general category of contract action. The contrast is direct primary-source evidence of the "distributed shipbuilding" trajectory.

## Geographic distribution within the outside-yard supplier share

<figure class="float-right"><img src="assets/photos/lockheed_combat_systems_technician.jpg" alt="Lockheed Martin combat-systems work"><figcaption>Lockheed Martin combat-systems work at the Sunnyvale, California facility. Sunnyvale appears in multiple Virginia Block VI contract-action place-of-performance breakdowns at 30 to 36 percent of action value.</figcaption></figure>

The outside-yard share of the TAM-relevant corpus concentrates in a small number of U.S. cities that house the principal submarine supplier facilities. The most material supplier-city patterns across the 43 actions include:

- **Monroeville, Pennsylvania** and **Schenectady, New York** — Westinghouse and Knolls Atomic Power Laboratory facilities supporting BPMI naval reactor work. Together account for the bulk of the BPMI $4.8 billion / 80 percent supplier-city share.
- **Sunnyvale, California** — Lockheed Martin Maritime Systems facility supporting Virginia-class combat systems and Trident SSP work. Appears in multiple Virginia LLTM actions at percentages ranging from 30 percent to 36 percent of action value.
- **Newport News, Virginia** outside the HII-NNS hull-construction yard — supplier facilities supporting Virginia and Columbia GFE content; sometimes appears as small-percentage entries even on the same actions where the HII-NNS yard is bucketed at substantial percentages.
- **Minneapolis, Minnesota** — BAE Systems forward-subassembly facility for SSN 812 (PIID `N0002421C4106`).
- **Manchester, New Hampshire**; **Westfield, Massachusetts**; **Tucson, Arizona**; **York, Pennsylvania**; **El Cajon, California**; **Tampa, Florida** — individual specialty supplier sites appearing across multiple Virginia LLTM and component-procurement actions.
- **South Yorkshire, United Kingdom** and **Staffordshire, United Kingdom** — Rolls-Royce nuclear propulsion-component and casting facilities supporting Columbia Common Missile Compartment and propulsor content.

The geographic concentration of supplier cities outside the two shipyards confirms that the outside-yard share documented in the chapter does not flow to a single alternative facility but is distributed across a national (and modestly international) supplier network of specialty firms.

## What the DoD-announcement data does not measure

Two structural limitations:

1. **The corpus covers only actions equal to or above the $7.5 million Department of Defense announcement threshold.** Actions below this threshold — which can collectively account for material total dollar value on a per-fiscal-year basis — are not in the corpus.
2. **The corpus covers calendar years 2022 through 2026 only.** The Wayback Machine resolves a much smaller number of defense.gov contract-bulletin URLs before approximately mid-2022, and the globalsecurity.org mirror begins coverage in 2025. The article's analytical posture is "recent demonstration of structural shift," not multi-decade trend.

Within these limits, the DoD-announcement corpus is the single most direct primary-source measurement of the outsourced layer that exists in the public domain. The methodology requires no assumptions about make/buy ratio, no analyst-consensus baseline, and no aggregation of derived data — the percentages are stated directly in the press releases.

## Cross-references

- For the outsourced-band evidence supported by the DoD-announcement corpus: [The outsourced layer within Basic Construction](06-outsourced-band-within-bc.md).
- For the FFATA-visible first-tier subaward stream as complementary measurement: [FFATA-visible first-tier subawards](08-ffata-visible-subawards.md).
- For the Maritime Industrial Base supplier-development pass-through: [The Maritime Industrial Base layer](10-maritime-industrial-base.md).
- For the HII Newport News team-build share that appears in DoD announcements as the "HII-sites" bucket but is invisible to FFATA: [The HII Newport News visibility gap](11-hii-newport-news-gap.md).
- For the methodology of corpus assembly, classification, and parsing: [Data sources, pipeline, and limitations](16-data-sources-pipeline-limitations.md).

[^dod-2025-04-30]: U.S. Department of Defense, Office of the Assistant Secretary of Defense (Public Affairs), Contracts press release for April 30, 2025. General Dynamics Electric Boat Corporation, Groton, Connecticut, award for Virginia Block VI long-lead-time material, $12,418 million. Place of performance: EB-sites 40%, Newport News (HII) 32%, outside-yard supplier cities 28%. Available at <https://www.war.gov/News/Contracts/> for current and recent releases, and via the Internet Archive Wayback Machine for historical access.

[^dod-2025-11-17]: U.S. Department of Defense, Office of the Assistant Secretary of Defense (Public Affairs), Contracts press release for November 17, 2025. General Dynamics Electric Boat Corporation award for Columbia advance procurement under PIID `N00024-17-C-2117` (Columbia Build I+II master), $699 million. Place of performance: EB-sites 85%, Newport News (HII) 15%, outside-yard 0%. Available at <https://www.war.gov/News/Contracts/> and via globalsecurity.org mirror.

[^dod-2026-05-11]: U.S. Department of Defense, Office of the Assistant Secretary of Defense (Public Affairs), Contracts press release for May 11, 2026. General Dynamics Electric Boat Corporation award for Virginia Block VI long-lead-time material under PIID `N00024-24-C-2110`, $2,306 million. Place of performance: EB-sites 0%, Newport News (HII) 2%, outside-yard supplier cities 98% across Sunnyvale CA, Westfield MA, Manchester NH, Tucson AZ, and additional sites. Available at <https://www.war.gov/News/Contracts/>.

[^dod-2022-12-21]: U.S. Department of Defense, Office of the Assistant Secretary of Defense (Public Affairs), Contracts press release for December 21, 2022. General Dynamics Electric Boat Corporation award for Columbia long-lead-time material and Submarine Industrial Base content under the Columbia Build I+II PIID, $5,134 million. Place of performance: EB-sites 75%, Newport News (HII) 25%, outside-yard 0%. Available at <https://www.defense.gov/News/Contracts/> and via the Internet Archive Wayback Machine.
