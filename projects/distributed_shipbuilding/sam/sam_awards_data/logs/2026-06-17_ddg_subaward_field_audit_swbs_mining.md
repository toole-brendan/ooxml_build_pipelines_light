# 2026-06-17 — DDG subaward field audit, stop-work investigation, Ingalls SWBS component mining

Scope: methodology Q&A on `deck_primary` + `workbook_award_analysis`; a new
deck reference slide; a deep empirical audit of the raw SAM/FFATA subaward data
(what fields exist, are descriptions usable, did we capture everything, can
stop-work orders be surfaced); and a new extraction that mines HII-Ingalls DDG
`subawardDescription` work-item codes → SWBS → work-type. Heavy emphasis on
**verifying claims against live data and the raw corpus** rather than asserting.

---

## 1. Deck — "Data Reference" slide (deck_primary)

Built a plain, fill-free methodology backup slide: three stacked native tables
(`table_skin="rule"`, no cell fills) — in-scope PIIDs grouped by platform
(SSN/SSBN/DDG), the 7 work-type buckets + NAICS-4 + definitions, and a sample of
**native** FSRS subaward fields.

- **First attempt was the wrong target:** built it as a *workbook sheet*
  (`workbook_award_analysis/.../sheets/data_reference.py`, group `sources`, last
  in registry). User clarified they wanted a *deck slide*. **Reverted** the
  workbook (deleted the module, undid both `sheets/__init__.py` edits, rebuilt →
  back to 27 sheets).
- Final: `deck_primary/deck_primary/slides/data_reference.py`, registered last →
  **slide 14**. Deck builds green (14 slides, 6 charts). Fit check: tables bottom
  at 5.90in vs BODY_B 6.42in — fits with 0.52in slack. Uses `house_table` +
  `estimate_row_heights` (size 800, min_row_h 152_400) + `sources_line` footnote.
- Side note captured: PIID platform abbreviations — Virginia→**SSN**,
  Columbia→**SSBN**, DDG-51→**DDG**; "in-scope PIIDs" = shipbuilder-directed
  new-construction prime contracts (15 sub + 24 DDG; GFE primes/BlueForge excluded).

## 2. Methodology clarifications (no code change)

- **Concentration headroom:** the Concentration screen uses **top-1 share only**
  (no HHI / top-N / Gini anywhere). Small-% vendors in a concentrated lane enter
  only as (a) the SUMIFS **denominator** (so they dilute top-1, and can drop a
  lane below the 0.75 cutoff) and (b) the **Active-vendors** COUNTIFS. They are
  never itemized on that tab; per-vendor $ lives in the Lane Vendors / Lane
  Vendor FY leaves. The "emerging second source" case is the **Source
  Diversification** tab (prior single → recent multi, incumbent active).
- **OEM / component-feeder limitation:** a "lane" is a coarse NAICS-4 bucket, so
  co-lane vendors aren't guaranteed substitutes. FFATA is first-tier only, so
  true sub-tier feeders are invisible; the real risk is non-substitute first-tier
  vendors in one bucket. No tiering/substitute logic exists. The only finer lever
  is the capability tag (~⅔ coverage, currently secondary).

## 3. Subaward NAICS provenance

SAM does **not assign** a NAICS to a UEI — the entity **self-certifies** a list
(with one designated primary) in its SAM registration. The corpus' `naics4` is
the subawardee **entity** NAICS (per UEI), not a per-subaward classification
(proven: different vendors under one PIID carry different NAICS, so it's not the
prime's single NAICS). Hence "classify on the vendor, not the award text," with
registry-first resolution and 3364/3344 removed as a corporate-NAICS artifact.

## 4. Stop-work order investigation — TWO self-corrections

Question: can stop-work orders (SWOs) be surfaced? Verified empirically.

- **Correction #1 (prime stream):** I first claimed they "can't reliably be
  surfaced." **Wrong.** FPDS/USAspending modification descriptions carry them:
  scanned 1,912 mods across 5 shipbuilding primes — no structured stop-work code
  (the `action_type` taxonomy has none; SWOs file as **OTHER ADMINISTRATIVE
  ACTION**, often **$0**), but the free-text `description` clearly does, e.g.
  `EXTENSION OF STOP WORK ORDER (SWO) 073 …`. Change orders themselves are scope
  changes, NOT SWOs.
- **Correction #2 (subaward feed):** I then claimed the subaward pipeline "cannot
  surface stop-works." **Also wrong for the raw pull.** Grepped the full raw
  corpus: SWO text **is** present — but only in `descriptionOfRequirement` (the
  **prime-context** field that rides on every subaward), for 2 DDG PIIDs:
  - `N0002413C2307` ×48 — "EXTENSION OF SWO FOR SONAR DOME PRESSURE RELIEF VALVE"
  - `N0002418C2307` ×15 — "ISSUE STOP WORK ORDER (SWO) … DDG 128-139 … STEERING SYSTEM"
  **Zero** in the per-subaward `subawardDescription`. So it's a **prime-level**
  signal stamped onto unrelated subawards (bleed-air-coolers, stern-tube-seals) —
  not a per-subaward stop signal — and the work-type pipeline discards that field.
  (Also caught a false-positive trap: "GRI**SWO**LD INDUSTRIES" matches a naive
  "SWO" substring — needs token-aware matching.)

Net: prime FPDS/USAspending = yes via keyword scan; subaward = only the
prime-context field, prime-scope, currently discarded.

## 5. `subawardDescription` re-audit — quality is BIMODAL by program

Re-audited 22,499 deduped in-scope subawards (dedup on `subAwardReportId`):

- **Submarines (16,119):** genuinely bad — 100% filled but **53% explicit filler**
  ("See Below", "SEE COMPLETE DESCRIPTION", "See remarks"), only **11% informative**,
  median 11 chars. The "complete description" it points to is **not transmitted**.
- **DDG (6,380):** actually usable — **0% filler-pattern, 48% informative**,
  median 23 chars; format `<NNNNN-NN code> <COMPONENT>` (e.g. "01021-01
  STRUCTURAL DOORS", "01043-02 DECK COVERING"). The methodology's blanket
  "descriptions are junk" is a *submarine* truth over-generalized.
- **0.0%** of descriptions echo `descriptionOfRequirement` verbatim → they're
  genuinely sub-level, not the prime's text.
- Enumerated **every** field present: the only descriptive strings are
  `subawardDescription` and the prime's `descriptionOfRequirement`. `subAwardNumber`
  is coded PO/line numbers (not prose); no hidden narrative field. For subs the
  real content genuinely isn't in the pull → vendor identity is the only signal
  (vindicates classify-on-vendor for subs; under-uses DDG).

## 6. "Did we pull all available fields?" — verified YES

- The pull script (`pull_sam_subawards_fullhistory.py`) saves the API response
  **verbatim** (`records.extend(page_data)` → `"published": pub`), and pulls
  `status=Deleted` separately. No field dropped.
- **Live probe (4 read-only calls, key from `.env`):** unfiltered call returned
  `totalRecords: 2,713,376` (endpoint alive); a live record's leaf-path set
  **exactly matches our saved 28-field schema** — diff = none. So **no** POP,
  **no** longer description, **no** subawardee NAICS/PSC/period exists in the
  endpoint. We captured 100%.
- **Operational finding (refresh caveat):** filtering `piid=...` now returns
  **0 records** (HTTP 200, valid key, filter echoed in `nextPageLink`) even
  though the endpoint holds 2.7M nationally and these PIIDs have thousands on
  USAspending. So **by-PIID SAM retrieval no longer returns our PIIDs** — a future
  corpus refresh can't just re-run the old pull; it'd come back empty. Data still
  on USAspending (thinner ~6-field schema).

## 7. NEW: Ingalls DDG component / SWBS extraction

`subawardDescription` is already in the raw corpus (no new pull needed; SAM
by-PIID is empty anyway). Built `ddg/research/scripts/extract_ingalls_components.py`
to mine it.

- **Anchored-regex bug fixed:** original `^\s*(\d{5}-\d{2})` only matched the code
  at the *start*, missing hull-prefixed lines (`DDG 146 03013-01 …`). Switched to
  `\b(\d{5}-\d{2})\b` searched **anywhere** → recovered **533 rows / $877M**,
  lifting HII work-item-code coverage **64.5% → 90.2% of $**.
- Coverage (HII-Ingalls, 5,900 subawards, $3,407M): work-item code **90.2% of $**;
  ≥1 free-text component word 34%; **GD-BIW 0%**, submarines junk → one-builder,
  one-program enrichment.
- Code dictionary: **365 distinct codes**; **top-50 = 73.6% of $, top-100 =
  82.6%** → small curated dictionary captures most value. Codes recur across hulls.
- Family→component is coherent (01xxx structural, 02xxx HVAC, 03xxx propulsion,
  04xxx electrical, 07xxx piping, 09xxx coatings).
- Outputs: `ingalls_subaward_components.csv` (per-subaward), `ingalls_vendor_capabilities.csv`
  (per-vendor), `ingalls_code_dictionary.csv` (per-code).

## 8. SWBS lookup via the ESWBS registry

User pointed to a saved SWBS registry → found `ESWBS_potential_codes.xls`
(`projects/mro/research/award_based/docs/`; Sheet1: `eswbs`, `eswbs_nomenclature`,
`eswbs.Remarks`; ~1,960 codes, 9 SWBS groups). Reads via pandas.

- The `CSE PS ###` token's 3-digit number = an **SWBS group**; resolves cleanly
  to Navy nomenclature (234 PROPULSION GAS TURBINES, 516 REFRIGERATION SYSTEM,
  310 ELECTRIC POWER GENERATION, 324 SWITCHGEAR & PANELS, 241 REDUCTION GEARS,
  561 STEERING, 512 VENTILATION, 541 FUEL, 532 COOLING WATER…).
- **Key disambiguation:** HII tags with its **own work-item code** (90.2% of $),
  NOT SWBS directly. SWBS is a **cross-reference** on the purchase-spec, present
  on **57.8% of $** explicitly; propagating SWBS via the code→SWBS dictionary
  lifts it to **69.9% of $** (113 codes auto-learned). Free-text component word
  = 34.2% of $. So "90%+" applies to the *work-item code*, not SWBS.
- SWBS→bucket crosswalk basis: 1xx→structural, 2xx→machining/propulsion,
  3xx→electrical, **5xx splits** (51x→HVAC; 53x–59x→piping), 6xx→coatings/structural,
  4xx/7xx→outside supplier pool.

---

## Files created / modified this session

- **Created:** `deck_primary/deck_primary/slides/data_reference.py` (slide 14)
- **Modified:** `deck_primary/deck_primary/slides/__init__.py` (registered slide 14)
- **Created+deleted (reverted):** `workbook_award_analysis/.../sheets/data_reference.py`
  + its two `sheets/__init__.py` edits — was the wrong target; workbook back to 27 tabs
- **Created:** `ddg/research/scripts/extract_ingalls_components.py`
- **Created (outputs):** `ddg/research/ingalls_subaward_components.csv`,
  `ingalls_vendor_capabilities.csv`, `ingalls_code_dictionary.csv`
- **Rebuilt:** deck (14 slides) and workbook (27 sheets) — both green

## Open items / next steps

1. Build the curated **`code → SWBS → work-type bucket`** dictionary (seed from the
   113 auto-learned SWBS codes + the top uncovered high-$ codes; wire in the ESWBS
   registry). Closeable from ~70% → ~83–90% of HII $ with ~50–100 curated codes.
2. **Cross-check** code-derived work-type vs each vendor's NAICS bucket → surface
   disagreements (misclassification / substitute-vs-complement signal).
3. Clean `component_text` admin-token noise (`VSR`, `ESO`, `OSI`, `MOD`).
4. Decide whether to wire the DDG capability tag into `workbook_award_analysis`
   (DDG/Ingalls-only, with coverage caveat).
5. Corpus-refresh caveat: SAM by-PIID pull now returns empty — pivot to USAspending
   or investigate the filter/endpoint change before any refresh.
