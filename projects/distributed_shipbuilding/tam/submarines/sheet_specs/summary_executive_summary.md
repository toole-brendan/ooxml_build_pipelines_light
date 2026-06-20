Executive Summary
Tab color: 6A4C93 (purple)  ·  group: Executive summary
Module: summary_executive_summary.py

Purpose
The reader-facing answer page (first in the workbook): headline TAM/SAM, key
takeaways, the TAM bridge, the fiscal-year profile, the scenario menu, and audit
status. It LINKS to producer cells (green cross-sheet links) and never recomputes;
the only same-sheet arithmetic is per-stream FY sums (=N(...)+N(...), shown black).

Reads
- TAM Build         cumulative + avg-annual TAM, BC + AP/LLTM reference coeffs, cumulative BC base,
                    per-FY BC/AP/portfolio TAM totals, FY_COLUMNS
- SAM Build         per-scenario cumulative SAM / % of TAM / avg-annual SAM, portfolio TAM, bucketed
                    total, scenario_keys_ordered
- AP Bridge           AP bridge gross / GFE-removed / in-BC-removed / residual / additive base
                    [ap_bridge_*_cell]
- Assumptions  scenario_name (for the scenario-menu labels)
- Number Audit      fail count formula  [fail_count_formula]
- QA Reconciliation  fail count formula  [fail_count_qa_formula]

Feeds
- none (reader-facing answer page; nothing imports this module)

On the sheet
§1  Headline answer
    - Metric / Value / Source / Note table, all green links: Average annual portfolio TAM <- TAM Build,
      FY22-27 cumulative portfolio TAM <- TAM Build, Average annual broad SAM <- SAM Build, FY22-27
      cumulative broad SAM <- SAM Build, Applied BC supplier coefficient <- TAM Build, AP/LLTM additive
      base <- AP Bridge (confirmed $0).

§2  Key takeaways
    - Prose bullets: headline = modeled FY22-27 outsourced supplier TAM; avg annual = cumulative spread
      over the FY count; applied BC coeff = non-nuclear, BPMI-excluded POP share; AP/LLTM contributes $0
      additive TAM (no double-count); broad SAM is a scenario menu, not SOM.

§3  TAM bridge
    §3a BC stream: BC construction base (FY22-27) <- TAM Build cumulative_bc_base_cell; Applied BC supplier
        coefficient <- TAM Build; BC-stream supplier TAM = sum of TAM Build tam_bc_total_cell over FY
        (derived black S_NUM).
    §3b AP/LLTM stream (all <- AP Bridge except coeff): P-10 gross AP top-line = ap_bridge_gross_cell;
        less GFE/design/weapons = ap_bridge_gfe_removed_cell; less already inside P-5c BC =
        ap_bridge_in_bc_removed_cell; less un-itemized overlap = ap_bridge_residual_cell; AP/LLTM additive
        base = ap_bridge_base_cell; AP/LLTM reference coefficient <- TAM Build; AP/LLTM-stream supplier TAM
        = sum of TAM Build tam_ap_total_cell over FY.
    §3c Portfolio TAM: BC-stream supplier TAM (FY sum) + AP/LLTM-stream supplier TAM (FY sum); Total
        portfolio TAM <- TAM Build cumulative_tam_cell.

§4  TAM by fiscal year
    - Per FY: BC-stream TAM <- tam_bc_total_cell(fy), AP/LLTM-stream TAM <- tam_ap_total_cell(fy),
      Portfolio TAM <- tam_total_cell(fy); Total (FY22-27) row = BC FY sum, AP FY sum, cumulative TAM.

§5  SAM scenario menu
    - Per scenario (scenario_keys_ordered, named via Assumptions scenario_name): Cumulative SAM
      <- sam_cell(k), % of TAM <- sam_pct_cell(k), Avg annual SAM <- avg_annual_sam_cell(k), plus an
      interpretation note.

§6  Caveats and audit status
    §6a Interpretation caveats: SAM is not SOM; no win probability; no capability-fit haircut; no
        capacity-constrained ramp; AP/LLTM additive base confirmed zero unless reconciliation changes.
    §6b Audit status: Number Audit fail count + OK/FAIL <- Number Audit; QA Reconciliation fail count +
        OK/FAIL <- QA Reconciliation; AP/LLTM additive base = IF(ABS(ap_bridge_base) < 0.5, OK, FAIL);
        Broad SAM <= TAM = IF(sam_cell("broad") <= portfolio_tam + 0.5, OK, FAIL); Bucketed TAM = portfolio
        TAM = IF(ABS(bucketed_total - portfolio_tam) < 0.5, OK, FAIL).

Notes
- Native cell notes: 3 -
    §1 (C): average annual = FY22-FY27 cumulative TAM / fiscal years (the build cadence is lumpy)
    §1 (C): broad SAM = the all-seven-buckets scenario, a subset of TAM with no capture haircut
    §1 (C): gross P-10 advance procurement is a reference stream; its additive TAM base is $0
- Note column: none.
