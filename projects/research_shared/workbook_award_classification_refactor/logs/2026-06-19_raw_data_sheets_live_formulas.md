# 2026-06-19 — Raw data pulls as sheets + live-formula roll-ups

Ported the underlying subaward **raw data pulls into the workbook as their own
sheets** and rewrote the program-vendor sheets' hardcoded roll-up columns as **live
Excel formulas** over those sheets. The vendor sheets are now a thin *derived* layer
(`model` group) over an in-workbook *source* layer (`data` group), mirroring
`workbook_award_analysis` (leaf `data_lane_vendors` → derived `model_by_vendor`).
Workbook grew from 5 → **10 sheets**. Build green. Follow-on to
`2026-06-19_program_vendor_refactor.md`.

---

## §1 — The reframe (why this session happened)

Last session's three program-vendor sheets carried four roll-up columns —
`Subaward $M`, `Subaward Actions`, `First Subaward`, `Last Subaward` — as **hardcoded
values** computed in Python by `scripts/build_program_vendors.py`. Those aggregates
don't appear "like that" in any raw pull, violating the house rule that only
leaf/source data is hardcoded and every aggregation is a live formula (memory
`derived-metrics-live-formulas`).

User ask: (a) bring the raw data pulls into the workbook as sheets so the numbers are
traceable in-workbook, and (b) rewrite the roll-up columns as live formulas
referencing them. Mid-session the user noticed the domestic/foreign flag is already
present per-transaction in the raw pull, so **Domestic or Foreign was also converted
to a formula** and the redundant **Subawardee Origin dimension sheet was deleted**.

---

## §2 — Final sheet inventory (10 tabs, 3 layers)

| Group | Tab | Grain / source |
|---|---|---|
| guide | Taxonomy · Methodology | unchanged |
| **model** | DDG / Virginia / Columbia **Program Vendors** | 1 row per UEI; 5 derived columns are live formulas (group moved `data`→`model`) |
| **data** | DDG / Virginia / Columbia **Subaward Transactions** | 1 row per `report_id` (the fact spine) |
| **data** | **Subawardee UEI Index** | 1 row per (UEI × program) + primary NAICS-6 + description |
| **data** | **Subawardee Parents** | 1 row per (UEI × program): parent name + raw parent UEI(s) |

Tab color/order is enforced by `workbook_core.groups` (guide < model < data); the
program-vendor sheets are now `group="model"` (a derived cut sits ahead of the
evidence dump), matching `award_analysis`.

**Deleted this session:** `Subawardee Origin` sheet — its Domestic/Foreign became a
vendor-sheet formula and Country lives per-transaction on the tx sheets, so the
roll-up sheet would only be a stale copy.

---

## §3 — The five live formulas (vendor sheets)

Each is keyed on the row's Subawardee UEI (vendor-sheet **column B**) over the
matching program's **Subaward Transactions** leaf. Each corpus record is one distinct
`report_id`, so `COUNTIFS` == the distinct action count; dates are real serials, so
`MINIFS`/`MAXIFS` are well-defined; the tx flag is per-transaction, so the foreign
majority is a plain `IF` over two `COUNTIFS`.

| Vendor column | Formula (tx ranges abbreviated) |
|---|---|
| Subaward $M | `=SUMIFS(tx[$M], tx[UEI], $B{r})` |
| Subaward Actions | `=COUNTIFS(tx[UEI], $B{r})` |
| First Subaward | `=_xlfn.MINIFS(tx[Date], tx[UEI], $B{r})` |
| Last Subaward | `=_xlfn.MAXIFS(tx[Date], tx[UEI], $B{r})` |
| Domestic or Foreign | `=IF(COUNTIFS(tx[UEI],$B{r},tx[D/F],"Foreign")>COUNTIFS(tx[UEI],$B{r},tx[D/F],"Domestic"),"Foreign","Domestic")` |

`MINIFS`/`MAXIFS` carry the `_xlfn.` prefix (Excel-2016 future-function rule, per
`award_analysis`). Derived numeric/date cells render **black** (`S_NUM`/`S_INT`/
`S_DATE`); the text D/F formula stays `S_DEFAULT`. The packager already sets
`<calcPr fullCalcOnLoad="1" forceFullCalc="1"/>`, so Excel computes on open (no
cached `<v>`; no manual F9).

All other vendor columns remain hardcoded leaf: UEI, NAICS-6 + desc, Parent UEI
(blank), Parent name, Subawardee name, archetype/basis (blank), Role/Description,
Source URLs.

---

## §4 — Files built / changed / deleted

**New — extraction scripts** (`scripts/`)
- `build_program_transactions.py <ddg|virginia|columbia>` → `extracted/<program>_subaward_transactions.csv`,
  one row per deduped `report_id` (blank-UEI records dropped, so per-UEI roll-ups
  reconcile to the vendor sheets). Same scope/dedup as `build_program_vendors.py`.
- `build_uei_dimensions.py` → `extracted/subawardee_uei_index.csv` +
  `subawardee_parents.csv` (UEI × program). Imports the NAICS loaders from
  `build_program_vendors.py` so NAICS-6 precedence matches the vendor sheets.

**New — sheet modules** (`sheets/`)
- `ddg_subaward_transactions.py`, `virginia_subaward_transactions.py`,
  `columbia_subaward_transactions.py` — leaf tx sheets; **export `*_tx_cols`
  accessors** (`cols(header) → "'Tab'!$X$f:$X$l"`).
- `subawardee_uei_index.py`, `subawardee_parents.py` — plain leaf dimension sheets.

**Changed**
- `sheets/_flat.py` — `make_flat_sheet` extended: new `date_cols`, `input_cols`,
  `formula_cols={header: fn(r)->"=..."}` params; per-column style resolution
  (formula→black derived, input→blue, typed-leaf→black, else `S_DEFAULT`); **now
  returns `(SheetEntry, cols)`** where `cols(header)` gives the absolute data range.
- `sheets/_cuts.py` — added `_EPOCH` + `date_serial` (ISO → Excel serial), copied
  from `award_analysis`.
- `sheets/_widths.py` — added `W_PIID`, `W_REPORTID`, `W_DATE`, `W_PROGRAM`,
  `W_COUNTRY`, `W_FY`.
- `sheets/_tabs.py` — added 5 tab constants (3 tx + UEI index + parents).
- `sheets/{ddg,virginia,columbia}_program_vendors.py` — `group="data"`→`"model"`;
  import the program's `*_tx_cols`; pass `formula_cols` (5 columns) + `date_cols`
  for First/Last; unpack `(entry, _)`.
- `sheets/__init__.py` — imports + `SHEETS` reordered guide → model → data.

**Deleted**
- `sheets/subawardee_origin.py`, `extracted/subawardee_origin.csv`; plus the
  `TAB_ORIGIN` constant and the origin generation in `build_uei_dimensions.py`.

**Left untouched**
- `scripts/build_program_vendors.py` — still the source of truth for the vendor
  CSVs' non-formula columns + its reconciliation report.

---

## §5 — Build / extraction commands

```bash
cd projects/research_shared/workbook_award_classification_refactor
# raw transaction fact CSVs (one per program; each prints a $M-vs-corpus reconcile)
for p in ddg virginia columbia; do python3 scripts/build_program_transactions.py $p; done
# per-UEI dimension CSVs (UEI index + parents)
python3 scripts/build_uei_dimensions.py
# build the workbook (writes ../award_classification_refactor.xlsx)
python3 build_workbook.py
# structural QA (openpyxl): xml errors + error-literal scan
python3 validate_workbook.py
```

---

## §6 — Raw transaction sheet schema (13 cols, per program)

`Subawardee UEI · Subawardee Vendor Name · Parent UEI · Parent Vendor Name ·
Prime PIID · Subaward Report ID · Subaward Date · Subaward $M · Domestic or Foreign ·
Country · NAICS-4 · NAICS-4 Description · FY` — maps 1:1 to corpus record fields
(`entity_uei, vendor, parent_uei, parent_name, piid, report_id, date[:10], dollar_m,
foreign→"Domestic"/"Foreign", country, naics4, naics_desc, fy`).

Column letters (with the gutter): UEI=**B**, $M=**I**, Date=**H**, Dom/For=**J** —
these are what the vendor formulas reference. `Subaward $M` is a blue numeric input
(`S_NUM_INPUT`); `Subaward Date` is a blue native-date serial (`S_DATE_INPUT`).

Provenance gotcha: per-transaction `Domestic or Foreign` is a 1:1 recode of the raw
SAM `entityPhysicalAddress.country.code` via `_corpus.is_foreign` (USA→Domestic, else
Foreign). The separate `Country` column is the NAICS-enrichment country, patchier
(USA / "-" / ITA / "Foreign" / CAN / FRA …), so the foreign flag is the more complete
of the two — that's why the foreign formula reads the **D/F** column, not Country.

---

## §7 — Volumes & verification

**Volumes (this build):**
| Program | Transactions | Distinct UEIs | $M (= corpus, to the cent) |
|---|---|---|---|
| DDG | 6,380 | 470 | 3,604.198 |
| Virginia | 8,465 | 645 | 5,118.693 |
| Columbia | 5,916 | 595 | 4,444.805 |
| UEI dimensions | — | 1,215 distinct (1,710 UEI×program rows) | — |

0 blank-UEI records dropped in any program (so tx total == vendor total exactly).

**Checks (all green):**
- **Formula-equivalence (Excel-free):** grouping each tx CSV by UEI reproduces the
  vendor CSV's `$M` (±1e-6), `Actions`, `First`, `Last` — **0 mismatches**, identical
  UEI sets (no missing/extra) across all three programs.
- **Domestic/Foreign:** the `COUNTIFS`-majority reproduces the prior hardcoded value
  — **0 mismatches** across all three programs.
- **Built-file spot checks:** vendor formula cells hold the correct cross-sheet
  ranges (e.g. DDG `$I$7:$I$6386`; Virginia `…$8471`; Columbia `…$5922`); tx leaf
  date reads back as a real `datetime`, `$M` as a real float.
- `validate_workbook.py`: 10 sheets, **0 XML errors, 0 error-literal cells**, 8
  native tables.

---

## §8 — Decisions made (resolved this session)

- **Dimension grain = (UEI × program)** — a UEI active on two programs appears once
  per program (Program column distinguishes); the union over the three vendor sheets
  is reproduced exactly (1,710 rows).
- **Vendor sheets moved `data`→`model`** — they are derived cuts now; matches the
  groups doc and `award_analysis` (calc before evidence).
- **Master-index NAICS-6 = reference-`is_primary` → SAM fallback → title backfill**
  (the same value the vendor sheets show), not SAM-only.
- **NAICS / parent / names stay hardcoded leaf** on the vendor sheets (they *are*
  listed in the raw pulls). Vendor names are dollar-weighted modes with no clean
  formula equivalent — intentionally not formula-ized.
- **Domestic/Foreign converted to a formula; Origin sheet deleted** (mid-session, at
  the user's call, once the per-transaction flag was confirmed in the raw pull).

---

## §9 — Open work / next-agent notes

- **(A) Subawardee Parents sheet** — by the same redundancy logic, parent UEI +
  parent name are both per-transaction in the tx sheets; the dimension sheet only
  uniquely adds the deduped *set* of parent UEIs per vendor. KEPT for now; user may
  drop it. (The **UEI Index stays** regardless — primary NAICS-6 is entity-level SAM
  data not in the tx pull, which only has NAICS-4.)
- **(B) Archetype-assignment pass** — still the gating phase from last session: cols
  `Capability Domain (D)` / `Primary Output (P)` + the two Basis cols are blank,
  awaiting a NAICS-6→archetype map with a vendor-registry override.
- **(C) Parent UEI** (vendor col 4) — still blank pending a standardized parent-UEI
  list; raw parent UEIs are now visible on the Parents sheet.
- **(D) Optional dedup** — the vendor-sheet NAICS/parent/foreign-source columns could
  later become `XLOOKUP`s into the dimension sheets to remove duplication; out of
  scope now.
- **(E) Port to `workbook_award_analysis`** — this leaf-tx + live-rollup model is the
  intended replacement for its single `vendors` sheet.

---

## §10 — Conventions / gotchas (this session)

- **Dollars/actions/dates only from `_corpus`** (memory `canonical-corpus-source`);
  enrichment files are attribute lookups only.
- **`make_flat_sheet` now returns `(entry, cols)`** — every caller must unpack;
  leaf/tx sheets keep `cols`, vendor/dimension sheets discard it (`entry, _`).
- **Formula columns are NOT read from the CSV** — `formula_cols[header]` is a
  `fn(r)->"=..."` callable resolved by `RowCursor.write` against the row; the CSV's
  values for those columns are ignored (the build script still computes them for its
  reconciliation report).
- **Edit headers in the build scripts**, not the renderers; tx/dimension renderers
  only carry `_WIDTHS` (must equal column count) + which cols are float/date/input.
- Build green = done; user verifies visually (memory `no-png-render-verification`).
