# 2026-06-10 — Work-type bucket shares: yard/GDEB gate, FY22-25 window, per-class + per-FY vectors (both workbooks)

## Problem / findings (user asked: is the work-type categorization wrong?)

Both SAM Builds applied ONE pooled bucket-share vector (all FFATA records, all
years, all primes) to every FY's TAM. Three problems found, one of them a genuine
scope error:

1. **DDG scope error — 58.5% of the share evidence came from GFE/combat-system
   prime chains** (LM-Aegis, Raytheon SPY-6, BAE guns/VLS, DRS, GE, NG): subawards
   under those PIIDs voted in the bucket shares although the TAM removes the GFE
   stream before the BC base. Major Tool & Machine alone (~$947M under LM/Raytheon,
   VLS canister + radar-structure machining) carried the "machining ~39%" headline.
   Yard-prime evidence looks very different (machining 34%, electrical 11%, HVAC
   15%, unbucketed 20% vs 43% under GFE chains).
2. **Window contamination** — 48% of the DDG pooled corpus was FY2002-FY2021
   records, outside the FY22-27 TAM window (subs: ~23% outside).
3. **Subs class weighting** — Columbia was ~50% of the corpus but only ~35% of TAM,
   over-weighting its electrical-heavy / coatings-light mix; the class mixes
   genuinely differ (window: electrical Va 31.8% vs Col 45.4%, coatings 6.8% vs
   1.4%, structural 20.6% vs 15.9%).

Annualization context: per-FY shares are computable FY22-25 only (FFATA reporting
lags 6-12 months; subs FY26 = one $0.3M record, DDG FY26 partial with a negative
HVAC cell; FY27 structurally empty). FY26-27 must ride an assumed vector.

## Method (user approved all four)

1. **Gate** share evidence to yard construction PIIDs — DDG: GD-BIW + HII-Ingalls
   groups; subs: GDEB primes (drops BPMI reactor/IBI 2.8%, LM/BAE/RR slivers).
2. **Window** to FY2022-FY2025 subaward action years (complete reporting years;
   partial FY26 excluded). In-window gated cells are all >= 0 (the negative-cell
   problem lives outside the gate+window; an import-time assert guards regressions).
3. **Per class (subs)**: Virginia and Columbia vectors measured separately
   (nc_scope_summary.json maps every in-scope PIID to a class) and applied to each
   class's own annual TAM (`tam_cell(li, fy)`, OBBBA rides Virginia) — companion to
   the same-day class-vintage coefficients.
4. **Per FY**: FY22-25 allocate at their own year's vector; FY26-27 use the FY22-25
   window vector. Bucket TAM = Σ_fy annual TAM(fy) x share(fy, b); SUMPRODUCT
   algebra keeps scenario SAM = Σ_fy TAM(fy) x factor(fy) exactly, so annual broad
   sums to cumulative by construction.

**Show-the-work design (user pushback on v1 hardcoding):** the gate lives in the
Entity Master TABLE as per-entity dollar columns — DDG: `Yard $M` + `Yard FY22..25`;
subs: `GDEB $M` + `Va FY22..25` + `Col FY22..25` — same provenance level as the
existing `$M` column (Python aggregation of nc_records_long.csv). Everything on the
new "Worktype by FY" sheet is then a live SUMPRODUCT over the table, the
reconciliation (gated + excluded = supplier total) is live arithmetic, and the gate
is visible per vendor (Major Tool & Machine: $947M lifetime, $0 yard-window).

## Changes

### Both workbooks (mirrored)
- `data_entity_master.py` — extracted **`classified_records()`** (the single
  registry-first classification pass, now shared); added the gate columns to the
  table (DDG 11->16 cols, subs 11->20); accessors `yard_dollar_range`/`yard_fy_range`
  (DDG), `gdeb_dollar_range`/`class_fy_range` (subs). Lifetime corpus totals
  unchanged (DDG $6,027.2M / subs $5,451.1M — refactor verified no-op).
- NEW `data_worktype_by_fy.py` -> **"Worktype by FY"** tab (data group, after
  Worktype Evidence): §1 evidence-basis fields; observed $ by bucket x FY grids
  (live SUMPRODUCTs; subs has Va + Col blocks); share grids (columns sum to 100%);
  modular tag (gated window, per class for subs); reconciliation to Entity Master
  with OK/FAIL tie. Import-time guard asserts no negative gated cell.
- `model_sam_build.py` — rewritten. Modeled shares = N(gated observed) + Inputs
  adjustment, per FY column (FY22..25 + "FY26-27 (window)"); allocation =
  Σ_fy TAM(fy) x share(fy); "Effective share" column = bucket TAM / portfolio (the
  honest blended share); annual SAM uses per-FY SUMPRODUCT factors; modular
  scenario = gated-window modular share (DDG: **0** — all DDG modular-flagged
  entities sit under GFE-chain primes; disclosed). All public accessor names
  preserved (chartdata/exec/figure-register/QA consumers untouched); subs adds
  class_bucket_tam_cell / class_tam_total_cell / va_/col_modeled_share_total_cell.
- `guide_methodology.py` — §1 "Worktype share gate" definition row; §2b SAM
  framework gate + per-FY lines; §3 flow row "Gate work-type share evidence ->
  Worktype by FY".
- FY column headers on all new/edited grids read "FY2022..FY2025" (user request).

### DDG-specific
- `model_sam_build.py` §2b keeps the full-corpus excluded-roles audit + a new
  "Supplier (addressable, full corpus)" row (addressable_total_cell keeps meaning);
  figure-register label "(full corpus)"; QA-04 label "(window vector)".

### Subs-specific
- `inputs_assumptions.py` §8 — now adjustment-only ("applied to both class share
  vectors"); the modeled-share producer machinery (observed/modeled cells, share
  range, totals) MOVED to SAM Build; accessors deleted, `bucket_adjustment_cell`
  now col C. Entity Master §4 relabeled "(full corpus reference)".
- `validation_qa_reconciliation.py` (unregistered) — QA-04 -> Virginia window
  vector, NEW QA-04b Columbia; import repointed to model_sam_build.
- Subs SAM Build §§ renumbered: §3 modeled shares (a Va / b Col / c excluded
  roles), §4 allocation (a Va / b Col / c combined), §5 scenarios, §6 selected,
  §7 annual, §8 checks (per-class share-sum checks across all FY columns).
- Spec files NOT updated (user: mostly stale anyway) except the new DDG
  data_worktype_by_fy.md written before that call.

## Numbers (recalc-verified via headless soffice + openpyxl; constant FY2026 $M, OBBBA on)

Portfolio TAMs unchanged (allocation-only change): DDG 6,421.7 / subs 18,133.8;
bucketed totals tie exactly; annual broad sums to cumulative exactly; share columns
all sum to 100%; both books 0 error cells, 0 FAIL/REVIEW anywhere; Worktype by FY
grids match the offline gated matrices to the cent; reconciliation ties OK.

| DDG bucket | Before (pooled 33.6%-residual vector) | After | Eff. share |
|---|---|---|---|
| Machining | 2,524 (39.3%) | **2,260.8** | 35.2% |
| HVAC | 397 (6.2%) | **984.2** | 15.3% |
| Electrical | 375 (5.8%) | **687.8** | 10.7% |
| Piping | 343 (5.3%) | **603.9** | 9.4% |
| Structural | 351 (5.5%) | **371.5** | 5.8% |
| Castings | 111 (1.7%) | **146.6** | 2.3% |
| Coatings | 165 (2.6%) | **9.7** | 0.2% |
| Unbucketed residual | 2,160 (33.6%) | **1,357.3** | **21.1%** |
| Broad SAM | 4,262 | **5,064.4** | 78.9% |
| Modular scenario | ~ none flagged in-gate | **0.0** | — |

| Subs bucket (combined Va+Col) | Before (pooled) | After | Eff. share |
|---|---|---|---|
| Electrical | 6,746 (37.2%) | **5,594.9** | 30.9% |
| Piping | 3,464 (19.1%) | **3,711.6** | 20.5% |
| Structural | 3,065 (16.9%) | **3,616.2** | 19.9% |
| Coatings | 961 (5.3%) | **963.0** | 5.3% |
| Castings | 780 (4.3%) | **785.8** | 4.3% |
| Machining | 598 (3.3%) | **708.3** | 3.9% |
| HVAC | 308 (1.7%) | **191.5** | 1.1% |
| Unbucketed residual | 2,212 (12.2%) | **2,562.5** | **14.1%** |
| Broad SAM | 15,921 | **15,571.3** | 85.9% |

Gated evidence bases: DDG $1,597.9M (of $6,027.2M corpus; GFE-chain $3,526.3M +
out-of-window yard $903.0M excluded); subs Va $1,771.1M + Col $2,413.1M (non-GDEB
$159.0M + out-of-window GDEB $1,107.9M excluded). Subs modular shares: Va 15.26% /
Col 9.41% (was one pooled entity-tag share).

Notable reversals vs the pooled story: DDG machining is still #1 but HVAC jumps to
#2 (the GFE chains had ~zero HVAC, diluting it); DDG coatings nearly vanishes (its
evidence was BAE/Raytheon-chain); DDG residual drops 33.6% -> 21.1% (the GFE-chain
records were 43% unbucketed). Subs residual RISES 12.2% -> 14.1% (TAM-weighting
leans Virginia, whose gated mix is residual-heavier); electrical falls ~$1.15B
(Columbia's electrical-heavy corpus no longer over-weighted).

## Now stale downstream (adds to the existing consolidated restate list)

- **Consolidated workbook/deck**: z_ChartData §8 (work-type combined) and §15
  (per-program stacked columns) + slides s03b/s12 hardcode the OLD per-program
  bucket values; s13 scenario chart (modular: DDG contribution is now 0); every
  "machining leads DDG ~39%"-flavored copy. These were ALREADY stale from the
  same-day DDG-coefficient + subs class-vintage restates — fold this into that
  single consolidated pass.
- Program z_ChartData tabs are live links and already reflect the new buckets.
- Wiki/spec prose describing the pooled work-type method (subs ch8-adjacent, DDG
  deck specs) — same sweep.

## Gotchas / notes for next time

- **The work-type gate lives in Entity Master columns** (`Yard*`/`GDEB`/`Va`/`Col`),
  computed during the entity aggregation from `classified_records()` +
  `nc_scope_summary.json`'s PIID->group/class map. Worktype by FY contains ONLY
  live formulas — change the gate by changing the columns, not the sheet.
- `classified_records()` is the single classification pass for BOTH the entity
  table and the gate columns — don't reintroduce a second CSV-reading pass.
- The subs Assumptions §8 no longer produces modeled shares; `bucket_adjustment_cell`
  moved D->C. The one adjustment knob per bucket applies to BOTH class vectors and
  every FY column (unbucketed absorbs per column).
- DDG modular scenario is honestly 0 under the gate (Advanced Industries + W
  International sit under BAE-Guns/VLS). If a yard-issued modular subaward appears
  in a future refresh it picks up automatically.
- FFATA reporting lag means the FY window should advance on refresh (FY26 becomes
  usable ~mid-FY27); the window is a single list constant `WT_FY_WINDOW` in each
  data_entity_master (worktype sheet + SAM Build column maps derive from it).
- BIW under-reports FFATA (~$178M vs Ingalls $2,323M lifetime) — the DDG gated mix
  is effectively Ingalls' mix; disclosed limitation, not fixable from this data.
- Effective blended residual (21.1% DDG) ≠ window pooled residual (19.3%) because
  allocation TAM-weights the FY vectors — FY22/23 are residual-heavier years.

---

# Same day, cleanup pass — SOM/haircut copy deleted; Assumptions citations -> native notes

Two user-requested cleanups of earlier (other-session) content:

1. **All SOM mentions deleted** from rendered text in BOTH workbooks: the §1
   definition rows ("share Saronic could realistically win") on each Methodology,
   the exec-summary "not SOM" note tails (DDG), and — extended by the user — every
   "no capture / win-probability haircut" disclaimer: the §2b prose lines, the
   "(no haircut)" tails on the SAM definition treatment and the DDG SAM Build §4a
   banner, and the SAM hover notes. The Sensitivity tab's "coefficient haircut"
   rows (85%/70% AP/LLTM cases) are a different, factual usage and stay. While
   editing the DDG SAM hover note, fixed two stale figures inside it: residual
   ~33.6% -> ~21.1%, and the TAM note's ~$573M/yr -> ~$1,070M/yr (BC ~$897M +
   AP/LLTM ~$174M) to match the day's restates.

2. **Assumptions gray S_NOTE citation cells -> native Excel notes** (the S_NOTE
   style remains in workbook_core for future use; these sheets no longer use it):
   - DDG: P-10 EOQ citation -> note at B{ap_eoq}; FY18-22 MYP bulletin citation ->
     note at B{biw18 row}; AP/LLTM coefficient classification rationale -> note at
     C{coeff} (the 1.00 input).
   - Subs: AP-base "Held at 0" rationale -> note at B{Va AP-base row}; Block V /
     Build I verbatim POP quotes + Block VI tripwire -> note at B{Va vintage row}.
   - Mechanics: texts moved verbatim into ExcelNote(...) lists; the Assumptions
     renders now return WorksheetSpec(ws, notes=...) (note parts 1 -> 2 per book).

Verification: rebuild + DDG validate (0/0), recalc both via soffice -> 0 error
cells, 0 FAIL/REVIEW; portfolio TAMs unchanged (6,421.7 / 18,133.8); grep of
rendered cells shows zero SOM/capture-haircut copy (only "HANSOME ENERGY" vendor
substring matches); citation text confirmed inside the comment parts at the right
anchors (DDG B26/B35/C42; subs B26/B55).
