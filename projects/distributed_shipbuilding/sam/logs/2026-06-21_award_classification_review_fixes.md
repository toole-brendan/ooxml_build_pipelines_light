# 2026-06-21 — Award-Classification workbook: independent-review fixes (7 findings)

Session goal: implement an independent reviewer's verdict on the `award_classification_refactor`
workbook (`projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/`).
The reviewer judged the refactor architecturally sound but **not sign-off-ready**: prime-contract
scope was uncontrolled, report-ID dedup was insufficient, a blank-override bug produced numeric-0
codes, the Market Bridge blended units, taxonomy notes contradicted assigned codes, and
concentration was UEI-only. All 7 findings implemented + 5 build-stopping guards added. Build is
clean (**20 sheets, 0 XML errors, 0 error-literal cells**); every regeneration reconciles to the cent.

## Headline re-baseline (intentional)

Per four user decisions (AskUserQuestion), out-of-scope primes are **REMOVED** (not quarantined),
re-baselining the headline down:

| | Nominal | FY2026$ |
|---|---:|---:|
| Before | $13,504.98M | $15,508.22M |
| **After** | **$12,075.06M** | **$13,883.99M** |
| Δ | −$1,429.92M | −$1,624.22M |

Per-program FY2026$ now: DDG $4,028.22M / Virginia $6,027.51M / Columbia $3,828.26M.

## Scope decisions (the four material calls)

1. **Mechanism = REMOVE** (drop rows + re-baseline), not quarantine.
2. **Virginia `N00024-20-C-2120`** ("Lead Yard Support & Design", ~$1.018B nom / 670 rows / 151
   UEIs — the largest Virginia prime) → out of scope. It was a 2026-06-21 addition; surfaced its
   true magnitude (the prior log framed it as a $14.37M HII slice) before the call was made.
3. **All 4 flagged DDG primes** out: `N00024-14-C-4313` (LCS), `N00024-19-C-2322` (DDG-1000),
   `N00024-19-C-4452` (planning-yard/PIO), `N00024-12-C-2312` (Flight III design).
4. **Market Bridge = full formula-driven.**

After review, the user extended (3) to apply the Basic-Construction rule **consistently**: also
remove Columbia "Design Drawings" (`N00024-13-C-2128`, $273.5M) and the zero-row DDG/sub
design·LYS·ship-alteration·concept primes. **12 primes excluded total** (−$1.43B nominal:
DDG −$138.4M, VA −$1,018.0M, Col −$273.5M dollar-bearing; the rest zero-row).

---

## Finding 1 (blocker) — prime-contract scope manifest + REMOVE + assertion

- **New `prime_contract_scope.csv`** (34 queried primes; generator `scripts/build_prime_scope_manifest.py`):
  piid, program, class, builder_group, scope_type, include(Y/N), rationale, source. 12 `include=N`.
- **Exclusion chokepoint** = `corpus/scripts/_corpus.py::load_scope()` (defensive manifest read,
  drops `include=N`). Both `build_program_transactions.load_scope` and `iter_records` (→ vendors +
  supplier_master) consult it, so all three CSVs stay aligned and the build's $-reconciliation holds.
- **`_integrity.assert_piids_in_manifest()`** (wired into `lib.build()`): every tx PIID ∈ manifest
  as include=Y; no include=N leaked; zero-subaward queried primes reported (10 accounted, not silent).

## Finding 2 (blocker) — semantic-duplicate audit (report both, never delete)

- `build_program_transactions.py`: detect rows identical on all fields **except** Subaward Report
  ID/Number. Emits `duplicate_candidates.csv` (adjudication log) + `duplicate_audit.csv` (per-program
  gross / candidate / net). Post-exclusion: **270 candidates / $59.83M nom / 0.50% of gross**.
- New **Duplicate-Report Audit** sheet renders the summary; `_integrity.assert_duplicate_audit_recorded()`
  asserts the log accounts for every candidate and warns if candidate $ > 2% of gross.
- Reviewer's guidance honoured: candidates flagged, not removed; gross stays the headline.

## Finding 3 (high) — blank Primary-Output override → numeric 0

- `_flat.override_or_map` / `override_or_map_basis` made **axis-specific**: use the override only
  when that axis's override cell is non-blank (`INDEX(...)<>""`), else NAICS map, else D0/P0;
  `supplier_master.py` passes the axis range into the basis. The 4 D-set/P-blank rows (Scot Forge,
  Goodrich ×2, D.W. Clark) now resolve P via the map/P0 (verified in the rendered formula), so the
  Primary-Output matrices total 100%.
- New `_integrity.assert_archetype_codes_valid()`: every override + NAICS-map D∈{D0..D11}/P∈{P0..P6}
  or blank → every *resolved* code valid by construction.

## Finding 4 (high) — Market Bridge → illustrative, formula-driven, live overlap

Rewrote `market_bridge.py`: renamed "Illustrative cumulative outsourcing / co-build scenario";
per-program **observed nominal** + FY2026$ memo; co-build gross **Low = disclosed input**, **Base/High
= Low × editable scale multiple** (blue cells G/H, e.g. VA 10200 × 1.47 / 2.16); a **live** "−less
FFATA-visible HII-NNS overlap" = `SUMIFS` over the Virginia tx sheet keyed on the HII-NNS UEIs
(`WMXDDH6HJNA5`, `CR39JL3216G7` ≈ $98.4M, post-exclusion); bridge math harmonised to **nominal**;
deleted the false "net of HII <$100M" caveat.

## Finding 5 (high) — NAICS rationale vs assigned-D drift (40 rows)

- `scripts/align_naics_rationales.py` (idempotent): rewrote only the terminal `-> Dxx` token of the
  40 rationales to the assigned (authoritative) code, body preserved (38 → D11 services, 335312 → D3,
  333611 → D2). `_integrity.assert_naics_rationale_aligned()` fails the build on future drift.

## Finding 6 (medium) — parent-collapsed concentration + positive-dollar Top-1

- `domain_concentration.py`: Top-1 **share** denominator changed net → **positive** spend (consistent
  with HHI). New **Parent Concentration** sheet (UEI vs ultimate-parent Top-1 % / HHI / eff-firms),
  built by `scripts/build_parent_concentration.py` (replicates resolution + deflation + parent map;
  **validated against the reviewer's Columbia D2 exactly**: UEI 55.5%/0.384 → parent 60.4%/0.438).

## Finding 7 (medium) — wording / caption / label drift

- **Data-derived captions** via new `_cuts.cy_span` / `cy_span_union` (6 program-vendor + transaction
  sheets + Exec Summary intro — can't drift on refilter).
- "Foreign %" → **"Foreign-maj. UEIs %"** + clarifying note (it is an entity-count ratio, not $ share).
- Exec Summary §3/§4 mix labelled **FY2022-FY2025 window** (pre-FY22 + partial FY26 excluded).
- HII narrative reconciled: "~$90M / <$100M" + removed-prime reference → **~$98M**, tied to the live
  Market Bridge overlap (`hii_co_build.py`, `executive_summary.py`).
- Methodology `scope_status` rewritten from the unbuilt "quarantine-and-report" to the implemented
  **manifest REMOVE** behaviour (`guide_methodology.py` §7 + glossary).

---

## Build / verify

```
python3 scripts/build_program_transactions.py            # tx CSVs + dup audit (exclusions applied)
python3 scripts/tag_ddg_transactions_swbs.py
python3 scripts/build_program_vendors.py {ddg,virginia,columbia}
python3 scripts/build_supplier_master.py
python3 scripts/build_swbs_crosswalk.py ; python3 scripts/build_ddg_swbs_rollup.py
python3 scripts/build_parent_concentration.py
python3 build_workbook.py        # 5 guards run first, then packages
python3 validate_workbook.py     # 20 sheets, 0 XML errors, 0 error-literal cells
```

Tie-outs confirmed: reconcile Δ = 0 every program; 0 excluded-PIID rows in any CSV; universe guard
green (tx == program-vendor == Supplier Master); manifest + dedup + code-validity + NAICS-lint guards
pass. Note: this machine has **`python3`**, not `python`.

## Files

- **New:** `prime_contract_scope.csv`; `scripts/build_prime_scope_manifest.py`,
  `scripts/align_naics_rationales.py`, `scripts/build_parent_concentration.py`;
  `sheets/duplicate_audit.py`, `sheets/parent_concentration.py`;
  `extracted/duplicate_candidates.csv`, `extracted/duplicate_audit.csv`, `extracted/parent_concentration.csv`.
- **Modified:** `corpus/scripts/_corpus.py`, `lib.py`, `sheets/_integrity.py` (+4 guards), `_flat.py`,
  `_cuts.py`, `_tabs.py`, `sheets/__init__.py`, `supplier_master.py`, `domain_concentration.py`,
  `market_bridge.py`, `executive_summary.py`, `hii_co_build.py`, `guide_methodology.py`,
  `naics6_archetype_map.csv`, the 3 `*_program_vendors.py`, the 3 `*_subaward_transactions.py`,
  `scripts/build_program_transactions.py`; the regenerated tx / vendor / supplier_master CSVs and
  `award_classification_refactor.xlsx`.

## Carry-forward

- **Nothing committed** — staged in the working tree only; commit when ready.
- **Not verified headless:** opening in Excel to watch cells evaluate. All formula *structures* were
  verified in the rendered xlsx (Market Bridge bands/overlap, axis-specific override P, deflation);
  parent-concentration was validated against the reviewer's exact Columbia D2 figures. Force a recalc
  in Excel/LibreOffice and re-confirm the headline ($12.08B nom / $13.88B FY2026$) + 100% PO matrices.
- **Market Bridge** Low/Base/High and scale multiples are **editable blue inputs** — order-of-magnitude,
  basis-labelled; refine as better HII disclosures land (the estimate + live HII-overlap update live).
- **Consistency note for the reviewer:** the Basic-Construction exclusion rule was applied uniformly
  (design / lead-yard-support / ship-alteration / planning-yard / other-class). The manifest documents
  every queried prime with rationale; flipping any include flag + rebuilding re-scopes in one edit.
