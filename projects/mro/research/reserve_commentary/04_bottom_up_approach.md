# Slide 04 — Bottom-Up Methodology (module: `bottom_up_approach.py`)

> Breadcrumb: TAM › Bottom-Up Approach · content transcribed from `_chart_xml/slide04.xml` + `slide04_table.xml`

## On-slide claims (verbatim)

- **Takeaway:** "Filtering FPDS contract-award data from **2,539 federal PSCs** down to **65
  ship-MRO services codes** sizes the FY2025 Navy and Coast Guard MRO contracting TAM at
  **$9.0B**."
- **Funnel (Input → Filter → Output):**
  1. **2,539 PSCs** — "All federal contract-action codes" → *filter:* USN/USCG services codes
     (J, K, N, H, L, M families) → **~1,800 Services PSCs**
  2. **~1,800 Services PSCs** → *filter:* Ship MRO codes (Repair, modification, overhaul,
     husbanding) → **65 Ship MRO PSCs**
  3. **65 Ship MRO PSCs** → *apply* FY2025 obligations → **FY2025 MRO TAM: $9.0B**
- "FPDS Atom Feed, post-FMS carve-out."
- **Footer:** "Source: FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard (65
  ship-MRO PSCs). Data as of April 2026."

## Claim-by-claim sourcing

| Claim | Source / how derived |
|---|---|
| 2,539 federal PSCs | FPDS-NG Product/Service Code manual (`sources_references.py` CITE-04, fpds.gov) |
| ~1,800 services PSCs (J/K/N/H/L/M) | Services-class PSC families; `_crosstab.py` PSC definitions |
| 65 ship-MRO PSCs | `data_awards.py` / SRC-01: "65 J/K/N/M/H/L MRO PSCs … with an Is MRO flag" |
| **$9.0B** TAM | Reconciled FPDS-visible MRO TAM **$8,971M** = services **$7,067M** + embedded PSC 1905 **$1,904M** |
| post-FMS carve-out | FMS removed from addressable scope (`inputs_assumptions.py` FMS plug −$100M; `mro_tam_exclusions.md` FMS $86M) |

- **The $7,067M services figure ties exactly to source data.** Summing `Is MRO == TRUE`
  FY2025 obligations in `workbook/extracted/awards.csv`: Navy **$6,794.2M** + Coast Guard
  **$272.6M** = **$7,066.9M** (see `00_INDEX.md` tie-out). Add the classifier-locked
  embedded **$1,904M** (`model_reconciliation.py` `PSC1905_MRO_EMBEDDED`) → **$8,971M** = "$9.0B".

## Reserve facts (could be added)

- **Exclusion ladder** (`research/award_based/docs/methodology/mro_tam_exclusions.md`): the raw
  MRO-PSC universe is **$8,769M**; **$1,702M (19.4%)** is excluded to reach the $7,067M
  services TAM —
  - Cross-platform engineering IDIQs **$500M** (SeaPort-NxG $379M, Cyber $72M, …)
  - Aviation MRO **$376M** (NAWC, FRC, NAVAIR)
  - Shore-base facilities **$323M** (ATFP/security, NAVFAC)
  - Non-Navy / non-ship **$224M** (Army watercraft, JCREW, USACE dredge, USMC)
  - LLM-flagged non-ship-MRO **$151M**; FMS **$86M**; inactive/decommissioned **$42M**.
- **Why awards, not budget** (`research/award_based/docs/research/WHY_PSC_DATA.md`): PSC awards
  give per-contract vendor/hull granularity that budget exhibits can't. External validation:
  GD's FY2025 10-K "repair and other services" = **$1,183M** vs the workbook's bottom-up GD
  consolidated services TAM **$939M** — same order of magnitude.
- **Obligations vs revenue (Frame A vs Frame B)** (`METHODOLOGY_TAM_FRAMING.md`): the deck uses
  **Frame A** (FY25-dated obligations = contracting activity, $7,067M services). **Frame B**
  (POP-apportioned revenue actually delivered in FY25) is **~$3.3–3.8B (~49%)** — useful if
  someone asks "how much revenue is actually recognized this year."

## Quotable stats & attributions

- "2,539 federal PSCs → ~1,800 services PSCs → 65 ship-MRO PSCs → **$9.0B** FY2025 USN+USCG MRO
  contracting TAM." (deck, slide 04)
- "**$1,702M (19.4%)** of the raw MRO-PSC universe is excluded (aviation, shore-base, FMS,
  cross-platform IDIQs, non-ship)." (`mro_tam_exclusions.md`)
- "GD 10-K repair & services $1,183M vs model $939M — same order of magnitude." (`WHY_PSC_DATA.md`)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard (65 ship-MRO PSCs); (2) FPDS-NG Product/Service Code catalog

## Caveats / confidence / staleness flags

- **Confidence: high** on $7,067M (exact tie-out) and $9.0B (reconciled).
- `[!]` **PSC count 65 vs 68.** The deck says **65** ship-MRO PSCs; the April research
  (`METHODOLOGY_TAM_FRAMING.md`, `mro_tam_exclusions.md`) says **68 services PSCs**. The
  reconciliation note is `research/deck_specs/domnann_deck/PSC_COUNT_NOTE.md` — quote the deck's
  **65** for consistency with the current build.
- `[!]` **The 3-step funnel literally yields the $7,067M services layer; the on-slide "$9.0B"
  already includes the +$1,904M embedded PSC 1905 reconciliation step.** The bridge doc
  `research/psc1905/IMPACT_psc1905_on_workbook_tam.md` §B recommended showing the embedded
  addback as an explicit 4th funnel row. If asked "does 65 PSCs × obligations = $9.0B?" — no;
  65 PSCs = $7.07B, and the embedded PSC 1905 addback lifts it to $9.0B.
- FMS treatment differs slightly by source (workbook plug −$100M vs measured $86M); immaterial.
</content>
