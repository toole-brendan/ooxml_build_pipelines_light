# Public Naval Shipyard Revenue -- FY2025 Direct Sourcing

**Headline:** $7.5B in FY2025 OMN Ship Maintenance transfers flowed
directly to the four public naval shipyards (Norfolk, Portsmouth,
Puget Sound, Pearl Harbor). This is a floor on total public-yard
activity; SCN (CVN RCOH and SSN major-life-cycle work), OPN (ship-alt
/ install work during availabilities), and RDT&E customer orders add
additional workload that is not cleanly isolated in the OMN exhibit.

**Purpose:** Replace the "Size: pending" placeholder in Slide 3
top-right cell ("Public-yard labor") of `deck/MRO_DECK_v1.5_
RECONCILIATION_SPEC.md` with a direct, defensible, citable number.
Replace the suspect v1.3 derivation (OMN 1B4B total $11,764M less
CE-928 Ship Maintenance by Contract $2,228M = $9,535M) which was
conceptually wrong (the non-CE-928 remainder includes private-yard
availability funding, not just public-yard labor).

## Source

**Primary exhibit:** OMN Exhibit OP-5, 1B4B "Ship Maintenance"
(Page 8 of 29) -- FY2026 President's Budget Submission, Department of
the Navy, Operation and Maintenance, Navy. Budget Activity: Operating
Forces. Activity Group: Ship Operations. Detail by Subactivity Group:
Ship Maintenance.

Extracted from `sources/OMN_Book.txt` lines 5614-5618.

**Table heading:** "Navy-wide Ship Maintenance Support (1B4B) --
Transferred via RRN". RRN = Reimbursable Work Request Number; these
are customer-order transfers from the OMN appropriation into the
public naval shipyards' working-capital activities for execution of
the planned maintenance workload.

## Four public shipyards -- FY2024 actual, FY2025 enacted, FY2026 PB

All figures in thousands of dollars ($K).

| Shipyard                      | FY24 Actual | FY25 Enacted | FY26 PB    |
|-------------------------------|------------:|-------------:|-----------:|
| Norfolk (NNSY)                |   1,702,115 |    1,789,606 |  1,775,132 |
| Portsmouth (PNSY)             |   1,317,076 |    1,468,055 |  1,401,503 |
| Puget Sound (PSNSY)           |   2,544,027 |    2,741,203 |  2,944,801 |
| Pearl Harbor (PHNSY)          |   1,394,013 |    1,485,973 |  1,656,378 |
| **TOTAL Four Shipyards**      | **6,957,231** | **7,484,837** | **7,777,814** |
| Total OMN 1B4B Ship Maint     |  11,501,126 |   11,763,594 | 13,803,188 |
| Shipyard share of 1B4B        |       60.5% |        63.6% |      56.3% |

**Cited in deck: $7.5B (FY2025 OMN transfers to public shipyards).**

## What this number captures

1. Civilian federal workforce at the four public shipyards executing
   OMN-funded depot availabilities -- primarily nuclear work (SSN
   EDSRA/DSRA/DMP, SSBN mid-life, SSGN, CVN PIA/DPIA/SRA). See
   reconciliation-of-increases text at OMN_Book.txt lines 5497-5561
   for specific FY26 inductions by shipyard:
     - PHNSY: USS INDIANA (SSN 789) EDSRA; USS MISSOURI (SSN 780)
       DMP; USS SPRINGFIELD (SSN 761) DSRA.
     - PSNSY: USS KENTUCKY (SSBN 737); USS ABRAHAM LINCOLN (CVN 72)
       DPIA; USS CARL VINSON (CVN 70) PIA; USS GEORGE WASHINGTON
       (CVN 73) SRA; USS MICHIGAN (SSGN 727).
     - PNSY: USS NEW MEXICO (SSN 779) DMP; USS ALBANY (SSN 753) DSRA.
     - NNSY: USS GERALD R. FORD (CVN 78) PIA.
2. Base operating support for shipyard facilities, tooling, and
   infrastructure.
3. Materials and non-labor costs associated with OMN-funded
   availabilities at public yards.

## What this number does NOT capture

1. **SCN funding flowing to public shipyards.** Major-life-cycle
   events -- CVN Refueling Complex Overhaul (RCOH), SSN Engineered
   Overhaul (EOH), CVN / SSN inactivation -- are funded through SCN
   (Shipbuilding and Conversion, Navy), not OMN. From earlier
   session research: SCN Line Item 2086 "CVN Refueling Overhauls"
   FY25 Enacted = $6,271M. A portion of this flows to Norfolk
   Naval Shipyard for CVN-73 George Washington RCOH support;
   another portion flows to HII Newport News (private yard) for
   CVN-74 John C. Stennis RCOH. The split is not directly readable
   from public exhibits.

2. **OPN funding for ship-alt and equipment installs during
   availabilities.** BA-7 (Personnel and Command Support Equipment)
   funds modernization and C4ISR installation work performed during
   depot availabilities. Some portion of this OPN work is executed
   in-house at public shipyards (NAVSEA engineering, combat-system
   integration). Size: unresearched.

3. **RDT&E customer orders.** Naval Surface / Undersea Warfare
   Centers place orders with the shipyards for test & evaluation
   activities. Size: small (likely sub-$500M Navy-wide across
   shipyards); unresearched.

4. **OPN BA-8 spares and repair parts** consumed during public-yard
   availabilities. These are procurement accounts but support MRO
   execution; they transfer through the Navy supply system rather
   than as direct transfers to shipyards.

## Total public-yard activity -- bounded estimate

| Source                                   | FY25 $B |
|------------------------------------------|--------:|
| OMN 1B4B Ship Maintenance (direct, this doc) |   $7.5 |
| SCN Line 2086 CVN RCOH (portion to NNSY)  |  ~$2-3 |
| SCN nuclear sub depot work (portion to PHNSY/PSNSY/PNSY) |  ~$1-2 |
| OPN ship-alt / install at public yards   |  ~$1-2 |
| RDT&E customer orders                    |  ~$0.5 |
| **Total public-yard revenue (FY25)**     | **~$12-15B** |

The $7.5B OMN number is the single defensible direct cite. The
$12-15B total includes approximate bounds on non-OMN sources and
is less directly sourced.

## Correction to the old $9.5B derivation

The v1.3 spec derived a $9,536M "implied public-yard labor" figure
as `OMN 1B4B Total ($11,764M) - OMN 1B4B CE-928 Ship Maintenance By
Contract ($2,228M)`. This derivation was **conceptually wrong**:

- The correct interpretation of the residual is not "public-yard
  labor" but "everything in 1B4B except the `Ship Maintenance By
  Contract` cost element." That residual includes:
  - Direct transfers to the four public shipyards ($7.5B per this
    doc)
  - Non-depot / Intermediate Maintenance (IL) performed at Regional
    Maintenance Centers ($1,429M per FY25 enacted)
  - Availability categories executed at public OR private yards
    (OH, SRA, SIA, PIA, CIA, ORATA, ERATA, CM = $2.2B aggregate)
  - Minus overlaps / carry-in / reconciliation adjustments

- The $9.5B residual is therefore larger than the actual public-yard
  transfer ($7.5B) because it double-counts some private-yard OMN
  availability work.

**Correction to v1.5:** replace footnote (1) of Slide 3 and the
top-right cell size note with the direct $7.5B OMN transfer figure.
Remove the OMN 1B4B minus CE-928 derivation from the footnote (it
was wrong). Add the $12-15B total bound as a secondary footnote for
readers asking "what's the total public-yard footprint?"

## Recommended v1.5 edits

**Slide 3 -- Top-right cell ("Public-yard labor")**:

Replace:
> Civilian federal workforce at Portsmouth, Norfolk, Puget Sound,
> Pearl Harbor. NWCF-funded; no FPDS record. Size: pending direct
> NWCF sourcing (see research below).

With:
> Civilian federal workforce at Norfolk, Portsmouth, Puget Sound,
> Pearl Harbor. OMN-funded via reimbursable transfer (RRN); no
> FPDS record. FY2025: $7.5B OMN transfers to the four yards
> (floor). Estimated $12-15B total with SCN / OPN / RDT&E customer
> orders added.

**Slide 3 -- Footnote (1)**:

Replace:
> Public-yard cell: $[direct NWCF number] for FY2025, sourced to
> [NWCF exhibit]. As an interim bound while direct sourcing is
> pending: OMN SAG 1B4B less CE-928 implies ~$9.5B (suspect -- see
> research); bottom-up from ~35-40k FTE at public shipyards at
> fully-loaded labor rates gives ~$5-8B labor-only.

With:
> Public-yard cell: $7.48B in FY2025 OMN transfers to the four
> public naval shipyards, sourced to OMN Exhibit OP-5, 1B4B
> (FY2026 President's Budget Submission, Page 8 of 29) --
> Norfolk $1,790M, Portsmouth $1,468M, Puget Sound $2,741M, Pearl
> Harbor $1,486M. Total public-yard activity (including SCN-funded
> CVN RCOH / SSN EOH / inactivation work, OPN-funded ship-alts,
> and RDT&E customer orders) estimated $12-15B. See
> docs/methodology/public_naval_shipyard_revenue.md.

## Confidence and caveats

1. **High confidence on the $7.5B direct number.** It is a single
   line-item read from the OMN justification book, not a derived
   figure. Shipyard-by-shipyard totals are given and they sum to
   the cited figure.

2. **Medium confidence on the $12-15B total bound.** The SCN RCOH
   share going to public vs private yards is not directly split
   in public exhibits. OPN ship-alt volume at public yards is
   estimated from availability-count intuition, not a direct
   cite.

3. **Low confidence that this is "NWCF-funded".** The four public
   shipyards receive OMN appropriation funds via RRN customer-
   order transfers. They are industrial-fund (working-capital-
   type) activities internally, but the appropriation color is
   OMN, not NWCF. The v1.5 top-right cell label should be
   updated from "NWCF-funded" to "OMN-funded (direct transfer)"
   or "appropriated-fund industrial activity".

## Source data

Lines 5608-5618 of `sources/OMN_Book.txt`:

```
Non-depot / Intermediate Maintenance (IL)  -  1,497,600  -  1,517,398  -  -  -  1,429,333  -  -  1,525,270
Navy-wide Ship Maintenance Support (1B4B) -- Transferred via RRN
Norfolk Naval Shipyard (NNSY)     9  1,635,116  5  1,702,115  -  -  3  1,789,606  3  2  1,775,132
Portsmouth Naval Shipyard (PNSY)  2  1,191,581  3  1,317,076  -  2  3  1,468,055  1  2  1,401,503
Puget Sound Naval Shipyard (PSNSY)  9  2,521,756  5  2,544,027  -  2  9  2,741,203  1  7  2,944,801
Pearl Harbor Naval Shipyard (PHNSY)  6  1,237,273  4  1,394,013  -  -  1  1,485,973  3  3  1,656,378
TOTAL                            59  11,164,248  45  11,501,126  8  16  44  11,763,594  20  30  12,219,188
```

Column interpretation (from table headers at lines 5596-5599):
- FY 2024 President's Budget: Qty, $K
- FY 2024 Actual Inductions: Qty, $K (these are the FY24 actuals)
- FY 2025 Completions: Pri Yr Qty, Cu Yr Qty (just counts, no $)
- FY 2025 Current Budget: Qty, $K (these are the FY25 enacted)
- FY 2025 Carry-In: Qty
- FY 2026 President's Budget: Qty, Qty (from prior year FY25), $K

Generated: 2026-04-20 (walk-in build session for v1.5 deck).
