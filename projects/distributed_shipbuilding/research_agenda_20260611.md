# Research agenda — post-review next steps (2026-06-11)

Three research items coming out of the colleague review of the mini-deck.
Captured here as standalone research tasks; deck integration comes later.

---

## 1. Penetration ceiling testing — what is the true upper limit on outsourcing?

**The question.** What is the structural maximum share of new-construction Basic
Construction work that *can* be outsourced from the prime yards? The current
ceiling in the model is intent-based (stated ~30% uplift over recent actuals),
not physics-based. Colleague's hypothesis: the irreducible prime-yard core is
**final assembly + integration + final test** — work that has to happen where
the hull comes together — and everything else is in principle movable. But
nobody has sized that core as a % of Basic Construction.

**Sub-questions.**
- What work content is genuinely location-locked to the prime yard?
  Candidate buckets: erection/final assembly of hull modules, shafting/alignment,
  combat-system integration and light-off, dockside/sea trials, final test &
  certification. What else — e.g., nuclear work on VCS/CLB (reactor module
  installation, primary plant) is locked to NNS/EB regardless.
- How big is that locked core as a share of BC cost or BC labor hours, per
  class? DDG-51 (conventional, serial production) vs Virginia (nuclear,
  module-built across EB/NNS already) vs Columbia will differ materially.
- Is there a precedent ceiling to benchmark against? Candidates:
  - Virginia-class module split between EB and NNS (the most heavily
    distributed US naval program already) — what share of construction hours
    happen away from the delivering yard?
  - Submarine "module outfitting" levels cited in EB/NNS investor and trade
    press material (degree of outfitting before module shipment).
  - Commercial shipbuilding and Korean/Japanese yard block-subcontracting
    rates as an outside-in upper bound.
  - Aircraft analogy (777/787-style structures outsourcing) as a sanity
    check on how far final-assembler share can compress.
- Does the ceiling bind on dollars or on labor? If the locked core is
  labor-heavy but material-light, a dollar-based ceiling could be higher than
  an hours-based one (links to item 2).

**Candidate sources.**
- WSARA/SAR and GAO shipbuilding reports (GAO-23/24/25 series on shipbuilding)
  — occasionally break out assembly vs outfitting vs test phases.
- RAND and CBO shipbuilding cost studies (CBO's ship cost analyses break
  hull/mech/elec vs integration in places).
- SCN budget justification "Basic Construction / Change Orders" cost detail
  and the P-5c subline structure — check whether end-cost categories separate
  assembly/test from fabrication.
- NAVSEA cost-estimating literature (e.g., NSWCCD/NAVSEA 05C papers) on ship
  work breakdown structure (SWBS) group shares — SWBS 800/900 (integration,
  trials, support) vs 100–700.
- EB / HII statements on module outfitting percentages and "ship's worth of
  work" moved to suppliers.

**Deliverable.** A per-class estimate (or bounded range) of the
non-outsourceable core as % of BC, with an explicit basis (hours vs dollars),
that can replace or validate the flat ×1.30 intent ceiling.

---

## 2. Converting "manhours" growth claims to outsourced dollars

**The question.** Primes and the 30-Year Shipbuilding Plan talk about
outsourcing in **manhours** ("grow outsourced manhours to distributed
shipbuilding ~30% y/y"). The model and TAM are in **dollars**. What is the
defensible conversion, and does 30% hours growth equal 30% dollar growth?

**Sub-questions.**
- What does a manhour of outsourced work *cost* vs a manhour of prime-yard
  work? Components: fully burdened labor rate differentials (prime yard vs
  regional fabricator), overhead/G&A treatment, and whether outsourced work
  packages carry their own material.
- Is the cited 30% y/y growth on a labor-only base, or does the dollar value
  of an outsourced package include material pass-through? If a package is
  ~50% material, hours growth understates dollar growth (or vice versa).
- What share of Basic Construction cost is labor vs material per class?
  (SCN budget detail, SAR cost variance breakouts, NAVSEA cost models.)
  This gives the bridge: outsourced hours × burdened rate (+ attached
  material) → outsourced $.
- Do the primes define "manhours outsourced" as hours *displaced from the
  prime yard* or hours *worked at the supplier*? Productivity differentials
  (a supplier hour may not equal a yard hour of progress) change the
  conversion.
- Cross-check: can the FPDS/subaward dollar series already assembled be
  divided by plausible burdened rates to back out an implied hours series,
  and does its growth rate match the stated hours-growth claims?

**Candidate sources.**
- HII / GD earnings calls and investor days (where the ~30% y/y outsourcing
  language appears) — pull exact phrasing: hours, dollars, or "work".
- 30-Year Shipbuilding Plan (FY25/FY26/FY27 editions) outsourcing/distributed
  shipbuilding language.
- BLS / DoD labor-rate data and DCAA forward-pricing-rate context for prime
  yards vs second-tier fabricators; union contract reporting (Newport News
  USW, EB MTC) for base wage anchors.
- SUBMEPP / NAVSEA standard-hour estimating references if findable.
- PB27 P-10 Strategic Outsourcing narrative (already cited for the 30%
  intent) — check whether its basis is hours or dollars.

**Deliverable.** A conversion rule (e.g., "1% outsourced-hours growth ≈ X%
outsourced-dollars growth, because …") with stated rate and material
assumptions, so manhour-based public statements can be mapped onto the
dollar-based TAM and forecast bands.

---

## 3. Identifying *competable* work within the outsourced pool (priority)

**The question.** Within the already-sized outsourced % of new construction
for DDGs and submarines, which work areas / specific awards are realistic
targets for a new entrant — i.e., not structurally locked up — and what
methodology identifies them systematically?

**Hypotheses for what makes work competable.**
- **Prime wants a second source**: explicit second-source solicitations,
  dual-sourcing language in SIB/industrial-base documents, primes publicly
  recruiting suppliers for a work type (e.g., HII/EB supplier days,
  BlueForge Alliance solicitations).
- **Incumbent is a poor performer**: schedule/quality problems visible via
  GAO/DOT&E mentions, CPARS-adjacent signals, stop-work or re-award
  patterns, repeated re-solicitation of the same scope.
- **Incumbent is capacity-constrained**: supplier already at max (e.g., the
  known casting/forging and valve bottlenecks), so growth gets competed even
  if the incumbent keeps base volume.
- **Short award cadence / expiring vehicles**: scope re-awarded annually or
  per-block rather than locked into long MYP subcontracts; upcoming
  recompete dates.
- **Low specialization / transferable certifications**: work types where the
  barrier is general (NAVSEA welding certs, MIL-spec QA) rather than
  proprietary (nuclear-grade, single-qualified part).
- **Geographic insensitivity**: work that ships (pipe spools, vent dampers,
  electrical panels, outfitted modules) vs work tied to the waterfront.

**Methodology sketch.**
1. **Decompose the outsourced pool by work type and supplier.** Use the
   subaward records behind the existing TAM: cluster by NAICS / PSC code and
   by description keywords into work-type buckets (structural fab, pipe,
   electrical, machinery, joiner/outfitting, etc.).
2. **Score each bucket / incumbent on competability signals**: incumbent
   concentration (1 supplier vs many), award cadence, second-source language,
   performance red flags, certification barrier height, ship-ability.
3. **Build a target list**: rank buckets (and within them, specific
   incumbent awards) by score; flag the "why now" for each (recompete date,
   stated second-source intent, incumbent distress).
4. **Validate top targets qualitatively**: trade press, supplier-day
   materials, and the exec-quote corpus for stated sourcing intent in those
   exact work types.

**Candidate sources.**
- FPDS-NG + FSRS/SAM subaward data (already in hand for the TAM) — the
  decomposition substrate; NAICS/PSC + free-text descriptions.
- SAM.gov solicitations from the primes' supplier portals and from NAVSEA
  for GFE-adjacent scope; HII/EB supplier-opportunity pages.
- BlueForge Alliance / Submarine Industrial Base program announcements —
  these explicitly name work types being seeded with new suppliers.
- GAO and CRS shipbuilding industrial-base reports for named bottleneck
  commodities and poor-performance areas.
- DDG-51 land-based and follow-yard history (BIW vs HII Ingalls split) for
  what scope has historically been competed between yards.
- usaspending.gov sub-award detail for incumbent concentration and award
  cadence per work type.

**Deliverable.** A scored, ranked "competability map": work-type buckets ×
competability criteria, with named incumbent awards and the evidence trail
for the top targets. This becomes the methodology exhibit for the next deck
iteration.

---

## Sequencing

Item 3 is the stated priority and is also the most data-driven (it reuses the
subaward corpus). Items 1 and 2 are primarily document research and can run
alongside; item 2's hours→dollars bridge feeds item 1 (whether the ceiling
binds on hours or dollars) and the credibility of the 30% growth framing.
