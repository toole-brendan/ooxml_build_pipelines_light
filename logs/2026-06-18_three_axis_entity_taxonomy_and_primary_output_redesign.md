# 2026-06-18 — Three-axis entity taxonomy (domain × role) + primary-output redesign: session log

Continues `logs/2026-06-18_classification_methodology_merge_and_consolidated_workbook.md`. This session split the
single `work_type` axis into **two** entity-level axes, replaced the deliverable taxonomy with a new 8-form
**primary output** set, and rewrote the `Taxonomy` sheet of `award_classification_refactor.xlsx` accordingly.
Written to be read cold. Active workbook: `projects/research_shared/award_classification_refactor.xlsx`.

---

## 1. The core decision — split `work_type` into two axes

The old single `work_type` list (01–18 + 99) was **not MECE**: categories 01–12/18 were *capability/domain*
buckets (electrical, propulsion, fluids, metals, electronics, ordnance, interiors…) while 13–17 were *role*
buckets (shipyard integration, engineering, installation/repair, distribution, support). One column answered two
orthogonal questions, forcing overlaps (a distributor of electrical gear → `01` or `16`?). NAICS structure
already encodes both separately (2-digit sector ≈ role; 6-digit detail ≈ domain), so the split is *more* faithful
to the source, not less.

**Settled entity-level model — three axes, keyed per (UEI × program):**
- **Capability domain** — technical/material area of competence. **Published.**
- **Operating role** — supply-chain function. **Internal validation layer, NOT published** (see §2).
- **Primary output archetype** — physical form / integration level of the primary delivered article. **Published.**

Plus the unchanged transaction-level `subsystem` (SWBS, HII-DDG only) and end-stage `scope_status`.

**Keying change:** classification is now per **UEI × program** (DDG-51 / Virginia / Columbia), not per UEI. The
same UEI may carry different (domain, role, output) across programs — they don't have to differ but can. Many
vendors recur across the three sheets (Curtiss-Wright, Globe, Hunt, Scot Forge, ESCO, Austal, W International).

## 2. Why operating role is a validator, not a headline

Role and output are partly **collinear** (a "service provider" role ≈ a non-article output; a distributor's
output is just what it resells). Rather than fight that, role is demoted from a co-equal published axis to an
**internal layer that informs and validates the primary-output assignment**. Mechanism: role is derived from the
entity's *business character* (NAICS sector, self-description), output from the *specific product evidence*; the
expected role→output crosswalk turns mismatches into review flags. Symmetric model that fell out of this:
- **role** is the universal axis (every entity has one);
- **domain** applies to technically-capable entities (N/A, carried by role, for pure non-technical firms);
- **output** applies to article-producers (N/A for service/distribution/support roles);
- role does the filtering. This fits the prior "present data before characterization / gates stay in the
  research layer" principle — role is the gate, domain+output go to the deck.

## 3. MECE legends designed from the three program vendor sheets

The two legends were designed to **cover every distinct vendor** in `DDG/Virginia/Columbia Top Vendors`, reading
**only the prose work-descriptions**. The pre-existing bracketed category tags in those sheets were explicitly
**ignored** — the user authored them under the now-retired methodology. One shared legend each, across all three
programs.

**The MECE fix that drove the domain list:** "precision machining" and "structural fabrication" are *how* a thing
is made → they are **roles (CF)**, not domains. Domain = technical area only.

### Capability domain (10 observed + 1 retained + residual)
`01` Electrical power (gen/conv/dist) · `02` Propulsion & power-transmission machinery (incl. electric drive) ·
`03` Fluid & pressure systems (valves/pumps/piping/air) · `04` Thermal/HVAC/refrig/atmosphere-life-support ·
`05` Hull, structures & marine fabrication · `06` Primary metals & metal-form production · `07` Polymers,
elastomers, composites & signature materials · `08` Sensors/electronics/comms/combat-control systems ·
`09` Ordnance, launchers & weapon systems · `10` Mechanical handling, deck machinery & access systems ·
`11` Interiors/habitability & general manufactured products (*no top-vendor hits — retained for full universe*) ·
`99` Cross-domain / unresolved.
- vs the old list: merged old `09`+`10` electronics into `08`; material-handling → `10`; signature/composite
  materials → `07`; **dropped "precision machining" as a domain** (now a role).

### Operating role (5 substantive + 2 residual)
`EM` Equipment & system manufacturer (OEM) → validates IS/EU · `PM` Component, parts & materials manufacturer →
PT/AS/NN/SF/CM · `CF` Contract fabricator / machinist & module builder (build-to-print) → VB/AS/PT ·
`DS` Distributor, processor & supplier · `SVC` Engineering, test, repair & sustainment services (non-article) ·
`HP` Holding / non-operating parent · `UR` Unresolved role.
- The two distinctions doing the real work: **EM vs PM** (operates standalone vs installs into something) and
  **own-product (EM/PM) vs build-to-print capacity (CF)**. Neither tracks output 1:1, so role stays an
  independent cross-check.

### Boundary / tie-break rules (to be written into the methodology doc)
1. Domain = technical area; role = supply-chain function; output = physical form. Machining/welding is a role, not a domain.
2. EM vs PM: functions standalone (pump/valve/radar/compressor → EM) vs installed part/material (fitting/seal/mount/forging/machined part → PM).
3. PM vs CF: own catalog/product (PM) vs build-to-customer-print capacity (CF).
4. Bare-vs-outfitted modules carried by the **output** axis (AS vs VB), not role — keeps CF non-redundant.
5. Multi-product firms → assign the primary (UEI×program) capability; may differ by program.
6. Pure service/holding firms → domain and output may be N/A, carried by role.

### Seven vendor adjudication calls agreed (for the applied table, NOT yet recorded anywhere)
CP Industries → domain `03`; American Steel & Aluminum → role `DS`; forges (Scot/Ellwood/Erie) → role `PM`;
Taylor Forge → role `CF` / domain `05`; Northrop-on-Columbia → domain `01` (turbine generators) as primary;
ESCO → domain `07` / role `PM`; machine shops B&F → `02` (shafting), Advance → `05` (HY-80 fab).

## 4. Primary output archetypes — replaced 10 → 8 (physical-form set)

The §5-prior 10-class deliverable set (`MA/SY/EQ/FB/CP/FG/MT/SV/MX/UN`) was **replaced wholesale** with a new
8-form physical taxonomy supplied verbatim by the user, each with a definition + boundary test:
**`VB` vessel block/zone module · `IS` integrated system/plant · `EU` equipment/packaged functional unit ·
`AS` assembly/subassembly/fabrication · `PT` finished part/discrete item · `NN` near-net/semi-finished workpiece ·
`SF` standard stock/mill form · `CM` bulk/process material or consumable.**
- Note the new set is **physical-form only** — no `SV` (service now lives on the role axis), no `MX`/`UN`. Open
  question deferred: how non-article entities and unknown-form article-producers are represented on this axis
  (currently N/A via role; no explicit residual row in the 8-set).

## 5. Workbook change — `Taxonomy` sheet rebuilt

- **Wiped and recreated** the `Taxonomy` sheet (fresh sheet at position 0, default Excel styling — no fills, bold,
  widths, freeze, or merges). Old structure (WORK TYPES / DELIVERABLE CATEGORIES / SWBS, 37 rows) fully replaced.
- New structure, 40 rows: top preamble (UEI×program keying + 3-axis model + which are published) → **CAPABILITY
  DOMAIN ARCHETYPES** → **OPERATING ROLE ARCHETYPES** → **PRIMARY OUTPUT ARCHETYPES** → **SWBS CODE MAPPINGS**
  (`TBD`, unchanged). Column-A ID/Code cells forced to text so leading zeros survive.
- Built via a **one-off `/tmp` script, run once, then deleted** (no standing re-run/overwrite risk, per the prior
  session's lesson). The other five sheets are untouched — row counts unchanged (Classifications 56, Vendor
  Context 56, DDG 39, Virginia 36, Columbia 30).

## 6. Where things stand / open items

- **`CLASSIFICATION_METHODOLOGY_OVERVIEW.md` is now materially stale** — still describes the single `work_type`
  axis and the old 5-class deliverable. Needs a rewrite to the three-axis model, the §3 boundary rules, the
  UEI×program keying, and the new 8-form output set. **Not done this session** (user deferred).
- **The seven §3 adjudication calls live only in this log** — should be moved into the methodology doc (or a rules
  note) before the applied table is built, so they aren't lost.
- **Primary-output residual/non-article handling** still undecided (§4).
- Platform tabs still un-normalized; `subsystem` (SWBS) still `TBD`; applied 1,203-UEI table (task C, tie to
  $13.1B) still the next substantive build.
