# Slide 09 — Top-Down Funnel (module: `topdown_funnel.py`)

> Breadcrumb: TAM › Top-Down Funnel · native stacked-column funnel · `_chart_xml/slide09.xml` + `slide09_chart1.xml`

## On-slide claims (verbatim)

- **Takeaway:** "The PB26 budget anchors **$17.0B** of FY2025 USN/USCG MRO spend; stripping the
  **$7.49B** Public NSY federal-civilian floor leaves **$9.5B** of private-addressable MRO TAM."
- **Chart:** "FY2025 MRO Top-Down Funnel to TAM ($M)" — three stages:
  1. **$17.0B input pool** — OMN 1B4B $11.76B · OPN LI 1000 $2.39B · SCN LI 2086 CVN RCOH
     $1.48B · MSC M&R $1.24B · USCG ISVS $0.12B.
  2. **− $7.49B Public NSY (44% of input)** — "Federal civilian labor at four public yards:
     Norfolk, Portsmouth, Puget Sound, Pearl Harbor. Executed in-house, structurally
     FPDS-invisible."
  3. **= $9.5B private-addressable residual** — "$4.28B OMN 1B4B private availabilities +
     $5.23B non-1B4B anchors (OPN, SCN, MSC, USCG). USN/USCG private-addressable scope.
     Reconciles to bottom-up FPDS on slide 10."
- **Footer:** anchors pinned to PB26 PDFs (OP-5 p.157, MSC p.129, OPN P-40 p.521, SCN P-40
  p.175, USCG p.6); "Public NSY ($7.49B) reflects federal civilian workforce at the four public
  yards, FPDS-invisible by construction."

## Claim-by-claim sourcing

| Stage | Value | Source |
|---|---:|---|
| Input pool | **$16,996M** | five PB26 anchors (see `08_topdown_detail.md`) |
| Less Public NSY | **−$7,484,837K** | `model_op5_navy_topdown.py` `op5_public_nsy_cell()` (Norfolk $1,790M + Portsmouth $1,468M + Puget Sound $2,741M + Pearl Harbor $1,486M) |
| Private-addressable | **$9,511M** | `model_private_addressable.py` §2; `model_tam_bridge.py` private drop-through |

- **$7,485M ÷ $16,996M = 44%.** **$16,996M − $7,485M = $9,511M ≈ $9.5B.**
- Residual decomposition: **$4.28B** OMN 1B4B private availabilities + **$5.23B** non-1B4B
  (OPN $2.39B + SCN $1.48B + MSC $1.24B + USCG $0.12B) = **$9.51B**.

## Reserve facts (could be added)

- **Why Public NSY isn't private-addressable:** it is federal civil-servant labor at the four
  naval shipyards, executed in-house and reimbursed through the **Navy Working Capital Fund
  (NWCF)** — it never becomes a contract a private MRO entrant could win, and it generates **no
  FPDS record** (`research/award_based/docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md`;
  `public_naval_shipyard_revenue.md`).
- **The $7.49B is a floor.** All-in public-yard activity is **$12–15B** once SCN-funded CVN
  RCOH support and OPN ship-alteration work at public yards are added
  (`model_reconciliation.py` `PUBLIC_SHIPYARD_NWCF` note). The funnel strips only the OMN 1B4B
  floor, which is the defensible, source-pinned number.
- **Submarine/carrier understatement on the bottom-up side** is the mirror image: a submarine
  in a 2-year SRA at a public yard burns millions of labor-hours with zero contract data —
  FPDS sees only ~$12M of non-nuclear submarine availability work
  (`METHODOLOGY_CVN_SSN_COVERAGE.md`). The funnel makes that visible by quantifying the public
  floor.
- The **$9.5B top-down private-addressable** is designed to reconcile to the **$8,971M**
  bottom-up FPDS TAM — that hand-off is slides 10–11 (~6% spread).

## Quotable stats & attributions

- "**$17.0B** PB26-anchored MRO − **$7.49B** Public NSY federal-civilian floor (44%) = **$9.5B**
  private-addressable." (deck, slide 09)
- "Public naval shipyard labor is **FPDS-invisible by construction** — federal civil servants
  don't generate contract records." (deck footer; `METHODOLOGY_CVN_SSN_COVERAGE.md`)
- "All-in public-yard activity is **$12–15B**; the $7.49B funnel cut is the OMN 1B4B floor."
  (`model_reconciliation.py`)

## Source line — ready to use

> Sources: (1) PB26 OMN OP-5 Exhibit 1B4B Ship Maintenance (p.157, MSC p.129); (2) PB26 OPN BA-1 P-40 LI 1000 (p.521); (3) PB26 SCN P-40 LI 2086 CVN RCOH (p.175); (4) PB26 USCG Justification ISVS PC and I (p.6)

## Caveats / confidence / staleness flags

- **Confidence: high** — input anchors and the Public NSY cut are published budget lines.
- `[!]` **$9.5B is the *top-down* private-addressable; $8,971M is the *bottom-up* reconciled
  TAM.** They are two estimates of the same thing and converge within ~6% (slide 11). Don't
  treat $9.5B and $9.0B as additive or as a range of one method.
- `[!]` Public NSY cut here ($7.49B) is the **OMN 1B4B floor only**; the all-in $12–15B figure
  is a different (broader) measure — keep them distinct.
</content>
