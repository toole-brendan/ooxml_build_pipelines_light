QA Reconciliation
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_qa_reconciliation.py

Purpose
The reconciliation gate: invariant checks must all read OK and figures must be
0 FAIL before the build is considered Phase-2 clean. A status block on top, then
the QA-01..QA-13 check table. The figure-audit fail count LINKS to Number Audit's
rendered cell (not recomputed).

Reads
- TAM Build      anchor-OK flag, outside-yards disclosed/corrected, BC- & AP-stream TAM
                 [anchor_ok_cell, portfolio_bc_tam_cell, portfolio_ap_tam_cell, ...]
- SAM Build      portfolio TAM, modeled-share total, bucketed total, unbucketed residual,
                 broad SAM  [portfolio_tam_cell, modeled_share_total_cell, ...]
- POP Source Audit      partition OK, coverage, GFE-excluded $  [partition_ok_cell, coverage_cell,
                 gfe_excluded_dollar_cell]
- AP Bridge      in-window CY AP, AP/LLTM stream TAM  [cy_ap_inwindow_cell, ap_tam_cell]
- Number Audit   the deck-figure fail count (linked, not recomputed)  [fail_count_cell]

Feeds
- Executive Summary (consumes the QA status / fail count)
- Producer accessors: fail_count_qa_formula, qa_fail_count_cell (-> C8),
  qa_status_cell (-> C7)

On the sheet
§1  Status
    - QA status = IF(qa_fail_count=0, "OK", "FAIL")  [qa_status_cell -> C7], where
      qa_fail_count = COUNTIF(§2 Status column G, "FAIL") over QA-01..QA-13.
    - Number of failed checks = same COUNTIF  [-> C8].
    - Figure audit fails    <- Number Audit fail_count_cell (linked).
    - POP partition status  <- POP Source Audit partition_ok_cell.
    - POP coverage          <- POP Source Audit coverage_cell (%).

§2  Reconciliation checks (the Phase-2 gate: all OK + Figures 0 FAIL)
    Columns: Check, Description, Expected, Actual, Delta, Status. Per row,
    text checks: Status = IF(Actual=Expected, "OK", "FAIL");
    numeric checks: Delta = Actual - Expected, Status = IF(ABS(Delta) < tol, "OK", "FAIL").
    - QA-01  anchor: MYP-corrected outside-yards near ~33%  <- TAM Build anchor_ok (text = "OK")
    - QA-02  POP stream partition OK (every in-scope action BC)  <- POP Source Audit (text = "OK")
    - QA-03  confirmation coverage of in-scope = 100%  <- POP Source Audit; expected 1.0, tol 0.001
    - QA-04  modeled bucket shares (7 + residual) sum to 100%  <- SAM Build; expected 1.0, tol 0.001
    - QA-05  sum of bucketed TAM = portfolio TAM  <- SAM Build; expected = portfolio_tam, tol 0.5
    - QA-06  sum of bucketed TAM <= TAM  = IF(bucketed <= TAM + 0.5, 1, 0); expected 1, tol 0.5
    - QA-07  broad-component SAM <= TAM  = IF(SAM_broad <= TAM + 0.5, 1, 0); expected 1, tol 0.5
    - QA-08  broad SAM = TAM - unbucketed residual; expected = TAM - unbucketed, tol 0.5
    - QA-09  MYP correction real = IF(disclosed > corrected, 1, 0)  <- TAM Build; expected 1, tol 0.5
    - QA-10  GFE / Navy-directed scope dropped = IF(GFE_excl $ > 0, 1, 0)  <- POP Source Audit; expected 1, tol 0.5
    - QA-11  figures: every deck figure ties (0 FAILs)  <- Number Audit fail_count; expected 0, tol 0.5
    - QA-12  portfolio TAM = BC stream + AP/LLTM stream  <- TAM Build; expected = TAM, tol 0.5
    - QA-13  AP/LLTM stream TAM <= in-window CY AP  = IF(ap_tam <= cy_ap_inwindow + 0.5, 1, 0)
             <- AP Bridge; expected 1, tol 0.5

§3  Failure detail
    - Prose: any FAIL is a gate stop; the Status column names the failing check;
      resolve on the producer tab.

Notes
- Native cell notes: none.
- Note column: none.
