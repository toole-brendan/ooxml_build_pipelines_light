QA Reconciliation
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_qa_reconciliation.py

Purpose
The official audit gate: core invariant checks across the corpus, the TAM/SAM
identities, the exclusions, and the audit chain. All checks must read OK with Number
Audit at 0 FAIL before the build is considered clean. Produces status_range.

Reads
- TAM Build           anchor_ok_cell  (QA-01)
- POP Source Audit    partition_ok_cell (QA-02), coverage_cell (QA-03),
                      gfe_excluded_dollar_cell (QA-10)
- Assumptions  modeled_share_total_cell  (QA-04)
- SAM Build           portfolio_tam_cell, bucketed_total_cell, sam_cell("broad"),
                      unbucketed_tam_cell  (QA-05/06/07/08)
- SIB Excluded        sib_total_cell  (QA-09)
- Number Audit        fail_count_formula  (QA-11)
- AP Bridge             ap_bridge_base_cell  (QA-12)

Feeds
- Executive Summary (reads status_range / fail_count_qa_formula)
- Accessors: status_range() -> 'QA Reconciliation'!G<first>:G<last>;
  fail_count_qa_formula() -> COUNTIF(status_range, "FAIL")
- Hardcoded anchors: SIB $4,251.8M; GFE $1,283.0M + nuclear-LLTM $4,813.6M

On the sheet
(Layout note: §2 checks are built first so status_range is promoted before §1.)

§1  At a glance: audit gate
    - QA FAIL count = COUNTIF(§2 status column, "FAIL")   (target 0 = all invariants hold)

§2  Core invariant checks (gate: all OK + Number Audit 0 FAIL)
    - Per check (Check, Description, Expected, Actual, Delta, Status). "text" checks use
      Status = IF(Actual = Expected, "OK", "FAIL"); numeric checks use Delta = Actual -
      Expected and Status = IF(ABS(Delta) < tol, "OK", "FAIL") with per-check tolerance:
        - QA-01 Anchor regression holds        Expected "OK"  Actual <- TAM Build anchor_ok_cell
        - QA-02 POP partition: in-scope = BC or AP/LLTM  Expected "OK"  Actual <- POP Source Audit partition_ok_cell
        - QA-03 Confirmation coverage = 100%   Expected 1.0  Actual <- coverage_cell        tol 0.001
        - QA-04 Modeled shares sum to 100%     Expected 1.0  Actual <- modeled_share_total_cell  tol 0.001
        - QA-05 Bucketed TAM = portfolio TAM   Expected =portfolio_tam_cell  Actual <- bucketed_total_cell  tol 0.5
        - QA-06 Bucketed TAM <= TAM            Expected 1    Actual = IF(bucketed_total <= portfolio+0.5, 1, 0)  tol 0.5
        - QA-07 Broad SAM <= TAM               Expected 1    Actual = IF(sam("broad") <= portfolio+0.5, 1, 0)    tol 0.5
        - QA-08 Broad SAM = TAM - unbucketed   Expected =portfolio - unbucketed_tam  Actual <- sam_cell("broad")  tol 0.5
        - QA-09 SIB exclusion ties to $4,251.8M  Expected 4251.8  Actual <- SIB Excluded sib_total_cell  tol 0.5
        - QA-10 GFE + nuclear LLTM out of corpus  Expected 1283.0+4813.6  Actual <- gfe_excluded_dollar_cell  tol 2.0
        - QA-11 Number Audit: 0 FAILs          Expected 0    Actual = Number Audit fail_count_formula  tol 0.5
        - QA-12 AP/LLTM additive base = 0      Expected 0    Actual <- AP Bridge ap_bridge_base_cell  tol 0.5

Notes
- Native cell notes: none.
- Note column: none.
