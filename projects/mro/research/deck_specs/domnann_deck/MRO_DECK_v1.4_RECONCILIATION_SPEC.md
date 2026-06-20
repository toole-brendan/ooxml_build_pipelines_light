================================================================================
MRO DECK v1.4 -- RECONCILIATION SLIDES SPEC
Purpose: Detailed spec for the slides that collectively prove the $7.1B MRO TAM
reconciles against Navy / USCG budget materials. Replaces v1.3 Slide 3
(Addressable vs Adjacent Spend / waterfall frame) with a new Slide 3 (Scope
Reconciliation / 2x2 frame), elevates Slide 9 (Appropriation Sourcing) from
appendix to main-deck Slide 4, and trims appendix Slide 10 (Frame A / B).

Companion file: deck/MRO_DECK_v1.3_WALKIN_SPEC.md carries the full 10-slide
spec with renumbering applied. This file carries the deep detail and research
plans for Slides 3, 4, and 10 only.
================================================================================


# Why these slides matter most right now

The boss question that these three slides answer -- Q2, "what's in scope vs
out of scope and how do you know?" -- is THE pivotal question of the walk-in.
Every other slide depends on the $7.1B TAM being a defensible number. If these
three slides aren't tight, nothing downstream lands.

The v1.3 draft attempted this with three separate arguments:
  - Slide 3 (waterfall): reduce $56.6B "total pool" to $7.1B via subtractions
  - Slide 9 (appendix): compose $7.1B into ~10 federal appropriations
  - Slide 10 (appendix): hedge with Frame A vs Frame B apportionment

Two problems with v1.3:
  (a) The $56.6B "total pool" on Slide 3 is a frankenpool that mixes FPDS
      obligations with budget-implied labor and reactor procurement. The
      tie-out is suspiciously exact because the pool is defined as the sum
      of the deductions.
  (b) The $9,536M "implied public-yard labor" on Slide 3 has three weak
      joints (wrong top, wrong bottom, wrong residual-interpretation) and
      cannot be defended with a workbook cell.

v1.4 response:
  - Slide 3 reframes as a 2x2 matrix. The $7.1B is the intersection of two
    independent axes, not the residual of a subtraction chain. Adjacent cells
    (public-yard labor, newbuild PSC 1905, reactor PSC 4470, unmeasured
    in-house RDT&E) are shown explicitly, not subtracted.
  - Slide 4 (promoted from appendix) drops the $7.4B pre-exclusion universe
    and rebases all appropriation figures to $7,067M. The 49 / 51 direct vs
    imputed TAS attribution split moves from footnote to foreground.
    (Verified against data_pull/output/usaspending/approp_rollup_imputed.json:
    direct $3.645B, imputed $3.761B, total $7.406B universe.)
  - Slide 10 trims to a single appendix slide with decision-linked framing
    ("use Frame A for market-entry decisions, use the segment-level Frame B
    rates for contractor-modeling") instead of "industry convention".


# Revised slide order (v1.4)

| # | Title | Change vs v1.3 |
|---|---|---|
| 1 | Cover | unchanged |
| 2 | TAM & Scope | unchanged |
| 3 | Scope Reconciliation | NEW -- replaces Addressable vs Adjacent waterfall |
| 4 | Appropriation Sourcing | MOVED from appendix; numbers rebased to $7,067M |
| 5 | MRO Work Segments | was Slide 4 |
| 6 | Vessel Mix | was Slide 5 (submarine-MRO callout de-quantified) |
| 7 | Fleet Reference + Hull-Class % | was Slide 6 |
| 8 | Marauder-Like Platform TAM | was Slide 7 |
| 9 | Prime Landscape | was Slide 8 |
| 10 | TAM Framing -- Frame A vs Frame B (appendix) | trimmed |

Slides 3 and 4 form the "defensibility block". Reading them back-to-back, the
boss should leave with: the TAM is the intersection of two measurement systems
(Slide 3), and its composition on the budget side traces to auditable
appropriation lines (Slide 4).


================================================================================
SLIDE 3 -- SCOPE RECONCILIATION [NEW in v1.4]
================================================================================

# BREADCRUMB
Commercial Strategy / Defense Demand Drivers

# TITLE
Scope Reconciliation | $7.1B MRO TAM is the intersection of Navy / USCG ship-sustainment appropriations and ship-services PSCs in FPDS

# LEDE
Budget exhibits and FPDS obligations are two different views of Navy and Coast Guard ship spending. The MRO TAM is the slice visible in both -- economic activity that is both (a) ship-MRO in character and (b) contracted out to private industry. Adjacent cells explain what's nearby but structurally out of scope.

# JOB OF THIS SLIDE
Prove the $7.1B. Establish for the boss that this number isn't an FPDS curiosity -- it's the defensible intersection of two independent measurement systems (appropriation-side and execution-side). Label each adjacent cell (public-yard labor, newbuild PSC 1905, reactor PSC 4470, unmeasured in-house RDT&E) so downstream questions about "what's not in here" are pre-answered. Replace the v1.3 reduction waterfall (which required constructing a $56.6B total pool of mixed provenance) with a two-axis frame that doesn't require any made-up totals.

# LHS VISUAL -- 2x2 MATRIX

Horizontal axis: FPDS-visible (private contract) vs Not FPDS-visible (in-house / NWCF)
Vertical axis: Ship-MRO economic activity vs Ship spending, non-MRO

-----------------------------------------------------------------------------------------------------
                      |  FPDS-visible (private contract)   |  Not FPDS-visible (in-house / NWCF)
-----------------------------------------------------------------------------------------------------
Ship MRO              |  [HIGHLIGHTED TAM CELL]            |  Public-yard labor
economic activity     |                                    |
                      |  $7,067M MRO TAM                   |  Civilian federal workforce at
                      |  68 Services PSCs, Navy + USCG,    |  Portsmouth, Norfolk, Puget Sound,
                      |  post-exclusions                   |  Pearl Harbor. NWCF-funded; no FPDS
                      |  (deck focus)                      |  record. Size: pending direct NWCF
                      |                                    |  sourcing (see research below).
-----------------------------------------------------------------------------------------------------
Ship spending,        |  $38,100M Newbuild (PSC 1905,      |  Not measured
non-MRO               |  Navy + USCG) -- includes est. $X  |
(by PSC)              |  of nuclear engineered overhauls   |  Primarily in-house ship-design and
                      |  and depot work bundled as         |  systems-engineering RDT&E labor at
                      |  shipbuilding                      |  warfare centers and SYSCOMs; outside
                      |                                    |  reconciliation scope.
                      |  $1,875M Reactor components        |
                      |  (PSC 4470) -- BWXT Lynchburg and  |
                      |  reactor OEMs; new cores and       |
                      |  long-lead parts                   |
-----------------------------------------------------------------------------------------------------

Visual treatment: top-left cell highlighted (filled background, emphasized type) as the TAM ("deck focus"); the other three cells are de-emphasized (neutral fill, smaller type). $ amounts left-aligned; labels below. No arrows or connectors -- the axis labels carry the logic.

# RHS COMMENTARY -- THREE CALLOUT CARDS

**Top-right -- Public-yard labor (budget-side only)**
The four public naval shipyards are NWCF industrial activities; their civilian workforce executes depot availabilities on SSNs, SSBNs, and CVNs without generating FPDS contract records. This cell is where the "submarine MRO looks understated" story lives -- most nuclear depot work on strategic and attack submarines is performed in-house at Portsmouth, Puget Sound, and Pearl Harbor.

**Bottom-left -- Newbuild and reactor PSCs (FPDS-visible, non-MRO by PSC)**
PSC 1905 is predominantly ship construction, but is known to contain MRO -- e.g., HII's $424M USS Boise SSN-764 Engineered Overhaul at Newport News is coded 1905 rather than J998 / J999. Under a work-type-first classification, an estimated $X of PSC 1905 would migrate into the MRO TAM; this is the load-bearing reason the $7.1B is a floor, not a ceiling, on submarine MRO activity. PSC 4470 is reactor-component procurement (not sustainment) -- new cores, long-lead forgings, and reactor OEM spares.

**Bottom-right -- Not measured**
Ship-design RDT&E labor performed in-house at Naval Surface Warfare Centers, Naval Undersea Warfare Centers, and SYSCOM headquarters. Out of scope for market sizing; noted here to close the matrix.

# FOOTER NOTES
(1) Public-yard cell: $[direct NWCF number] for FY2025, sourced to [NWCF exhibit]. As an interim bound while direct sourcing is pending: OMN SAG 1B4B less CE-928 implies ~$9.5B (suspect -- see research); bottom-up from ~35-40k FTE at public shipyards at fully-loaded labor rates gives ~$5-8B labor-only.
(2) PSC 1905 embedded MRO share: estimated at $X via keyword + POP-length + vendor-pattern classification (method in docs/methodology/psc_1905_mro_share.md, to create).
(3) Exclusions applied to the $7,067M: shore-base work and Foreign Military Sales, approximately $333M combined; see Slide 4.

# SOURCE
FPDS FY2025 contract obligations (U.S. Navy and U.S. Coast Guard, Awards master, post-exclusions); FY2026 President's Budget exhibits (OMN Vol 1 SAG 1B4B OP-5, SCN P-1, NWCF volume); directly-sourced NWCF depot-ship customer-order data [pending]. Data as of April 2026.

# RESEARCH NEEDED -- SLIDE 3

**[PRIORITY 1] Replace the implied public-yard number with a directly-sourced NWCF figure.**

Why: the v1.3 number ($9,536M implied from OMN 1B4B minus CE-928) is the single weakest derivation in the deck. Three reasons it's suspect:
  (a) OMN 1B4B may not be the full universe of ship maintenance if OPN BA-7 also funds availabilities.
  (b) CE-928 is one cost element under 1B4B and may not capture all private contract maintenance.
  (c) The residual "everything else in 1B4B" is not necessarily all public-yard labor -- it likely also includes material, inter-service transfers, travel, and facility support.

What to look for: total NWCF customer-order revenue for depot-ship activities, FY2025 (or most recent actual).

Sources to check, ordered by likelihood of success:
  1. Navy Working Capital Fund budget volume, FY2026 President's Budget (PB-26) or FY2025 actuals in PB-25. Look for section "Operations -- Depot Maintenance, Ship" or equivalent. Should report gross revenue, net operating result, and customer-order composition by appropriation source and by activity (the four public shipyards as named industrial activities).
  2. NAVSEA Naval Shipyard public-affairs releases or strategic workforce plans (publicly available via navsea.navy.mil).
  3. OUSD Comptroller working-capital-fund reports (comptroller.defense.gov).
  4. DFAS WCF exhibits.
  5. GAO reports on public shipyard capacity (periodic; most recent GAO report on SIOP -- Shipyard Infrastructure Optimization Program -- may cite revenue figures).

If found: replace the "Size: pending" label in the top-right cell with the direct number. Update footnote (1) to cite the exhibit directly and remove the OMN 1B4B derivation entirely.
If not found: present the cell as a bounded range ("~$8-12B") with both the OMN derivation (upper bound proxy) and bottom-up labor estimate (lower bound proxy) cited in footnote.
Effort: 2-4 hours.

**[PRIORITY 1] Quantify PSC 1905 embedded MRO share.**

Why: required to populate "est. $X of nuclear engineered overhauls" in the bottom-left cell and in RHS callout card #2. Without a number, the "TAM is a floor, not a ceiling" narrative is hand-waving.

What to look for: $ subset of the $38,100M PSC 1905 FY2025 Navy + USCG obligations that is MRO-character rather than newbuild-character.

Method:
  1. Pull all PSC 1905 PIIDs from the Awards table (or FPDS directly) for FY2025 Navy + USCG.
  2. Tag each PIID on three dimensions:
     - Description keyword scan. MRO-positive: {"engineered overhaul", "refueling", "refueling complex overhaul", "RCOH", "DSRA", "selected restricted availability", "extended drydocking", "depot maintenance", "modernization", "availability"}. Newbuild-positive: {"construction", "detail design", "build", "delivery", "fabrication", "new construction"}.
     - POP-length heuristic. Newbuild POPs typically 4-7 years from award to delivery; MRO POPs typically 6-24 months. Compute pop_end_date minus pop_start_date; flag outliers.
     - Vendor pattern. HII Newport News does both construction (CVN-80 Enterprise, CVN-81 Doris Miller) and engineered overhauls (SSN-764 Boise, RCOH on Nimitz-class CVNs); GD Electric Boat does both Virginia-class newbuild and SSN reactor work. Classify at PIID level, not vendor level.
  3. Output: single $ number with method described in a methodology doc; insert into bottom-left cell; update footnote (2).

Expected result: plausibly $1-5B depending on tagging aggressiveness. Even a modest $2B embedded figure materially changes the "is the TAM a floor or ceiling?" story.
Effort: 1 day. Data access is straightforward (Awards table has all required fields).
Output location: new file docs/methodology/psc_1905_mro_share.md.

**[PRIORITY 2] Source the OPN BA-7 depot-availability funding claim.**

Why: Slide 4 (Appropriation Sourcing) asserts depot availabilities are funded through OPN BA-7 rather than OMN CE-928. This claim partly resolves the Slide 3 / Slide 4 tension about where availability dollars flow. Without a citation, it's an assertion that a Navy comptroller can challenge.

Sources to check:
  - OPN P-5 justification book (FY2026 Navy). Look for "Ship Depot Availability" or similar line items in BA-7.
  - NAVSEA Type Commander (TYCOM) or Fleet budget submissions.
  - DoD Financial Management Regulation (FMR Volume 2B, Chapter 11) for appropriation-to-maintenance-type rules.
  - CNO availability planning guidance.

If found: cite in Slide 4 RHS callout card 3 and in Slide 3 footnote. Removes the last load-bearing uncited assertion from the deck.
If the picture is more mixed (e.g., OMN and OPN both fund availabilities with a ratio): revise the Slide 4 claim to match reality. This will weaken the contradiction with Slide 3's old $9.5B public-yard derivation, which is another reason direct NWCF sourcing (Priority 1) matters.
Effort: 2-4 hours.

**[PRIORITY 2] Break down the $333M shore-base and FMS exclusions.**

Why: the $7.067M post-exclusion number is derived from the $7.4B pre-exclusion MRO-PSC universe by removing ~$333M. Document what that $333M contains so the exclusion is defensible.

Method: the Awards table likely already has exclusion flags (shore_base_flag, fms_flag, or similar); tabulate and summarize.
Effort: 1-2 hours.
Output: one-line footnote addition to Slide 3, or a short methodology note in docs/methodology/mro_exclusions.md.

**[PRIORITY 3] Allocate public-yard NWCF total to nuclear vs conventional.**

Why: once the top-right cell has a direct NWCF number (Priority 1), the submarine-MRO-understatement callout on Slide 6 (Vessel Mix) can be re-quantified with a defensible number (replacing the dropped "$4-6B" figure).

Method: per-yard customer-order breakouts in NWCF exhibits (if available) or per-yard workforce mix from NAVSEA public sources. Portsmouth ~100% SSN; Puget Sound ~80% nuclear (SSN / SSBN / CVN) + 20% conventional; Pearl Harbor ~90% SSN + small surface; Norfolk ~60% CVN RCOH + 40% conventional surface. Weight by yard revenue to get nuclear vs conventional split.
Effort: 2-3 hours, assuming per-yard revenue is available.


================================================================================
SLIDE 4 -- APPROPRIATION SOURCING [MOVED from appendix in v1.4]
================================================================================

# BREADCRUMB
Commercial Strategy / Defense Demand Drivers

# TITLE
Appropriation Sourcing | The $7.1B MRO TAM is funded by ~10 federal appropriations, with Navy OMN and OPN together at 72%

# LEDE
On the budget side, the $7,067M MRO TAM traces to Navy OMN and OPN (together funding ~72% of obligations), RDT&E Defense-Wide (11%, almost entirely Trident / SSP / SMDC sustainment), and smaller shares from USCG, Air Force, Army, and SCN. OPN is concentrated in BA-7 (Personnel & Command Support Equipment -- funds modernization and C4ISR installation) and BA-8 (Spares & Repair Parts).

# JOB OF THIS SLIDE
Show where the $7.1B comes from on the budget side. Answer the boss question "which appropriations pay for ship MRO?" so a comptroller-savvy reader can reconcile this deck against Navy budget materials and know what to ask the Navy comptroller shop for. Reinforce Slide 3's defensibility: the TAM is not only an intersection of two measurement systems (Slide 3), its composition on the appropriation side follows an auditable, documentable structure (Slide 4).

# CHANGES FROM v1.3 SLIDE 9

1. **Scrap the $7.4B pre-exclusion universe.** All per-appropriation $M figures recomputed by applying the existing ratios to $7,067M. Removes a distracting secondary number that invited "which number is right?" questions.
2. **Foreground the 49 / 51 direct-TAS / imputed split.** Move from footnote (1) to a top-of-slide callout card. Readers trust the numbers more when the imputation is disclosed upfront.
3. **Cite the BA-7 depot-availability claim.** Replace the unsourced assertion with a specific budget-exhibit reference (pending research; see Priority 2 above).
4. **Remove old footnote (2)** on the $7.4B vs $7.067M reconciliation -- not needed once the slide is consistent with the rest of the deck.
5. **Promote from appendix to main deck.** Defensibility block (Slides 3 + 4) sits together.

# LHS CHART SUBTITLE
FY2025 MRO TAM obligations by Treasury appropriation -- OPN drilled to Budget Activity ($M, TAS-attributed)

# LHS CHART -- TWO 100%-STACKED COLUMNS SIDE BY SIDE

Column 1 (MRO TAM by appropriation, Total $7,067M):
  OMN:                            $2,615M (37%)
  OPN:                            $2,473M (35%)
  RDT&E, Defense-Wide:              $778M (11%)
  AF / Army / SCN / other:          $353M  (5%)
  USCG:                             $283M  (4%)
  DW other:                         $283M  (4%)
  Navy other:                       $283M  (4%)

Column 2 (OPN by Budget Activity, OPN Total $2,473M):
  BA-7 Personnel & Cmd Support Equip: $1,533M (62%)
  BA-8 Spares & Repair Parts:           $791M (32%)
  Other BAs:                            $173M  (7%)

Note on numbers: ratios shown here are the v1.3 ratios (originally computed against $7.4B) applied to $7,067M. Percentages will need 1-2 p.p. reconciliation so the $M figures sum precisely to $7,067M. See research task below.

# LEGEND
Navy-direct (OMN / OPN / Navy-other) | Defense-Wide (RDT&E-DW + DW-other) | Other agencies (USCG, AF, Army, SCN)

# RHS CALLOUT CARDS -- TAKEAWAYS (in order of emphasis)

**[FOREGROUND] 49% of MRO $ are directly TAS-attributed; 51% are imputed from peer PSCs**
Direct attribution uses USAspending's /awards/funding/ endpoint (Treasury File C) to tie each award to its specific Treasury Account Symbol. Where the endpoint returns no match, the award inherits the appropriation mix observed in the directly-attributed peers within the same PSC bucket. Rollup totals are stable across the direct and imputed split; per-award precision is lower for the imputed subset. (Verified: $3.645B direct / $3.761B imputed, total $7.406B universe per approp_rollup_imputed.json coverage key.)

**Navy OMN and OPN drive 72% of MRO obligations**
Navy sustainment is the dominant funding source. The MRO market is a Navy story, not a DoD-wide one. USCG is only 4% of obligations.

**OPN concentrates in Command Support Equipment (62%) and Spares (32%)**
BA-7 funds installation and modernization electronics, C4ISR, and combat-system integration. BA-8 funds spares and repair parts. Depot availabilities (DSRAs, DPIAs, CNO avails) are funded through BA-7, not through OMN CE-928 [source: pending; see research].

**RDT&E Defense-Wide contributes 11%**
Almost entirely Trident II, Strategic Systems Programs (SSP), and Space and Missile Defense Command (SMDC) sustainment on J-series PSCs. Draper MK7 Trident ($318M FY2025) is the single-largest MRO PIID and is funded here.

**SCN contributes approximately $40M on MRO PSCs**
De minimis at the PSC level. Nuclear-platform MRO bundles under PSC 1905 shipbuilding rather than onto MRO PSCs; see Slide 3 for the full scope reconciliation.

# FOOTER NOTES
(1) Direct TAS attribution via USAspending /awards/funding/ endpoint; imputed attribution applies per-PSC-bucket appropriation ratios from the directly-classified peer sample to awards without a matched TAS. Rollup totals are stable across the direct / imputed split
(2) OPN BA-7 depot-availability funding per [specific source: pending research]
(3) All figures on a post-exclusion ($7,067M) basis. Shore-base and FMS exclusions (~$333M) are treated proportionally across appropriations; see Slide 3 footnote (3)

# SOURCE
USAspending /awards/funding/ joined to FPDS FY2025 contract obligations (U.S. Navy and U.S. Coast Guard, 68 services PSCs, post-exclusions). Data as of April 2026.

# RESEARCH NEEDED -- SLIDE 4

**[PRIORITY 1] Recompute the appropriation $M table on the $7,067M basis.**
Mechanical conversion. Take the existing per-appropriation ratios (37%, 35%, 11%, 5%, 4%, 4%, 4%) from the $7.4B basis, apply to $7,067M, round to whole $M, and reconcile so the sum is exactly $7,067M. Same for the OPN BA drilldown ratios (62%, 32%, 7%) against $2,473M. Document the conversion in a one-line footnote.
Effort: 30 minutes.
Output: updated tables above with exact reconciled numbers.

**[PRIORITY 2] Source the OPN BA-7 depot-availability funding claim.**
Same research task as Priority 2 under Slide 3 -- single effort benefits both slides.

**[PRIORITY 3] Per-segment appropriation mix table (optional extension).**
Optional supplementary table. For each work segment (Depot Ship Repair, HM&E, Combat Systems, Electronics & C4ISR, Port & Technical), show the appropriation mix. E.g., Depot Ship Repair is likely ~80% OMN; Combat Systems Sustainment is likely ~60% RDT&E-DW + 30% OPN BA-7; etc. Ties Slide 4's appropriation story directly to Slide 5's segment story.
Effort: 1-2 hours (data exists; verification and formatting are the work).
Value: helps modelers tie segment-level revenue to specific appropriation pots.
Output location: a secondary small table on Slide 4, or a standalone appendix slide if the segments deserve more room.


================================================================================
APPENDIX SLIDE 10 -- TAM FRAMING -- FRAME A vs FRAME B [TRIMMED in v1.4]
================================================================================

# BREADCRUMB
Appendix / TAM Framing

# TITLE
TAM Framing | The $7.1B contracting TAM apportions to a ~$3.3-3.8B range of FY2025-delivered contractor revenue under period-of-performance sensitivity

# LEDE
The $7,067M MRO TAM measures contract obligations -- the flow of contract dollars transacted in FY2025. Contractor revenue earned in FY2025 is a different number, obtained by apportioning each award's obligation over its period of performance; that estimate falls in a $3.3-3.8B range depending on apportionment method. The deck uses the obligation number (Frame A) throughout; this appendix exists to support readers who model specific public comps on an earned-revenue basis (Frame B).

# JOB OF THIS SLIDE
Acknowledge that $7.1B is a contracting-activity number (Frame A) that differs from contractor-revenue numbers (Frame B) by roughly 50%. Give readers modeling specific public comps the per-segment conversion rates. Preempt the "why don't your numbers match HII Mission Technologies's 10-K" objection without elevating it to a main-deck story.

# CHANGES FROM v1.3 SLIDE 10

1. **Replace "industry convention" framing with decision-linked framing.** The Frame A choice is defended by the reader's decision (market-entry, capability-build, acquisition), not by industry habit.
2. **Emphasize segment-apportionment spread (19-71%) more prominently.** The 2.7x spread across work segments is the most important takeaway for anyone applying blended apportionment -- the 47.5% blended rate is unsafe for single-segment or single-contractor modeling.
3. **POP-vs-delivery caveat moved up.** Acknowledge that POP is the contract window, not the work-delivery window, in footnote (2) rather than buried in footnote (3).

# TOP STRIP -- Obligations x Apportionment = Revenue

Obligations
  $7,067M Frame A (FPDS FY2025 MRO TAM, this deck's primary number)

Apportionment
  Share of each award's period-of-performance landing inside FY2025

Revenue
  $3.27B - $3.75B Frame B range (POP-apportioned contractor revenue)

# LHS CHART SUBTITLE
FY2025 Services MRO TAM by period-of-performance apportionment method ($M)

# LHS CHART -- LEGEND
Frame A -- contract obligations (deck primary)
Frame B -- revenue earned approximation, POP-apportioned (sensitivity)
Central Frame B estimate ~$3.5B (49% of Frame A)

# LHS CHART -- BARS
Frame A (No apportionment):               $7,067M -- 100%
M2 (12-mo POP cap):                       $3,747M -- 53%
M3 (18-mo POP cap):                       $3,499M -- 49%
M1 (Pure linear, primary Frame B):        $3,354M -- 48%
M4 (Front-loaded 60 / 40):                $3,266M -- 46%

# LHS CHART -- FRAME B RANGE CALLOUT
$3.27B - $3.75B

# RHS TABLE -- SEGMENT APPORTIONMENT

Work Segment                  | Frame A $M | Frame B M1 $M | Apport %
Port & Technical Services     |        431 |           307 |    71.3%
Depot Ship Repair             |      4,781 |         2,468 |    51.6%
HM&E                          |        938 |           363 |    38.7%
Electronics & C4ISR           |        333 |           105 |    31.4%
Combat Systems Sustainment    |        585 |           112 |    19.1%
Total                         |      7,067 |         3,354 |    47.5%

# RHS CALLOUT -- DECISION-LINKED FRAMING NOTE

Frame A measures the flow of contract dollars that the market will transact -- the number relevant to market-entry, capability-build, and acquisition decisions. Frame B approximates existing-contractor revenue -- the number relevant to modeling specific public comps on an earned-revenue basis. This deck is sizing the former. Readers modeling the latter for a specific contractor should multiply their relevant segment $ by that segment's apportionment rate (above), not by the blended 47.5% -- the 19-71% spread across segments makes the blended rate unsafe for single-segment modeling.

# FOOTER NOTES
(1) FY2025 window: 2024-10-01 to 2025-09-30. POP apportionment uses start_date and end_date fields on FPDS award rows (100% populated in the MRO dataset)
(2) POP is the contract window, not the work-delivery window. For short-POP segments (depot availabilities deliver in weeks to months) Frame B linear undercounts actual FY25 delivery; for long-POP segments (combat-systems engineering services can span 5+ years) Frame B linear is reasonable. Segment-level calibration pending (see research)
(3) M1 Pure Linear is the primary Frame B estimate; M2 through M4 are bounds on reasonable apportionment assumptions

# SOURCE
FPDS FY2025 contract obligations (U.S. Navy and U.S. Coast Guard, 68 services PSCs, post-exclusions). Period-of-performance dates per FPDS. Data as of April 2026.

# RESEARCH NEEDED -- SLIDE 10

**[PRIORITY 3] POP-to-delivery calibration.**

Why: validate the M1 linear method against actual work-delivery windows on closed availabilities. Turns the appendix from "directional sensitivity" to "calibrated on actual closed work."

Method:
  1. Pick a sample of closed MAC-MO depot task orders where availability start and end dates are publicly knowable. DSRA / DPIA windows are published by the RMCs (SERMC, SWRMC, MARMC, etc.).
  2. For each sampled task order, compare FPDS pop_start / pop_end to the actual availability start / end.
  3. Compute empirical apportionment rate (share of contract $ landing in FY25 given actual work delivery) and compare to the M1 linear estimate.
  4. Optionally recompute segment-level apportionment rates using empirical multipliers on depot specifically; propagate to HM&E, Electronics, etc. where availability-linked work is material.

Output: "For closed depot availabilities in the sample, POP linear apportioned $X; actual work delivery apportioned $Y; divergence Z%. Segment-level apportionment rates recalibrated accordingly."
Effort: 1-2 days. Data assembly is the bulk of the work (scraping RMC availability schedules + joining to FPDS PIIDs).


================================================================================
RESEARCH PRIORITY SUMMARY
================================================================================

One consolidated list, ordered by defensibility leverage per hour of effort:

| Priority | Task | Slide | Effort | What it unlocks |
|---|---|---|---|---|
| 1 | Direct NWCF public-yard $ | 3 | 2-4 hr | Replaces imputed $9.5B with sourced number; strengthens top-right cell; indirectly enables Priority 3 (sub-MRO allocation) |
| 1 | PSC 1905 MRO share | 3 | 1 day | Quantifies "$X embedded MRO" callout; makes floor-vs-ceiling argument concrete |
| 1 | Rebase appropriation $M to $7,067M | 4 | 30 min | Mechanical; needed for Slide 4 numbers to reconcile |
| 2 | Source BA-7 availability funding | 3 + 4 | 2-4 hr | Removes last uncited assertion; resolves Slide 3 / 4 internal tension |
| 2 | $333M exclusion breakdown | 3 | 1-2 hr | Defends the shore-base / FMS footnote |
| 3 | Allocate NWCF to nuclear vs conventional | 6 | 2-3 hr | Re-quantifies sub-MRO understatement on Vessel Mix (depends on Priority 1 NWCF task) |
| 3 | Per-segment appropriation mix | 4 | 1-2 hr | Optional extension; ties appropriation to segment stories |
| 3 | POP-to-delivery calibration | 10 | 1-2 days | Strengthens Frame B appendix only |

If time before walk-in is tight, prioritize tasks #1 (NWCF direct, PSC 1905, Slide 4 rebase). The first two replace the two numbers the deck is currently citing with hand-waving; the third is mechanical cleanup that the deck needs regardless.


================================================================================
END OF RECONCILIATION SLIDES SPEC
================================================================================
