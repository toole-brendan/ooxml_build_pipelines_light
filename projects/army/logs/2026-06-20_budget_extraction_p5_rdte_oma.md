# 2026-06-20 — Budget extraction extended: P-5 child packages, RDT&E, O&M (session log)

Fourth session (same day, continuation of the OPA watercraft spine extraction). Added three
extraction layers to `research/budget_materials/extract_budget_cuts.py`, all flowing into the same
`workbook/extracted/` CSV contract the workbook loads. Builds on the P-40 spine
(see `2026-06-20_budget_extraction_opa_watercraft.md`).

## Output state (`workbook/extracted/`)

| CSV | Rows | What |
|-----|------|------|
| `budget_line_items.csv` | 5 | 3 OPA procurement + 2 RDT&E (PE 0603804A + Project 526) |
| `budget_funding_facts.csv` | 1008 | P-40 (864) + R-2 PE total (72) + R-2A Project 526 (72) — unified tidy schema |
| `budget_p5_cost_elements.csv` | 1272 | P-5 sub-line cost elements (child work packages) |
| `budget_oma_watercraft_notes.csv` | 6 | O&M watercraft evidence notes (NOT a funding profile) |
| `source_log.csv` | 15 | OPA34 ×6, RDTE_BA4 ×2, RDTE_BA4A ×4, OMA1 ×3 |

Re-run order unchanged: `download_budget_books.py` → `convert_to_txt.py` → `extract_budget_cuts.py`.

## 1. Exhibit P-5 — sub-line cost elements (the child-work-package breakout)

The P-5 "Cost Analysis" decomposes each P-1 line item into cost elements. Table = **6 column groups**
(Prior | FY Y-2 | FY Y-1 | FY Y Base | FY Y OCO | FY Y Total) × **3 metrics** (Unit Cost $K, Qty Each,
Total Cost $M) = **18 numeric tokens/row**. Numbers anchored by the 18-token run; element names wrap
across 2–3 lines, reconstructed by prefix-accumulate + conditional-suffix heuristic (raw text kept per
row in `raw_context` for audit). Section (Flyaway / Recurring / Non-Recurring) and `is_subtotal` tagged.

- **Gotchas solved:** the P-5's own 6-column "Resource Summary" is skipped (gate on `Exhibit P-40` for
  the P-40 path); page-footer lines ("LI …", "UNCLASSIFIED", "Volume 3 -", "Army … Page") were leaking
  into element names → now filtered; a handful of wrapped name-tails ("Support", "Cost", …) are treated
  as continuations so "Program Management/Matrix Support" / "LCU SLEP Contractor Logistics Support (CLS)"
  assemble correctly.
- **Validation anchor:** `Gross/Weapon System Cost` (grand total) == P-40 Net P-1 — NOT Flyaway subtotal.
  MSV carries a non-Flyaway "Support - Training Cost" category, so Gross = Flyaway + Support; ESP has no
  support category so Flyaway alone happens to tie. **16/16 funded line-item-books reconcile to <$0.05M**
  (FY22 & FY24 Float/Rail have $0 net → no P-5, correctly skipped).
- ESP decomposes exactly as expected: LCU SLEP (`SLEP Vessels (LCU-2000)`), MCS SLEP (`SLEP Vessels
  (MCS)`), MIBS (`MIBS Vessels`), HCCC (`Harbormaster command and control center (HCCC)`), LSV SLEP, +
  PM/CLS/logistics — the capability-stack child packages.

## 2. RDT&E — watercraft program element (R-2 / R-2A)

Swept all **33 R-2 books** (BA3/4/4A/4B/5A/5D/7 × FY22–27) attributing watercraft-signal hits to owning
PEs. The watercraft RDT&E concentrates in **ONE** PE across all six years: **PE 0603804A "Logistics and
Engineer Equipment – Adv Dev"** (BA4 in FY22–23, BA4A in FY24–27), specifically **Project 526 "Marine
Oriented Logistics Equipment"** (AWS engineering, seaworthiness, emergent tech, trade studies/BCA/AoA).
~$2.4–2.8M/yr. The PE total also carries non-watercraft projects (EW8 Armored Engineer Vehicles, G11 Adv
Elec Energy), so Project 526 is the watercraft-addressable line; the PE total is captured for context only.

- R-2/R-2A use the **same 12-column grammar** as the P-40, so the column logic is reused
  (`trailing_cells` accepts numeric/`-`/`Continuing`). Facts go into the unified `budget_funding_facts.csv`
  (`measure=rdte_cost`, exhibit `R-2`/`R-2A`).
- **MSV(L) has no standalone development PE** — it appears only inside the shared AoA PE 0604100A (funds
  AoAs for many programs), so it is deliberately NOT extracted as watercraft funding.
- Verified: FY2024 Project 526 column profile matches raw cell-for-cell; cross-vintage works (FY2026
  request in PB26 = enacted in PB27 = 2.716).

## 3. O&M — watercraft sustainment NOTES (no discrete funding line)

O&M has **no discrete watercraft line item**. Watercraft sustainment lives inside OP-5 Subactivity Groups;
the only watercraft-attributable dollars are **bundled program-change items**. So this is an evidence CSV
(`budget_oma_watercraft_notes.csv`), not summed and not a time series — each row = SAG context + (bundled)
amount + narrative + page + relevance flag + `amount_is_watercraft_discrete=N`.

6 notes (FY25–27). The headline force-structure signal the methodology wanted: **FY27 SAG 113 (Echelons
Above Brigade) $10.5M "Home Station Training – CSS Force Structure" = the new Composite Watercraft Company
+ 3 EOD detachments** (flagged `direct`). Others (`lists-watercraft`): LSV depot maintenance (SAG 123),
APS-4 watercraft care (SAG 211), theater-equipment reset (SAG 137). Bare "vessel" false positives
(APS-afloat cargo ships, ammo shipping) are deliberately excluded.

## 4. Open items / next steps

- **Analyst tags still `seed`** across all line items (`mission_family`/`product_layer`) — review pass needed.
- **P-5 `section` is best-effort** for non-standard categories (e.g. MSV "Support - Training" elements get
  tagged with the prior section); cost_element + total_cost_m + is_subtotal are the reliable fields.
- **O&M is evidence, not funding** — do not sum `amount_k`; it is bundled. Composite Watercraft Company is
  the one watercraft-specific O&M signal.
- **Scope now covers the funding evidence layer** (procurement + RDT&E + O&M). Next methodology layers are
  contracts (SAM.gov / USAspending → `05_Contracts_Awards`, `06_Pipeline`, recompete radar) and the
  org/alias `02_Customer_Map` — different sources, not in the budget corpus.
- Possible deepening: P-5 unit-cost/qty are captured but unused; MSV REA/Engineering-Changes elements
  could be tagged to kill-chain nodes (Platform/Sensors/Effectors/C2; see `workbook/analyst/capability_nodes.csv`)
  via the capability bridge (NOT as columns on the facts).

---

# HANDOFF — read this first if you're picking this up cold

## A. Orientation (the mental model)

**Project:** a "where to play" market-mapping **workbook** for a defense-tech company selling autonomous
surface vessels, with the **US Army** as customer. Methodology + the analyst's intent are captured in
`projects3/army_transcript.xml` (read it) and summarized across the four `logs/2026-06-20_*.md`. The
overall evidence chain is: *mission problem → user → requirement owner → acquisition owner → **funding** →
contracting mechanism → timing → competitive route.* **We have only built the FUNDING layer so far.**

**The build contract (how data reaches the workbook):**
```
research/budget_materials/                          workbook/
  download_budget_books.py  ──┐                       workbook_army/lib.py  load_extracted_csv(name)
  convert_to_txt.py           │  (PDF→txt→CSV)                ↑  reads at build time
  extract_budget_cuts.py  ────┴──►  workbook/extracted/*.csv ─┘  ──►  sheets/*.py  ──► .xlsx
```
The **CSV in `workbook/extracted/` is the hand-off boundary.** Data-mining writes it; the workbook only
reads it (numeric-coerced, `=`-prefixed cells pass as Excel formulas, blanks→None). This mirrors the two
reference pipelines: `projects/distributed_shipbuilding/workbook_award_analysis` and
`projects/research_shared/workbook_award_classification_refactor` — study those for the workbook-build half,
which is **not yet started** for `army` (only `workbook/extracted/` is populated; `workbook_army/sheets/`
has just a stub `summary_overview.py`).

**Key paths:**
- Corpus (search this, not PDFs): `research/budget_materials/txt_versions/FY{22..27}/{procurement,rdte,om}/*.txt`
  — layout-preserved, with `===== PAGE N =====` markers for exact-page citations.
- Manifest: `research/budget_materials/_manifest.csv` (51 books; status/sha/pages/url/paths).
- Extractor: `research/budget_materials/extract_budget_cuts.py` (one file, all exhibit types).
- Outputs: `workbook/extracted/{budget_line_items,budget_funding_facts,budget_p5_cost_elements,
  budget_oma_watercraft_notes,source_log}.csv`.

## B. How-to cookbook

**Re-run everything** (idempotent): from `research/budget_materials/`:
`python3 download_budget_books.py && python3 convert_to_txt.py && python3 extract_budget_cuts.py`.
The extractor prints tie-outs; a clean run has **no `WARN` lines** and "16/16 reconcile".

**Search the corpus** (always the `.txt`, never the PDF):
`grep -nE "<term>" txt_versions/FY2027/procurement/OPA_BA34_*.txt` — note the line, then read with a
PAGE-aware `awk '/===== PAGE 329/{p=1} p; /===== PAGE 330/{exit}'`. Find an exhibit page by its header
(`Exhibit P-40,` / `Exhibit P-5,` / `Exhibit R-2,` / `Exhibit OP-5`).

**Add a procurement line item:** add to the `LINE_ITEMS` dict (it auto-flows to P-40, P-5, dimension).
**Add a book:** add its per-year URL to `download_budget_books.py`, then register it in `CITED_BOOKS` +
`CITED_FY` for the source log.
**Add another RDT&E PE/project:** ⚠️ `extract_rdte` is currently hardwired to a SINGLE target
(`RDTE_PE`/`RDTE_PROJECT`/`RDTE_BOOK`). To add more PEs you must **generalize it to iterate a list of
targets** — don't just add dict entries. The discovery sweep that found the target lives inline in the
session log §2 (keyword-attribution to owning PE); re-run that logic if widening scope (e.g. to include
autonomy PEs beyond watercraft, or BA5/BA7 systems-development).

**Verify any new extraction:** every exhibit has a built-in tie-out anchor — use it. P-40: the `Total
Obligation Authority` row == `Net Procurement (P-1)`. P-5: `Gross/Weapon System Cost` (NOT Flyaway) ==
P-40 Net P-1. R-2: `Total Program Element` == sum of its project rows. Spot-check 2–3 cells against the
raw txt at the cited page before trusting a parse.

## C. Exhibit-grammar gotchas (the load-bearing parsing facts)

- **`-layout` text aligns columns by spaces.** Parse by anchoring on the trailing run of numeric tokens,
  not by character position. P-40/R-2 = **12 tokens**; P-5 = **18 tokens** (6 col-groups × unit/qty/total).
- **Column roles are derived from the PB year Y, not from labels** (OCO↔OOC drift is immaterial):
  `Prior | FY(Y-2) actual | FY(Y-1) enacted | FY(Y) Base | FY(Y) OCO | FY(Y) Total | FY(Y+1..Y+4) | To
  Complete | Total`. This is THE unifying spine across procurement and RDT&E — preserve it.
- **Cell conventions:** `-` → 0.0 (dollars) or blank (P-5 unit-cost/qty, where it means "not separately
  priced"); `Continuing` → blank (only in To Complete/Total rollups). **Per-FY analytical columns are
  always clean numerics** — that's where the signal is; prior_years/to_complete/total are as-printed.
- **Same exhibit type can appear twice per page set** — gate on the exhibit header (P-40 vs P-5's own
  6-col "Resource Summary"). **Strip page footers** (`LI …`, `UNCLASSIFIED`, `Volume 3 -`, `Army … Page`)
  before they pollute wrapped names.
- **Never pre-difference requested vs enacted across books.** The tidy long shape keeps every vintage's
  own view; the same FY is `request` in its PB book, `enacted` the next, `actual` the one after.

## D. Schema state + refactoring guidance (a likely next task)

Current tables (see headers in each CSV):
- `budget_line_items` — dimension; one row per fundable line (OPA BLIs + synthetic `RDTE-*` ids). Carries
  **`seed` analyst tags** (`mission_family`, `product_layer`) — judgment, deliberately separate from facts.
- `budget_funding_facts` — tidy/long; `(line_item_id, source_book_fy, exhibit, measure, unit, observed_fy,
  column_role, amount_type, amount, dollars_basis, page, source_id, extract_run_id, row_hash)`. Mixed
  appropriations & measures unified by the `column_role` spine + `measure`/`unit` discriminators;
  `amount_type` (added 2026-06-20) is the derived semantic money-kind — never sum across distinct values.
  `p5_cost_elements` / `oma_notes` likewise gained `amount_type`(p5)/`dollars_basis`/`extract_run_id`/`row_hash`.
- `budget_p5_cost_elements` — child grain (sub-line); 6 col-groups × 3 metric columns + `raw_context`.
- `budget_oma_watercraft_notes` — evidence, not facts; **never sum `amount_k`**.
- `source_log` — 15 cited books → workbook `11_Source_Log`.

**If you refactor, hold these invariants:**
1. **Keep the `column_role` spine** — it's what lets procurement, RDT&E, (and future contract) money
   coexist without being summed. The methodology's hard rule: never add request + obligations + ceiling;
   they're overlapping views. Model each as a distinct `column_role`/`measure`, never a total.
2. **Keep "faithful source data" separate from "analyst judgment."** Extracted CSVs = what the book says.
   Tags/mappings = editable analyst layer (the `seed` flag pattern). Don't bake judgment into the extractor.
3. **The likely refactor is capability-stack / parent-child alignment** (transcript §2).
   **⚠️ REVISED later the same day (2026-06-20) — see `2026-06-20_schema_adjustments_killchain.md`.**
   Corrected plan:
   - **Capability stack = a 4-node KILL-CHAIN spine, not a 6-layer list:** **Platform → Sensors →
     Effectors → C2** (the sensor-to-shooter / JADC2 decomposition). *Effectors keeps its literal kinetic
     meaning and is expected to be BLANK for Army maritime (logistics/maneuver, not strike) — a blank node
     is a valid answer; do not back-fill it.* Autonomy, assured PNT, comms and integration fold into **C2**;
     lifecycle/sustainment/training are NOT kill-chain nodes. Controlled vocabulary:
     `workbook/analyst/capability_nodes.csv`.
   - **A P-5 cost element is NOT a "work package."** A cost element is budget-native faithful evidence (it
     stays in `budget_p5_cost_elements.csv`); a work package is an *analyst* commercial decomposition of an
     opportunity. Do not equate them or bury analyst judgment in the extracted facts (invariant #2).
   - **Split the crosswalk into two bridges, not one:** (a) an **attribution bridge** (budget line / cost
     element → opportunity or work package) owning `addressable_content_%` + relationship type (Direct /
     Enabling / Comparable / Adjacent / Hypothesized); (b) a **capability bridge** (work package →
     `node_id`) owning fit/gap semantics. Both analyst-editable under `workbook/analyst/`, joined at build
     time — never new columns in the extracted facts. Preserves the guardrail that child values are
     *allocations* of the parent, never additive new markets.
4. Minor: `line_item_id` namespace is inconsistent (bare BLI for OPA vs `RDTE-…`). Normalizing to an
   appropriation prefix (`OPA-3569M11101`, `RDTE-0603804A-526`) would be cleaner if you touch it — but it's
   a join key referenced by 1008 fact rows + p5 rows, so migrate with a script, not by hand.

## E. Contract data — the next layer (05_Contracts_Awards / 06_Pipeline / recompete radar)

Transcript §3-4 is the spec. Different sources, NOT in the budget corpus — this is a fresh data pull.
Suggested approach (verify current API specifics — they change; my cutoff is Jan 2026):

- **USAspending.gov** — free, **no API key**. REST API (`api.usaspending.gov`) + bulk "Custom Award Data"
  downloads. Use for the award universe: prime awards + sub-awards, obligations, recipient/UEI, awarding &
  funding office, parent IDV, PSC/NAICS, competition type, place of performance, **current vs potential
  period-of-performance end dates** (the recompete-radar inputs). ⚠️ DoD/USACE data has a **~90-day
  reporting lag** — not the earliest signal.
- **SAM.gov** — **requires a free API key** (`api.sam.gov`), rate-limited. Opportunities API for the
  pipeline (sources-sought, RFIs, solicitations, special notices, award notices); Entity API for vendors.
  Use for the *forward* signal SAM surfaces before USAspending.
- **Army OSBP / ACC acquisition forecasts** — earliest planning signal; watch **ACC–Detroit Arsenal**
  (named watercraft competency) + ERDC/USACE.
- **Starting search params:** PSC **1940** (Small Craft) + NAICS **336611 / 336612**; then expand by the
  actual PSC/NAICS seen on hits (autonomy/engineering often classify non-maritime). Anchor on the programs
  we already have funding for: MSV(L) (`8211R01001`), Army Watercraft ESP (`3569M11101`), and the SLEP/MIBS/
  HCCC efforts from the P-5; search vendors/incumbents from awards.
- **Tie contracts back to the budget layer** via program/BLI/PE where derivable (so the workbook can show
  funded → on-contract). Keep contract money concepts (obligations, ceiling, funded value, remaining
  capacity) as **distinct `column_role`/`measure` values** in the same spine — never summed with budget $.
- **Recompete radar** (transcript §3): one row per contract *family* (predecessor → current → task orders
  → expected follow-on); estimate a *window* not a date; confidence scale (Confirmed/Strong/Inferred/
  Speculative) + a **separate** pursuit-access rating; track IDIQ task-order vs parent expiry and OTA
  follow-ons distinctly. Suggested CSVs mirroring the budget pattern: `contracts.csv` (family/award dim),
  `contract_obligations.csv` (tidy facts), `pipeline_notices.csv`, `recompete_radar.csv`, all feeding
  `source_log` (extend `CITED_BOOKS`-style registry, or a parallel source registry for non-book sources).

## F. The cross-cutting lessons (don't relearn the hard way)

- **Watercraft procurement is OPA BA3&4 (Vol 3), not BA1** — BA1 only has the P-1 index. (Whole reason the
  corpus had to be re-downloaded; see [[army-opa-watercraft-budget-source]].)
- **asafm.army.mil sits behind Akamai** — bare curl 403s; the full browser header set in
  `download_budget_books.py` passes; HTML index pages 403 even then, so URLs are probed/constructed, and
  filenames drift every year (FY25 OPA BA3&4 is literally titled "Other Support *Vehicles*").
- **O&M has no discrete watercraft line** — it's bundled program-change notes; the one clean signal is the
  FY27 Composite Watercraft Company stand-up. Don't try to build an O&M funding time series.
- **MSV(L) has no standalone RDT&E PE** — only the shared AoA PE; don't extract it as watercraft R&D.
