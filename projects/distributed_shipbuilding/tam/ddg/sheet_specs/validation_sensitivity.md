Sensitivity
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_sensitivity.py

Purpose
Shows how the headline moves with the key levers: the supplier-coefficient
ladder, the MYP redaction swing, and the AP/LLTM knobs. A validation tab, not an
inputs tab: editable knobs stay on Assumptions; this sheet only LINKS to them (pure
assumption links green, derived sensitivities black).

Reads
- TAM Build   BC coeff (applied + disclosed-only), outside-yards corrected/disclosed,
              portfolio / BC- / AP-stream TAM  [bc_supplier_coeff_cell,
              bc_supplier_coeff_disclosed_cell, outside_yards_corrected_cell, ...]
- Assumptions      ship-construction share of CY AP, AP/LLTM supplier coeff (editable knobs)
              [ap_ship_construction_share_cell, ap_supplier_coeff_cell]
- POP Source Audit   MYP masters $, gated corpus $  [masters_dollar_cell, gated_dollar_cell]

Feeds
- none (read-only sensitivity leaf; producer: SENSITIVITY SheetEntry)

On the sheet
§1  Coefficient ladder (BC coeff vs all-gated outside-yards POP)
    - BC supplier coeff (applied, MYP-corrected)  <- TAM Build (%); other-US + foreign
      over non-GFE BC corpus incl. masters.
    - Outside-yards POP, MYP-corrected  <- TAM Build (%); all-gated, masters folded back (~33%).
    - Outside-yards POP, disclosed (ARTIFACT)  <- TAM Build (%); masters excluded - DO NOT HEADLINE.

§2  MYP swing (the headline lever) - editable on Assumptions
    - Outside-yards swing = disclosed - corrected (= C{disc} - C{corr})  (the redaction-artifact magnitude).
    - MYP masters $M (reconstructed)  <- POP Source Audit (~$14.58B BIW + Ingalls).
    - Masters as % of gated corpus $ = masters $ / gated $  <- POP Source Audit (how much the
      reconstruction carries).

§3  TAM sensitivity (MYP adjustment effect: corrected vs disclosed-only coeff)
    - Portfolio TAM (applied, MYP-corrected)  <- TAM Build (BC base x corrected BC coeff).
    - Portfolio TAM (disclosed-only BC coeff) = applied TAM x (disclosed BC coeff / applied BC coeff)
      <- TAM Build (what TAM reads if the $14.58B masters were NOT reconstructed).
    - MYP adjustment uplift on TAM = applied TAM - disclosed-only TAM (the masters'
      supplier-POP slice added back; the single largest lever - cell note).
    - Memo: masters' embedded content @ 42% band = masters $ x 0.42  <- POP Source Audit
      (content-lens view, POP-invisible).
    - FFATA-visible floor caveat (prose, cell note): FFATA subawards ~15% of true
      yard-side flow; a coverage floor used to seed bucket shares, not the TAM denominator.

§4  AP/LLTM stream (Phase 3) - editable knobs + BC/AP split
    - Ship-construction share of CY AP  <- Assumptions (%); non-GFE EOQ fraction.
    - AP/LLTM supplier coefficient      <- Assumptions (%); supplier POP share assumption.
    - AP/LLTM stream TAM ($M)           <- TAM Build (CY AP x share x coeff).
    - AP/LLTM share of portfolio TAM = N(ap_tam) / (bc_tam + N(ap_tam))  <- TAM Build
      (how much of the headline TAM is the AP/LLTM stream).

Notes
- Native cell notes: 1 -
    §3 (C): MYP-adjustment sensitivity = the TAM the masters' supplier-POP slice adds back vs disclosed-only
- Note column: none.
