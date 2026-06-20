Number Audit
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_number_audit.py

Purpose
Ties every deck figure back to its source cell, so the deck contract is provably
consistent with the model. Each deck value must equal its producer; the fail count
gates the deck. §2 is a native no-format table.

Reads
- Figure Register   the figure REGISTRY, plus value_cell (the rendered Figure Register E
                 cell per figure) and source_ref (the producer cell each figure links)

Feeds
- Executive Summary, QA Reconciliation (both link the figure-audit fail count, not recompute it)
- Producer accessors: fail_count_formula, fail_count_cell (-> 'Number Audit'!C7)
- Native table: tbl_ddg_figure_audit

On the sheet
§1  Tie-out status
    - Figures failing tie-out = COUNTIF(Status column G, "FAIL") over the §2 rows
      [fail_count_cell -> C7]; note "must be 0 to ship the deck".
    - Status = IF(fail_count=0, "OK", "FAIL"); note states the number of deck figures
      checked (= len(REGISTRY)).

§2  Figure tie-out (deck value vs source cell)
    - Native table, columns: Figure ID, Slide, Deck value, Source value, Delta, Status;
      one row per figure in Figure Register' REGISTRY.
    - Deck value = value_cell(fid)  <- Figure Register (the rendered E cell).
    - Source value = ref            <- the producer cell that figure links to.
    - Delta  = Deck value - Source value  (= D{r}-E{r}).
    - Status = IF(ABS(Delta) < 0.01, "OK", "FAIL")  (tolerance _TOL = 0.01).
    - % figures use the percent link/number styles; everything else the numeric styles.

Notes
- Native cell notes: none.
- Note column: none.
