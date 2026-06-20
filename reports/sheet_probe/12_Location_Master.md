# sheet_probe: Location Master

- source: `file`
- tab name: `Location Master`
- tab color: `FF7B1F3A`
- gridlines shown: `0`
- columns: 5 · rows: 14 · cells: 47 · formulas: 4

## Banners
- `B2` S_TITLE_SHEET — Location Master
- `B4` S_TITLE_SECTION — §1 - Prime sites
- `B11` S_TITLE_SECTION — §2 - Location principle
- `B17` S_TITLE_SECTION — §3 - Domestic / foreign split (foreign / FMS is excluded scope)

## Hardcoded inputs (2)
- `C20` S_NUM_INPUT = 8612.0
- `C21` S_NUM_INPUT = 2589.9

## Cells
- `B2` S_TITLE_SHEET: Location Master
- `C2` S_TITLE_SHEET: 
- `D2` S_TITLE_SHEET: 
- `E2` S_TITLE_SHEET: 
- `A4` S_DEFAULT: x
- `B4` S_TITLE_SECTION: §1 - Prime sites
- `C4` S_TITLE_SECTION: 
- `D4` S_TITLE_SECTION: 
- `E4` S_TITLE_SECTION: 
- `B6` S_HEADER_LEFT: State
- `C6` S_HEADER_LEFT: Name
- `D6` S_HEADER_LEFT: Prime-controlled site
- `E6` S_HEADER_LEFT: Role
- `B7` S_DEFAULT: ME
- `C7` S_DEFAULT: Maine
- `D7` S_DEFAULT: GD Bath Iron Works (BIW)
- `E7` S_DEFAULT: final-assembly yard
- `B8` S_DEFAULT: MS
- `C8` S_DEFAULT: Mississippi
- `D8` S_DEFAULT: HII Ingalls Shipbuilding
- `E8` S_DEFAULT: final-assembly yard
- `A11` S_DEFAULT: x
- `B11` S_TITLE_SECTION: §2 - Location principle
- `C11` S_TITLE_SECTION: 
- `D11` S_TITLE_SECTION: 
- `E11` S_TITLE_SECTION: 
- `B13` S_DEFAULT: Vendor location is context, not a scope test; scope is set per award action.
- `B14` S_DEFAULT: BIW (Maine) + Ingalls (Mississippi) are prime-controlled final-assembly sites; work there is not addressable.
- `A17` S_DEFAULT: x
- `B17` S_TITLE_SECTION: §3 - Domestic / foreign split (foreign / FMS is excluded scope)
- `C17` S_TITLE_SECTION: 
- `D17` S_TITLE_SECTION: 
- `E17` S_TITLE_SECTION: 
- `B19` S_HEADER_LEFT: Origin
- `C19` S_HEADER_CENTER: $M lifetime
- `D19` S_HEADER_CENTER: % of total
- `E19` S_HEADER_LEFT: 
- `B20` S_DEFAULT: Domestic (US)
- `C20` S_NUM_INPUT: 8612.0
- `D20` S_PCT: =C20/C22
- `B21` S_DEFAULT: Foreign
- `C21` S_NUM_INPUT: 2589.9
- `D21` S_PCT: =C21/C22
- `B22` S_TOTAL: Total
- `C22` S_NUM_TOTAL: =SUM(C20:C21)
- `D22` S_PCT_TOTAL: =SUM(D20:D21)
- `E22` S_BORDER_TOP: 
