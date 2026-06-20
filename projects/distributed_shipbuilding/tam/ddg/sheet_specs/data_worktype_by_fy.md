Worktype by FY
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_worktype_by_fy.py

Purpose
The gated work-type share evidence: supplier-addressable subaward dollars by bucket
and subaward action FY, restricted to yard construction PIIDs (GD-BIW + HII-Ingalls
prime groups) and the FY2022-FY2025 action-year window. GFE / combat-system prime
chains (Aegis, SPY-6, guns/VLS, DRS, GE) are excluded because the TAM removes the
GFE stream before the BC base; partial FY2026 reporting is excluded as incomplete.
SAM Build allocates annual TAM at each FY's own share vector from this sheet.

Reads
- Entity Master   per-entity Yard $ columns (the gate, visible per vendor)
                  [yard_fy_range / yard_dollar_range], role / bucket / modular /
                  $M ranges - every figure here is a live SUMPRODUCT over the table
- nc_scope_summary.json   PIID -> prime group (drives the Yard columns themselves,
                  inside the Entity Master aggregation)

Feeds
- SAM Build   per-FY observed shares [wt_share_cell], window shares
              [wt_window_share_cell], modular tag [wt_modular_share_cell]

On the sheet
§1  Evidence basis (gated share evidence)
    - Field rows: source, prime scope, FY window, feeds.

§2  Observed supplier $M by bucket x subaward FY (gated)
    - 7 buckets + unbucketed rows; each FY cell =
      SUMPRODUCT((role=supplier)*(bucket=k)*YardFY<yy> column); window column = SUM.
    - Total row: per-FY supplier-addressable (gated).

§3  Observed bucket shares by FY
    - Same grid; share = column $ / column addressable. Columns each sum to 100%.

§4  Modular tag (gated window)
    - Modular-flagged supplier $M in the gated window (live SUMPRODUCT; 0.0 - DDG
      modular-flagged entities all sit under GFE-chain primes) + share of window.

§5  Reconciliation to Entity Master (all live arithmetic)
    - Supplier total -> yard-PIID $ -> gated window $; the two exclusions are the
      differences; tie check gated + excluded = supplier total.

Notes
- Native cell notes: none.
- A negative gated cell (de-obligations exceeding obligations in a bucket/FY)
  fails the module's import-time guard; FY22-25 yard-gated cells are all >= 0.
