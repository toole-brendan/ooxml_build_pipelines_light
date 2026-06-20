# sheet_probe: POP Source Audit

- source: `file`
- tab name: `POP Source Audit`
- tab color: `FF6E6E6E`
- gridlines shown: `0`
- columns: 4 · rows: 20 · cells: 49 · formulas: 17

## Banners
- `B2` S_TITLE_SHEET — POP Source Audit
- `B4` S_TITLE_SECTION — §1 - Confirmation approach (risk-weighted)
- `B12` S_TITLE_SECTION — §2 - Coverage (gated corpus, incl. MYP masters)
- `B24` S_TITLE_SECTION — §3 - Risk ratios + partition

## Formula dependencies (referenced sheet → cells)
- **POP Corpus** (14): C15, D15, C16, D16, C17, D17, C18, D18, C19, D19, C20, D20 …

## Cells
- `B2` S_TITLE_SHEET: POP Source Audit
- `C2` S_TITLE_SHEET: 
- `D2` S_TITLE_SHEET: 
- `A4` S_DEFAULT: x
- `B4` S_TITLE_SECTION: §1 - Confirmation approach (risk-weighted)
- `C4` S_TITLE_SECTION: 
- `D4` S_TITLE_SECTION: 
- `B6` S_DEFAULT: Tier 1 - top-$ actions covering ~90-95% of the weighted pool; all $250M+ / $100M+.
- `B7` S_DEFAULT: Tier 2 - the two MYP masters (redacted; reconstructed from FPDS + trade press); all AP/EOQ.
- `B8` S_DEFAULT: Tier 3 - POP not summing ~100% (high unparsed); GFE-suspect; any coefficient-mover.
- `B9` S_DEFAULT: Confirmed = gated AND in-scope (non-GFE) AND manual_review_status<>unresolved (default 1).
- `A12` S_DEFAULT: x
- `B12` S_TITLE_SECTION: §2 - Coverage (gated corpus, incl. MYP masters)
- `C12` S_TITLE_SECTION: 
- `D12` S_TITLE_SECTION: 
- `B14` S_HEADER_LEFT: Metric
- `C14` S_HEADER_CENTER: Actions
- `D14` S_HEADER_CENTER: $M
- `B15` S_BOLD: Gated TAM corpus
- `C15` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160)
- `D15` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*'POP Corpus'!M7:M160)
- `B16` S_LABEL_INDENT_1: less: GFE / Navy-directed scope
- `C16` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*'POP Corpus'!J7:J160)
- `D16` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*'POP Corpus'!J7:J160*'POP Corpus'!M7:M160)
- `B17` S_BOLD: In-scope (non-GFE) gated
- `C17` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*(1-'POP Corpus'!J7:J160))
- `D17` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*(1-'POP Corpus'!J7:J160)*'POP Corpus'!M7:M160)
- `B18` S_LABEL_INDENT_1: confirmed
- `C18` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*(1-'POP Corpus'!J7:J160)*'POP Corpus'!K7:K160)
- `D18` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*(1-'POP Corpus'!J7:J160)*'POP Corpus'!K7:K160*'POP Corpus'!M7:M160)
- `B19` S_LABEL_INDENT_1: of which BC stream
- `C19` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*(1-'POP Corpus'!J7:J160)*'POP Corpus'!K7:K160*('POP Corpus'!H7:H160="BC"))
- `D19` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*(1-'POP Corpus'!J7:J160)*'POP Corpus'!K7:K160*('POP Corpus'!H7:H160="BC")*'POP Corpus'!M7:M160)
- `B20` S_BOLD: MYP masters (reconstructed)
- `C20` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*'POP Corpus'!L7:L160)
- `D20` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*'POP Corpus'!L7:L160*'POP Corpus'!M7:M160)
- `B21` S_DEFAULT: Disclosed (excl. masters)
- `C21` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*(1-'POP Corpus'!L7:L160))
- `D21` S_NUM: =SUMPRODUCT('POP Corpus'!I7:I160*(1-'POP Corpus'!L7:L160)*'POP Corpus'!M7:M160)
- `A24` S_DEFAULT: x
- `B24` S_TITLE_SECTION: §3 - Risk ratios + partition
- `C24` S_TITLE_SECTION: 
- `D24` S_TITLE_SECTION: 
- `B26` S_DEFAULT: Confirmation coverage (% of in-scope $)
- `C26` S_PCT: =IF(C17=0,0,D18/D17)
- `B27` S_DEFAULT: Stream partition OK? (every in-scope action is BC)
- `C27` S_DEFAULT: =IF(C19=C18,"OK","FAIL")
- `B28` S_DEFAULT: MYP masters as % of gated $
- `C28` S_PCT: =IF(D15=0,0,D20/D15)
