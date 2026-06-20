# Manifest — destroyer_outsourced_work

Status: **Initial gathering pass complete.** FPDS + SAM.gov subaward + SAM Entity
NAICS pulls all completed 2026-05-23. USAspending pulls intentionally skipped per
user direction (SAM.gov is the upstream FFATA source with no per-prime cap).

Last updated: 2026-05-23 21:30.

## Quick stats

| Source | Files | Records | $ |
|---|---:|---:|---:|
| FPDS Atom Feed | 13 raw + summary | 21,131 unique mod records | — |
| SAM.gov subawards (89 PIIDs) | 89 + summary | **24,559 published**, 0 collisions | **$15.50B raw** |
| SAM Entity NAICS lookups | 150 cached + 1 CSV | 97 ok / 53 not_found | — |
| In-scope new construction | 1 CSV per dim | **22,235 records** | **$13.84B lifetime** |
| Extracted CSVs (SCN) | 3 | 20 + 15 + 30 rows | — |

**Key finding:** SAM.gov subaward API on macOS required forcing IPv4 via
`socket.getaddrinfo` monkeypatch — Python urllib hangs ~225s per request on IPv6
SYN retransmit, while curl is fine (RFC 8305 Happy Eyeballs). Documented in
`SAM_GOV_HOWTO.md`. Without the fix, the 89-PIID SAM pull would have taken ~20+
hours; with it, ~3 minutes.

---

## What's in this folder

### Top-level

- `README.md` — project goal, prime cast list, definitions, plan
- `SAM_GOV_HOWTO.md` — copy of the submarine project's SAM.gov guide (source-agnostic)
- `MANIFEST.md` — this file
- `.env` — same SAM API key as the submarine project
- `scripts/` — Python pull + parse scripts (adapted from `submarine_outsourced_work/scripts`)
- `logs/` — per-session markdown logs (one file per work session)
- `pull_logs/` — background-process stdout (`.log` files from FPDS, SAM, USAspending, NAICS, transcript scrapers)

### Symlinks (shared sources with submarine project)

- `budget_books/` → `submarine_outsourced_work/budget_books/`
  - Same SCN justification books (FY22–FY27), same 30-year shipbuilding plan
- `reference_prior_analysis/` → `submarine_outsourced_work/reference_prior_analysis/`
  - Same FPDS / USAspending / SAM.gov reference docs + lessons-learned

### `scripts/` — DDG-specific adaptations

| Script | Source | Notes |
|---|---|---|
| `pull_fpds_ddg_primes.py` | submarine `pull_fpds_sub_primes.py` | 12 vendor + description queries: HII-Ingalls, GD-BIW, LM-Aegis, Raytheon-SPY-6/missiles, GE-LM2500, Rolls-Royce, BAE-guns/VLS, NG, L3Harris, DRS, GD-MissionSys + DDG-51/Arleigh Burke/destroyer/Flight III description sweeps. Date window: FY18 signed-date floor (catches FY18-22 + FY23-27 MYP masters). |
| `extract_scn_destroyer_lines.py` | submarine `extract_scn_submarine_lines.py` | Parses **LI 2122 only** (DDG-51 main + AP). DDG-1000 (LI 2119) is explicitly out of scope per 2026-05-23 user direction. **Verified working** on FY27 SCN book — produced 20 resource-summary + 15 cost-category + 30 production-schedule rows. |
| `pull_usaspending_subawards.py` | submarine equivalent | **Empty seed list** — uses `--discover` mode to derive seed PIIDs from FPDS pulls. Vendor groups: HII-Ingalls, GD-BIW, LM-Aegis, Raytheon, GE-Propulsion, BAE-Guns/VLS, L3Harris, NG, DRS. |
| `pull_sam_subawards.py` | submarine equivalent | Reads seed PIIDs from `usaspending_subawards/_discovered_piids.json`. Same SAM.gov gotchas honored (lowercase `piid`, `/prod/` URL, etc — see SAM_GOV_HOWTO.md). |
| `pull_sam_entity_naics.py` | submarine equivalent | Identical methodology — reads top-150 vendors from `nc_lifetime_vendors.csv`. |
| `aggregate_annual_outsourcing.py` | submarine equivalent | DDG vendor patterns instead of sub patterns. Per-FY × group rollup of FPDS records + per-FY × PIID rollup of USAspending subawards. |
| `aggregate_sam_subawards.py` | submarine equivalent | Identical methodology. Verifies subAwardReportId uniqueness; rolls up by subParentUei. |
| `aggregate_new_construction.py` | submarine equivalent | **Dynamic in-scope PIID list** — reads from `usaspending_subawards/_discovered_piids.json` instead of hardcoding (no prior DDG analysis to seed from). `MIB_EXCLUDED_UEIS` starts empty — populate as DDG-specific industrial-base pass-throughs are identified. |
| `pull_dod_announcements_pop.py` | submarine equivalent (2026-05-24) | 2025+ globalsecurity.org daily-index crawl. Destroyer filter (DDG/Arleigh Burke/BIW/Ingalls/Aegis/SPY-6/LM2500/Mk 41/Mk 45). BIW/Ingalls/Other-US/Foreign bucket logic. Reuses submarine cache via symlink. |
| `fetch_wayback_batch.py` | submarine equivalent (2026-05-24) | 2022-2024 Wayback batch fetch. Used for Aug-2023 DDG MYP backfill. |
| `ingest_wayback_bulletins.py` | submarine equivalent (2026-05-24) | Parses cached Wayback HTMLs → CSV. Includes the single-supplier-no-% patch (assigns 100% to single matched site). |
| `classify_dod_action_worktype.py` | submarine equivalent (2026-05-24) | First-pass program × work_type classifier. DDG-specific program tags (ddg51, ddg_gfe_aegis, ddg_gfe_radar, ddg_gfe_propulsion, ddg_gfe_guns, ddg_gfe_vls, ddg_gfe_combat_systems, ddg_gfe_weapons, ddg1000, etc.). |
| `reclassify_dod_action_subrelevance.py` | submarine equivalent (2026-05-24) | Second-pass hard-drop + promote pass. Drops submarine / carrier / LCS / LCAC / amphib / oiler / Polar Security Cutter / Zumwalt / foreign-MIL noise. Final `is_ddg_new_construction_tam` gate. |

### `extracted/` — Parsed structured tables (DDG-51 only)

Generated by `extract_scn_destroyer_lines.py`.

| File | Source | Description |
|---|---|---|
| `scn_li_resource_summary.csv` | SCN P-40 | Resource Summary rows for LI 2122 main + AP × FY columns (Prior Years / FY25 / FY26 / FY27 Base / FY27 OOC / FY27 Total / FY28-31 / To Complete / Total). 20 rows. |
| `scn_li_cost_categories.csv` | SCN P-5c | Cost category breakdown per ship hull per FY (Plan Costs, Basic Construction, Change Orders, Electronics, HM&E, Ordnance, Other, Total Ship Estimate). 15 rows. |
| `scn_li_production_schedule.csv` | SCN P-27 | Ship × shipbuilder × FY × award/start/delivery dates. **30 hulls** DDG 127–DDG 156 mapped to Bath Iron Works or Huntington Ingalls Industries. |
| `dod_announcement_pop.csv` | DoD daily contract bulletins (war.gov / globalsecurity.org / Wayback) | 776 rows × 21 columns. Per-action POP percentages bucketed BIW / Ingalls / Other-US / Foreign. Final filter `is_ddg_new_construction_tam == 'yes'` → 152 supplier-TAM-relevant DDG actions / $7.13B / **87% outside the two yards**. See `DOD_ANNOUNCEMENT_HOWTO.md` for methodology + source-selection redaction caveat. |
| `dod_action_pop_by_worktype.csv` | derived | Per (program_refined × work_type_primary) bucket rollup with $-weighted POP shares. |

### `fpds_raw/` — Raw FPDS Atom Feed pulls

Will be populated by `pull_fpds_ddg_primes.py`. Each `<slug>_raw.json` has format:
```json
{
  "label": "...", "notes": "...", "queries": [...],
  "date_window": "SIGNED_DATE:[2017/10/01,2026/12/31]",
  "record_count": N,
  "records": [ /* per-mod records, NOT deduped to latest mod */ ]
}
```

12 slugs: `hii_ingalls_navy`, `gd_biw_navy`, `lm_aegis_navy`, `raytheon_navy_ddg`,
`ge_lm2500_navy`, `rolls_royce_navy_ddg`, `bae_navy_ddg`, `ng_navy_ddg`,
`l3harris_navy_ddg`, `drs_navy_ddg`, `gd_mission_navy_ddg`, plus 2 description
sweeps (`desc_ddg51_class`, `desc_destroyer_navy_big`, `desc_flight_iii_navy`).

### `usaspending_subawards/` — First-tier subaward pulls (USAspending)

Will be populated by `pull_usaspending_subawards.py --discover`. Format same as
submarine project.

### `sam_subawards/` — First-tier subaward pulls (SAM.gov)

Will be populated by `pull_sam_subawards.py`. Format same as submarine project.

### `sam_entity_lookups/`, `edgar_research/`, `hii_earnings_transcripts/`, `gd_earnings_transcripts/`

Created as empty dirs for the optional follow-on pulls:
- `pull_sam_entity_naics.py` populates `sam_entity_lookups/`
- HII + GD 10-K and earnings transcript scrapers are **NOT yet ported** from the
  submarine project (`pull_hii_10k_research.py`, `scrape_hii_transcripts.py`).
  Port if/when needed — the destroyer project differs from the sub project in
  that BOTH yards (HII-Ingalls + GD-BIW) are visible primes in FPDS, so the
  10-K-based "invisible team-build partner" workaround is less critical.

---

## How to re-run

```bash
cd /Users/brendantoole/projects2/destroyer_outsourced_work

# 1. Re-extract from the SCN PDF (cheap, <1 second)
python3 scripts/extract_scn_destroyer_lines.py

# 2. Re-pull FPDS (slow, ~20-30 minutes due to pagination + politeness delays)
python3 scripts/pull_fpds_ddg_primes.py

# To re-run only one query:
python3 scripts/pull_fpds_ddg_primes.py gd_biw_navy

# 3. Re-pull USAspending subawards (medium, ~5-10 minutes)
python3 scripts/pull_usaspending_subawards.py --discover

# 4. Re-pull SAM.gov subawards (slow on big PIIDs)
python3 scripts/pull_sam_subawards.py

# 5. Aggregate
python3 scripts/aggregate_annual_outsourcing.py
python3 scripts/aggregate_sam_subawards.py
python3 scripts/aggregate_new_construction.py

# 6. NAICS enrichment (after aggregate_new_construction.py produces nc_lifetime_vendors.csv)
python3 scripts/pull_sam_entity_naics.py
```

---

## Key DDG-51 differences from the submarine project

1. **Two visible prime yards.** HII-Ingalls (Pascagoula, MS) AND GD-BIW (Bath, ME).
   Both appear as prime of record on individual DDG-51 ships in FPDS. There is
   NO submarine-style team-build invisibility — what's in FPDS is what's there.

2. **No pre-seeded PIID list.** Submarines had 17 PIIDs from prior analysis;
   destroyers start from zero. The `--discover` mode in
   `pull_usaspending_subawards.py` derives candidate PIIDs from the FPDS pulls.

3. **Different GFE primes.** Instead of Bechtel Plant Machinery (naval reactor)
   + Lockheed Martin Trident (SSBN missile), the DDG GFE primes are:
   - Lockheed Martin (Aegis Combat System + Mk 41 VLS)
   - Raytheon/RTX (AN/SPY-6 AMDR + SM-2/3/6/ESSM/Tomahawk + Phalanx CIWS)
   - GE Aerospace (LM2500 gas turbines, 4 per ship)
   - BAE Systems (Mk 45 5-inch gun)

4. **Different SCN line item.** LI 2122 (DDG-51) vs LI 1045/2013 (Columbia/Virginia).
   Different P-1 line numbers (#13/#14 instead of #1/#2/#6/#7). All under
   1611N / BA 02 / BSA 1 (Other Warships).

5. **MIB/mandatory funding is newer for DDG.** $5.4B mandatory funding shows in
   FY26 SCN estimate and $314M in FY27 request — explicitly tagged for "U.S surface
   maritime industrial base productivity in various areas including supplier
   development, shipyard infrastructure, strategic sourcing, workforce development,
   technology opportunities, and wages." Equivalent to submarine MIB but newer +
   different scope.

6. **DDG-1000 is out of scope** per user direction (2026-05-23). Only 3 ships,
   essentially complete, remaining flows are OPN not SCN.
