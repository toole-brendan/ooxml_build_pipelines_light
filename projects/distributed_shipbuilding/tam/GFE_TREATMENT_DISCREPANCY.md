# OPEN ISSUE — GFE treatment is inconsistent between submarines and DDG

**Status:** parked / known issue. Documented 2026-06-20 for later resolution — **not fixed**.
**Scope:** affects the per-program TAM bases, the GFE figures, the ceiling layer,
and any cross-program (portfolio) GFE rollup in the master TAM workbook.

---

## TL;DR

The two programs define **GFE (government-furnished equipment)** differently, so the
"GFE" line — and therefore the Basic Construction (BC) base that TAM is built on — is
**not computed on a like-for-like basis** across programs:

| Program | What `GFE` captures | Source column |
|---|---|---|
| **Submarines** (Virginia, Columbia) | **Propulsion (BPMI nuclear reactor plant) + Electronics + Ordnance** | `gfe_sum_$M` |
| **DDG-51** | **Electronics + Ordnance only** — **propulsion (LM2500) is NOT in GFE** | `gfe_elec_ord_$M` |

The DDG funnel-build script itself flags its GFE as **"a LOWER BOUND on GFE"** because
the LM2500 propulsion GFE is "folded into HM&E, not broken out." Submarines, by
contrast, put their propulsion plant squarely in GFE.

So: **submarines count propulsion as GFE; DDG does not.** When the master workbook
places the three programs side by side (and the Portfolio Summary / ceiling layer treat
them as one portfolio), the GFE scope silently differs by program.

---

## Evidence

### Submarine GFE = Propulsion + Electronics + Ordnance
`virginia_columbia_research/research/scripts/build_cost_funnel.py`:
- line ~25: `Propulsion  ← GFE (BPMI nuclear plant)`
- line ~33: `The 'gfe_sum_$M' column groups Propulsion + Electronics + Ordnance`
- line ~252: `gfe_parts = [x for x in (pr, el, ord_) if x is not None]; gfe_sum = sum(gfe_parts)`

Consumed by `master/workbook_master_tam/sheets/submarines/data_scn_budget.py`
(`§Na - GFE components`: Propulsion Equipment / Electronics / Ordnance / GFE Sum).

### DDG GFE = Electronics + Ordnance ONLY (lower bound; LM2500 excluded)
`ddg_research/research/scripts/build_cost_funnel.py`:
- line ~13: `HM&E  ... (CFE; LM2500 propulsion sits here)`
- lines ~27-29: `NO separate Propulsion line for DDG in the P-5c (unlike submarines);
  LM2500 GFE is folded into HM&E, not broken out. GFE here = Electronics + Ordnance
  only -- a LOWER BOUND on GFE. (HM&E sits in the "other non-BC" bucket, not GFE.)`
- line ~231: `gfe = (el or 0) + (ordn or 0)`

Consumed by `master/workbook_master_tam/sheets/ddg/data_scn_budget.py`
(`GFE Sum (Electronics + Ordnance)`).

### Magnitude (FY2022-27 cumulative, from `master/extracted/ceiling/wb_cost_base.csv`)

| Program | BC $M | GFE $M | Total Ship $M | BC % | GFE % |
|---|--:|--:|--:|--:|--:|
| Virginia | 36,277 | 9,755 | 51,871 | 69.9% | 18.8% |
| Columbia | 20,370 | 7,108 | 31,919 | 63.8% | 22.3% |
| DDG-51 | 17,471 | 10,290 | 29,937 | 58.4% | **34.4%** (lower bound) |

DDG's GFE% is already the highest **even though it excludes propulsion** — adding the
LM2500 would push it higher still. The submarine GFE%/BC% already net out propulsion;
DDG's do not, so the columns are not directly comparable.

---

## Where the inconsistency propagates

1. **GFE figures & GFE%** on each SCN Budget tab — different scopes per program.
2. **Ceiling layer** (`Cost Base`, `Ceiling Model`, `Headroom`): `wb_cost_base.csv`
   carries `gfe_$M` per program sourced from the two different columns
   (`build_ceiling_base.py` reads `gfe_col="gfe_sum_$M"` for subs vs
   `gfe_col="gfe_elec_ord_$M"` for DDG). Any GFE-derived ceiling/headroom comparison
   inherits the asymmetry.
3. **Penetration denominators** (Outlook): both use Total Ship Estimate, which is
   internally consistent, but the BC numerator's GFE-free-ness differs in scope.
4. **Portfolio Summary / any portfolio GFE rollup**: summing sub GFE (with propulsion)
   and DDG GFE (without) mixes definitions.

## Does it move the TAM number?

Partly — and the direction needs a domain call:
- Both programs' **BC bases exclude their propulsion** (subs: reactor → GFE; DDG:
  LM2500 → HM&E / "other non-BC"), so the TAM = BC × coefficient base is *roughly*
  GFE-free for both.
- **But the classification differs in a way that may understate DDG TAM:** the sub
  reactor is genuinely non-addressable (government nuclear, BPMI), so excluding it is
  correct. The DDG **LM2500 is contractor-furnished (CFE) — the yard buys it from
  GE/Rolls-Royce — i.e., it is supplier-addressable**, yet it is currently parked in
  "other non-BC" and excluded from the DDG TAM. If LM2500 belongs in the supplier-
  addressable base, **DDG TAM is understated**; if it belongs in GFE, **DDG GFE% is
  understated**. Either way it is mis-bucketed relative to how subs handle propulsion.

## The question to resolve (later)

Pick ONE consistent cross-program rule for propulsion and apply it to both books:
- **Option A — GFE = government-furnished only.** Sub reactor = GFE (non-addressable).
  DDG LM2500 = CFE → **supplier-addressable, belongs in BC/TAM** (not GFE). This would
  *raise* DDG TAM and make GFE mean the same thing (gov-furnished) everywhere.
- **Option B — GFE = "not yard-addressable propulsion + combat systems."** Then DDG
  must add LM2500 to its GFE (raising DDG GFE%, matching the sub treatment), and the
  DDG funnel's "lower bound" caveat goes away.
- **Option C — document the asymmetry as intentional** (sub propulsion is nuclear-GFE;
  DDG propulsion is CFE) and clearly label the two GFE columns as different scopes so
  no one sums or compares them naively.

## Where a fix would land

- Source of truth: the two `research/scripts/build_cost_funnel.py` scripts (the GFE
  column definitions) in `virginia_columbia_research/` and `ddg_research/`.
- Then regenerate the cost-funnel CSVs → refresh `master/extracted/{submarines,ddg}/`
  snapshots → rerun `master/build_ceiling_base.py` → rebuild the master workbook.
- Touch points to re-verify: `data_scn_budget.py` (both), `model_tam_build.py` BC base
  (both), `build_ceiling_base.py`, and the Portfolio Summary / ceiling tabs.

## Cross-refs
- Master workbook + restructure: `tam/logs/2026-06-20_master_tam_consolidation.md`
- Cost-funnel builders: `*/research/scripts/build_cost_funnel.py`
- Ceiling base builder: `master/build_ceiling_base.py`
