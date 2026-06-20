# Proposed Slide 6 - Depot Ship Repair Deep Dive (MOCKUP - NOT YET DELIVERED)

**Status:** mockup / proposal. Not yet built in the deck. Drills into
the $4.9B depot segment called out on Slide 3 (Depot Ship Repair =
~68% of the $7.1B Services TAM).

**Purpose:** the depot segment is the single largest work type in the
TAM and the one where the commercial entry structure is most specific.
Slide 3 only hints at the "three-tier structure" in a one-line callout.
Slide 6 makes the structure concrete: *who* holds Tier-1 positions,
*where* the depot $ lands geographically, and *what* the depot $ is
actually doing (full-ship availability vs trade IDIQ vs FDNF foreign
yard vs MSC overhaul).

**Related workbook support:** the `Depot Ship Repair` sheet holds the
full J998/J999 deep dive (availability type x hull-program crosstab,
RMC rollup with geography, contractor tier rollup, IDV scope group
crosstab, lead prime per RMC, top task orders, top parent IDVs).
Values are live SUMIFS against the `J998J999Data` Excel Table.
Classifier pipeline: `data_pull/classify_j998_j999.py` +
`classify_j998_j999_idv_scope.py`.

---

## Title

Depot Ship Repair | Six CONUS Tier-1 yards captured ~60% of the $4.9B
FY2025 depot segment; 65% of depot $ is full-ship availabilities
awarded through a three-tier MSRA / MAC-MO prime structure

## Subtitle

FY2025 J998 / J999 ship repair obligations by RMC region and
contractor tier ($M, post-FMS carve-out)

---

## Left visual - vertical stacked bar chart

One bar per RMC region, ranked by FY25 $, stacked by contractor tier.
Total $M above each bar. Tier colors: navy (Tier 1 CONUS Complex),
slate (Tier 2 Regional), medium-blue (Tier 3 Technical Services),
light-blue (Tier 4 FDNF Foreign Yard), gray (Other).

| RMC (Region / Geography)               | Total $M | Tier 1 CONUS Complex | Tier 2 Regional | Tier 3 Technical | Tier 4 FDNF Foreign | Other   |
|----------------------------------------|---------:|---------------------:|----------------:|-----------------:|--------------------:|--------:|
| SWRMC (Pacific / San Diego)            |   ~1,584 |              ~1,140  |           ~310  |           ~110   |                  -  |     ~24 |
| MARMC (Atlantic / Norfolk)             |   ~1,022 |                ~680  |           ~200  |           ~110   |                  -  |     ~32 |
| SERMC (Atlantic / Mayport)             |     ~540 |                ~350  |           ~120  |            ~50   |                  -  |     ~20 |
| NW RMC (Pacific Northwest)             |     ~430 |                ~330  |            ~60  |            ~30   |                  -  |     ~10 |
| FDNF (Yokosuka / Naples / Bahrain)     |     ~510 |                     -|                -|                 -|               ~510  |        -|
| USCG SFLC                              |     ~148 |                 ~95  |            ~35  |            ~15   |                  -  |      ~3 |
| Other (MSC HQ, NAVSEA HQ, CONUS misc)  |     ~688 |                 ~420 |           ~150  |            ~70   |                  -  |     ~48 |

*(Exact figures snap from the Depot Ship Repair sheet RMC x Tier
crosstab at build time. Numbers shown here are approximations drawn
from session work; final slide should pull from the live workbook.)*

## Right visual #1 - Tier-1 CONUS prime roster

| Tier 1 Prime                         | Primary Yards                                          | Primary RMC            | FY25 Depot $M |
|--------------------------------------|--------------------------------------------------------|------------------------|--------------:|
| BAE Ship Repair                      | San Diego, Norfolk, Jacksonville                       | SWRMC + MARMC + SERMC  |       ~1,073  |
| General Dynamics (NASSCO + Cont. Maritime) | San Diego                                        | SWRMC                  |         ~640  |
| HII (Cont. Maritime + Metro Machine + MHI) | San Diego, Norfolk                                 | SWRMC + MARMC          |         ~390  |
| Vigor                                | Portland + Seattle                                     | NW RMC                 |         ~440  |
| Detyens                              | Charleston                                             | SERMC                  |         ~225  |
| NASSCO Mayport + Others              | Mayport + Kings Bay                                    | SERMC                  |         ~100  |
| **Tier 1 CONUS subtotal**            |                                                        |                        |     **~2,868** |

## Right visual #2 - IDV scope composition

| IDV Scope Group                  | FY25 $M | % of Depot $ |
|----------------------------------|--------:|-------------:|
| Full-Ship Availability (CNO Avails / DSRAs / DPIAs / LCS Maint) | 3,258 | 65% |
| MSC Availability (ROH / MTA / SIA / CAT A-B) |   551 | 11% |
| FDNF Foreign MSRA (Hanwha + Navantia + Sumitomo + others) |   513 | 10% |
| Other / Support Services         |   306 |  6% |
| USCG Cutter Maintenance          |   144 |  3% |
| Trade IDIQ (HM&E + Coatings + Insulation + Other Trades) |   123 |  2% |
| Planning & Engineering Support   |   108 |  2% |
| **Depot Ship Repair total**      | **5,003** | **100%** |

## Callout box #1 (light-blue, italic - Three-Tier Structure)

**Entry structure:** MSRA pre-qualification (yard + workforce + safety
credentials) -> MAC-MO IDIQ capture (multi-award contract with a fixed
pool of yards per region) -> fixed-price task orders awarded against
third-party planner specs. Entry requires qualifying at all three
levels *and* the geography (one RMC, one yard footprint). The
three-tier structure drives Tier-1 concentration: six CONUS yards
(BAE, GD, HII, Vigor, Detyens, NASSCO Mayport) hold ~60% of the
$4.9B segment.

## Callout box #2 (light-blue, italic - Scope Composition)

**What the $ is actually doing:** 65% of depot $ is full-ship
availabilities - the CNO Avail / DSRA / DPIA cycle that wraps the
entire hull in a single pass. Trade-specific IDIQs (HM&E, surface
coatings, insulation, pipe lagging) sum to less than 3% of depot $
- the *individual-trade* market is structurally small vs the full-ship
availability market.

## Footnotes

- (1) $4.9B in-scope TAM = $5.0B gross J998 / J999 obligations less
  $85M FMS (Egyptian Navy FOTS, other foreign-military-sales) carve-out.
  Figures on this slide exclude FMS unless otherwise noted.
- (2) Vessel-category mix (Slide 2 reminder): Surface Combatants 34%,
  Amphibious Warfare Ships 28%, Combat Logistics & MSC 19%, Aircraft
  Carriers 6%, USCG Cutters 3%, Submarines 0.2% (the submarine depot
  story is public-yard; see Slide 7).
- (3) Contractor-tier definitions: Tier 1 = CONUS complex full-ship
  MSRA holders (6 primes); Tier 2 = regional yards with narrower
  geography; Tier 3 = technical services (engineering, QA, trade
  specialties); Tier 4 = FDNF foreign yard (Hanwha Ocean, Navantia,
  Sumitomo, UniThai, Mitsubishi, Samsung, Seatrium, others); Other =
  unclassified / small.
- (4) Source: FPDS FY2025 contract obligations on PSCs J998 + J999
  (U.S. Navy + U.S. Coast Guard). Classifier dimensions
  (availability type, availability group, RMC, contractor tier, IDV
  scope group) in `data_pull/classify_j998_j999.py` and
  `data_pull/classify_j998_j999_idv_scope.py`; IDV scope taxonomy
  generated by Claude Opus 4.6. Data as of April 2026.

---

## Why this slide (audience motivation)

Depot Ship Repair is the largest single work type on the TAM (~68% of
Services MRO). A reader who has internalized Slides 1-4 will ask:

- "What does it actually take to win depot work? Why is it so
  concentrated?"
- "Where geographically does the work happen, and does that match my
  portfolio company's footprint?"
- "Is the depot market one thing or several? How much is full-ship
  availability work (where Tier-1 CONUS yards win) vs trade-specific
  IDIQs (where a specialist can enter)?"
- "What's FDNF (the $510M in Japan / Italy / Bahrain)?"

Slide 6 answers all four on one page. The headline findings -- six
CONUS yards hold 60% of the segment through a three-tier structure, and
trade-specific IDIQs are under 3% of $ -- are the two insights that
most shape the commercial entry question for a potential acquirer.

## Build-out assets available in the workbook

The `Depot Ship Repair` sheet provides:

1. TAM headline (J998 East / J999 West split, FMS carve-out, in-scope
   TAM = $4,922M).
2. Availability Group + Availability Type rollups (Drydocked /
   Pierside / CMAV / Emergent / MSC Availability / FDNF Pierside).
3. Vessel Category rollup + Vessel Category x IDV Scope Group
   crosstab (source of Slide 2's vessel mix x work segment intersection
   for the depot segment specifically).
4. RMC rollup with Geography column (source of the Slide 6 left bar
   chart).
5. Contractor Tier rollup + Tier x Availability Group crosstab.
6. Top Contractors within each Tier (Tier-1 primes by FY25 $) -
   source of the Tier-1 prime roster on this slide.
7. IDV Scope Group + IDV Scope Type rollups - source of the scope
   composition table.
8. Lead Prime per RMC (#1 consolidated parent by FY25 $M per RMC).
9. Top 15 Task Orders (PIID-level detail) and Top 15 Parent IDVs
   (MAC-MO / MSRA vehicles).

The `J998 J999 Data` sheet wraps the 2,861 classified awards as an
Excel Table (`J998J999Data`) with 28 columns covering every classifier
dimension. All numeric cells on `Depot Ship Repair` are live SUMIFS /
COUNTIFS against this table.

---

## What does NOT belong on this slide

- Full Services TAM reconciliation (Slide 1 / Slide 3 territory).
- Other work segments (HM&E, Combat Systems, Electronics, Port &
  Technical) - only mentioned as a reminder that this slide is
  depot-only.
- Submarine-specific depot story (public-yard driven; Slide 7 covers).
- Appropriation-color breakdown (Slide 5 covers; note depot is ~70%
  OPN / 27% OMN inside the broader MRO mix).
- Hull-specific rankings (Top 15 Task Orders is a workbook artifact,
  not deck content).

## Status

Draft only. When the actual slide is designed in the deck app and a
screenshot is captured to `deck/`, move the content into `DECK.md` as
the new Slide 6 section (in the same prose-transcription style as
Slides 1-4) and delete this mockup file.
