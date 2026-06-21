---
title: Government-furnished equipment and the team-build pattern
---

# Government-furnished equipment and the team-build pattern

Two distinct procurement patterns in U.S. submarine construction route major dollar flows around the General Dynamics Electric Boat prime contract: **government-furnished equipment (GFE)**, in which the Navy buys equipment under a separate prime contract and ships it to GDEB for installation; and the **team-build pattern**, in which HII Newport News Shipbuilding performs a portion of hull construction under the GDEB prime without appearing as a prime itself. Both patterns mean that significant portions of the SCN-funded outsourced flow are not visible in the GDEB first-tier subaward tree. This chapter describes how each pattern works and what it means for any "outsourced share" measurement built only from GDEB subaward records.

## Government-furnished equipment in submarine construction

In submarine construction, several major component categories are procured by the U.S. Navy under *separate* prime contracts with the producing firm — not by GDEB out of its construction-contract scope. The producing firm ships the completed equipment to GDEB, which installs it during integration. From the perspective of submarine production, the dollars are outsourced (they do not stay at the prime shipyard) but they are **not first-tier subawards of GDEB** because the underlying contract is a separate Navy prime.

The major GFE categories on Virginia-class and Columbia-class submarines, and the firms that hold the corresponding Navy prime contracts, are:[^repo-readme][^repo-sam-prior]

| GFE category | GFE prime contractor | Major PIIDs | Notes |
|---|---|---|---|
| **Naval reactor plant** (S9G reactor on Virginia; generation-after reactor on Columbia) | Bechtel Plant Machinery, Inc. | `N0002419C2114`, `N0002419C2115`, `N0002416C2106`, `N0002424C2114`, plus six other active PIIDs | Naval Reactors / NAVSEA Code 08 customer; stable $1.4–2.2 billion per year of new-money obligation FY18–FY26 |
| **Virginia-class combat system** (hardware/software) | Lockheed Martin | `N0002410C6266` | ~$899M cumulative obligated / $1.37B ceiling |
| **Trident II D5 / D5LE2 strategic weapon** (Columbia) | Lockheed Martin Space | `N0003019C0100`, `N0003020C0100`, `N0003023C0100`, `N0003024C0100`, `N0003020C0101` | Approximately $1.1–1.2 billion per FY-shipset production contract; funded outside SCN |
| **Trident SSBN Material & Kit Additions** | Lockheed Martin | `N0002417C6259` | ~$1.02B cumulative / $1.52B ceiling |
| **AN/BLQ-10 EW and sonar arrays** | Northrop Grumman | mixed | Documented in companion analysis; some scope flows through GDEB subawards rather than as a separate prime |
| **Photonic mast (Type-18 / Type-M1)** | L3Harris Maritime Services (formerly Kollmorgen) | mixed | Most photonic-mast volume is captured inside the GDEB Virginia prime as L3 Technologies subawards rather than as a separate L3Harris prime |

GFE flow does not appear in the USAspending subaward tree of the GDEB Virginia or Columbia prime contracts. It appears, instead, as the producing firm's own prime contracts with the Navy. For a complete measurement of outsourced submarine work, the GFE prime contracts must be added to the GDEB first-tier subaward tree — being careful not to double-count flows that appear in both views.

### Why GFE attribution is structurally ambiguous

When Bechtel Plant Machinery receives a $1 billion Navy prime contract for Columbia reactor components, the work is outsourced from the *Navy's* point of view (in the sense that the Navy is paying a non-government firm to do the work), but it is **not** outsourced from *GDEB's* point of view (GDEB is not paying anyone — the Navy is, on its own contract). Whether the BPMI dollars are counted as "outsourcing by the prime" depends on the choice of denominator:

- If "outsourced" means "the share of the GDEB construction contract that GDEB pays to others," the BPMI dollars are excluded — they were never on GDEB's contract.
- If "outsourced" means "the share of the SCN dollar that goes to anyone other than the assembling yard," the BPMI dollars are included — and represent a major component of the outsourced flow.

The Navy's 30-Year Shipbuilding Plan and other public-facing documentation use language ("outsourcing partners") suggestive of the second framing. This article tracks both views separately:[^repo-readme]

1. **Direct first-tier outsourcing by GDEB** — captured by the GDEB subaward tree, reported in [First-tier subawards and supplier visibility](06-first-tier-subawards.md).
2. **GFE prime spend** — captured by the BPMI, Lockheed Martin, and other GFE-prime vendor sweeps in FPDS, reported in [Procurement and prime contracts](03-procurement-and-contracts.md) and in the per-FY annual roll-up.

Both views are summed in [Annual outsourced flow estimate](08-annual-outsourced-flow.md), with explicit caveats about overlap.

## The HII Newport News team-build pattern

The second pattern is the most opaque feature of submarine industrial-base data. Both Virginia and Columbia are built by a **two-yard team**: General Dynamics Electric Boat (Groton, CT) and HII Newport News Shipbuilding (Newport News, VA). Per the team agreements that have been described in public reporting:[^repo-readme][^repo-lessons-v1]

- **Virginia**: approximately **50/50 work split** between GDEB and HII-NNS.
- **Columbia**: approximately **78/22 work split** with GDEB as the lead yard and HII-NNS as the partner.

In federal procurement data, however, **only GDEB appears as the prime of record** on every SCN 2013 (Virginia) and SCN 1045 (Columbia) construction contract. HII-NNS does not appear as a separate prime on submarine construction. Its work flows *through* the GDEB prime via the team agreement.

This produces four consequences for outsourcing-data interpretation:

1. **A keyword search for `VENDOR_NAME:"NEWPORT NEWS"` looking for submarine prime contracts returns aircraft carrier work.** HII-NNS holds many CVN-78 *Ford*-class construction PIIDs, CVN refueling and complex overhaul (RCOH) PIIDs, and similar carrier work — but essentially no submarine prime contracts (recorded as vendor-of-record). The annual FPDS roll-up for the HII-NNS vendor group shows small negative obligations in most years (de-obligations on carrier contracts that net out small new flows), confirming that submarine-related prime work, as captured by FPDS vendor-of-record, is effectively zero on the HII-NNS line.[^repo-fpds-annual]
2. **A subaward search on the GDEB Virginia primes shows partial HII-NNS visibility.** The legal entity `HUNTINGTON INGALLS INC` appears as a first-tier subaward recipient on the GDEB Virginia Block V/VI master at approximately **$98 million cumulative** across the FY16–FY25 window — vastly less than the ~50% work-share that the team agreement implies for a multi-decade master.[^repo-subaward-top]
3. **Some HII-NNS work may be routed through Northrop Grumman as a flow-through.** Companion analysis flags Northrop Grumman Systems Corporation, which appears as the **second-largest** first-tier subaward recipient on the GDEB Virginia and Columbia primes ($1.27 billion Virginia + $669 million Columbia, $2.21 billion combined across the FY16–FY25 window), as a possible HII-NNS routing channel for some portion of that flow. The data do not allow this to be separated from genuine NG-direct sonar and combat-systems work.[^repo-subaward-top][^repo-lessons-v1]
4. **Public NAVSEA contract announcements occasionally describe modifications as awarded to both GDEB and HII-NNS, even when FPDS records GDEB as the sole vendor of record.** The April 2025 NAVSEA announcement of modifications for FY24 Virginia-class construction, shipyard productivity investments, and nuclear-powered-vessel workforce support named GDEB at approximately $12.4 billion and HII-NNS at approximately $1.3 billion. The April 2025 modification does not appear in this article's FPDS pull as an HII-NNS-vendor-of-record line; the corresponding FPDS records on the GDEB master vehicle list vendor-of-record as `ELECTRIC BOAT CORPORATION`. The press-release framing therefore acknowledges the teaming partner explicitly even when the FPDS recording does not. This is a useful third visibility channel — separate from both the GDEB first-tier subaward tree and the underlying corporate-segment team-build share — that future analyses should track via the NAVSEA / DoD contract announcement stream.

The companion lessons-learned material describes the consequence cleanly: "To see HII's actual share of a sub program, you have to read HII investor filings, not federal procurement data."[^repo-lessons-v1]

### What the team-build pattern means for outsourcing measurement

For the purposes of "outsourced submarine work" measurement, the team-build pattern creates an **understated** outsourced flow when the measurement is built only from federal procurement data:

- HII-NNS work is genuine non-GDEB-yard activity — by definition outsourced from the GDEB perspective.
- But the GDEB subaward tree only shows ~$98 million of HII-NNS work, against an implied workload share that should produce several billion dollars per year of cross-yard flow given the ~50% Virginia and ~22% Columbia split applied to the multi-billion-dollar SCN line items.
- The gap is invisible in federal data and reconstructible only from HII corporate disclosures (10-K segment revenue × analyst estimate of submarine share), which is out of scope for this article.

This article tracks the team-build pattern as a known structural gap rather than attempting to estimate the HII-NNS submarine share. See [Limitations and blind spots](10-limitations-and-blind-spots.md#hii-nns-team-build-share-is-invisible-in-federal-procurement-data).

## Other invisible work in the procurement data

Two additional categories of submarine-related dollar flow are structurally invisible in FPDS and USAspending:

- **Federal naval shipyard depot work.** Norfolk Naval Shipyard (Virginia), Portsmouth Naval Shipyard (Maine), Pearl Harbor Naval Shipyard & IMF (Hawaii), and Puget Sound Naval Shipyard & IMF (Washington) perform depot maintenance, engineered overhauls, and refueling work on Navy submarines. Combined, these four yards employ approximately 36,000 federal workers and consume the bulk of the $6 billion-plus annual Operations and Maintenance, Navy (OMN) submarine sustainment budget. Federal-shipyard work is federal payroll and federal materiel procurement (which appears in FPDS but under generic Defense Logistics Agency descriptions); the labor and overhead component is invisible. This is excluded from the "outsourced" definition by design — federal-employee work is not outsourcing — but is called out in [Limitations and blind spots](10-limitations-and-blind-spots.md).[^repo-lessons-v1]
- **Classified payload modules.** Intelligence-community modules carried on submarines (for example, the historical SSGN special-operations payload extensions and certain classified surveillance equipment) are procured outside the public SCN appropriation. These are invisible in FPDS by design and are excluded from the visible flow.[^repo-readme]

A third category — **work performed by federally-funded research and development centers (FFRDCs)** such as Penn State University Applied Research Laboratory, Johns Hopkins University Applied Physics Laboratory, and MIT Lincoln Laboratory — appears partially in federal procurement data through specific Navy task orders. Examples from the Columbia program include `N0002419F8435` (Penn State ARL, Columbia Class Propulsor & Shafting Support FY19–22, $18M), `N0001423C1015` (Applied Physical Sciences Corp, Navy Supporting Tech for Virginia & Columbia, $18M), and `N0002423F8296` (JHU APL Columbia Class Testing Program, $8M).[^repo-sam-prior] FFRDC task orders appear in the relevant prime sweeps but are small relative to the dominant flows.

## How this article handles the dual-prime question

The "Annual outsourced flow estimate" in this wiki ([chapter 8](08-annual-outsourced-flow.md)) presents a combined view that adds:

- **First-tier subawards visible in USAspending** on the GDEB submarine prime PIIDs (the direct measure of GDEB's first-tier outsourcing), and
- **GFE prime spend in FPDS** for BPMI naval-reactor procurement (the most stable and clearly attributable GFE flow).

Trident II D5 / D5LE2 production, Virginia combat systems, and other GFE categories are *not* added into the headline combined number to avoid double-counting against the SCN top-line — Trident is funded outside SCN, and Virginia combat systems appear in both the LM prime and (potentially) in the GDEB Electronics cost-category line in the SCN P-5c. They are reported separately in [Procurement and prime contracts](03-procurement-and-contracts.md).

HII-NNS team-build dollars are **not** included in the headline because they are not measurable from the visible data. The article flags the team-build share as a known understatement of true outsourced flow rather than estimating it.

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^repo-sam-prior]: SAM Submarine & Cutter Contract Awards (April 2026). See full citation under [References](INDEX.md#references).

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).

[^repo-fpds-annual]: submarine_outsourced_work, "extracted/fpds_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-subaward-top]: submarine_outsourced_work, "extracted/subaward_top_recipients.csv." See full citation under [References](INDEX.md#references).
