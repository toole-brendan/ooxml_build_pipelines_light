---
title: Annual outsourced flow estimate
---

# Annual outsourced flow estimate

This chapter combines the per-fiscal-year first-tier subaward flow visible in USAspending with the per-fiscal-year Bechtel Plant Machinery naval-reactor government-furnished-equipment prime obligations visible in the Federal Procurement Data System to produce a single headline view of publicly visible annual outsourced work on U.S. nuclear submarine construction, fiscal years 2018 through 2025. The headline is best read as a **publicly visible flow estimate with asymmetric coverage gaps**, not as a strict mathematical floor: several large categories are excluded (which pushes the true total upward), while the undeduplicated USAspending subaward column may overstate some of the largest recipient totals (which can push specific lines downward). Three structural exclusions and the dedup-uncertainty issue are documented at the end of this chapter and in [Limitations and blind spots](10-limitations-and-blind-spots.md).

## Data-channel map

The conceptual model behind the headline is summarized in the following text diagram. Each arrow is a public dollar-flow channel, and the headline counts only the channels marked with **(✓ counted)**; channels marked **(× excluded)** are excluded to avoid double-counting or because they are out of scope:

```text
SCN appropriation (LI 1045 Columbia, LI 2013 Virginia)
   │
   ├──► GDEB construction prime (N0002417C2100, N0002417C2117, …)
   │       ├── GDEB in-yard labor / material / overhead       (× not outsourced)
   │       ├── HII-NNS team-build / module sections           (× invisible in FPDS;
   │       │                                                   visible only in HII
   │       │                                                   corporate disclosures
   │       │                                                   and partial NAVSEA
   │       │                                                   press releases)
   │       ├── first-tier supplier subawards in USAspending   (✓ counted — GDEB-prime)
   │       └── BlueForge / MIB consortium subaward channel    (✓ counted within
   │                                                           GDEB-prime subaward)
   │
   ├──► direct GFE/GFP primes
   │       ├── BPMI naval reactor plant                       (✓ counted — pillar 2)
   │       ├── LM Virginia combat systems                     (× excluded — overlap
   │       │                                                   risk with SCN P-5c
   │       │                                                   Electronics line)
   │       ├── LM Trident II D5 / D5LE2                       (× excluded — funded
   │       │                                                   outside SCN under SSP)
   │       └── LM SSBN Material & Kit Additions               (× excluded — overlap risk)
   │
   └──► direct industrial-base / workforce / supplier-development primes
           ├── BlueForge Alliance direct NAVSEA prime          (× excluded — overlap
           │                                                   risk with BlueForge
           │                                                   GDEB-prime subaward
           │                                                   channel above)
           └── other direct GDEB / HII workforce or
               productivity modifications                      (× partially in pillar 1
                                                                or in NAVSEA press
                                                                release stream only)
```

The headline number combines the two ✓-marked pillars. The × channels are reported separately in the relevant chapters but are not added to the headline. The wide range of × channels is the principal reason the headline should be read as a publicly visible flow estimate rather than as a comprehensive measurement.

## The two pillars

The headline number is the sum of two pillars, constructed to avoid the most obvious double-count between subaward and GFE-prime channels:

1. **Direct first-tier outsourcing by GDEB**, measured as the sum of USAspending `/api/v2/subawards/` `amount` fields by `action_date` fiscal year, aggregated across the **GDEB-prime PIIDs only** (the 8 GDEB construction-prime PIIDs with non-zero subaward records). This excludes the subaward trees of the BPMI, BAE, and Rolls-Royce GFE/component primes, which are reported separately on those primes' own subaward chapters and are downstream uses of the second pillar — not additive to it. This is the most direct measure of what GDEB pays to others on its own submarine construction prime contracts. (See [First-tier subawards and supplier visibility](06-first-tier-subawards.md).)[^repo-subaward-annual]
2. **Navy → BPMI prime $ for naval reactor components**, measured as the sum of per-modification `obligatedAmount` (this-action only, not cumulative `totalObligatedAmount`) on Bechtel Plant Machinery, Inc. submarine-relevant prime PIIDs, bucketed by signed-date fiscal year. This is the most reliable annual GFE flow in the dataset. (See [Procurement and prime contracts](03-procurement-and-contracts.md).)[^repo-fpds-annual]

Both pillars use the per-modification or action-date fiscal-year bucketing methodology described in [Terminology and scope](01-terminology-and-scope.md#cumulative-versus-window-dollars), not the latest-mod cumulative method. This is the only methodology that produces a meaningful annual number; using cumulative `totalObligatedAmount` would massively overstate the window flow by counting pre-window obligations.[^repo-lessons-v1]

The reason for the GDEB-prime-only restriction on pillar 1 is straightforward: if pillar 2 captures Navy → BPMI prime obligations of approximately $2 billion per year, and BPMI in turn pays BWXT, Curtiss-Wright, DRS Naval Power Systems, and others, then **BPMI's first-tier subaward tree is downstream of pillar 2, not additive to it**. Adding the BPMI subaward column to the GDEB subaward column and then adding the BPMI prime column on top would double-count the BPMI channel. Earlier drafts of this analysis carried that small double-count on FY2019 and FY2020; the figures below are corrected.

## The headline

Combining the two pillars by fiscal year, with the GDEB-prime-only restriction applied to the subaward column:[^repo-summary-findings][^repo-subaward-annual][^repo-fpds-annual]

| FY | GDEB-prime subawards in USAspending ($M) | Navy → BPMI prime $ (per-mod GFE, $M) | Approx total annual outsourced flow ($M) |
|---|---:|---:|---:|
| FY2018 | 1,028 | 416 | **~1,444** |
| FY2019 | 994 | 1,912 | **~2,906** |
| FY2020 | 261 | 1,291 | **~1,552** |
| FY2021 | 706 | 2,000 | **~2,706** |
| FY2022 | 696 | 2,119 | **~2,815** |
| FY2023 | **3,813** | 1,430 | **~5,243** |
| FY2024 | **4,162** | 2,182 | **~6,344** |
| FY2025 | 761 (reporting lag) | 2,145 | ~2,906 (low due to lag) |

### Class-split headline (Virginia / Columbia / Mixed BPMI)

Each in-scope GDEB-prime construction PIID is class-pure at the contract-title level, so the first-tier subaward column can be cleanly split into Virginia-class and Columbia-class trails. The BPMI naval-reactor pillar serves both classes; at the cumulative contract-title level, approximately 35% of BPMI obligations are named Columbia, 14% are named Virginia, and 51% are generically titled "Reactor Components" without a class designator. Per-fiscal-year BPMI class allocation requires reading individual modification descriptions for SSN/SSBN hull-number references (the v1 lessons-learned mod-description technique) and is not implemented in the current aggregator; BPMI is therefore reported here as a single "Mixed (both classes)" trail.[^repo-subaward-class][^repo-aggregate-script]

| FY | Virginia GDEB-sub ($M) | Columbia GDEB-sub ($M) | BPMI mixed ($M) | Total visible ($M) |
|---|---:|---:|---:|---:|
| FY2018 | 775 | 252 | 416 | **~1,444** |
| FY2019 | 592 | 402 | 1,912 | **~2,906** |
| FY2020 | 202 | 59 | 1,291 | **~1,552** |
| FY2021 | 461 | 245 | 2,000 | **~2,706** |
| FY2022 | 375 | 322 | 2,119 | **~2,815** |
| FY2023 | 1,059 | **2,755** | 1,430 | **~5,243** |
| FY2024 | 512 | **3,650** | 2,182 | **~6,344** |
| FY2025 | 278 (lag) | 488 (lag) | 2,145 | ~2,911 (low due to lag) |

Three patterns the class split makes visible that the combined view obscures:

1. **The Virginia subaward trail is roughly flat across the window** — $0.2–1.1 billion per year, with no structural step change. FY24 Virginia GDEB-sub of $0.5 billion is in fact *lower* than FY18's $0.8 billion. The visible Virginia outsourced flow is not what's driving the headline growth.
2. **The Columbia subaward trail accounts for essentially all of the FY23–FY24 ramp** — from approximately $0.3 billion in FY22 to $2.75 billion in FY23 to $3.65 billion in FY24, an order-of-magnitude jump. Almost the entire FY23–FY24 step change in the combined headline is the BlueForge Alliance subaward stream on the Columbia Build I+II prime `N0002417C2117`.
3. **The BPMI reactor pillar is steady and class-mixed** — $1.4–2.2 billion per year regardless of which class is in heavier production. The cumulative split (~35% Columbia / ~14% Virginia / ~51% generic at the contract-title level) implies that per-FY Columbia probably receives more than Virginia from the BPMI line, but the per-FY allocation is not currently reconstructed.

A reader summarizing the trend with the class split should say: **"Visible Virginia outsourced flow is roughly flat; the entire FY23–FY24 ramp from $1.4 billion to $6.3 billion is Columbia, driven almost entirely by the BlueForge Alliance / Maritime Industrial Base subaward on the Columbia Build I+II prime; BPMI naval-reactor procurement serves both classes at a steady $1.4–2.2 billion per year."**

### Named-MIB filter (ex-BlueForge plus ex-BPMI Industrial Base Increase)

Two channels in the visible-channel headline are explicitly-named industrial-base / supplier-capacity investments rather than direct payment for components or services going into a hull. Filtering them out separates the underlying recurring outsourced flow from the one-time-ish capacity-investment layer:[^repo-mib-extracts]

- **BlueForge Alliance subawards** on the Columbia Build I+II prime contract `N0002417C2117`. BlueForge is a non-profit consortium pass-through to small and mid-tier submarine suppliers and workforce-training partners; the dollars do not go to component fabrication. Cumulative FY16 to FY25: approximately **$4,214 million** across approximately 7 reported subaward actions. Per-FY: $1,514 million in FY2023 and $2,700 million in FY2024; effectively zero in other years in the action-date window. (See [Maritime Industrial Base and BlueForge Alliance](07-maritime-industrial-base.md).)
- **BPMI `N0002419C2115` "Columbia Class Industrial Base Increase"** prime obligations. The contract title itself names this PIID as an industrial-base investment, distinct from BPMI's other PIIDs that buy reactor-plant components. Cumulative window obligations: approximately **$2,710 million** ($3.00 billion ceiling, fully committed). Per-FY new-money obligation: $890 million FY2019, $32 million FY2020, $662 million FY2021, $622 million FY2022, $504 million FY2023; effectively zero in FY2024 and later (the PIID closed out before the FY23–FY24 BlueForge ramp).

Subtracting both named-MIB channels from the visible-channel headline produces the ex-MIB underlying outsourced flow:

| FY | Visible (with MIB) ($M) | BlueForge MIB ($M) | BPMI IBI MIB ($M) | Named MIB total ($M) | **Ex-MIB underlying ($M)** |
|---|---:|---:|---:|---:|---:|
| FY2018 | 1,444 | 0 | 0 | 0 | **1,444** |
| FY2019 | 2,906 | 0 | 890 | 890 | **2,016** |
| FY2020 | 1,552 | 0 | 32 | 32 | **1,520** |
| FY2021 | 2,706 | 0 | 662 | 662 | **2,044** |
| FY2022 | 2,815 | 0 | 622 | 622 | **2,193** |
| FY2023 | 5,243 | 1,514 | 504 | 2,018 | **3,225** |
| FY2024 | 6,344 | 2,700 | 0 | 2,700 | **3,644** |
| FY2025 | 2,911 (lag) | 0 (lag) | 0 | 0 | **2,911** (lag) |
| FY2026 | 1,897 | 0 | 0 | 0 | **1,897** |

The trend ex-MIB is **still real growth, just smaller than the with-MIB headline implies**: the underlying component and services outsourced flow approximately doubled from $1.4 billion in FY2018 to $3.6 billion in FY2024, a 2.5× expansion driven by genuine supplier-base activity (Northrop Grumman sonar, DRS power distribution, Curtiss-Wright reactor pumps, Bechtel reactor procurement, and the Block IV / V / VI progression). The remaining $2.7 billion of the FY24 with-MIB headline is the named-MIB capacity investment layer that does not represent recurring component or services delivery.

A reader summarizing the trend with the MIB filter should say: **"With-MIB, the visible outsourced flow ramped from ~$1.4 billion (FY18) to ~$6.3 billion (FY24). Ex-named-MIB, the underlying component and services outsourced flow ramped from ~$1.4 billion (FY18) to ~$3.6 billion (FY24). The difference — the $2.7 billion FY24 'named MIB layer' — is supplier-capacity and workforce investment routed through the Columbia Build I+II prime (BlueForge Alliance) and the Naval Reactors program (BPMI Industrial Base Increase)."**

#### Caveat: "ex-named-MIB" is not "ex-all-MIB"

The named-MIB filter catches the two channels explicitly identified by recipient or contract-title naming. Other MIB-flavored flows are present in the underlying data but cannot be cleanly identified without mod-description sweeping:

- "Class Lead Yard Support" and similar engineering / supplier-development modifications inside the GDEB construction primes (`N0002417C2100`, `N0002417C2117`, and others). These modifications fund lead-yard support, engineering services, and supplier coordination that sit between "direct construction" and "MIB."
- DPA Title III activities routed through other supplier recipients.
- Supplier-capacity portions of the generically-titled BPMI "Reactor Components" PIIDs (`N0002416C2106`, `N0002424C2115`, `N0002412C2106`, others). These PIIDs run roughly half the BPMI total at the cumulative level and may contain some capacity-investment content mixed with component procurement.
- Future Hadrian Cherokee, Alabama factory recurring component production (post-2026, not yet in the data; the $2.4 billion facility stand-up is itself MIB but the recurring flow once operational will be direct-construction subaward flow).

The ex-MIB number is therefore a **lower bound on the named-MIB capacity layer and an upper bound on the underlying component / services flow**. A more complete MIB filter would require mod-description sweeping and is left as a future-pass refinement.

The trend is unmistakable. The combined publicly visible annual outsourced flow rose from approximately **$1.4 billion in FY2018** to a peak of approximately **$6.3 billion in FY2024**, an approximately 2–3× expansion over a six-year window. The bulk of the FY2023–FY2024 step change is the **BlueForge Alliance / Maritime Industrial Base ramp** on the Columbia Build I+II prime contract `N0002417C2117` (BlueForge subaward records of approximately $2.75 billion in FY2023 and $3.65 billion in FY2024). The FY2025 number is depressed by the typical 6–18 month FFATA subaward reporting lag; the true number will revise upward as filings catch up over the following 12–18 months, with the magnitude of the revision sensitive to which prime PIIDs file late and how heavily.[^repo-summary-findings][^repo-lessons-v1]

## What is and is not in the headline

### Included

- **First-tier subawards on the 12 GDEB and BPMI in-scope submarine PIIDs** with non-zero subaward records. This includes:
  - GDEB Virginia Block IV, V/VI master, Block VI LLTM, VPM Ventilation Valve, Columbia Design Drawings, Virginia HPAD, USS *Hartford* EOH, plus several others.
  - BPMI Naval Reactor Components Columbia, BPMI Columbia Industrial Base Increase.
- **Per-modification new-money obligation on Bechtel Plant Machinery prime contracts** in FPDS across the FY18–FY26 window. This captures the steady $1.4–2.2 billion per year of naval reactor procurement.

### Excluded from the headline (significant)

The headline does **not** add the following categories, even though some of them are genuine outsourced flow that belongs in a more complete view:

1. **Lockheed Martin Trident II D5 / D5LE2 prime contracts.** Trident is funded outside the SCN appropriation under separate Navy Strategic Systems Programs (SSP) line items. The FY20, FY21, FY24, and FY25 Trident Production & Deployed Systems Support contracts each carry approximately $1.1–1.2 billion of cumulative obligation. Including Trident would overstate the SCN-funded outsourced flow.[^repo-sam-prior]
2. **Lockheed Martin Virginia-class combat systems prime (`N0002410C6266`).** Approximately $899M cumulative obligated against a $1.37B ceiling. This is a direct Navy prime contract with LM, separate from the GDEB construction contract. Some portion of the LM combat-systems work likely appears inside the GDEB Electronics cost-category line in the SCN P-5c, so adding the LM prime to the GDEB subaward total without checking for overlap would double-count.[^repo-sam-prior]
3. **The Lockheed Martin TI18 SSBN Material & Kit Additions prime (`N0002417C6259`, ~$1.02B cumulative)** and related GD Mission Systems SSBN fire-control contracts (`N0003014C0005`, `N0003010C0005`, `N0003016C0005`). These fund Columbia SSBN combat / fire-control work and are routed through the SSP office, not through the SCN line.[^repo-sam-prior]
4. **HII Newport News Shipbuilding team-build share.** Per the team agreement, HII-NNS performs approximately 50% of Virginia and approximately 22% of Columbia construction. This work flows through the GDEB prime via the team agreement and is not consistently recorded as HII-NNS vendor-of-record in FPDS. The visible HII-NNS subaward of GDEB is approximately $98 million cumulative FY16–FY25, which dramatically understates the real share. Public NAVSEA contract announcements occasionally name HII-NNS directly (the April 2025 modification announcement for FY24 Virginia construction publicly named HII-NNS at approximately $1.3 billion), but the FPDS recording for the same action lists vendor-of-record as `ELECTRIC BOAT CORPORATION`. The true HII-NNS submarine share is reconstructible from HII corporate financial disclosures plus the NAVSEA announcement stream and is out of scope for the current pass.[^repo-subaward-top][^repo-lessons-v1]
5. **Federal naval shipyard depot work.** Excluded by definition — federal-employee payroll is not outsourcing. The four public naval shipyards (Norfolk, Portsmouth, Pearl Harbor, Puget Sound) consume the bulk of the $6 billion-plus annual Navy submarine depot maintenance budget.[^repo-lessons-v1]
6. **Classified payload modules.** Excluded by design — intelligence-community submarine modules are procured outside the public SCN appropriation.[^repo-readme]
7. **The long tail of small first-tier subawards on the two big GDEB master vehicles.** USAspending caps the `/api/v2/subawards/` response at approximately 2,000 records per prime. Both `N0002417C2100` (Virginia Block V/VI) and `N0002417C2117` (Columbia Build I+II) hit this cap. The top-spend subs are captured (sorted by amount descending), but the long tail of small subs is missing.[^repo-lessons-v1]

### Headline implications

The **published headline of approximately $1.4B (FY18) → $6.3B (FY24)** represents publicly visible outsourced flow with asymmetric coverage gaps. Several exclusions push the true total *higher*: a more complete view that includes (1) the GFE-prime spending on Lockheed Martin Trident, LM Virginia combat systems, and LM SSBN material, and (2) an estimated HII-NNS team-build share derived from HII corporate disclosures would produce a meaningfully higher annual number. Other data-quality issues — most importantly the absence of v3 subaward dedup — could push specific subaward-driven lines (especially the largest recipients with long-running primes) *lower* once corrective methodology is applied. The two effects do not cancel; they operate on different parts of the table. Without v3 dedup and an HII-NNS estimate in place, this article reports the visible-channel view explicitly and flags the directionality of each known correction.

## Direction of the trend

The trend direction is unambiguous: **the annual visible outsourced flow has grown approximately 2–3× from FY2018 to FY2024**, with most of the increase concentrated in FY2023 and FY2024 and driven by the BlueForge Alliance / Maritime Industrial Base ramp on Columbia. The Bechtel Plant Machinery naval-reactor flow has also grown — from approximately $416 million in FY2018 to approximately $2.1 billion in recent years — but the growth there is roughly linear and started earlier.

The composition of the flow has shifted:

- **Before FY2023:** BPMI naval reactor procurement and GDEB first-tier subawards (Northrop Grumman, Curtiss-Wright, BAE, Scot Forge, etc.) were comparable in size. The total visible flow was approximately $1.5–3 billion per year.
- **After FY2023:** BlueForge Alliance Maritime Industrial Base subawards dominate the GDEB subaward column, lifting the combined total to approximately $5–6 billion per year. Conventional supplier-base subawards continue at roughly the pre-FY23 rate; the new MIB flow is additive.

A reader summarizing the trend in one sentence should say: **"The visible outsourced flow on U.S. nuclear submarine construction grew from roughly $1.4 billion per year in FY2018 to roughly $6 billion per year in FY2024, driven mostly by the new Maritime Industrial Base supplier-development line on Columbia and steady growth in BPMI naval-reactor procurement; the true outsourced flow is probably higher overall — because the HII-NNS team-build share, the Lockheed Martin combat-system and Trident GFE primes, and the long tail of small subs on the two big GDEB master vehicles are not in the visible number — but some of the largest subaward lines may also be modestly overstated until v3 dedup is applied."**

## Confidence and what would improve it

The headline carries three notable uncertainties:

1. **The aggregator does not apply v3 subaward dedup.** USAspending's `/api/v2/subawards/` endpoint has a documented cumulative-snapshot duplication issue that can inflate naive sums of `amount` records by 5×–50× when the same `sub_id` appears at multiple action dates with cumulative-style amounts. The companion v2 lessons-learned material describes a three-stage v3 dedup methodology (per-`sub_id` MAX, identical-amount collapse, cap at prime contract size) that materially reduces this inflation. The aggregator in this repository does not implement v3 dedup; it performs only naive sums. This means the reported subaward column may be **overstated** for fiscal years where the dominant subaward flow has many cumulative-snapshot duplicates per `sub_id` (most likely for the largest, longest-running subs — Northrop Grumman, BlueForge, BAE, Curtiss-Wright). Re-running with v3 dedup applied would tighten the headline, likely downward.[^repo-lessons-v2][^repo-aggregate-script]
2. **The FY2025 reporting lag is large.** The reported $766M GDEB subaward column for FY2025 is consistent with approximately 6–18 months of FFATA reporting lag on a year in which the underlying prime activity (per-mod obligation, FPDS) is comparable to FY2024. The true FY2025 subaward flow will revise upward as filings catch up; companion analysis of similar lag patterns suggests the eventual figure could be several billion dollars higher than the $766M currently reported, but the precise magnitude is sensitive to which prime PIIDs file late and is not formally modeled here. The FY2025 row in the headline table should be read as understated by an unmodeled amount.[^repo-lessons-v1]
3. **The GDEB column hits the ~2,500-record retrieval cap on the two big masters.** The pull script paginates at 25 pages × 100 records. For Virginia Block V/VI and Columbia Build I+II, the long tail of small subs is missing. This is an unrelated source of understatement (separate from the dedup-overstatement risk above).[^repo-lessons-v1]

A future revision of this analysis that:

- Applies v3 dedup to the subaward records,
- Adds an HII-NNS team-build estimate from HII corporate disclosures,
- Adds the Lockheed Martin Virginia combat-system and SSBN material flows (with overlap-checking against the SCN Electronics line), and
- Waits 12–18 months for FY2025 FFATA reporting to clear,

would produce a substantially more complete view of the annual outsourced flow. The current headline is the floor view that the available data supports today.

[^repo-subaward-annual]: submarine_outsourced_work, "extracted/subaward_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-fpds-annual]: submarine_outsourced_work, "extracted/fpds_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).

[^repo-summary-findings]: submarine_outsourced_work, "SUMMARY_INITIAL_FINDINGS.md." See full citation under [References](INDEX.md#references).

[^repo-sam-prior]: SAM Submarine & Cutter Contract Awards (April 2026). See full citation under [References](INDEX.md#references).

[^repo-subaward-top]: submarine_outsourced_work, "extracted/subaward_top_recipients.csv." See full citation under [References](INDEX.md#references).

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^repo-lessons-v2]: Subaward Pull Lessons Learned (v2). See full citation under [References](INDEX.md#references).

[^repo-aggregate-script]: submarine_outsourced_work, `scripts/aggregate_annual_outsourcing.py`. See full citation under [References](INDEX.md#references).
