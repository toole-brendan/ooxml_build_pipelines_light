# Slide 11 — Private-Addressable Convergence (module: `private_addressable.py`)

> Breadcrumb: TAM › Private-Addressable Convergence · dual-narrative tiles + callout · `_chart_xml/slide11.xml`

## On-slide claims (verbatim)

- **Takeaway:** "Stripping Public NSY labor from top-down (**$9.51B** private) lands within
  **~6%** of bottom-up FPDS (**$8.97B**), converging at **~$9 to $10B**."
- **Convergence callout:** "A = **$8,971M** / B = **$9,511M** / Delta = **$540M (~6%)**. Within
  ±10% reconciliation target. Residual driven by RDT&E-DW Strategic Systems, AF/Army
  cross-service, and USCG-above-ISVS flows visible in BU FPDS but not in OP-5/MSC/SCN/USCG
  top-down anchors."
- **Narrative A (Bottom-Up / FPDS):** FPDS 65-PSC services universe → **Navy $6,794M + USCG
  $273M = $7,067M** → + PSC 1905 embedded MRO (classifier-derived: **$1,904M**) → **Reconciled
  FPDS MRO TAM: $8,971M**. "All private contractors. Public NSY = $0 by construction."
- **Narrative B (Top-Down / Budget Anchor):** Top-down MRO anchor (slide 08 total) → OMN 1B4B +
  OPN LI 1000 + MSC + SCN + USCG = **$16,996M** → minus Public NSY (4 yards): federal civilian
  workforce **$7,485M** → **Private-addressable TD: $9,511M**. "Captive HII/GDEB complex OH
  retained (addressability is a SAM question)."
- **Footer:** "Source: workbook_build Private Addressable sheet (corrected 2026-04-27);
  Reconciliation sheet TAS-attributed appropriation rollup. Captive HII/GDEB complex OH retained
  inside both numbers …"

## Claim-by-claim sourcing

| Quantity | Value | Source |
|---|---:|---|
| Narrative A: Navy services | **$6,794M** | awards.csv `Is MRO` sum = $6,794.2M (tie-out, `00_INDEX.md`) |
| Narrative A: USCG services | **$273M** | awards.csv = $272.6M |
| Narrative A: services subtotal | **$7,067M** | `navy_tam_svc_cell()` + `cg_tam_svc_cell()` |
| Narrative A: embedded PSC 1905 | **$1,904M** | `model_reconciliation.py` `PSC1905_MRO_EMBEDDED` |
| Narrative A: reconciled TAM | **$8,971M** | `reconciled_mro_tam_cell()` |
| Narrative B: top-down anchor | **$16,996M** | five PB26 anchors (slide 08) |
| Narrative B: less Public NSY | **−$7,485M** | `op5_public_nsy_cell()` |
| Narrative B: private-addressable | **$9,511M** | `model_private_addressable.py` §2 |
| Convergence delta | **$540M (~6%)** | `model_private_addressable.py` §3 `convergence_delta_cell()` |

**This slide is the cleanest proof the workbook is current:** Narrative A's printed numbers
($6,794M + $273M = $7,067M; + $1,904M = $8,971M) reproduce the live `awards.csv` tie-out to the
dollar.

## Reserve facts (could be added)

- **What the ~6% residual is** (and why it's expected): RDT&E-DW Strategic Systems (Draper
  Trident), Air Force / Army cross-service, and USCG-above-ISVS flows are **visible in
  bottom-up FPDS but absent from the five top-down anchors** — the same content as slide 10's
  "Other" row (~$1,520M BU). It pushes A below B, hence A=$8,971M < B=$9,511M.
- **Captive HII/GDEB complex overhaul is *retained* in both numbers.** "Captive" (work a private
  entrant effectively can't contest because it's locked to the SUPSHIP incumbent) is an
  **addressability filter applied at the SAM layer (Phase 2), not at the TAM layer.** So the
  $8.97B / $9.51B private-addressable TAM still includes captive SUPSHIP work; it's removed only
  when deriving SAM.
- **Reconciliation target:** the deck's internal standard is **±10%**; the achieved spread is
  **6%**, so it passes. The convergence band the deck states is **$9–10B**.

## Quotable stats & attributions

- "Two independent methods — FPDS award data (bottom-up) and PB26 budget anchors (top-down) —
  converge at **$9–10B**, within **6%** of each other ($8,971M vs $9,511M)." (deck, slide 11)
- "Navy $6,794M + USCG $273M = $7,067M services-MRO; + $1,904M embedded PSC 1905 = **$8,971M**
  reconciled FPDS-visible TAM." (deck, ties exactly to `awards.csv`)
- "Captive HII/GDEB complex overhaul is retained in TAM and removed only at the SAM layer."
  (deck footer)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard; (2) PB26 budget anchors (OMN OP-5, OPN BA-1 P-40 LI 1000, SCN P-40 LI 2086, USCG Justification); (3) Treasury TAS appropriation attribution

## Caveats / confidence / staleness flags

- **Confidence: high** — Narrative A ties to source data exactly; Narrative B is source-pinned.
- `[!]` **A ($8,971M) and B ($9,511M) are two estimates of the same TAM, not a low/high range of
  a single method.** The headline is the *convergence* (~6%), and the stated band is $9–10B.
- `[!]` This slide is the canonical place where the **$7,067M services layer** and the **$8,971M
  reconciled total** both appear explicitly — use it to settle any "$7B vs $9B" confusion. The
  April methodology docs' "$7,067M" is Narrative A's *first row*, not the TAM.
- Footer "corrected 2026-04-27" — the Private Addressable sheet reflects a post-correction state
  (the OPN LI 1000 substitution and TAS-attributed rollup).
</content>
