# 2026-06-25 — Outyear growth: compound phase-in (raw 30%, BIW carve-out kept)

Reconfigured the FY2028-31 outyear **high-case** BC-coefficient growth on the three
program TAM tabs. Was: a single throughput-normalized **+13.0%** intensity step
(`(1.30)/(1.15)−1`), taken once and held **flat** across all four outyears. Now: the
**raw +30%** HII outsourcing-hours growth, **compound-ramped** across the outyears to its
full effect at FY2031, with the DDG-51 BIW carve-out retained. Three explicit user calls
drove it — **ramp** (not a one-time step), **no throughput discount** (use the full 30%),
**keep the BIW carve-out** (only HII's 55% of DDG BC responds). Low case (status-quo
coefficient, flat) unchanged. A deliberate **value change** to the high band, not a refactor.

## Why
The prior treatment took the explosive FY2026 +30% y/y hours target, divided out a +15%
throughput assumption to a +13% intensity step, and applied it once. The user wanted the
opposite emphasis: keep the full 30% (the throughput normalization read as
double-discounting), spread it over the ~4-5 outyears rather than a one-time bump, and
keep BIW (Bath Iron Works) held flat since it isn't pursuing outsourcing.

On the ramp **shape** — compound-phase-in vs. linear-phase-in vs. sustained-30%/yr — the
cardinal IB rule settled it: **never compound a peak rate.** Sustained 30%/yr compounds
the coefficient to ~2.9× by FY31 (subs nearly tripling outsourcing intensity), a hockey
stick that contradicts the observed deceleration off 2025. Both phase-ins cap the
cumulative uplift at the observed +30% magnitude. Picked **compound phase-in** (constant
~6.8%/yr CAGR to the +30% endpoint) over linear for its back-loaded conservatism (lower in
the early outyears) and clean constant-rate story; the two sit <1 pt apart and are
identical at FY31.

## The mechanic
For the i-th of N outyears (N = 4; FY2028→i=1 … FY2031→i=4), the HII-responsive portion of
the BC coefficient grows by **(1+g)^(i/N)**, so FY2031 = (1+g)^1 = the full uplift.
g = raw hours growth = **30%** (no throughput division).

- **Subs (Virginia, Columbia)** — whole coefficient ramps:
  `coeff_high[i] = coeff_low × (1+g)^(i/N)`
- **DDG-51 (BIW carve-out)** — only HII's w = 55% share responds, BIW (45%) held flat:
  `coeff_high[i] = coeff_low × (1 + w·((1+g)^(i/N) − 1))`

In Excel each outyear column is `=$C$<coeff_low>*POWER(1+$C$<g>,i/N)` (subs) or the
`1+$C$<w>*(POWER(...)−1)` blend (DDG). The single flat `coeff_high` scalar is gone,
replaced by a per-outyear **"Outyear BC coefficient, high (compounded)"** row in the §3
grid; `Outsourced BC, high` now multiplies `oy_bc` by the same-column ramped coefficient.
`Outsourced BC, low` still multiplies by the flat `$C$<coeff_low>`.

Resulting coefficient ramp (recalc, ×status-quo):

| ×status-quo | FY28 | FY29 | FY30 | FY31 |
|--|--|--|--|--|
| Virginia / Columbia (full 30%) | 1.0678 | 1.1402 | 1.2175 | **1.3000** |
| DDG-51 (BIW carve-out → 16.5%) | 1.0373 | 1.0771 | 1.1196 | **1.1650** |

## Assumptions §4 restructure
Was four rows (hours 30% · throughput 15% · computed intensity 13% · HII share 55%); now
two input knobs — **HII outsourcing-hours growth (annual) = 30%** and **DDG-51 HII share
of BC = 55%**. The throughput row and the computed-intensity row are deleted; the model
reads the hours-growth cell directly (hours-growth = applied intensity-growth, no wedge).
Section retitled "§4 - Outyear outsourcing growth". Accessor
**`outlook_g_intensity_cell` → `outlook_growth_cell`** (now points at the hours cell),
updated in `_program_tam`, `checks`, and the assumptions export. Cell notes rewritten —
the +30% note now states the compound-ramp-to-FY2031 treatment and the no-throughput basis.

## Impact on the band (the intended value change)
Low band (status-quo coeff, flat) unchanged. The high band now fans out instead of sitting
~parallel to low:

| Total high $M | FY28 | FY29 | FY30 | FY31 |
|--|--|--|--|--|
| Prior (flat +13.0% subs / +7.2% DDG) | ~4,921 | ~4,831 | ~4,858 | ~4,931 |
| Now (compound ramp) | 4,663 | 4,870 | 5,203 | **5,610** |

FY2028 high drops ~260 (ramp starts at only +6.8% subs / +3.7% DDG), FY2031 high rises
~680 (reaches the full +30% / +16.5%). Low band for reference: 4,383 / 4,303 / 4,344 / 4,409.
(Prior-config high is reconstructed from the flat throughput-normalized uplift × the
unchanged low band; ties to the FY28 4922 / FY31 4931 recorded in the structural-refactor log.)

## Verification
`validate_workbook.py` → **RESULT: PASS** (full soffice headless recalc, OOXMLRecalcMode=0).
- **0** XML errors, **0** error-literal cells, **0** recalc formula-error cells — the new
  `POWER(...)` formulas evaluate clean (base 1.30 > 0, fractional exponent safe; no
  `#NUM!`/`#VALUE!`).
- All **12 firm-year tie-out anchors unchanged** — the edits touch only the FY28-31 high
  case, which no anchor covers; the 6 Exec FY-total cross-checks and 8 band
  Total=Σprograms checks tie.
- Direct recalc inspection (`scratchpad/inspect_ramp.py`): per-program high/low coefficient
  ratios match the closed form to 5 dp (subs → 1.30000 at FY31; DDG → 1.16500); high > low
  at every outyear.
- In-workbook **master check = "OK"** (0 FAILs; the completeness knob-count check still
  finds 6 numeric knobs via the renamed accessor). Stale-term scan across all live label
  cells: **0** surviving "throughput" / "intensity" labels.

## Files touched
`assumptions.py` (§4 knobs + accessor rename + notes), `_program_tam.py` (the ramp; §3
outyear block — `coeff_high` scalar → per-outyear ramped row), `executive_summary.py`
(band narrative; live cells flow through unchanged), `checks.py` (accessor name). Output
filename unchanged.

## Open / not done
- **Structural ceiling cap not added.** Offered a `MIN(coeff_high, ceiling)` guard; left
  out as non-binding — the highest terminal coefficient is Virginia at **44.2%**, far from
  any structural ceiling. Worth adding only as a guardrail against future knob edits (e.g.
  someone bumps 30%→80%); the ceiling would be a new Assumptions knob.
- **Throughput (15%) fully removed**, not parked as a memo cell; trivial to restore as a
  commented/greyed note if the number should stay visible for context.
- The ramp denominator **N = len(OY) = 4**, so full effect lands at **FY2031** (the last
  FYDP outyear). If the intent is "full by FY2032" or a 5-year runway anchored at FY2027,
  the exponent denominator is the single knob to change.
- Decks / any downstream consumers of the outyear band unchanged (out of scope).
