# 2026-06-22 — Subaward Activity: incorporated external review (honest labels, two-tier axes, live churn)

Third session of the day on `award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`). The prior session rewrote **Subaward Activity** into a
4-section sheet with two native tables (see `2026-06-22_subaward_activity_multisection_refactor.md`).
This session **incorporated an external review** of that sheet. The review's verdict: the math and
workbook engineering are strong (**9/10 plumbing**) but the **terminology overstated what the data
proves** (**7/10 as published analysis**). Every critique was confirmed against the source and is
valid. All changes land on **one file** — `sheets/subaward_activity.py`. Build is clean (**22 sheets,
16 native tables, 0 XML errors, 0 style hard-failures**).

Everything is **uncommitted** (working tree only).

---

## The one mid-flight design correction (load-bearing)

The plan first proposed materializing a per-engagement 0/1 "in prior block" helper to drive §4
churn. The user rejected that: **churn must be live formulas — no hardcoded calculation results.**
Reworked §4 to be **fully live**: each block row embeds its own label *and* its predecessor label as
string **literals** (exactly as §4 already embeds the block label in `COUNTIF`), and every count and
dollar is a `SUMPRODUCT`/`SUMIF` over §3. The only hardcoded thing is the chronology *assumption*
(`_BLOCK_PRED`) — input/judgment, like the block labels themselves. Net effect: **no build-script
change, no new CSV column** — the two spines are untouched.

---

## Decisions locked (user chose the fuller scope on all four)

- **Two-axis transparency** — rename `Vendor Type` → **Observed Activity Profile**, and expose the
  two driving axes as their own integer **Breadth Tier** (0-3) and **Duration Tier** (0-3) columns in
  both native tables. Profile now = `CHOOSE(MAX(breadth tier, duration tier)+1, …)` referencing the
  two tier CELLS (no recompute).
- **Honest category labels** — `Single / one-time · Limited · Established · Core / sustained`
  (replaces the mechanism-claiming `One-off / single-component · Repeat-buy, short window ·
  Recurring · Core / long-running`; the old names implied repeat-buying / component complexity a
  single axis can't establish). **Proposed defaults — adjustable.**
- **§4 churn built for real** (fully live, see above) — `New · Returning · Returning % ·
  Retention % · $ to Returning`, with the section renamed **Activity by block / MYP: churn vs
  continuity** (it now earns the claim).
- **Renumber 1-4 top-to-bottom** — Type summary = **§1** (was §3), Vendor rollup = **§2**, Engagement
  detail = **§3** (was §1), Block = **§4**. Internal vars renamed to roles (`type_/roll_/eng_/blk_`).
- **§3 single-leaf binding** — each engagement row's net/reports/neg-adj/first/last reference **only
  its own program leaf** (PIIDs are program-disjoint, so the other two leaves contributed exactly 0).
  The §1 `MAX(MINIFS…)` "drop the zero" trick is gone (no non-matching leaves left to zero out). §2
  stays **3-way additive** — a UEI legitimately spans programs.

---

## Label / framing fixes (the review's substance)

- **"Distinct Subawards" meant two different things.** §2 counts UEI-level distinct subaward numbers
  (Σ = **14,700**); §3/§4 count UEI×PIID-level (Σ = **14,919**; EB reuses a subcontract number across
  prime PIIDs). Disambiguated: §2 → **Distinct Subaward Numbers**, §3/§4 → **Distinct PIID-Subawards**
  (ASCII hyphen — en/em dashes are a style_audit hard-fail).
- **`Corrections` → `Negative Adjustments`** — the formula only counts reports with
  `Subaward Amount $ < 0` (deobligations / negative adjustments, not necessarily corrections; positive
  corrections aren't counted).
- **`Coverage % PoP` → `Action Span / PoP %`** — "coverage" sounded more definitive than the measure
  is (same-date first/last actions read as 0%).
- **Clipping fixed** — §1/§4 are styled blocks that started in column B (UEI width 14), clipping
  "One-off / single-component" and "Virginia Block V (LLTM)" into the numeric column C. Both now
  start at **column C** (`start_col=2`), where the 31-wide vendor-name column holds the labels.
- **Stale number removed** — dropped the hardcoded `$13,883.99M` from the caption ("reconciles to the
  program-vendor total" instead).
- **Reconciliation cells** — §1 and §4 total rows now carry live **100%** in their percent columns
  (sum of the column = an immediate cross-check).

---

## Grid (one worksheet, B..Q = 16 cols, two native tables)

```
 B UEI | C Vendor | D Distinct subawards | E Breadth Tier | F Span | G Duration Tier
 H Observed Activity Profile | I Net $M | J Reports | K Negative Adjustments
 §3:  L Program | M Prime PIID | N Block/MYP | O Action Span / PoP % | P First | Q Last
 §2:  L Distinct PIIDs | M Distinct Programs
```
Tables: `SubawardVendorRollup` (B..M, 12 cols) · `SubawardActivity` (B..Q, 16 cols). §1/§4 are styled
blocks (start at C). Section banners renumbered §1..§4 in display order.

---

## Build / verify

```
python3 scripts/build_subaward_activity.py    # unchanged: 2485 §3 rows + 1102 §2 rows
python3 build_workbook.py                      # -> 22 sheets, 16 native tables, 7 note parts
python3 validate_workbook.py                   # 76 parts, 0 xml errors, 0 error-literal cells
python3 tools/style_audit.py                   # 0 hard failures; 1 warning (pre-existing, below)
```

**style_audit:** the lone warning is `[Methodology] column C width 84 (>44)` — an **untouched** sheet
(prior-session carry-forward). The renamed long headers (`Negative Adjustments`,
`Action Span / PoP %`, `Distinct PIID-Subawards`, `Observed Activity Profile`) did **not** trip the
width rule (their columns stay ≤ 26).

**Gold-standard recalc diff — STARTED, NOT FINISHED.** soffice headless recalc succeeded; the
independent replica was built from the recalc'd transaction leaves (**19,655 rows**: DDG 6,020 ·
Virginia 8,443 · Columbia 5,192). The per-cell diff phase was **aborted** — the ad-hoc verifier used
openpyxl `read_only` **random** cell access against the Subaward Activity sheet, which is
pathologically slow. **Must rerun** with an iterate-the-sheet-once approach before the numbers are
trusted / committed. The scratchpad verifier already encodes every check (net, reports, neg-adj,
distinct, breadth/duration tiers, profile, block, §1 summary totals, §4 churn incl. the
`New + Returning = # Vendors` identity, and the $13,883.9944723494 reconciliation) — it just needs the
cell-access rewrite.

---

## Files

- **Edited (only file):** `workbook_award_classification_refactor/sheets/subaward_activity.py`
  (flat-but-large rewrite: grid constants, tier columns + Profile, header/label renames, §1/§4
  `start_col=2` + formula shifts, `_BLOCK_PRED` + live §4 churn, §3 single-leaf formulas, total-row
  100%, docstring + INTRO/CAV1/CAV2 prose).
- **Regenerated artifact:** `award_classification_refactor.xlsx`.
- **Ad-hoc (scratchpad, not committed):** `verify_subaward.py` (the gold-standard checker; needs the
  iterate-once fix described above).
- **No change:** `scripts/build_subaward_activity.py`, `scripts/pull_prime_awards.py`,
  `sheets/prime_awards.py`, or any other sheet module.

---

## Carry-forward

- **Gold-standard per-cell recalc diff is NOT complete** — rerun the verifier (iterate-once) and
  confirm 0 mismatches + Σ Net = 13,883.9944723494 **before committing**. Build/validate/style are
  green, but the live values have not yet been independently re-confirmed this session.
- **`_BLOCK_PRED` chronology is hand judgment** — esp. whether Virginia `LYS (cross-block)` belongs in
  the `IV → LYS → V → VI` chain or should be skipped. Surface for review. (DDG and Columbia chains are
  unambiguous; Columbia has no predecessor.)
- **Observed Activity Profile category labels** (`Single / one-time` … `Core / sustained`) are
  proposed defaults — easy to re-word after seeing them rendered.
- **`Action Span / PoP %`** rename — confirm the wording reads right.
- **Pre-existing `[Methodology] column C width 84` warning** — still needs confirming as pre-existing
  (not a regression) before committing, per the prior session.
- **Nothing committed** — all working tree only.
```
