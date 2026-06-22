# 2026-06-21 — Submarine EB-denominator completion + "where to play" concentration layer

Session goal: address the `DOMAIN_SHARE_CONCENTRATION_CAVEAT.md` issues before doing "where to
play" analysis. Two problems were in play: (A) domain shares are concentrated (a *feature* for
where-to-play, not a bug), and (B) HII-Newport News co-build is structurally absent from the
submarine subaward denominator. Decision: fix the **submarine data** first (complete the EB-reported
denominator + re-test HII), then build the where-to-play + honesty workbook layer (A–G).

Net result: **16 → 18 sheets**; Virginia denominator completed (+$1.0B, +36 vendors); a live
**Domain Concentration** ("where to play") sheet; an **HII Co-Build Workshare** memo; a tightened
Executive Summary reframe. Workbook builds green (0 error cells, validator clean).

---

## Load-bearing discovery: the SAM subaward API `piid` casing FLIPPED

`SAM_GOV_HOWTO.md` (2026-05) said the subaward `piid` filter must be **lowercase**. As of
**2026-06-21 it is the opposite** — case-sensitive, wants **UPPERCASE no-dash**:

| sent | result |
|---|--:|
| `piid=N0002417C2100` (UPPER, no dash) | **5687** records ✅ |
| `piid=n0002417c2100` (lower) | **0** — filter echoed in `nextPageLink`, matches nothing, **silently** |
| dashed (`N00024-17-C-2100`) | **HTTP 400** |

The trap: lowercase returns a clean `200` with `totalRecords: 0`, so it *looks* like "no subs"
rather than "mis-cased filter." Caught it via the master sanity-check. **Always re-test in uppercase
before declaring a reporting gap real.** `SAM_GOV_HOWTO.md` updated (⚠ box at top + TL;DR + param
table + code pattern + history). `pull_eb_missing_subawards.py` uses `.upper()`.

---

## Generator repair (was "broken", actually just a moved path)

`corpus/scripts/_corpus.py` `PROGRAMS` pointed at `tam/submarines/` and `tam/ddg/`; the `tam/`
restructure (`c8fdc925`) renamed those to `tam/virginia_columbia_research/` and `tam/ddg_research/`.
Repointed all three paths each (fullhistory / scope_json / naics_csv). `build_program_transactions.py`
now runs and reproduces the committed CSVs byte-for-byte (Δ=0). This un-blocks the documented
"complete the EB denominator" path.

---

## Scope decision — added ONE prime, documented four exclusions

`in_scope_piids` was a curated 15 (9 GDEB-construction kept; 6 GFE/reactor primes present-but-filtered
by the generator's `prime=='GDEB'` cut). Discovery (FPDS NAICS-narrowed + USAspending authoritative
EB-recipient enumeration of 1,073 Navy awards) surfaced missed EB primes. Verified each by **DoD
announcement language + place-of-performance** (PSC is a useless `1905` catch-all — even the excluded
planning-yard and Hartford EOH are `1905`; only reactor breaks out as `4470`):

| PIID | what | decision |
|---|---|---|
| **N00024-20-C-2120** Lead Yard Support | "...design efforts related to **Virginia-class**"; PoP Groton 91% / **NNS 8%** | **ADDED** (Virginia new construction) — 670 subs / $1,018M |
| N00024-14-C-2104 Submarine Planning Yard | "...support for **active** nuclear submarines"; PoP fleet bases | excluded (sustainment) |
| N00024-20-C-2114 Naval Reactors | PSC 4470 | excluded (reactor/GFE) |
| N00024-21-C-2103 FY21 Conform | "R&D concept formulation, current+future platforms" | excluded (generic R&D, immaterial $19M) |
| N00024-19-C-2125 Planning Yard/backfit | already `out_of_scope` ("upgrades to existing boats") | stays excluded |

All four exclusions recorded in `out_of_scope_piids` with reasons. The driving distinction:
**Lead/Design Yard = new construction (in); Planning Yard = in-service sustainment (out).**

---

## HII re-test (the point of completing the set)

Scanned the completed EB prime set for HII UEI `WMXDDH6HJNA5`: **11 records / $14.65M**, incl. exactly
the **$14.37M / 7 recs on C2120** the caveat doc had named. This **confirms** the doc's forensics
(part of HII's documented ~$75–90M Virginia FFATA footprint) and does **not** overturn "structurally
absent" — the true co-build workshare is still tens of billions and FFATA-invisible. The denominator
was simply missing this slice; now it isn't. "Data forensics exhausted" stands (do not re-run UEI /
deleted-record / USAspending variants).

---

## Data-layer impact (reconciles to the cent)

`build_program_transactions.py virginia columbia` → `build_program_vendors.py virginia`:
- Virginia: **8,443 → 9,113** tx, **$5,112M → $6,130M** nominal, **633 → 669** vendors (Δ=0 both stages).
- Columbia / DDG unchanged. DDG tagged-tx CSV untouched (no SWBS re-tag needed).
- Biggest C2120 vendors: Northrop Grumman $402M, Oceaneering $276M — they shift/concentrate the
  Virginia domain mix (see below), which is the honest where-to-play signal, not a side effect to hide.

---

## New workbook layer (A–G), all over the corrected data

- **B — `Domain Concentration` sheet (model, live).** The "where to play" engine. Per (program ×
  capability domain): Domain $M, Share, Suppliers, **Top-1 firm + share** (INDEX/MATCH on `_xlfn.MAXIFS`),
  **HHI** (`SUMPRODUCT(--(D=code),$M^2)/total^2`), **Eff. # firms** (=1/HHI), and a live **Contestability**
  label (Fortress = Top-1≥60% or HHI≥0.40; Concentrated = effN≤3; else Contestable). 297 formulas over
  the program-vendor sheets' `$AB`(D)/`$I`($M)/`$G`(name) columns. Column mapping + math verified; a
  Python replica matched the caveat doc to the dollar (Virginia D2 $2,280M / NG 73% / Fortress;
  Columbia D6 $922M / NG 57%; Virginia D4 contestable effN 10).
- **A — Executive Summary reframe.** §1 HII caveat tightened to "unexplained reporting/data-treatment
  gap, not a clean carve-out," now cites the recovered C2120 $14.37M and points to the HII Co-Build
  sheet; added a concentration caveat pointing to Domain Concentration (read size WITH contestability).
- **C/D/F/G — `HII Co-Build Workshare` sheet (guide, static memo).** §1 two-tier framing
  (subcontractable *bidding* game vs co-build *teaming* game); §2 what FFATA captures for HII now
  (<$100M incl. recovered $14.37M); §3 issuer-disclosed subcontract ledger (D), amount-basis-typed
  (Block V ≈ **$10.2B** cumulative 2023-05-24 as the strongest public Virginia figure; itemized Columbia
  mods; **DO NOT SUM** caption); §4 CRS cross-check (C) — Va ~50% / Block-V ~25% NN PoP, Col ~22–23% /
  12.7% PoP → tens of billions; §5 SEC 10-K bound (F) — NNS segment ~$6.0B/yr, submarine not separately
  split; §6 sources (G) — CRS RL32418/R41129, DoD announcements, SEC, FAR 52.204-10.

Build: `python3 build_workbook.py` → 18 sheets, 13 native tables, validator clean (0 xml errors,
0 error-literal cells; Domain Concentration 297 formulas / 0 error cells).

---

## Files

**Changed (data/scope):** `corpus/scripts/_corpus.py` (PROGRAMS paths), `tam/virginia_columbia_research/
extracted/nc_scope_summary.json` (+C2120 in scope; +4 documented exclusions), regenerated
`extracted/virginia_subaward_transactions.csv` + `virginia_program_vendors.csv`.
**New pull/discovery scripts** (`tam/virginia_columbia_research/research/scripts/`):
`discover_eb_primes_fpds.py`, `pull_eb_missing_subawards.py` (uppercase-piid, HII re-test).
**New raw pulls:** `sam_subawards_fullhistory/N0002420C2120_subawards.json` (+ C2104/C2114/C2103,
pulled but not scoped). **Doc:** `SAM_GOV_HOWTO.md` (casing reversal).
**New sheet modules:** `sheets/domain_concentration.py`, `sheets/hii_co_build.py`.
**Changed sheet modules:** `sheets/executive_summary.py` (reframe), `sheets/_tabs.py`,
`sheets/__init__.py`.

---

## Carry-forward

- **Numbers are Excel-computed** (Domain Concentration is live formulas). Structure + math verified
  against the caveat doc via a Python replica; eyeball once in Excel — esp. the DDG block (its D
  resolution uses program label `"DDG"`, which a throwaway replica got wrong as `"DDG-51"`; the
  workbook reads the resolved program-vendor column, so it is correct).
- **C2120 changes the published Virginia figures** — the caveat doc's pre-2026-06-21 Virginia numbers
  (D2 = 40.2% $2,053M) are now D2 = 37% $2,280M (NG 73%); update any external quote.
- **Domain Concentration is the where-to-play substrate.** Next analytical step (the original ask):
  pick target domains from the Contestable quadrant (Virginia D4/D7/D9; Columbia D4/D7/D9; DDG D3/D4)
  vs Fortress incumbency. The HII co-build tier is a separate *teaming* game, not bid-able from here.
- **SWBS sheets unaffected** (DDG-only; submarine scope change does not touch them).
- **Do NOT re-run HII subaward forensics** (exhausted); the recoverable HII signal is issuer
  disclosures (the Co-Build sheet) + NAVSEA FOIA / PIEE-EDA (out of band).
