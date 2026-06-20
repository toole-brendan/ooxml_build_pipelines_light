# Slide 07 — TAM Composition (module: `tam_composition.py`)

> Breadcrumb: TAM › TAM Composition · static Marimekko (work segment × vessel type) · `_chart_xml/slide07.xml`

## On-slide claims (verbatim)

- **Takeaway:** "Depot ship repair and nuclear and complex overhauls drove **~74%** of the
  **$9.0B** FY2025 MRO TAM, led by **DDG availabilities** and **SSN / CVN overhauls**."
- **Marimekko:** "Segment composition by hull" — work segment (rows) × vessel type (columns).
- **Six vessel-type column totals ($M):** 2,239 · 1,441 · 2,093 · 769 · 759 · 1,667 (sum ≈
  $8,971M). Columns: Submarines, Surface Combatants, Aircraft Carriers, Amphibious Warfare
  Ships, Combat Logistics Ships, Other.
- **Commentary rail (per segment, from the source exhibit):**
  - Depot Ship Repair — DDG **25% ($1.2B)**, LPD **13% ($613M)**; T-AO/CVN/LSD/LCS each 6–7%.
  - Nuclear & Complex Overhauls — **SSN 66% ($1,255M)**, **CVN 18% ($337M)**.
  - HM&E — DDG 6%; LCS/LPD/T-AO/CVN 2–3% each.
  - Combat Systems — **SSBN 55% ($319M)** (Trident II / VLS).
  - Port & Technical — T-AO/DDG/T-AKE/CVN 8–10%; ESB 4%.
  - Electronics & C4ISR — SSBN **13% ($42M)**; CVN/SSN/DDG trace.
- **Footer:** "(Uncl) columns reflect equipment-maintenance contracts referencing components
  rather than specific hulls. Source: FPDS FY2025. Data as of April 2026."

## Claim-by-claim sourcing

| Cell anchor | Value | Source |
|---|---:|---|
| SSN nuclear/complex | **$1,255M** | `model_reconciliation.py` `PSC1905_MRO_SSN` (EB Seam Split $831M + USS Boise EOH $424M) |
| CVN nuclear/complex | **$337M** | `model_reconciliation.py` `PSC1905_MRO_CVN` (CVN-68 inactivation + Eisenhower PIA + CVN-74/75 RCOH support) |
| SSBN combat systems | **$319M** | Trident II sustainment — Draper MK7 LE2, RDT&E-DW 097-0400 (`model_reconciliation.py` §2 RDTE-DW note: "$318M") |
| DDG depot | **$1.2B (25%)** | `model_services.py` §13–14 vessel × segment cross-tab |
| Full per-cell $M and % grid | — | `model_services.py` §13–14; `model_depot_ship_repair.py` §13–14 |

- Embedded PSC 1905 by vessel (the Nuclear & Complex rows) is locked in `model_reconciliation.py`:
  **SSN $1,255M · CVN $337M · DDG $77M · LCS $41M · Unclassified $193M** (= $1,904M total). The
  per-vessel attribution rationale is `research/psc1905/ANSWER_psc_1905_embedded_mro.md` §4.3 and
  the Mekko-uplift mapping is `research/psc1905/IMPACT_psc1905_on_workbook_tam.md` §D.

## Reserve facts (could be added)

- **SSBN Combat Systems = $319M is essentially one program:** Draper Laboratory **MK7 LE2
  Trident II** sustainment, funded **RDT&E Defense-Wide (097-0400)**, >5-yr POP — why it shows
  up under SSBN and why it barely converts to FY25 revenue (19% Frame-B apportionment).
- **The two leaders behind the "~74%":** Depot Ship Repair $4,781M + Nuclear & Complex $1,904M
  = $6,685M = **74.5%** of $8,971M. Within depot, **DDG ($1.2B) and LPD ($613M)** lead; within
  nuclear/complex, **SSN ($1,255M) and CVN ($337M)** lead.
- **"(Uncl)" columns** = equipment-maintenance contracts that name a component, not a hull
  (e.g. a pump or a radar line item) — `PSC1905_MRO_UNCL` ($193M) is the embedded-MRO portion
  of that.
- Exact per-cell values (every segment × vessel intersection, $M and %) live in
  `model_services.py` §13–14 — point there if anyone wants a number not on the rail.

## Quotable stats & attributions

- "Depot + nuclear/complex = **~74%** ($6.7B) of the $8,971M TAM; led by DDG availabilities and
  SSN/CVN overhauls." (deck, slide 07)
- "Submarine nuclear/complex MRO = **$1,255M**, almost entirely Electric Boat seam-split hull
  repairs ($831M) and the USS Boise engineered overhaul ($424M)." (`model_reconciliation.py`)
- "SSBN combat-systems sustainment = **$319M**, dominated by the Draper MK7 Trident II program."
  (`model_reconciliation.py` §2)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard; (2) FPDS PSC 1905 shipbuilding awards (embedded MRO: SSN, CVN, surface combatants)

## Caveats / confidence / staleness flags

- **Confidence: high** on the named anchors (SSN $1,255M, CVN $337M, SSBN $319M all tie to
  workbook cells); **medium** on the rail's rounded mid-size percentages (read exact from
  `model_services.py` §13–14).
- `[!]` The **Nuclear & Complex Overhauls** rows are the embedded PSC 1905 integration
  (SSN/CVN/DDG/LCS/Uncl) — absent from the April methodology framing. The "$9.0B" denominator
  is the reconciled $8,971M.
- Vessel-column-total → bucket mapping (2,239/1,441/2,093/…) is read off the static exhibit;
  if you need the authoritative per-column figure, use the workbook cross-tab rather than the
  chart label.
</content>
