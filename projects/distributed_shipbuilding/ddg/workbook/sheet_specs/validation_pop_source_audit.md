POP Source Audit
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_pop_source_audit.py

Purpose
Confirmation coverage and risk ratios over the gated POP corpus (including the
MYP masters) behind the BC supplier coefficient. Risk-weighted confirmation,
coverage roll-up over the gated corpus, and the risk ratios + stream partition.

Reads
- POP Corpus   gate / GFE-excl / confirmed / stream / $ / MYP-master ranges - the
               SUMPRODUCT operands behind every coverage line  [gate_range, gfe_excl_range,
               confirmed_range, stream_range, pop_dollar_range, myp_master_range]

Feeds
- Figure Register (gated $, GFE-excluded $, MYP-masters $), Executive Summary,
  QA Reconciliation (partition OK, coverage), Sensitivity (masters $, gated $)
- Producer accessors: coverage_cell, partition_ok_cell, gated_dollar_cell,
  gfe_excluded_dollar_cell, masters_dollar_cell

On the sheet
§1  Confirmation approach (risk-weighted)
    - Prose tiering of the review effort:
      Tier 1 = top-$ actions covering ~90-95% of the weighted pool (all $250M+ / $100M+).
      Tier 2 = the two MYP masters (redacted; reconstructed from FPDS + trade press).
      Tier 3 = POP not summing ~100% (high unparsed) / GFE-suspect / any coefficient-mover.
    - Confirmed := gated AND non-GFE AND manual_review_status <> unresolved (default 1).

§2  Coverage (gated corpus, incl. MYP masters)
    Masks over POP Corpus: in-scope = gate x (1 - GFE_excl); confirmed = in-scope x confirmed.
    Each row reports an action count = SUMPRODUCT(mask) and $ = SUMPRODUCT(mask x $):
    - Gated TAM corpus                  = SUMPRODUCT(gate ...)        (gate + 2 MYP master rows)
    - less: GFE / Navy-directed scope   = SUMPRODUCT(gate x GFE_excl) (ddg_gfe_*; dropped)  [feeds Figure Register]
    - In-scope (non-GFE) gated          = SUMPRODUCT(in-scope ...)    (corpus the BC coeff is measured over)
    - confirmed                         = SUMPRODUCT(confirmed ...)   (manual_review_status = confirmed)
    - of which BC stream                = SUMPRODUCT(confirmed x (stream="BC"))  (all DDG gated work is BC)
    - MYP masters (reconstructed)       = SUMPRODUCT(gate x myp_master) (~$14.58B BIW + Ingalls)  [feeds Figure Register]
    - Disclosed (excl. masters)         = SUMPRODUCT(gate x (1 - myp_master)) (announcement corpus only)

§3  Risk ratios + partition
    - Confirmation coverage (% of in-scope $) = IF(in-scope actions=0, 0,
      confirmed $ / in-scope $); target ~90-95%+, 100% = all confirmed.  [feeds QA Reconciliation / cell note]
    - Stream partition OK? = IF(BC-stream actions = confirmed actions, "OK", "FAIL")
      (every in-scope action is BC; DDG has no AP/LLTM POP corpus).  [feeds QA Reconciliation]
    - MYP masters as % of gated $ = IF(gated $=0, 0, masters $ / gated $)
      (the reconstruction's weight in the corpus).
    - Cell notes: coverage formula definition (confirmed in-scope $ / in-scope $, risk-weighted)
      and the masters note (~$14.58B redacted, reconstructed from FPDS obligatedAmount + trade press).

Notes
- Native cell notes: 2 -
    §2 (D): the two MYP masters are $-redacted; their ~$14.58B is reconstructed from FPDS + trade press
    §3 (C): confirmation coverage = confirmed in-scope $ / in-scope $ (confirmed = gated AND non-GFE)
- Note column: none.
