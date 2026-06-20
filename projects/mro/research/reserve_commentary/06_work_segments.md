# Slide 06 — MRO Work Segments (module: `work_segments.py`)

> Breadcrumb: TAM › Work Segments · native stacked column + coverage table · `_chart_xml/slide06.xml`

## On-slide claims (verbatim)

- **Takeaway:** "Depot ship repair at ~53% and nuclear and complex overhauls at ~21% together
  captured ~75% of FY2025 MRO TAM."
- **Chart caption:** "FY2025 MRO Bottom-Up TAM by Work Segment ($M)" · **Total = $8,971M.**
- **Six segments (share):** Depot Ship Repair **53%** · Nuclear & Complex Overhauls **21%** ·
  Hull, Mechanical & Electrical (HM&E) **10%** · Combat Systems Sustainment **7%** · Port &
  Technical Services **5%** · Electronics & C4ISR Sustainment **4%**.
- **Footer:** "Nuclear & Complex Overhauls includes **embedded MRO on shipbuilding contracts at
  SUPSHIP yards (HII Newport News, Fluor Marine, Bechtel)**, distinct from J998/J999 depot
  repair. Source: FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard. Data as of
  April 2026."

## Claim-by-claim sourcing

Segment shares are dollars ÷ $8,971M reconciled TAM. The dollar values (Frame A obligations)
come from `model_services.py` §5 and `research/award_based/docs/methodology/METHODOLOGY_TAM_FRAMING.md`:

| Segment | FY25 $M | Share of $8,971M | Source |
|---|---:|---:|---|
| Depot Ship Repair | **$4,781M** | 53.3% | `model_services.py` §5; J998/J999 (also slide 14) |
| Nuclear & Complex Overhauls | **$1,904M** | 21.2% | = embedded PSC 1905 (`model_reconciliation.py` `PSC1905_MRO_EMBEDDED`) |
| HM&E | **$938M** | 10.5% | `model_services.py` §5 |
| Combat Systems Sustainment | **$585M** | 6.5% | `model_services.py` §5 |
| Port & Technical Services | **$431M** | 4.8% | `model_services.py` §5 |
| Electronics & C4ISR Sustainment | **$333M** | 3.7% | `model_services.py` §5 |
| **Total** | **$8,971M** | 100% | reconciled FPDS-visible MRO TAM |

- **"Nuclear & Complex Overhauls" IS the embedded PSC 1905 slice** ($1,904M) — engineered
  overhauls, RCOH, and inactivations booked under shipbuilding PSC 1905 at SUPSHIP yards,
  deliberately broken out as its own segment and kept "distinct from J998/J999 depot repair"
  per the footer. Confirmed by `research/psc1905/IMPACT_psc1905_on_workbook_tam.md` §C.

## Reserve facts (could be added)

- **What's inside Nuclear & Complex Overhauls** (top embedded PIIDs, `model_reconciliation.py`
  notes): Electric Boat Special Hull Treatment **Seam Split Repairs $831M**, **USS Boise
  (SSN-764) Engineered Overhaul $424M**, **CVN-68-class inactivation**, **USS Eisenhower
  (CVN-69) FY25 PIA**. SUPSHIP-administered yards: HII Newport News, GDEB/Electric Boat, Fluor
  Marine, Bechtel.
- **Revenue-delivered (Frame B) apportionment by segment** (`METHODOLOGY_TAM_FRAMING.md`) — how
  much of FY25 obligation converts to FY25 revenue: Port & Technical **71%**, Depot **52%**,
  HM&E **39%**, Electronics **31%**, Combat Systems **19%**. Combat Systems is low because of
  multi-year Trident II / AEGIS work (Draper MK7 LE2 alone $318M, >5-yr POP).
- **Coverage-table definitions** (right side of slide, verbatim in `work_segments.py` `_ROWS`)
  are ready-made one-liners for each segment if you need to expand any single bar.

## Quotable stats & attributions

- "Depot ship repair (**53%**) + nuclear & complex overhauls (**21%**) = **~75%** of the
  **$8,971M** FY2025 MRO TAM." (deck, slide 06)
- "Nuclear & Complex Overhauls = **$1,904M** of embedded MRO bundled under shipbuilding PSC
  1905 at SUPSHIP yards — distinct from J998/J999 depot repair." (deck footer + `model_reconciliation.py`)
- "Electric Boat seam-split hull-treatment repairs alone are **$831M**." (`model_reconciliation.py` PSC1905 note)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard; (2) FPDS PSC 1905 shipbuilding awards (embedded MRO at SUPSHIP yards: HII Newport News, Fluor Marine, Bechtel)

## Caveats / confidence / staleness flags

- **Confidence: high.** The five services segments sum to $7,068M (≈ the $7,067M tie-out) and
  the sixth (embedded, $1,904M) lifts the total to exactly $8,971M.
- `[!]` **Denominator is $8,971M, not $7,067M.** In the April methodology framing there were
  only **5** services segments summing to **$7,067M** and **no** "Nuclear & Complex Overhauls"
  segment. The current slide computes shares against the reconciled **$8,971M** and adds the
  embedded segment. Don't mix the two denominators when quoting a percentage.
- `[!]` Presentation choice: the embedded PSC 1905 is shown as its **own** segment here; the
  bridge doc had floated rolling it into Depot. Either is defensible — the slide keeps it
  visible and separate.
</content>
