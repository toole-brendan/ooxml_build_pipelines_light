# 2026-06-21 — Phases 2-3: budget rendering + market-sizing model + executive dashboard

Session log AND handoff. Continues the same-day Phase-1 integrity refactor
(`2026-06-21_phase1_analytical_integrity_refactor.md`). This session built **Phase 2**
(render budget evidence + canonical models + market sizing) and **Phase 3** (the decision-
output layer). The workbook now answers the question the two reviews said it couldn't:
**"how large is the Saronic-addressable Army market, by program and year, and which
opportunities matter."**

Build: **18 sheets, 15 native tables, 2 note parts, 0 error cells.** Output:
`projects/army/20260620_US Army Market Mapping_vS.xlsx`.

---

## Phase 2 — budget rendering + canonical models + market sizing

### 2.A Budget + source evidence rendered (were entirely absent from the workbook)
New data leaves via `make_flat_sheet`: **Budget Facts** (`budget_funding_facts`, 1,008 rows),
**P-5 Cost Elements** (1,272; `raw_context` folded to a hover note), **O&M Watercraft Notes**
(6), and **Source Log** (`source_log`, 15; url folded to a note). Files:
`data_budget_facts.py`, `data_p5_cost_elements.py`, `data_oma_notes.py`, `data_source_log.py`.

### 2.B Budget Market sheet (`model_budget_market.py`) — funded demand by program x FY
Live SUMIFS over Budget Facts, **single PB2027 vintage** (no cross-vintage blending), each FY
in its own money-type (FY25 actual -> FY26 enacted -> FY27 request -> FY28-31 outyears).
Anti-double-count enforced in the formula: request uses `column_role=request_total` (never
base+oco+total). **Forward FY27-31 $M = FY27 request + FY28-31 outyears.**
- Eligible watercraft lines roll up: MSV(L) $216.4M + ESP $212.6M + Project 526 $14.0M =
  **$443.1M gross funded forward spine** (matches the reviewers' ~$443M exactly).
- `<$5M` float/rail aggregate + PE-0603804A total (context) are memo rows, excluded.

### 2.C Market Size sheet (`model_market_size.py`) — the TAM->SAM->SOM bridge
Per opportunity: **Gross Funded** (live SUMIFS forward spine of its budget line) -> **x
Addressable %** -> **Saronic-Serviceable (SAM)** -> **x timing x pursuit x win = Weighted
Pursuit (SOM)**. The `$` columns are live formulas; the % / probability knobs are BLUE inputs
from the durable **`analyst/market_assumptions.csv`** (seeded illustrative, `source=seed`).
- Headline on seed assumptions: **Gross $443M -> Addressable $130M -> SAM $62M -> Weighted
  SOM $4.8M.** Edit the knobs -> everything re-computes.

---

## Phase 3 — decision-output layer

### 3.A Canonical + reference leaves
- **Contract Families** (`data_contract_families.py`) — the canonical per-family table
  (1,688 rows) rendered as a leaf so the Overview/QA can COUNTIFS/SUMIFS over it live.
- **Customer Map** (`data_customer_map.py`) — from `analyst/customer_org_map.csv` (the leaf
  temporarily repoints `_flat.load_table` at `workbook/analyst/` for this one sheet).
- **Data Freshness** (`data_source_clocks.py`) — `source_clocks.csv` (per-source
  data-through + lag, incl. the SAM CA 90-day Revealed exclusion).

### 3.B Executive Overview (`summary_overview.py`, replaced the stub)
Front-page dashboard: the market-size bridge as **GREEN single-source links** to the Market
Size totals (`model_market_size.TOTAL_REFS` / `model_budget_market.TOTAL_REFS`, exported so
no hardcoded rows), the evidence base as **live COUNTIFS/SUMIFS** over Contract Families
(radar universe count, **Army-ops vs USACE split**, hydrated IDVs, historical obligations as
a labeled separate lens), the model As-of as a date link, and the freshness/caveat pointers.

### 3.C QA & Reconciliation (`qa_reconciliation.py`) + Scope & Assumptions (`scope_assumptions.py`)
- **QA** (validation) — all live over Contract Families: universe/scope counts, the coverage
  histogram (complete 1530 / partial 50 / over 1 / negative 21 / no-actions / no-award-$),
  hydration count, the **Army-vs-USACE segment split** (radar: USACE 172 vs Army-ops 36),
  and the historical-obligation lens (explicitly "never added to budget").
- **Scope & Assumptions** (guide) — purpose, in/out scope, the money-discipline rules, the
  market-sizing method + SEED caveat, lineage/notice "evidence not verdict" framing, and the
  freshness + analyst-layer pointers.

### 3.D Tab reorder (`__init__.py`)
Decision-first, group-constrained order: Overview -> Scope -> Customer Map -> Budget Market
-> Market Size -> Recompete Radar -> Recompete Calendar -> [contract + budget data leaves] ->
Contract Families -> QA & Reconciliation -> Data Freshness -> Source Log.

---

## Files created / changed
**Created:** `model_budget_market.py`, `model_market_size.py`, `data_budget_facts.py`,
`data_p5_cost_elements.py`, `data_oma_notes.py`, `data_source_log.py`,
`data_contract_families.py`, `data_customer_map.py`, `data_source_clocks.py`,
`qa_reconciliation.py`, `scope_assumptions.py`; `analyst/market_assumptions.csv` (seeded).
**Changed:** `summary_overview.py` (stub -> dashboard), `_tabs.py` (+tab names),
`__init__.py` (register + reorder), `aggregate_contracts.py` (seed market_assumptions).

## How to re-run / verify
```bash
cd projects/army/research/contracts/scripts && python3 aggregate_contracts.py
cd ../../../workbook && python3 build_workbook.py      # -> 18 sheets, 0 error cells
```
Verified: 0 error cells (18 sheets); Budget Market spine = $443.1M (Python replica matches
the SUMIFS); Market Size bridge = $443M/$130M/$62M/$4.8M on seed knobs; Overview green links
resolve to `'Market Size'!$E$12/$G$12/$I$12/$M$12` + `'Budget Market'!$L$12`; QA live counts
correct. LibreOffice still cannot recalc (verify via Python replica + `t="e"` scan).

---

# HANDOFF — what remains

## A. The analyst pass (human; the structures are now ready and wired)
Everything below recomputes the moment the values are filled — they are blank/seed today:
- **`analyst/market_assumptions.csv`** — replace the SEED addressable % / Saronic fit % /
  timing / pursuit / win with real judgments (the headline TAM/SAM/SOM moves live).
- **`analyst/recompete_reviews.csv`** — Window / Confidence / Pursuit / program /
  capability_node / Notes per family (renders blue on Radar + Calendar, rebuild-durable).
- **`analyst/lineage_edges.csv`** — set `analyst_disposition` (Confirmed/Probable suppress a
  predecessor; only the Birdon chain is seeded). **`analyst/notice_family_links.csv`** —
  confirm notice<->vehicle links. **opportunities / attribution / work_packages(+capability,
  +saronic_route) / customer_org_map** — flesh out beyond the seed rows.

## B. Phase 4 — recompete + source modernization (coding, when prioritized)
1. **Wire In-market to confirmed notice links** — the radar "In-market notice" still keys on
   `award_number` only. Now that notices are a sheet (Pipeline) and links exist
   (`notice_family_links.csv`), render the links on/near the Pipeline sheet and switch the
   formula to count CONFIRMED links. (Carried from Phase 1.)
2. **Different-vendor (competed-away) successors** — generalize `build_lineage_edges` beyond
   same-UEI: same PSC + same contracting office + different UEI + gap, as a lower-confidence
   tier; moves some "Expired - successor unresolved" rows to "competed away".
3. **Periodic recompete snapshots** — persist dated radar snapshots to show movement.
4. **FPDS Atom -> SAM Contract Awards API migration** (decision #4 deferred it to here; FPDS
   ezSearch decommissioned 2026-02-24). `pull_sam_contract_awards.py` is the foundation; add
   per-record action retrieval. Keep the 355MB FPDS raw as historical backstop.

## C. Optional decision-layer polish (Phase 3 extensions, lower value)
- Dedicated **Opportunity Map** / **Saronic Fit** / **Contract & Vendor Landscape** sheets —
  largely already covered (Market Size = opportunity+fit; Contract Families = vendor/landscape).
  Add only if the analyst wants them broken out.
- Surface the remaining reconciliation detail (SAM third-lens $, first/last action date,
  difference) on a Vendor Landscape sheet (today in `contract_families.csv` + 4 radar cols).

## D. Invariants to hold (unchanged)
Money discipline (never sum across amount_type/column_role; budget vs obligations are
separate lenses; historical obligations != TAM/SAM). Faithful facts (`workbook/extracted/`)
vs analyst judgment (`workbook/analyst/`, merged blue + rebuild-durable). SAM CA $ is a third
lens (Revealed-only), not ground truth. Single As-of cell re-clocks timing. `python3` only;
verify via Python replica + `t="e"` scan (LibreOffice can't recalc this book).
