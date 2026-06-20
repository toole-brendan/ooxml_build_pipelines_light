# sheet_probe: Sensitivity

- source: `file`
- tab name: `Sensitivity`
- tab color: `FF6E6E6E`
- gridlines shown: `0`
- columns: 3 · rows: 34 · cells: 68 · formulas: 18

## Banners
- `B2` S_TITLE_SHEET — Sensitivity
- `B4` S_TITLE_SECTION — §1 - The swings
- `B13` S_TITLE_SECTION — §2 - Coefficient ladder (the swings that move TAM/SAM)
- `B21` S_TITLE_SUBSECTION — §2a - Nuclear-boundary BPMI exclusion (applied)
- `B29` S_TITLE_SUBSECTION — §2b - TAM impact (headline vs pre-boundary sensitivity; AP base=0)
- `B37` S_TITLE_SECTION — §3 - Sensitivity guardrails
- `B44` S_TITLE_SECTION — §4 - VLS launch-control sensitivity (boundary launcher electronics: out vs in)

## Formula dependencies (referenced sheet → cells)
- **Assumptions** (1): C34
- **Entity Master** (2): C47, C48
- **POP Corpus** (3): C16, C24, C27
- **Sensitivity** (2): C9, C10
- **TAM Build** (6): C7, C8, C17, C18, C25, C32

## Cross-sheet links (5)
- `C7` S_LINK_PCT = 'TAM Build'!C54
- `C8` S_LINK_PCT = 'TAM Build'!C55
- `C17` S_LINK_PCT = 'TAM Build'!C54
- `C18` S_LINK_PCT = 'TAM Build'!C55
- `C25` S_LINK_PCT = 'TAM Build'!C54

## Cells
- `B2` S_TITLE_SHEET: Sensitivity
- `C2` S_TITLE_SHEET: 
- `B4` S_TITLE_SECTION: §1 - The swings
- `C4` S_TITLE_SECTION: 
- `B6` S_HEADER_LEFT: Measure
- `C6` S_HEADER_CENTER: Value
- `B7` S_BOLD: Headline supplier coefficient
- `C7` S_LINK_PCT: ='TAM Build'!C54
- `B8` S_DEFAULT: AP/LLTM reference coefficient
- `C8` S_LINK_PCT: ='TAM Build'!C55
- `B9` S_DEFAULT: Pre-boundary sensitivity TAM $M
- `C9` S_NUM: ='Sensitivity'!C33
- `B10` S_DEFAULT: Real P-10 gross AP $M (reference)
- `C10` S_NUM: ='Sensitivity'!C34
- `A13` S_DEFAULT: x
- `B13` S_TITLE_SECTION: §2 - Coefficient ladder (the swings that move TAM/SAM)
- `C13` S_TITLE_SECTION: 
- `B15` S_HEADER_LEFT: Variant
- `C15` S_HEADER_CENTER: Value
- `B16` S_DEFAULT: All-gated POP anchor (not applied)
- `C16` S_PCT: =IF(SUMPRODUCT('POP Corpus'!H17:H674*'POP Corpus'!K17:K674)=0,"",SUMPRODUCT('POP Corpus'!H17:H674*'POP Corpus'!K17:K674*('POP Corpus'!N17:N674+'POP Corpus'!O17:O674))/SUMPRODUCT('POP Corpus'!H17:H674*'POP Corpus'!K17:K674))
- `B17` S_BOLD: Headline coeff (non-nuclear)
- `C17` S_LINK_PCT: ='TAM Build'!C54
- `B18` S_BOLD: AP/LLTM coeff (reference; base=0)
- `C18` S_LINK_PCT: ='TAM Build'!C55
- `B19` S_DEFAULT: BC - AP/LLTM delta
- `C19` S_PCT: =C17-C18
- `A21` S_DEFAULT: x
- `B21` S_TITLE_SUBSECTION: §2a - Nuclear-boundary BPMI exclusion (applied)
- `C21` S_TITLE_SUBSECTION: 
- `B23` S_HEADER_LEFT: BC coefficient under each attribution
- `C23` S_HEADER_CENTER: Value
- `B24` S_DEFAULT: BC coeff incl. BPMI (sensitivity)
- `C24` S_PCT: =IF(SUMPRODUCT('POP Corpus'!H17:H674*'POP Corpus'!J17:J674*((1-'POP Corpus'!I17:I674)*('POP Corpus'!G17:G674="BC")+('POP Corpus'!D17:D674="bpmi_nuclear"))*'POP Corpus'!K17:K674)=0,"",SUMPRODUCT('POP Corpus'!H17:H674*'POP Corpus'!J17:J674*((1-'POP Corpus'!I17:I674)*('POP Corpus'!G17:G674="BC")+('POP Corpus'!D17:D674="bpmi_nuclear"))*'POP Corpus'!K17:K674*('POP Corpus'!N17:N674+'POP Corpus'!O17:O674))/SUMPRODUCT('POP Corpus'!H17:H674*'POP Corpus'!J17:J674*((1-'POP Corpus'!I17:I674)*('POP Corpus'!G17:G674="BC")+('POP Corpus'!D17:D674="bpmi_nuclear"))*'POP Corpus'!K17:K674))
- `B25` S_BOLD: Headline applied (BPMI excluded)
- `C25` S_LINK_PCT: ='TAM Build'!C54
- `B26` S_DEFAULT: BC swing (BPMI removal)
- `C26` S_PCT: =C24-C25
- `B27` S_DEFAULT: BPMI $ (now GFE-excluded)
- `C27` S_NUM: =SUMPRODUCT('POP Corpus'!H17:H674*('POP Corpus'!D17:D674="bpmi_nuclear")*'POP Corpus'!K17:K674)
- `A29` S_DEFAULT: x
- `B29` S_TITLE_SUBSECTION: §2b - TAM impact (headline vs pre-boundary sensitivity; AP base=0)
- `C29` S_TITLE_SUBSECTION: 
- `B31` S_HEADER_LEFT: Measure
- `C31` S_HEADER_CENTER: $M
- `B32` S_BOLD: Headline non-nuclear supplier TAM (cum.)
- `C32` S_NUM: =N('TAM Build'!C117)+N('TAM Build'!D117)+N('TAM Build'!E117)+N('TAM Build'!F117)+N('TAM Build'!G117)+N('TAM Build'!H117)
- `B33` S_DEFAULT: Pre-boundary sensitivity TAM
- `C33` S_NUM: =C32*(C24/C25)
- `B34` S_DEFAULT: Real P-10 gross AP (FY22-27, ref)
- `C34` S_NUM: =N('Assumptions'!C32)+N('Assumptions'!D32)+N('Assumptions'!E32)+N('Assumptions'!F32)+N('Assumptions'!G32)+N('Assumptions'!H32)+N('Assumptions'!C33)+N('Assumptions'!D33)+N('Assumptions'!E33)+N('Assumptions'!F33)+N('Assumptions'!G33)+N('Assumptions'!H33)
- `A37` S_DEFAULT: x
- `B37` S_TITLE_SECTION: §3 - Sensitivity guardrails
- `C37` S_TITLE_SECTION: 
- `B39` S_DEFAULT: Sensitivity values are not headline.
- `B40` S_DEFAULT: The BPMI-included coefficient (~75.7%) is not applied.
- `B41` S_DEFAULT: The AP/LLTM coefficient is reference-only while the additive base is zero.
- `A44` S_DEFAULT: x
- `B44` S_TITLE_SECTION: §4 - VLS launch-control sensitivity (boundary launcher electronics: out vs in)
- `C44` S_TITLE_SECTION: 
- `B46` S_HEADER_LEFT: Measure
- `C46` S_HEADER_CENTER: $M
- `B47` S_BOLD: Physical supplier base (VLS launch-control OUT - base case)
- `C47` S_NUM: ='Entity Master'!C973-'Entity Master'!C972
- `B48` S_DEFAULT: + VLS launch-control boundary (mission_systems)
- `C48` S_NUM: ='Entity Master'!C980
- `B49` S_BOLD: = Physical supplier base (VLS launch-control IN - sensitivity)
- `C49` S_NUM: =C47+C48
