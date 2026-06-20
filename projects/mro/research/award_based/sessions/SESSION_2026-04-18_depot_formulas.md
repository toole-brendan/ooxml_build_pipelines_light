# Session 2026-04-18 (pt 3): Depot Ship Repair -> live formulas - v2.71 -> v2.73

## Context

Third same-day session on Depot Ship Repair. User opened v2.69/v2.71 and
noticed the numbers on the sheet were baked-in Python values, not
references to the underlying data -- "not references from the data sheet
files and there's no formulas being used at all." Asked whether a new
data sheet was needed since the J998/J999 classification dimensions
(availability type/group, RMC, contractor tier, IDV scope) aren't on the
unified Awards schema.

pt 1 (`SESSION_2026-04-18_depot_ship_repair.md`) had intentionally written
static values -- docstring on the module called it out as "a
report/snapshot, not a live driver." That decision is reversed here.

Ended at **v2.73** with a new `J998 J999 Data` sheet wrapping the 2,861
classified awards in an Excel Table, and the Depot Ship Repair sheet
rewritten so every numeric cell is a SUMIFS / COUNTIFS against that
table. One round-trip on a structured-reference escape bug
(`[# Mods]` -> `[Mod Count]`) before Excel stopped stripping formulas on
open.

---

## Decision: new data sheet vs folding into Awards

Two options on the table:

1. **New dedicated data sheet** -- one row per J998/J999 award, all
   classifier columns as separate fields.
2. **Extend the Awards master** with availability/RMC/tier/scope columns
   set empty for non-J998/J999 rows.

Picked (1). Three reasons:
- The classifier columns only apply to ~2 PSC codes; pushing them onto
  the shared Awards schema leaves ~20k rows with empty fields.
- The data source is a separate JSON pipeline
  (`data_pull/classify_j998_j999.py`) with its own cadence.
- The Awards master applies `is_shore_base_excluded` which strips FMS
  rows; the Depot Ship Repair TAM wants the gross + FMS carve-out,
  so it needs the pre-exclusion extract.

---

## Work completed, in order

### 1. New `sheets/j998_j999_data.py`

Mirrors the `sheets/awards.py` pattern:
- Reads `data_pull/output/fpds/j998_j999_classified.json` (falls back to
  in-memory classification from the raw JSON if the classified file is
  missing -- same guard as the old `_load_awards` in depot_ship_repair).
- Normalizes `service` from `'navy'` / `'cg'` to `'Navy'` / `'Coast Guard'`
  to match the Awards sheet's title-case convention.
- Augments each row with `corporate_parent` (via
  `sheets.services.consolidate_parent`) and `vessel_category` (via
  `sheets.vessel_taxonomy.vessel_category_for` with an
  IDV-scope-type fallback for awards whose `hull_program` is empty --
  carried over from pt 2's IDV_SCOPE_TO_CATEGORY dict, but now lives
  here as the single source of truth).
- Writes 28 columns as an openpyxl `Table` with
  `displayName='J998J999Data'`.
- Loader memoized so depot_ship_repair.py and the data-sheet writer
  don't each re-parse the 11 MB JSON.

### 2. `sheets/depot_ship_repair.py` rewrite

Swapped the Python aggregation helpers (`_sum_m`, `_count`, `_crosstab_m`)
for formula builders against the J998J999Data table:

```
=SUMIFS(J998J999Data[FY2025 Obligation],
        J998J999Data[Availability Group],"Drydocked Availability")/1000000
=COUNTIFS(J998J999Data[RMC],"SWRMC")
=SUMIFS(J998J999Data[Mod Count],J998J999Data[PSC],"J998")
```

Sections rewritten (every numeric cell is a formula):
- TAM headline (J998/J999 split, FMS carve-out, in-scope TAM)
- Availability Group rollup
- Availability Type rollup
- Vessel Category rollup
- Contractor Tier rollup
- IDV Scope Group rollup
- IDV Scope Type rollup
- RMC rollup (with Geography column)
- 5 crosstabs (AG x Hull, RMC x AG, Tier x AG, VesselCat x IDV Scope,
  IDV Scope Group x AG, IDV Scope Group x Tier)
- Lead Prime per RMC (parent name Python-picked, $ + % live formulas)
- Top Contractors per Tier (same pattern)
- Top 15 Task Orders ($M keyed on PIID, which is unique on the data
  sheet, so SUMIFS resolves to that single row's obligation)

Row/column *visibility* (hide_empty filtering, top-N rankings) is still
Python-decided from the loaded awards -- only the displayed values are
formulas. Percent and average cells reference the total-row cell by
coordinate (back-filled after the total row is known) so the sheet is
internally consistent if any filter changes downstream.

**Top 15 Parent IDVs** is the one Python-rendered $ block left on the
sheet. Each task order can reference multiple parent IDVs; the existing
roll-up apportions the award's $ equally across them. That's not
expressible as a single SUMIFS against a one-row-per-PIID data sheet.
Section title now flags this inline: `"(MAC-MO / MSRA Ecosystem,
static - apportioned allocation)"`.

### 3. Build + verification (v2.71 -> v2.72)

Built v2.72. Spot-check via openpyxl:
- 1,244 formula cells vs 60 literal numeric cells on Depot Ship Repair.
- The 60 literals exactly account for Rank columns (Top 15 Task Orders
  + Top 15 Parent IDVs = 30) + Parent IDVs descriptive columns
  (# TOs + $M = 30) = 60. Matches intent.

### 4. Bug fix: `[# Mods]` stripped by Excel (v2.72 -> v2.73)

Opening v2.72 surfaced:

> Removed Records: Formula from /xl/worksheets/sheet4.xml part

sheet4 = Depot Ship Repair (4th in workbook order). Root cause:
structured-reference column `[# Mods]`. The `#` character has special
meaning inside `[]` in a structured reference (it's reserved for item
specifiers like `[#Headers]`, `[#Data]`, `[#Totals]`, `[#This Row]`).
A literal `#` in a column name must either be escaped with a leading
apostrophe (`['# Mods]`) or the header itself should avoid `#`.

Picked the latter. Renamed the data-sheet column `# Mods` -> `Mod Count`
in `sheets/j998_j999_data.COLUMNS`, updated `_FIELD_TO_COL` and
`_MODS_REF` in `sheets/depot_ship_repair.py`. Rebuilt v2.73. openpyxl
verification: 0 remaining `[# Mods]` refs, 17 new `[Mod Count]` refs.
User confirmed Excel opens v2.73 clean.

Grep confirmed no other part of the codebase references any
`Awards[#...]` style column, so this was the only bit of the pipeline
hitting the escape issue. Awards.py does define columns named `# Hulls`
and similar, but nothing SUMIFS against them.

---

## Files created

- `sheets/j998_j999_data.py` -- new data sheet builder (2,861 rows x
  28 cols, wrapped as openpyxl Table `J998J999Data`).

## Files modified

- `sheets/depot_ship_repair.py` -- full rewrite to emit SUMIFS /
  COUNTIFS formulas. Removed `_load_awards`, `_load_idv_taxonomy`
  (moved taxonomy loader in-place), `_sum_m`, `_count`, `_crosstab_m`,
  `IDV_SCOPE_TO_CATEGORY` (moved to j998_j999_data.py). Imports
  `load_rows` + `TABLE_NAME` from the new data-sheet module.
- `build_from_data.py` -- import and call `create_j998_j999_data` after
  `create_awards` in the Data Sheets block; slate tab color on the new
  sheet.
- `README.md` -- added `j998_j999_data.py` to the sheets listing per
  the CLAUDE.md structural-change rule.
- `CLAUDE.md` -- updated the Depot Ship Repair Notes bullet to
  describe the new live-formula architecture and the one Python-
  rendered block.

## Files unchanged

- `data_pull/classify_j998_j999.py` -- classifier pipeline untouched;
  the same JSON artifact feeds the new data sheet.
- `data_pull/classify_j998_j999_idv_scope.py` -- untouched.
- `docs/research/J998_J999_RESEARCH.md` -- numbers unchanged from
  v2.69 (this session only changed how values are stored, not what
  they are).

## Memories added

None.

---

## Workbook progression

| Version | Change | Impact |
|---|---|---|
| v2.71 -> v2.72 | New J998 J999 Data sheet + depot_ship_repair rewrite to SUMIFS | Depot Ship Repair: 1,244 formula cells, 60 literal numerics (all from top-N ranking rows -- rank numbers + apportioned Parent IDV block). Excel flagged `[# Mods]` formulas as removed on open. |
| v2.72 -> v2.73 | Rename `# Mods` -> `Mod Count` on data sheet + refs | 17 formulas now reference `[Mod Count]` cleanly. Excel opens without the recovery-log warning. |

v2.73 is current.

---

## Open flags

- **Top 15 Parent IDVs is still Python-rendered $.** Documented inline
  on the section title. Could be made live if the data sheet switched
  to one-row-per-(PIID, parent_idv) grain with apportioned $ baked
  in at data-sheet write time, but that breaks the "one row per task
  order" invariant the other sections rely on. Not worth fixing unless
  the IDV-vehicle ranking becomes deck-facing.

- **Tier header bands no longer show the tier total $M inline.** The
  previous version embedded `${tier_m:,.0f}M total` in the
  subsubsec_band label; the formula version dropped that so the
  section band stays a clean heading. The tier total is implicit in
  the `% of Tier` denominator but isn't surfaced as a visible number.
  If we want it back, the cleanest path is a dedicated tier-total
  row written with `_sumifs_m(contractor_tier=tier)` right under the
  band.

- **Services sheet long-name formula-length guardrail** (pt 1 open
  flag) -- still untouched. Not related to this session but worth
  revisiting when we touch Services next.
