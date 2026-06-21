---
title: Limitations and blind spots
---

# Limitations and blind spots

The publicly visible outsourced flow on U.S. nuclear submarine construction differs materially from the true outsourced flow. Three structural exclusions, two data-quality issues, and several pull-design constraints together mean that the headline numbers in [Annual outsourced flow estimate](08-annual-outsourced-flow.md) are best read as a **publicly visible flow estimate with asymmetric coverage gaps** rather than as a strict mathematical floor: most exclusions push the true total upward, while the absence of v3 subaward dedup on the largest recipients can push specific lines downward. This chapter consolidates the limitations identified across the article set into a single inventory, with cross-references to where each limitation is discussed in detail.

## Structural exclusions

These three categories are excluded from the visible outsourced flow by design, not by data limitations. Including them would require sources beyond the federal procurement data.

### Federal naval shipyard depot work is invisible in FPDS by design

The four U.S. public naval shipyards — Norfolk Naval Shipyard (Virginia), Portsmouth Naval Shipyard (Maine), Pearl Harbor Naval Shipyard & Intermediate Maintenance Facility (Hawaii), and Puget Sound Naval Shipyard & IMF (Washington) — perform depot maintenance, engineered overhauls, and refueling work on U.S. Navy submarines. Combined, these yards employ approximately 36,000 federal workers and consume the bulk of the $6 billion-plus annual Operations and Maintenance, Navy (OMN) submarine sustainment budget. Federal-shipyard work is federal payroll and federal materiel procurement (which appears in FPDS but under generic Defense Logistics Agency descriptions); the labor and overhead component is invisible.[^repo-lessons-v1]

This is excluded from the "outsourced" definition by construction — federal-employee work is not outsourcing — but it is a major component of the total Navy submarine spend and is structurally invisible. When SCN P-5c shows a Plan Costs line at $200M per Virginia boat and the federal-shipyard chart-of-accounts shows $5 billion per year for SSN depot maintenance, the two are not double-counted in this article because they fund different work; but a reader asking "where does the Navy's submarine money go?" should be aware that depot maintenance is the largest single use category and is invisible here. See [GFE and the team-build pattern](05-gfe-and-team-build.md#other-invisible-work-in-the-procurement-data).

### HII-NNS team-build share is largely invisible in federal procurement data

Per the team-build agreement, HII Newport News Shipbuilding performs approximately **50 percent of Virginia construction** and approximately **22 percent of Columbia construction**, with GDEB as the lead yard. The vast majority of this HII-NNS workload share does not appear as HII-NNS-vendor-of-record prime records in FPDS — the prime of record on every Virginia and Columbia construction master contract is GDEB. HII-NNS work flows *through* the GDEB prime via the team agreement.[^repo-readme][^repo-lessons-v1]

Two narrow visibility channels do exist:

- The visible HII-NNS subaward of GDEB across the FY16–FY25 window is approximately **$98 million** (recipient `HUNTINGTON INGALLS INC`), vastly less than the workload share would imply.[^repo-subaward-top]
- Public NAVSEA contract announcements have at times described specific Virginia and Columbia contract modifications as awarded to **both** GDEB and HII-NNS — for example, the April 2025 announcement of modifications for FY24 Virginia construction publicly named HII-NNS at approximately $1.3 billion. These press-release figures are not picked up by the article's FPDS pull as HII-NNS-vendor-of-record records, because FPDS records the same actions on the GDEB master vehicle with vendor-of-record `ELECTRIC BOAT CORPORATION`. The NAVSEA announcement stream is a useful third channel that future analyses should track in parallel to FPDS.

Some additional HII-NNS work may also be routed through Northrop Grumman as a flow-through (NG appears as a $2.21 billion combined Virginia+Columbia subaward of GDEB, and the data do not allow NG-direct sonar work to be separated from NG-as-router of HII-NNS work). The remainder is not reconstructible from federal procurement data; the only reliable source is HII corporate financial disclosures (10-K segment revenue × analyst estimate of submarine share).[^repo-subaward-top][^repo-lessons-v1]

The article does not attempt a quantitative estimate of the HII-NNS team-build share. Including it would substantially raise the headline annual outsourced flow. See [GFE and the team-build pattern](05-gfe-and-team-build.md#the-hii-newport-news-team-build-pattern).

### Classified payload modules are invisible in FPDS by design

Intelligence-community submarine modules — historically including the SSGN special-operations payload extensions and various classified surveillance equipment — are procured outside the public SCN appropriation through classified contracting channels. None of this activity appears in FPDS by design. The total dollar magnitude is not public.[^repo-readme]

This is a structural exclusion of public procurement data, not a measurement gap. No methodology change would bring classified payload work into the visible flow.

## Data-quality issues

### The aggregator does not apply v3 subaward dedup

The companion v2 lessons-learned material documents that USAspending's `/api/v2/subawards/` endpoint exhibits a **cumulative-snapshot duplication** pattern in which the same `subaward_number` appears at multiple `action_date` values, each at a cumulative-style amount. Naive summation of the returned `amount` values can inflate true subaward delivery by a factor of approximately **5× to 50×** for subs with this pattern.[^repo-lessons-v2]

The corrective methodology is a three-stage v3 dedup: (Stage 1) for each `sub_id`, keep the record with the maximum amount; (Stage 2) collapse identical (recipient, amount) duplicates across different sub_ids; (Stage 3) cap any single (recipient, prime) pair at 1.0× the prime contract's total obligation and exclude any pair exceeding 2× prime. Applied to a prior 170-PIID dataset in companion analysis, v3 dedup reduced an implied total of approximately $80+ billion in-window subawards to a corrected approximately $10.35 billion — an 8× correction across the full dataset.[^repo-lessons-v2]

**The aggregator in this repository (`scripts/aggregate_annual_outsourcing.py`) does not implement v3 dedup.** It performs naive sums of the USAspending `amount` field, grouped by `action_date` fiscal year and by recipient. This is acknowledged explicitly in the aggregator's own citation footnote in `INDEX.md` and in [Data sources and methodology](09-data-sources-and-methodology.md#known-aggregator-limitation-no-v3-dedup).[^repo-aggregate-script]

The implication is that **the reported subaward column in `extracted/subaward_annual_by_prime.csv` and the cumulative subaward totals in `extracted/subaward_top_recipients.csv` may be overstated** — by an unknown but potentially material factor — for recipients with multiple cumulative-snapshot records under a single `sub_id`. The most likely candidates for inflation are the largest, longest-running subs:

- **BlueForge Alliance** ($4.21B / 7 actions) — the small action count makes large per-`sub_id` snapshot inflation structurally unlikely; the figure is probably approximately correct.
- **Northrop Grumman Systems** ($2.21B / many actions on long-running primes) — could be materially overstated by v3 dedup; would need to be re-tested.
- **BAE Systems Land & Armaments** ($355M / 18 actions on Virginia Block V/VI master) — could be moderately overstated.
- **Curtiss-Wright Electro-Mechanical** ($515M combined across CW entities, ~150 actions across multiple PIIDs) — could be materially overstated.

A future revision applying v3 dedup would tighten the headline subaward totals downward. The Bechtel Plant Machinery GFE column in `extracted/fpds_annual_by_prime.csv` is **not** affected by the v3 dedup issue, because it uses FPDS per-modification `obligatedAmount` data (this-action only), which does not exhibit cumulative-snapshot duplication.

### Vendor-name normalization is not applied

The aggregator's vendor-group regex matches against raw `vendor_name` strings and does not apply parent-company normalization. General Dynamics Mission Systems, GD Information Technology, NASSCO, Bath Iron Works, and other GD entities appear as separate vendors; Aerojet Rocketdyne (acquired by L3Harris in 2023) is not rolled into L3Harris; Marinette Marine (owned by Fincantieri) is not rolled into its parent. Companion v2 material describes a hand-curated parent-company mapping table approach for cross-program rollups.[^repo-lessons-v2]

For the submarine article, this is a minor issue because the dominant primes appear under their dominant submarine-related legal entity names (`ELECTRIC BOAT CORPORATION`, `BECHTEL PLANT MACHINERY, INC.`, `LOCKHEED MARTIN CORPORATION`, `NORTHROP GRUMMAN SYSTEMS CORPORATION`, `BAE SYSTEMS LAND & ARMAMENTS L.P.`). A reader doing parent-company rollup for cross-program purposes should consult v2 of the lessons-learned material for the mapping table approach.

## Pull-design constraints

### USAspending ~2,500-record retrieval cap on the two big GDEB master vehicles

The pull script paginates USAspending's `/api/v2/subawards/` endpoint at 100 records per page with a maximum of 25 pages, producing a practical ceiling of approximately 2,500 records per prime. Two of the in-scope GDEB master vehicles hit this retrieval cap:[^repo-usaspending-summary][^repo-lessons-v1]

- **`N0002417C2100`** (Virginia Block V/VI master): 2,500 returned subaward records, $4.19 billion total visible subaward value.
- **`N0002417C2117`** (Columbia Build I+II): 2,500 returned subaward records, $8.17 billion total visible subaward value.

For these two PIIDs, the long tail of small subs (typically below approximately $100,000 per subaward action) is missing. The pull sorts by amount descending, so the top spend is captured. The visible totals are floor values: the true subaward sums on these two vehicles are larger than reported by an unknown amount in the long tail.

This understatement runs in the opposite direction from the v3-dedup overstatement noted above. The two effects do not cancel cleanly and would need to be quantified separately by re-running the pull with v3 dedup applied.

### FFATA reporting lag affects FY2025

USAspending subaward reporting lags prime obligation by approximately 6–18 months. The FY2025 subaward action-date column in `extracted/subaward_annual_by_prime.csv` shows $766 million across the 12 in-scope PIIDs, against an FY2024 figure of $4,162 million — a step-down of roughly 5× that is inconsistent with the underlying FPDS prime activity in FY2025, which shows comparable obligations to FY2024.[^repo-subaward-annual][^repo-fpds-annual] The companion v1 lessons-learned material flags this as a typical reporting lag pattern and recommends treating fresh-year subaward totals as substantially understated until 12–18 months have elapsed.[^repo-lessons-v1]

The FY2025 figure in the headline is therefore artificially low. The true FY2025 visible outsourced flow will be revised upward in any future re-pull conducted in 2027 or later; the magnitude of the revision depends on which prime PIIDs file late and how heavily, and is not formally modeled in this pass. The trend direction (sharp FY2023–FY2024 ramp) and the FY2024 peak are not affected by this lag.

### Five PIIDs report zero subawards

Of the 17 in-scope seed PIIDs, five returned zero subaward records:[^repo-usaspending-summary]

- **`N0002409C2104`** (Virginia Block II residual, $16.24B prime): mostly closed out; little remaining first-tier activity expected.
- **`N0002410C2118`** (VPM Tube Fabrication, $1.42B prime): the prime is large and ongoing; the lack of subaward records is consistent with a non-reporting pattern rather than absence of subcontracting activity.
- **`N0002411C2109`** (SSBN-R concept formulation, $480M prime): concept-stage R&D; few first-tier subs expected.
- **`N0002424C2114`** (BPMI FY26 Virginia Component Funding, $2.54B prime): too new for subaward reporting to flow yet.
- **`N0002410C6266`** (LM Virginia Combat Systems, $899M prime): the prime is large and ongoing; the lack of subaward records is consistent with a non-reporting pattern rather than absence of subcontracting activity.

Two of these (VPM Tube Fabrication and LM Virginia Combat Systems) represent multi-hundred-million-dollar primes whose first-tier supplier bases are invisible in the data. Companion v1 lessons-learned material documents this as a general FFATA compliance gap: some primes report subawards on some PIIDs and not on others; foreign-owned primes typically do not report; new contracts often do not have sub records for 12–24 months after award.[^repo-lessons-v1]

The visible outsourced flow on these five primes is **structurally zero in USAspending**, but the true outsourced flow is positive (probably substantial for VPM Tube Fabrication and LM Virginia Combat Systems). This means the headline subaward column is **understated** with respect to these primes.

### FPDS pagination caps the GDEB query at 300 pages

The repository's FPDS pull script caps each query at 300 pages (3,000 records). The GDEB vendor sweep `gdeb_navy` hits this cap, against an estimated true count of approximately 7,520 records.[^repo-fpds-summary][^repo-fpds-script]

The cap affects the latest-mod cumulative aggregate displayed in the pull log (which understates the true GDEB cumulative obligation across all 166+ in-scope PIIDs) but does **not** affect the per-modification annual aggregation in `extracted/fpds_annual_by_prime.csv`, because the latter aggregates at the modification level: a missing modification in the cap-truncated tail of the GDEB query would be missed regardless, but the structure of the per-FY aggregation does not amplify this miss.

Raising the cap to 1,000 pages would address this fully. The current pull was performed with a 300-page cap as a politeness measure given the FPDS Atom Feed's response-time characteristics.

### Three vendor sweeps lack description filters

Three of the 13 FPDS vendor sweeps lack description-keyword filtering and over-collect non-submarine activity:[^repo-fpds-summary][^repo-fpds-script]

- **Curtiss-Wright** (`curtiss_wright_navy`): 2,490 records / 991 unique PIIDs. Includes all Curtiss-Wright Navy nuclear work, not just submarine work.
- **Rolls-Royce** (`rolls_royce_navy_sub`): 2,980 records / 1,391 PIIDs. Includes the firm's much larger Navy aircraft-engine business.
- **BlueForge Alliance** (`blueforge_navy`): 3,901 records / 1,972 PIIDs. The `"BLUE FORGE"` substring matches many unrelated "Blue *" vendors (Blue Tech, Blue Rock, etc.).

The annual obligation columns for these three vendor groups in `extracted/fpds_annual_by_prime.csv` should be treated as **upper bounds** on submarine-relevant activity, not as net submarine exposure. The genuine BlueForge Alliance prime activity is much smaller than the 3,901 records suggest — approximately $923 million cumulative on one PIID, with per-modification new-money obligation of $538M (FY24) + $366M (FY25) + $19M (FY26 to date).[^repo-fpds-annual][^repo-summary-findings]

A future re-pull adding `DESCRIPTION_OF_REQUIREMENT` filters to the Curtiss-Wright and Rolls-Royce queries, and tightening the BlueForge query to `VENDOR_NAME:"BLUEFORGE ALLIANCE"` only, would substantially clean these three vendor-group columns.

## Outsourced work is not just a dollar-flow issue — it is also a SUPSHIP oversight and quality-assurance issue

A consideration that does not change the headline number but materially shapes the policy reading is the **quality-assurance oversight posture** of the Navy's on-site supervisor-of-shipbuilding organizations. The U.S. Government Accountability Office reported in 2024 that the **Supervisor of Shipbuilding (SUPSHIP) Groton** and **Supervisor of Shipbuilding (SUPSHIP) Newport News** organizations — the Navy's principal in-yard oversight bodies at the two team-build shipyards — were not well positioned to conduct quality-assurance oversight for the significant amount of Columbia work being outsourced. GAO recommended that the Navy update its oversight planning for the expected hours and locations of outsourced Columbia work, and observed that the Navy and the shipbuilders had not consistently defined the information needed to determine whether the multi-billion-dollar Submarine Industrial Base supplier-development investments are producing the intended production improvements.[^gao-24-107732]

This dimension of "outsourced work" — the oversight and risk-management posture, not the dollar size — is treated only briefly in this article but is a central consideration in the industrial-base policy literature. The MIB ramp described in [Maritime Industrial Base and BlueForge Alliance](07-maritime-industrial-base.md) is partly a response to a binding production-rate constraint (Columbia plus Virginia ramps against a smaller-than-needed supplier base), and the GAO findings indicate that the supplier-investment leg of the response is, as of 2024, not yet well-instrumented for measurement of its production-improvement payoff. Future analyses that combine the dollar-flow view in this article with the GAO oversight findings will produce a more complete picture of the industrial-base policy response.

## Other limitations worth noting

### Date window choice

The FPDS pull uses `SIGNED_DATE:[2018/01/01,2026/12/31]`. Pre-FY2018 modifications on contracts that pre-date the window — most notably Virginia Block IV `N0002412C2115` (FY14 award), Block II `N0002409C2104` (FY09 award), and various Bechtel PIIDs — are not in the pull. This means the **window-period delta** for older contracts is computed from incomplete data: the per-modification annual aggregation correctly buckets only the FY18+ mods, but the baseline against which to compute true window delta (the cumulative `totalObligatedAmount` at the latest pre-FY18 modification) is not available because the script did not pull pre-FY18 records.[^repo-lessons-v1]

The companion v1 lessons-learned material recommends pulling 2–3 years of pre-window modifications to enable proper window-delta computation. The submarine pull does not do this. For the major contracts whose cumulative values are reported in [Procurement and prime contracts](03-procurement-and-contracts.md), the cumulative figures cited (Block IV $19.90B, Block V/VI $34.94B, Columbia Build I+II $24–30B) are sourced from companion prior analysis (`SAM_Submarine_Cutter_Contract_Awards.md`) rather than from the current pull.[^repo-sam-prior]

### Scope: Virginia and Columbia only

This article covers Virginia-class and Columbia-class new construction only. Other submarine programs — Ohio-class refueling/conversion, Los Angeles-class sustainment, future SSN(X), and the historical Seawolf class — are not in scope. SSBN(R) concept formulation work appears in the data via `N0002411C2109` ($480M cumulative, no subawards reported) but is not analyzed.

### Per-ship attribution is not produced

The subaward data is per-PIID. Many PIIDs cover multiple ships in a block or build (Block IV `N0002412C2115` covers 10 boats; Block V/VI `N0002417C2100` covers Block V and now extends into Block VI). Mapping the per-FY subaward dollars back to specific hulls would require parsing modification descriptions for hull references (for example, identifying which modifications fund SSN 812 versus SSN 814). This article does not produce per-hull subaward attribution.[^repo-lessons-v1]

### Quantitative HII-NNS share estimate not produced

As noted under "Structural exclusions" above, this article does not estimate the HII-NNS team-build share. Producing such an estimate would require HII Form 10-K segment revenue data, analyst estimates of submarine share within the Newport News Shipbuilding segment, and assumptions about cost allocation across the team-build agreement. This is in scope for a future analysis pass but not for the initial gathering described here.[^repo-readme]

## Summary — how to read the headline

The published headline of **approximately $1.4 billion (FY18) → $6.3 billion (FY24) of visible annual outsourced flow** should be read with the following modifiers:

- It is a **publicly visible flow estimate with asymmetric coverage gaps**, not a comprehensive measurement and not a strict mathematical floor.
- It **excludes** federal naval shipyard depot work, HII-NNS team-build share, and classified payload work — all of which are large and push the true total upward.
- It **does not include** the LM Virginia combat-system, LM SSBN material, and LM Trident GFE prime flows (excluded to avoid double-counting against SCN line items where overlap is possible; including them with overlap-checking would push the true total upward).
- The first-tier subaward column may be **overstated** for the largest long-running subs due to the absence of v3 dedup (Northrop Grumman, BAE, and Curtiss-Wright are the most likely candidates for downward correction; BlueForge at 7 actions is structurally less exposed).
- The first-tier subaward column is also **understated** by the ~2,500-record retrieval cap on the two big GDEB master vehicles and by the five zero-subaward primes.
- The FY2025 row is **artificially low** due to FFATA reporting lag.
- The trend direction (sharp FY23–FY24 ramp on Maritime Industrial Base / BlueForge Alliance flow) is robust to all of the above modifiers.

A reader who needs a single-sentence summary should say: **"Publicly visible outsourced flow on U.S. nuclear submarine construction grew from roughly $1.4 billion per year in FY2018 to roughly $6 billion per year in FY2024, driven mostly by the new Maritime Industrial Base supplier-development line on Columbia (BlueForge Alliance) and steady growth in Bechtel Plant Machinery naval-reactor procurement; the true outsourced flow is probably materially larger because the HII-NNS team-build share, the Lockheed Martin combat-system and Trident GFE primes, the long tail of small subs on the two big GDEB master vehicles, and the FY2025 reporting lag are all under-reported in the visible number, though specific subaward lines for the largest long-running recipients may also be modestly overstated until v3 dedup is applied."**

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^repo-subaward-top]: submarine_outsourced_work, "extracted/subaward_top_recipients.csv." See full citation under [References](INDEX.md#references).

[^repo-lessons-v2]: Subaward Pull Lessons Learned (v2). See full citation under [References](INDEX.md#references).

[^repo-aggregate-script]: submarine_outsourced_work, `scripts/aggregate_annual_outsourcing.py`. See full citation under [References](INDEX.md#references).

[^repo-usaspending-summary]: submarine_outsourced_work, "usaspending_subawards/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-subaward-annual]: submarine_outsourced_work, "extracted/subaward_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-fpds-annual]: submarine_outsourced_work, "extracted/fpds_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-fpds-summary]: submarine_outsourced_work, "fpds_raw/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-fpds-script]: submarine_outsourced_work, `scripts/pull_fpds_sub_primes.py`. See full citation under [References](INDEX.md#references).

[^repo-summary-findings]: submarine_outsourced_work, "SUMMARY_INITIAL_FINDINGS.md." See full citation under [References](INDEX.md#references).

[^repo-sam-prior]: SAM Submarine & Cutter Contract Awards (April 2026). See full citation under [References](INDEX.md#references).

[^gao-24-107732]: U.S. Government Accountability Office, *Columbia Class Submarine: Overcoming Persistent Challenges Requires Yet Undemonstrated Performance and Better-Informed Supplier Investments*, GAO-24-107732 (2024). See full citation under [References](INDEX.md#references).
