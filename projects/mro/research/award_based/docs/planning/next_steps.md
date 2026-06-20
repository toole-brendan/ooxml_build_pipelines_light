# Next Steps

Prioritized by impact on the model's usefulness, not by effort.

---

## High Priority

### 1. Pull FY2022-2024 to show market trends

The model currently shows a single FY2025 snapshot. Adding FY2022-2024 gives four years
of trend data -- enough to show whether the market is growing, which vessel programs are
ramping or winding down, and how the module/integration mix is shifting.

**Effort:** Low. Same `pull_fpds.py` script, just run per FY. Dedup and classification
scripts work on any FY. ~30-60 min of pull time per FY per collection.

**Impact:** High. Trend data is far more useful to a decision-maker than a single-year
snapshot. A company evaluating market entry needs to see trajectory, not just current state.

### 2. Subcontract SAM (Dimension 3)

The current SAM ($10.7B module work) only captures contracts where the Navy buys subsystems
directly. It misses the subcontracted portion of integration contracts -- when Electric Boat
builds a submarine, they subcontract 40-60% of contract value to module suppliers. That
subcontracted spend is part of the module supplier's real addressable market.

Two steps:
1. Run `--enrich` on the deduped set to add subaward counts and total subaward amounts
   from USAspending (~1 API call per award, ~2-3 hours runtime)
2. Pull full subaward detail for the top 50-100 integration contracts by value to see
   who the subs are and what they were paid

**Effort:** Medium. Enrichment is automated. Subaward detail analysis is manual.

**Impact:** High. Could double the SAM estimate by revealing the subcontracted module
market within integration contracts. Also identifies which primes are the largest sources
of subcontracting opportunity.

### 3. Re-pull FY2026 via FPDS

The existing FY2026 data was pulled via the old USAspending pipeline and lacks GFE/GFP,
ultimate parent company, and CAGE codes. Re-pulling via `pull_fpds.py` gets the full field
set. FY2026 is a partial year (Oct 2025 - Apr 2026 as of today) but still useful for
showing current-year run rate.

**Effort:** Low. Single script run.

**Impact:** Medium. Completes the FY range and enables current-year tracking.

---

## Medium Priority

### 4. Coast Guard integration

CG FY2025 data is pulled and sitting in `data_pull/output/fpds/` for all four CG
collections ($1.28B shipbuilding, $142M ship repair, $54M combat electronics, $931M combat
vessels). Needs dedup, classification, and inclusion in the workbook.

CG is ~5% of the combined Navy+CG market. The DHS-wide pulls confirmed that non-CG DHS
ship work is negligible (<$1M), so the CG-specific pulls are sufficient.

**Effort:** Low. Run `dedup_collections.py cg --fy 2025`, then `classify_awards.py`.
Update Awards Data sheet to load both Navy and CG classified JSONs.

**Impact:** Medium. Completes the scope defined in the objective. Small dollar impact but
important for completeness -- some companies target CG specifically.

### 5. Improve vessel classification coverage

Currently 85.7% of dollars are classified by vessel. The remaining 14.3% ($7.5B) is mostly
small MRO contracts with generic descriptions. Three approaches documented in
`vessel_classification_gaps.md`:

- **Transaction-level description scan** -- scan all mod descriptions per PIID (not just
  the latest) to find vessel references in earlier, more descriptive modifications. Uses
  existing cached raw mod data. Would recover ~$2-3B.
- **IDV inheritance** -- link delivery orders to their parent IDV via USAspending's
  `parent_award_piid` field (requires `--enrich`). If the parent IDV is vessel-specific,
  all delivery orders inherit that classification. Would recover ~$1-2B.
- **Expand PIID lookup table** -- manually research the next 50-100 largest unclassified
  PIIDs. Diminishing returns but straightforward.

**Effort:** Medium (code changes + enrichment API calls).

**Impact:** Medium. Pushes vessel coverage from 85% toward 95%.

### 6. Build Module & Integration and Competitive Dynamics sheets

Two placeholder sheets in the workbook that need implementation:

- **Module & Integration** -- cross-cutting view showing the module/integration split by
  vessel class and SWBS group simultaneously (the 2D matrix). Shows which vessel programs
  have the most module opportunity and in which system areas.
- **Competitive Dynamics** -- contractor landscape analysis. Top primes by vessel class,
  top module suppliers by SWBS group, competition status (sole-source vs competed),
  contract pricing types (FFP vs cost-plus). All the fields are already in Awards Data.

**Effort:** Medium. Same SUMIFS pattern as Newbuild and MRO sheets.

**Impact:** Medium. These are the "so what" sheets -- they answer who competes where and
what the competitive structure looks like.

---

## Lower Priority

### 7. Phase 2 NAICS codes

The current collections cover the core market (shipbuilding, combat electronics, ship
repair, combat vessels). Phase 2 adds system-specific manufacturing NAICS codes:

| NAICS | Description | What it adds |
|---|---|---|
| 333611 | Turbine and Power Transmission Equipment | Propulsion OEMs (GE, Rolls-Royce) |
| 336414 | Guided Missile and Space Vehicle Manufacturing | Weapons primes (Raytheon, Lockheed) |
| 334419 | Other Electronic Component Manufacturing | Electronics sub-tier |
| 335311 | Power/Distribution/Specialty Transformer Mfg | Electrical plant components |

These would expand the module SAM by capturing contracts coded to manufacturing NAICS
rather than the broader 336611/334511. Some overlap with existing collections is expected.

**Effort:** Low per collection (same script). Medium overall due to number of collections.

**Impact:** Low-medium. Most high-value contracts in these areas are already captured via
combat_electronics (334511) or combat_vessels (PSC 1901/1904/1905). Phase 2 adds the
long tail.

### 8. Multi-year workbook with trend sheets

Once FY2022-2025 data is pulled and classified, build trend-oriented sheets:
- Spending by vessel class over time (ramp-up/ramp-down curves)
- Module SAM trend by SWBS group
- Contractor market share shifts
- New entrants and exits

**Effort:** High. Requires multi-FY data in the Awards table and more complex formulas
or pivot-style layouts.

**Impact:** High for the final deliverable, but depends on completing the FY2022-2024
pulls first.

### 9. Budget data validation layer

Reintroduce Navy budget exhibits as a top-down validation of the bottom-up awards data.
Not as a primary data source, but as a reasonableness check: does the awards-based TAM
for DDG-51 newbuild roughly match the SCN budget line for DDG-51? Large discrepancies
would flag classification errors or missing contracts.

**Effort:** Medium. Budget data was extracted in v1.x and is available in `sources/`.

**Impact:** Low for market sizing, high for credibility. Being able to say "the bottom-up
awards data reconciles to within X% of the top-down budget" strengthens the model's
authority.
