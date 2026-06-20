# Slide 15 — Contract Vehicles & Qualifications (module: `contract_vehicles.py`)

> Breadcrumb: GTM › Contract Vehicles · five-vehicle table + qualification paths · `_chart_xml/slide15_table.xml` + `slide15.xml`

## On-slide claims (verbatim)

- **Takeaway:** "MSRA and MAC-MO carry **~84% of Navy depot MRO**, with Coast Guard cutter
  repair on a separate USCG track."
- **Five-vehicle table:**
  - **MSRA (Master Ship Repair Agreement)** — DFARS master agreement (not a contract). CNRMC
    application per location: ship-repair identity, on-site survey, DCMA financial capability
    review. Tier 1/2/3 by workload capacity (22,000 or 1,040 man-days). POP ~123-day notional
    (up to ~1 yr actual); 5-yr recert; DCMA annual reviews. Awardees: ~11 private CONUS yards;
    Tier-1 primes (**BAE, GD NASSCO, HII, Vigor, Detyens**) anchor depot $ share.
  - **MAC-MO (Multiple-Award Contract, Maintenance & Overhaul)** — Navy ship-maintenance
    strategy, not a standing qualification. Pre-qualified contractors compete per home port
    (SWRMC, MARMC, SERMC). ~5-yr period; FFP delivery orders per availability. Awardees:
    MSRA-holders who win each home-port pool.
  - **SeaPort-NxG** — Navy professional support services IDIQ; Rolling Admissions (N00178-24-R-
    7000). Engineering/PM/technical, **not depot repair**. 5-yr POP.
  - **FedMall / GSA** — small-purchase & professional services; FedMall is DLA's catalog portal;
    GSA MAS / OASIS+. Outside the depot MRO pipeline. FedMall <$250K; GSA MAS 5-yr options.
  - **USCG / SFLC** — Coast Guard procurement via SAM; separate gate (NAICS 336611). Drydock
    work requires **Std Spec 8634** facility certification + qualified Dockmaster.
- **Footnotes:** (1) "**~84% of FY2025 Navy depot obligations ($4.1B of $4.9B)** awarded to
  MSRA-holders under MAC-MO regional pools, priced as FFP delivery orders. Remaining ~16%: Trade
  IDIQ carve-outs, FDNF pierside (foreign MSRAs), SeaPort-NxG overflow, direct-award small
  services." (2) "Coast Guard cutter MRO runs on a separate USCG/SFLC track; drydock work
  requires Std Spec 8634." Source: FPDS FY2025 obligations; DFARS 217.71 (Master Agreements);
  GAO MAC-MO references; CNRMC MSRA instruction (2025); USCG Std Spec 8634.

## Claim-by-claim sourcing

| Claim | Source |
|---|---|
| MSRA / MAC-MO structure, tiers, recert | **DFARS 217.71** (Master Agreements); **CNRMC MSRA instruction (2025)** (deck source line) |
| RMC home-port pools (SWRMC/MARMC/SERMC) | workbook `sources_references.py` **CITE-02** (NAVSEA RMC structure) |
| ~84% = $4.1B of $4.9B Navy depot | FPDS FY2025 obligations; depot universe in `model_depot_ship_repair.py` (J998/J999) |
| Tier-1 prime awardees (BAE, GD NASSCO, HII, Vigor, Detyens) | `model_depot_ship_repair.py` §10–12 top-contractor / market-share blocks |
| USCG / SFLC + Std Spec 8634 | **USCG Std Spec 8634**; SRC-09 USCG; NAICS 336611 |
| SeaPort-NxG N00178-24-R-7000 | current Navy IDIQ solicitation (deck) |

- The depot universe the 84% is measured against is the J998/J999 contract base
  (`model_depot_ship_repair.py`; SRC-02 `extracted/j998_j999.csv`, 2,862 task orders). Tier-1
  prime shares come from the top-10 contractor block (§10) and per-segment market share (§12).

## Reserve facts (could be added)

- **MSRA mechanics worth having on hand:** it's a **DFARS master agreement, not a contract** —
  qualification is per-location via CNRMC (ship-repair identity, on-site survey, DCMA financial
  capability review), tiered 1/2/3 by workload capacity (**22,000 vs 1,040 man-days**), ~123-day
  notional POP, **5-year recertification** with DCMA annual reviews. ~**11 private CONUS yards**
  hold one.
- **The ~16% non-MAC-MO remainder** is the entry-edge map: Trade IDIQ carve-outs, **FDNF
  pierside (foreign MSRAs)**, SeaPort-NxG overflow, and direct-award small services — the
  channels a new entrant might use before winning a home-port pool.
- **Depot prime landscape** (`model_depot_ship_repair.py` §10–12): BAE, GD NASSCO, HII, Vigor,
  Detyens anchor the depot $ share. After the PSC 1905 reconciliation, GD (Electric Boat) and
  HII (Newport News) gain on the embedded-MRO side (`research/psc1905/IMPACT…` §H/§I) — but that
  is *prime-landscape* (slides 17/18 in the workbook), not this contract-vehicle slide.
- **USCG gate is lower for dockside than drydock:** dockside repair has lighter gating; drydock
  needs **Std Spec 8634** facility certification and a qualified Dockmaster — a real barrier
  worth flagging for any cutter-MRO entry plan.

## Quotable stats & attributions

- "**~84%** of FY2025 Navy depot obligations (**$4.1B of $4.9B**) flow to MSRA-holders via
  MAC-MO regional pools as FFP delivery orders." (deck, slide 15)
- "~11 private CONUS MSRA yards; **BAE, GD NASSCO, HII, Vigor, Detyens** anchor the depot dollar
  share." (deck table)
- "Coast Guard cutter MRO is a separate **USCG/SFLC** track; drydock requires **Std Spec 8634**
  facility certification." (deck)

## Source line — ready to use

> Sources: (1) FPDS FY2025 obligations; (2) DFARS 217.71 (Master Agreements); (3) GAO MAC-MO references; (4) CNRMC MSRA instruction (2025); (5) USCG Std Spec 8634

## Caveats / confidence / staleness flags

- **Confidence: high** on the vehicle structure (DFARS 217.71 / CNRMC / USCG Std Spec 8634 are
  authoritative); **medium** on the exact **84% / $4.1B-of-$4.9B** split, which is an
  FPDS-derived ratio.
- `[!]` The 84% base is **"$4.9B Navy depot obligations,"** slightly broader than slide 14's
  **$4,781M** Depot Ship Repair (likely J998/J999 plus adjacent depot actions). If you need to
  defend the exact base, pull it from `model_depot_ship_repair.py` rather than equating it to the
  $4.78B segment figure — the **84% ratio** is the robust headline.
- This is a go-to-market / qualifications slide; figures are FPDS- and policy-sourced rather than
  tied to a single workbook accessor.
</content>
