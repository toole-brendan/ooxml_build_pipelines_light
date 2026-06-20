TAM Build
Tab color: 34406B (indigo)  ·  group: Model (TAM/SAM)
Module: model_tam_build.py

Purpose
The TAM calc engine and audit-readable bridge; the true portfolio-TAM producer
(the deck headline and DO-01 source link here, not SAM).

Reads
- SCN Budget          BC base (P-5c Basic Construction), per FY  [scn_cell]
- Assumptions              AP/LLTM base (CY AP) per FY, ship-construction share, AP supplier
                      coeff, BC/AP include toggles; MYP master $ + reconstructed POP %
- POP Corpus          gated / GFE-excl / confirmed / stream / $ / POP-% / MYP-master ranges
                      - the SUMPRODUCT operands behind every coefficient
- Production Schedule  in-window hull count, award FY22-27  [in_window_hull_count]

Feeds
- SAM Build, Executive Summary, Figure Register, z_ChartData, QA Reconciliation, Sensitivity
- Defined name: portfolio_tam (the headline TAM; DO-01 source)
- Producer cells: portfolio / BC-stream / AP-stream TAM, TAM by FY, average-annual TAM,
  supplier-TAM & BC-TAM per hull, BC & AP coefficients, MYP-corrected outside-yards POP,
  all-gated POP site shares, MYP swing, anchor-OK flag

On the sheet
§1  At a glance: headline TAM
    - Same-sheet summary of the §3/§5 producer cells, shown as black derived values (not
      green links - these are this sheet's own outputs): portfolio TAM, BC- and AP/LLTM-
      stream TAM, average-annual TAM, supplier-TAM & BC-TAM per in-window hull, applied
      BC coefficient, AP/LLTM coefficient.

§2  Normalized budget (stream bases, $M FY22-27)
    §2a Include-in-TAM toggles  = Assumptions include_bc / include_ap_lltm (1 = include).
    §2b DDG-51 (LI 2122) stream bases:
        - BC base              <- SCN Budget P-5c, per FY
        - AP/LLTM base         <- Assumptions CY AP, per FY
        - less prior-yr AP credit (input row, default 0 - guards double-count)
        - BC base in TAM       = include_bc x BC_base
        - AP base in TAM       = include_ap x ship_share x (AP_base - PY_credit)
        - TAM base             = BC_in + AP_in           [feeds §5]

§3  Supplier coefficients (dollar-weighted, gated, non-GFE; SUMPRODUCT over POP Corpus)
    in-scope mask = gated x (1 - GFE_excl) x confirmed
    §3a Per-stream coefficients:
        - BC coeff (MYP-corrected) = SUMPRODUCT(BC-mask x $ x (other_US% + foreign%))
                                     / SUMPRODUCT(BC-mask x $)
        - AP/LLTM coeff            <- Assumptions knob (default 0.85; no DDG AP POP corpus
                                     to SUMPRODUCT over)
        - plus total-weighted (display) and BC disclosed-only (masters excluded) variants
    §3b MYP correction view: disclosed-only outside-yards (ARTIFACT ~87%, masters EXCLUDED,
        never present) vs MYP-corrected (~33%, masters folded back); swing = disclosed - corrected.
    §3c All-gated POP site shares - BIW / Ingalls / other-US / foreign / unparsed residual,
        each = SUMPRODUCT(gated x $ x class%) / SUMPRODUCT(gated x $).
    §3d Distributed-production view (appendix): away-from-BIW and outside-both-yards shares.
    §3e Anchor regression: corrected outside-yards vs 0.33 target; OK if |delta| < 0.05.

§4  MYP correction (master reconstruction)
    §4a BIW + Ingalls MYP master awards - $-redacted master $ and reconstructed POP %,
        all <- Assumptions (myp_master_cell / myp_pop_cell); combined master $M row.
    §4b Outside-yards POP: disclosed artifact vs corrected (links §3) + swing row.
    §4c Guardrail prose: travel the POP numbers together; FPDS obligatedAmount + trade-press
        (USNI / Defense Daily) recovery basis; per-hull master allocation is reconstructed.

§5  Model - TAM by fiscal year -> portfolio -> per-hull -> bridge
    §5a TAM by FY  = BC_base x BC_coeff + AP_base x AP_coeff (per stream, then summed),
        with a FY22-27 total column.
    §5b Coefficients applied (live links to §3).
    §5c Portfolio TAM = sum of TAM-by-FY total  [defined name portfolio_tam].
    §5d Average-annual = portfolio / n years (an average, not a run-rate); supplier-TAM-
        per-hull and BC-TAM-per-hull = portfolio (or BC) TAM / in-window hulls (<- Production
        Schedule).
    §5e Bridge components: BC construction base (sum of §2b BC-in) and POP removal
        (prime + co-prime + GFE) = BC base - BC-stream TAM.

Notes
- Native cell notes: 4 -
    §3a (C): applied BC coefficient = MYP-corrected other-US + foreign POP over the non-GFE BC corpus
    §3a (C): AP/LLTM coefficient is an Assumptions-tab input (default 0.85; no DDG AP POP corpus to measure)
    §4a (D): MYP masters are $-redacted; the combined ~$14.58B is reconstructed from FPDS + trade press
    §5d (C): average annual TAM = FY22-27 cumulative / fiscal years (an average, not a run-rate)
- Note column: none.
