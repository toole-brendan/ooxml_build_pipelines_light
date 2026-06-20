# 2026-06-20 — Workbook layer: contracts data sheets + recompete radar — session log + handoff

Eighth session (same day). Continues from `research/contracts/logs/2026-06-20_contracts_layer_pipeline_build.md`
(the 6-stage pull pipeline + four extracted CSVs). This session put the **contracts evidence into the
workbook** for the first time. **Pass 1:** ported a faithful-flat sheet toolkit into `workbook_army` and
rendered the four contract CSVs as **raw data tabs** (every source field a column). **Pass 2:** built the
**recompete radar** — a live-formula screen over those leaves. Final build is green (**6 tabs, 5 native
tables**) and verified. Pass 1 is documented first; Pass 2 in its own section below.

## Decisions locked this session (from the user)
- **This pass = data sheets first.** Render the four contract CSVs as filterable raw tables; the radar
  follows in a separate pass once the leaves are reviewed.
- **Faithful raw rendering.** The data tabs render *every source field as a column*, even always-blank
  ones, identifiers kept as exact strings — not curated subsets. Reference idiom adopted:
  `projects/research_shared/workbook_award_classification_refactor` (its `make_flat_sheet` builder +
  the directive *"every data field on the record becomes a column, even if every value is blank"*).
  The user explicitly steered AWAY from a curated ~20-column view.
- **Recompete radar (Pass 2) = a LIVE-FORMULA sheet**, scoped to a **deterministic watercraft-relevant
  flag**. Methodology is the army's own handoff spec (one row per contract *family*, a *window* not a
  date, Confirmed/Strong/Inferred/Speculative confidence + a separate pursuit-access rating) — **not**
  the shipbuilding `workbook_award_analysis` cadence/wave model (user was skeptical of it; do not copy).

## What was built (`workbook_army/sheets/`)
The army pipeline had only a placeholder `summary_overview`; it had none of the shared helpers. Ported
copy-from `workbook_award_classification_refactor/sheets/` (engine untouched; helpers live per-pipeline),
package name rewritten to `workbook_army`:

| New file | Role | Adaptation from source |
|---|---|---|
| `_layout.py` | `RowCursor` over workbook_core primitives | none (docstring only) |
| `_cuts.py` | **raw-string** CSV loader + `as_int/as_float/cell/date_serial` | bound to `workbook_army.lib.EXTRACTED` |
| `_text_input.py` / `_italic.py` | scoped blue-text-input / italic styles (CELL_XFS append) | none |
| `_widths.py` | width constants + `header_styles` + **new `contract_width(header)`** | added the contract column→width map |
| `_flat.py` | `make_flat_sheet` single-table builder | trimmed the archetype INDEX/MATCH helpers; **added `width_fn=` param** so a raw pull auto-sizes from its headers (no hand-counted widths list) |
| `_tabs.py` | canonical tab names | new |
| `data_contract_awards.py` | "Contract Awards" tab | ~30-line config |
| `data_award_actions.py` | "Award Actions" tab (the sum-able table) | ~30-line config |
| `data_subawards.py` | "Subawards" tab | ~25-line config |
| `data_pipeline_events.py` | "Pipeline Events" tab | ~25-line config |

`sheets/__init__.py` — added the `data` block (the four tabs) after `summary_overview` (groups stay
contiguous; summary → data is valid per `workbook_core.groups`).

### Typing per sheet (declared by header NAME in the config module)
- **awards**: float = obligation_amount/current_value/ceiling_value/total_outlay/total_subaward_amount;
  int = subaward_count/number_of_offers; date = date_signed/pop_start_date/pop_current_end_date/
  pop_potential_end_date/first_action_date/last_action_date; **input (blue)** = those float+int+date.
- **actions**: float = amount; int = fiscal_year (left black — derived FY); date = action_date;
  input = amount + action_date.
- **subawards**: float = amount; date = sub_action_date/submitted_date; input = those.
- **pipeline**: date = posted_date/response_deadline; input = those; no money.
Everything else renders raw text (black); identifiers (PIID, UEI, NAICS/PSC codes, TAS) stay exact
strings; the blank `program`/`capability_node` bridge columns + the provenance columns
(source_system/source_id/extract_run_id/row_hash) are kept as real columns.

### Each data module exposes a `cols(header)` accessor
`make_flat_sheet` returns `(SheetEntry, cols)`; module-level `awards_cols` / `actions_cols` /
`subawards_cols` / `pipeline_cols` give absolute ranges like `'Contract Awards'!$U$9:$U$2603`. **These
are the hooks Pass 2's live-formula radar reads** (SUMIFS over `actions_cols("amount")` keyed on
`awards_cols("piid")`/`parent_idv_piid`; date math on `awards_cols("pop_current_end_date")`).

## Build + verification (all green)
`cd projects/army/workbook && python3 build_workbook.py` → `../20260620_US Army Market Mapping_vS.xlsx`
(1.84 MB, **5 sheets, 4 native tables**).

- **Faithful columns:** table column sets equal the CSV headers exactly — awards **44**, actions **23**,
  subawards **23**, pipeline **19** (incl. blank bridges + provenance). 
- **Row counts (records):** awards **2,595** · actions **7,757** · subawards **305** · pipeline **4** —
  all match `csv.reader` record counts.
- **Sums tie to the pull log:** Award-Actions `amount` = **$3,249.6M** (sum-able obligations);
  Subawards `amount` = **$112.5M**; awards-level obligation = **$3,587.0M** (the ~9% > per-mod gap is
  the expected FPDS-Army-scope drop, documented in the pull log).
- **0 error-literal cells** across all worksheets (`t="e"` scan).
- **Cell-type spot checks (awards row 9, Eastern Shipbuilding `W912BU23C0020`):**
  `piid`/`recipient_uei`/`naics_code`='336611'/`psc_code`='1955' render as **strings** (no int
  coercion); obligation/current/ceiling are **numeric** (money numFmt 164); `pop_current_end_date`=46708
  is a real **date serial** (numFmt 169); source numbers/dates use **fontId 3 = blue** (`FF0000FF`)
  input styling while text stays black; `program`/`capability_node`/`funding_tas` are **empty cells**.

## Gotchas worth keeping
- **`wc -l` overcounts the contract CSVs.** `contract_award_actions.csv` / `contract_subawards.csv`
  carry requirement-description and title fields with **embedded newlines inside quoted fields**, so
  `wc -l` reports 8,291 / 543 while the true record counts are **7,757 / 305**. Always count with a real
  CSV parser; the table renders the correct record counts.
- **Use the raw-string `_cuts.load_table`, NOT `workbook_army.lib.load_extracted_csv`.** The core loader
  auto-coerces numerics, which would turn NAICS/PSC codes and UEIs into ints (dropping leading zeros /
  exact form). The flat builder needs raw strings so it casts *only* the columns declared numeric/date.
- **`python` is not on PATH in this env — use `python3`.**

## Files created / changed
Created: `workbook_army/sheets/{_layout,_cuts,_text_input,_italic,_widths,_flat,_tabs}.py`,
`workbook_army/sheets/{data_contract_awards,data_award_actions,data_subawards,data_pipeline_events}.py`.
Changed: `workbook_army/sheets/__init__.py` (registered the data block).
Output: `projects/army/20260620_US Army Market Mapping_vS.xlsx` (rebuilds from the same command).

## Pass 2 — the recompete radar (DONE, same session)
`model_recompete_radar.py` → tab **"Recompete Radar"** (group `model`, so it sorts ahead of the data
leaves; SHEETS reordered to summary → model → data). A **live-formula** screen, one row per watercraft
contract **family** (vehicle), built straight on the Pass-1 `cols()` accessors (no re-extraction). Methodology
is the army's own handoff spec (window-not-a-date, parent-vs-task-order expiry distinct, analyst judgment
left blank) — **not** the shipbuilding cadence model.

**Scope finding that drove the design:** the watercraft flag is **near-saturating** — 1,667 of 1,688
families match (discovery was already NAICS/PSC-scoped to watercraft), so the flag alone barely filters.
The real focusing lever is a **materiality floor**: `_MIN_OBLIG = $1.0M` lifetime obligations →
**226 vehicles** (median family is a ~$65k micro-buy; lower the constant to widen). Both gates are
build-time + documented in the sheet caption; rows sorted by $ desc.

**Columns (23):** build-time identity (Family/vehicle PIID, Incumbent = dominant-$ recipient, Relevance
basis, rep PSC/NAICS, Last competition) · **live formulas** (Vehicle type, Task orders = COUNTIFS;
Obligated $M = SUMIFS over `actions_cols('amount')` keyed on parent_idv **and** piid; Actions; Current
end / Potential end = blank-guarded MAX of two `_xlfn.MAXIFS` over the awards leaf; Parent/vehicle end =
the IDV ordering-period expiry, tracked distinctly; Months-to-current-end & Option-headroom vs the As-of
cell; Recompete window bucket; In-market notice = COUNTIFS over `pipeline_cols('award_number')`) ·
**analyst-blank inputs** (Window override, Confidence, Pursuit access, `program`, `capability_node`, Notes).
An editable **As-of date** input cell (`'Recompete Radar'!$C$6`, default 2026-06-20, blue) re-clocks every
expiry column in-book.

**Verification (replicated the live math in Python over the CSVs — Excel was not run):**
- Build green: **6 sheets, 5 native tables, 0 error cells**; radar table = **226 rows × 23 cols**.
- Formula ranges resolve correctly: Award Actions `$K`=amount/`$D`=parent/`$C`=piid; Contract Awards
  `$U`=current-end/`$V`=potential-end/`$C`=piid/`$D`=parent; Pipeline `$N`=award_number; As-of `$C$6`=46193.
- Replica top vehicles match intent: Vigor `W56HZV17D0086` $417.8M → current end 2029-05-13 → "24-36 mo";
  Eastern `W912BU23C0020` $258.5M → 2027-11-17 → "12-24 mo"; Birdon `W56HZV19D0093` $241.6M → 2030-12-25 →
  "36+ mo"; `W56HZV14C0015` shows the parent/option split (current 2020-09-30 **Expired**, potential 2024-11-19).
- Window distribution across the 226: **Expired 185 · 0-12 mo 26 · 12-24 mo 6 · 24-36 mo 4 · 36+ mo 5**
  (the 16-year award history means most vehicles have run past PoP; the ~41 forward vehicles are the live
  targets — filter the Recompete window column). Renamed the past-PoP bucket "Lapsed / overdue" → **"Expired"**
  so it does not overstate opportunity; whether an expired vehicle is a live overdue recompete is left to
  the analyst Confidence / Pursuit columns.

## HANDOFF — what's left
- **Analyst tagging pass** — fill the blank bridges/judgment on the radar + data sheets: `program`,
  `capability_node` (kill-chain), recompete Window override, Confidence (Confirmed/Strong/Inferred/
  Speculative), Pursuit access. These are deliberately empty input cells (blue) today.
- **Follow-on / lineage detection** — the radar treats each family independently; it does NOT yet link a
  predecessor vehicle to its successor (the "→ expected follow-on" half of the spec). An expired vehicle
  with a live successor is a *different* signal from a true overdue recompete; distinguishing them needs a
  predecessor↔successor map (by incumbent + PSC + gap), a good next derivation.
- **Stage 5 Opportunities full run** — the In-market notice column is live but sparse (4 notices) until the
  ~70-min Opportunities pull runs; rebuild and it populates with no code change.
- **Tunables** — `_MIN_OBLIG` (materiality floor) and `_AS_OF` live in `model_recompete_radar.py`;
  the As-of date is also editable directly in the sheet.

## How to re-run
```bash
cd projects/army/workbook
python3 build_workbook.py     # → ../20260620_US Army Market Mapping_vS.xlsx (6 tabs)
```
The data sheets read straight from `workbook/extracted/contract_*.csv` and the radar recomputes live over
them; re-running the aggregate upstream and rebuilding is all that is needed to refresh everything.

## Files created / changed (Pass 2)
Created: `workbook_army/sheets/model_recompete_radar.py`. Changed: `workbook_army/sheets/_tabs.py`
(+`TAB_RECOMPETE_RADAR`), `workbook_army/sheets/__init__.py` (registered the model block before data).
