---
title: Data sources, pipeline, and limitations
---

# Data sources, pipeline, and limitations

This chapter documents the seven primary-source data feeds used in this article, the pipeline scripts that transform the raw feeds into the analytical CSVs cited throughout, the multi-vintage reconciliation rules, the dollar-bucketing conventions, and the catalogue of known limitations and uncertainty. It is intended both as a methodology reference for readers of the article and as a "how to update" guide for the project repository maintainer.

## The seven primary-source data feeds

| Feed | Source | Article use |
|---|---|---|
| 1. SCN Justification Books (P-5/P-5a/P-5b/P-5c/P-21/P-27/P-40 exhibits) | U.S. Department of the Navy, SECNAV / FMB | Per-ship and per-FY top-line cost; production schedule; cost-category breakdown |
| 2. Federal Procurement Data System (FPDS) Atom Feed | U.S. General Services Administration | Prime-contract obligation flow; PIID discovery; per-mod signed-date attribution |
| 3. FFATA Subaward Reporting System via SAM.gov | U.S. GSA / Treasury | First-tier subaward stream; vendor identification; per-recipient $ flow |
| 4. USAspending.gov subaward API (cross-validation only) | U.S. Treasury | Cross-check against SAM.gov; not the canonical source |
| 5. SAM.gov Entity Management API (NAICS, registration) | U.S. GSA | Vendor NAICS coding; country-of-registration; CAGE codes |
| 6. SEC EDGAR Form 10-K filings (HII + GD + LM + RTX + NG + BAE + GE + L3Harris) | U.S. SEC | Segment-level revenue, operating income, capital expenditure trajectories |
| 7. Public earnings call transcripts (Motley Fool, Insider Monkey, q4cdn.com) | Third-party publishers + corporate IR | Executive commentary; quantitative outsourcing commitments; supplier-base discussion |
| 8. DoD daily contract announcement bulletins (war.gov / globalsecurity.org / Wayback) | DoD Office of the Assistant Secretary of Defense (Public Affairs) | Per-action place-of-performance percentages; the single most direct outsourced-share measurement |

(The eighth feed is the DoD-announcement corpus; for narrative continuity it is sometimes counted with the SCN P-5b "named contractor" reporting as a single primary source.)

## Pipeline scripts

The destroyer-project pipeline is organized as a sequence of Python scripts in `scripts/` that consume one or more primary-source feeds and produce structured CSVs in `extracted/`. The scripts are documented in `MANIFEST.md` and the README; they are adapted from the parallel submarine-project scripts with destroyer-specific filters and buckets.

### FPDS pull and recovery

- **`pull_fpds_ddg_primes.py`** — initial vendor-name and DDG-description sweeps against the FPDS Atom feed. Captures 13 vendor-name slugs (HII-Ingalls, GD-BIW, LM-Aegis, Raytheon, GE-LM2500, Rolls-Royce, BAE-guns/VLS, NG, L3Harris, DRS, GD-Mission, plus 2 description sweeps for DDG-51 / Arleigh Burke / destroyer / Flight III). Date window: FY18 signed-date floor. Output: `fpds_raw/{slug}_raw.json` + `_summary.json`.
- **`pull_fpds_capped_recovery.py`** — the date-bisection recovery pull added on May 24, 2026, for the two slugs that hit the FPDS Atom-feed 300-page pagination cap on the initial pull: `gd_biw_navy` (estimated 7,990 + 31,240 page-equivalents) and `rolls_royce_navy_ddg` (estimated 3,590 + 3,590 page-equivalents). The recovery script uses recursive date-window bisection: if the total-pages estimate for a date window exceeds 300, the window is split in half and each half is queried separately, with a maximum recursion depth of 6 (≤64 leaves per query). The recovered record counts: BIW from 5,692 → **30,236 records** (5.3× improvement); Rolls-Royce from 2,979 → **3,562 records** (modest improvement, as the original cap was less binding). Output: `fpds_raw_v2/{slug}_raw.json` + `_summary.json`.

The date-bisection recovery procedure is a generic FPDS-coverage technique that should be applied whenever a vendor-name FPDS query hits the 300-page cap. The technique is documented in `scripts/pull_fpds_capped_recovery.py` and is reusable across project contexts.

### SAM.gov subaward pull

- **`pull_sam_subawards.py`** — SAM.gov first-tier subaward pull with `--discover` mode that derives seed PIIDs from FPDS pull data. Uses the lowercase `piid` parameter against the `/prod/contract/v1/subcontracts/search` endpoint with the IPv4 socket monkeypatch. Documented in `SAM_GOV_HOWTO.md`. Output: `sam_subawards/{piid}_subawards.json` + `_summary.json`.

The principal SAM.gov methodological details (per `SAM_GOV_HOWTO.md`):

- Production tier API key with 1,000 requests/day cap
- Lowercase `piid` parameter casing (silent zero-result on uppercase)
- `socket.getaddrinfo` IPv4 monkeypatch for macOS (225s → 0.3s per request)
- `subAwardReportId` as the primary dedup key (zero collisions observed)
- Both published and deleted streams captured

### USAspending subaward pull (cross-validation)

- **`pull_usaspending_subawards.py`** — parallel pull of the USAspending `/api/v2/subawards/` endpoint, used for cross-validation against SAM.gov. Same `--discover` mode for seed PIIDs. Output: `usaspending_subawards/{piid}_subawards.json`.

The principal USAspending limitations (chapter 5):

- Per-PIID record cap at approximately 2,500 records (SAM.gov has no cap)
- Aberrant high-dollar artifacts on cooperative-development PIIDs (the Thales NL $4.2B example)
- Slower per-record retrieval than SAM.gov

USAspending is used only as a cross-validation source.

### NAICS enrichment

- **`pull_sam_entity_naics.py`** — SAM Entity Management API pull for top-150 vendors by lifetime in-scope $. Captures primary NAICS, country of registration, CAGE code, and active-registration status. Output: `sam_entity_lookups/{uei}.json` + `extracted/entity_naics_lookup.csv`.

The 35-percent not-found rate on the destroyer top-150 vendor pool is a material coverage gap (chapter 6). Resolution would require either alternative NAICS data sources (Dun & Bradstreet, Manta) or manual fixup; documented as future work.

### DoD-announcement pipeline (added May 24, 2026)

Five scripts produce the DoD-announcement-corpus CSV:

- **`pull_dod_announcements_pop.py`** — 2025+ globalsecurity.org daily-index crawl. Reuses the submarine-project cache directly via symlink (cache symlinked at `research_primary_sources/dod_announcement_pop/cache`). Destroyer-specific keyword filter (`DDG\d+`, `Arleigh Burke`, `Bath Iron Works`, `Ingalls`, `Aegis`, `SPY-6`, `LM2500`, `Mk 41`, `Mk 45`, etc.). Output: appends to `extracted/dod_announcement_pop.csv` and writes per-action audit files to `research_primary_sources/dod_announcement_pop/*.txt`.
- **`fetch_wayback_batch.py`** — 2022-2024 batch fetch via Wayback Machine `curl` (not WebFetch — Wayback Machine WebFetch is session-blocked from this environment). Consumes a `/tmp/wayback_urls_to_fetch.txt` URL list pre-enumerated via the Wayback CDX API. Saves to the Wayback cache `cache_wayback/` symlinked from the submarine project (with 240+ additional Aug-2023 and Jul-Sep-2024 articles added on May 24, 2026 to capture the FY23-27 MYP master + option exercises). 2-second sleep between fetches.
- **`ingest_wayback_bulletins.py`** — parse the cached Wayback HTMLs into the destroyer-specific bucket logic (BIW / Ingalls / Other-US / Foreign). Includes the **single-supplier-no-percentage parser patch** (the `RE_POP_SINGLE` regex) that assigns 100 percent of POP to the matched single city when no explicit percent figure is present in the bulletin paragraph.
- **`classify_dod_action_worktype.py`** — first-pass regex classifier (program × work_type). DDG-specific program tags: `ddg51`, `ddg_gfe_aegis`, `ddg_gfe_radar`, `ddg_gfe_propulsion`, `ddg_gfe_guns`, `ddg_gfe_vls`, `ddg_gfe_combat_systems`, `ddg_gfe_weapons`, `ddg1000`, plus the non-DDG buckets `va`, `col`, `cvn`, `lcs`, `surface_other`.
- **`reclassify_dod_action_subrelevance.py`** — second-pass judgment-based reclassification with hard-drop rules for submarine / carrier / LCS / LCAC / amphib / oiler / Polar Security Cutter / Zumwalt / foreign-MIL / FMS noise. Sets the final `is_ddg_new_construction_tam` gate. The hard-drop rules are conservative — actions that match a destroyer keyword but also match a hard-drop keyword are excluded — so the resulting 152-action TAM-relevant corpus is likely an undercount of true destroyer-attributable activity by 5-10 percent.

The full DoD-announcement pipeline methodology, including the source-selection redaction caveat, is documented in `DOD_ANNOUNCEMENT_HOWTO.md`.

### Aggregation scripts

- **`aggregate_annual_outsourcing.py`** — per-FY × group rollup of FPDS records + per-FY × PIID rollup of USAspending subawards. Produces `extracted/nc_annual_by_vendor.csv` and `extracted/nc_annual_by_piid.csv`.
- **`aggregate_sam_subawards.py`** — verifies subAwardReportId uniqueness; rolls up by `subParentUei`. Produces `extracted/sam_subaward_top_parents.csv`, `extracted/sam_subaward_annual_by_prime.csv`, `extracted/sam_vs_usaspending_per_piid.csv`.
- **`aggregate_new_construction.py`** — applies the in-scope new-construction PIID filter and produces the headline aggregations: `extracted/nc_lifetime_vendors.csv`, `extracted/nc_records_long.csv`, `extracted/nc_scope_summary.json`. The in-scope-PIID list is dynamic — derived from the FPDS-discovery output rather than hard-coded.
- **`extract_scn_destroyer_lines.py`** — parses the SCN Justification Book PDF for Line Item 2122 (DDG-51) main and AP. Produces `extracted/scn_li_resource_summary.csv`, `extracted/scn_li_cost_categories.csv`, `extracted/scn_li_production_schedule.csv`.

## Multi-vintage reconciliation rule

For any historical fiscal year that appears in multiple successive SCN Justification Book vintages, the article uses the **most-recent-vintage-as-actual** rule: the value from the most recent Justification Book that shows that year as a settled actual rather than a forward estimate is used. For example, FY2024 is reported using the FY26 Justification Book value (the first vintage to show FY24 as a settled actual) rather than the FY24 Justification Book's then-forward estimate.

This convention is applied silently throughout the article. The FY27 Justification Book (April 2026) is the primary source for all forward-vintage values: FY25 estimate, FY26 estimate, FY27 base, FY27 OOC, FY28-FY31 outyears, To Complete, and Total.

## Dollar-bucketing conventions

Throughout the article, dollar figures follow these conventions:

- **FPDS prime obligations**: per-modification `obligatedAmount` summed by `signed_date` fiscal year. The cumulative `totalObligatedAmount` field is *not* used as a window measurement.
- **FFATA subaward values**: as reported in SAM.gov FSRS, summed by `action_date` fiscal year. Deduplication is by `subAwardReportId`.
- **DoD announcement values**: as reported in the bulletin paragraph. Source-selection-redacted values appear with empty `amount_usd` in the CSV and are excluded from dollar-weighted aggregations.
- **Currency**: U.S. dollars (USD), then-year (nominal).

## The source-selection redaction caveat

The most consequential methodological caveat in the article is the source-selection-sensitive redaction of the FY23-27 DDG-51 multiyear master award dollar values (chapter 12). Both the BIW master (PIID `N00024-23-C-2305`, war.gov article 3479250, August 1, 2023) and the Ingalls master (PIID `N00024-23-C-2307`, war.gov article 3491276, August 11, 2023) have their obligated dollar values redacted under 41 U.S. Code 2101 et seq. and FAR §§ 2.101 and 3.104.

The trade-press-reported dollar value of the two combined awards is approximately $14.58 billion (BIW $6.40B + Ingalls $8.18B). For dollar-weighted analyses that need the actual values rather than the trade-press estimates, the recommended cross-reference is the FPDS Atom feed (`fpds_raw_v2/gd_biw_navy_raw.json`), which records the per-modification obligated amount.

The redaction structurally biases the chapter 4 headline 87 percent figure upward (away from the yards). The adjusted reading — with trade-press-reported MYP master values folded in — has the outside-yards share at approximately 33-40 percent rather than 87 percent. The chapter 4 figure stands as reported (against the disclosed-only corpus) with the explicit acknowledgment that adjusting for the redaction shifts the headline materially.

## Known limitations

A consolidated catalogue of the limitations that affect this article:

### Time-window limitations

- **DoD-announcement corpus coverage is July 2022 - May 2026 only.** Pre-2022 Wayback Machine snapshot density is too thin to enumerate systematically. The September 2018 FY18-22 multiyear master awards (DDGs 122-134) are NOT in the corpus, so multi-year trend analysis at high precision is not possible.
- **SCN Justification Book data is bounded by the FY27 vintage (April 2026).** FY28 and forward values are forward estimates that will revise in subsequent Justification Book vintages.
- **FFATA reporting lag is 12-30 months.** First-tier subaward filings against the FY23-27 multiyear master and the FY24 single-year buy are still accumulating; the cumulative FFATA-visible flow against recent prime obligations is undercounted by an estimated 2-3× for the most recent reporting years.

### Coverage gaps

- **NAICS lookup has a 35-percent not-found rate** on the top-150 vendor pool ($2.28B of unclassified dollar value across 53 vendors). Resolution requires either alternative NAICS data sources or manual fixup.
- **The IVECO MARCORSYSCOM contamination** on PIID `M67854-16-C-0006` (~$707M of subaward value attributable to Marine Corps amphib-warship Mk 110 gun production, not destroyer work) is flagged but not yet filtered out at the upstream FPDS discovery layer.
- **EDGAR 10-K pull has not yet been executed** as an automated script. Segment financial figures in chapter 15 are sourced from the auto-mined `extracted/exec_quotes_outsourcing.md` and direct read of selected 10-K filings; a full automated EDGAR pipeline parallel to the submarine project's would tighten the financial-segment data quality.
- **GE-LM2500 single-supplier-no-percentage parser caveat** remains partially un-fixed: approximately $50M of LM2500 value across 5-8 rows is unattributed in the POP analysis (chapter 11).

### Definitional caveats

- **DDG-1000 / Zumwalt-class is excluded** from the headline TAM by design (closed program; OPN-funded modernization). The underlying dataset retains `ddg1000` and `ddg_repair` tags for completeness.
- **WPN/OPN-funded ordnance procurement is excluded** (CIWS, Standard Missile, ESSM, Tomahawk) — these are loaded onto destroyers but funded under different appropriations. The cumulative WPN/OPN flow against destroyers is comparable in magnitude to the SCN-funded GFE flow.
- **Federal naval shipyard depot work is not counted as outsourced** — Norfolk, Portsmouth, Pearl Harbor, Puget Sound work is federal payroll.
- **Private ship-repair work at BAE San Diego et al. is not in the new-construction scope** — those facilities perform destroyer sustainment under different prime contracts.

### Estimation uncertainty

- **The chapter 9 yard-side outsourcing estimate of ~$1.8B/yr carries a 1.4-2.2B/yr confidence band**, driven principally by uncertainty in (a) the BIW share of GD Marine Systems revenue (range 18-25 percent), (b) the DDG share of HII Ingalls revenue (range 46-70 percent), and (c) the yard-side supplier content as a share of revenue (range 35-50 percent).
- **The chapter 13 distributed-shipbuilding hours figures** are sourced from HII's earnings-call disclosures; they are point-in-time statements that may be revised in subsequent quarters.
- **The chapter 4 ~87 percent outside-yards POP share is conservative** (the MYP-redaction caveat biases it upward). Adjusting for the trade-press-reported MYP master values shifts the figure to approximately 33-40 percent.

## How to refresh the data

To re-run the destroyer-project pipeline against the latest available data:

```bash
cd /Users/brendantoole/projects2/destroyer_outsourced_work

# 1. Re-extract from the SCN PDF (cheap, <1 second)
python3 scripts/extract_scn_destroyer_lines.py

# 2. Re-pull FPDS (slow, ~20-30 minutes; long for capped slugs)
python3 scripts/pull_fpds_ddg_primes.py
python3 scripts/pull_fpds_capped_recovery.py  # for capped slugs

# 3. Re-pull subawards
python3 scripts/pull_usaspending_subawards.py --discover
python3 scripts/pull_sam_subawards.py  # uses _discovered_piids.json

# 4. NAICS enrichment (requires aggregate first)
python3 scripts/aggregate_new_construction.py
python3 scripts/pull_sam_entity_naics.py

# 5. Aggregate
python3 scripts/aggregate_annual_outsourcing.py
python3 scripts/aggregate_sam_subawards.py

# 6. Re-run DoD-announcement pipeline
python3 scripts/pull_dod_announcements_pop.py
python3 scripts/fetch_wayback_batch.py
python3 scripts/ingest_wayback_bulletins.py
python3 scripts/classify_dod_action_worktype.py
python3 scripts/reclassify_dod_action_subrelevance.py

# 7. Re-build the wiki
cd wiki_ddg
python3 build_wiki_html.py
```

## Where to extend this work

Five directions in which the destroyer-project analysis could be productively extended:

1. **EDGAR 10-K automated pipeline** — port the submarine-project EDGAR pull script (`pull_hii_10k_research.py`) to the destroyer project to automate the segment-financial data capture from the principal company filings. The full FY24-FY25 segment-financial picture for HII Ingalls, GD Marine Systems, LM RMS, RTX Raytheon, NG Mission Systems, BAE Land & Armaments, and GE Aerospace would tighten chapter 15.
2. **NAICS coverage refresh** — resolve the 53 not-found UEIs in the top-150 vendor pool via Dun & Bradstreet or alternative NAICS data sources. Currently $2.28B of unclassified dollar value.
3. **GE-LM2500 parser patch** — complete the single-supplier-no-percentage parser logic to capture the remaining ~$50M of unattributed LM2500 value across 5-8 paragraphs.
4. **IVECO contamination cleanup** — drop PIID `M67854-16-C-0006` from the in-scope set at the FPDS discovery layer.
5. **FY18-22 multiyear master capture** — execute a targeted Wayback Machine pull for the September 2018 DoD-announcement bulletins to capture the FY18-22 multiyear master awards. This would provide a multi-year baseline against which to measure trajectory in the chapter 4 corpus. Currently the corpus has no pre-2022 visibility.

None of these is in the active pipeline. They are documented here as the natural next-steps for a project maintainer.
