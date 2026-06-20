# Slide 03 — Definitions (module: `definitions.py`)

> Breadcrumb: TAM › Definitions · Layout: slideLayout4

## On-slide claims (verbatim)

- **Takeaway:** "Sizing breaks the MRO market down into five levels."
- **Five nested rings (outer → inner):** Total Funding · TAM · SAM · Company TCV · Company ACV.
- **Level / Definition table:**
  | Level | Definition |
  |---|---|
  | Total Funding | "All Service-PSC code award spending for US Navy and US Coast Guard in FY2025" |
  | Total Addressable Market (TAM) | "Funding for MRO-type service codes" |
  | Serviceable Addressable Market (SAM) | "Depot Ship Repair spend on Marauder-type platforms" |
  | Company TCV | "Share of SAM that Saronic can likely capture" — *greyed, "Future effort"* |
  | Company ACV | "Portion of TCV exercised through Growth and Programs action" — *greyed, "Future effort"* |

## Claim-by-claim sourcing

| Level | Live value behind it | Where it comes from |
|---|---|---|
| Total Funding | The full FPDS Service-PSC award universe for USN+USCG FY2025 (the **2,539-PSC** base on slide 04) | FPDS-NG PSC manual (workbook `sources_references.py` CITE-04); `data_awards.py` |
| TAM | **$8,971M** reconciled FPDS-visible MRO TAM ("$9.0B") = services $7,067M + embedded PSC 1905 $1,904M | `model_reconciliation.py` → `reconciled_mro_tam_cell()`; tie-out in `00_INDEX.md` |
| SAM | **$623M** = depot ship repair (PSCs J998/J999) on the 14-hull Marauder comp-set (~7% of TAM) | `model_sam_build.py` `target_hull` scenario; deck slide 14 (`slide14.xml`) |
| Company TCV / ACV | Unsized — "Future effort" | Not modeled; company-capture share is Phase-2 work |

- The five-level ladder is the deck's rendering of the workbook's two-universe TAM/SAM framing
  documented in `workbook_mro/sheets/guide_methodology.py` §1 (Definitions) and §2 (Formula
  framework), and `research/award_based/docs/methodology/sam_methodology.md`.
- "Saronic" is the **company**; "Marauder" is its platform — a 180-ft ASV with a 150MT modular
  deck (see slide 12, `slide12_table.xml`). "Marauder-type platforms" = the 14-hull comp-set
  defined on slide 12.

## Reserve facts (could be added)

- **Dollar anchors per level** if you want to put numbers on the rings: Total Funding = the
  ~$ Service-PSC universe (slide 04 funnel head, 2,539 PSCs); TAM = **$8,971M** ($9.0B);
  SAM = **$623M** (~7% of TAM, 82% of comp-set MRO); TCV/ACV = future effort.
- The workbook actually models **nine** SAM "scenarios" (`taxonomy_mro.py` `SCENARIO_SPEC`;
  `model_sam_build.py`) — `broad_tam`, `broad_addressable`, `core_depot`, `regional_yard`,
  `uscg_cutter`, `msc_aux`, `technical_services`, `electronics_c4isr`, and `target_hull`. The
  SAM drawn on this slide is the **`target_hull`** scenario (Marauder comp-set ∩ depot ship
  repair). The slide picks the most defensible single cut; the others are spare framings.
- `guide_methodology.py` §1 also defines **SOM** (Serviceable Obtainable Market) below SAM —
  the deck's "Company TCV/ACV" rings are the SOM layer under a go-to-market label.
- Between Total Funding and TAM sits an intermediate the deck compresses: the **services-only**
  layer ($7,067M) before the embedded-PSC-1905 addback ($1,904M). See slide 04 / slide 11.

## Quotable stats & attributions

- "Sizing breaks the MRO market into five levels: Total Funding → TAM → SAM → Company TCV →
  Company ACV." (deck, slide 03)
- "TAM = funding for MRO-type service codes; SAM = depot ship-repair spend (J998/J999) on
  Marauder-type platforms." (deck definitions, consistent with `guide_methodology.py` §1)
- TAM **$8,971M**; SAM **$623M** (~7% of TAM). (`reconciled_mro_tam_cell()`; slide 14)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard; (2) PB26 budget anchors (OMN OP-5, OPN BA-1 P-40, SCN P-40, USCG Justification)

## Caveats / confidence / staleness flags

- **Confidence: high** on TAM ($8,971M, tie-out exact) and SAM ($623M, deck slide 14).
- **TCV/ACV are intentionally unsized** ("Future effort") — do not quote a capture figure.
- **Layer note:** "TAM = MRO-type service codes" is the reconciled $8,971M, which *includes*
  the $1,904M embedded PSC 1905 addback — not the services-only $7,067M. Keep that straight if
  someone asks "is TAM $7B or $9B?" → it's $9.0B reconciled (see `00_INDEX.md`).
- No `$1,660M`-era figures appear on this slide; it is definitional, so low staleness risk.
</content>
