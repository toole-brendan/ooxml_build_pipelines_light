# Flagged-vendor deep-dive research — 5 uncovered NAICS-flag vendors (2026-06-18)

Second-pass vendor characterization for the 5 high-dollar vendors behind the HII low-purity
NAICS flags that were NOT in the top-50 registry (see `../taxonomy_hii_scoring/low_purity_flags.csv`
and `../audit_log.md` §6). Ownership current through 2026-06-18. Same schema as the top-50 registry.
Derived work_type/delivered-output classifications are in `flagged_vendor_assignments.csv`.

---

### Parker-Hannifin Corporation — UEI N5KMLMXEPFM5 — $48.9M ($18.7M sub / $30.1M DDG)
- **What it is:** Parker's **Carson, CA Water Purification / Racor–Village Marine Tec** operation —
  NOT a generic Parker machinery site. Designs/builds/tests MIL-SPEC reverse-osmosis
  desalination/watermaker systems (potable + reactor-grade water) for Navy surface ships, subs,
  carriers; plus parts, technical assistance, repair.
- supplier_type: **integrator/OEM** · typical_deliverable: **integrated assembly/module**
- **NAICS verdict: MISLEADING — 333310** "Commercial & Service Industry Machinery" is too generic;
  it is a naval desalination-system OEM, not HVAC/service machinery.
- Parent/owner: establishment of Parker-Hannifin Corporation (parent UEI W138B61KN3Q7); ultimate =
  public shareholders, **NYSE: PH**. Domestic. Confidence: high.

### Alfa Laval Inc. — UEI WSK3WRSGKAU1 — $27.4M (all DDG)
- **What it is:** U.S. Alfa Laval entity — **heat exchangers**, centrifugal separators/decanters,
  filters/membranes, pumps, valves, marine pumping systems + parts/service. Characteristic naval
  outputs = heat-transfer, liquid-separation, fluid-handling (not raw piping material).
- supplier_type: **manufacturer** · typical_deliverable: **discrete component/equipment**
- **NAICS verdict: ACCURATE but INCOMPLETE — 332410** describes the heat-exchanger line (not
  misleading) but omits separators, filtration, pumps, valves, marine pumping.
- Parent/owner: **Alfa Laval AB (publ)**, Sweden (100% owner); ultimate = public shareholders,
  Nasdaq Stockholm (Winder Holding AG 29.53%, not majority). Domestic entity / foreign-owned. Confidence: high.

### Aircraft Appliances and Equipment Limited — UEI G78MQ69BN636 — $18.8M (all DDG)
- **What it is:** Mississauga operation, now **Trident Maritime Systems Canada**. Designs/builds/tests
  bespoke marine fuel- & lube-oil filtration/separation systems (diesel pre-filter coalescers, AVCAT
  filter-separators), specialized valves/actuators, aviation-support equipment, component overhaul.
  Filtration installed broadly across the USN fleet.
- supplier_type: **integrator/OEM** · typical_deliverable: **integrated assembly/module**
- **NAICS verdict: MISLEADING — 332420** "Metal Tank Mfg" understates engineered naval
  filtration/separation systems (proprietary internals, qualification, testing, integration).
- Parent/owner: immediate parent **Lake Shore Systems, Inc.** (AAE transferred 2025-03-01); group =
  **Trident Maritime Systems**; ultimate control = funds managed by **J.F. Lehman & Company**.
  Foreign operating entity (Canada) / U.S.-controlled. Confidence: high.

### Young Engineering & Manufacturing, Inc. — UEI LG88NCWJ3A95 — $12.6M (all sub)
- **What it is:** Designs/builds pressure-vessel-based **fluid-energy & hydraulic-transient control
  equipment** — bladder surge tanks, surge arrestors, pulsation dampeners, related pressure vessels.
  ASME Sec VIII, NAVSEA Level I/SUBSAFE; used aboard nuclear submarines.
- supplier_type: **manufacturer** · typical_deliverable: **discrete component/equipment**
- **NAICS verdict: ACCURATE — 332420.** Heavy-gauge pressure vessels are the physical product/central
  process; engineering + bladder internals add value but don't make the tank classification misleading.
- Parent/owner: no corporate parent identified; appears independent. Ultimate owner **not publicly
  verified** (Winston B. Young founded 1987; current beneficial ownership unconfirmed). Domestic.
  Confidence: **medium** (capability high; ownership unverified).

### INDEECO LLC — UEI FLMQAKFEMG64 — $11.2M ($0.4M sub / $10.8M DDG)
- **What it is:** Vertically integrated maker of engineered **electric-heating / thermal-management
  equipment** — immersion heaters, circulation/in-line process heaters, process-air heaters, tubular
  elements, marine heaters, SCR/step controls, control panels; ASME pressure-vessel heater packages.
- supplier_type: **manufacturer** · typical_deliverable: **discrete component/equipment**
- **NAICS verdict: ACCURATE — 333414** "Heating Equipment Mfg" directly describes the output; heating
  flowing fluids does not make it a piping supplier.
- Parent/owner: platform **ASPEQ Heating Group** (SPX electric-heating platform); ultimate parent
  **SPX Technologies, Inc.**, **NYSE: SPXC**. Domestic. Confidence: high.

---

**Takeaway:** the two materially misleading codes — **Parker 333310** and **AAE 332420** — hide an
engineered, integrated naval subsystem behind a broad machinery/vessel label; both flip to **03 Fluid**.
Alfa Laval 332410 is legitimate (heat exchanger) but under-scoped; Young 332420 and INDEECO 333414
accurately represent their characteristic outputs.
