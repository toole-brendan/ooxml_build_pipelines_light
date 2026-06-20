# Data Sheet: Awards (unified)

The workbook has one master data sheet, **Awards**, that feeds both Product Procurement and Services via SUMIFS with a PSC filter.

## Structure

- **Granularity**: per-hull row. For services PIIDs (PSC in `MRO_PSCS`), one row per (PIID, detected hull). Same PIID can appear 1-4 times if mods touch multiple hulls. For newbuild PIIDs (PSC in `NEWBUILD_PSCS`) and any other non-services PSCs, 1 row per PIID (newbuild is 1:1 with hull - no explosion needed).
- **Scope**: all PSCs (newbuild + services).
- **Source**: `data_pull/output/fpds/{navy,cg}_awards_master.json`
- **Built by**: `sheets/awards.py`
- **Excel Table name**: `Awards`

## Pipeline

```
deduped.json
    |
    v
classify_awards_v2.py  ->  classify_awards.py  ->  *_deduped_classified.json  (per-PIID)
    |   Baseline vessel classification for every PIID: vessel_class,
    |   hull_program, vessel_supergroup from PSC / DAP / award-description
    |   cascade.
    |
    v
vessel_explode_v2.py  (unified, handles all PSCs)
    |   Services PSCs  -> per-mod tier cascade:
    |       Tier -1  residual overrides (LLM + FPDS MOD 0)
    |       Tier 0   proper-name lookup: mod -> IDV -> award
    |       Tier 0b  hull-number lookup: mod -> IDV -> award
    |       Tier 0c  DAP field
    |       Tier 1   VESSEL_DESC_PATTERNS regex: mod -> IDV
    |       Tier 2   supergroup regex: mod -> IDV
    |       Tier 5   recipient supergroup prior
    |       else     residual (passes through classify_awards classification)
    |   Newbuild PSCs  -> 1 row per PIID, classification inherited from
    |                     classify_awards (newbuild is 1:1 hull)
    |
    v
*_awards_master.json
    |
    v
sheets/awards.py  ->  "Awards" sheet / `Awards` Excel table
    |
    v
Product Procurement (SUMIFS + PSC in NEWBUILD_PSCS)
Services          (SUMIFS + PSC in MRO_PSCS)
```

## Columns (40)

Identity: `service`, `piid`, `recipient_name`, `ultimate_parent_name`, `corporate_parent`

Amounts: `fy2025_obligation`, `fy2025_actions`, `base_and_all_options`, `total_obligation`

Classification: `hull_program`, `vessel_class`, `vessel_supergroup`, `vessel_confidence`, `hull_source`

Match metadata: `matched_proper_name`, `matched_hull_number`, `hulls_detected`, `n_hulls_detected`, `proper_names_detected`, `is_residual`

Parent IDV: `parent_idv_piid`, `parent_idv_description`

Award attributes: `psc_code`, `psc_description`, `product_or_service_type`, `naics_code`, `gfe_gfp`, `dod_acquisition_program_description`, `type_of_contract_pricing`, `extent_competed`, `number_of_offers`

Vendor / location: `cage_code`, `pop_state`, `pop_zip`, `contracting_office`

Descriptive: `description`, `source_collections`, `start_date`, `end_date`, `subcontracting_plan`

## Shore/base exclusion

`awards.load_rows` applies `is_shore_base_excluded` to services rows only (PSC in MRO_PSCS). Newbuild rows pass through untouched. Excluded services markers include ATFP, NAVFAC facilities, JCREW, SEAPORT-NXG, inactive vessels, FMS, and the LLM-flagged `llm_exclusions.json` set.

## TAM reconciliation

- `SUM(Awards[FY2025 Obligation])` where `PSC` in `MRO_PSCS` = Navy + CG Services TAM
- `SUM(Awards[FY2025 Obligation])` where `PSC` in `NEWBUILD_PSCS` = Navy + CG Product Procurement TAM
- Per-PIID for services: sum of exploded rows = deduped FY25 obligation (enforced by `_normalize_to_deduped` in `vessel_explode_v2.py`)
- Per-PIID for newbuild: single row FY25 obligation = deduped FY25 obligation (trivially)

## Why this is one table, not two

Prior versions maintained two separate tabs (Awards Data, per-PIID; Awards By Hull, per-(PIID,hull)) fed by two parallel pipelines. That meant services PIIDs appeared in both sheets, sometimes with different classifications (the per-PIID pipeline read only award-level text, while the per-mod pipeline used a richer cascade across mod/IDV/award descriptions).

The unified Awards table is produced by one classification path (`vessel_explode_v2.py`) so every row - services or newbuild - is consistent. Product Procurement and Services are each a PSC-filtered view of the same table. Newbuild explosion is trivial (1 row per PIID) since those PSCs are 1:1 with hulls.
