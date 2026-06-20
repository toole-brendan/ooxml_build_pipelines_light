# 2026-06-09 — DDG workbook: integrate OBBBA Sec. 20002(17) mandatory funding (FY2026)

## Problem / goal

Manager asked for the OBBBA "mandatory" (reconciliation) numbers to be integrated into the
DDG-51 workbook (`projects/ddg/workbook/workbook_ddg`) to inform FY2026 and FY2027. Source:
**FY 2026 Mandatory Funding Allocation Plan** (PL 119-21 Title II, a/o 2026-02-18), converted
from PDF to `/Users/brendantoole/projects3/obbba_funding_allocation_narrative_20260218.txt`
(`pdftotext -layout`, 3,110 lines).

## What the source says (DDG-relevant)

- **Sec. 20002 (Shipbuilding), line 17: $5,400.0M, all in the FY2026 column** — "Two
  additional Guided Missile Destroyer (DDG) ships … procurement of 2 DDG-51 destroyers in
  FY 2026, which is part of the current multiyear procurement contract. Funds for basic
  construction and government furnished equipment are expected to award starting in Q2 of
  FY 2026." (txt lines 319, 467–469). Obligation availability through 2029-09-30.
- **No FY2027 DDG money anywhere in the document.** FY27 stays discretionary-only
  ($4,256.9M, 1 ship, per the FY27 PB already in the workbook).
- The rest of Sec. 20002 ($29,176.3M total) is industrial-base (cross-platform /
  submarine-heavy), other-platform procurement, or fleet/capability — none of it is DDG-51
  SCN hull procurement. Only line 17 enters the model.

## Double-count verification (both directions)

- **Dollars: purely additive.** The FY27 PB P-1 resource summary shows FY2026 procurement
  **quantity = 0** (gross cost $306.1M; BC base in the model was $282.6M). The two FY26
  ships were funded by reconciliation, not discretionary SCN — nothing to net out of P-5c.
- **Hulls: already counted.** The production schedule already lists DDG 147 (HII) and
  DDG 149 (BIW) at FY2026, inside the 13 in-window hulls. An external-AI suggestion to add
  two placeholder hulls would have double-counted hulls (15) and broken the hull↔dollar
  reconciliation — rejected; the hulls got a one-line funding-source note instead.
- **No AP overlap.** FY26 AP base ($1,750M) is CY advance procurement for future hulls;
  the $5.4B is full-ship procurement of the two FY26 ships.

## Design decisions (user-confirmed)

1. Integrate the hull line only; the other Sec. 20002 lines stay out of the model (all 36
   lines are transcribed in the CSV for provenance; an on-sheet "considered & excluded"
   table was built, then removed in the trim pass below).
2. **BC/GFE split**: the source gives no breakout, so an editable Assumptions knob
   "OBBBA BC share of award" = **0.628** (= portfolio constant-$ BC / (BC + GFE) =
   $18,157.1M / $28,916.4M = 62.79%) allocates the BC-addressable portion.
3. **Booked all in FY2026, budget-year basis** (consistent with P-5c); no FY26/FY27
   execution-phasing knobs.
4. The existing **MYP-corrected BC supplier coefficient (12.55%) applies unchanged** — the
   ships are options under the same two MYP masters (same yards, same POP structure). The
   coefficient is a ratio over the POP corpus; the OBBBA award is not a published
   POP-bearing action, so there is nothing to fold in, and folding it in at the masters'
   reconstructed POP would leave the ratio ~unchanged.

## Changes

### NEW `extracted/obbba_ddg_mandatory.csv` (workbook + research mirrors)
All 36 Sec. 20002 lines: `section, line, item, fy2026_$M, included, category, note`.
Only line 17 has `included = 1`. Sums to the section total $29,176.3M.

### NEW `sheets/data_obbba_funding.py` → "OBBBA Mandatory" tab (data group)
- §1 Source line: 8 provenance fields + then-year FY row (blue input, $5,400.0M in FY26).
- §1b Constant FY2026 $M: then-year × `deflator_factor_cell(fy)` — follows the constant-$
  convention added earlier today (see `2026-06-09_ddg_sub_workbooks_constant_fy2026_deflator_conversion.md`).
  FY2026 factor = 1.00, so numerically a no-op; structurally consistent (levels deflated,
  ratios untouched).
- §2 BC/GFE bridge: two FY rows — OBBBA BC base (= const × Assumptions knob, $3,391.2M)
  and GFE / non-BC remainder ($2,008.8M, excluded from TAM).
- Accessors: `obbba_gross_cell(li, fy)`, `obbba_bc_base_cell(li, fy)`.

### EDIT `sheets/inputs_assumptions.py`
§2: third stream toggle "Include OBBBA mandatory (Sec. 20002(17)) in BC stream" (default 1,
0/1 dv) → `include_obbba_stream_cell()`. §5: knob "OBBBA BC share of award (BC vs GFE)"
= 0.628 (decimal 0–1 dv) → `obbba_bc_share_cell()`. Both added to the promoted-accessor
tuple/docstring; dv sqrefs extended.

### EDIT `sheets/model_tam_build.py` (§2)
- §2a: third toggle link row.
- §2b: new linked row "OBBBA mandatory BC base (Sec. 20002(17))" between `bc_raw` and
  `ap_raw`; `bc_in` is now
  `IF(N(bc_raw)+N(obbba_raw)=0,"", incl_bc*N(bc_raw) + incl_obbba*N(obbba_raw))`, labeled
  "BC base in TAM (P-5c + OBBBA mandatory)". Everything downstream (§5 TAM, headline,
  bridge, Exec Summary, SAM Build) inherits through the unchanged `bc_base_cell` accessor.

### EDIT note rows (one line each)
- `data_scn_budget.py` §1: FY2026 is discretionary-only; the two FY26 ships are
  OBBBA-funded (explains the otherwise-odd FY26 dip without touching P-5c provenance).
- `data_production_schedule.py` §3: DDG 147/149 funding-source note.

### EDIT sources / registry
- `sources_references.py`: SRC-15 (the allocation plan + CSV pointer) and CITE-06
  (PL 119-21 Title II).
- `sources_source_index.py`: dataset row + Budget-area rollup mention.
- `sheets/__init__.py`: registered after `data_scn_budget` in the data block (group
  contiguity assert passed).

### EDIT validation / summary / guide
- `validation_qa_reconciliation.py` (unregistered module, kept compiling): `_N_CHECKS`
  13 → 16; QA-14 gross ties to $5,400.0M; QA-15 FY26 BC-in-TAM = P-5c BC + OBBBA BC;
  QA-16 OBBBA FY2027 = 0.
- `validation_sensitivity.py`: §6 OBBBA BC-share sensitivity (gross, applied share, uplift
  @ applied / 55% / 70%, band width, % of portfolio TAM).
- `summary_executive_summary.py`: §2 TAM-bridge row "incl. OBBBA mandatory BC, FY26
  (Sec. 20002(17), 2 ships)".
- `guide_methodology.py`: §3 flow row, §4a/§4b scope bullets, new §4c "Mandatory (OBBBA)
  funding treatment" (three short statements).

## Trim pass (user: remove LLM-isms)

1. Deleted the OBBBA tab's "§3 - Sec. 20002 lines considered & excluded" table and the §2
   derived-share / applied-share / guardrail block; §2 banner parenthetical dropped. The
   BC-base formula now references the Assumptions knob directly. CSV keeps all 36 lines.
2. Follow-up audit removed the residue: stale "guard-railed on the OBBBA Mandatory tab"
   references (Methodology §4c + Assumptions comment) left behind by (1); the TAM Build §5b
   justification prose row; reviewer-reassurance tails on the SCN Budget / Production
   Schedule notes; "consistent with P-5c treatment" / "not discretionary SCN" field text;
   QA-16 "(source-backed; no phasing)"; module docstring "by construction" paragraph.
   Kept: "(no source breakout)" (load-bearing — it is why the knob exists), "-> tab"
   pointers (house idiom), SRC-15 context note (References is the context-note exception).

## Verification

Build `python3 build_workbook.py` (24 sheets, OBBBA Mandatory = sheet 9) +
`validate_workbook.py` (0 xml errors, 0 error-literal cells). Recalc via headless
LibreOffice (`-env:UserInstallation=file:///tmp/lo_ddg_profile --convert-to xlsx`) +
`openpyxl(data_only=True)`:

| Metric | Before | After |
|---|---|---|
| Portfolio TAM (FY22-27, constant FY26 $M) | 3,525.80 | **3,951.28** (+425.48) |
| BC-stream TAM | 2,278.08 | 2,703.56 |
| FY26 BC base in TAM | 282.60 | 3,673.80 |
| Exec Summary BC construction base | 18,157.1 (impl.) | 21,548.3 |
| Avg annual TAM ($M/yr) | 587.63 | 658.55 |
| Per-hull TAM (13 hulls, unchanged) | 271.22 | 303.94 |
| BC supplier coefficient | 12.546% | 12.546% (unchanged, by design) |
| SAM unbucketed residual | 1,185.78 (33.63%) | 1,328.87 (33.63%) |

- Toggle test: Include-OBBBA = 0 → portfolio TAM reverts to 3,525.80 exactly.
- 0 Excel error cells after every pass (incl. post-trim rebuild).
- Unregistered `validation_qa_reconciliation` render-tested manually (it is NOT compiled by
  the build — commented out of `SHEETS` — so syntax breaks there don't surface at build).

## Manager-expectation reconciliation (asked post-integration)

- BC construction base ↑ — yes (+$3,391.2M).
- BC supplier coefficient ↑ "implicitly" — **no, and correctly no** (see design decision 4).
  A coefficient rise would be a forward-looking outside-yards assumption → Sensitivity
  territory, not a source fact.
- BC stream TAM ↑ — yes (+$425.5M).
- SAM residual ↑ — **in dollars only, pro-rata** (share constant at 33.63%). The SAM
  allocates TAM by observed subaward shares, not evidence-matched dollars, so new TAM
  spreads across all buckets ~12.07% each. Observed subaward evidence untouched. If the
  conservative treatment is wanted (hold OBBBA TAM in unbucketed until subawards appear),
  that is a small SAM Build change — residual would go to ~$1,611M (~41% of TAM); offered,
  not implemented.

## Gotchas / notes for next time

- **Placeholder-hull trap**: the schedule's FY-2026 hulls ARE the OBBBA ships. Any future
  "add the mandatory ships" instinct double-counts hulls.
- **PB28 tripwire** (shared with the submarines overlay): if a future P-5c vintage starts
  carrying the mandatory-funded ships in the discretionary exhibit, net the OBBBA add or
  flip the toggle off.
- The FY26 column of SCN Budget (~$283M BC) looks anomalously empty *on purpose* — do not
  "fix" it by editing P-5c.
- `load_extracted_csv` coerces numerics, so `r["included"] == 1` (int) is the right test.
- `total_row` pads values out to `n_cols` — values list may be shorter than the divider.
- Deck untouched (slide 05 funnel etc. still pre-OBBBA); workbook and deck diverge until a
  deck pass.
