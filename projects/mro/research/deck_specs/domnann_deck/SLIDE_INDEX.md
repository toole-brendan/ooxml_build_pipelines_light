# Slide Index

Per-slide: lede, chart, commentary format. Pattern numbers refer to
`deck/DECK_RHS_PATTERN_MAP.md`.

---

## Chart title convention

All chart subtitles (the `slide-subtitle` element directly under the
chart head) follow a consistent schema so titles read the same across
the deck.

**Template:**

    [Time period] [Subject] by [Cut A]{ x [Cut B]}{ - [Auxiliary]} ([unit]{, qualifier})

**Rules:**

1. **Time period first** - always `FY2025` (or range if applicable,
   e.g., `FY2020-FY2025`)
2. **Subject** - the $ quantity actually visualized; choose the
   narrowest accurate term:
   - `MRO TAM` for the full $7.1B contracting TAM (slides 5, 8)
   - `J998 / J999 depot obligations` for the $4.9B depot subset
     (slides 6 LHS, 7, 9)
   - `MRO-PSC obligations` for the broader $7.4B pre-exclusion
     universe (slide 10)
   - `Services MRO TAM` for slide 11
   - `Navy and USCG ship-related spending` for slide 4 (waterfall
     context)
3. **`by` as the connector** from subject to cuts (unifies 1D and 2D
   cases - no mixing of `by` / comma / dash connectors)
4. **` x ` (lowercase ASCII `x`, spaces around)** for cross-tab cuts
5. **` - ` (hyphen with spaces)** for auxiliary info (Top-N, drill-
   downs, annotations)
6. **`($M)` or `($M, %)` or `($M, TAS-attributed)`** at the end -
   single parenthetical, comma-separated inside for multiple
   unit / qualifier items; do not use secondary parens like `($M) (%)`
7. **Sentence case** except for: acronyms (MRO, PSC, RMC, USCG, IDV,
   TAS, OPN, OMN), proper nouns (Navy, Coast Guard, Treasury, Budget
   Activity), PSC codes (J998, J999, 1905), command names (NAVSEA,
   MARMC, SWRMC), and fixed terms (Top 10)

**Per-slide proposed titles (canonical reference):**

| Slide | Chart | Title |
|---|---|---|
| 3 | approach-flow diagram | *no subtitle - title + lede carry the derivation* |
| 4 | waterfall | `FY2025 Navy and USCG ship-related spending reconciled to MRO contracting TAM ($M)` |
| 5 | mekko | `FY2025 MRO TAM by vessel type x work segment ($M)` |
| 6 LHS | mekko | `FY2025 J998 / J999 depot obligations by IDV scope x contractor segment ($M)` |
| 6 RHS | process flow | `Depot entry pipeline - MSRA to MAC-MO to task order` |
| 7 | mekko | `FY2025 J998 / J999 depot obligations by RMC region x contractor segment ($M)` |
| 8 | ranked columns + concentration callouts | `FY2025 MRO TAM by prime contractor - Top 10 with cumulative share ($M, %)` |
| 9 | ranked columns + concentration callouts | `FY2025 J998 / J999 depot obligations by prime contractor - Top 10 with cumulative share ($M, %)` |
| 10 | dual 100%-stacked columns | `FY2025 MRO-PSC obligations by Treasury appropriation - OPN drilled to Budget Activity ($M, TAS-attributed)` |
| 11 | combination chart | `FY2025 Services MRO TAM by period-of-performance apportionment method ($M)` |

**Changes vs. current HTML (for reference when rebuilding):**

- Slide 3: current subtitle `FY2025 Navy and USCG MRO TAM derivation`
  dropped entirely
- Slide 5: `Vessel Type x Work Segment` (Title Case) -> `vessel type
  x work segment` (sentence case)
- Slide 6 LHS: `- IDV scope group x contractor tier` ->
  `by IDV scope x contractor segment` (connector + segment rename +
  drop `group`)
- Slide 6 RHS: `three qualification tiers` phrasing dropped (tier-
  terminology collision)
- Slide 7: `contractor tier` -> `contractor segment`
- Slide 8: `MRO Obligations by Contractor` -> `MRO TAM by prime
  contractor` (term alignment + precision); `($M) with cumulative
  share (%)` -> `with cumulative share ($M, %)` (single paren)
- Slide 9: `by prime` -> `by prime contractor`; dropped
  `of $4.9B depot TAM` (redundant with lede); single paren
- Slide 10: semicolon -> ` - ` for auxiliary; parenthetical moved
  to final position
- Slide 11: `under alternative X methods` -> `by X method` (by-
  connector schema)

---

## Overview
- **Breadcrumb**: *(none)*
- **Job**: orient the reader on context + objectives before the
  analysis starts
- **Lede**: (framing slide, no lede)
- **Chart**: none
- **Commentary**: two-column Context + Objectives text on split-color
  canvas (framing exception). Mirrors manager's Matson/Jones Act
  overview template: 5-bullet Context sequencing from "why" to "what
  data" + tight 3-4 bullet Objectives list + preliminary-disclaimer
  box in RHS footer.

  **Context (LHS, dark):**
  1. These materials provide foundational analysis to inform two
     key decisions:
     - The type of defense work to conduct at BuildCo
     - How the Gulf Coast and California candidate sites sit
       relative to the existing USN and USCG MRO footprint
  2. MRO TAM structure shapes BuildCo's go-to-market sequencing,
     yard-certification priorities, and programming-floor work mix
  3. Measures FY2025 contract obligations across 65 MRO-class PSCs
     for the USN and USCG, classified to <N> vessel classes and
     <M> prime contractors across six active RMC regions [fill N
     and M from workbook]
  4. Analysis leverages FPDS contract obligations, Treasury File C
     (via USAspending), FY2026 President's Budget, SAM.gov entity
     registrations, SEC 10-K filings, and federal procurement
     research

  **Objectives of this document (RHS, light):**
  - Size and decompose the FY2025 USN + USCG MRO contracting TAM
    by work segment, vessel category, prime contractor, RMC
    geography, and funding appropriation
  - Reconcile TAM against adjacent Navy and USCG ship-related
    spending categories (newbuild, reactor, public-yard labor)
  - Characterize depot-ship-repair entry architecture (MSRA ->
    MAC-MO -> task order) and MRO prime-contractor landscape
  - Bound contracting-market TAM against period-of-performance-
    apportioned contractor revenue
  - *(Ongoing effort)* Size volume and average contract value for
    priority segments
  - *(Ongoing effort)* Map USG industrial-base funding and path-
    to-access
  - *(Ongoing effort)* Assess competitor archetypes, positioning,
    and capability requirements
  - *(Ongoing effort)* Project BuildCo financial outlook and
    required USG investment
  - *(Ongoing effort)* Deliver scorecard summary and sequenced
    path-to-market

  Preliminary-answers disclaimer box retained in RHS footer

## Agenda
- **Breadcrumb**: *(none -- Agenda IS the wayfinder)*
- **Job**: wayfinding across the deck's four sections
- **Lede**: (framing slide, no lede)
- **Chart**: none
- **Commentary**: 4-section list on full-bleed dark-slate (framing
  exception). Sections:
  1. Commercial Strategy (slides 3-4)
  2. Market Segmentation (slides 5-7)
  3. Competitive Landscape (slides 8-9)
  4. Appendix (slides 10-11)

## TAM Sizing Approach
- **Breadcrumb**: Commercial Strategy / MRO Defense Demand Research Overview
- **Job**: convey the methodology for sizing MRO TAM (FPDS contract
  award data + PSC-code filtering, not budget-exhibit extraction) and
  land the $7.1B number
- **Lede**: Filtering FPDS contract-award data from 2,539 federal
  PSCs down to 65 ship-MRO services codes sizes the FY2025 Navy
  and Coast Guard MRO contracting TAM at $7.1B
- **Chart**: Approach-flow diagram mirroring the manager's TCV
  template (step-column left, flow right, "Included in sizing"
  black-box color key). No chart subtitle - title + lede already
  describe the derivation ("FY2025 Navy and USCG MRO TAM derivation"
  subtitle is dropped).

  **LHS "Approach steps" narrative column** - matches the manager's
  verb-forward construction ("Identify... / Sum... / Multiply by...")
  and turns the diagram into a readable top-to-bottom narrative so
  the reader doesn't have to parse three rows of input / filter /
  output boxes to infer what's happening. Three rows matching the
  three flow rows:
  1. Filter federal PSCs to USN / USCG services-class codes
  2. Filter to ship MRO codes
  3. Apply FY2025 obligations to size the MRO TAM

  **Main-area flow - three rows, differentiated operator convention
  (fixes current HTML's semantically muddled `+ FILTER =` pattern):**
  - **Rows 1 and 2 (filter rows):** three boxes per row -
    `[INPUT] -> [FILTER CRITERION] -> [OUTPUT]` - connected by arrows.
    Drop the `+` and `FILTER` text labels on the operators. Filter
    operations aren't arithmetic; `+` in the current HTML reads as
    addition when the semantics are intersection / narrowing. Arrows
    carry the "flows through" meaning; the middle box IS the filter
    criterion.
  - **Row 3 (arithmetic row):** three boxes per row -
    `[INPUT] x [MULTIPLIER] = [OUTPUT]`. Keep `x` and `=` operators -
    this row IS arithmetic (PSCs x obligations = $). Drop the `APPLY`
    text label - `x` already carries the "multiply" meaning. Row 3
    content: `[65 Ship MRO PSCs] x [FY2025 obligations, FPDS Atom
    Feed, post-FMS carve-out] = [$7.1B FY2025 MRO TAM]` (terminal
    box = navy hero).

  **Operator rhythm across the slide:** arrows (narrowing set) ->
  arrows (narrowing set) -> math (measurement). The visual shift
  from arrows to `x` marks where the methodology transitions from
  PSC-filtering to dollar-measuring - which is the actual
  methodological story the slide tells
- **Commentary**: single PSC definition callout on the RHS (~25-30%
  of slide width) - not a table, just a compact labeled block.
  Structure: small "WHAT IS A PSC?" header + one-sentence body ("A
  4-character Product and Service Code assigned by the contracting
  officer at the buying command to every federal contract action").
  PSC is load-bearing vocabulary across slides 2, 3, 4, 5, and 10,
  so the definition earns its place on this slide. The prior
  `TAM SCOPE DEFINITIONS` 2-row table is dropped in favor of this
  single callout - table scaffolding (super-header, column rules,
  two-column Note / Detail grid) was overbuilt for one definition.
  Awards-data-vs-budget-materials commentary moved to appendix:
  it's methodology defense, and the LHS chart step 3 already flags
  "FY2025 obligations, FPDS Atom Feed, post-FMS carve-out" which
  is load-bearing enough without on-slide prose. In-scope / out-
  of-scope definitions also live in appendix. Nuclear-MRO caveat
  (J044 / K044 / N044 emptiness) removed from this slide -
  reduced to a single footer line: "Nuclear-MRO PSC scope
  addressed on Slide 4"

## Addressable vs Adjacent Spend
- **Breadcrumb**: Commercial Strategy / MRO Defense Demand Research Overview
- **Job**: reconcile the $7.1B out against the $56.6B in total
  FY2025 Navy and Coast Guard ship-related federal spending (top-
  down: show what is adjacent but not in scope)
- **Lede**: Subtracting newbuild (-$38.1B), public-yard labor
  (-$9.5B), and reactor procurement (-$1.9B) from $56.6B in total
  FY2025 Navy and Coast Guard ship-related spending leaves the
  $7.1B MRO contracting TAM
- **Chart**: Waterfall - $56.6B in total FY2025 Navy and USCG
  ship-related spending, less newbuild (-$38.1B), less public-yard
  labor (-$9.5B), less reactor procurement (-$1.9B), equals $7.1B
  MRO contracting TAM (LHS). Chart title: "FY2025 Navy and USCG
  ship-related spending reconciled to MRO contracting TAM ($M)"
- **Commentary**: single RHS text box with three bolded parent
  lines, each followed by 2-3 unbolded bullets. Replaces the
  previous #2 Legend table + #10 Callout card stack -- the scope-
  reconciliation table is deleted entirely (the waterfall chart +
  x-axis labels on the LHS already carry the per-step breakdown,
  so the table was redundant). Content:
  - **PSC 1905 is not purely newbuild**
    - Nuclear-platform depot events (e.g., the $424M HII USS Boise
      SSN-764 Engineered Overhaul at Newport News) are coded as
      shipbuilding rather than J998 / J999
    - The Services MRO TAM therefore undercounts private-sector
      sub and carrier depot work bundled under the newbuild PSC
  - **Public-yard labor is implied, not directly observed**
    - The $9.5B figure derives from OMN 1B4B Ship Maintenance total
      ($11,764M) less Ship Maintenance By Contract CE 928 ($2,228M)
    - The four public naval shipyards (Portsmouth, Norfolk, Puget
      Sound, Pearl Harbor) are NWCF activities; their payroll
      generates no FPDS record
  - **Nuclear MRO PSC emptiness explained**
    - PSCs J044, K044, and N044 sit at approximately $0 in FY2025
    - Reactor maintenance is contracted under ship-level PSC 1905
      and PSC 4470 rather than standalone service PSCs

  This slide remains the sole home for the nuclear-MRO carve-out
  explanation across the whole deck. Slides 3, 5, and 10 previously
  carried duplicate versions of the caveat; those are removed and
  cross-ref this slide instead.

  **Optional appendix strengthening:** replace the "PSC 1905 is
  not purely newbuild" prose with a measured $-amount of FY2025
  PSC 1905 obligations classifiable as nuclear MRO (RCOH / EOH /
  life extension), turning the point from hand-wave to measurement

## TAM Composition
- **Breadcrumb**: Market Segmentation / TAM Composition
- **Job**: decompose the $7.1B by vessel category x work segment to
  show where depot dominates and which hulls drive the spend
- **Lede**: Depot ship repair drove ~68% of FY2025 MRO TAM with ~62%
  of hull spend on surface combatants, amphibious warfare ships, and
  submarines
- **Chart**: Mekko, vessel category x work segment (LHS)
- **Commentary**: one card per work segment (header = segment name +
  $M + %, body = category-definition phrase + specific examples) ->
  **#10 Callout card stack** (RHS). No nuclear-MRO caveat on this
  slide - TAM is already $7.1B by this point (nuclear excluded
  upstream on Slide 4); repeating the caveat here is redundant.

  **Full segment names (restore from workbook - current HTML
  truncated "Sustainment" / "Services" / HM&E full form):**
  Canonical names per `sheets/services.py`
  `SERVICE_CONDENSED_GROUPS` + `sheets/deck_data.py` `SLIDE4_COVERAGE`:
  - `Depot Ship Repair` (unchanged)
  - `Hull, Mechanical & Electrical (HM&E)` (was `HM&E` on HTML -
    restore full form + HM&E parenthetical)
  - `Combat Systems Sustainment` (was `Combat Systems` on HTML -
    restore `Sustainment`)
  - `Port & Technical Services` (was `Port & Technical` on HTML -
    restore `Services`)
  - `Electronics & C4ISR Sustainment` (was `Electronics & C4ISR`
    on HTML - restore `Sustainment`)

  **Card body text template:** `[category-definition phrase]:
  [specific examples]`. Pattern leads with a one-phrase definition
  of what the category IS so reader understands the category, not
  just a list of example items. Workbook nouns preserved (propulsion
  accessories, fire control, husbanding, etc.); only the framing
  changes. Proposed bodies:

  - **Depot Ship Repair ($4,781M, 68%):** Whole-ship availabilities
    (DSRAs, SRAs, CMAVs, DPIAs) executed at private yards under
    RMC-administered MAC-MO IDIQ task orders.
  - **Hull, Mechanical & Electrical (HM&E) ($938M, 13%):** Ship
    mechanical and structural systems: propulsion accessories,
    pumps, valves, piping, HVAC, and diesel engines.
  - **Combat Systems Sustainment ($585M, 8%):** Ship-borne weapons
    and fire control: VLS, guided missiles, launch and arresting
    gear. Includes Trident II sustainment carried by Ohio-class
    SSBNs.
  - **Port & Technical Services ($431M, 6%):** Husbanding (fuel,
    transport, port visits), QC and inspection, OEM technical
    representation, and shipyard operations support.
  - **Electronics & C4ISR Sustainment ($333M, 5%):** Afloat
    electronics: radar, sonar, communications, navigation, alarms,
    and instrumentation.

## Depot Ship Repair Structure
- **Breadcrumb**: Market Segmentation / Depot Structure
- **Job**: unpack the largest segment (J998 + J999 depot) and the
  three-tier MSRA to MAC-MO to task-order entry architecture that
  governs it
- **Lede**: Full-ship availabilities drove 65% of the $4.9B FY2025
  depot segment, awarded under a three-tier MSRA to MAC-MO to task-
  order prime structure
- **Chart**: Mekko, IDV scope x contractor segment (LHS)
- **Commentary**: three expanded step-cards forming the MSRA -> MAC-MO
  -> task order entry pipeline (RHS) -> **#4 Process flow**. Each
  card is educational rather than a one-line label: acronym expanded,
  what actually happens at that stage, who administers, and
  characteristic cadence / scale (e.g., MSRA = NAVSEA yard pre-
  qualification with ~N certified yards; MAC-MO = RMC-level multi-
  award IDIQ pool with typical awardee count + PoP length; FPTO =
  per-availability fixed-price task order with typical duration
  range). Orphan prose block underneath the current numbered list
  dropped; Trade-IDIQ scale note (<3% of depot) moves to footer;
  the ~58% six-CONUS-full-ship-primes concentration stat stays in
  the lede and is the payoff for Slide 9. Source content to draw
  from: docs/research/J998_J999_RESEARCH.md and docs/methodology/

  **Contractor-segment taxonomy rename (affects mekko legend + all
  contractor-axis references deck-wide):** drop the `Tier 1 / 2 /
  3 / 4` jargon prefix, which sounded standardized but isn't (not
  a Navy term; "tier" is already overloaded in DoD contracting for
  OEM / sub / sub-sub supply chains and for capability
  classifications). Use descriptive category names directly in the
  legend:
  - `CONUS full-ship primes` (was Tier 1 - BAE Ship Repair, GD
    NASSCO, HII / Metro Machine / Marine Hydraulics Intl, Vigor
    Marine, Continental Maritime, Detyens)
  - `Regional yards` (was Tier 2 - East Coast R&F, Colonna's,
    Alabama Shipyard, Pacific Shipyards Intl, Bay Ship & Yacht,
    Bayonne Drydock, Tecnico)
  - `Technical services (non-shipyard)` (was Tier 3 - Epsilon
    Systems third-party planner, Amentum, Southcoast Welding,
    MAN Energy Solutions OEM support)
  - `Foreign MSRA yards` (was Tier 4 - Sumitomo, Navantia, Hanwha
    Ocean, UniThai, Cabras Marine, Seatrium, Yokohama Engineering)

  Source taxonomy still tracks J998_J999_RESEARCH.md Section 3,
  just without the numeric-tier wrapper. Note: the "three-tier
  MSRA -> MAC-MO -> task-order entry architecture" phrasing on
  this slide is a different use of "tier" (describing the
  contract-vehicle stack, not contractors) and stays unchanged -
  reader disambiguates via context (the three steps are
  explicitly named)

## Depot Geographic Footprint
- **Breadcrumb**: Market Segmentation / Depot Geography
- **Job**: map depot $ to RMC geography and situate Gulf Coast /
  California candidate sites against the existing RMC footprint
- **Lede**: FY2025 depot spend concentrates on the West Coast (SWRMC
  $1.6B) and East Coast (MARMC $1.0B), with no established RMC anchor
  on the Gulf Coast
- **Chart**: Mekko, RMC region x contractor segment (LHS) - inherits
  the descriptive-name legend introduced on Slide 6 (CONUS full-ship
  primes / Regional yards / Technical services / Foreign MSRA yards);
  no separate Tier 1-4 labels
- **Commentary**: Active RMCs + Candidate Sites as two grouped-bullet
  sections (each RMC = header + geography / primes / homeports sub-
  bullets) -> **#9 Grouped bullet commentary** (RHS)

## Prime Landscape - Total MRO
- **Breadcrumb**: Competitive Landscape / Total MRO
- **Job**: rank primes at the total-MRO level and show segment-by-
  segment #1 / #2 / #3 concentration
- **Lede**: BAE, General Dynamics, and HII collectively captured ~36%
  of the FY2025 MRO TAM, with the top 10 primes at ~57%
- **Chart**: Ranked column chart with concentration callouts (full-
  width top). Base element is a think-cell stacked column chart, 1
  series, sorted descending by FY2025 $M. Two pill / oval callouts
  are layered above the chart as PowerPoint shapes (NOT think-cell
  brackets) -- "Top 3 = 36%" and "Top 10 = 57%" -- each with a
  horizontal connector rule underscoring the span of columns it
  covers. Replaces the Pareto combination chart (cumulative line on
  secondary axis) -- think-cell doesn't carry Pareto as a premade
  element, and the manager's house style uses oval / pill callouts
  above columns (see Screenshots 6.09.09, 6.09.19 in
  `slide_style_gold_standard_examples/`) rather than brackets or
  dual-axis combos
- **Commentary**: work segment x #1 / #2 / #3 prime lookup -> **#3
  Filled matrix** (full-width bottom)

## Prime Landscape - Depot
- **Breadcrumb**: Competitive Landscape / Depot Ship Repair
- **Job**: rank primes within the depot segment only and show their
  RMC coverage (which yards compete where)
- **Lede**: Six CONUS full-ship primes captured ~58% of the $4.9B
  FY2025 depot segment, with the top 10 primes (including foreign
  MSRA yards) at ~70%
- **Chart**: Ranked column chart with concentration callouts (full-
  width top). Base element is a think-cell stacked column chart, 3
  series (CONUS full-ship primes / Regional yards / Foreign MSRA
  yards), each prime's $ populated in only one series so each
  column renders as a single segment-colored block. Sort by total
  descending. Two pill / oval callouts layered above the chart as
  PowerPoint shapes (NOT think-cell brackets) -- "CONUS 6 = 58%"
  and "Top 10 = 70%" -- each with a horizontal connector rule
  underscoring the span of columns it covers. Replaces the Pareto
  combination chart -- segment-color fill carries the second
  dimension (who's CONUS vs. Foreign MSRA) better than a dual-axis
  Pareto could, and the oval callouts match the manager's house
  style (see Screenshots 6.09.09, 6.09.19 in
  `slide_style_gold_standard_examples/`)
- **Commentary**: prime x RMC crosstab -> **#3 Filled matrix** (full-
  width bottom)

## Appropriation Sourcing
- **Breadcrumb**: Appendix / Appropriation Sourcing
- **Job**: break down the $7.4B MRO-PSC $ by federal appropriation
  color (which funding buckets pay for MRO)
- **Lede**: The $7.4B FY2025 MRO-PSC universe spans ~10 federal
  appropriations, with OMN and OPN each at ~35-37% and Defense-Wide
  RDT&E at 11%
- **Chart**: Two 100%-stacked columns side-by-side (LHS)
- **Commentary**: atomic findings, one card per takeaway -> **#10
  Callout card stack** (RHS). No nuclear-MRO caveat on this slide -
  this slide is about appropriation colors (OMN / OPN / SCN / RDT&E
  Defense-Wide), which is an orthogonal cut to PSC scope; the
  nuclear-PSC-emptiness caveat was conflating the two cuts and is
  removed, cross-ref Slide 4 instead

## TAM Framing
- **Breadcrumb**: Appendix / TAM Framing
- **Job**: bound Frame A (contracting-activity obligations) against
  Frame B (POP-apportioned contractor revenue) as a methodology
  sensitivity
- **Lede**: The $7.1B FY2025 contracting-market TAM apportions to a
  ~$3.3B to $3.8B range of FY2025-delivered contractor revenue under
  period-of-performance sensitivity
- **Chart**: Combination chart, columns + horizontal reference line
  (bottom-left)
- **Commentary**: `Obligations x Apportionment = Revenue` equation ->
  **#4 Process flow** (top strip); segment x Frame A / Frame B /
  Apport % lookup -> **#3 Filled matrix** (bottom-right)
