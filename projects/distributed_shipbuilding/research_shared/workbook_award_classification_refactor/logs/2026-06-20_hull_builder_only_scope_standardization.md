# 2026-06-20 - Hull-builder-only scope standardization (DDG vs submarines)

Session that standardized the program scope across the three program-vendor sheets to
**hull-builder-only (Basic Construction prime only)**, so the DDG / Virginia / Columbia
archetype distributions are comparable. Build stays green throughout (12 sheets, 10 native
tables, 6 note parts, 0 XML errors, 0 error-literal cells, no repair).

Supersedes nothing in the prior handoff
(`2026-06-20_naics_crosswalk_sheet_and_override_first_archetype_wiring.md`); that doc's §8
(Phase 4 - 2026 dollars) is still OPEN and was explicitly NOT done this session (the user is
reconsidering whether constant-FY2026 dollars are needed at all).

---

## §1 - The problem (why the cross-program comparison was broken)

The three program-vendor sheets were built from `_corpus.iter_records`, but the two programs
were scoped to **different cost-funnel denominators** (per the submarine research wiki
`distributed_shipbuilding/submarines/research/wiki/01-scope-and-funnel-framework.md`,
"Four denominators of outsourced"):

- **DDG** = denominator #1 ("outsourced from the shipbuilder") = the hull-construction primes
  ONLY. The DDG fullhistory pull contains subaward JSONs for just GD-BIW (17 PIIDs) +
  HII-Ingalls (7); the Navy GFE/combat-system primes catalogued in the scope JSON
  (GE-Propulsion, LM-Aegis, BAE-Guns/VLS, Raytheon, NG, GD-MissionSys, DRS) were never pulled,
  and `_corpus.PROGRAMS["ddg"]["groups"]={"GD-BIW","HII-Ingalls"}` re-enforces it.
- **Submarines** = denominator #2 ("outsourced from the Navy/SCN perspective") = Basic
  Construction (GDEB) **plus the four GFE primes** the wiki names as in-scope: BPMI (naval
  reactor), LM (combat systems), BAE (ordnance/deck modules), RR (propulsion).
  `_corpus.PROGRAMS["submarines"]["groups"]=None` keeps them all.

Net: GFE/nuclear was IN for submarines and OUT for DDG - the opposite of an early hypothesis,
and the reason e.g. Columbia D2 (propulsion) and P2 (finished parts) read high (the BPMI
naval-reactor supply chain was inflating them).

`role`/`bucket` are NOT raw fields - they are a derived overlay (169-row hand registry +
mechanical `classify(name,naics4)` fallback, the registry itself largely NAICS/SAM-based with
0 source URLs), so we did NOT use them as the scope lever. The reliable lever is the raw
**prime group** (`bgroup`, from `nc_scope_summary.json` scope meta).

## §2 - The fix (hull-builder-only = Basic-Construction-only = denominator #1)

Keep only the hull-construction prime's subawards:

| Program  | Kept (hull builder)          | Dropped (GFE primes, separate SCN lines) |
|----------|------------------------------|------------------------------------------|
| DDG      | GD-BIW + HII-Ingalls         | - (already BC-only; no change)           |
| Virginia | GDEB                         | RR, BAE                                  |
| Columbia | GDEB                         | **BPMI** (naval reactor), + LM/BAE/RR    |

Implemented as a `bgroup == "GDEB"` filter for submarines (DDG already restricted upstream).
**Scoped to THIS workbook's build scripts, NOT to shared `_corpus`** - `_corpus.iter_records`
still yields the full $13.1B incl. GFE primes (the deck / competability analysis depends on
it); only the classification-refactor pipeline applies the hull-builder cut.

## §3 - Files changed

- `scripts/build_program_transactions.py` - `raw_records()` skips non-GDEB scope groups for
  subs; the iter_records reconciliation sum (the Δ assert) got the same `bgroup=="GDEB"` filter
  so it still reconciles to the cent.
- `scripts/build_program_vendors.py` - the `recs` comprehension adds `and r["bgroup"]=="GDEB"`
  for subs (with a comment block explaining the scope + the HII-NNS caveat).
- `scripts/build_uei_dimensions.py` - same `recs` filter (the UEI Index feeds program-vendor
  column C = the NAICS-6 that drives D/P resolution, so it MUST match the vendor scope).
- `sheets/{ddg,virginia,columbia}_program_vendors.py` - intro captions now state the scope;
  the two submarine captions add the HII-NNS gap note.
- `scripts/build_archetype_overrides.py` - unchanged; it filters overrides to UEIs present on
  each program sheet, so it auto-followed (293 -> 287 override rows).

## §4 - Impact

Reconciliation clean (Δ = 0 on transactions; +4e-6 rounding on the vendor roll-ups).

| Program  | nominal $ before | after      | Δ                       | UEIs       |
|----------|------------------|------------|-------------------------|------------|
| DDG      | $3,604.2M        | $3,604.2M  | unchanged               | 470 (=)    |
| Virginia | $5,118.7M        | $5,112.2M  | -$6.5M (RR/BAE)         | 645 -> 633 |
| Columbia | $4,444.8M        | $3,770.5M  | **-$674.3M (BPMI)**     | 595 -> 582 |

Workbook total ~$13.17B -> ~$12.49B. All impact is Columbia losing the BPMI naval-reactor
supply chain (BWXT $272M, B&W $49M, Curtiss-Wright $110M, Taylor Forge, Hamill, ...).

**Columbia D/P shift** ($674M came mostly out of P2 -$366M and P3 -$276M; D2 17.4%->13.3%,
D7 4.8%->2.4%). P4/P5/P1 unchanged in absolute $, so their shares ROSE - Columbia now reads
correctly as more module/integrated-system heavy once the GFE reactor chain is out.

**The propulsion asymmetry is NOT a filter artifact:** even standardized, DDG D2 stays 29.4%
(Rolls-Royce propulsors $460M, GE turbines $333M, Timken gears $169M - genuine shipbuilder
subawards) vs Virginia 7.1% / Columbia 13.3%. Real make-vs-buy difference.

## §5 - Known residual: the HII-NNS gap (NOT fixable from this data)

HII Newport News builds ~50% of Virginia / ~22% of Columbia construction, but that team-build
workshare flows through GDEB as vendor of record and is essentially unreported in FSRS (~$98M
visible on Virginia over 2016-2021, **$0 on Columbia**; wiki ch11). It is overwhelmingly hull
modules + structural fabrication -> **D1 / P5**, so submarine D1 (hull) and P5 (outfitted
structures/modules) are understated vs DDG. Noted in the two submarine sheet captions.

## §6 - How to rebuild

From `projects/research_shared/workbook_award_classification_refactor/`:

```
python3 scripts/build_program_transactions.py            # 3 tx CSVs (reconcile Δ=0)
python3 scripts/build_uei_dimensions.py                  # UEI Index + Parents
python3 scripts/build_program_vendors.py ddg|virginia|columbia
python3 scripts/build_archetype_overrides.py             # -> 287 override rows
python3 build_workbook.py && python3 validate_workbook.py
```

D/P are live formulas - cached values refresh only when the user opens/saves in Excel. To see
the resolved D/P split without Excel, `/tmp/recut_dp.py <extracted-dir>` replicates
`override_then_map` (validated to reproduce the pre-change cached values exactly).

## §7 - OPEN / next

- Archetype MECE pass (the user's "I didn't make these categories MECE enough") - in progress
  next.
- §8 of the prior handoff (constant-FY2026 dollars) still open / on hold.
