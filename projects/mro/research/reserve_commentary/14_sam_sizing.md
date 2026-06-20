# Slide 14 — SAM Sizing (module: `sam_sizing.py`)

> Breadcrumb: SAM › SAM Sizing · TAM→SAM funnel tiles + note table · `_chart_xml/slide14.xml` + `slide14_table.xml` · Blank layout, "Preliminary"

## On-slide claims (verbatim)

- **Takeaway:** "Intersecting the Marauder-like fleet with depot ship repair lands **SAM at
  ~$623M**, ~**7% of TAM** and **82% of Marauder-like comp-set MRO**."
- **Funnel tiles:**
  - **MRO TAM** — FY2025 Navy + USCG services obligations. **$8,971M** total.
  - **Depot Ship Repair** — **$4,781M**. 53% of TAM. PSCs J998 (scheduled) + J999 (unscheduled).
  - **Marauder-like Fleet MRO** — **$758M**. 8% of TAM. 14-hull comp-set across all 6 work
    segments (reference).
  - **SAM = $623M** — J998 + J999 depot PSCs only, 14-hull Marauder comp-set.
- **Note table:**
  - SAM = Serviceable Addressable Market: depot ship-repair spend on Marauder-type platforms
    (per Definitions slide).
  - Derivation: FY2025 FPDS obligations, filtered to depot PSCs (J998, J999) **intersected**
    with the 14-hull comp-set. 82% of comp-set MRO lands in depot because MSC auxiliaries book
    scheduled ROH / mid-term availabilities at MSRA yards.
  - **Out of scope:** non-depot work on the comp-set (**$135M**: HM&E, Port & Technical, Combat/
    Electronics/Nuclear); depot work on non-comp-set hulls (**$4,158M**: CVN, DDG, SSN/SSBN,
    other combatants).

## Claim-by-claim sourcing

| Claim | Value | Source |
|---|---:|---|
| MRO TAM | **$8,971M** | `reconciled_mro_tam_cell()` |
| Depot Ship Repair | **$4,781M** (53%) | `model_services.py` §5 / `model_sam_build.py` `core_depot` |
| Marauder Fleet MRO | **$758M** (8%) | `model_sam_build.py` `target_hull` (all segments) |
| **SAM** | **$623M** (~7% TAM, 82% comp-set) | `model_sam_build.py` `target_hull` ∩ depot scenario |

- **The intersection arithmetic ties both ways:**
  - SAM $623M + non-depot comp-set $135M = comp-set **$758M** ✓
  - SAM $623M + depot non-comp-set $4,158M = depot **$4,781M** ✓
- This is the workbook's `target_hull` SAM scenario at the depot cut — a SUMPRODUCT over TAM
  atoms carrying both the `target_hull` flag and the depot work-segment flag (see memory
  `mro-sam-atom-engine`; `model_sam_build.py`).
- SAM definition matches slide 03 ("Depot Ship Repair spend on Marauder-type platforms").

## Reserve facts (could be added)

- **SAM = $623M is the same $623M as slide 13's depot bar** — the deck's two SAM-adjacent slides
  are internally consistent (comp-set depot = SAM).
- The **two "out of scope" buckets** are the most useful reserve detail: they show SAM is a tight
  double-intersection. $4,158M of depot work is real MRO but on hulls outside the comp-set
  (CVN/DDG/SSN/SSBN); $135M is comp-set work outside depot. Neither is in SAM.
- The workbook carries **9 SAM scenarios**; SAM here is the most conservative go-to-market cut
  (`target_hull` ∩ depot). Adjacent scenarios (e.g. `core_depot` = all addressable depot
  $4,781M, `msc_aux`, `uscg_cutter`) are spare framings if a broader SAM is wanted.
- SAM → SOM (Company TCV/ACV) is the next funnel step — **not yet sized** ("Future effort,"
  slide 03).

## Quotable stats & attributions

- "**SAM = $623M** — depot ship repair (J998/J999) on the 14-hull Marauder comp-set; ~7% of the
  $9B TAM, 82% of comp-set MRO." (deck, slide 14)
- "TAM $8,971M → Depot $4,781M (53%) → Marauder comp-set $758M (8%) → **SAM $623M**." (deck funnel)
- "Out of scope: $4,158M of depot work on non-comp-set hulls (CVN/DDG/SSN/SSBN); $135M of
  non-depot comp-set work." (deck note)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard; (2) depot PSCs J998 and J999 intersected with the Marauder-like comp-set

## Caveats / confidence / staleness flags

- **Confidence: high** — the intersection sums reconcile exactly.
- `[!]` Slide carries a **"Preliminary"** chip — SAM is a preliminary sizing, and the next layer
  (Company TCV/ACV capture) is explicitly **future effort**.
- `[!]` The note cites "3 mission-fit tiers (slide 10)" and "comp-set (slide 10)," but the tier
  roster is **slide 12**. Slide-number callouts in the notes are approximate.
- SAM uses the reconciled **$8,971M** TAM as the denominator (so "~7%" is $623M/$8,971M).
</content>
