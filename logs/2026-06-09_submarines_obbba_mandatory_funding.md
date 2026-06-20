# 2026-06-09 — Submarines workbook: OBBBA Sec. 20002 mandatory funding

## What

Integrated OBBBA (PL 119-21 Title II, reconciliation) mandatory funding for
submarine new construction into `projects/submarines/workbook` as a separate
data sheet — never an edit to the SCN Budget P-5c source. Source: FY 2026
Mandatory Funding Allocation Plan (2026-02-18), Sec. 20002 Shipbuilding
($29,176.3M, all FY2026 BA; FY2027 column is zero; obligation availability
through 2029-09-30). Only Sec. 20002(16) — second FY2026 Virginia-class
submarine, $4,600.0M — is new-construction procurement and feeds TAM.
Submarine-relevant capacity / workforce lines ($2,900.0M: items 1, 2, 3, 10, 13,
14, 15) are memo evidence (SIB-style exclusion); repair / nuclear-adjacent lines
(dry dock, cold spray, Ohio tube conversion) memo-excluded.

## Double-count verification

Every PB vintage (PB22–PB27) reports Virginia FY2026 qty = 1; the workbook FY26
column (PB2027 via `reconcile_best_vintage`) is the discretionary boat only
(TSE $5,389.1M). PB2027 restated FY26 TSE from PB2026's $3,465.5M — still qty 1 —
so a tripwire pins Virginia FY26 TSE to $5,389.109M: a future PB2028 refresh that
folds the reconciliation boat into FY26 FAILs the check, signalling the mandatory
stream must be zeroed or re-based.

## Mechanics

- NEW `sheets/data_obbba_funding.py` ("OBBBA Mandatory", data group, after SCN
  Budget): §2 source line (authority / title / scope / award timing fields) +
  then-year award grid, §3 BC/GFE bridge (gross × BC share, FY27 via spillover,
  GFE / non-BC remainder row, × deflator to constant FY2026), §4 capacity memo,
  §5 excluded memo. Full-gross sensitivity row at render (lazy TAM Build import).
  No checks block on the data sheet (not the house idiom — checks live on model
  sheets); the TSE tripwire sits in TAM Build §5.
- `inputs_assumptions.py`: "Include OBBBA mandatory (Sec. 20002(16)) stream"
  toggle (§2, 0/1 dropdown), new §4 controls — FY2027 execution spillover %
  (default 0) + "OBBBA BC share of award" (observed = Virginia FY26 P-5c BC%
  ≈ 58.2%, linked, + adjustment); old §4–§6 renumbered §5–§7.
- `model_tam_build.py`: third stream — "OBBBA mandatory BC base" rows per class
  in §2, portfolio row, §4 "TAM - OBBBA mandatory (BC coeff)" rows at the SAME BC
  coefficient (35.0%), `br_obbba` bridge row, tw-coeff denominator, §4e
  cumulative OBBBA base/TAM rows, removal = BC base + OBBBA base − TAM, §5
  three-stream identity check + "Virginia FY26 ship estimate ties to PB2027"
  tripwire (anchor 5,389.109). `_BN_BASE` 13→14.
- Exec Summary: §1 "incl. OBBBA mandatory TAM" line, new §2c OBBBA bridge
  subsection (old §2c → §2d), §3 table gains an OBBBA mandatory TAM column.
- Figure Register: DO-58..62 (gross award / mandatory BC base / mandatory TAM /
  FY26 TAM / capacity memo). Methodology: definition + flow + scope + exclusion
  rows + hover note.
- Source Index: allocation-plan row (§2 + refresh); narrative txt copied to
  `projects/submarines/docs/`. References: claim 31 appended to
  `industry_baseline_citations.csv` (workbook + research copies, kept identical).
- Dormant `validation_qa_reconciliation.py` updated for parity (QA-13..17).

## DDG parity pass

The DDG workbook (`projects/ddg/workbook`) received its OBBBA Sec. 20002(17)
integration separately; submarine terms were aligned to it so the two read as
siblings:

| Term | DDG (reference) | Submarines (after alignment) |
|---|---|---|
| Tab name | OBBBA Mandatory | OBBBA Mandatory (was "OBBBA Funding") |
| Module / entry | `data_obbba_funding.py` / `OBBBA_FUNDING` | same |
| Authority cite | PL 119-21 Title II, Sec. 20002, line 17 | same form, line 16 |
| Source-line field block | §1 (authority/title/scope/timing) | added (§2) |
| Bridge naming | "BC/GFE bridge", "OBBBA mandatory BC base" | same (was "BC-equivalent conversion") |
| GFE remainder row | "GFE / non-BC remainder (excluded from TAM)" | added |
| Toggle / share accessors | `include_obbba_stream_cell` / `obbba_bc_share_cell` | same |
| BC base accessor | `obbba_bc_base_cell` | renamed from `obbba_bc_equiv_cell` |
| Exec line | "incl. OBBBA mandatory BC, FY26 (...)" | "incl. OBBBA mandatory TAM $M (...)" |
| QA label | "OBBBA gross award ties to Sec. 20002(17)" | same form, (16) |

Intentional differences kept (content, not naming): submarines runs OBBBA as its
own toggled TAM stream (visible delta vs BC stream) where DDG folds it into the
BC stream; submarines' BC share is linked to the P-5c ratio (DDG: flat 0.628
input); submarines adds the FY2027 spillover control and the capacity / excluded
memo sections (DDG sources its line items from `obbba_ddg_mandatory.csv`).

## Numbers (recalc-verified via soffice)

- OBBBA BC base: $2,677.5M (4,600 × 58.21%); GFE / non-BC remainder $1,922.5M;
  mandatory TAM **$937.7M**, all FY26.
- Portfolio TAM FY26: 3,606.2 → **4,544.0**; FY27 unchanged (5,403.5).
- Cumulative TAM 20,274.4 → **21,212.2**; broad SAM → 18,625.3.
- A/B: toggle off restores 20,274.4 exactly; spillover 25% moves $229.7M
  (constant FY26) into FY27 with then-year split invariance holding.
- All sheet checks OK, anchor regression OK, zero error cells.

## Open

- Deck/chart treatment of the OBBBA stream (z_ChartData blocks untouched; values
  flow through links, but no OBBBA series exists yet) — separate decision.
- On any budget-book refresh to PB2028: watch the TSE tripwire (TAM Build §5 /
  dormant QA-16).
