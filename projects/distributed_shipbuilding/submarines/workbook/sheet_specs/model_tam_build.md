TAM Build
Tab color: 34406B (indigo)  ·  group: Model (TAM/SAM)
Module: model_tam_build.py

Purpose
The TAM calc engine and bridge across both ship classes (Virginia + Columbia);
produces portfolio TAM and the annualized deck-bridge figures. Two streams (BC +
AP/LLTM), per-stream $-weighted POP supplier coefficients, then the portfolio bridge.

Reads
- SCN Budget           BC base (P-5c Basic Construction) per class/FY  [scn_cell(li, fy, 'basic')]
- POP Corpus   gate / GFE-excl / confirmed / stream / $ / POP-% ranges - the
                       SUMPRODUCT operands behind every coefficient  [gate_range, gfe_excl_range,
                       confirmed_range, stream_range, pop_dollar_range, pct_range]
- Assumptions  AP/LLTM additive base (confirmed 0) per class/FY [ap_lltm_base_cell],
                       BC / AP-LLTM include toggles, n_years count formula

Feeds
- Methodology, SAM Build, z_ChartData, Figure Register, Slide Data,
  Executive Summary, QA Reconciliation, Sensitivity
- Producer cells: per-class & portfolio TAM by FY, BC-stream & AP/LLTM-stream TAM,
  cumulative portfolio TAM, average-annual TAM, n_years, cumulative BC base, POP removal,
  per-stream supplier coefficients (BC / AP-LLTM / total-weighted), distributed-view
  coeffs (low / high), primary all-gated coeff, anchor-OK flag, per-class stream bases
- Exports FY_COLUMNS (consumed by the register / validation tabs)

On the sheet
§1  At a glance: headline TAM
    - Same-sheet summary of the §3/§4 producer cells: cumulative portfolio TAM (FY22-27),
      average annual portfolio TAM (= cumulative / n_years), applied BC supplier coefficient
      (~35.0%, non-nuclear, BPMI excluded), AP/LLTM reference coefficient (~48.5%, not applied
      because base = 0). Note: AP/LLTM coeff is reference-only since the AP/LLTM additive base is $0.

§2  Budget normalized (two TAM stream bases per class/FY, $M FY22-27)
    §2a Applied stream toggles  <- Assumptions (1 = include):
        - Include BC stream      = include_bc_stream_cell
        - Include AP/LLTM stream = include_ap_lltm_stream_cell
    §2b Virginia (LI 2013) stream bases / §2c Columbia (LI 1045) stream bases, each:
        - BC base (P-5c)         <- SCN Budget scn_cell(li, fy, 'basic'), per FY
        - AP/LLTM base (P-10)    <- Assumptions ap_lltm_base_cell (confirmed 0), per FY
        - less prior-yr AP credit  = 0 (input row; guards double-count)
        - BC base in TAM         = IF(BC_raw=0,"", include_bc x BC_raw)
        - AP/LLTM base in TAM    = IF(AP_raw=0,"", include_ap x (AP_raw - PY_credit))
        - TAM base               = N(BC_in) + N(AP_in)
    §2d Portfolio stream-base totals (Va + Col) = per-metric N(Va) + N(Col), per FY
        (BC base in TAM, AP/LLTM base in TAM, TAM base). Promotes bc_base_cell, ap_lltm_base_cell,
        tam_base_cell, portfolio_bc_base_cell.

§3  POP coefficients (per-stream TAM supplier coefficients; SUMPRODUCT over POP Corpus)
    in-scope mask = gate x (1 - GFE_excl) x confirmed
    coeff(mask)   = IF(den=0,"", SUMPRODUCT(mask x $ x (other% + foreign%)) / SUMPRODUCT(mask x $))
    share(which)  = IF(den=0,"", SUMPRODUCT(gate x $ x which%) / SUMPRODUCT(gate x $))
    §3a Per-stream supplier coefficients (feed §4):
        - Headline BC coefficient (applied)  = coeff(in-scope x stream="BC"); construction +
                                               component_procurement, GFE + BPMI nuclear dropped (~35.0%)
        - AP/LLTM coefficient (reference)    = coeff(in-scope x stream="AP_LLTM"); ~48.5%, not applied
        - Total weighted (corpus, display)   = coeff(in-scope); both streams, not base-weighted
    §3b All-gated POP shares (dollar-weighted building blocks): EB site % (prime, not addressable),
        HII site % (co-prime), other-US supplier %, foreign %, unparsed % = 1 - eb - hii - other - foreign.
    §3c Distributed-production view (appendix): distributed-confirmed = hii + other + foreign (~68%);
        distributed-incl-unparsed = 1 - eb (~78%).
    §3d Reconciliation & scope variants (reference, not applied): BC incl-GFE = coeff(gate x stream="BC")
        (~61%); all-gated GFE-excluded = coeff(gate x (1 - GFE_excl)) (~54.5%).
    §3e Anchor regression (drift guard): published anchor = 0.518 (v4: 43 actions -> 51.8% primary);
        computed all-gated primary = coeff(gate); delta = computed - published; Anchor OK? =
        IF(ABS(delta) < 0.01, "OK", "FAIL"). Promotes bc/ap/total coeff cells, distributed low/high,
        anchor_ok, primary_tam_coeff.

§4  TAM bridge (TAM = BC_base x BC_coeff + AP_base x AP_coeff)
    §4a Applied per-stream supplier coefficients (live links to §3): BC coeff <- §3a, AP/LLTM coeff <- §3a.
    §4b Virginia (LI 2013) TAM / §4c Columbia (LI 1045) TAM, each per FY:
        - BC base               <- §2 bc_base_cell(li, fy)
        - TAM - BC stream       = IF(N(BC_base)=0,"", N(BC_base) x BC_COEFF)
        - AP/LLTM base          <- §2 ap_lltm_base_cell(li, fy)
        - TAM - AP/LLTM stream  = IF(N(AP_base)=0,"", N(AP_base) x AP_COEFF)
        - TAM (both streams)    = N(TAM_BC) + N(TAM_AP)
    §4d Portfolio TAM + stream bridge (Va + Col): BC stream TAM, AP/LLTM stream TAM, TAM (portfolio),
        each = N(Va) + N(Col) per FY. Total weighted coefficient = SUM(portfolio TAM, all FY) /
        SUM(all per-class BC+AP bases, all FY).
    §4e Annualization + deck-bridge figures (FY22-27):
        - Cumulative portfolio TAM  = SUM(portfolio TAM, FY22-27)
        - Number of fiscal years    = n_years_count_formula  <- Assumptions (fy_end - fy_start + 1)
        - Average annual portfolio TAM = cumulative / n_years (an average, not a run-rate)
        - Cumulative BC construction base = sum of §2d portfolio BC base over FY  <- portfolio_bc_base_cell
        - Removed by POP (prime / co-prime / GFE) = cumulative BC base - cumulative TAM
        Promotes tam_cell, tam_total_cell, tam_bc_total_cell, tam_ap_total_cell, cumulative_tam_cell,
        n_years_cell, avg_annual_tam_cell, cumulative_bc_base_cell, removal_cell, tam_bridge_cell.

§5  TAM checks
    - Portfolio TAM = BC TAM + AP/LLTM TAM  = IF(ABS(cumulative - (sum BC-stream + sum AP-stream)) < 0.5,
      "OK","FAIL")
    - Average annual = cumulative / fiscal years  = IF(ABS(avg x n_years - cumulative) < 0.5,"OK","FAIL")
    - Anchor regression holds  = anchor_ok_cell (computed all-gated primary ties the v4 51.8% anchor)

Notes
- Native cell notes: 2 -
    §1 (C): applied BC coefficient is the strict, non-nuclear POP supplier + foreign share (BPMI excluded)
    §1 (C): reference only - the AP/LLTM POP coefficient (~48.5%) is not applied (AP additive base = 0)
- Note column: none.
