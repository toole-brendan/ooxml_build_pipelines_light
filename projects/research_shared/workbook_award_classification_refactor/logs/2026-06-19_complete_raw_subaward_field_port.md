# 2026-06-19 — Complete raw subaward field port (tx sheets) + vendor link styling + width floor

Three pieces this session, in order: (1) **green link-font** on the vendor roll-up
columns that surface tx-sheet values; (2) a **column-width floor** pass; and the
headline — (3) **rebuilt the three Subaward Transactions sheets as faithful raw
FSRS pulls**: every field on the `published` subaward record (28 fields → **50 leaf
columns**), the SAM-enrichment columns removed, and the vendor roll-ups rewired to
the new raw columns. Build green, all roll-ups reconcile 0-mismatch. Follow-on to
`2026-06-19_raw_data_sheets_live_formulas.md`.

---

## §1 — The reframe (why the port happened)

Last session's tx sheets carried `NAICS-4`, `NAICS-4 Description`, and `Country` as
if they were transaction-level facts. They're not: a subaward record has **no NAICS
at all** — those came from a separate SAM entity-registration enrichment
(`entity_naics_lookup.csv`), joined by UEI and constant per UEI. The user flagged
the "Transactions" sheets as misleading (entity-dimension data denormalized onto the
fact rows — a star-schema violation).

Resolution: make the tx sheets a **faithful raw pull** of the FSRS `published`
record (all real fields, nothing enrichment-derived), and leave the subawardee's
NAICS-6 on the entity dimension (Subawardee UEI Index). User directive: *every data
field on the record becomes a column, even if every value is blank.*

---

## §2 — Scope / post-filter (unchanged record set)

Rows are the **canonical corpus** set — identical to `_corpus.iter_records`:
in-scope new-construction PIIDs, DDG restricted to shipbuilder-directed groups,
**MIB/BlueForge UEIs stripped**, report-id deduped. Confirmed against the source:

- **BlueForge already out** — `BLUEFORGE ALLIANCE` (UEI `F8PEZKXES8B1`) sits in the
  submarine `excluded_mib_ueis` set (+ Training Modernization Group + Institute for
  Advanced Learning); DDG has none. The corpus docstring: "strips MIB/BlueForge."
- **GFE prime contracts out** at the PIID-scope level (handoff decision #3).
- **GFE *subaward* vendors (`gfe_sib`) kept** per user call ("leave them in"):
  DDG 20 / $3.3M, Virginia 14 / $4.2M, Columbia 65 / $391.8M. All other roles
  (`supplier`, `service`, `mission_systems`, `foreign_fms`, `prime`, `co_prime`,
  `holding`) retained too.

Counts unchanged: **DDG 6,380 · Virginia 8,465 · Columbia 5,916**. The new extractor
walks the raw JSON directly (reusing `load_scope`, not mutating `_corpus`) and
**asserts $ + count reconcile to `iter_records`** (Δ = 0.00e+00 all three programs).

---

## §3 — The 50-column schema (28 record fields, faithfully expanded)

Nested objects → one column per leaf; the two array fields → joined leaves
(`"; "`-delimited); always-blank fields kept as columns. UEI is **column B** (sort +
join key). Groups:

| Group | Cols | Fields |
|---|---|---|
| Subawardee entity | 5 | UEI · Vendor Name · DBA Name · Parent UEI · Parent Vendor Name |
| The subaward | 7 | Report ID · Report Number · Subaward Number · Subaward Date *(date)* · Submitted Date *(date)* · Subaward Amount $ *(num)* · Subaward Description |
| Subawardee address (`entityPhysicalAddress`) | 9 | Street · Street 2 *(≈99% blank)* · City · Congressional District · State Code · State Name · Country Code · Country Name · ZIP |
| Business types (`subBusinessType[]`) | 2 | Codes · Names *(joined)* |
| Top-pay execs (`subTopPayEmployee[]`) | 2 | Salaries · Employee Names *(joined; ~6% of rows)* |
| Prime context | 11 | Prime PIID · Prime Contract Key · Agency ID · **Referenced IDV PIID** *(always blank, kept)* · **Referenced IDV Agency ID** *(always blank, kept)* · Prime Award Type · Total Contract Value $ *(num)* · Base Award Date Signed *(date)* · Prime Entity UEI · Prime Entity Name · Description of Requirement |
| Prime NAICS (`primeNaics`) | 2 | Code · Description |
| Prime org (`primeOrganizationInfo`) | 12 | Funding & Contracting × Agency/Office/Department × code+name |

**Not given a column:** the two array *parent* keys (`subBusinessType`,
`subTopPayEmployee`) — represented by their leaf columns, not redundant empty
scalars. **Removed from tx (enrichment / derived, not raw):** `NAICS-4`,
`NAICS-4 Description`, enrichment `Country`, `FY`, and the derived
`Domestic or Foreign` flag.

Typing: `Subaward Amount $`, `Total Contract Value $` → float; the three dates →
native serials; all are blue **input** (hardcoded source). Everything else text
(black); blank kept-fields render as real empty cells.

---

## §4 — Vendor roll-ups rewired (still reconcile exactly)

The five live formulas keep their headers but re-target the new raw columns:

| Vendor column | Formula change |
|---|---|
| Subaward $M | `=SUMIFS(tx[Subaward Amount $], tx[UEI], $B{r})/1000000` (raw dollars → millions) |
| Subaward Actions | unchanged (`COUNTIFS` over UEI) |
| First / Last Subaward | unchanged (`_xlfn.MINIFS`/`MAXIFS` over Subaward Date) |
| Domestic or Foreign | foreign-majority over raw **Country Code**: `=IF(COUNTIFS(UEI,$B{r},CC,"<>USA",CC,"<>")>COUNTIFS(UEI,$B{r},CC,"USA"),"Foreign","Domestic")` — exact recode of `_corpus.is_foreign` (code not USA/blank; ties → Domestic) |

`$M` stays black (a genuine aggregate total); Actions/First/Last stay **green**
(`S_LINK_*`, surface tx-sheet values — see §6); D/F is black text.

---

## §5 — Files built / changed

**Rewritten**
- `scripts/build_program_transactions.py` — raw-JSON walker (canonical scope via
  `load_scope`, MIB strip, dedup), 50-column `COLUMNS` schema (`g()` nested-get +
  `jl()` array-join), asserts $ + count reconcile to `iter_records`. No longer uses
  the enrichment.
- `sheets/{ddg,virginia,columbia}_subaward_transactions.py` — 50-column `_WIDTHS`,
  `float_cols`/`date_cols`/`input_cols`; still export `*_tx_cols` accessors.

**Changed**
- `sheets/_widths.py` — **+16** raw-field width constants (`W_UUID`, `W_SUBNUM`,
  `W_AMOUNT`, `W_TCV`, `W_STREET2`, `W_CITY`, `W_CD`, `W_STATE`, `W_CC`, `W_ZIP`,
  `W_BIZCODE`, `W_PAY`, `W_CONTRACTKEY`, `W_REFIDV`, `W_AWARDTYPE`, `W_ORGCODE`);
  plus the §7 width-floor bumps. (`W_FY` now unused — harmless.)
- `sheets/{ddg,virginia,columbia}_program_vendors.py` — `$M` `/1000000`, D/F over
  Country Code, accessor headers (`Subaward Amount $`, `Country Code`); plus the §6
  `link_cols` (green) addition.
- `sheets/_flat.py` — added `link_cols` param + 3-tuple `_STYLE_BY_TYPE`
  (black/blue/green); the green-text branch was added then reverted (see §6).

**Created then deleted** (same session)
- `sheets/_link_text.py` — scoped green-**text** style for a briefly-green D/F;
  removed when D/F reverted to black.

---

## §6 — Vendor link styling (green) — the first piece

Per the workbook_core convention (blue input / black derived / **green = cross-sheet
link**), the user superseded to make the roll-up columns that *surface* a tx-sheet
value render green: **Subaward Actions** (`S_LINK_INT`), **First / Last Subaward**
(`S_DATE_LINK`). `$M` stays **black** (a new aggregate total, not a surfaced value).
Mechanism: new `link_cols` param on `make_flat_sheet` → green link style instead of
the default black derived style.

`Domestic or Foreign` was briefly greened too (needed a green-**text** style, since
the system reserves color for numerics — added scoped `S_LINK_TEXT` via the `_yn.py`
append-to-`CELL_XFS` pattern), **then reverted to black** at the user's call; the
`_link_text.py` module and its `_flat.py` wiring were removed, restoring the
"color = numeric cells only" rule.

---

## §7 — Column-width floor — the second piece

Diagnosis: the "too narrow" feel was **header clipping**, not data. Applied a floor
of **10** + header-fit bumps in `_widths.py`: `W_RANK`/`W_CAGE`/`W_CODE`/`W_FY` → 10,
`W_NAICS` → 11, `W_COUNT` → 13, `W_DOLLAR` → 12, `W_DATE` → 14, `W_CONF` → 15,
`W_DOMFOR` → 20. Wide prose/name columns left as-is. (Recommendation 2 — header
renames for the few long-header/short-data columns — was deferred.)

---

## §8 — Build / extraction commands

```bash
cd projects/research_shared/workbook_award_classification_refactor
# raw 50-column transaction CSVs (all three; each asserts reconcile to iter_records)
python3 scripts/build_program_transactions.py            # ddg virginia columbia
# build the workbook (writes ../award_classification_refactor.xlsx)
python3 build_workbook.py
# structural QA
python3 validate_workbook.py
```

---

## §9 — Verification (all green)

- **Extraction reconcile:** raw-walk $M == `iter_records` $M to the cent, Δ = 0.00e+00
  (DDG 3,604.197717 · Virginia 5,118.693071 · Columbia 4,444.804788); 0 blank-UEI
  dropped; 50 columns each.
- **Formula-equivalence (Excel-free):** recomputed all five vendor roll-ups from the
  new tx CSVs vs. the prior vendor values — **0 mismatches on $M, Actions, First,
  Last, and D/F across all three programs**, UEI sets identical (470 / 645 / 595).
- **Built-file spot checks:** tx col B = `Subawardee UEI`; enrichment headers absent;
  `Subaward Amount $`/dates render blue (real float/serial); blank kept-fields empty;
  vendor `$M` = `SUMIFS($L…)/1e6`, D/F = `COUNTIFS($T…)`; array fields joined
  (`2X; MF`, 5 joined exec salaries).
- `validate_workbook.py`: 10 sheets, **0 XML errors, 0 error-literal cells**, 8
  native tables. File **1.75 MB → 5.6 MB** (description/address text fields).

---

## §10 — Open work / next-agent notes

- **Archetype-assignment pass** — still the gating phase: vendor cols
  `Capability Domain Archetype (D)` / `Primary Output Archetype (P)` + the two Basis
  cols are blank, awaiting a NAICS-6 → archetype map with vendor-registry override.
- **Parent UEI** (vendor col) — still blank pending a standardized parent-UEI list.
- **Header renames (deferred Rec 2)** — `Subaward Actions` (16) / `Primary NAICS-6`
  code col / `Subaward Report ID` headers still clip; rename to shorten if desired.
- **Optional dedup** — vendor NAICS/parent columns could become `XLOOKUP`s into the
  dimension sheets.
- **Port to `workbook_award_analysis`** — this raw-tx + live-rollup model is the
  intended replacement for its single `vendors` sheet.

---

## §11 — Conventions / gotchas (this session)

- **Subaward records have NO NAICS** — `naics4`/`naics_desc`/`country` on the *old*
  tx sheets came from `entity_naics_lookup.csv` (SAM entity-reg enrichment by UEI),
  not the FSRS record. Raw country lives on `entityPhysicalAddress.country.code`;
  `is_foreign` = that code not in (USA, "").
- **Don't mutate `_corpus`** — the extractor reuses `load_scope` / `iter_records`
  read-only and replicates the dedup/MIB filter; counts proven equal.
- **Faithful = every field a column**, even always-blank ones (`referencedIDV*`);
  array fields are joined leaf columns, not dropped.
- **Green = surfaced cross-sheet value, black = new aggregate** — `$M` (SUMIFS total)
  black; count/min/max (values that exist on the tx sheet) green. Text stays black
  (no green-text style in the system).
- Build green = done; user verifies visually (memory `no-png-render-verification`).
