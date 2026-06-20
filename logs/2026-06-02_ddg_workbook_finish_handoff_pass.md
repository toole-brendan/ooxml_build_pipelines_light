# 2026-06-02 — DDG workbook: finish-handoff pass (description-led bucketing, annual headlines, z_ChartData, notes)

## Scope

Implemented `core/ddg/ddg_finish_handoff_plan_2026-06-02.md` across the
`workbook_ddg` sheet modules. This is the DDG counterpart to the submarine
finish-handoff pass — a **finishing pass, not a modeling rewrite**: the TAM/SAM
calc chain, the AP/LLTM additive stream, the MYP-correction logic, and the no-SOM
boundary are unchanged. Work was the description-led bucketing model-path fix,
annual headline promotion, a deck-facing `z_ChartData` contract, selective native
Notes, and the same-sheet green-link / gutter / round-integer style cleanup.

**Hard constraints honored (per the plan's non-negotiables):**
- **No edits to any `core/workbook_core/` engine file.** Every change is in
  `core/ddg/workbook/workbook_ddg/sheets/`. Verified: zero engine edits.
- **No submarine SIB work carried over; no SOM / capture / win-probability outputs.**
- **No label-convention cleanup.** Canonical terms preserved (`AP/LLTM`, `TAM/SAM`,
  `GFE/MIB`, `MYP`, `FFATA`, `POP`, `BC`, `HM&E`).
- **Kept the RowCursor closure-accessor pattern** (no `sheet_ref()`/`range_ref()` conversion).
- **No raw `extracted/*.csv` edits** — those are read-only inputs.

Final: `python build_workbook.py` → **24 sheets, 12 native tables, 6 note parts,
267,704 bytes**.

---

## Phase 0 — baseline + source-only audit harness

Established the baseline from a fresh raw build (23 sheets, 11 tables). Built a
**temporary DDG-local audit harness** (`_finish_audit.py`, removed at end of pass)
that reads the freshly-built `.xlsx` (not an Excel-resaved copy) and runs the
package / formula / style / green-link / notes gates. Baseline confirmed the **35
same-sheet green links** the plan flagged.

---

## Phase 1 — description-led bucket classification (`entities.py`)

The model path was vendor/NAICS-led (classified the 150-row `entity_naics_lookup.csv`),
contradicting the methodology's "description-led" claim. **Rewrote the upstream
Entities data, kept the downstream SAM contract stable.** `entities.py` now:
- loads `nc_records_long.csv` (15,720 FFATA subaward records, all with a description)
  and enriches NAICS-4 per UEI from `entity_naics_lookup.csv`;
- calls `classify(vendor, naics4, desc)` per record (description is the primary arbiter);
- aggregates to **one row per (vendor, UEI, role, bucket)** — a vendor splits across
  buckets when descriptions support it — with a dominant-basis label (`+N` when mixed);
- preserves every accessor `sam_build`/`bucket_evidence` consume
  (`ent_dollar_range`/`role_range`/`bucket_range`/`ent_row_cell`/`top_vendor_indices`),
  so SAM's `SUMPRODUCT(role, bucket, $)` observed-share contract is unchanged.

User chose the **full-population** option (vs. top-N): the bucket shares are now
computed over the complete $11.2B description-led population. Result: **2,408
vendor-bucket rows**; supplier-addressable $10,334.8M, 57.1% bucketed (electrical
$2.4B, structural $1.8B, machining $1.2B…), 42.9% unbucketed residual (visible,
handled by the model). Added `top_supplier_indices(n)` for the deck CD09 block.

The bucketed-TAM = portfolio-TAM and broad-SAM = TAM − residual identities still hold
**by construction** (shares sum to 1; description-led changed share *values*, not the
identity structure).

---

## Phase 2 — annual headline outputs + defined names

- **`executive_summary.py` §1** reordered annual-first: average annual TAM, average
  annual broad SAM (new row, links `sam_avg_annual_cell("broad")`), then the FY22-27
  cumulative figures as backup, then BC/AP streams, coefficient, MYP-corrected POP.
- **`sam_build.py`** gained a new **§5 Annual SAM by fiscal year** block (+ §5b
  tie-out), with producers `annual_sam_cell(scenario, fy)` and
  `annual_broad_sam_cell(fy)` = annual portfolio TAM(FY) × SUMPRODUCT(modeled bucket
  shares, scenario flags); FY22-27 sum ties to the cumulative scenario SAM by
  construction. SAM Build widened to 8 content columns for the FY table (§1-§4 keep
  the 5-col look; only §5 uses B-I).
- **`deck_outputs.py`** added explicit defined names — `portfolio_tam_annual`,
  `portfolio_tam_cumulative`, `broad_sam_annual`, `broad_sam_cumulative`,
  `fiscal_year_count` — keeping `portfolio_tam` / `sam_broad` (and the BC/AP names)
  as backward-compatible cumulative aliases.

---

## Phase 3 — `z_ChartData` deck-loader contract (new sheet)

New `chart_data.py` (`_GROUP="outputs"`, `_TAB="z_ChartData"`), registered after Deck
Outputs (outputs group stays contiguous). A two-pass build: blocks built first
capturing anchors, then a `tbl_ddg_chart_manifest` native table indexing every block
(chart_id / slide / **block_anchor** / chart_factory / unit / source_ref /
producer_tab / note). **12 main-deck blocks** CD01-CD11 + SD12, categories down
column B, series across:
- producer-linked (green cross-sheet) where a producer exists: CD01 KPIs, CD02 stream
  split, CD03 FY24 cost funnel (SCN Budget), CD04 MYP POP distribution (exported new
  §3c share cells from `tam_build`), CD05 TAM bridge, CD06 TAM-by-FY, CD07 bucket TAM,
  CD08 SAM scenarios, CD09 top suppliers (Entities), SD12 scorecard;
- **source-backed, not invented**: CD10 FFATA gap summed from `cost_funnel_summary.csv`
  (visible $2,728.6M vs BC-outsourced low/mid/high $11.3/13.6/16.2B) as labelled
  inputs; CD11 market direction has no structured numeric producer → degraded to a
  qualitative exec-quote shape-table (`exec_quotes_outsourcing.csv`). SD12 qualitative
  scoring left to the deck (not fabricated).

Verified every manifest anchor lands exactly on its block's header row.

---

## Phase 4 & 7 — Deck Outputs REGISTRY + Figure Audit

Rebuilt `Deck Outputs.REGISTRY` for the **16-slide DDG deck**: annual-headline-first,
sequential `DO-NN` ids, an explicit per-figure `pct` flag (replacing the fragile
`_PCT_IDS` set), and slide numbers tracking slides 3/5/6/7/8/9/11/12. **46
producer-linked figures**, all cross-sheet. `figure_audit.py` ties out all 46 (it
iterates REGISTRY; delta = deck value − source = 0 by construction); updated its
5-tuple unpacking.

---

## Phase 5 — selective native Excel Notes

**18 notes on 6 sheets**, attached to **label cells (column B), never numeric value
cells**, threaded through the `_build_*` blocks' acc dicts and aggregated in render:
- Executive Summary (4): avg-annual cadence, annual broad SAM = menu not SOM,
  MYP-corrected outside-yards, FFATA coverage-floor caveat.
- TAM Build (4): BC coefficient, AP/LLTM coefficient, MYP master reconstruction,
  average-annual-not-run-rate.
- SAM Build (3): unbucketed residual, description-led bucketing basis, broad scenario.
- AP Bridge (3): ship-construction share, AP/LLTM stream TAM, no-double-count.
- Sensitivity (2): MYP-adjustment sensitivity, FFATA-visible floor.
- POP Audit (2): confirmation-coverage method, reconstructed MYP masters.

Comments/VML parts created on exactly those 6 sheets; refs unique per sheet;
`validate_excel_notes` passes; no row-by-row note sprawl in data tables.

---

## Phase 6 — style / build cleanup

- **35 same-sheet green links → black derived** (`S_NUM`/`S_PCT`): TAM Build §1
  at-a-glance (8) + §4b disclosed/corrected (2) + §5b coefficients (2); SAM Build §1
  at-a-glance (15) + §3b modeled-share column (8). True cross-sheet pure links
  (TAM Build toggles/bases → Inputs/SCN; SAM §3a portfolio-TAM → TAM Build; all
  z_ChartData producer links) correctly **stay green**.
- **Removed the one false gutter `x`** on TAM Build §5c (it's followed by a total row,
  not collapsible detail). Methodology and other umbrella markers kept.
- **Round-integer metadata → `S_DEFAULT`** (year/count/ID, not analytical decimals):
  Inputs FY range start/end; TAM Build years-in-window + in-window hulls;
  Production Schedule hull counts; Scope Exclusions record/UEI counts + pre-clean
  (in-scope **dollars** kept as input); Scenarios bucket counts. Values unchanged
  (formulas still resolve); only the display loses the `#,##0.0` format.
- **`methodology.py`** now defines `_TAB = "Methodology"` and uses it for the row-2
  title banner and the SheetEntry (drift prevention; not a relabel).

---

## Verification (read-only / structural — the agreed ceiling)

Fresh raw build, audited via the throwaway harness + a final XML/identity pass:
- **Package:** 24 sheets, group order canonical/contiguous; `cellXfs` == `len(CELL_XFS)`,
  `dxfs` == `len(DXFS)`; **no `sharedStrings.xml`**, **no worksheet `mc:Ignorable`**;
  all **12 native tables** use `WorkbookCore_NoFormatTable`; comments/VML parts exist
  on exactly the 6 note-bearing sheets; **all 72 package parts parse as well-formed
  XML**; zip integrity OK.
- **Formula/style:** **0 dangling sheet refs**, **0 formula-error literals**, **0
  same-sheet/derived green links** (was 35); headline figures formula-driven from
  producers; defined names resolve to producers (`portfolio_tam_annual → 'TAM Build'!
  $C$133`, `broad_sam_annual → 'SAM Build'!$E$70`, …).
- **Model identities (structural):** QA-05 `bucketed TAM ('SAM Build'!C58) = portfolio
  TAM (C44)`; QA-12 `portfolio TAM = 'TAM Build'!I112 + I113 (BC + AP/LLTM)`; broad
  SAM ≤ TAM — all wired to valid producers and hold by construction.
- **z_ChartData:** every block value is a producer link, a derived formula over
  producers, or a source-backed labelled input (CD10) / qualitative evidence (CD11),
  documented in `tbl_ddg_chart_manifest`.

**Environment:** `python` 3.14.4 on PATH; read-only checks + the workbook build output.

---

## Deliberately NOT done

- **No Excel recompute.** `QA Checks` 0 FAIL / `Figure Audit` 0 FAIL and the numeric
  tie-outs (bucketed TAM = portfolio TAM, broad SAM ≤ TAM, portfolio = BC + AP/LLTM)
  cannot be evaluated here — formula chains are intact and the identities hold by
  construction, but a real Excel pass is the remaining confirmation.
- **No core engine edits / no PPTX-pipeline edits / no image wiring** (per the plan).
- **No invented CD10/CD11 numbers** — source-backed inputs / qualitative shape-table.
- **No dedicated chart-data audit sheet** — z_ChartData values are producer links or
  explicitly source-backed, so a separate tie-out would be redundant.

---

## Files changed this session

- **Added:** `workbook_ddg/sheets/chart_data.py` (z_ChartData).
- **Edited:** `entities.py` (description-led record-level classification +
  `top_supplier_indices`), `sam_build.py` (§5 annual block + accessors + notes +
  green fixes + widen), `tam_build.py` (§3c share-cell exports + notes + green fixes +
  §5c gutter + round-int), `executive_summary.py` (annual-first §1 + notes),
  `deck_outputs.py` (16-slide REGISTRY + annual/cumulative defined names + pct flag),
  `figure_audit.py` (5-tuple unpack), `ap_bridge.py` / `sensitivity.py` /
  `pop_audit.py` (notes), `inputs.py` / `production_schedule.py` /
  `scope_exclusions.py` / `scenarios.py` (round-integer metadata),
  `methodology.py` (`_TAB`), `sheets/__init__.py` (register chart_data).
- **Unchanged:** all of `core/workbook_core/`; the deck pipeline; the submarine workbook (content).
- **Temporary (created then removed):** `_finish_audit.py`.
- **Rebuilt artifact:** `20260601_Distributed Shipbuilding DDG_v1.0.xlsx` (24 tabs) — see the output rename below.
- **This log.**

---

## Post-pass output rename → v1.0 (both pipelines)

A follow-up after the finish pass: renamed both workbook pipelines' output filenames
to a clean v1.0 label, rebuilt, and removed the old-named artifacts.

- **DDG** (`workbook_ddg/lib.py`): `OUT` filename
  `20260601_Destroyer Outsourced Construction_vS.xlsx` →
  **`20260601_Distributed Shipbuilding DDG_v1.0.xlsx`**. Rebuilt fresh
  (24 sheets, 12 native tables, 6 note parts, 267,703 bytes).
- **Submarine** (`core/submarine/workbook/workbook_sub/lib.py`): `OUT` filename
  `20260601_Distributed Shipbuilding Submarines_vS.xlsx` →
  **`20260601_Distributed Shipbuilding Submarines_v1.0.xlsx`**. Rebuilt fresh
  (12 native tables, 8 note parts, 155,619 bytes; **content unchanged** — this is a
  filename-only change to the submarine pipeline, no sheet edits).
- Only `OUT` was changed in each `lib.py`; the docProps `_TITLE` / `_CREATOR` strings
  were left as-is (filename rename only, not a metadata relabel).
- **Old-named artifacts deleted** (kept only the two `_v1.0` files): the DDG dir held
  `20260601_DDG Outsourced Construction_vS.xlsx` (an Excel-resaved copy, 288,003 bytes,
  NOT the pipeline's prior raw output — flagged to the user), and the submarine dir held
  `20260601_Distributed Shipbuilding Submarines_vS.xlsx`.

---

## Follow-ups

- **Open in Excel** to confirm `QA Checks` / `Figure Audit` evaluate to 0 FAIL and no
  cell trips a repair dialog (the one out-of-environment check).
- The **DDG deck pipeline** (`core/ddg/deck`) can now consume `z_ChartData` (CD01-CD11 /
  SD12, indexed by `tbl_ddg_chart_manifest`) and the new annual/cumulative defined
  names; `portfolio_tam` / `sam_broad` remain as cumulative aliases until it adopts the
  explicit names.
- Optional: a structured producer for the CD11 outsourcing-direction index (it is a
  qualitative shape-table until that data exists); a structured FFATA-gap producer so
  CD10 can link rather than read the CSV.
