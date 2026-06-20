# Methodology: Aircraft Carrier and Submarine MRO Coverage

**Purpose**: explain what the FPDS-based TAM captures (and what it doesn't) for U.S. Navy nuclear-powered platform sustainment — aircraft carriers (CVNs), attack submarines (SSNs), and ballistic-missile submarines (SSBNs).

---

## The structural limitation up front

A large slice of Navy nuclear MRO is performed by **Navy-owned public shipyards** staffed by federal civil servants, not contractors. That labor does not generate FPDS contract records.

The four public naval shipyards:

| Shipyard | Location | Primary workload |
|---|---|---|
| Portsmouth Naval Shipyard (NNSY) | Kittery, ME | SSN / SSBN maintenance, refueling |
| Norfolk Naval Shipyard | Portsmouth, VA | CVN / SSN maintenance, RCOH support |
| Puget Sound Naval Shipyard (PSNS) | Bremerton, WA | CVN / SSN maintenance, inactivation |
| Pearl Harbor Naval Shipyard (PHNSY) | Pearl Harbor, HI | SSN maintenance (Pacific fleet) |

Public-yard work flows through NWCF (Navy Working Capital Fund) budget exhibits, not contract awards. Any FPDS-sourced TAM is therefore structurally a **private-sector addressable market**, not the full Navy MRO market.

This was a deliberate scope decision. An earlier workbook version (v1.x) tried to reconcile FPDS contract data with top-down budget exhibits and hit incommensurability problems — budget authority (annual) is not directly comparable to FPDS obligations (cumulative lifetime). The current model focuses on the private-contractor slice because that data is clean and addressable, and accepts the public-yard gap.

**Live top-down anchors (v2.76+)**: the `Budget Anchors` data sheet now
surfaces the SCN line items relevant to nuclear-platform reconciliation
(Columbia BA-01 rollup, Virginia parent, CVN RCOH net-execution, CVN-80,
CVN-81) with FY24/FY25/FY26 values sourced from `data_v2.xlsx` and
cross-checked against `sources/SCN_Book.txt`. The Sub & Carrier Coverage
sheet references these via defined names (`SCN_COLUMBIA_FY25`,
`SCN_VIRGINIA_FY25`, etc.) so its reconciliation table is live.

The reconciled SCN nuclear-platform FY25 Enacted subtotal is **$22.7B**
(Columbia $9.58B BA-01 rollup + Virginia $9.60B parent + CVN RCOH $1.48B
net execution + CVN-80 $1.36B + CVN-81 $675M). An earlier snapshot
reported $27.5B, which conflated multi-year program authority for CVN
RCOH ($6.27B) with single-FY execution authority ($1.48B) and carried a
stale CVN-81 number. The corrected top-down $22.7B is **less** than
FPDS-captured obligations of $27.6B — which is the expected pattern:
SCN is multi-year money, so dollars enacted in FY22-FY24 are still
being obligated on new FY25 task orders, and each FY25-dated obligation
lands in the FY25 FPDS sum regardless of when the backing BA was
enacted. The gap is not a coverage failure; it is the same
appropriation-vintage dynamic that makes Services TAM ($7.1B) exceed
OMN 1B4B CE 928 Contract ($2.4B) on the MRO side. See
`METHODOLOGY_MRO_BUDGET_RECONCILIATION.md` for the parallel MRO-side
narrative.

---

## Aircraft Carrier (CVN) coverage

### What the model captures

| Work type | Coverage path | Approximate FY25 $ visibility |
|---|---|---|
| **RCOH** (Refueling Complex Overhaul, ~$3-4B per ship, every ~25 years) | HII Newport News contracts pulled via `combat_vessels` / `navy_vessels` / `shipbuilding` collections | Multi-billion per active RCOH |
| **Non-nuclear availabilities** (PIA, CIA, DPIA) — flight deck, catapult, hull coatings, HVAC, elevators | PSC J998/J999 (non-nuclear ship repair) | ~$203M FY25 |
| **CVN catapult + arresting gear M&R** | PSC J017 (2026-04-17 services expansion pull, minus FRC aviation exclusions) | ~$14M FY25 kept |
| **Elevators, cranes, materials handling** | PSC J039 in `navy_equip_services` | Small $ |
| **Reactor plant modernization via HII NNS** | Bundled inside combat_vessels / shipbuilding contracts, not under J044 directly | Multi-billion |

### What's missing (public-yard labor)

- Labor performed at **Norfolk NSY** on CVN availabilities (in-house labor, not contract)
- Labor performed at **Puget Sound NSY** on CVN availabilities and inactivations
- Labor performed at **Portsmouth NSY** on CVN-related tasking (limited)

These appear in NWCF budget data, not FPDS. The model's CVN TAM should be read as "private-sector CVN sustainment," not "total CVN sustainment."

---

## Submarine (SSN / SSBN) coverage

### What the model captures

| Work type | Coverage path | Approximate FY25 $ visibility |
|---|---|---|
| **SSN / SSBN new construction** | Electric Boat + HII NNS contracts in `combat_vessels` / `shipbuilding` | Tens of billions annually across active programs |
| **Reactor plant sustainment** | Fluor Marine Propulsion + Bechtel Plant Machinery contracts in `navy_aux_components` and `shipbuilding` | Multi-billion |
| **Submarine non-nuclear availability** (drydock, hull coatings) | PSC J998/J999 | Only ~$12M FY25 — very small |
| **Component-level OEM sustainment** — photonics masts, SSTGs, towed sonar arrays | PSC J020 in `navy_equip_services`; L019/L020 in 2026-04-17 services expansion | Tens of millions |
| **Afloat C4ISR installation** (CSRR, periscope successors) | PSC N019 via NIWC Atlantic AGCIS IDIQ | Tens of millions |
| **Submarine preservation / inactive fleet** | PSC J019 via IMIA, OWL International contracts | Tens of millions |

### What's structurally invisible

Public naval shipyards do the bulk of submarine MRO labor. This is the dominant gap:

- **Portsmouth NSY (Kittery ME)** — SSN/SSBN depot maintenance, MCRAs (Major Complex Repair Availabilities), refueling
- **Puget Sound NSY (Bremerton WA)** — SSN depot maintenance, SSGN conversions historically, Ohio-class work
- **Pearl Harbor NSY (Pearl Harbor HI)** — SSN depot maintenance for Pacific fleet
- **Norfolk NSY (Portsmouth VA)** — some SSN work

None of this labor generates FPDS contract records. A submarine sitting in a public yard for a 2-year SRA sees millions of labor-hours that do not appear in any contract data.

Additionally, SSBN strategic weapon sustainment is out of scope by design:

- **Trident II missile body** (MK6 guidance, MK7 reentry vehicle) — sustained under Strategic Systems Programs through Lockheed Sunnyvale + Draper Lab. This is weapon-system work, not ship MRO. Excluded.
- **Trident warheads** (W76, W88) — DOE/NNSA responsibility, not Navy FPDS. Never in scope.

### What IS in the TAM on the SSBN side

Ship-integrated weapon sustainment (launch tubes, fire control hardware installed in the hull) remains in scope when procured through NAVSEA channels. Cross-platform weapon system sustainment (the missiles themselves) is out.

Edge case to be aware of: Electric Boat "SHIPALT" (Ship Alteration) contracts under Strategic Systems Programs that physically modify the SSBN to accept new Trident configurations. These are ship work in character (hull modification), even though the program office is weapon-side. The current exclusion filter strips them by office; a future refinement could keep SHIPALT-in-description while excluding missile-body-only work.

---

## Why PSC J044 (Nuclear Reactors Maintenance) is nearly empty

A direct pull of PSC J044 / K044 / N044 for FY25 returned only $0.6M. Nuclear reactor sustainment is actually a multi-billion-dollar business. Why the disconnect?

Reactor plant work is bundled into prime-platform contracts at the **ship-level PSC** rather than broken out under J044. Specifically:

- Fluor Marine Propulsion (formerly BMPC) reactor plant components → PSC 4470 Nuclear Reactors (product), or PSC 1904/1905 (combat vessels)
- Bechtel Plant Machinery reactor plant sustainment → same
- HII Newport News RCOH work → PSC 1901/1905 (combat ships), bundled with the CVN's overall availability

Navy does not typically award post-delivery reactor maintenance work as a standalone J044 service contract. That work is part of larger availability contracts coded with the ship-level PSC. So the J044 PSC is technically the "right" code for post-delivery reactor M&R by contract language, but in practice the industrial base doesn't use it — the work is inside shipyard contracts that carry the ship PSC.

Bottom line: the reactor sustainment dollars ARE in the model. They just live under shipbuilding / combat vessels / aux components pulls, not under J044.

---

## Reconciliation guidance for readers

If you're presenting this model to an audience that will ask "does this include CVN reactor work?" or "does this include SSN depot maintenance?" — here is the response framework:

- **Private contractor slice**: Yes, comprehensively. Every major private prime (HII Newport News + HII Ingalls, Electric Boat, Fluor Marine, Bechtel Plant Machinery, BAE ship repair, NASSCO, Vigor, Detyens, Austal, Bollinger, etc.) is captured at the transaction level.
- **Public-yard slice**: Not by design. The four public naval shipyards (Portsmouth, Norfolk, Puget Sound, Pearl Harbor) perform labor in-house that does not appear in FPDS. A conservative estimate: ~$4-6B/yr of public-yard nuclear MRO labor is outside the TAM.
- **Strategic weapons**: Excluded. Trident missile body sustainment (Draper Lab, Lockheed Sunnyvale) is weapon-system work under SSP, not ship MRO.
- **Nuclear warheads**: Never in scope. DOE/NNSA responsibility.

This framing makes the TAM defensible: it is the **private-sector addressable Navy newbuild + MRO market, excluding strategic weapons and public-yard in-house labor.** That's the right scope for a contractor / investor who wants to size the commercially-available market.

---

## Sources and precedents

- `OBJECTIVE.md` — top-level project scope
- `J998_J999_RESEARCH.md` — detailed analysis of the non-nuclear ship repair market; documents the "CVN non-nuclear $ = $203M, SSN nearly absent" finding
- `J019_J020_N019_N020_RESEARCH.md` — component-level equipment M&R, photonics, SSTGs
- `EXCLUSION_CROSS_PLATFORM_ENG_IDIQS.md` — rationale for excluding SEAPORT-NXG / cross-platform engineering
- `restructuring/restructure_progress.md` — history of the v1 budget-reconciliation approach and why it was abandoned
- NAVSEA CNRMC (Commander, Navy Regional Maintenance Center) — the umbrella office coordinating the private-contractor sustainment network captured by this model
- NAVSEA 08 (Naval Nuclear Propulsion Program) — the program office coordinating reactor plant sustainment, whose contract flow shows up in the model via Fluor Marine + Bechtel Plant Machinery
