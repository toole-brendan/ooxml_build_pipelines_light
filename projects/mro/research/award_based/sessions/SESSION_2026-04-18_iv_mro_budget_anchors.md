# Session 2026-04-18 (iv): MRO Budget Anchors + SCN Reconciliation - v2.74 -> v2.76

## Context

Follow-on to session (iii). The Sub & Carrier Coverage sheet already
anchored FPDS award data to top-down budget-book line items via the
`Budget Anchors` data sheet (7 rows, 7 defined names). User asked to
extend that pattern to the rest of the Services (MRO) sheet so a reader
can see where the ~$7.1B FY25 Services TAM sits inside the ~$23B OMN
Ship Operations annual appropriation, with USCG ISVS as a small anchor
on the Coast Guard side.

User also flagged `data_v2.xlsx` as an earlier budget-focused research
input that holds most of the needed line items structured. Inspection
uncovered a second concern: the existing Sub & Carrier Coverage SCN
anchors diverged meaningfully from the same-line values in
`data_v2.xlsx` (notably Columbia $9.58B vs $3.36B, CVN RCOH $6.27B vs
$1.48B). User directed resolving that reconciliation against
`sources/SCN_Book.txt` as part of this change.

Ended at **v2.76** with:
- `sheets/budget_anchors.py` refactored to read from `data_v2.xlsx`,
  extended from 7 to **19 defined names** across 4 sections (OMN Ship
  Ops BA-1, SCN Capital Ships, USCG ISVS, NWCF Memo), with Excel SUM
  formulas for the 3 rollup cells.
- `sheets/services.py` with a new "FY2025 MRO Budget Reconciliation"
  block and "Budget-Book Anchors" reference table, both live via
  defined names.
- SCN nuclear-platform subtotal reconciled from $27.5B to $22.7B;
  Columbia now an Excel SUM formula (construction + AP) on the Budget
  Anchors sheet so the BA-01 rollup is transparent.
- New doc `docs/methodology/METHODOLOGY_MRO_BUDGET_RECONCILIATION.md`
  explaining why FPDS $7.1B != OMN CE 928 $2.4B (multi-year IDV
  actions, NWCF rate cross-charging, SCN-funded CVN RCOH, OPN spares).
- Standalone slide mockup `deck/SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md`
  describing the Budget-Book Anchor callout proposal for Slide 3
  (DECK.md untouched; mockup awaits delivery).

---

## Work completed, in order

### 1. Plan formation

Plan file at `~/.claude/plans/similar-to-what-the-peppy-lovelace.md`.
Three Explore passes in parallel captured: Services sheet structure
(10 sections, TAM headline + 3 cross-tabs + contractor views),
Sub & Carrier Coverage template (SUMIFS helpers, defined-name refs,
public-yard subtraction formula), and available OMN/NWCF/USCG budget
data in the `sources/*.txt` extracts. Plan agent returned a detailed
structural plan with 5 open design questions. User answered three via
AskUserQuestion:

- **Slide path**: callout on Slide 3 (not standalone Slide 6).
- **NWCF**: memo row only, no defined name.
- **Reconciliation structure**: FPDS + OMN side-by-side with explicit
  labeled gap row.

User then added: use `data_v2.xlsx` as source, and resolve the SCN
discrepancy as part of this plan (not a follow-up).

### 2. SCN discrepancy reconciliation against `sources/SCN_Book.txt`

Dug into the 1611N Detail P-1 exhibit. Findings:

| LI | Program | Canonical FY25 $K | Prior hard-coded $K | Basis |
|---|---|---|---|---|
| 1045 | Columbia Class | 9,580,774 | 9,580,774 | BA-01 rollup = construction $3,364,835 (line 227) + concurrent AP $6,215,939 (line 231) |
| 2013 | Virginia Class | 9,599,908 | 9,500,534 | Parent aggregate (construction + SFF + CPY) - data_v2.xlsx correct |
| 2086 | CVN Refueling Overhauls | 1,480,314 | 6,271,049 | Net FY25 execution authority - $6.27B conflated multi-ship program with single-FY - data_v2.xlsx correct |
| 2001 | CVN-80 Carrier Replacement | 1,359,124 | 1,359,124 | SFF + Completion PY - both sources agree |
| 2004 | CVN-81 | 674,930 | 800,492 | SFF for FY 2020 - data_v2.xlsx correct, prior Python was stale |

**Subtotal impact**: $27,512,073K -> **$22,695,050K**, -$4.8B driven
almost entirely by correcting LI 2086. This flips the Sub & Carrier
Coverage top-down-vs-FPDS framing: top-down $22.7B < FPDS $27.6B.
The direction of the gap now matches the MRO-side dynamic (FPDS
exceeds top-down because SCN is multi-year money - dollars enacted
in FY22-FY24 obligate on new FY25 task orders, and each FY25-dated
obligation lands in the FY25 FPDS sum regardless of BA vintage).

### 3. Budget Anchors refactor

`sheets/budget_anchors.py` rewritten end-to-end. Key decisions:

- **`SECTIONS` dict** replaces the old flat `LINE_ITEMS` list. Four
  section bands: OMN Ship Operations BA-1 / SCN Capital Ships / USCG
  Cutter Sustainment / NWCF Memo.
- **`load_budget_anchors()`** (memoized) reads `data_v2.xlsx` "Budget
  Data" keyed by `(source_book, title)`. Rows fall back to hard-coded
  `values` tuple when data_v2.xlsx doesn't cover the line (1B1B SAG
  total, and the 1B1B / 1B2B / 1B5B CE 928 sub-rows, all citing the
  relevant OMN_Book.txt line number).
- **Row `kind`** controls what gets written: `data` (values from
  data_v2 or fallback), `formula` (Excel SUM of other rows by line
  code), or `memo` (literal display only, no named range).
- **3 new formula rollups**: `OMN_SHIPOPS_BA1_TOTAL_FY25` (=SUM of 4
  SAG totals), `OMN_SHIPOPS_BA1_CONTRACT_FY25` (=SUM of 4 CE 928
  sub-rows), `SCN_COLUMBIA_FY25` (=SUM of construction + AP rows for
  LI 1045). Any upstream value correction propagates automatically.
- **12 new defined names**: OMN_1B1B_TOTAL, OMN_1B1B_CONTRACT,
  OMN_1B2B_TOTAL, OMN_1B2B_CONTRACT, OMN_1B4B_TOTAL (existing),
  OMN_1B4B_CONTRACT (existing), OMN_1B5B_TOTAL, OMN_1B5B_CONTRACT,
  OMN_SHIPOPS_BA1_TOTAL, OMN_SHIPOPS_BA1_CONTRACT, USCG_ISVS_TOTAL,
  USCG_ISVS_47MLB, USCG_ISVS_WMEC, USCG_ISVS_HEALY. Plus the 5
  existing SCN names repointed to their reconciled Budget Anchors
  rows (Columbia now a SUM formula).
- Total 19 named cells + 3 non-named rows (Columbia detail + NWCF
  memo) = 22 line items across 4 sections.

**v2.75 build** completed clean. Smoke test verified all 19 defined
names resolve, SCN values reconciled, OMN rollups write correct
formulas (`=E6+E8+E10+E12` etc.).

### 4. Services sheet budget reconciliation sections

`sheets/services.py` additions:

- **`_write_mro_budget_reconciliation`**: single consolidated table,
  FPDS and OMN side-by-side. FPDS rows reference `NAVY_TAM_SVC` /
  `CG_TAM_SVC` (already defined at end of `create_mro`); OMN rows
  reference Budget Anchors named cells via `=<NAME>/1000` for $M
  display. Explicit labeled "Implied gap" row at the bottom. FPDS
  subtotal and OMN BA-1 total are deliberately NOT summed into a
  cross-total (different denominators - FPDS FY25 is net sum of
  FY25-dated mod actions across every appropriation color; OMN CE 928
  is FY25-enacted OMN 1-year BA for one cost element only).
- **`_write_mro_budget_anchors_refs`**: reference table with three
  section bands (OMN BA-1 / USCG ISVS / NWCF Memo), one row per
  anchor linking to its defined name. NWCF memo is a literal cell
  (no named cell, no formula) with a caveat about no published
  public-shipyard-only line.
- **`_write_mro_budget_narrative_pointer`**: single gray-italic row
  pointing at `METHODOLOGY_MRO_BUDGET_RECONCILIATION.md`.

Insertion point in `create_mro`: immediately after the TAM Headline
block (which anchors `NAVY_TAM_SVC` / `CG_TAM_SVC`) and before the
Work Segment Coverage. This keeps the budget anchor adjacent to the
$7.1B TAM it contextualizes.

`F_GRAY` added to the styles import.

### 5. v2.76 build

Ran `python3 -m domnann.build_from_data`. v2.75 auto-archived.
v2.76 saved clean. Sheet order unchanged. Services sheet grew from
~225 rows to 381 rows, adding:

- Rows 235-249: Budget Reconciliation table (headline).
- Rows 252-271: Budget-Book Anchors reference table.
- Rows 273-274: Narrative pointer.

Spot-check via openpyxl: all defined-name references resolve (no
`#REF!` / `#NAME?`), NAVY_TAM_SVC still at Services!$C$218 and
CG_TAM_SVC at $C$219 (unchanged from v2.75), OMN_SHIPOPS_BA1_TOTAL
at 'Budget Anchors'!$E$14 (formula cell). Awards data and MRO PSC
filter logic are untouched so the underlying Services TAM value is
unchanged from v2.75.

### 6. Docs + session log

- **New**: `docs/methodology/METHODOLOGY_MRO_BUDGET_RECONCILIATION.md`
  (full narrative - appropriation color mixing, vintage mixing within
  multi-year money, lump-sum funding of multi-year performance,
  public-yard labor not in FPDS as a parallel structural point).
- **Updated**: `docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md`
  gains a "Live top-down anchors (v2.76+)" paragraph explaining the
  reconciled $22.7B SCN subtotal and pointing readers at the Budget
  Anchors sheet + the new MRO methodology doc.
- **Updated**: `deck/SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md` - SCN
  anchor table updated to reconciled values ($22,695 subtotal),
  narrative line rewritten to explain the direction of the
  FPDS-vs-top-down gap.
- **New**: `deck/SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md` - standalone
  proposal for the Slide 3 callout. Per user direction, DECK.md
  itself is not modified (it reflects delivered state only; mockups
  stay in standalone files until redrawn in the slide app).

### 7. Plan file course-correction

Four mid-session updates from the user:

- "data_v2.xlsx might be useful" -> inspected the Budget Data sheet
  (3,382 rows x 36 cols), found it covers 3 of 4 OMN Ship Ops SAGs
  (1B1B absent), most SCN line items, and full USCG ISVS detail.
  Adjusted plan to use data_v2.xlsx as primary source with Python
  fallback for the missing rows.
- "Resolve the SCN discrepancy as part of this plan" -> folded the
  SCN reconciliation into this session instead of a follow-up.
- "DECK.md shouldn't be updated, make a separate mockup file" ->
  reverted the DECK.md edit plan, wrote
  `SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md` instead.
- "FPDS obligations are per-mod transactions within FY25, not
  cumulative lifetime" -> corrected framing throughout. Initial draft
  described the FPDS-vs-OMN gap as "cumulative FPDS obligations
  against multi-year IDV ceilings"; that was wrong. FPDS FY25 is the
  net sum of mod actions dated within FY25 (each action paired with a
  specific appropriation). The gap vs OMN CE 928 is driven by (1)
  appropriation color mixing - SCN / OPN / NWCF-reimb on MRO PSCs,
  (2) vintage mixing - multi-year BA enacted earlier obligated as
  FY25 task orders, (3) lump-sum funding of multi-year performance.
  Public-yard labor invisibility is a separate structural point, not
  a gap driver. Rewrote `METHODOLOGY_MRO_BUDGET_RECONCILIATION.md`,
  the Services reconciliation Notes column, the
  `METHODOLOGY_CVN_SSN_COVERAGE.md` addition, and the two deck
  mockup files to use the correct framing. v2.77 is the post-
  correction build.

---

## Files created

- `sheets/budget_anchors.py` - full refactor (not new file; full
  rewrite)
- `docs/methodology/METHODOLOGY_MRO_BUDGET_RECONCILIATION.md` - new
- `deck/SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md` - new

## Files modified

- `sheets/services.py` - added 3 writer helpers + wired into
  `create_mro`; F_GRAY import
- `docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md` - added
  reconciled-SCN paragraph
- `deck/SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md` - SCN anchor table
  values and framing narrative updated

## Files unchanged (intentionally)

- `deck/DECK.md` - per user direction, reflects delivered state
  only; Slide 3 callout proposal lives in the new standalone mockup
- `sheets/sub_carrier_coverage.py` - no code changes; the defined
  names it references (`SCN_COLUMBIA_FY25` etc.) now resolve to the
  reconciled values automatically

---

## Workbook progression

| Version | Change | Impact |
|---|---|---|
| v2.74 -> v2.75 | Budget Anchors refactor: data_v2.xlsx loader, SCN reconciliation (3 values corrected, Columbia now a formula), 10 new MRO-side anchors | 19 workbook-scope defined names (up from 7). Sub & Carrier Coverage top-down subtotal shifts from $27.5B to $22.7B. FPDS-captured remains $27.6B -> gap flips: FPDS now exceeds top-down, same pattern as MRO side. |
| v2.75 -> v2.76 | Services sheet gains Budget Reconciliation + Anchor Refs sections (1 subsec band + ~35 rows) | Services sheet grows from ~225 rows to 381 rows. No change to TAM, cross-tabs, or contractor blocks; no change to other sheets. |

v2.76 is current.

---

## Open flags

- **Slide 3 callout not yet drawn** - `SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md`
  describes the proposed addition. When the actual slide is redrawn,
  update DECK.md and replace the screenshot reference per the mockup
  file's "When this moves into DECK.md" section.
- **Services formula-length guardrail** (carried over from sessions
  i and ii) - still staged but unverified in real Excel open.
- **Army Watercraft Maintenance ($137M)** - still not excluded from
  Depot Ship Repair TAM; has no bearing on this session's changes.
- **NWCF public-shipyard slice** - memo-only treatment; a harder
  figure would require extracting NAVSEA 07 workload plan data
  (30-year shipbuilding plan or Naval Shipyards workload exhibit)
  which is not in the current source set.
- **FY27 coverage** - data_v2.xlsx has FY27 Request column but
  Budget Anchors does not yet surface it. Low-priority; not asked.
- **v2.76 not yet opened in Excel** - smoke-test via openpyxl
  confirms formula strings are valid and defined names resolve, but
  only Excel's evaluation confirms the cells actually compute to the
  intended values. Worth a manual open.
