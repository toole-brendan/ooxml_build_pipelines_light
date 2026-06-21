# Session Log — destroyer_outsourced_work — 2026-05-28 (workbook build)

**Handoff doc for the next AI agent.** This session built the project workbook
(`destroyer_outsourced_construction_workbook.xlsx`) from `WORKBOOK_SPEC.md`, using the
`ddg_workbook/` build pipeline and modeling on `sub_workbook/`. It is the numeric
layer that sits between the `extracted/` CSVs and the deck (`DECK_SPEC_v3.md`).

Read first for context:
1. `logs/2026-05-28_methodology_overhaul.md` (the methodology + data state this builds on)
2. `WORKBOOK_SPEC.md` (the plan), `DECK_SPEC_v3.md` (what consumes the workbook)
3. `METHODOLOGY.md` (the method; the workbook realizes it)
4. This file

---

## 1. TL;DR — the one thing that matters

The workbook is the **source of truth**. It *computes* the headline numbers from the
data + the editable Inputs; whatever it computes IS the number. The
spec/methodology's 87 / 33 / 78 were back-of-envelope and are **superseded** by the
workbook's computed figures:

| Measure | Workbook (computed) | Where |
|---|---|---|
| Disclosed-corpus outside-yards POP % | **84.8%** | `DoD POP!C14` (do not headline — redaction artifact) |
| MYP-corrected outside-yards POP % | **46.8%** | `DoD POP!C20` (masters folded back in) |
| Funnel cost-share (outsourced % of total ship cost, FY16-27 avg, Mid) | **58.3%** | `DoD POP!C8` ← Funnel |

These re-solve live when Inputs change (the control loop — see §3). All three are
editable-assumption-driven, not hardcoded.

---

## 2. What was built

- **Pipeline**: `ddg_workbook/` (a fresh copy of the generic stdlib-only OOXML engine,
  renamed from the `telemetry_one_pager` scaffold). Package `workbook_ddg/` =
  `lib.py` (engine) + `styles.py` (palette) + `sheets/` (one module per tab).
  `build_workbook.py` → `destroyer_outsourced_construction_workbook.xlsx` at the repo root.
- **Engine ported from `sub_workbook/workbook_sub/`** (lib.py + styles.py), repointed:
  `EXTRACTED = ../extracted`, `EDGAR = ../edgar_research`, `OUT` at repo root.
- **Strictly stdlib** (csv, json, zipfile, pathlib, datetime, xml). No openpyxl, no
  subprocess anywhere in the build.
- **12 sheets**, tab order mirrors the sub workbook (deck-data + control + funnel up
  front, data sheets in the middle, References last):
  `Charts · Inputs · Funnel · SCN Annual · FFATA Subawards · DoD POP · Top Vendors ·
  Scope Excluded · Production · Prime 10-K · FPDS Primes · References`.
  (A Cover sheet was built then **deleted at the user's request**.)

### Per-sheet (what feeds it, what it does)
- **Inputs** — the editable control panel. Supplier-content band 35/42/50% (IN-01..03);
  Ingalls DDG-share 46/53/70% (IN-04..06); BIW share of GD Marine 22% + BIW DDG-share
  85% (IN-07/08); MYP master $ BIW 6400 / Ingalls 8180 + in-yard POP 69% / 77%
  (IN-09..12); FFATA lag uplifts (IN-13..15); scope/windows (IN-16..22); 73 in-scope
  PIIDs reference. Accessor: `cell_ref("IN-xx")` → `Inputs!D{row}`.
- **SCN Annual** ← `cost_funnel_summary.csv`. Per-FY P-5c (Total/Plans/Elec/Ord/HM&E/
  Other/GFE-sum/CO/BC) + derived BC%, GFE%. Caveats as visible rows. `scn_cell(fy, metric)`.
- **Funnel** — the spine. Total − Plans − GFE − CO = BC; BC × band = yard-side (Low/Mid/
  High); − FFATA floor = unseen; GFE + yard-side = total outsourced; outsourced %.
  Two-yard block (BIW vs Ingalls). `funnel_cell(fy, metric)`, `outsourced_pct_mid_range()`.
- **FFATA Subawards** ← `nc_annual_by_piid.csv`. Per-yard FY totals (formulas summing 73
  PIIDs grouped BIW/Ingalls/GFE-prime). Window FY13-26 reconciles to the $11.2B in-scope
  total. `floor_cell(yard, fy)`, `biw/ingalls/grand_total_cell()`.
- **DoD POP** ← `dod_action_pop_by_worktype.csv`. Disclosed POP rollup (SUMPRODUCT over
  in-scope flag) + MYP reconciliation (folds masters from Inputs). Outputs the three
  numbers. In-scope = `ddg51*` + `ddg_gfe_*` except `ddg_gfe_weapons`.
- **Top Vendors** ← `sam_subaward_top_parents.csv` + `entity_naics_lookup.csv`. Top 50,
  % of in-scope total (denominator = FFATA grand). `dollars_range(start,end)`.
- **Scope Excluded** ← `nc_scope_summary.json` + `_discovered_piids.csv`. 16 contaminants
  (IVECO 1 / DDG-1000 6 / WPN-OPN 9) with FPDS size + cleanup-impact summary.
- **Production** ← `scn_li_production_schedule.csv`. 30 hulls (BIW 11 / Ingalls 13 / TBD 6)
  + yard×FY count matrix.
- **Prime 10-K** ← `edgar_research/{hii_ingalls,gd_marine_systems}_segment_reconciled.csv`.
  Segment financials + live yard-side triangulation referencing Inputs.
  `modeled_yardside_mid_avg_cell()`, `ddg_alloc_fy_cell(yard, fy)`.
- **FPDS Primes** ← `fpds_annual_by_prime.csv` (de-capped). Per-FY obligations by vendor
  group. `group_total_cell(group)`.
- **Charts** — think-cell-ready blocks (all cross-refs): funnel, POP reconciliation,
  FFATA gap, vendor concentration, two-yard, direction-of-travel.
- **References** ← `exec_quotes_outsourcing.csv` (52) + `all_transcripts_index.csv` (134
  rollup) + hardcoded GAO/CRS/Navy/CSIS citations.

---

## 3. How it works — the control loop (the reason it exists over flat CSVs)

Editing an **Inputs** cell re-solves everything downstream via cross-sheet formulas.
Proven this session: band mid 0.42 → 0.60 moved Funnel outsourced% 58.3%→69.2%, the
triangulation $1,742M→$2,489M, and the DoD POP cost-share 58.3%→68.8%, while raw SCN
inputs stayed put. Every numeric cell is either a blue hardcoded input, a black derived
formula, or a green cross-sheet link — applied explicitly per cell (no auto-detection).

---

## 4. Validation

- **`ddg_workbook/validate_workbook.py`** is a separate QA tool (uses openpyxl). NOT part
  of the pipeline — never import it from the build.
- For computed-value checks, recalc headless with LibreOffice (also QA-only):
  ```
  soffice --headless --calc -env:UserInstallation=file:///tmp/wbcalc/profile \
    --convert-to xlsx:"Calc MS Excel 2007 XML" --outdir /tmp/wbcalc/out wb.xlsx
  ```
  then read with `openpyxl(data_only=True)`. `forceFullCalc/fullCalcOnLoad` are set, so
  LibreOffice/Excel compute on open.
- Final state: 0 XML errors, **0 formula errors** across all 12 sheets, **0 em-dashes**.
  Reconciliations tie: FFATA grand `$11,198M` (= the cleaned in-scope total), Funnel BC
  links exactly to SCN BC, Production = 30 hulls, BIW de-capped prime = `$13,575M`.

---

## 5. Decisions / user feedback applied (do not silently reverse)

- **Audit-trail is font-color, NOT fill-based.** Blue font = hardcoded input; black =
  derived; green = cross-sheet link; bold = total. The spec's "yellow fill = input" wording
  was never implemented (and the engine docstring says "No yellow fills"). Don't add fills.
- **No heavy top border on total rows.** The medium top border (`borderId=2`) was removed
  from `S_TOTAL`/`S_NUM_TOTAL`/`S_PCT_TOTAL`/`S_NUM_INPUT_TOTAL` (now `borderId=0`,
  bold-only) — the user flagged it as odd/unintended. The sub workbook still has it.
- **Em/en dashes normalized to hyphens** at the text-write boundary in `lib.cell()`, so no
  source-CSV punctuation (NAICS sector labels, transcript quotes) leaks an em-dash.
- **Plain section titles.** No "source of truth", "travel together", "the spine", etc. in
  banners — terse noun phrases only.
- **Two yard-side estimates differ on purpose:** Funnel uses BC × band (~$1.4-1.7B/yr);
  Prime 10-K triangulation uses segment revenue (~$1.5-1.7B/yr avg). Kept separate.

---

## 6. Files created / modified

**Created (this session):** `ddg_workbook/workbook_ddg/sheets/{inputs, scn_annual,
production, ffata_subawards, scope_excluded, top_vendors, fpds_primes, prime_10k, funnel,
dod_pop, charts, references}.py`; `ddg_workbook/validate_workbook.py`; the output
`destroyer_outsourced_construction_workbook.xlsx`; this log.

**Modified:** `ddg_workbook/build_workbook.py` (launcher), `ddg_workbook/workbook_ddg/
{lib.py, styles.py, __init__.py, sheets/__init__.py}` (renamed pkg + ported engine +
border fix + em-dash normalize), `~/.claude/.../memory/project_ddg_workbook.md` (+ MEMORY.md).

**Deleted:** `ddg_workbook/workbook_ddg/sheets/cover.py` (built then removed per user).

**Untouched:** all `extracted/` CSVs, `edgar_research/`, `sub_workbook/`, the deck,
`METHODOLOGY.md`, `WORKBOOK_SPEC.md`, `DECK_SPEC_v3.md`, the wiki.

---

## 7. Things to NOT do

- **Don't put openpyxl / soffice in the pipeline.** Build is stdlib-only; QA tools are
  separate (`validate_workbook.py`, ad-hoc LibreOffice recalc).
- **Don't re-introduce the 87/33/78 figures** as the answer — the workbook computes
  84.8 / 46.8 / 58.3 and that supersedes the spec's back-of-envelope math.
- **Don't add yellow fills or total-row borders** (see §5).
- **Don't treat the funnel as fully reconciled** — single-vintage; HM&E blank pre-FY24;
  FY26 base AP-anomalous; GFE = Elec+Ord is a lower bound (no LM2500). Surfaced on SCN Annual.
- **Don't forget the transfer tarball** is a point-in-time snapshot — it predates the
  workbook + `ddg_workbook/`; rebuild before uploading.

---

## 8. Open items / next steps

1. **The MYP-corrected POP % (46.8%) is sensitive to the MYP master $/POP inputs**
   (IN-09..12). If those firm up (trade-press vs FPDS-recovered), edit Inputs and it
   re-solves. Currently BIW $6.40B@69% in-yard, Ingalls $8.18B@77%.
2. **Refresh stale figures elsewhere** (from the prior log, still open): the wiki +
   `outsourcing_assumptions.md` still cite pre-cleanup numbers; the deck slides still
   anchor on a 72pt "~87%".
3. **Build the deck** from `DECK_SPEC_v3.md` — it can now pull from the workbook's Charts
   sheet (and cite the computed 84.8/46.8/58.3 instead of the old figures).
4. **SCN multi-vintage reconciliation + HM&E backfill** (METHODOLOGY §4 [Planned]) would
   let the Funnel drop its single-vintage caveat.
5. **Optional Checks sheet** — the sub workbook had one; not built here (kept to 12).

---

## 9. Quick orientation for the next agent

- **"How do I rebuild it?"** → `cd ddg_workbook && python3 build_workbook.py` (stdlib only).
- **"How do I verify the numbers?"** → `python3 validate_workbook.py` (structure), or the
  LibreOffice recalc one-liner in §4 for computed values.
- **"What's the outsourcing number?"** → the workbook: 58.3% funnel cost-share / 46.8%
  MYP-corrected POP / 84.8% disclosed POP. NOT the spec's 78/33/87.
- **"Where do I change an assumption?"** → the **Inputs** sheet (blue cells); everything
  downstream re-solves.
- **"Why two yard-side numbers?"** → Funnel (BC × band) vs Prime 10-K (segment
  triangulation) — two independent estimates, kept separate by design.
- **"Where's the deck-facing data?"** → the **Charts** sheet (cross-refs, think-cell-ready).
