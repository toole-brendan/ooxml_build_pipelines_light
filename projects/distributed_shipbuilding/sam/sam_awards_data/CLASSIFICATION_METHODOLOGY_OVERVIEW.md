# Supplier classification — methodology overview

**As of 2026-06-18.** A concise statement of how the Navy new-construction subaward supplier base is
classified. Scope here is the *approach*; the task roadmap lives in `TASKS.md`.

## Purpose

Give every supplier in the post-filtered **$13.1B** canonical universe a defensible description of
*what it contributes to the shipbuilding supply base*, so dollars can be rolled up by capability and by
program (submarines vs DDG-51) without inventing record-level detail.

## Classification unit

The primary unit is the **supplier operating entity (UEI)** — not the corporate parent, and not the
subaward transaction. A subaward transaction carries no NAICS/PSC of its own; NAICS is an entity-level,
self-reported attribute. So entity-level labels describe *what the company makes or does*, and all of a
UEI's subaward dollars inherit its labels (join on `entity_uei`), preserving the $13.1B total.

The one exception is the **subsystem** dimension, which is genuinely record-level and is carried on the
transaction itself (see below). The entity-vs-transaction split is reconciled at the subaward join.

## The classification dimensions

Each dimension answers a different question and is kept independent of the others.

1. **`work_type` — type of work done.** The primary axis. Built on the granular **NAICS-6**
   entity taxonomy, refined by the vendor registry. 18 mutually-exclusive process categories +
   `99 Unresolved`, one label per UEI. Corpus-wide and comparable across programs.

2. **`delivered_output_class` — nature of the deliverable.** An additive overlay on the same
   NAICS-6 / registry evidence, describing the integration level of what the supplier delivers:
   `MA` Modular / integrated assembly · `CE` Discrete component / equipment ·
   `MT` Material / semi-finished input (with `SV` Service / non-article and `UN` Unresolved for
   completeness). One label per UEI.

3. **`subsystem` — part of the ship worked on.** Taken from the observed **SWBS** code present on
   **HII-DDG** subawards. Record-level, populated only where an SWBS code exists. SWBS identifies the
   ship system being worked on; it does not identify the type of work or the specific component — those
   come from `work_type` / `delivered_output_class`.

4. **`scope_status` — relevance to new construction.** A hygiene tag, independent of the other
   dimensions and applied at the end of the effort, once the full mapping and vendor registry are
   complete. It flags residual entries that should have been excluded upstream — e.g. workforce/training,
   GFE, prime-owned in-house work (an illustrative, non-exhaustive set). Handled by quarantine-and-report,
   not by purging the corpus.

## Evidence sources & precedence

For the entity-level dimensions, evidence is applied in this order per UEI:

1. **Curated vendor registry** — hand-verified operating-entity research, with the highest-dollar UEIs
   researched first and compared against their NAICS-6. Authoritative; highest precedence.
2. **NAICS-6 entity default** — the granular NAICS-6 → category mapping for the long tail.
3. **Unresolved** — when evidence is insufficient. Every UEI still receives a label on every axis;
   nothing is silently dropped.

Positive entity evidence beats the mechanical NAICS default (e.g. a desalination UEI maps to fluid
systems rather than the generic "machinery" code). The **`subsystem`** dimension is supplied directly by
the SWBS code on HII-DDG records and is not subject to this precedence.

## How HII-DDG and submarine data differ

- **HII-DDG subawards** carry all applicable dimensions: `work_type` and `delivered_output_class` from
  the entity (NAICS-6 / registry), plus `subsystem` from the observed SWBS code. Running both angles
  lets a single HII record describe both the ship system *and* the type of work / deliverable.
- **Virginia / Columbia (submarine) subawards** have no SWBS-equivalent. About half carry a
  GDEB-originated code, but it largely reflects order details (e.g. subcontracting dates) rather than
  work type, so it is not used for classification. Submarine suppliers are classified via the
  NAICS-6 / registry dimensions only.

## Standing rules

- `work_type` and `delivered_output_class` are **mutually exclusive, one label per UEI per axis**; the
  dimensions are not collapsed into one another.
- **Module (`MA`) is positive-evidence-only** — assembly-suggestive NAICS codes set a candidate flag,
  never an automatic module assignment.
- Always the **post-filtered $13.1B base** (GFE primes and SIB pass-throughs already removed upstream);
  the raw per-PIID pulls are not analyzed directly.
- **Scope is hull-builder new construction, including shipbuilder-procured non-nuclear long-lead / EOQ**
  material (carried on the GDEB master / LLTM PIIDs for submarines, commingled with Basic Construction).
  Excluded: nuclear-reactor LLTM (BPMI), GFE / component-prime advance procurement (GE propulsion, Aegis),
  and design / lead-yard / ship-alteration / planning-yard work. DDG long-lead is predominantly GFE, so
  the DDG base captures far less AP / LLTM / EOQ than the submarine base — **not a like-for-like make/buy
  comparison.**
- **`scope_status` is quarantine-and-report** — residuals are shown separately and retained so totals
  still tie to $13.1B; the corpus is not re-baselined for them.
- **Never compare subsystem mix across programs** — `subsystem` exists only for HII-DDG, so any
  cross-program system comparison would be a data artifact.
- Coverage is always reported segmented by **assignment basis** (registry / NAICS / unresolved).
