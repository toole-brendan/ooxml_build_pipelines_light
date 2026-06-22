# 2026-06-21 — Phase 1 (instrument/observability) built, validated against prime data, then reverted

Short session. Began executing `TENTATIVE_PLAN.md` PART A; built Phase 1, then a quantification + a USAspending
prime-data cross-check showed the dollar issue it addressed is **footnote-level**, so Phase 1 was reverted. The
workbook is back to its byte-identical green baseline. Pending army + distributed-shipbuilding work was committed
and pushed to `origin/master`. Detail of the decision lives in the **ADDENDUM** at the bottom of
`sam/TENTATIVE_PLAN.md`; this log is the session narrative.

## What happened
1. **Phase 0** — branched `feat/award-classification-foundation`, snapshotted the `.xlsx` + transaction CSVs,
   confirmed the green 12-sheet baseline (build + validate clean).
2. **Phase 1 (built)** — appended an instrument + observability layer to the three subaward-transaction sheets
   (Instrument ID conservative/split, Reports-in-Instrument, Exact-Duplicate?, Cross-Prime-Key?, Ledger Signature,
   Positive/Negative dollar split, Reporting-Threshold-Regime, Recent-Period-Provisional?, Vendor-of-Record-Masking?)
   plus a new **Reported Instruments** tab. Done via a post-processor (`enrich_program_transactions.py`) because
   `build_program_transactions.py` can't re-run here — its source FSRS JSON isn't in this working tree. Built green
   (13 sheets), reconciled to $12.487B. Threshold dates web-verified ($25k→$30k 2015-10, →$40k 2025-10).
3. **Quantified the dollar risk** (to decide whether Phase 1 was worth it): credible overstatement ~2–8%,
   submarine-driven; **45% of dollars are in single-report instruments (no ambiguity)**; the −42% "cumulative=last"
   interpretation is an artifact of correction ledgers ending negative.
4. **Pulled the 6 submarine prime contracts from USAspending** (no API key needed; `Prime Contract Key` = the
   USAspending award id). Subawards are **~9% of prime obligations** ($8.88B vs ~$95B) → under-capture, not
   over-count. **USAspending's own subaward totals match ours to the dollar on 5 of 6 contracts** → our "sum the
   rows" methodology = what the government portal does.
5. **Columbia N0002417C2117 anomaly** (USAspending $7.75B vs ours $3.50B) = **BlueForge Alliance**: $4.214B across
   7 cumulative-snapshot records under subaward# `1000042855`, which we **correctly filter out** (MIB intermediary,
   not a hull subcontractor). Validates our scope; our figure is the cleaner one.
6. **Decision: reverted Phase 1 entirely** (`git restore` tracked files + delete the new script/sheet/CSVs) — back
   to the byte-identical 12-sheet baseline (5,895,937 bytes, 10 tables, 0 errors). Switched to `master`, deleted the
   no-op feature branch (it had no commits; identical to master).
7. **Committed + pushed** pending other-folder work to `origin/master` (`c8fdc925..aa0603c1`): army recompete
   calendar/radar; distributed-shipbuilding SAM plan + logs + a TAM GFE note.

## Outcome
- **Methodology validated** — "sum the report rows" matches USAspending and sits far under the prime ceiling;
  defensible as the canonical public figure. Residual cumulative-restatement risk is a footnote (~2% exact-dups).
- **Workbook unchanged from baseline** — Phase 1 left no trace; no instrument layer in the tree.
- `TENTATIVE_PLAN.md` body untouched; an addendum records this decision and closes Open decision #2.
- **Phases 2–4** (month/CY-FY, SWBS apply, FY2026$) remain available but were not started.

## For any future "$X B" headline
Label it: *first-tier reported flow; matches USAspending; under-captures true subcontracting; BlueForge/MIB
excluded.* Drive "where to play" off shares / counts / rankings (robust to the re-filing question).
