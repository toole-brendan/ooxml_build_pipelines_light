## Proposed Slide 5 - Sub & Carrier Scope (MOCKUP - NOT YET DELIVERED)

Status: mockup / proposal. Not yet built in the deck. Paired with the new
workbook sheet `Sub & Carrier Coverage`, which is the data source for
every figure on this slide.

Purpose: anticipate the reader question from Slides 1-3 ("does this TAM
include submarine and carrier MRO?"). Answer honestly by showing where
those dollars actually live - in Services TAM, under Newbuild / Product
Procurement PSCs, inside the structurally empty nuclear PSCs, or entirely
outside FPDS in public naval shipyard labor.

Style: matches the existing 4-slide deck. `Topic | assertion` title, left
chart / right table / call-out / source footer layout.

---

### Title

Sub & Carrier Scope | FY2025 private-contractor sub and carrier MRO in the
Services TAM is ~$1.3B; the bulk of nuclear-platform work is either
bundled into shipbuilding PSCs or performed in-house at public naval
shipyards

### Subtitle

Where FY2025 U.S. Navy submarine + aircraft carrier dollars actually live
($M)

---

### Left visual - horizontal bar chart

Eight bars, ranked largest to smallest, darkening from light slate (out of
scope) to navy (in Services TAM) to signal "captured in this workbook"
status. Each bar labeled with $ value and the data source convention
("FPDS" vs "Budget book").

| Bucket                                                      | FY25 $M  | Data source               | In Services TAM?  |
|-------------------------------------------------------------|---------:|---------------------------|-------------------|
| Submarines - Newbuild/Product (PSC 1905 family)             | $24,279  | FPDS Awards master        | No (Newbuild)     |
| Public naval shipyard labor (implied, all Navy ships)       |  $9,535  | OMN SAG 1B4B derivation   | No (out of FPDS)  |
| PSC 4470 Nuclear Reactors (cross-platform product)          |  $1,875  | FPDS Awards master        | No (Reactor)      |
| Aircraft Carriers - Newbuild/Product (PSC 1905 family)      |  $1,431  | FPDS Awards master        | No (Newbuild)     |
| Submarines - Services MRO (J/K/N/M PSCs)                    |    $838  | FPDS Awards master        | **Yes**           |
| Aircraft Carriers - Services MRO (J/K/N/M PSCs)             |    $422  | FPDS Awards master        | **Yes**           |
| Nuclear Maintenance PSCs (J044 / K044 / N044)               |     $~0  | FPDS Awards master        | No (empty)        |

Legend below chart: navy bars = in Services TAM; slate bars = captured in
FPDS but out of Services scope; light-gray bar = NOT in FPDS at all
(public-yard labor).

### Right visual - Budget-book anchor table

Column header "FY25 Enacted Budget Authority" with two mini-sections:

**OMN - Ship Maintenance (SAG 1B4B)**

| Line                                       | FY25 $M   | Source             |
|--------------------------------------------|----------:|--------------------|
| Total 1B4B Ship Maintenance                | $11,764   | OMN_Book line 6714 |
| of which "Ship Maintenance By Contract"    |  $2,228   | OMN_Book line 6698 |
| implied non-contract (public yard + supt.) |  $9,535   | Computed           |

**SCN - Nuclear Platform Line Items**

| Line Item                                       | FY25 $M | Source             |
|-------------------------------------------------|--------:|--------------------|
| LI 1045 Columbia Class (BA01 total = construction + AP) | $9,581  | SCN_Book line 270  |
| LI 2013 Virginia Class (parent aggregate)       | $9,600  | SCN_Book lines 310+SFF+CPY |
| LI 2086 CVN Refueling Overhauls (FY25 net execution) | $1,480  | SCN_Book lines 357-362 |
| LI 2001 Carrier Replacement (CVN-80)            | $1,359  | SCN_Book lines 280-281 |
| LI 2004 CVN-81                                  |   $675  | SCN_Book line 307  |
| **SCN nuclear-platform subtotal**               | **$22,695** | Sum                |

Top-down cross-check: SCN nuclear-platform FY25 Enacted budget authority
$22.7B vs FPDS PSC 1905 subs + carriers + PSC 4470 = $27.6B captured
obligations (net sum of FY25-dated mod actions). FPDS exceeds top-down
because SCN is multi-year: dollars enacted in FY22-FY24 are still being
obligated on new task orders in FY25, and the full obligation dollar
lands in FPDS FY25 even when the backing BA was enacted earlier. Same
dynamic on the MRO side: Services TAM $7.1B vs OMN 1B4B CE 928 contract
slice $2.4B (plus OMN CE 928 is 1-year money only - SCN/OPN/NWCF-reimb
obligations on MRO PSCs land on FPDS but not on OMN CE 928).

### Call-out box (light-blue, italic, below the right table)

Note: PSC 1905 is NOT purely newbuild. The $424M HII USS Boise (SSN-764)
Engineered Overhaul is a real SSN depot event coded as shipbuilding, not
J998/J999. OMN SAG 1B2B text explicitly funds "Virginia Class submarine
obsolescence materials public shipyard outsourcing work." The Services
TAM submarine slice therefore undercounts private-sector sub MRO that
gets bundled under the newbuild PSC.

### Footnotes

1. "Public naval shipyard labor" is implied: OMN SAG 1B4B Ship Maintenance
   total ($11,764M FY25 Enacted) minus the explicit "Ship Maintenance By
   Contract" cost element ($2,228M) leaves $9,535M flowing to public-yard
   labor, supplies, intra-government support, and NWCF reimbursement.
   This figure covers all Navy ships, not just nuclear.
2. The four public naval shipyards (Portsmouth NH, Norfolk VA, Puget
   Sound WA, Pearl Harbor HI) are NWCF activities staffed by federal
   civil servants. Payroll is funded from NWCF; no FPDS record is
   created. See docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md.
3. J044 / K044 / N044 appear at ~$0 because reactor work is contracted
   under ship-level PSC 1905 (HII Newport News, Electric Boat) and PSC
   4470 (Fluor Marine Propulsion, Bechtel Plant Machinery) - not as
   standalone J044 service awards.
4. Sources: FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast
   Guard, 68 services PSCs + newbuild PSCs); FY2026 President's Budget
   (SCN P-1, OMN Vol 1 SAG 1B4B Ship Maintenance OP-5). Data as of April
   2026.

---

### Why this slide (audience motivation)

Slide 2 already gestures at the submarine / nuclear-platform gap in its
right-margin callout ("An estimated ~$4-6B of annual nuclear depot work is
performed in-house at the four public naval shipyards..."). That callout
is correct but soft - the range is an estimate pulled from methodology
notes, not from a named budget line. A diligent reader will ask:

- "What is the exact FY25 figure, and how did you derive it?"
- "If submarine MRO is mostly public-yard, what IS in your $838M
  submarine services slice?"
- "If carrier MRO is mostly RCOH at HII, is CVN RCOH in your Services
  TAM? Under which PSC?"
- "Why is the PSC for nuclear reactor maintenance (J044) empty?"

Slide 5 answers all four questions on one page with figures anchored on
FY2026 President's Budget line items (OMN Vol 1 SAG 1B4B, SCN P-1). The
new workbook sheet `Sub & Carrier Coverage` backs every number with
PIID-level detail and the exact budget-book source lines.

### Build-out assets available in the workbook

The `Sub & Carrier Coverage` sheet in the output workbook provides:

1. Scope reconciliation headline table (the source of the left-bar chart)
2. Budget-book anchor table (the source of the right-side table)
3. Top-15 submarine PIIDs under PSC 1905 (shows Electric Boat Columbia /
   Virginia construction + Bechtel reactor + HII Boise EOH)
4. Top-12 submarine Services MRO PIIDs (Draper Trident, Oceaneering,
   Amentum - what the $838M is actually made of)
5. Top-15 aircraft carrier PIIDs under PSC 1905 (HII CVN-68 inactivation,
   CVN-74 RCOH administrative transfers, CVN-80/81 construction)
6. Top-12 aircraft carrier Services MRO PIIDs (HII PIAs / CIAs at SWRMC,
   CVN-76 DPIA at Puget Sound NSY IMF, husbanding, GD CVN-69 PIA)
7. Top-10 PSC 4470 Nuclear Reactor product rows (Fluor Marine $1.81B)
8. Nuclear Maintenance PSC emptiness table (J044 / K044 / N044)
9. Scope reconciliation notes (plain-English explainer)

### Status

Draft only. Move the ".mockup" content into `DECK.md` as Slide 5 once
the actual slide is designed in Google Slides / PowerPoint and the
screenshot is captured. Delete this file at that point.
