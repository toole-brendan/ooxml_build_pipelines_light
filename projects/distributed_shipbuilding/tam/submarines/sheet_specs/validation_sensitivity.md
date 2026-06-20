Sensitivity
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_sensitivity.py

Purpose
The swings that move TAM/SAM: the coefficient ladder, the nuclear-boundary BPMI
exclusion (applied), the resulting TAM impact, and the real P-10 gross AP reference.
None of the sensitivity values are headline.

Reads
- TAM Build           bc_supplier_coeff_cell, ap_lltm_supplier_coeff_cell (the applied
                      coefficients), tam_bc_total_cell(fy) (BC-stream TAM per FY)
- POP Corpus  gate / gfe_excl / confirmed / stream / program ranges +
                      pop_dollar_range + pct_range - the SUMPRODUCT operands behind the
                      coefficient variants
- Assumptions  ap_gross_cell(li, fy) - real P-10 gross AP per LI (2013, 1045) x FY

Feeds
- z_ChartData (CD_A5, via headline_coeff_cell / ap_coeff_cell / sens_tam_cell / gross_ap_cell)
- Accessors: headline_coeff_cell, ap_coeff_cell, delta_cell, sens_tam_cell, gross_ap_cell,
  bc_swing_cell (each -> 'Sensitivity'!C<row>)

On the sheet
(Layout note: §2 ladder is built first so the C-column accessor cells are promoted before §1.
 Coefficient = SUMPRODUCT(mask x $ x (other% + foreign%)) / SUMPRODUCT(mask x $), guarded
 by IF(denominator = 0, "", ...).)

§1  At a glance: the swings
    - Headline supplier coefficient <- TAM Build bc_supplier_coeff_cell        (applied ~35.0%)
    - AP/LLTM reference coefficient <- TAM Build ap_lltm_supplier_coeff_cell   (~48.5%, not applied)
    - Pre-boundary sensitivity TAM $M  <- §2b sens_tam_cell                    (~$42.9B, NOT headline)
    - Real P-10 gross AP $M (reference) <- §2b gross_ap_cell                   (overlaps BC, not additive)

§2  Coefficient ladder (the swings that move TAM/SAM)
    - All-gated POP anchor (not applied) = SUMPRODUCT over gate mask only (drift guard; v4 51.8% anchor)
    - Headline coeff (non-nuclear)  <- TAM Build bc_supplier_coeff_cell  (applied; BPMI excluded ~35.0%)
    - AP/LLTM coeff (reference; base=0) <- TAM Build ap_lltm_supplier_coeff_cell  (~48.5%; not applied)
    - BC - AP/LLTM delta = C(headline) - C(AP/LLTM)   (spread between stream coeffs)
    §2a Nuclear-boundary BPMI exclusion (applied):
        - BC coeff incl. BPMI (sensitivity) = coeff over mask
          gate x confirmed x ((1 - gfe_excl) x (stream = "BC") + (program = "bpmi_nuclear"))
          (pre-boundary ~75.7%, NOT applied)
        - Headline applied (BPMI excluded) <- bc_supplier_coeff_cell  (BPMI is GFE; ~35.0%)
        - BC swing (BPMI removal) = C(incl. BPMI) - C(headline)        (~40.7pt drop)
        - BPMI $ (now GFE-excluded) = SUMPRODUCT(gate x (program = "bpmi_nuclear") x $)
          (naval-nuclear LLTM removed, ~$4.8B)
    §2b TAM impact (headline vs pre-boundary sensitivity; AP base = 0):
        - Headline non-nuclear supplier TAM (cum.) = SUM over FY of N(tam_bc_total_cell(fy))
          <- TAM Build BC stream; AP = $0
        - Pre-boundary sensitivity TAM = headline TAM x (C(incl. BPMI) / C(headline applied))
          (~$42.9B, NOT headline)
        - Real P-10 gross AP (FY22-27, ref) = SUM over (LI in 2013,1045) x FY of
          N(ap_gross_cell(li, fy))  <- Assumptions; overlaps BC -> AP base = 0

§3  Sensitivity guardrails
    - Prose: sensitivity values are NOT headline; the BPMI-included coefficient (~75.7%) is
      not applied; the AP/LLTM coefficient is reference-only while the additive base is zero.
    - Cell notes on the at-a-glance Pre-boundary sensitivity TAM and Real P-10 gross AP rows
      explain why each is reference-only (BPMI is GFE / AP overlaps BC).

Notes
- Native cell notes: 2 -
    §1 (C): pre-boundary sensitivity TAM (~$42.9B) keeps BPMI naval-nuclear inside the coefficient
    §1 (C): real P-10 gross AP is shown only as a reference magnitude; it overlaps Basic Construction
- Note column: none.
