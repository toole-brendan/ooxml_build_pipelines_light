# Session Log -- PSC-Centered Rebuild (2026-04-15)

Everything done in this session to shift the model from NAICS-centered to
PSC-centered data pulls and rebuild the workbook.

---

## What Changed and Why

The v2.3 model used NAICS codes as the primary discovery filter -- pulling
contracts from vendors classified as shipbuilders (336611) or combat electronics
manufacturers (334511). This missed contracts from vendors in other industries:
propulsion manufacturers (333611), weapons companies (336414), electrical
equipment manufacturers (335xxx), and service contractors not classified as
shipbuilders.

PSC (Product and Service Code) answers "what is being purchased" rather than
"what industry is the vendor in." Centering on PSC captures the full universe
of ship-relevant contracts regardless of vendor NAICS classification.

Result: Navy FY2025 total went from $52.6B (NAICS-only) to $76.2B (NAICS + PSC),
adding ~$23.6B in previously missed contracts including:
- $5.76B in gas turbines (PSC 2840) -- RTX, Rolls-Royce, GE
- $3.83B in guided missiles (PSC 1410) -- Raytheon, Boeing
- $1.88B in nuclear reactors (PSC 4470) -- Fluor Marine Propulsion
- $933M in guided missile components (PSC 1420) -- Lockheed Martin

---

## Scripts Created

### Archived (untouched copies of originals)

| File | Description |
|---|---|
| `data_pull/archive/pull_fpds_v1.py` | Original FPDS pull script with 10 collections |
| `data_pull/archive/dedup_collections_v1.py` | Original dedup with 4 Navy + 4 CG collections |
| `data_pull/archive/classify_awards_v1.py` | Original classifier with spend_type, work_role, SWBS |

### v2 Data Pipeline Scripts

#### `data_pull/pull_fpds_v2.py`

FPDS pull script with 22 collections (10 original + 12 new PSC-based). The pull
pipeline (XML parsing, pagination, checkpointing, FY decomposition, award
aggregation) is unchanged -- only the collection definitions were added.

New Navy PSC collections (6):

| Collection | PSC Codes | Filter |
|---|---|---|
| `navy_vessels` | 14 codes (all 19xx) | + Navy |
| `navy_weapons` | 31 codes (10xx, 12xx, 13xx, 14xx) | + Navy |
| `navy_electronics` | 25 codes (58xx, 59xx) | + Navy |
| `navy_propulsion_electrical` | 40 codes (20xx, 28xx, 29xx, 30xx, 61xx, 63xx, 66xx) | + Navy |
| `navy_aux_components` | 22 codes (41xx-48xx, 53xx) | + Navy |
| `navy_equip_services` | 52 codes (J0xx, K0xx, N0xx, M2xx) | + Navy |

Same 6 collections mirrored for Coast Guard (agency 7008 instead of 1700).

Usage unchanged:
```
python data_pull/pull_fpds_v2.py navy_vessels --fy 2025
python data_pull/pull_fpds_v2.py --list
python data_pull/pull_fpds_v2.py navy_weapons --fy 2025 --dry-run
```

#### `data_pull/dedup_collections_v2.py`

Deduplicates awards across collections. Updated GROUPS dict to include all
new PSC collections alongside the originals:

- `navy` group: 10 collections (4 original + 6 new)
- `cg` group: 10 collections (4 original + 6 new)

Imports `aggregate_awards` from `pull_fpds_v2` instead of `pull_fpds`.

Usage:
```
python data_pull/dedup_collections_v2.py navy --fy 2025
python data_pull/dedup_collections_v2.py cg --fy 2025
```

#### `data_pull/classify_awards_v2.py`

Stripped-down classifier. Removed: spend_type, work_role, SWBS group, SWBS
confidence, and all the PSC-to-SWBS mapping, description regex patterns, and
spend/work-role classification logic.

Kept and improved:
- **Vessel class**: PIID lookup table (~80 manually researched contracts), DAP
  field mapping, description regex (~20 patterns). Unchanged from v1.
- **Hull program** (new): Derived from vessel class. DDG-51 -> DDG, Virginia
  (SSN-774) -> SSN, etc. For multi-class contracts, scans description for hull
  designator mentions -- if all matches point to the same hull program, assigns it.
- **USCG vessel patterns** (new): Added 13 Coast Guard hull programs: OPC
  (Heritage-class), NSC (Legend-class), FRC (Sentinel-class), WMEC, WAGB
  (icebreaker), WLB, WLM, WLIC, WLR, WLI, WTGB, WPB. Patterns match hull
  designators (WMSL, WPC, etc.) and named cutter classes (Bertholf, Waesche,
  Healy, etc.).

Output fields per award: `vessel_class`, `vessel_confidence`, `hull_program`.

Usage:
```
python data_pull/classify_awards_v2.py data_pull/output/fpds/navy_fy2025_deduped.json --fy 2025 --stats
python data_pull/classify_awards_v2.py data_pull/output/fpds/cg_fy2025_deduped.json --fy 2025 --stats
```

### Workbook Sheet Builders

#### `sheets/awards_data.py` (updated)

Loads BOTH `navy_fy2025_deduped_classified.json` and `cg_fy2025_deduped_classified.json`.
Tags each award with `service` = "Navy" or "Coast Guard". 29 columns including
Service, Hull Program, Vessel Class, PSC. Creates Excel Table named "Awards" for
structured references.

Removed columns: Spend Type, Work Role, SWBS Group, SWBS Group Name, SWBS Confidence.

#### `sheets/product_procurement.py` (new, replaces newbuild.py)

PSC x hull program cross-tab for all 132 product-type PSC codes. Two tables:
- U.S. Navy: 132 rows x 24 hull programs + Unclassified + Total
- U.S. Coast Guard: 132 rows x 12 hull programs + Unclassified + Total

Every cell is a SUMIFS formula:
```
=SUMIFS(Awards[FY2025 Obligation], Awards[PSC],"5840", Awards[Hull Program],"DDG", Awards[Service],"Navy")
```

PSC codes organized by family: 19xx vessels, 10xx weapons, 12xx fire control,
13xx ordnance, 14xx missiles, 58xx electronics, 59xx components, 20xx marine
equipment, 28xx engines, 29xx engine accessories, 30xx power transmission,
61xx electrical, 63xx alarm/signal, 66xx navigation, 41xx-48xx auxiliary systems,
53xx hull hardware.

#### `sheets/services.py` (new, replaces mro.py)

Same cross-tab structure for 54 service-type PSC codes: J998/J999 ship repair,
J0xx equipment maintenance, K0xx modification, N0xx installation, M2xx husbanding.

#### `sheets/overview.py` (updated)

Summary of Navy and CG spend by broad PSC group (22 groups). Uses wildcard
SUMIFS (e.g., `Awards[PSC],"58*"`) to aggregate by PSC family. Replaced the
old spend_type/work_role/SWBS waterfall.

#### `sheets/competitive_dynamics.py` (unchanged)

Placeholder stub. Title only.

#### `sheets/module_integration.py` (deleted)

Removed entirely -- no longer part of the workbook.

#### `build_from_data.py` (updated)

Sheet order: Overview, Product Procurement, Services, Competitive Dynamics,
Awards Data, Vessel Taxonomy.

Tab colors centralized here (removed from individual sheet builders):
- Overview: navy blue (#1F314F)
- Product Procurement + Services: green (#2E7D32)
- Competitive Dynamics: dark red (#8B0000)
- Awards Data + Vessel Taxonomy: slate (#5B7A99)

---

## Data Pulled

### Navy PSC Collections (FY2025)

| Collection | Awards | FY2025 $ | Duration |
|---|---|---|---|
| `navy_vessels` | 317 | ~$37.1B | ~10 min |
| `navy_weapons` | 665 | ~$8.5B | ~10 min |
| `navy_electronics` | 3,539 | ~$7.5B | ~20 min |
| `navy_propulsion_electrical` | 3,141 | ~$6.5B | ~15 min |
| `navy_aux_components` | 3,587 | ~$2.3B | ~15 min |
| `navy_equip_services` | 5,371 | $5.0B | ~25 min |

### Coast Guard PSC Collections (FY2025)

| Collection | Awards | FY2025 $ |
|---|---|---|
| `cg_vessels` | 71 | $1.1B |
| `cg_weapons` | 25 | $9.5M |
| `cg_electronics` | 263 | $71.5M |
| `cg_propulsion_electrical` | 1,327 | $171M |
| `cg_aux_components` | 842 | $56.5M |
| `cg_equip_services` | 1,612 | $342M |

### After Dedup + Classify

| Group | Raw Mods | After Dedup | Awards | FY2025 $ |
|---|---|---|---|---|
| Navy | 72,664 | 50,587 | 19,668 | $76.2B |
| Coast Guard | 11,280 | 8,664 | 4,667 | $1.9B |
| **Total** | | | **24,335** | **$78.1B** |

---

## Output Files

### Workbook

`output/08APR2028_Newbuild_and_MRO_Spend_v2.8.xlsx`

| Sheet | Rows | Cols | Content |
|---|---|---|---|
| Overview | 54 | 4 | Navy + CG totals by PSC group |
| Product Procurement | 274 | 28 | 132 PSC codes x hull programs (Navy + CG tables) |
| Services | 118 | 28 | 54 PSC codes x hull programs (Navy + CG tables) |
| Competitive Dynamics | 1 | 6 | Placeholder |
| Awards Data | 24,338 | 29 | 24,335 awards (Navy + CG) with hull program + vessel class |
| Vessel Taxonomy | 180 | 3 | USN/MSC/USCG vessel hierarchy reference |

### Classified JSON

| File | Awards | Size |
|---|---|---|
| `data_pull/output/fpds/navy_fy2025_deduped_classified.json` | 19,668 | 53MB |
| `data_pull/output/fpds/cg_fy2025_deduped_classified.json` | 4,667 | 12MB |

### Raw Mod Cache (for future re-dedup)

All raw mod-level data cached in `data_pull/output/fpds/raw/` -- 20 files
covering all Navy and CG collections. These feed into dedup and can be
re-processed without re-fetching from FPDS.

---

## Pipeline to Rebuild

Full rebuild from cached data (no FPDS calls):
```
python data_pull/dedup_collections_v2.py navy --fy 2025
python data_pull/classify_awards_v2.py data_pull/output/fpds/navy_fy2025_deduped.json --fy 2025
python data_pull/dedup_collections_v2.py cg --fy 2025
python data_pull/classify_awards_v2.py data_pull/output/fpds/cg_fy2025_deduped.json --fy 2025
cd /Users/brendantoole/projects2 && python3 -m domnann.build_from_data
```

To add a new PSC collection:
1. Add entry to COLLECTIONS dict in `data_pull/pull_fpds_v2.py`
2. Add to appropriate GROUPS list in `data_pull/dedup_collections_v2.py`
3. Run `python data_pull/pull_fpds_v2.py <name> --fy 2025`
4. Re-run dedup + classify + build

---

## Next Steps

See `SAM_PLAN.md` for the plan to identify outsourceable work using
USAspending subaward data, the subcontracting plan field, and GFE/GFP.
