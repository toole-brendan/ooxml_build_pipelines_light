# Vessel Classification -- Gaps and Future Improvements

Current vessel classification covers 52.5% of FY2025 Navy dollars ($27.6B of $52.6B).
The remaining 47.5% ($25.0B) across 3,199 awards is unclassified. This doc describes
the main gaps and approaches to close them.

---

## What's Working

Two-layer approach:
1. **DAP field** (DoD Acquisition Program): 175 awards, $25.6B. When populated with a
   real program code (DDG 51, SSN 774, CVN 78, etc.), maps cleanly to vessel class with
   high confidence. Covers the biggest contracts.
2. **Description regex**: ~1,576 awards, $4.0B. Catches hull designators (DDG-51, CVN-72),
   ship names (USS KIDD, USNS JOHN LEWIS), and class names (Arleigh Burke, Virginia-class)
   in the contract description field.

---

## What's Missing and Why

### 1. Large integration contracts with generic descriptions ($15B+)

The biggest gap. Examples:

| PIID | Recipient | FY2025 | Description |
|---|---|---|---|
| N0002417C2117 | Electric Boat | $5.9B | "FUNDING" |
| N0002424C2114 | Bechtel Plant Machinery | $843M | "DE-SCOPE COMPONENTS" |
| N0002424C2106 | HII | $701M | "UPDATE ATTACHMENT K AND L" |
| N0002419C2210 | Bollinger | $614M | "DEOBLIGATE AND OBLIGATE FUNDING" |
| N0002424C2124 | Electric Boat | $528M | "INC FUNDING" |

These are clearly identifiable by PIID + recipient, but the description is a funding/admin
mod that doesn't name the program. The latest mod's description overwrites earlier more
descriptive text during aggregation.

**Fix: PIID lookup table.** Build a manual mapping of known PIIDs to vessel classes for
the top ~50-100 contracts by value. These are stable, long-lived contracts -- a PIID like
N0002417C2117 will always be Columbia-class (Electric Boat). This would recover $15B+ in
a few hours of manual research.

Sources for PIID -> vessel mapping:
- USAspending award detail page (search by PIID, description often has program name)
- FPDS base award (mod 0) description -- often more descriptive than later mods
- Defense news / contract award announcements (search PIID)
- The `dod_acquisition_program` code (currently "000" for these) may be populated on
  older mods even when the latest mod has "000"

Implementation: add a `PIID_TO_VESSEL` dict in `classify_awards.py`, checked before
DAP and description regex. Highest confidence since it's manually verified.

### 2. Combat system contracts that serve multiple vessel classes ($3-5B)

Examples:
- SPY-6 radar (Raytheon, $850M) -- goes on DDG-51 Flight III, FFG-62, and potentially
  DDG(X). Description says "DDG FLT III" but the production line serves multiple classes.
- Aegis fire control (Lockheed Martin, $362M) -- serves DDG-51, CG-47, and international.
- SEWIP EW suite -- installed across multiple surface combatant classes.
- MK 48 torpedo -- cross-platform weapon.

**Fix: multi-class tagging.** Instead of forcing a single vessel_class, allow a list. Tag
these as the primary platform where known (SPY-6 -> DDG-51 primary) with a `vessel_note`
field indicating multi-class applicability. Or tag as "multi-class: surface combatant" to
at least narrow the scope.

### 3. Ship repair availabilities under multi-ship IDIQs ($2-3B)

Many J998/J999 repair contracts are delivery orders under IDIQs that cover multiple ships.
The base IDIQ might be "ship repair services, Pacific Fleet" with individual delivery orders
for specific ships. Our aggregation rolls delivery orders up to the PIID level, losing the
per-ship granularity.

**Fix: transaction-level classification.** The raw mod data (in `output/fpds/raw/`) has
per-mod descriptions. Instead of using only the latest mod's description (which may be an
admin change), scan ALL mod descriptions for the same PIID and take the most specific vessel
match found. This would catch cases where mod 0 says "USS KIDD DDG-100 FY25 DSRA" but mod
P00005 (the latest) says "CODE 440A GROWTH WORK".

Implementation: modify `classify_awards.py` to optionally load raw mods and build a
PIID -> best_description lookup by scanning all descriptions per PIID for vessel patterns.

### 4. Small MRO contracts with no vessel in description ($1-2B)

Hundreds of small contracts (<$1M) for parts, labor, and services with descriptions like
"SHIP REPAIR", "EXECUTION COST", or just a funding modification reference. These may never
be classifiable without pulling the full mod history or the referenced IDV (parent contract).

**Fix: IDV inheritance.** Many of these are delivery orders under an IDV. The IDV itself
may have a vessel-specific scope. USAspending's `parent_award_piid` field (available via
`--enrich`) links the delivery order to its parent IDV. If the IDV is vessel-specific, all
its delivery orders inherit that classification.

Implementation: run `--enrich` to get `parent_award_piid`, then build a lookup from IDV
PIID -> vessel class (using the same regex patterns on the IDV's description).

---

## Priority Order

| Approach | Effort | Recovery | Notes |
|---|---|---|---|
| PIID lookup table (top 50-100) | 2-4 hours manual | ~$15B | Highest ROI, do first |
| Transaction-level description scan | 1-2 hours code | ~$2-3B | Use existing raw mod cache |
| IDV inheritance via --enrich | 2-3 hours code + API | ~$1-2B | Depends on parent_award_piid |
| Multi-class tagging | 1 hour code | ~$3-5B (reclassified) | More nuanced, not more coverage |

Combined, these could push vessel classification from 52% to 80-85% of dollars.

---

## Known PIID -> Vessel Mappings (Starter List)

These are the largest unclassified contracts. Fill in vessel class manually:

```
N0002417C2117  Electric Boat         $5.9B   -> Columbia (SSBN-826)?
N0002424C2114  Bechtel Plant Mach    $843M   -> (nuclear propulsion components)
N0002424C2106  HII                   $701M   -> ?
N0002419C2210  Bollinger             $614M   -> Towing/Salvage/Rescue?
N0002425C4135  Northstar Maritime    $534M   -> (ship dismantling)
N0002424C2124  Electric Boat         $528M   -> Columbia or Virginia?
N0002425C5434  Kongsberg             $435M   -> NSM (multi-class)
N0002418C4314  HII                   $424M   -> SSN-764 (Virginia refit?)
N0002421C2106  HII                   $388M   -> CVN-74 RCOH
N0002424C2135  BlueForge Alliance    $366M   -> (submarine supply chain)
```

To research: search each PIID on USAspending.gov or FPDS.gov for the base award description.
