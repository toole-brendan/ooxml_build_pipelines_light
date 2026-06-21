---
title: Maritime Industrial Base and BlueForge Alliance
---

# Maritime Industrial Base and BlueForge Alliance

A new line of submarine-related outsourced flow appeared in the public procurement data beginning in approximately fiscal year 2023: a multi-billion-dollar **Maritime Industrial Base (MIB)** supplier-development and workforce-expansion flow, contractually routed through the General Dynamics Electric Boat Columbia Build I+II prime contract and distributed almost entirely outside the prime shipyard. The dominant single recipient is **BlueForge Alliance**, a non-profit consortium based in College Station, Texas. This chapter describes the MIB flow as a distinct category of submarine outsourcing — separate from conventional first-tier subaward subcontracting and from government-furnished equipment — and documents what the data show.

## Why MIB exists

Beginning in fiscal year 2022, the U.S. Navy began directing significantly more SCN appropriation dollars to supplier-base capacity expansion, workforce training, and small and mid-tier supplier development in the submarine industrial base. The 30-Year Shipbuilding Plan accompanying the FY2027 President's Budget describes the MIB flow under the framing of "outsourcing partners," and the FY2027 SCN justification book Columbia line item P-5c exhibit places the MIB pass-through inside the **Plan Costs** cost category for SSBN 826 (the Columbia lead boat).[^scn-30yr-pb27][^scn-fy27pb]

The driver is the **rate gap** between Columbia and Virginia ramps and the supplier base's existing capacity. Columbia Build I and Build II are under construction simultaneously with Virginia Block V (nine boats, five with VPM) and Block VI (nine boats planned), against a supplier base — castings, forgings, machined parts, valves, electrical equipment, welders, machinists — that was sized for a smaller production rate. The MIB investments are intended to close that gap by funding new equipment installations, new facility construction, workforce training programs, and small/mid-tier supplier subsidies across multiple states.

### Production-rate and policy context

The MIB ramp is a deliberate Navy policy response to several converging pressures:[^navy-fy27-press][^gao-24-107732]

- **Columbia serial production with no slack.** The Navy plan calls for procurement of approximately one Columbia hull per year through the Build-XII boat in the early 2030s. There is no second Columbia yard; both yards (GDEB and HII-NNS as team partner) are simultaneously on Virginia Block V, Block VI, and Columbia.
- **Virginia stretch goal of two boats per year.** Public Navy commentary across multiple budget cycles has described the Virginia program target as **two boats per year**, sustained, with one Columbia overlaid. The combined demand (one Columbia + two Virginia per year, plus modules for the AUKUS partnership) is a rate not seen in the U.S. submarine industrial base since the late Cold War, with a different (smaller, more specialized) supplier base than then.
- **Skilled-trades labor shortage as a binding constraint.** Welders, pipefitters, electricians, and other shipyard trades are in short supply. Workforce-training and apprenticeship subsidies are a major use of BlueForge consortium funds. The shortage is structural, not cyclical, and is one reason the MIB investments include education and recruitment programs alongside facility build-out.
- **Supplier-base concentration on aging firms.** Some single-source or limited-source suppliers in castings, large forgings, valves, and electrical equipment have aging capital stock and uncertain capacity to absorb the rate increase. MIB funds underwrite equipment replacements and facility expansions targeted at these chokepoints.
- **An approximately $65.8 billion FY2027 Navy shipbuilding request** accompanies the FY2027 30-Year Shipbuilding Plan, with the Navy's public framing emphasizing industrial-base revitalization, workforce and shipyard capacity, and production-rate goals as a coherent package.

The Government Accountability Office has separately reported that, as of 2024, the Navy and the shipbuilders had not consistently defined the information needed to determine whether the multi-billion-dollar supplier-development investments are producing the intended production improvements, and that the SUPSHIP Groton and SUPSHIP Newport News organizations were not well positioned to conduct quality-assurance oversight for the significant amount of Columbia work being outsourced. The MIB ramp described above is therefore a policy response to a binding production-rate constraint, but its production-improvement payoff is not yet well-instrumented for measurement — a consideration that bears on how the dollar-flow numbers in this article should be interpreted as a leading or lagging indicator of capacity. (See [Limitations and blind spots](10-limitations-and-blind-spots.md#outsourced-work-is-not-just-a-dollar-flow-issue-it-is-also-a-supship-oversight-and-quality-assurance-issue).)

## How MIB flow appears in the data

In FPDS, MIB flow is captured under the GDEB Columbia prime PIID `N0002417C2117` (Columbia Build I + Build II). The contract description on later modifications references "ADDITIONAL SUPPLIER DEVELOPMENT AND CLASS LEAD YARD SUPPORT" as a frequent scope element.[^repo-sam-prior] In USAspending, MIB flow appears as a small number of large first-tier subaward records under `N0002417C2117` to a single recipient: **BlueForge Alliance**.

In SCN budget terms, MIB lives inside the Columbia **Plan Costs** line. The FY27 PB SCN P-5c exhibit shows SSBN 826 Plan Costs at $6,946.3 million — approximately **5–8 times higher** than the comparable line on later Columbia boats (SSBN 827 at $1,443.3M, SSBN 828 at $1,095.8M, SSBN 829 at $861.5M). The bulk of the SSBN 826 lead-ship Plan Costs is the MIB and supplier-development load.[^repo-scn-extract]

## BlueForge Alliance — the consortium pass-through

**BlueForge Alliance** is a non-profit consortium based in College Station, Texas, established to operate as the **Submarine Industrial Base (SIB)** workforce, supplier-development, and capacity-expansion pass-through. It channels SIB funds from the Columbia prime contract to small and mid-tier suppliers, training programs, welding workforce-development organizations, and capacity-build projects across the United States. Companion analysis describes BlueForge as "effectively a pass-through for SIB grants and the dominant 'vendor' on the Columbia subaward tree."[^repo-sam-prior]

In the FY16–FY25 first-tier subaward data across all 17 in-scope submarine prime PIIDs, **BlueForge Alliance is the single largest recipient at $4,213.96 million cumulative**, concentrated entirely on `N0002417C2117` (Columbia Build I+II).[^repo-subaward-top]

The $4.21 billion is reported across just **7 subaward action records** — meaning the consortium is receiving very large lump-sum subaward actions rather than many small task orders. This is consistent with the consortium pass-through model: BlueForge receives a small number of large subaward "tranches" from the Columbia prime, then disburses to its own roster of approximately 10,000-plus supplier and training partners through mechanisms (DPA Title III awards, training-program grants, equipment-installation contracts) that are not themselves reported in the USAspending first-tier subaward stream because BlueForge's onward distributions are second-tier subcontracts.[^repo-sam-prior]

### Columbia Build I+II subaward flow by fiscal year

The action-date breakdown of the per-FY per-PIID column for `N0002417C2117` in `subaward_annual_by_prime.csv` shows:[^repo-subaward-annual][^repo-summary-findings]

| FY | `N0002417C2117` subaward $ ($M) | Notes |
|---|---:|---|
| FY2023 | ~2,755 | Initial Maritime Industrial Base ramp |
| FY2024 | ~3,650 | Peak so far |
| FY2025 | ~488 | Reporting lag |

These figures are **total subaward dollars across all recipients on `N0002417C2117`**, not BlueForge-only. BlueForge Alliance is the dominant recipient inside this PIID at $4,213.96 million across 7 reported action records (per the cumulative top-200 list), but the remaining ~$2.7 billion of the Build I+II PIID subaward flow goes to Northrop Grumman Systems (~$669M cumulative), DRS Naval Power Systems (~$403M), Curtiss-Wright Electro-Mechanical (~$176M), Babcock Marine Rosyth (~$172M), Scot Forge (~$171M), APCO Technologies SA (~$131M), Rhoads Metal Fabrications (~$124M), and a wider tail of suppliers. The per-FY breakdown of BlueForge alone is not separated out of the per-PIID column in the aggregator; a future revision could compute it by reading BlueForge action records directly from the raw subaward JSON.[^repo-subaward-top][^repo-sam-prior]

The total across the visible window is approximately $6.9 billion of total Build I+II subaward flow, of which approximately $4.2 billion is attributable to BlueForge Alliance and approximately $2.7 billion to the rest of the supplier base on this PIID.

### BlueForge in the FPDS prime data

`VENDOR_NAME:"BLUEFORGE ALLIANCE"` and `VENDOR_NAME:"BLUE FORGE"` against the Navy contracting-agency filter return approximately 3,901 records / 1,972 unique PIIDs in the pull — but the substring "BLUE FORGE" matches a wide range of unrelated "Blue *" vendors (Blue Tech, Blue Rock, etc.), so most of those records are spurious matches.[^repo-fpds-summary] The genuine BlueForge Alliance prime activity is much smaller: companion analysis identifies approximately $923 million cumulative obligation on a single BlueForge prime PIID, with per-modification new-money obligation of approximately $538 million in FY2024, $366 million in FY2025, and $19 million in FY2026 to date. Public reporting also identifies a separate September 2024 direct NAVSEA prime contract to BlueForge Alliance worth approximately $950.7 million (with options up to approximately $980.7 million; $503.1 million obligated at award) for Submarine Industrial Base and Foreign Military Sales support.[^repo-fpds-annual][^repo-summary-findings]

BlueForge therefore appears in **at least two distinct public channels**: as a large first-tier subaward recipient under the GDEB Columbia prime `N0002417C2117` ($4.21 billion cumulative across the FY16–FY25 window) and as a direct NAVSEA prime contractor for SIB and FMS support (sub-$1 billion cumulative across the same window, on the order of ~$923 million per FPDS). These channels are closely related in purpose — both fund the same Submarine Industrial Base supplier-development ecosystem — and they may overlap in specific line items, but the public data do **not** demonstrate that they are the same dollars seen twice. The annual outsourced-flow headline in [chapter 8](08-annual-outsourced-flow.md) counts only the GDEB-Columbia-subaward channel and excludes the direct BlueForge NAVSEA prime to avoid the risk of double-counting; a more complete view would either reconcile the two channels at the contract-line level or report them separately with explicit caveats.

## What the MIB ramp looks like in the headline data

The signature feature of the visible MIB flow is the FY2023–FY2024 step-change in the annual outsourced total visible in USAspending.[^repo-summary-findings][^repo-subaward-annual]

Annual subaward flow across all 12 PIIDs that returned non-zero subaward counts:

| FY | Total subaward $ ($M) | Driver |
|---|---:|---|
| FY2016 | 206 | Block IV ramp |
| FY2017 | 1,307 | Block V signing on `N0002417C2100` |
| FY2018 | 1,028 | Block V continuation |
| FY2019 | 1,456 | Block V + Columbia Build I awards |
| FY2020 | 353 | Trough |
| FY2021 | 826 | |
| FY2022 | 696 | |
| **FY2023** | **3,813** | **Columbia BlueForge MIB ramp begins** ($2,755M on `N0002417C2117`) |
| **FY2024** | **4,162** | **Peak so far** ($3,650M on `N0002417C2117`) |
| FY2025 | 766 | Reporting lag |

The visible direct-outsourced flow jumped from approximately $700 million in FY2022 to approximately $3.8 billion in FY2023 — a step change of approximately $3 billion that is essentially entirely attributable to the BlueForge consortium flow on the Columbia prime. FY2024 added another $349 million on top. The FY2025 trough of $766 million is expected to be revised upward as the typical 6–18 month FFATA reporting lag clears; the magnitude of the eventual revision depends on which prime PIIDs file late and is not formally modeled here.[^repo-summary-findings][^repo-lessons-v1]

## What BlueForge does with the money

The $4.21 billion does not represent BlueForge performing $4.21 billion of work. The consortium operates as a pass-through to:

1. **Small and mid-tier submarine suppliers** — castings, forgings, machined parts, valves, electrical equipment, pressure vessels. BlueForge's disbursements include facility build-outs, equipment purchases, and capacity-expansion subsidies for these firms.
2. **Workforce training and education partners** — welding training programs, machinist apprenticeships, technical college partnerships. The shortage of skilled trades labor is one of the binding constraints on submarine production rate.
3. **Industry workforce attraction programs** — public-facing recruitment, retention bonuses, and similar initiatives.

The onward distribution from BlueForge to its supplier and training partners is a second-tier subcontract relationship and does **not** appear in USAspending's first-tier `/api/v2/subawards/` data. Some portion appears in adjacent databases (DPA Title III award announcements, individual prime-contractor press releases, BlueForge's own public reporting), but no single comprehensive public dataset captures the onward distribution. For the purposes of measuring submarine outsourcing, BlueForge is the visible "end" of the flow in USAspending; what happens beyond is not captured.[^repo-readme][^repo-manifest]

## Implications for outsourcing measurement

The BlueForge / MIB flow has three measurement implications:

**1. It is genuinely outsourced from GDEB's perspective.** The $4.21 billion is paid by the GDEB prime to a non-GDEB entity (BlueForge Alliance) and does not stay at the prime shipyard. It belongs in the visible annual outsourced flow.

**2. It is concentrated.** The Columbia first-tier subaward tree is dominated by a single recipient (BlueForge at $4.21B) on a small number of action records (7), in contrast with the Virginia first-tier tree, which is distributed across a much broader supplier base (the visible top-eight Virginia Block V/VI subs add to approximately $2.36 billion across 600-plus subaward actions). MIB concentration on Columbia is a function of the consortium pass-through structure, not of the underlying supplier diversity, which is broad.

**3. It is new.** The pre-FY2022 historical visible outsourced flow on the same PIIDs was approximately $0.7–1.4 billion per year. The post-FY2022 flow is approximately $3.8–4.2 billion per year (FY2023 and FY2024). The step change is essentially entirely the MIB ramp. Any time-series of "outsourced submarine work" that does not annotate this break will misread it as organic supplier-base growth rather than a deliberate Navy industrial-base policy change.

[^scn-30yr-pb27]: U.S. Navy FY2027 PB 30-Year Shipbuilding Plan. See full citation under [References](INDEX.md#references).

[^scn-fy27pb]: U.S. Navy FY2027 PB SCN Justification Book. See full citation under [References](INDEX.md#references).

[^repo-sam-prior]: SAM Submarine & Cutter Contract Awards (April 2026). See full citation under [References](INDEX.md#references).

[^repo-scn-extract]: submarine_outsourced_work, parsed SCN extracts. See full citation under [References](INDEX.md#references).

[^repo-subaward-top]: submarine_outsourced_work, "extracted/subaward_top_recipients.csv." See full citation under [References](INDEX.md#references).

[^repo-subaward-annual]: submarine_outsourced_work, "extracted/subaward_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-summary-findings]: submarine_outsourced_work, "SUMMARY_INITIAL_FINDINGS.md." See full citation under [References](INDEX.md#references).

[^repo-fpds-summary]: submarine_outsourced_work, "fpds_raw/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-fpds-annual]: submarine_outsourced_work, "extracted/fpds_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^repo-manifest]: submarine_outsourced_work, "MANIFEST.md." See full citation under [References](INDEX.md#references).

[^navy-fy27-press]: U.S. Department of the Navy, FY2027 Shipbuilding Plan release. See full citation under [References](INDEX.md#references).

[^gao-24-107732]: GAO-24-107732, *Columbia Class Submarine: Overcoming Persistent Challenges* (2024). See full citation under [References](INDEX.md#references).
