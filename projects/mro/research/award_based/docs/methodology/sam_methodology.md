# SAM Methodology

How the model defines and calculates the Serviceable Addressable Market (SAM).

---

## Definition

SAM = the subset of total Navy spending where a module/subsystem supplier can realistically
compete. In this model, SAM is operationalized as all awards where `work_role = "module"`.

The premise: if you're a company that builds discrete subsystems or components -- not a
shipyard that assembles entire ships -- your addressable market is the contracts where the
Navy is buying modules directly. You can't realistically compete for the $9.3B Columbia-class
prime contract (that's Electric Boat's integration work), but you can compete for the $850M
SPY-6 radar production contract or the $362M Aegis fire control contract.

---

## TAM vs SAM

| Layer | Definition | FY2025 | What's in it |
|---|---|---|---|
| **TAM** | Total spending on newbuild + system procurement + MRO + modernization | $52.0B | Everything the Navy obligates on ship construction and maintenance |
| **SAM (Module)** | Awards where work_role = module | $10.7B | Subsystem deliveries, component procurement, system-specific MRO |
| **Not in SAM** | Awards where work_role = integration | $41.1B | Ship-level prime contracts, large depot availabilities |
| **Unclassified** | Awards where work_role = unclassified | $813M | Can't determine module or integration from available data |

---

## What makes an award "module" vs "integration"

### Module (SAM)

The contractor delivers a discrete subsystem, component, or system-specific service:

- Raytheon delivering SPY-6 radar arrays (PSC 5840, $850M)
- Lockheed Martin delivering Aegis fire control systems (PSC 1230, $362M)
- Kongsberg delivering NSM missile systems (PSC 1425, $435M)
- Undersea Sensor Systems delivering sonobuoys (PSC 5845, $137M)
- A shipyard doing main engine overhaul on a specific vessel (J998 with propulsion
  description)
- A contractor replacing nonskid deck covering (J999 with hull description)

Key signals: system-specific PSC code (5840, 1230, etc.), GFE=N on a component contract,
description naming a specific subsystem.

### Integration (not in SAM)

The contractor manages ship-level work and receives/assembles modules:

- Electric Boat building Columbia-class submarines (PSC 1905, $9.3B)
- HII building DDG-51 destroyers (PSC 1905, $2.5B)
- BAE Systems managing a DDG depot availability (J999, $248M)
- Metro Machine managing a carrier maintenance period (J998, $128M)

Key signals: vessel-level PSC code (19xx), large dollar value on ship program, GFE=Y on
a shipyard contract, description referencing a full availability (DSRA, DMP, etc.).

---

## SWBS: Which module market?

The SWBS (Ship Work Breakdown Structure) group tells you which system area the module work
falls in. This is critical because a company's actual SAM depends on what they build:

| SWBS Group | FY2025 Module $ | Share | Who competes here |
|---|---|---|---|
| 4: Command & Surveillance | $7.8B | 72.6% | Raytheon, Lockheed Martin, L3Harris, Northrop Grumman, BAE Systems |
| 7: Armament | $1.3B | 11.8% | Raytheon, Kongsberg, GD Mission Systems, SAIC |
| 9: Ship Assembly/Support | $413M | 3.9% | Regional shipyards, trade labor contractors |
| 2: Propulsion Plant | $386M | 3.6% | Rolls-Royce, GE, BAE Systems, Bechtel |
| 1: Hull Structure | $315M | 2.9% | Regional shipyards, marine contractors |
| 3: Electric Plant | $218M | 2.0% | Raytheon (converters), DRS, L3 |
| 6: Outfit & Furnishings | $59M | 0.5% | Various small contractors |
| 5: Auxiliary Systems | $19M | 0.2% | Various small contractors |
| Unclassified | $269M | 2.5% | Mixed |

A radar company's SAM is $7.8B (Group 4). A propulsion OEM's SAM is $386M (Group 2). A
weapons integrator's SAM is $1.3B (Group 7). The total module market is $10.7B but no
single company addresses all of it.

The SWBS breakdown also crosses with spend type. Within Group 4 (C&S):
- $7.2B is system procurement (new radar/sonar/EW buys for new ships)
- $372M is MRO (combat system repairs and upgrades on existing ships)
- $107M is modernization (equipment modifications like SEWIP upgrades)

A company focused on combat system sustainment sees a different SAM than one focused on
new-build system production, even within the same SWBS group.

---

## What SAM doesn't capture yet (Dimension 3)

The current SAM definition (work_role = module) answers: "how much does the Navy spend on
discrete subsystem/component contracts?" This captures direct module procurement.

It does NOT capture a second important SAM pathway: **subcontracting on integration
contracts**. When Electric Boat builds a submarine, they subcontract billions of dollars to
module suppliers -- propulsion components, combat system elements, hull outfitting. That
subcontracted spend is part of the module supplier's real addressable market, but it shows
up in our data as a single $9.3B integration contract awarded to Electric Boat.

To capture this, we need:

1. **Subaward data** from USAspending (`--enrich` flag on the pull script adds subaward
   counts and total subaward amounts per prime contract)
2. **Subaward detail pulls** for high-value integration contracts to see who the subs are,
   how much they receive, and what SWBS group the subcontracted work falls in

This would create a second SAM lens:

| SAM Lens | What it measures | Data source |
|---|---|---|
| **Direct module SAM** (current) | Navy contracts awarded directly for subsystem work | Awards where work_role = module |
| **Subcontract SAM** (future) | Work subcontracted by primes to module suppliers | Subaward data on integration contracts |
| **Combined SAM** | Total addressable market for module suppliers | Union of both |

The combined SAM would be significantly larger than the current $10.7B because it would
include the subcontracted portion of the $41.1B integration market. For context, major
shipbuilding programs typically subcontract 40-60% of contract value.

---

## How to use this in the workbook

The Awards Data table has `work_role` and `swbs_group` on every row. To find your SAM:

1. Filter Awards Data to `work_role = "module"`
2. Filter to your SWBS group(s)
3. Optionally filter by `spend_type` (newbuild vs MRO) and `vessel_class`

The Newbuild and MRO sheets have pre-built SWBS tables that show this breakdown. The
Output sheet shows the full waterfall from TAM to module SAM.
