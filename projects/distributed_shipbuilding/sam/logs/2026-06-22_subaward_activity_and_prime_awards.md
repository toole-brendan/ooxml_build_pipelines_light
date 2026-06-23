# 2026-06-22 — Subaward Activity sheet (PoP proxy) + Prime Awards data sheet

User-driven build session on `award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`). Goal: "back into" a period-of-performance metric for
subawards (FFATA has no PoP field, unlike primes). Net result: workbook grew **20 → 22 sheets**
with two new tabs — a live **Subaward Activity** sheet (summary group) and a materialized
**Prime Awards** data sheet — arrived at through a data-model investigation that reframed the
metric twice and discarded a classification scheme before it was built. Build is clean
(**22 sheets, 0 XML errors, 0 error-literal cells, style audit 0/0, 15 native tables**); the
$12.08B / $13.88B headline is untouched.

(Same session also committed + pushed the pending **army house-style + shipbuilding SIB-doc**
work to `origin/master` as `4a2c3058`, and added a `.gitignore` rule for Office `~$` lock
files. That is unrelated to the SAM workbook; the two new SAM sheets below are **uncommitted**.)

---

## The load-bearing investigation — there is NO "modification" field in FFATA subaward data

The ask started as "modifications per UEI per PIID." Chasing whether that's even a real signal
drove the whole design. Findings, each verified:

1. **No modification / action-type field exists.** Dumped the full key-union across our 269
   cached raw pulls **and** a fresh live API call (`api.sam.gov/prod/contract/v1/subcontracts/
   search`, HTTP 200) — both return the **identical 28 fields**, none of which is an
   amendment/action-type/version flag. `subAwardReportNumber` is a **UUID** (not a sequence);
   `primeAwardType` is uniformly `AWARD` (the prime's type); `referencedIDVPIID` is empty on
   every record (all our primes are definitive contracts, no IDV delivery orders). So there is
   no native modification signal and no award-type dimension to mine.

2. **`subAwardNumber` is NOT a reliable "one subcontract" key.** Tracing repeat reports on one
   number showed it is used inconsistently: blanket/IDIQ numbers (e.g. `1000055031` = **170**
   separate dated actions over 2021–2024, including negative corrections, under ONE number) vs
   single-PO numbers (`GPR224-004`). It also **collides across UEIs** (Virginia 84, Columbia 58
   cases — simple numbers like "1" reused), so the only safe instrument key is the triple
   `(UEI, PIID, Subaward Number)`. Consequence: "reports per subAwardNumber" ≠ modifications and
   "distinct subAwardNumbers" ≠ clean subcontract breadth.

3. **The report-ID dedup does not prune modifications.** `build_program_transactions` dedups on
   exact `subAwardReportId` only (the same filing emitted twice across pulled files); Report IDs
   are **100% unique** in all three committed CSVs (6,020 / 8,443 / 5,192, 0 blank). Semantic
   duplicates are flagged, never removed (270 rows / $59.8M / 0.50% of gross). Report counts are
   complete; if anything marginally generous, never undercounted.

**Reframe:** the only honest atom is the **dated subaward report**. "Modification" was dropped
(it overclaims); the metric is the stream of dated reported actions per `(UEI × PIID)`, and the
**first→last action-date span** is the PoP proxy — explicitly a reporting-based lower bound, not
contractual PoP. A `subAwardNumber`-based class taxonomy (Single / Separate-subawards / Repeat-
lineage / Mixed) was designed, found uninformative against the data, and **discarded per user
direction** ("don't even include classes until we see the data").

---

## Sheet 1 — **Subaward Activity** (summary group, live)

Slots **after Parent Concentration, before Market Bridge**. One row per `(UEI × PIID)`
relationship — **2,485 rows** (DDG 895 / Virginia 1,055 / Columbia 535). Columns:

`Program · Prime PIID · UEI · Vendor · Reports · Distinct Subaward Numbers · Correction Actions ·
First Action · Last Action · Activity Span (Years) · Net Subaward $M (FY2026$)`

- **Live** (all of it except one column): `Reports`/`Correction Actions` = `COUNTIFS`;
  `First/Last Action` = `MAX(_xlfn.MINIFS(...))` / `MAX(_xlfn.MAXIFS(...))` (non-matching program
  returns 0, the real date serial wins); `Activity Span` = `(Last−First)/365.25`; `Net $M` =
  `SUMIFS` over the tx `Subaward $ FY2026$` column `/1e6`. Each is **3-way additive** across the
  three transaction leaves (PIIDs are program-disjoint, so two of the three contribute 0).
- **Materialized** (one column only): `Distinct Subaward Numbers` — distinct-count has no clean/
  performant live-Excel form at this row count. Built by `scripts/build_subaward_activity.py`
  (reads the committed tx CSVs only — no corpus dependency).
- **Verified gold-standard:** LibreOffice headless recalc, then diffed every cell vs a Python
  replica of the formula semantics — **0 mismatches across all 6 live columns × 2,485 rows**;
  `Σ Net $M = 13,883.99` = the program-vendor FY2026$ headline **to the cent**.

### The payoff — span IS the metric (clean, monotonic, no guessing)

| Span | % of relationships | % of $ | median $/rel | mean reports |
|---|--:|--:|--:|--:|
| single date | 37% | 5% | $0.07M | 1.3 |
| <1 yr | 15% | 9% | $0.27M | 3.8 |
| 1–3 yr | 22% | 15% | $0.59M | 7.3 |
| 3–5 yr | 10% | 8% | $0.94M | 9.6 |
| **5+ yr** | **16%** | **64%** | **$3.78M** | **26.5** |

Duration tracks dollars and intensity almost perfectly: the 16% spanning 5+ years hold 64% of
the money and average ~27 reports. The natural tier cutpoints (single-date / <1 / 1–3 / 3–5 / 5+)
fall out of the distribution — span tiers are the obvious next analytical layer **if** wanted.
Corrections (≥1 negative action) touch 13% of relationships. Longest engagements are the
sustained DDG core suppliers (Warren Pumps 12.1y, Dover Energy 11.3y, …).

---

## Sheet 2 — **Prime Awards** (data group, materialized) — Phase 2 prime-PoP pull

Slots in the **data** group, just before the three transaction sheets. One row per in-scope
prime PIID (**12 today**). Pulled by `scripts/pull_prime_awards.py` from **USAspending award
detail** (`GET /api/v2/awards/{Prime Contract Key}/`, **no API key, no search step** — the key is
the USAspending `generated_unique_award_id` already carried on the tx rows). Raw full records
saved to `research_pulls/prime_awards_raw/<piid>.json` (project "keep full native records" rule).

Columns: `Program · Prime PIID · Prime Entity Name · Award Description · Date Signed · PoP Start ·
PoP Current End · PoP Potential End · Total Obligated $M (nominal) · Base + All Options $M
(nominal) · USAspending Subaward Count · USAspending Subaward $M`.

**Why pull:** the prime fields embedded on the subaward rows are per-report **snapshots** — the
same prime shows a different `Base Award Date Signed` row-to-row (C2100: embedded 2022 vs
USAspending `date_signed`/PoP-start **2017-02-14**), and one DDG prime carried 65 distinct TCVs.
Authoritative prime PoP + obligations must come from a direct pull.

Pull result (all 12, `start ≤ end` asserted): PoP windows 2011 → 2036, obligations $0.70B → $34.66B.
Two cross-checks the `USAspending Subaward …` columns expose:
- **Matches our scoped pull where there is no MIB:** C2100 = 5,681 subs / $4,176M = our cached
  `published_total_$` exactly.
- **Diverges where USAspending includes unscoped intermediaries:** Columbia C2117 = 5,208 / $7,749M
  vs our scoped Columbia ~$3.5B nominal — the gap is BlueForge ($4.2B) + other MIB we filter.
  (So those two columns are an unscoped coverage cross-check, NOT our scoped figures.)

Prime $ are **nominal cumulative obligations** (not deflated — a different basis from the FY2026$
subaward columns) and the PoP **includes option years** (end dates run to 2034–2036). Both
captioned on the sheet. Pure materialized reference — no live formulas.

---

## Build / verify

```
python3 scripts/build_subaward_activity.py     # (UEI x PIID) spine, 2485 rows, from committed CSVs
python3 scripts/pull_prime_awards.py           # 12 USAspending award-detail GETs (no key)
python3 build_workbook.py                       # 5 data guards run, then packages
python3 validate_workbook.py                    # 22 sheets, 0 xml errors, 0 error-literal cells
python3 tools/style_audit.py                    # 0 hard failures, 0 warnings
```

Subaward Activity additionally verified by a LibreOffice headless recalc + per-cell Python diff
(0 mismatches; reconciles to the headline). This machine has **`python3`**, not `python`.

## Files

- **New scripts:** `scripts/build_subaward_activity.py`, `scripts/pull_prime_awards.py`.
- **New sheet modules:** `sheets/subaward_activity.py`, `sheets/prime_awards.py`.
- **New extracted:** `extracted/subaward_activity.csv`, `extracted/prime_awards.csv`;
  `research_pulls/prime_awards_raw/<12 piids>.json`.
- **Modified:** `sheets/_tabs.py` (+`TAB_SUBAWARD_ACTIVITY`, +`TAB_PRIME_AWARDS` + assert),
  `sheets/__init__.py` (imports + `SHEETS` for both sheets); regenerated
  `award_classification_refactor.xlsx`.

## Carry-forward

- **Nothing committed** — both new SAM sheets are staged in the working tree only.
- **Classes deliberately omitted** (user: see the data first). The span distribution shows clean
  natural tiers — adding span-tier classification is the obvious next analytical step.
- **The prime-PoP "§1 band" on the activity sheet was scoped, then explicitly dropped** this
  session (user chose the standalone Prime Awards data sheet only). If revisited: a literal band
  atop Subaward Activity would require converting it to a custom renderer (losing the native
  sortable table), so the better path is Prime Awards adjacent in the summary group + per-row
  context columns on Subaward Activity via `INDEX/MATCH` on Prime Awards by PIID.
- **`Distinct action dates`** not added (reports ≈ 1.3× distinct dates — minor batch-refiling
  inflation; noted, not material).
- **Numbers:** Subaward Activity is Excel-computed (verified via LO recalc this session); Prime
  Awards is a static pull (re-run `pull_prime_awards.py` to refresh; reporting lags primes 6–18 mo).
- **Neither new sheet depends on the (still-finicky) corpus pipeline** — Subaward Activity reads
  the committed tx CSVs; Prime Awards reads USAspending. Re-run order if regenerating:
  `build_subaward_activity.py` + `pull_prime_awards.py` → `build_workbook.py`.
- **Do NOT re-run HII forensics** (exhausted/triple-sourced, per prior logs) — unrelated here.
