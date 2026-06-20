# Session 2026-04-18 (pt 2): Depot Ship Repair Slide 5 - Data Prep - v2.67 -> v2.69

## Context

Continuation of the same-day Depot Ship Repair session that landed v2.67
(`SESSION_2026-04-18_depot_ship_repair.md`). With the J998/J999 sheet in
place, the next ask was a Slide 5 to sit alongside the existing 4-slide
Services / MRO deck. User asked two questions: (1) what should be on the
slide, using Slides 1-4 as models, and (2) what data structures, if any,
are missing from the workbook to support it.

Ended at **v2.69** with six additive changes to `sheets/depot_ship_repair.py`
+ `sheets/vessel_taxonomy.py`, plus an IDV-scope fallback that pulled the
"unclassified" share of the vessel-category rollup from 31% down to 9%.

---

## Slide 5 concept (proposed, not yet drawn)

Drafted by reading `deck/DECK.md` and the existing Depot Ship Repair sheet
side by side. Deck style rules: action-statement title
(`Topic | assertion`), left chart / right table, navy-to-light-blue palette,
light-blue italic callout, FPDS footer. Managers prefer vertical bars.

**Working title:** `Depot Ship Repair | Surface combatants, amphibs, and
MSC auxiliaries drove ~80% of the $4.8B FY2025 depot segment; full-ship
availabilities captured ~65% of spend`

**Left visual - vertical stacked bar chart**, one column per vessel
category matched to Slide 2's columns for deck coherence. $M total above
each bar. Stack segments: Full-Ship Avail / MSC Avail / FDNF MSRA /
Trade IDIQ / Support & Planning / Other.

**Right visual - RMC table** (Region | Geography | FY25 $M | Lead Prime).

**Callout (light-blue, italic):** Three-tier structure - MSRA pre-qual ->
MAC-MO IDIQ -> fixed-price TOs. Five CONUS yards (BAE San Diego + Norfolk,
GD NASSCO, HII Continental Maritime / Metro Machine, Vigor) hold top-tier
MSRA positions for complex full-ship avails.

## Vessel classification - answered feasibility

Every J998/J999 award already carries `hull_program` via
`vessel_explode_v2.py`'s tier cascade. The missing piece was the rollup
from hull program (DDG, LPD, T-AO, WMSL, ...) to deck-facing vessel
category (Surface Combatants, Amphibs, Combat Logistics & MSC, ...).
`sheets/vessel_taxonomy.py` already defines the canonical hierarchy, so
the mapping lives there.

---

## Work completed, in order

### 1. Slide concept + data-gap list

Proposed the slide above; enumerated the six additive changes needed:

1. Vessel category mapping in `vessel_taxonomy.py`
2. Vessel Category rollup section on the Depot sheet
3. Vessel Category x IDV Scope Group crosstab (primary Slide 5 source)
4. RMC geography column
5. Lead-Prime-per-RMC mini-section
6. Bump `top_per_tier` from 3 to 5 in `_write_tier_top_vendors`

User approved. Built all six.

### 2. First round of additions (v2.67 -> v2.68)

**`sheets/vessel_taxonomy.py`**
- `VESSEL_CATEGORY_ORDER` (7 buckets + Other / Unclassified).
- `HULL_TO_CATEGORY` dict - 73 hull designators across Surface Combatants,
  Amphibious Warfare Ships, Aircraft Carriers, Combat Logistics & MSC
  (incl. all MSC `T-` prefixed variants), Submarines, USCG Cutters, Mine
  Warfare.
- `vessel_category_for(hull_program)` helper, defaults to
  'Other / Unclassified' for unknown hulls.

**`sheets/depot_ship_repair.py`**
- Imports from `vessel_taxonomy`.
- Preprocessing step on load: tags every award with `vessel_category` so
  the generic `_sum_m` / `_count` / `_crosstab_m` helpers can filter on
  it without change.
- `RMC_GEOGRAPHY` dict - 16 RMCs mapped to region labels
  (`'SWRMC' -> 'Pacific / San Diego'`, `'MARMC' -> 'Atlantic / Norfolk'`,
  and so on through FDNF + USCG + Army).
- New `_write_rmc_rollup` writer adds a Geography column between the RMC
  name and the FY25 $M column.
- New `_write_lead_prime_per_rmc` section - for each RMC, the #1
  consolidated parent by FY25 $M and that parent's share of the RMC
  total.
- `_write_tier_top_vendors`: default `top_per_tier` bumped `3 -> 5`.
- **Vessel Category rollup** inserted after the existing Availability
  Group x Hull Program crosstab.
- **Vessel Category x IDV Scope Group crosstab** inserted in the
  IDV-taxonomy-conditional block, labeled "Slide 5 source".

Docstring on `create_depot_ship_repair` updated to reflect the new 13-
section layout.

Built v2.68. Depot sheet reported 2,861 awards / $5,008M.

### 3. Post-build diagnostic: 31% unclassified

Quick spot-check showed a problem:

| Vessel Category | FY25 $M | % |
|---|---:|---:|
| Other / Unclassified | 1,541 | 30.8% |
| Surface Combatants | 1,441 | 28.8% |
| Amphibious Warfare Ships | 1,043 | 20.8% |
| Combat Logistics & MSC | 651 | 13.0% |
| Aircraft Carriers | 203 | 4.1% |
| USCG Cutters | 96 | 1.9% |
| Mine Warfare | 25 | 0.5% |
| Submarines | 9 | 0.2% |

Unclassified being the #1 category is deck-toxic. Dug in: of the $1,541M
unclassified, $1,514M came from awards with empty `hull_program` - 886
prime awards against multi-hull IDIQs where the upstream puller didn't
set a hull. Only $27M was from legitimately missing mappings (LCAC $13M,
MWT $13M).

### 4. IDV-scope fallback (v2.68 -> v2.69)

The IDV scope group on those 886 awards often implies a vessel category
directly:

| IDV Scope Type (no-hull) | FY25 $M | Implied Category |
|---|---:|---|
| CNO Avails - Surface Combatants | 200 | Surface Combatants |
| MSC / FDNF Foreign Yard MSRA | 179 | Combat Logistics & MSC |
| MSC General Ship Repair | 138 | Combat Logistics & MSC |
| USCG Cutter Maintenance | 53 | USCG Cutters |
| LCS Maintenance Vehicles | (part) | Surface Combatants |
| CVN Private Sector Maintenance | (part) | Aircraft Carriers |
| CNO Avails - Amphibious Ships | (part) | Amphibious Warfare Ships |

Added an `IDV_SCOPE_TO_CATEGORY` fallback dict. When `hull_program` is
empty, look up the award's `idv_scope_type` in that dict. Multi-hull
trade IDIQs, barge / planning / Army Watercraft / production support
IDVs stay unmapped by design (they span hull classes or aren't hull
work at all).

Also added LCAC, LCU, SSC -> Amphibious Warfare Ships in the base
`HULL_TO_CATEGORY` mapping.

Rebuilt v2.69:

| Vessel Category | FY25 $M | % | Awards |
|---|---:|---:|---:|
| Surface Combatants | 1,687 | 33.7% | 821 |
| Amphibious Warfare Ships | 1,417 | 28.3% | 602 |
| Combat Logistics & MSC | 968 | 19.3% | 452 |
| Aircraft Carriers | 304 | 6.1% | 86 |
| USCG Cutters | 148 | 3.0% | 260 |
| Mine Warfare | 25 | 0.5% | 153 |
| Submarines | 9 | 0.2% | 28 |
| Other / Unclassified | 450 | 9.0% | 459 |

Unclassified $1,541M -> $450M. The residual $450M is genuine non-hull
work (trade IDIQs, barges, planning & engineering, Army watercraft,
production support) that shouldn't be attributed to a specific vessel
class.

**Slide 5 headline now writes itself:** Surface Combatants + Amphibs +
MSC auxiliaries = **$4.07B / 81%** of the FY25 depot segment.
Surface Combatants + Amphibs alone = **$3.1B / 62%**.

---

## Files modified

- `sheets/vessel_taxonomy.py` - added `VESSEL_CATEGORY_ORDER`,
  `HULL_TO_CATEGORY` (73 hulls, later 76 after LCAC/LCU/SSC),
  `vessel_category_for()`.
- `sheets/depot_ship_repair.py` - vessel_taxonomy imports, vessel
  category preprocessing with IDV-scope fallback,
  `IDV_SCOPE_TO_CATEGORY` constant, `RMC_GEOGRAPHY` constant, new
  `_write_rmc_rollup`, new `_write_lead_prime_per_rmc`, `top_per_tier`
  default 3 -> 5, two new sections wired into `create_depot_ship_repair`
  (Vessel Category rollup + Vessel Category x IDV Scope Group crosstab),
  updated docstring.

## Files created

None. All additions were edits to existing modules.

## Memories added

None.

---

## Workbook progression

| Version | Change | Impact |
|---|---|---|
| v2.67 -> v2.68 | Six additive data structures (vessel category, RMC geography, lead prime per RMC, top-5 per tier, Vessel Category x IDV Scope crosstab) | Depot sheet grew from 13 -> 15 section blocks; numbers unchanged for existing sections |
| v2.68 -> v2.69 | IDV-scope fallback for empty hull_program; LCAC/LCU/SSC mappings | Unclassified share of vessel-category rollup: 30.8% -> 9.0%. Surface Combatants + Amphibs now 62% of depot |

v2.69 is current.

---

## Open flags

- **Services formula-length bug fix** (carried over from pt 1 of this
  session) is still staged but unverified. Both v2.68 and v2.69 built
  clean, but Excel may still flag a "Removed Records: Formula from
  sheet3.xml" warning on open if any long-name contractor triggers the
  pre-existing path. Worth opening v2.69 in Excel to confirm.

- **Unclassified residual ($450M / 9%)** is deck-acceptable but not
  ideal. Two reductions available if wanted:
  - Route "Barge & Small Craft Support" ($94M) to its own "Support
    Craft" bucket or to Combat Logistics & MSC.
  - Decide whether Army Watercraft ($124M, W9127N prefix) should be
    excluded from the depot TAM entirely (matches the same flag raised
    in pt 1 of this session).

- **Slide 5 itself is not yet drawn** - this session only built the
  data structures. Drawing the slide in the deck app is the next step,
  plus capturing a screenshot to `deck/` and adding the transcription
  to `deck/DECK.md` in the same style as Slides 1-4.
