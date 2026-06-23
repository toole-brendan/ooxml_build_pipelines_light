# 2026-06-22 — Subaward Activity: fuller churn split + breadth×duration matrix (2nd review)

Fourth session of the day on `award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`). The prior session incorporated a first external review and
rewrote **Subaward Activity** into honest two-axis labels with live §4 churn (see
`2026-06-22_subaward_activity_review_incorporation.md`). This session incorporated a **second
external review** of that same sheet. The review's verdict: **8.5/10 and worth keeping** — the
engineering and most semantics are now strong, but one **substantive** problem remained plus
polish. Every change landed on **one file**, `sheets/subaward_activity.py`. Build is clean
(**22 sheets, 16 native tables, 0 XML errors, 0 style hard-failures**).

Everything is **uncommitted** (working tree only).

---

## The substantive fix (the review's core point)

§4's "New / Returning" only tested the **immediately-preceding** block, so a vendor that **skipped a
block and came back** was mislabeled "New." Material in the live data: for **Virginia Block V** the
old formula would call 344 vendors "New" when only **208** are genuinely first-observed — **136** are
*reactivated* from Block IV via a skipped LYS, and **114** *continued* from LYS.

User chose the **fuller analytical split** (over the minimal relabel). §4 now splits each block's
vendors three ways, all **fully live** over §3:

- **First observed** — UEI never appears in ANY earlier block of the program's chain.
- **Reactivated** — UEI appears in some earlier block but NOT the immediate predecessor.
- **Continued from prior** — UEI appears in the immediate predecessor.

Identity (exact by construction): `First observed = # Vendors − Reactivated − Continued`. The new
`_earlier_blocks(blk)` helper walks `_BLOCK_PRED` back to the program's first block; those labels are
embedded as string literals in an `in_any = ((COUNTIFS…+COUNTIFS…)>0)` term, and `Reactivated`
uses the SUMPRODUCT-safe `in_any * (1 - in_pred)`. The `/_distinct` dedup is unchanged, so per-UEI
booleans collapse to one count per vendor exactly as `# Vendors` already does.

Static confirmation (no recalc needed): `_earlier_blocks("Virginia Block V (LLTM)")` →
`["Virginia LYS (cross-block)", "Virginia Block IV (LLTM)"]`. So Block V's `in_any` tests {LYS,
Block IV}; Reactivated = in-Block-IV-not-LYS = the 136; Continued = in-LYS = 114; First observed =
458 − 136 − 114 = **208**. The reviewer's cited partition reproduces.

---

## Decisions locked (user chose the fuller scope on all four)

- **§4 = fuller split** (First observed / Reactivated / Continued from prior), not the minimal relabel.
- **Keep LYS** as Virginia Block V's named predecessor (contract-to-contract). Block-IV returnees
  that skipped LYS now surface as **Reactivated**, so the procurement-block continuity is visible on
  the sheet without changing the chain. (`_BLOCK_PRED` unchanged.)
- **Add a 4×4 breadth×duration matrix** (§1b) — the headline Profile collapses both axes with `MAX`;
  the matrix shows them.
- **All three wording changes**: `Core / sustained` → `High / sustained activity`; §1 banner
  re-frame; shorten §2/§3 headers.

---

## What changed (one file: `sheets/subaward_activity.py`)

- **§4 rebuilt — 14 cols C..P:** `Block / MYP · Compared with · # Vendors · First observed ·
  Reactivated · Continued from prior · Continuation % · Prior-block retention · # Engagements ·
  PIID-Subaward Pairs · Net Subaward $M · $ to continued · Continued $ % · % of Portfolio $`. New
  `_earlier_blocks()` helper; loop body + 14-col total rewritten. Baseline blocks (DDG FY11, Virginia
  Block IV, Columbia — absent from `_BLOCK_PRED`) show `-` for D/G/H/I/J/N/O and `First observed =
  # Vendors`. Total row: `SUM` ignores the `-` text cells; ΣE must equal ΣF+ΣG+ΣH; ΣP = 1.00.
- **§1b matrix (new styled block, C..H):** breadth-tier rows × duration-tier cols, cells =
  `COUNTIFS` over §2 breadth/duration tier columns (new `RP_BTIER`/`RP_DTIER` ranges), row + column
  totals. Grand total reconciles to **1102** = §1 # Vendors total = §2 row count. An italic caption
  (`MTX_CAP`) states the tier thresholds and flags them as **analyst-defined descriptive
  thresholds**; the row/col labels embed the cut points (`Breadth 0 (1 sub)`, `Dur 2 (2-6y)`, …).
- **Predecessor visibility:** `Compared with` column names each block's predecessor (the modeling
  judgment is now on the sheet). `-` for baseline blocks.
- **Right-censoring note:** italic caption (`BLK_CAP`) under §4 — "continuity is observed-to-date,
  later blocks are right-censored, so continuation/retention are lower bounds."
- **Wording / labels:** `_PROFILE_LABELS` `Core / sustained` → `High / sustained activity` (ripples
  through CHOOSE, §1, matrix corner); §1 banner `Observed activity profile: recurring vs one-off` →
  **Observed activity intensity**; `% of $` → **% of Portfolio $** (§1 + §4); new **Continued $ %**
  (= $ to continued / block net $). Header shortenings (ASCII hyphens — en/em dash is a style
  hard-fail): `Distinct PIID-Subawards` → **PIID-Subaward Pairs** (§3 + §4), `Negative Adjustments` →
  **Neg. Adjustments** (§2 + §3), `Action Span / PoP %` → **Span / Prime PoP** (§3). `_CENTER` sets
  and `CAV2` prose updated to match. §2 keeps `Distinct Subaward Numbers` (still disambiguated).
- **Pass-1 row math:** inserted `mtx_banner/mtx_cap/mtx_header/mtx_first..mtx_last/mtx_total` (after
  §1) and `blk_caption` (in §4); docstring layout list + §4 semantics updated.

**No CSV / build-script change** — the §3 spine already carries UEI + a live block label per row, so
the whole split is live formulas. The two row spines are untouched.

---

## Grid (§4, styled block, start at C; C..P = 14 cols, Q blank)

```
 C Block / MYP | D Compared with | E # Vendors | F First observed | G Reactivated
 H Continued from prior | I Continuation % | J Prior-block retention | K # Engagements
 L PIID-Subaward Pairs | M Net Subaward $M | N $ to continued | O Continued $ % | P % of Portfolio $
```
§1b matrix (start at C; C..H = 6 cols): `C Breadth\Duration | D..G Dur 0..3 | H All`.

---

## Build / verify

```
python3 build_workbook.py        # -> 22 sheets, 16 native tables (matrix/§4 stay styled blocks), 7 note parts
python3 validate_workbook.py     # -> 76 parts, 0 xml errors, 0 error-literal cells
python3 tools/style_audit.py     # -> 0 hard failures; 1 warning (pre-existing [Methodology] width 84)
```

First §1b banner draft tripped a new `section title >60 chars` warning (84 chars); shortened to
`§1b - Breadth x Duration matrix (vendor counts by tier)` and rebuilt → back to the lone
pre-existing Methodology warning. The renamed/short §4 headers did not trip the width rule.

**Gold-standard recalc diff — SKIPPED this session (user instruction).** The soffice headless
per-cell recalc diff that the prior session left unfinished was explicitly de-scoped this session.
The **chain-walk logic** (highest risk) is confirmed statically (above), and the build's
`assert c.at() == …` Pass-1 row checks all passed — but the live cell **values** (that Block V
computes exactly 458/114/136/208, matrix grand total = 1102, Σ Net = 13,883.9944723494) are **not**
independently recalc-confirmed.

---

## Files

- **Edited (only file):** `workbook_award_classification_refactor/sheets/subaward_activity.py`
  (`_earlier_blocks` helper; `_BLK_*` rewrite; `_MTX_*` + `RP_BTIER/RP_DTIER`; `_PROFILE_LABELS`;
  header/label renames + `_CENTER` sets; `MTX_CAP`/`BLK_CAP`; §1 banner; Pass-1 rows; docstring/CAV2).
- **Regenerated artifact:** `award_classification_refactor.xlsx` (the 2nd reviewer's copy was stale;
  this rebuild contains the new module).
- **No change:** `scripts/build_subaward_activity.py`, any CSV spine, or any other sheet module.

---

## Carry-forward

- **Live values not recalc-confirmed** — if/when desired, run the iterate-once soffice recalc diff
  and confirm Block V = 208/136/114/458, per-block `F+G+H == E`, ΣP = 1.00, matrix grand total =
  1102, and Σ Net = 13,883.9944723494 **before committing**. Build/validate/style are green.
- **`_BLOCK_PRED` is still hand judgment** — Virginia LYS kept as Block V's predecessor; Block-IV
  returnees now show as Reactivated, so the choice is visible. Still flag for review.
- **§4 cosmetic header overflow** — long headers spill into the next header cell (as before); data
  cells (ints/%) don't clip. A width-optimized column order exists if undesirable.
- **Pre-existing `[Methodology] column C width 84` warning** — carry-forward, not a regression.
- **Nothing committed** — all working tree only.
