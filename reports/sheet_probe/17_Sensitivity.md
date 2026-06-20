# sheet_probe: Sensitivity

- source: `file`
- tab name: `Sensitivity`
- tab color: `FF6E6E6E`
- gridlines shown: `0`
- columns: 3 · rows: 30 · cells: 63 · formulas: 18

## Banners
- `B2` S_TITLE_SHEET — Sensitivity
- `B4` S_TITLE_SECTION — §1 - Coefficient ladder (BC coeff vs all-gated outside-yards POP)
- `B12` S_TITLE_SECTION — §2 - MYP swing
- `B20` S_TITLE_SECTION — §3 - TAM sensitivity (MYP adjustment effect: corrected vs disclosed-only coeff)
- `B29` S_TITLE_SECTION — §4 - AP/LLTM stream
- `B38` S_TITLE_SECTION — §5 - VLS launch-control sensitivity (boundary launcher electronics: out vs in)

## Formula dependencies (referenced sheet → cells)
- **Assumptions** (2): C32, C33
- **Entity Master** (2): C41, C42
- **POP Source Audit** (3): C16, C17, C26
- **TAM Build** (7): C7, C8, C9, C23, C24, C34, C35

## Cross-sheet links (8)
- `C7` S_LINK_PCT = 'TAM Build'!C42
- `C8` S_LINK_PCT = 'TAM Build'!C52
- `C9` S_LINK_PCT = 'TAM Build'!C51
- `C16` S_LINK_NUM = 'POP Source Audit'!D20
- `C23` S_LINK_NUM = 'TAM Build'!I114
- `C32` S_LINK_PCT = 'Assumptions'!C37
- `C33` S_LINK_PCT = 'Assumptions'!C38
- `C34` S_LINK_NUM = 'TAM Build'!I113

## Cells
- `B2` S_TITLE_SHEET: Sensitivity
- `C2` S_TITLE_SHEET: 
- `A4` S_DEFAULT: x
- `B4` S_TITLE_SECTION: §1 - Coefficient ladder (BC coeff vs all-gated outside-yards POP)
- `C4` S_TITLE_SECTION: 
- `B6` S_HEADER_LEFT: Coefficient
- `C6` S_HEADER_CENTER: Value
- `B7` S_BOLD: BC supplier coeff (applied, MYP-corrected)
- `C7` S_LINK_PCT: ='TAM Build'!C42
- `B8` S_DEFAULT: Outside-yards POP, MYP-corrected
- `C8` S_LINK_PCT: ='TAM Build'!C52
- `B9` S_DEFAULT: Outside-yards POP, disclosed (artifact)
- `C9` S_LINK_PCT: ='TAM Build'!C51
- `A12` S_DEFAULT: x
- `B12` S_TITLE_SECTION: §2 - MYP swing
- `C12` S_TITLE_SECTION: 
- `B14` S_HEADER_LEFT: Measure
- `C14` S_HEADER_CENTER: Value
- `B15` S_BOLD: Outside-yards swing (disclosed - corrected)
- `C15` S_PCT: =C9-C8
- `B16` S_DEFAULT: MYP masters $M (reconstructed)
- `C16` S_LINK_NUM: ='POP Source Audit'!D20
- `B17` S_DEFAULT: Masters as % of gated corpus $
- `C17` S_PCT: =C16/'POP Source Audit'!D15
- `A20` S_DEFAULT: x
- `B20` S_TITLE_SECTION: §3 - TAM sensitivity (MYP adjustment effect: corrected vs disclosed-only coeff)
- `C20` S_TITLE_SECTION: 
- `B22` S_HEADER_LEFT: Measure
- `C22` S_HEADER_CENTER: $M
- `B23` S_BOLD: Portfolio TAM (applied, MYP-corrected)
- `C23` S_LINK_NUM: ='TAM Build'!I114
- `B24` S_DEFAULT: Portfolio TAM (disclosed-only BC coeff)
- `C24` S_NUM: =C23*('TAM Build'!C45/'TAM Build'!C42)
- `B25` S_BOLD: MYP adjustment uplift on TAM
- `C25` S_NUM: =C23-C24
- `B26` S_DEFAULT: Memo: masters' embedded content @ 42% band
- `C26` S_NUM: ='POP Source Audit'!D20*0.42
- `A29` S_DEFAULT: x
- `B29` S_TITLE_SECTION: §4 - AP/LLTM stream
- `C29` S_TITLE_SECTION: 
- `B31` S_HEADER_LEFT: Measure
- `C31` S_HEADER_CENTER: Value
- `B32` S_DEFAULT: Ship-construction share of CY AP
- `C32` S_LINK_PCT: ='Assumptions'!C37
- `B33` S_DEFAULT: AP/LLTM supplier coefficient
- `C33` S_LINK_PCT: ='Assumptions'!C38
- `B34` S_BOLD: AP/LLTM stream TAM ($M)
- `C34` S_LINK_NUM: ='TAM Build'!I113
- `B35` S_DEFAULT: AP/LLTM share of portfolio TAM
- `C35` S_PCT: =N('TAM Build'!I113)/('TAM Build'!I112+N('TAM Build'!I113))
- `A38` S_DEFAULT: x
- `B38` S_TITLE_SECTION: §5 - VLS launch-control sensitivity (boundary launcher electronics: out vs in)
- `C38` S_TITLE_SECTION: 
- `B40` S_HEADER_LEFT: Measure
- `C40` S_HEADER_CENTER: $M
- `B41` S_BOLD: Physical supplier base (VLS launch-control OUT - base case)
- `C41` S_NUM: =SUMPRODUCT(('Entity Master'!H7:H2162="supplier")*'Entity Master'!G7:G2162)-SUMPRODUCT(('Entity Master'!H7:H2162="supplier")*('Entity Master'!I7:I2162="unbucketed")*'Entity Master'!G7:G2162)
- `B42` S_DEFAULT: + VLS launch-control (Leonardo DRS Training&Control + Laurel; mission_systems)
- `C42` S_NUM: =SUMPRODUCT(('Entity Master'!L7:L2162=1)*'Entity Master'!G7:G2162)
- `B43` S_BOLD: = Physical supplier base (VLS launch-control IN - sensitivity)
- `C43` S_NUM: =C41+C42
- `B44` S_DEFAULT: VLS uplift as % of base
- `C44` S_PCT: =C42/C41
