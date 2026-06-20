# Why the deliverable / output-form cut is hard

_Recorded 2026-06-18. A standing note on a structural difficulty in this data, not a decision. No
approach has been settled._

## The core problem

NAICS-6 classifies an establishment by its **industry / production process / operating role**. It does
**not** encode the **form or integration level at which a vendor's output crosses to the prime** — i.e.
whether the vendor hands over an outfitted module, an integrated system, a complete equipment unit, a
fabricated assembly, a discrete component, a near-net workpiece, or raw material.

That integration-level distinction — above all **"module" vs. "discrete component"** — is the headline
the downstream audience cares about, and it is precisely the distinction NAICS cannot see. The module↔
component boundary is a property of *what a given vendor actually delivers on these programs*, not of the
industry code it carries.

## The evidence (top-50 vendors by dollars)

Using the hand-adjudicated deliverable assignments for the 50 highest-dollar vendors — each assigned from
real product/vendor knowledge, independent of NAICS — vendors that **share the same NAICS-6 code** were
assigned **different** deliverable forms:

- **335312 Motor & Generator Mfg** — one vendor → module-level; another → discrete component.
- **336611 Ship Building & Repairing** — mostly module-level; at least one → discrete component.
- **333415 A/C & Heating Equipment** — split module vs. component.
- **332313 Plate Work Mfg** — split component vs. module.
- **335313 Switchgear Apparatus** — split module vs. component.

**~54% of the top-50 dollars sit in NAICS codes that map to more than one deliverable form.** If a single
NAICS code lands on both ends of the module↔component spine, NAICS cannot be the arbiter of that cut.

## The contrast — where NAICS *does* work

NAICS reliably pins only the **ends** of the spine, where the code names a process specific enough to imply
a form:

- **332111 Iron & Steel Forging** → material / near-net (consistent).
- **332911 / 332912 Valves & fittings**, **333914 Pumps** → discrete component / equipment (consistent).

So NAICS is a usable **coarse prior** for the material end, the discrete-component end, and the
service/non-article side — but it goes silent across the module / system / equipment / assembly middle.

## Why this likely understates the difficulty

- The assignments above used a **coarse 5-bucket scheme** (module / component-equipment / material /
  service / unresolved). A finer set (separating module vs. system vs. equipment vs. assembly vs.
  component) makes distinctions NAICS can resolve *even less* — so ~54% is a floor, not a ceiling.
- For a large share of dollars NAICS is **absent or misleading before resolvability even applies**: the
  single largest dollar code is a logistics-consulting code attached to a pass-through entity, and a
  further large block of dollars carries **no SAM NAICS at all**.

## The takeaway to remember

Getting output form at module/component granularity requires **entity-specific product evidence**, not the
industry code. NAICS can seed a first pass and pin the spine ends; the integration-level call in the middle
has to come from knowing what each vendor builds. This is the central reason the deliverable/output-form
axis is harder to populate than the capability/work-type axis.
