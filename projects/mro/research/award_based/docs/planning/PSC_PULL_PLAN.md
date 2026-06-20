# Plan: PSC-Centered Data Pulls and Workbook Rebuild

## Context

The current model uses NAICS codes (vendor industry) as the primary discovery filter, supplemented by PSC-based pulls for ship repair (J998/J999) and combat vessels (1901/04/05). This misses contracts from vendors NOT classified under NAICS 336611 (shipbuilding) or 334511 (combat electronics) -- for example, propulsion manufacturers (NAICS 333611), weapons companies (NAICS 336414), or electrical equipment manufacturers (NAICS 335312).

PSC (Product and Service Code) answers "what is being purchased" rather than "what industry is the vendor in." Centering on PSC captures the full universe of ship-relevant contracts regardless of vendor classification.

The goal: pull all Navy and CG contracts by ship-relevant PSC codes, dedup, classify, and rebuild the workbook with PSC-based spending views for FY2025.

---

## Step 0: Archive Existing Scripts, Create v2 Copies

Archive the current pull/dedup/classify scripts untouched, then create v2 versions for editing.

### Archive (copy originals, no modifications)
```
data_pull/archive/pull_fpds_v1.py      <-- copy of data_pull/pull_fpds.py
data_pull/archive/dedup_collections_v1.py  <-- copy of data_pull/dedup_collections.py
data_pull/archive/classify_awards_v1.py    <-- copy of data_pull/classify_awards.py
```

### Create v2 working copies
```
data_pull/pull_fpds_v2.py          <-- edited with new PSC-based collections
data_pull/dedup_collections_v2.py  <-- edited with updated GROUPS
data_pull/classify_awards_v2.py    <-- edited if needed for CG support
```

The v2 scripts import from the same underlying modules (`usa_client.py`, etc.) and extract the same ~63 fields per award. Only the collection definitions and dedup groups change.

---

## What We Already Have (Keep in dedup pool)

Existing pulls remain -- their raw mod data sits in `data_pull/output/fpds/raw/` and feeds into dedup alongside the new PSC pulls:

| Collection | Filter | Awards | FY2025 $ |
|---|---|---|---|
| `shipbuilding` | NAICS 336611 + Navy | 3,239 | $35.5B |
| `combat_electronics` | NAICS 334511 + Navy | 1,299 | $10.5B |
| `ship_repair` | PSC J998/J999 + DoD | 2,545 | $4.9B |
| `combat_vessels` | PSC 1901/04/05 + DoD | 191 | $37.1B |
| CG equivalents | Various | ~1,700 | ~$2.4B |

---

## Phase 1: Define New PSC-Based Collections (in pull_fpds_v2.py)

### Identifying Gaps

From the PSC April 2024 reference (2,539 active codes), ship-relevant PSC groups NOT fully captured by NAICS-based pulls:
- Weapons/missiles from non-334511 vendors (NAICS 336414 guided missile mfg)
- Propulsion components from non-336611 vendors (NAICS 333611/333618 engine mfg)
- Electrical plant equipment from NAICS 335xxx vendors
- J0xx/K0xx/N0xx services from non-shipbuilder contractors
- Auxiliary system components from industrial suppliers

### New Collections (6 Navy + 6 CG = 12 total)

#### 1. `navy_vessels` -- All vessel products (newbuild core)
```
PSC: 1901, 1904, 1905, 1910, 1915, 1920, 1925, 1930, 1935, 1940, 1945, 1950, 1955, 1990
Filter: + Navy (CONTRACTING_AGENCY_ID:"1700")
```
Supersedes `combat_vessels` (which only had 3 codes + DoD-wide). Adds codes for cargo/tanker vessels, special service vessels, small craft, barges, drydocks.

#### 2. `navy_weapons` -- Weapons, fire control, ordnance, missiles
```
PSC: 1005, 1010, 1015, 1025, 1035, 1040, 1045, 1055, 1075, 1095,
     1210, 1230, 1240, 1260, 1265, 1270, 1285, 1287, 1290,
     1350, 1352, 1355, 1367, 1377, 1386,
     1410, 1420, 1425, 1427, 1430, 1440
Filter: + Navy
```
~30 PSC codes. Captures weapons/fire control from ALL vendors.

#### 3. `navy_electronics` -- Radar, sonar, EW, comms, antennas
```
PSC: 5805, 5810, 5811, 5815, 5820, 5821, 5825, 5826, 5830, 5835, 5836,
     5840, 5841, 5845, 5850, 5855, 5860, 5865, 5895,
     5963, 5965, 5985, 5996, 5998, 5999
Filter: + Navy
```
~25 PSC codes. Includes airborne variants -- vessel class assignment separates ship from aircraft downstream.

#### 4. `navy_propulsion_electrical` -- Engines, propulsion, electrical, navigation
```
PSC: 2010, 2020, 2030, 2040, 2050, 2090,
     2815, 2820, 2825, 2830, 2840, 2845, 2895,
     2910, 2920, 2930, 2940, 2950, 2990,
     3010, 3040,
     6080, 6105, 6110, 6115, 6120, 6125, 6130, 6140, 6145, 6150,
     6320, 6350,
     6605, 6610, 6615, 6650, 6660, 6665, 6685
Filter: + Navy
```
~38 PSC codes. Marine equipment + engines + electrical plant + navigation + alarm systems.

#### 5. `navy_aux_components` -- Pumps, valves, piping, HVAC, hull fittings
```
PSC: 4130, 4140, 4210, 4220, 4235, 4240,
     4310, 4320, 4330,
     4420, 4470,
     4540, 4610, 4620, 4630,
     4710, 4720, 4730,
     4810, 4820,
     5340, 5342
Filter: + Navy
```
~22 PSC codes. Auxiliary systems + outfit/furnishing components + hull hardware.

#### 6. `navy_equip_services` -- Equipment maint, modification, installation, husbanding
```
PSC: J012, J013, J016, J019, J020, J028, J029, J030, J035, J036, J039,
     J041, J043, J047, J048, J049, J052, J056, J058, J059, J061, J063,
     J066, J069, J091, J099,
     K010, K012, K016, K019, K020, K034, K058, K059, K099,
     N010, N012, N016, N019, N020, N025, N056,
     M2AA, M2AB, M2AC, M2AD, M2AE, M2AF, M2BA, M2BB, M2BZ, M2CA
Filter: + Navy
```
~51 PSC codes. All equipment-level MRO, modernization, installation, and husbanding.

#### CG equivalents (same PSC sets, CONTRACTING_AGENCY_ID:"7008")
`cg_vessels`, `cg_weapons`, `cg_electronics`, `cg_propulsion_electrical`, `cg_aux_components`, `cg_equip_services`

---

## Phase 2: Pull Data

### Sequence
```
python data_pull/pull_fpds_v2.py navy_vessels --fy 2025
python data_pull/pull_fpds_v2.py navy_weapons --fy 2025
python data_pull/pull_fpds_v2.py navy_electronics --fy 2025
python data_pull/pull_fpds_v2.py navy_propulsion_electrical --fy 2025
python data_pull/pull_fpds_v2.py navy_aux_components --fy 2025
python data_pull/pull_fpds_v2.py navy_equip_services --fy 2025
# Then CG equivalents
```

Each pull: ~10-25 min. Total: ~2-5 hours. Use `--dry-run` first to preview volume.

All ~63 fields per award are extracted identically to current pulls (same `parse_entry()` and `aggregate_awards()` functions).

---

## Phase 3: Dedup and Classify

### Update dedup_collections_v2.py

```python
GROUPS = {
    "navy": {
        "collections": [
            # Existing (backup coverage from NAICS-based pulls)
            "shipbuilding", "combat_electronics", "ship_repair", "combat_vessels",
            # New PSC-based
            "navy_vessels", "navy_weapons", "navy_electronics",
            "navy_propulsion_electrical", "navy_aux_components", "navy_equip_services",
        ],
    },
    "cg": {
        "collections": [
            # Existing
            "cg_shipbuilding", "cg_ship_repair", "cg_combat_electronics", "cg_combat_vessels",
            # New PSC-based
            "cg_vessels", "cg_weapons", "cg_electronics",
            "cg_propulsion_electrical", "cg_aux_components", "cg_equip_services",
        ],
    },
}
```

### Run
```
python data_pull/dedup_collections_v2.py navy --fy 2025
python data_pull/classify_awards_v2.py data_pull/output/fpds/navy_fy2025_deduped.json --stats --fy 2025
python data_pull/dedup_collections_v2.py cg --fy 2025
python data_pull/classify_awards_v2.py data_pull/output/fpds/cg_fy2025_deduped.json --stats --fy 2025
```

---

## Phase 4: Update Workbook

### Awards Data changes (`sheets/awards_data.py`)
- Load BOTH `navy_fy2025_deduped_classified.json` AND `cg_fy2025_deduped_classified.json`
- Add `Service` column (Navy / Coast Guard) to distinguish

### New sheet: "Navy by PSC" (`sheets/navy_by_psc.py`)
- Rows: each PSC code with significant FY2025 Navy obligation
- Columns: PSC Code, PSC Description, FY2025 Obligation, # Awards, Module $, Integration $, Top Vessel Class
- Grouped by PSC family (19xx, 58xx, 12xx, J9xx, etc.)
- Subtotals by group
- SUMIFS referencing Awards Data table

### New sheet: "CG by PSC" (`sheets/cg_by_psc.py`)
- Same structure as Navy, filtered to Coast Guard

### Existing sheets
- **Output**: update for combined Navy + CG, or add CG section
- **Newbuild/MRO**: keep vessel class views, working as before
- **Module & Integration**: populate (currently stub) with PSC-based module/integration view

### Build script (`build_from_data.py`)
- Add new sheets to build sequence
- `config.py`: bump to v2.4

---

## Phase 5: Verification

1. Compare new Navy total against current $52.6B -- expect equal or higher (new PSC pulls add contracts from non-NAICS vendors)
2. Check dedup stats -- `source_collections` field shows which queries found each award
3. Spot-check known contracts (Electric Boat SSN, HII DDG, Raytheon SPY-6)
4. Verify CG totals (~$1.5-2.5B range)
5. Open workbook, verify SUMIFS resolve

---

## Key Files

| File | Action |
|---|---|
| `data_pull/pull_fpds.py` | Archive to `data_pull/archive/pull_fpds_v1.py` |
| `data_pull/dedup_collections.py` | Archive to `data_pull/archive/dedup_collections_v1.py` |
| `data_pull/classify_awards.py` | Archive to `data_pull/archive/classify_awards_v1.py` |
| `data_pull/pull_fpds_v2.py` | New -- v2 with PSC-based collections |
| `data_pull/dedup_collections_v2.py` | New -- v2 with updated GROUPS |
| `data_pull/classify_awards_v2.py` | New -- v2 (may be identical, edit if needed for CG) |
| `sheets/awards_data.py` | Edit -- load Navy + CG, add Service column |
| `sheets/navy_by_psc.py` | New -- Navy PSC spending view |
| `sheets/cg_by_psc.py` | New -- CG PSC spending view |
| `build_from_data.py` | Edit -- add new sheets |
| `config.py` | Edit -- bump version |
