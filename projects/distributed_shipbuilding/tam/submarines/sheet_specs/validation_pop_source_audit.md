POP Source Audit
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_pop_source_audit.py

Purpose
The risk-weighted manual-confirmation audit of the POP corpus: coverage summary, risk
ratios, and the top-$ action register. Reads the POP corpus ranges (and the gated-row
register) from POP Corpus; its own coverage / partition / unparsed / concentration
figures are computed in-sheet from those ranges.

Reads
- POP Corpus   gate_range / gfe_excl_range / confirmed_range / stream_range /
                       pop_dollar_range / pct_range(eb,hii,other,foreign) - the
                       SUMPRODUCT operands; gated_row_cell(rank, key) - the top-$ gated
                       action register

Feeds
- Methodology, Figure Register, QA Reconciliation
- Producer cells / accessors: coverage_cell (confirmation coverage %),
  partition_ok_cell (stream partition OK/FAIL), gated_dollar_cell (§2 gated $),
  gfe_excluded_dollar_cell (§2 GFE-excluded $), inscope_dollar_cell, unparsed_share_cell,
  concentration_cell

On the sheet
§1  At a glance: confirmation & risk
    - Same-sheet echo of the §2 / §2a producer cells: gated TAM corpus $M, in-scope
      non-GFE $M, confirmation coverage % (target ~90%+), unparsed share (gated;
      >1-2% warrants review), largest-action concentration, stream partition check.

§2  Confirmation coverage (gated corpus)
    - Coverage table (Metric, Actions, $M, Note); inscope mask = gate x (1 - gfe_excl),
      conf mask = inscope x confirmed:
        Gated TAM corpus    = SUMPRODUCT(gate)         | SUMPRODUCT(gate x $)  [gated]
        less: GFE / excluded = SUMPRODUCT(gate x gfe)  | SUMPRODUCT(gate x gfe x $)  [gfe]
        In-scope (non-GFE)  = SUMPRODUCT(inscope)      | SUMPRODUCT(inscope x $)  [inscope]
        confirmed           = SUMPRODUCT(conf)         | SUMPRODUCT(conf x $)
        unresolved          = SUMPRODUCT(inscope x (1 - confirmed)) ...  (excluded until resolved)
        BC stream (conf)    = SUMPRODUCT(conf x (stream = "BC")) ...      (x BC supplier coeff)
        AP/LLTM (conf)      = SUMPRODUCT(conf x (stream = "AP_LLTM")) ... (x AP/LLTM coeff)
        Redacted / missing-$ = SUMPRODUCT(gate x ($ = 0)) ...            (0 in sub corpus)

    §2a Risk ratios
        Confirmation coverage = confirmed $ / in-scope $   (target ~90%+)  [coverage]
        Unparsed share (gated) = SUMPRODUCT(gate x $ x (1 - eb% - hii% - other% - foreign%))
                                 / gated $   (single-site / no-% parses)  [unparsed]
        Largest-action conc.   = top gated action $ (gated_row_cell(0,'dollar')) / gated $
                                 [concentration]
        Stream partition check = IF(|confirmed $ - (BC $ + AP $)| < 0.1, "OK", "FAIL")
                                 (in-scope conf = BC + AP)  [partition]

    §2b High-$ action register (top 10 by $, Tier-1 confirmed)
        Rank, PIID, Program, $M, Stream, Scope Class, Conf - each pulled from
        gated_row_cell(i, key) for i = 0..9 (the top gated actions by $, live links into
        POP Corpus).

Notes
- Native cell notes: none.
- Note column: none.
