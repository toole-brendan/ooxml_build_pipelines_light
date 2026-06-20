# Award Classification Plan

## Context

With FY2025 Navy data deduplicated into a single set (4,892 awards, $52.6B), the next step
is classifying each award along the dimensions that matter for market sizing. The core
question: of the total spending, what is the serviceable addressable market (SAM) for a
company focused on module/subsystem work or subcontracting opportunities?

Three classification dimensions, in order of feasibility:

---

## Dimension 1: Spend Type (Newbuild vs MRO)

**Signal:** PSC code (deterministic for most awards)

| PSC Pattern | Classification | Examples |
|---|---|---|
| 19xx (product codes) | Newbuild | 1901 (Combatant Ships), 1905 (Combat Ships/Landing Vessels) |
| J9xx (service codes) | Repair/Overhaul | J998 (Ship Repair Overhaul), J999 (Ship Repair Alteration) |
| 58xx, 13xx, 14xx, etc. | System Procurement | 5840 (Radar), 5841 (Sonar), 1230 (Fire Control), 1425 (Guided Missile Launchers) |

System procurement (combat_electronics contracts) straddles newbuild and modernization --
a radar buy could be for a new ship or a mid-life upgrade. The `description` field or the
`dod_acquisition_program_description` can disambiguate in many cases (e.g., "DDG 51 Flight
III" = newbuild, "SEWIP Block III" = modernization of existing fleet).

**Confidence:** High for shipbuilding/ship_repair split. Medium for combat_electronics
newbuild-vs-modernization.

---

## Dimension 2: Module vs Integration

This is the key SAM filter. A module contract delivers a discrete subsystem (radar, engine,
combat system). An integration contract assembles modules into a ship.

**Signals available in the data:**

| Field | What it tells you | Strength |
|---|---|---|
| `gfe_gfp` | GFE=Y means the contractor receives govt-furnished equipment to integrate. GFE=N on a system-specific PSC means they deliver a module. | Strong -- best single field |
| `psc_code` specificity | Broad PSCs (1905) suggest integration. Narrow PSCs (5840, 1425) suggest module. | Strong |
| `dod_acquisition_program_description` | Ship programs (DDG 51, CVN 78) = integration. System programs = module. | Medium |
| Contract size | Very large ($1B+) contracts on ship programs are almost always integration. | Supportive |
| `recipient_name` | HII, GD/EB, Bath Iron Works = integrators. Raytheon, L3Harris, Rolls-Royce = module suppliers. | Supportive but brittle (same company does both) |

**Proposed logic:**
1. PSC 19xx + large value + ship DAP -> integration
2. PSC 58xx/13xx/14xx (system-specific) -> module
3. PSC J998/J999 (ship repair) -> classify by SWBS group if possible from description, otherwise "MRO - unclassified"
4. GFE=Y on a ship program -> integration (receiving modules)
5. GFE=N on a system-specific PSC -> module (delivering a subsystem)

**SWBS sub-layer:** Within module contracts, SWBS groups identify which system area:
- Group 100: Hull Structure
- Group 200: Propulsion Plant
- Group 300: Electric Plant
- Group 400: Command and Surveillance (radar, sonar, comms, EW)
- Group 500: Auxiliary Systems
- Group 600: Outfit and Furnishings
- Group 700: Armament (weapons, launchers, ordnance handling)

PSC codes map fairly cleanly to SWBS groups for combat_electronics. For ship_repair, the
contract `description` field is the primary signal (e.g., "main engine overhaul" -> Group 200,
"hull preservation" -> Group 100). This uses regex patterns against the ESWBS reference in
`docs/data_pulling_instructions/ESWBS_codes.txt`.

**Why SWBS matters for SAM:** The module/integration split tells you how much of the market
is module work vs prime integration work. SWBS tells you *which* module markets exist and
how large each one is. This is critical for SAM because a company's serviceable market
depends on what they actually build -- a propulsion OEM cares about Group 200 spending, a
radar company cares about Group 400, a weapons integrator cares about Group 700. Without
SWBS, you can say "there's $X in module work." With SWBS, you can say "there's $2B in
propulsion modules, $3B in C&S modules, $800M in armament modules" -- and a company can
map its capabilities to specific SWBS groups to calculate its actual SAM. The same logic
applies on the MRO side: a company that does combat system upgrades wants to know how much
MRO spending falls in Group 400, not just total MRO spending.

SWBS also enables competitive landscape analysis per system area. Group 400 (C&S) is
dominated by Raytheon and Lockheed Martin. Group 200 (Propulsion) has GE, Rolls-Royce,
and the shipyards. A company entering a specific SWBS group can see who the incumbents are
and what the contract structure looks like (FFP vs cost-plus, competed vs sole-source) in
that group specifically.

**Confidence:** High for the integration vs module split on newbuild. Medium for MRO SWBS
classification (depends on description quality).

---

## Dimension 3: Subcontracting / Outsourcing Opportunity

This is the most direct SAM measure -- which contracts actually flow work to subcontractors,
and how much?

**Signals available today:**
- `subcontracting_plan` -- whether the contract requires a subcontracting plan (already in
  the FPDS data). Presence of a plan means the prime is expected to subcontract.

**Signals requiring additional pulls:**
- `subaward_count` / `total_subaward_amount` -- from USAspending detail endpoint. Requires
  running `--enrich` on the deduped set. This gives actual reported sub-award volume per
  prime contract.
- Subaward detail -- who the subs are, what they were paid, for what work. Requires separate
  subaward pulls per PIID (the `subaward_data/` scripts or a new enrichment step).

**Proposed sequencing:**
1. Tag `subcontracting_plan` (already in data, free)
2. Run `--enrich` on the deduped set to get subaward counts (moderate effort, ~1 API call
   per award)
3. Pull full subaward detail for high-value awards with reported subs (targeted, not all
   4,892 awards)

**Confidence:** Low without enrichment (subcontracting_plan is binary, not quantitative).
High after enrichment for awards that report subs (not all do -- reporting thresholds apply).

---

## Recommended Sequence

1. **Tag spend type** (Dimension 1) -- PSC-based, deterministic, fast
2. **Tag module vs integration** (Dimension 2) -- PSC + GFE + DAP logic, build PSC-to-SWBS
   mapping from ESWBS reference
3. **Enrich with subaward data** (Dimension 3) -- run `--enrich` on deduped set, then
   targeted subaward pulls

All tagging happens on the deduped Navy FY2025 set (`navy_fy2025_deduped.json`, 4,892
awards). Output: same JSON with added classification fields, or a separate classified file.

---

## Reference Files

- `docs/data_pulling_instructions/ESWBS_codes.txt` -- ESWBS code definitions for SWBS mapping
- `docs/Expanded Ship Work Breakdown Structure (codes).pdf` -- Quick ESWBS reference
- `docs/data_pulling_instructions/usaspending_structured_fields.md` -- PSC/NAICS field analysis
- `data_pull/dedup_collections.py` -- Deduplication script (already built)
- `data_pull/output/fpds/navy_fy2025_deduped.json` -- Input for classification
