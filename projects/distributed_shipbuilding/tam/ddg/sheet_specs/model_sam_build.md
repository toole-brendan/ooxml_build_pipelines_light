SAM Build
Tab color: 34406B (indigo)  ·  group: Model (TAM/SAM)
Module: model_sam_build.py

Purpose
Allocates portfolio TAM across work-type buckets and computes scenario SAM as a
subset of TAM (no capture haircut). Three detail blocks - §2 Subawards (supplier-
addressable shares) -> §3 Allocation (bucket TAM) -> §4 Scenarios (the SAM menu),
plus §5 Annual SAM - behind a §1 at-a-glance headline.

Reads
- Entity Master             subaward $ by role + bucket - the SUMPRODUCT operands for
                       observed shares  [role_range, bucket_range, ent_dollar_range]
- TAM Build            portfolio TAM (single pure link, not recomputed), TAM by FY,
                       n-years  [portfolio_tam_cell, tam_total_cell, n_years_cell]
- Assumptions               editable bucket-share Adjustment +/- per bucket  [bucket_adjustment_cell]
- Scenarios            scenario keys / display names / 0-1 flag ranges per scenario
                       [scenario_keys, scenario_name, scenario_flag_range]

Feeds
- Executive Summary, Figure Register, z_ChartData, QA Reconciliation
- Producer cells: per-scenario SAM $M / % of TAM / SAM-per-year (sam_cell,
  sam_pct_cell, sam_avg_annual_cell), bucket TAM $M (bucket_tam_cell / range),
  unbucketed-residual TAM (unbucketed_tam_cell), portfolio-TAM basis + bucketed
  total (portfolio_tam_cell, bucketed_total_cell), modeled / observed bucket shares
  (modeled_share_cell, observed_share_cell, bucket_share_range), annual SAM by FY
  (annual_sam_cell, annual_broad_sam_cell), ordered scenario keys

On the sheet
§1  At a glance: SAM scenario menu
    - Same-sheet summary of the §4 scenario rows, shown as black derived values (not
      green links - these are this sheet's own outputs): per-scenario SAM $M, % of TAM,
      SAM $M/yr. Built at render; asserts it fills the rows reserved before the body.

§2  Supplier-addressable shares (observed subaward $ + Assumptions adjustment; residual explicit)
    §2a Observed bucket shares (subaward $) + Assumptions adjustment:
        - Observed $M (per bucket)  = SUMPRODUCT(role="supplier" mask x bucket=k mask x $)
                                      <- Entity Master
        - Observed %                = bucket observed $ / supplier-addressable total
        - Adj +/- (Assumptions)          <- Assumptions bucket_adjustment_cell (default 0 per bucket)
        - Modeled %                 = Observed % + Adj  (NOT renormalized)
        - Unbucketed / ambiguous row (EXCLUDED from scenario SAM): observed $ via the
          UNBUCKETED mask; modeled % = 1 - SUM(7 bucket modeled %) - the explicit residual.
        - Supplier-addressable total = SUMPRODUCT(role="supplier" x $); modeled-% total row.
    §2b Excluded from the addressable base (audit - not supplier-addressable):
        $M per role via SUMPRODUCT(role=rk x $) <- Entity Master, for prime yard (BIW),
        co-prime yard (HII Ingalls), GFE / Navy-directed (Aegis/SPY-6/weapons), and
        service / non-component; grand total = SUMPRODUCT($) over all recipients.

§3  Bucket allocation
    §3a Portfolio TAM basis (cumulative FY22-27): single green link <- TAM Build
        portfolio_tam (the producer; never recomputed here).
    §3b TAM by work-type bucket = portfolio TAM x modeled bucket share:
        - Bucket TAM $M  = portfolio_TAM x modeled_share(k)   (modeled share links §2a
          on THIS sheet -> black, same-sheet)
        - Unbucketed row = portfolio_TAM x unbucketed modeled share
        - Total (7 buckets + unbucketed) = SUM of bucket TAM = TAM by construction.

§4  Scenario calculation
    §4a SAM by leadership scenario (subset of TAM, no haircut):
        - SAM $M     = SUMPRODUCT(bucket-TAM range (§3b), scenario flag range)
                       <- Scenarios flags (1 = scenario targets that bucket)
        - % of TAM   = scenario SAM / portfolio TAM
        - SAM $M/yr  = scenario SAM / n_years  <- TAM Build n_years
    §4b Residual explanation: broad SAM = TAM - unbucketed residual (the all-buckets
        scenario excludes only the unbucketed share); broad is the widest menu, not SOM.

§5  Annual SAM by fiscal year (annual TAM by FY x scenario bucket share)
    - annual scenario SAM(fy) = TAM_total(fy) x SUMPRODUCT(modeled bucket shares (§2a),
      scenario flags)  <- TAM Build tam_total per FY (FY22-27), x Scenarios flags;
      FY22-27 column = SUM across the year columns.
    §5b Annual tie-out: annual broad SAM FY22-27 (sum) = cumulative broad SAM (§4) by
        construction.

Notes
- Native cell notes: 3 -
    §2a (C): unbucketed / ambiguous supplier $ stays visible but is EXCLUDED from scenario SAM
    §2a (C): observed bucket shares are description-led (every FFATA subaward classified by award description)
    §4a (C): broad scenario = all seven named work-type buckets, no capture haircut
- Note column: none.
