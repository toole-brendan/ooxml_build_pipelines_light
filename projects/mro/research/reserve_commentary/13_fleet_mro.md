# Slide 13 — Marauder-Like Fleet MRO (module: `fleet_mro.py`)

> Breadcrumb: SAM › Fleet MRO · static hull × work-segment Marimekko · `_chart_xml/slide13.xml`

## On-slide claims (verbatim)

- **Takeaway:** "Marauder comp-set MRO totals **$758M** across six work segments, with **82%
  concentrated in depot ship repair** and the rest in port and technical services."
- **Caption:** "FY2025 Marauder-Like Fleet MRO by Hull × Work Segment ($M)."
- **Primary work types:**
  - Depot Ship Repair: **$623M (82%)** — MSC ROH and mid-term availabilities at MSRA yards
    (J998/J999).
  - Port & Technical: **$107M (14%)** — husbanding, pierside tech reps, logistics support.
  - HM&E: **$28M (4%)** — hull/mechanical/electrical sustainment outside the depot envelope.
  - Combat, Electronics, Nuclear: **minimal** — MSC/USCG hulls carry no combat-system or
    nuclear-overhaul stream.
- **Hull concentration:**
  - T-AO oilers: **$384M (51%)** — largest single hull program by far.
  - T-AKE dry cargo: **$208M (27%)** — MSC Lewis & Clark class.
  - ESB + T-ESB: **$64M (8%)**.
  - T-EPF expeditionary fast transport: **$59M (8%)**.
  - WPC + WLB cutters: **$43M (6%)** — only USCG hulls with material FY2025 spend.
- **Note:** "Nuclear & Complex Overhauls column is blank because embedded MRO covers only CVN,
  SSN, SSBN, and surface-combatant programs, not MSC auxiliaries or USCG cutters." Source: FPDS
  FY2025 contract obligations.

## Claim-by-claim sourcing

| Claim | Source |
|---|---|
| Comp-set total **$758M** | `model_sam_build.py` `target_hull` SAM (all segments) |
| Depot **$623M (82%)** | `target_hull` ∩ depot = the SAM (slide 14); `model_depot_ship_repair.py` hull cross-tab |
| Port & Tech **$107M**, HM&E **$28M** | `model_sam_build.py` / `model_depot_ship_repair.py` segment cross-tabs |
| Per-hull (T-AO $384M, T-AKE $208M, …) | `model_depot_ship_repair.py` hull × segment; FPDS FY2025 |

- **The numbers close:** per-hull $384M + $208M + $64M + $59M + $43M = **$758M**; per-segment
  $623M + $107M + $28M = **$758M**. Both partitions of the same comp-set total.

## Reserve facts (could be added)

- **T-AO fleet oilers are the engine of the comp-set** — $384M, **51%** of all comp-set MRO
  (John Lewis-class / Kaiser-class). T-AKE dry cargo (Lewis & Clark class) adds $208M (27%). The
  two MSC auxiliary classes together are **78%** of comp-set MRO.
- **The $623M depot slice IS the SAM** (slide 14). The $135M non-depot remainder ($107M Port &
  Tech + $28M HM&E) is what slide 14 lists as "out of scope" for SAM.
- **Structural difference from the combatant fleet:** comp-set hulls carry **no nuclear or
  combat-systems work** — the Nuclear & Complex column is blank by construction because embedded
  PSC 1905 MRO only touches CVN/SSN/SSBN/surface combatants, never MSC auxiliaries or USCG
  cutters. This is why the comp-set is cleanly "depot + services," a good fit for a commercial
  entrant.

## Quotable stats & attributions

- "Comp-set MRO **$758M**, **82% depot** ($623M); **T-AO oilers $384M (51%)** and **T-AKE dry
  cargo $208M (27%)** dominate." (deck, slide 13)
- "MSC auxiliaries and USCG cutters carry no combat-system load or nuclear-overhaul stream —
  the comp-set is depot-and-services by nature." (deck note)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard (depot PSCs J998 / J999)

## Caveats / confidence / staleness flags

- **Confidence: high** — both the per-hull and per-segment partitions sum to $758M.
- `[!]` The takeaway says "the rest in port and technical services," but the non-depot remainder
  is actually **Port & Tech 14% ($107M) + HM&E 4% ($28M)** — a minor simplification.
- Per-hull Marimekko percentage cells (e.g. T-AO 81%/11%/5%) are read from the static exhibit;
  exact per-cell figures live in `model_depot_ship_repair.py`.
- PSC 1905 reconciliation has **zero effect** on this slide (embedded MRO excludes these hulls).
</content>
