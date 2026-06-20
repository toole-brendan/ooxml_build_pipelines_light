Executive Summary
Tab color: 6A4C93 (purple)  ·  group: Executive summary
Module: summary_executive_summary.py

Purpose
The reader-facing answer page, first in the workbook: headline TAM/SAM, the TAM
bridge, the SAM scenario menu, bucket allocation, and audit status, read top-to-
bottom. It LINKS to producer cells (green cross-sheet links) and never recomputes;
the cross-sheet links are the substance of every row.

Reads
- TAM Build       avg-annual TAM, portfolio TAM, BC- / AP-stream TAM, BC supplier
                  coeff, MYP-corrected outside-yards POP, BC construction base, MYP
                  anchor-OK  [avg_annual_tam_cell, portfolio_tam_cell, portfolio_bc_tam_cell,
                  portfolio_ap_tam_cell, bc_supplier_coeff_cell, outside_yards_corrected_cell,
                  portfolio_bc_base_cell, anchor_ok_cell]
- SAM Build       per-scenario SAM $M / % of TAM / avg-annual, bucket TAM, unbucketed
                  residual, bucketed total, ordered scenario keys  [sam_cell, sam_pct_cell,
                  sam_avg_annual_cell, bucket_tam_cell, unbucketed_tam_cell,
                  bucketed_total_cell, scenario_keys_ordered]
- Scenarios       scenario display names  [scenario_name]
- POP Source Audit       POP coverage, stream-partition-OK  [coverage_cell, partition_ok_cell]
- Number Audit    failed-figure count  [fail_count_cell]
- QA Reconciliation       failed-check count + status  [qa_fail_count_cell, qa_status_cell]

Feeds
- none (reader-facing answer page; nothing imports this module)

On the sheet
§1  Headline
    - KPI table; every Value is a green link, no recompute. Annual headline first:
      Average annual TAM $M/yr <- TAM Build avg_annual_tam, Average annual broad SAM
      $M/yr <- SAM Build sam_avg_annual("broad"). Cumulative backup: Portfolio TAM <-
      TAM Build, Broad SAM <- SAM Build, BC-stream TAM / AP-stream TAM <- TAM Build,
      BC supplier coefficient <- TAM Build, MYP-corrected outside-yards POP <- TAM Build
      (~33%; never the 87% artifact), Broad SAM / TAM <- SAM Build. Notes flag SAM != SOM
      and the MYP-correction guardrail.

§2  TAM bridge
    - Reconstructs the headline as a step bridge, all links <- TAM Build:
      BC construction base (FY22-27) <- portfolio_bc_base
      x BC supplier coefficient   <- bc_supplier_coeff
      = BC-stream TAM             <- portfolio_bc_tam   (base x coefficient)
      + AP/LLTM-stream TAM        <- portfolio_ap_tam   (CY AP x ship-constr share x AP coeff)
      = Portfolio TAM            <- portfolio_tam        (BC-stream + AP/LLTM-stream).

§3  SAM scenarios
    - One row per scenario (scenario_keys_ordered, names <- Scenarios): SAM $M <- SAM
      Build sam_cell, % of TAM <- sam_pct_cell, Avg annual SAM $M/yr <- sam_avg_annual,
      plus a static interpretation gloss. All green links; nothing recomputed.

§4  Bucket allocation
    - One row per work-type bucket: Bucket TAM $M <- SAM Build bucket_tam_cell; plus the
      Unbucketed residual (NOT in scenario SAM) <- unbucketed_tam_cell (why broad SAM <
      total TAM); Total (7 buckets + unbucketed = TAM) <- bucketed_total_cell.

§5  Audit status
    - Status panel linking the validation tabs' rendered cells:
      QA Reconciliation (failed) <- QA Reconciliation qa_fail_count, status <- qa_status
      Number Audit (failed) <- Number Audit fail_count; status = IF(fail=0,"OK","FAIL")
      POP coverage <- POP Source Audit coverage_cell; status = IF(coverage>=0.9,"OK","REVIEW")
      POP stream partition <- POP Source Audit partition_ok_cell
      MYP anchor <- TAM Build anchor_ok_cell.

§6  Caveats
    - Static prose: SAM is a target-bucket menu (not SOM/capture/win-prob/ramp);
      AP/LLTM is an additive, assumption-dependent stream; POP is a coefficient proxy
      with MYP masters reconstructed; FFATA subawards seed bucket shares but are not the
      TAM denominator (cell note on the FFATA line).

Notes
- Native cell notes: 3 -
    §1 (C): average annual TAM = cumulative / fiscal years (an average, not a run-rate)
    §1 (C): SAM is a target-bucket menu, not SOM / capture / win probability ("broad" = all 7 buckets)
    §1 (C): headline uses the MYP-corrected outside-yards POP (~33%); the ~87% artifact is never presented
- Note column: none.
