# 2026-05-28 — Methodology workbook build session

## Scope
Designed and built the methodology workbook (`sub_workbook/sub.xlsx`) from a single placeholder sheet to **14 fully wired sheets**, stdlib-only OOXML, no openpyxl. Final state: cover + 12 analytical sheets + deck-facing contract sheet, with 431 formulas (200 cross-sheet refs), all 14 sheets pass ZIP + XML integrity, every section banner has a gutter `x` collapse anchor, every data row carries `outlineLevel="1"`. Companion workbook to the methodology side deck (`sub_pptx/`).

---

## 1. Project housekeeping

- **Moved `submarine_outsourced_work/extracted/` → `sub_workbook/extracted/`** (46 CSVs + `nc_scope_summary.json`). The scaffold's `lib.py` defines `EXTRACTED = PROJECT_ROOT / "extracted"` where `PROJECT_ROOT` resolves to `sub_workbook/`; without the move every `load_extracted_csv` call would have either failed or required a hardcoded path override. Move keeps `sub_workbook/` self-contained.
- **Copied 2 EDGAR segment files** into `sub_workbook/extracted/` as `edgar_hii_nns.csv` and `edgar_gd_marine.csv`. These live under `submarine_outsourced_work/edgar_research/` originally; renamed-and-copied (not moved) because `edgar_research/` carries other artifacts (10-K HTML files, narratives, summary memos) that aren't worth dragging across.
- Flagged a tension worth noting: any rerun of the prior project's `submarine_outsourced_work/scripts/` will now write to a path that no longer exists in that subtree. Resolution deferred — those scripts are dormant.

## 2. Workbook design — 14 sheets, role-color taxonomy

Started from the methodology in `METHODOLOGY.md` (cost funnel, four denominators, MIB exclusion, 50/60/65% band, HII team-build, DoD POP, 8 data feeds, 10 guardrails) plus the 6-slide deck topics in `sub_pptx/slide_topics.md`.

The scaffold (`sub_workbook/workbook_submarines/`) already encoded a **6-color tab-role taxonomy** in `styles.py` that the prior 12-sheet workbook didn't use cleanly:

| Tab color | Role | Constant |
|---|---|---|
| Ochre | Editable inputs | `C_TAB_INPUTS` |
| Slate | Analytical calcs | `C_TAB_CALCS` |
| Dark green | Deck-facing contract | `C_TAB_DECKDATA` |
| Mid gray | Reconciliation | `C_TAB_CHECKS` |
| Dark navy | Citations | `C_TAB_SOURCES` |
| Burgundy | Research data dumps | `C_TAB_RESEARCH` |

The dark-green DeckData role was the architectural addition over the prior workbook — a single sheet the slide pipeline reads, decoupled from the analytical layer. The final sheet list:

| # | Tab | Role | Purpose |
|---|---|---|---|
| 1 | Cover | (none) | Sheet map, style key, 10 guardrails |
| 2 | References | Sources | Industry-baseline citations + exec commentary |
| 3 | Inputs | Inputs | 18 editable assumptions + 15-PIID reference table |
| 4 | SCN_Annual | Research | Per-class per-FY P-5c (incl. 5 GFE components) |
| 5 | LLTM_AP | Research | P-10 advance-procurement buckets FY20-FY31 |
| 6 | Subaward_Annual | Research | FFATA $ per PIID per FY (MIB-excluded floor) |
| 7 | MIB_Excluded | Research | BlueForge / TMG / IALR audit |
| 8 | Top_Vendors | Research | Top 50 in-scope parent UEIs |
| 9 | DoD_POP | Research | Place-of-performance %, dollar-weighted by program × work-type |
| 10 | Prime_10K | Research | HII NNS + GD Marine Systems segments FY19-FY25 |
| 11 | Funnel | Calcs | Per-class per-FY funnel + band scenarios |
| 12 | HII_TeamBuild | Calcs | MODELED HII team-build sub-portion (§9 guardrail) |
| 13 | Checks | Checks | 5 reconciliation rules with OK/FAIL status |
| 14 | DeckData | DeckData | 32 figures, the slide-facing contract |

## 3. Build phases

User asked for sheet-by-sheet build starting with the load-bearing trio (Inputs → DeckData → Funnel), then expand. Sequenced into four phases.

### Phase 1 — Load-bearing trio
- **Inputs** (`inputs.py`) — 18 editable inputs across 6 sections: outsourced band (IN-01..03 at 50/60/65%), HII team shares (IN-04 Va 50%, IN-05 Col 22%), HII sub-portion scenarios (IN-06..08 at 25/30/35%), FFATA lag uplifts (IN-09..12 FY23-FY26), scope (IN-13..18 line items + windows), and a 15-PIID reference table loaded from `nc_scope_summary.json`. Exposes `cell_ref('IN-NN')` → `Inputs!D{row}`.
- **DeckData** (`deckdata.py`) — 32 figures across 4 slide sections (S3 Scope, S4 Funnel headline, S5 Pipelines, S6 Band + supports). Built as a *contract* sheet — figures that didn't have producer sheets yet were rendered as blue `S_NUM_INPUT` placeholders with `"<producer> — pending wire-up"` in the source column, to be rewired as downstream sheets came online. Exposes `derived_cell('DD-SN-NN')`.
- **Funnel** (`funnel.py`) — per-class per-FY (FY22-FY27, the substantive-coverage window per §2). Block layout: raw P-5c (5 rows) → BC% derived → outsourced band (3 rows) → visibility split (floor + unseen). Started with raw P-5c values hardcoded blue from `cost_funnel_with_subawards.csv`; band/BC%/unseen all formula-driven. Exposes `funnel_cell(li, fy, metric)`.

Each sheet exposes an ID-based cell resolver so re-ordering rows on the producer only requires updating its offset map; every consumer follows automatically. This pattern repeated for every later sheet.

### Phase A — Research dumps that unlock the most wire-ups
Built four research sheets in priority order — each one let me delete a chunk of "pending wire-up" hardcoded blue values in Funnel and DeckData:

- **SCN_Annual** (`scn_annual.py`) — wide-format P-5c per class per FY with GFE components broken out. Loaded from `cost_funnel_with_subawards.csv`. Includes the CSV's `gfe_sum_$M` value verbatim (not a formula-driven sum of components — the script's computed `gfe_sum` doesn't exactly match the obvious sum of Propulsion + Electronics + HM&E + Ordnance + Other Cost, preserved per audit chain). Funnel's 5 raw P-5c rows refactored from blue hardcoded → green `S_LINK_NUM` cross-sheet refs to SCN_Annual (60 cells across Va + Col blocks).
- **Subaward_Annual** (`subaward_annual.py`) — section 1 per-class FY totals (formula SUMs of section 2), section 2 per-PIID detail (15 rows, hardcoded blue from `nc_annual_by_piid.csv`). Sort: Va (10 PIIDs) first, then Col (5 PIIDs). Funnel's FFATA-visible floor row rewired to read per-class totals from here; DeckData DD-S5-02 and DD-S5-06 wired to the grand-total cell.
- **MIB_Excluded** (`mib_excluded.py`) — 3-row audit table for the §8 guardrail exclusions. BlueForge ($4,173.27M) and TMG ($77.03M) loaded directly from `sam_subaward_top_parents.csv`; IALR ($1.50M) **derived** as JSON's `dollars_excluded_mib_$M` total minus BF and TMG (IALR is below the top-N cutoff in the parents CSV). DeckData DD-S6-04/05/06 rewired.
- **DoD_POP** (`dod_pop.py`) — full 42-row program × work-type table from `dod_action_pop_by_worktype.csv`, plus a SUMPRODUCT-weighted in-scope aggregate row at the bottom. POP %s converted from percentage-points (0-100) to decimals (0-1) at build time; dollars converted from raw USD to $M. An editable `In-Scope?` flag column (1/0) feeds the SUMPRODUCT — programs in {va, col, va_or_col, bpmi_nuclear} are flagged 1. DeckData DD-S5-04/05 wired to `=1-EB%` and `=1-EB%-HII%` respectively.

### Phase B — Funnel / DeckData refactors

Done implicitly as Phase A landed. End state:
- Funnel: 130 formulas. 60 cross-sheet refs to SCN_Annual (raw P-5c), 36 to Inputs (band scenarios), 10 to Subaward_Annual (FFATA floor for FY22-FY26 — FY27 is outside the FFATA window and renders blank), 24 within-sheet (BC%, unseen layer).
- DeckData: 25 formulas. 9 to Inputs, 9 to Funnel, 2 to Subaward_Annual, 2 to DoD_POP, 3 to MIB_Excluded. Of the 32 figures, 29 resolve through producer sheets; 3 remain hardcoded blue (DD-S6-07 HII +30%, DD-S6-08/09 Navy 10→50% — external anchors with no producer sheet, citations on References); 1 placeholder remains (DD-S5-03 floor coverage %, needs a methodology call on window alignment).

### Phase C — Remaining research + calcs
- **Top_Vendors** (`top_vendors.py`) — top 50 in-scope parent UEIs by cumulative $M. MIB UEIs filtered out before ranking so the table is the in-scope concentration view, not raw FFATA recipients.
- **LLTM_AP** (`lltm_ap.py`) — per-class per-FY (FY20-FY31) advance-procurement buckets. 10 buckets total (Plans/SIB, EOQ, Nuclear plant LLTM, Propulsor LLTM, Electronics LLTM, HM&E LLTM, Ordnance LLTM, Missile compartment LLTM, Shipbuilder-procured LLTM, Shipbuilder-procured LLTM (CFE)). Va has empty cells for Missile compartment + Ordnance buckets (not applicable to Va).
- **Prime_10K** (`prime_10k.py`) — HII NNS (revenue, op income, derived op margin) + GD Marine Systems (revenue, op income, op margin, capex, D&A, identifiable assets) FY19-FY25. Capex line is load-bearing for the "GD investing in own yards vs HII outsourcing" strategic-divergence framing in §9 / §11.
- **HII_TeamBuild** (`hii_teambuild.py`) — MODELED scenario per §9 guardrail. Per class: reads BC from Funnel (`S_LINK_NUM` green), computes implied portion (`= BC × team_share`), then sub-portion at Low/Mid/High scenarios (`= implied × 25/30/35%`). Section banner explicitly labels the block "MODELED" — never to be blended with observed Funnel data.

### Phase D — Orientation + audit + citations
- **References** (`references.py`) — section 1 industry-baseline citations from `industry_baseline_citations.csv` (~30 rows: CRS / GAO / Navy / OSD pillars), section 2 exec commentary from `exec_commentary_makebuy.csv` (~20 rows). Structured fields only (claim_id, label, value, unit, source_id, date); full quote text stays in the source CSVs to honor the workbook's no-wrap rule.
- **Checks** (`checks.py`) — 5 reconciliation rules with OK/FAIL status:
  - CHK-01: `Funnel!H10 == SCN_Annual!H18` (Va FY27 BC cross-sheet ref consistency)
  - CHK-02: same for Columbia
  - CHK-03: `Subaward_Annual!O8` (formula-driven grand total) == JSON-reported in-scope total ($6,139M)
  - CHK-04: `MIB_Excluded!D6+D7+D8` (sum of UEI Total $M) == JSON-reported MIB total ($4,251.80M) — verifies the IALR derivation
  - CHK-05: `Funnel!H11 == SCN_Annual!H21` (Va FY27 BC% cross-sheet consistency)
- **Cover** (`cover.py`) — sheet map + style key + 10 guardrails. No tab color (sits outside the role taxonomy).

## 4. Bug fixes (review-driven)

### Missing gutter `x` + outline_level
User flagged that section banners weren't displaying the gutter `x` collapse marker per the convention. Looked into `lib.py` and confirmed the pattern: section banners pass `mark_collapsible=True` (places `'x'` in column A) and data rows pass `outline_level=1` (joins them to a collapsible group below the banner). The prior 12-sheet project's `d_inputs.py` used this pattern; I had missed it on all three load-bearing sheets. Applied across Inputs, Funnel, DeckData (then carried into every later sheet). Final state: 6 `x` markers on Inputs, 6 on Funnel, 4 on DeckData, etc.; total **33 outlined rows** in Inputs, **22** in Funnel, **32** in DeckData.

### MIB_Excluded column-offset bug
User found calculation errors on MIB_Excluded. Root cause: `_bf()` / `_tmg()` / `_ialr()` cell helpers returned `MIB_Excluded!C{row}` referring to column C — but with `start_col=1`, column C holds the Name string (B=UEI, C=Name, **D=Total $M**, E=Action count, F=%). The per-row `% of total` formula and total-row SUM formulas all referenced the wrong columns. Shifted every column reference right by one. Also impacted Checks CHK-04 (which sums the three UEI cells) — fixed automatically once the helpers were corrected.

### Funnel `#DIV/0!` errors
Same review pass: Funnel showed `#DIV/0!` for Columbia FY22-FY25 BC% cells. Root cause: my `ISBLANK` guard returns FALSE for cells containing a cross-sheet ref (`=SCN_Annual!C26`), even when the source cell is genuinely empty. Excel evaluates the ref to 0, the IF condition `ISBLANK(=...)` is FALSE, and the formula falls through to `0/0` = `#DIV/0!`. Changed the guard from `ISBLANK(...)` to `... = 0` across the three formula types in Funnel (BC%, band scenarios, Unseen Mid). Same fix applied prophylactically to HII_TeamBuild.

### Cover column widths
User flagged columns C and D as wonky. Root cause: I set `cols=[18, 100, 4]` — column C (which was a short Role label) at width 100, column D (which held long descriptions) at width 4. The three sections were also inconsistent — sheet map put long text in D, style key + guardrails put long text in C. Restructured all three sections to put long text in D, set widths to `[34, 12, 90]`. Style key and guardrails rows now write `[label, "", long_text]` instead of `[label, long_text, ""]`.

### Checks CHK-03 was tautological
Initial CHK-03 had expected and actual formulas evaluating to the same expression, so delta was always 0 — a check that always passes is no check. Redesigned to: expected = JSON-reported `total_dollars_in_scope_$M` (hardcoded blue), actual = `=Subaward_Annual!O8` (the formula-driven grand total cell). Now meaningfully validates that the per-PIID rows + per-class formulas roll up to the ETL-reported aggregate.

### HII_TeamBuild `#VALUE!` errors
User reported `#VALUE!` errors after opening the workbook. Root cause: the implied row uses `=IF(BC=0, "", BC*team_share)` — returns the **string `""`** when BC is empty. The sub-portion row then references the implied row with `=IF(implied=0, "", implied*scenario)`. In Excel, `"" = 0` evaluates to FALSE (text vs number), so the FALSE branch runs `"" * 0.25` → `#VALUE!`. Fixed by changing the sub-portion guard from `... = 0` to `ISNUMBER(...)`, which returns FALSE for `""` and TRUE for a real number. 36 sub-portion cells now produce blank instead of `#VALUE!`.

### Checks font colors not following styling rules
Same review pass. Per the styling convention: pure `=Sheet!Cell` refs are green (`S_LINK_NUM` / `S_LINK_PCT`), hardcoded inputs are blue (`S_NUM_INPUT` / `S_PCT_INPUT`), derived formulas are black (`S_NUM` / `S_PCT`). My Checks rows used black `S_NUM` uniformly. Extended each `_CHECKS` tuple with an explicit `(expected_style, actual_style, delta_style)` triple. End state:
- CHK-01/02: green/green/black (pure refs)
- CHK-03: blue/green/black (hardcoded vs pure ref)
- CHK-04: blue/black/black (hardcoded vs derived sum of refs — sum-of-refs is derived, not pure-link, so black)
- CHK-05: green-italic/green-italic/black-italic (% comparison)

## 5. Style upgrade — total-row borders

User asked for top borders + bold treatment on LLTM_AP Class total rows, with a medium border weight (heavier than the header row's thin bottom underline). Applied `S_TOTAL` to the label cell and `S_NUM_TOTAL` to the numeric cells — these styles were already defined in `styles.py` with `borderId="2"` (medium top border) vs the header's `borderId="1"` (thin bottom). After confirming the result, user asked to apply the same treatment to MIB_Excluded's "Total (MIB exclusion)" row, which has the same rows-then-total pattern. Did so, including using `S_TOTAL` on the leading empty column B cell so the border line spans continuous across the row.

## 6. Architectural notes

### Stdlib-only OOXML
The `lib.py` primitives (cell, row, worksheet, banner_row, write_row, build_table, col_letter, cref) emit raw `<c>` / `<row>` / `<worksheet>` XML strings; no openpyxl, no xlsxwriter. Build packages each sheet into `xl/worksheets/sheetN.xml`, plus `[Content_Types].xml`, `_rels/`, `xl/styles.xml`, `docProps/`. `<calcPr fullCalcOnLoad="1"/>` set so Excel forces a full recalc on open.

### ID-based cross-sheet ref helpers
Every producer sheet exposes a typed cell-resolver:
- `inputs.cell_ref('IN-NN')` → `Inputs!D{row}`
- `scn_annual.scn_cell(li, fy, metric)` → `SCN_Annual!{col}{row}`
- `funnel.funnel_cell(li, fy, metric)` → `Funnel!{col}{row}`
- `subaward_annual.floor_cell(li, fy)` → `Subaward_Annual!{col}{row}` (per-class total)
- `subaward_annual.grand_total_cell()` → `Subaward_Annual!{Total_col}{Grand_row}`
- `mib_excluded.blueforge_cell()` / `tmg_cell()` / `ialr_cell()`
- `dod_pop.eb_pct_cell()` / `hii_pct_cell()`
- `deckdata.derived_cell('DD-SN-NN')` (for the slide pipeline)

Consumers import the helper and call it instead of hardcoding cell addresses. Re-ordering rows on a producer requires only an update to its offset map; every consumer follows.

### Sparse data handling
Three formula patterns coexist:
- For cells whose direct input is hardcoded blue (truly missing → no `<c>` element): `ISBLANK(...)` works (used on SCN_Annual BC% / GFE% derived ratios).
- For cells whose input is a cross-sheet ref (input cell has a formula, never blank even when ref'd source is empty): `... = 0` (used on Funnel BC% / band / unseen).
- For cells whose input might be the string `""` (cascading from a previous `IF(..., "", ...)`): `ISNUMBER(...)` (used on HII_TeamBuild sub-portion).

## 7. Final state

```
Building sub.xlsx with 14 sheets …
  sheet 1: Cover        11,343 bytes
  sheet 2: References   29,462 bytes
  sheet 3: Inputs       15,278 bytes
  sheet 4: SCN_Annual   11,404 bytes
  sheet 5: LLTM_AP      14,954 bytes
  sheet 6: Subaward_Annual   14,048 bytes
  sheet 7: MIB_Excluded    2,901 bytes
  sheet 8: Top_Vendors   19,607 bytes
  sheet 9: DoD_POP      22,196 bytes
  sheet 10: Prime_10K     6,005 bytes
  sheet 11: Funnel       12,496 bytes
  sheet 12: HII_TeamBuild    7,099 bytes
  sheet 13: Checks        3,916 bytes
  sheet 14: DeckData     14,656 bytes
Wrote sub.xlsx (37,415 bytes)
```

- All 14 sheets pass `zipfile.testzip()` and `xml.etree.ElementTree.parse()`.
- 431 formulas total; 200 cross-sheet refs.
- 5 Checks rows all evaluate (CHK-01..05).
- Outline collapse + gutter `x` markers on every section banner.

## 8. Known issues / future work

1. **DD-S5-03 (Floor coverage %)** still hardcoded blue at 0.0. Needs a methodology call on window alignment — the FFATA floor cumulative is FY16-FY26 while the Funnel outsourced layer is per-FY, so a single coverage % requires picking the comparison window. Punted.
2. **`gfe_sum_$M` reconciliation gap**: the CSV's pre-computed `gfe_sum_$M` doesn't equal the obvious sum of (Propulsion + Electronics + HM&E + Ordnance + Other Cost) — there's an unexplained adjustment in the upstream `build_cost_funnel.py` script. SCN_Annual preserves both the components AND the CSV's `gfe_sum` verbatim per audit chain. A Checks rule "SCN P-5c rollup gap (Va FY27)" would surface this; not yet added.
3. **Prior project's `submarine_outsourced_work/scripts/` paths**: those CSV-producing scripts write to `extracted/` which no longer exists at the path they expect. If anyone reruns them, they'll either fail or create a fresh `extracted/` dir. Either point them at the new location or document the dormancy.
4. **No visual verification in Excel**: I can't run Excel from this environment. The workbook passes static XML validation but Excel sometimes flags "repaired records" for issues static analysis misses. User confirmed clean visual after opening (modulo the bugs above that were then fixed).
5. **Tab color on Cover**: intentionally `None` so Cover sits outside the role taxonomy. Renders with Excel's default tab color.

## Artifacts

- `sub_workbook/sub.xlsx` — 37KB, 14 sheets
- `sub_workbook/workbook_submarines/sheets/` — 14 sheet modules + `sheet_template.py`
- `sub_workbook/workbook_submarines/lib.py` (unchanged this session — primitives only)
- `sub_workbook/workbook_submarines/styles.py` (unchanged — palette + cellXfs definitions)
- `sub_workbook/extracted/` — 48 CSVs + 1 JSON (relocated this session from `submarine_outsourced_work/extracted/` + EDGAR copies)
