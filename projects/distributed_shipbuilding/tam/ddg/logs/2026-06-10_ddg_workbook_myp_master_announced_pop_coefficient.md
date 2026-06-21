# 2026-06-10 — DDG workbook: MYP master POP restated to announced bulletin %, BC coefficient 12.5% → 25.3%

## Problem

User suspected the DDG workbook was not multiplying by the correct MYP-adjusted %
to find the outsourced (TAM) amount. Investigation confirmed it: the TAM math was
sound (BC base × the §3a non-GFE BC-corpus coefficient — the right *kind* of %),
but the two MYP master rows that carry 93.5% of that corpus's dollar weight were
held at **invented POP weights** (Inputs §4: BIW 86% Bath / 12% other-US / 2%
foreign; Ingalls 88% Pascagoula / 10% / 2% — i.e. only 14%/12% outside-yards) that
contradict the award bulletins' own announced POP. Only the masters' **dollars**
are source-selection redacted; their POP percentages were published:

- **BIW N00024-23-C-2305** (war.gov 3479250, 2023-08-01; re-confirmed by the
  2025 DDG 148 option mod, 4261297): Bath 69%; Cincinnati 4 / Walpole 4 / York 2 /
  South Portland 1 / Falls Church 1 (= 12% named); "other locations below 1%
  (collectively totaling **19%**)" → **31% outside the yard**.
- **Ingalls N00024-23-C-2307** (war.gov 3491276): Pascagoula 77% (79% Block II
  option); "other locations below 1 percent (collectively totaling **23%**)"
  → **23% outside the yard**.

The 86/88 weights had no documented basis anywhere (workbook, wiki, slide specs —
`appendix_myp_correction.md:347` acknowledges the conflict and just says "use the
reconstructed weights"). They appear back-solved to make the all-gated
outside-yards figure hit the §3e anchor target 0.33, which traces to wiki ch12's
"adjusted ~33%" table — itself arithmetically irreproducible (its 36% BIW-sites
share is impossible even at 100% Bath weighting) and a misreading of ch9 (whose
~33% is yard-side outsourcing as a share of *total ship cost*, a different
statistic; ch9's share of the BC layer is ~54%).

## Method decision (user-confirmed): mirror the submarines convention

Subs wiki ch7 + `workbook_submarines` corpus verified: **announcement-stated POP
percentages are used verbatim** (no reconstruction; "the percentages are stated
directly in the press releases"); stated below-1% aggregates ("all other locations
less than 1% (totaling X%)") **count as Other-US** (verified: the May 2026 $2.31B
Block VI action parses 0/2/98 where 98 = 63 named + 35 aggregate); only truly
percentage-less single-site rows are left unparsed (conservative floor). The subs
corpus has no master-row overrides — its masters' dollars AND POP are disclosed,
so the redaction workaround is DDG-specific.

Mirroring for DDG: masters keep trade-press/FPDS-reconstructed dollars
($6,400M / $8,180M) and take the announced POP — **BIW 69/0/31/0, Ingalls
0/77/23/0** (below-1% aggregates → other-US; named foreign = none → foreign 0;
South Portland stays other-US, matching the DDG parser's own bucketing of the
disclosed master rows). Block I 77% used for Ingalls (matches corpus row 495);
at the 79% Block II vintage the coefficient would be 24.2%.

## Changes (all in `projects/ddg/workbook/workbook_ddg/sheets/`)

- `inputs_assumptions.py` — §4 `_MYP` → (6400, 69, 0, 31, 0) / (8180, 0, 77, 23, 0)
  + provenance comment; banner → "($ reconstructed; POP % as announced)".
- `model_tam_build.py` — §3b comment ~33% → ~42% / "announced POP"; §3e banner
  "near ~42%"; anchor target 0.33 → **0.42**; §4a banner "($-redacted; announced
  POP)"; §4c guardrail line → "masters carry the bulletins' announced
  contract-level POP split".
- `guide_methodology.py` — §2c lead + figure table (~42% / 0.42 anchor / 25.3%
  applied) + the MYP-correction ExcelNote (12.5% → 25.3%, 32.8% → ~42%).
- `summary_executive_summary.py` — outside-yards KPI note "~42% (vs ~87%
  disclosed artifact)".
- `validation_qa_reconciliation.py` (unregistered; render-tested manually) —
  QA-01 label "near ~42%".
- `sources_references.py` — CITE-01 note: "$ only; POP as announced … 87% -> ~42%".
- `data_pop_corpus.py` — field-guide MYP-master row: "$ reconstructed; POP as
  announced".
- `validation_pop_source_audit.py` — Tier 2 text likewise.

No formula/engine changes — the coefficient SUMPRODUCTs, Sensitivity ladder, and
program z_ChartData are all live links and inherit.

## Numbers (recalc-verified via headless soffice + openpyxl, constant FY2026 $M, OBBBA on)

| Metric | Before | After |
|---|---|---|
| Applied BC supplier coefficient | 12.546% | **25.294%** |
| Outside-yards, MYP-corrected (all-gated) | 32.84% | **41.99%** (anchor 0.42, OK) |
| Outside-yards, disclosed-only (artifact) | 73.64% | 73.64% (unchanged) |
| BC-stream TAM | 2,703.6 | **5,450.4** |
| AP/LLTM-stream TAM | 1,247.7 | 1,247.7 (unchanged) |
| Portfolio TAM (FY22–27) | 3,951.3 | **6,698.1** |
| Average annual TAM $M/yr | 658.6 | 1,116.3 |
| Per-hull TAM (13 hulls) | 303.9 | 515.2 |
| SAM unbucketed residual | 1,328.9 (33.63%) | 2,252.7 (33.63%, share unchanged) |
| Penetration FY22–27 / FY26–27 | 10.80% / 20.10% | 18.30% / 28.28% |
| Implied outyear lo/hi $M/yr | 544.6 / 1,013.7 | 923.2 / 1,426.2 |
| FY22–25 avg TAM $M/yr | 491.5 | 976.2 |

Verification: build 26 sheets, validate 0 xml errors / 0 error-literal cells;
recalc 0 error cells; every OK/REVIEW/FAIL status cell across TAM Build / SAM
Build / Outlook / Sensitivity / POP Source Audit reads OK; SAM total = TAM
identity holds. A/B: OBBBA toggle off → portfolio TAM **5,840.3** =
(21,548.3 − 3,391.2) × 25.2937% + 1,247.7 exactly; coefficient toggle-invariant.

## Now stale downstream (NOT touched this session — pending decision)

1. **Consolidated workbook + deck** — z_ChartData §11–§15 and slides s03 (walk),
   s03b (work type), s11a (outlook) hardcode old DDG values (3.9513 walk endpoint,
   per-program buckets, penetration strips 6.0–28.9%, implied outyears, FY22–25
   avg 3.31 combined, "13%" supplier-share copy). Combined TAM/SAM headlines all
   move (~+$2.7B cum).
2. **DDG wiki ch12** — the "adjusted ~33%" table needs restating (~42%, and its
   BIW/Ingalls site shares recomputed); ch12's "consistent with ch9 self-perform
   ~33%" line misquotes ch9.
3. **DDG deck slide specs** — `appendix_myp_correction.md` + `myp_redaction.md`
   (86/88 weights, 32.8%, 12.5%, TAM $3.44B/$2.13B sensitivity) and draft module
   `slides_draft/appendix_myp_correction.py` ('Bath 86%, supplier 14%').
4. DDG program deck (if rebuilt) and any "13%" copy deck-wide.

## Gotchas / notes for next time

- **Only the masters' dollars are redacted — the POP % is published.** Any future
  "reconstruction" instinct on POP weights contradicts the bulletins.
- The announced below-1% aggregates are **disclosed totals, not unparsed** — count
  them as other-US (subs convention). Treating them as unparsed would yield a 5.4%
  coefficient; that is a parser-floor posture, not a source fact.
- The §3a basis comment "masters are ~93% of the BC corpus" still holds; the
  disclosed-only BC coefficient (7.78%) is still LOWER than corrected, so the
  "excluding them drops the coeff" note in §3a remains true.
- Keep the three readings straight (now): ~87% announcement headline artifact,
  73.6% live disclosed-only, **42.0% MYP-corrected all-gated**, **25.3% applied
  BC coefficient** (non-GFE BC corpus only). The 42% is still NOT the multiplier.
- The §3e anchor is a regression pin on the workbook's own corrected figure
  (subs pins its published 0.518 the same way); it was re-targeted 0.33 → 0.42
  with ±5pp tolerance.

---

# Same day, second pass — Exec header, S_NOTE style, AP/LLTM stream restated to the P-10 EOQ line

## 1. Exec Summary header
DDG "KPI | Value | Source" → "Metric | Value | Source" (mirrors subs).

## 2. NEW shared style `S_NOTE` (workbook_core/styles.py)
Gray-italic (#808080) side-note text style for source/citation annotations beside input
cells — font 9, cellXf 43. Added via the documented 3-step process; additive at list
end, so every existing style index is unchanged (MRO et al. unaffected). No inline
formatting exists in the engine, so a registered style was the only way.

## 3. AP/LLTM stream: 80% x 85% assumptions replaced by the P-10 line classification

User wanted a defensible source for the 85% AP supplier coefficient. None exists — the
project's own spec guardrails say "Inputs assumption (no DDG AP POP corpus)" — and the
DDG corpus structurally can't measure one (DDG AP awards are mods to the yards; the
largest AP-ish action parses 100% Bath). The defensible source was on disk all along:
**Exhibit P-10 (Advance Procurement Requirements Analysis), LI 2122**, in
`projects/research_shared/budget_books/SCN_Book_FY27.txt` (PB2027, Vol 1 p.243;
FY25 split also PB2026 p.235). It itemizes CY AP per FY:

- FY2026 $1,750.0M = **Ship Construction EOQ $1,000.0M** + congressional adds
  $450.0M shipyard infrastructure + $300.0M wage enhancements (yard capex/wages —
  the old 80% knob was silently sweeping these into supplier TAM).
- FY2025 $83.224M = **EOQ $41.5M** + NMT terminal GFE $41.724M.

New treatment (user-confirmed "no haircut is more defensible"): AP/LLTM base = the
P-10 Ship Construction EOQ line per FY (then-year, deflated to constant FY2026);
supplier coefficient = **1.00 by P-10 classification** ("Economic Order Quantity
procurements for material items" — vendor-purchased by definition). Conservatism
moved to Sensitivity §4 (85% / 70% haircut display rows).

Changes: `inputs_assumptions.py` §3 (gross row kept as P-1 reference; new blue
`_AP_EOQ` row {FY25 41.5, FY26 1000.0} with gray S_NOTE citation; constant-$ row
repointed to EOQ; `ap_gross_then_cell` accessor added; `ap_ship_construction_share_cell`
RETIRED + dv sqref adjusted), §5 (coefficient → 1.00, relabeled, gray classification
note), `model_tam_build.py` §2b (share term dropped from ap_in; labels), §5a label,
`data_ap_bridge.py` (docstring, §2 gross→EOQ→coeff derivation, §3 congressional-adds
EXCLUDE row, §4 caveat — the old "P-10 line-items don't parse cleanly" claim was
false), `validation_sensitivity.py` §4, `guide_methodology.py` AP note,
`sources_references.py` CITE-09, QA-13 label. Subs §3 AP-base rows also got a gray
S_NOTE (why base = 0; corpus-measured ~48.5% is reference-only).

## Numbers (recalc-verified)

| Metric | Before (this morning) | After |
|---|---|---|
| AP/LLTM base (constant FY26) | 1,834.9 gross x 0.80 | **1,042.33 (EOQ: 41.5x1.02 + 1,000.0)** |
| AP/LLTM supplier coefficient | 0.85 (unsourced) | **1.00 (P-10 classification)** |
| AP/LLTM-stream TAM | 1,247.72 | **1,042.33** |
| Portfolio TAM | 6,698.09 | **6,492.69** |

Deflator chain re-verified end-to-end after the repoint: constant EOQ FY25 =
41.5 x 1.02 exactly (2-dp Green Book Procurement factor), FY26 x 1.00; BC base
21,548.32 unchanged all day (SCN §1b constant rows untouched); master POP dollars sit
only in dimensionless SUMPRODUCT ratios (deflator-invariant by design). Build 26
sheets, validate 0/0, recalc 0 error cells, no REVIEW/FAIL anywhere, QA module
render-tested. Gray notes verified italic FF808080 (DDG Assumptions D40 + I26-area;
subs I26).

## Downstream stale (adds to the morning list)
Consolidated walk slide's AP/LLTM hatch math (1.8349 = 1.2477/0.68) and the
"AP/LLTM supplier factor 85%" row on appendix_supplier_share_pop_conversion; DDG deck
spec appendix_ap_lltm_sensitivity.md (80%/85%/$1.25B/$208M story) and
annual_tam_build.md coefficient notes; AP/LLTM $208M/yr mentions deck-wide → now
~$174M/yr.

---

# Same day, third pass — FY2022-vintage coefficient (FY18-22 masters) + basis-by-FY table

Manager asked which FYs use firm announced-POP % vs estimates. Two upgrades:

## 1. FY2022 now uses its own contracts' announced POP

The FY22 ships were funded under the FY18-22 MYP masters, absent from the corpus
(window starts Jul 2022). Pulled the primary bulletin via Wayback curl (HOWTO §2
route; defense.gov article 1647166, snapshot 20180928083950), saved verbatim to
`research_primary_sources/dod_announcement_pop/2018-09-27_dod-contracts_1647166.txt`:

- BIW N00024-18-C-2305: **$3,904,735,559** (announced, NOT redacted), 4 ships
  FY19-22, POP **Bath 61%** + 19% named cities + 20% below-1% aggregate = 39% outside.
- Ingalls N00024-18-C-2307: **$5,104,668,778**, 6 ships FY18-22, POP
  **Pascagoula 91%** + Erie 1% + 8% aggregate = 9% outside.

Dollar-weighted **FY2022-vintage BC coefficient = 22.0022%** — computed live in TAM
Build §3a from two new Inputs §4 rows (biw18/ingalls18, with gray S_NOTE citation);
§5a now applies FY22 -> 22.00%, FY23-27 -> 25.29% (corpus coefficient, relabeled
"applied FY23-27" in §1/§3a/§5b/Exec Summary). The 2018 masters stay OUT of the POP
corpus (predate the window; anchor 42% untouched). CITE-10 added.

## 2. Methodology §2e "Evidence basis by fiscal year"

New subsection after §2d: FY | Dollar basis | Outsourced % basis, for 2022 /
2023-2025 / 2026 / 2027 / 2028-2031, plus two caveat lines (announced POP =
contract-level planned distribution, not per-FY actuals; AP/LLTM = P-10
classification, not POP). Summary read: FY23-25 hard on both layers; FY26 hard $
+ firm % with the OBBBA BC/GFE split as the one assumption; FY27 firm % on request
$; FY22 own-vintage % (22.0%); FY28-31 labeled estimates.

## Numbers (recalc-verified, 0 errors, all checks OK)

| Metric | Before | After |
|---|---|---|
| FY2022 BC stream | 545.4 (at 25.29%) | **474.4** (2,156.0 x 22.0022%) |
| BC-stream TAM | 5,450.4 | **5,379.4** |
| Portfolio TAM | 6,492.7 | **6,421.7** |

Gotcha: the FY18-22 masters' dollars are NOT redacted (the redaction is specific to
the two-yard FY23-27 competitive structure's option values; the 2018 award amounts
were published) - so no reconstruction was needed for them at all.

Downstream stale list unchanged (consolidated deck/workbook, wiki ch12, DDG deck
specs) - all DDG-derived hardcodes now reflect a 6,421.7 portfolio TAM.

## Addendum: subs Methodology §2d "Evidence basis by fiscal year"

Mirrored the DDG §2e basis-by-FY table into the submarines workbook
(`guide_methodology.py` §2d, after the §2c penetration subsection). Subs-specific
content: one pooled 35.0% corpus coefficient for all FYs (no vintage split - the
Dec 2019 Block V construction master predates the corpus window, caveat row says
so); FY26 = enacted + OBBBA Sec. 20002(16) with the ~58.2% BC share as the one
assumption layer; FY27 = PB2027 request + spillover-0 default; FY28-31 = Outlook
estimate; AP/LLTM base-0 caveat. Rebuild + recalc: 0 error cells, no REVIEW/FAIL,
applied coefficient unchanged (35.02%) - display-only addition.

## Addendum 2: subs construction-master bulletin pull (vintage evidence; NOT applied)

Pulled the two pre-window construction masters via Wayback curl, saved verbatim to
subs `research_primary_sources/dod_announcement_pop/`:

- **Virginia Block V** (2019-12-02, article 2030017; $22,209,893,409 mod to
  N00024-17-C-2100, nine boats FY19-23): NNS 25 / Quonset 21 / Groton 20 /
  Sunnyvale 8 / named 3 / US-aggregate 22 / foreign 1 -> **34% outside-the-team**.
- **Columbia Build I** (2020-11-05, article 2406922; $9,473,511,245 mod to
  N00024-17-C-2117, SSBN 826 + 827): Groton 36 / NNS 25 / Quonset 17 /
  US-aggregate 22 -> **22% outside**.

Key finding while checking: the subs applied 35.02% BC coefficient rests on only
**8 disclosed actions, $526.0M** (largest: $188M va construction spares at 98%) —
the construction masters are absent (pre-window). Block V's own 34% happens to sit
right on the applied 35%; Columbia's 22% is 13pp below it. The Mar 2026 $15.38B
N00024-17-C-2117 mod is design/lead-yard/SIB (work_type lead_yard, gated no) — NOT
a Block VI construction master; Block VI construction is unawarded, so no FY24+
Virginia vintage POP exists yet.

Options quantified (per-class cum BC bases from the workbook: Va 37,402.2 /
Col 20,487.0 = 57,888 + OBBBA 2,677.5):
- B. DDG-style fold-in (masters into one pooled coeff): 30.49% on a $32.2B
  denominator -> portfolio TAM ~18,466 (-2.75B).
- C. Per-class vintage (Va 34%, Col 22%, OBBBA at Va 34%): TAM ~18,134 (-3.08B).
- A. Status quo: 35.02% on the $526M corpus, disclosed in Methodology §2d.

NOT applied — decision pending (cascades to every consolidated deliverable).
Tripwire for later: when the Block VI construction master is announced, its POP
becomes the FY24+ Virginia vintage evidence.

---

# Addendum 3: subs workbook moved to class-vintage coefficients (option C) — APPLIED

User decision: apply option C to submarines; DDG stays as-is (pooled corpus
coefficient + FY22 vintage split; the yard-level DDG variant was assessed at
~+$79M net and NOT built).

## What changed (`projects/submarines/workbook/workbook_submarines/sheets/`)

- `inputs_assumptions.py` — NEW **§5 "Construction-master announced POP
  (class-vintage BC coefficients)"** after §4 OBBBA (old §5-§7 renumbered §6-§8;
  no cross-file § references existed): Block V row (N00024-17-C-2100, $22,209.9M,
  EB 41 / HII 25 / other-US 33 / foreign 1) and Build I row (N00024-17-C-2117,
  $9,473.5M, EB 53 / HII 25 / other-US 22 / foreign 0), gray S_NOTE citation with
  both verbatim POP quotes + Block VI tripwire; `vintage_master_pop_cell(cls,
  field)` accessor; decimal dv on E:H.
- `model_tam_build.py` — §3a: two APPLIED lines "Virginia BC coefficient (Block V
  announced POP)" = other+foreign of its master (34.0%) and "Columbia BC
  coefficient (Build I announced POP)" (22.0%); pooled corpus line relabeled
  "(reference; not applied)" and de-bolded (bc_supplier_coeff_cell still points at
  it). §4a: two coefficient link rows; `BC_COEFF` is now a per-LI dict; each class
  block and the OBBBA stream multiply by `BC_COEFF[li]` ("class BC coeff" - the
  OBBBA boat is a Virginia -> 34%). §1 at-a-glance shows both (one row added,
  `_BN_BASE` 14 -> 15). New exports va_/col_bc_supplier_coeff_cell. Docstring
  restated.
- Consumers: `summary_executive_summary.py` (§1 takeaways, §2a BC bridge, §2c
  OBBBA bridge -> per-class rows), `guide_methodology.py` (§2a formula + live
  rows; §2d basis-by-FY table REWRITTEN to class-vintage; TAM hover note),
  `outputs_figure_register.py` (DO-02 -> Virginia, NEW **DO-82** Columbia;
  defined names `bc_supplier_coeff` -> `bc_supplier_coeff_va`/`_col` in _DEFINED
  + _DN_MEANING + dn_target), `chartdata_z_chart_data.py` (_COEFF block now 4
  rows: POP anchor / AP ref / Applied BC-Va / Applied BC-Col),
  `data_obbba_funding.py` (full-gross sensitivity -> Va coefficient),
  `validation_qa_reconciliation.py` (QA-14 -> Virginia class coeff),
  `validation_sensitivity.py` (corpus ladder relabeled "Pooled corpus ...
  (reference)").
- `industry_baseline_citations.csv` (workbook + research copies, kept identical):
  claims **33** (Block V POP, 34%) and **34** (Build I POP, 22%) appended with
  verbatim "Work will be performed..." quotes.

## Numbers (recalc-verified, 0 error cells, no REVIEW/FAIL)

| Metric | Before (pooled 35.02%) | After (class-vintage) |
|---|---|---|
| Virginia BC coefficient | 35.02% | **34.0% (Block V announced)** |
| Columbia BC coefficient | 35.02% | **22.0% (Build I announced)** |
| Cumulative portfolio TAM | 21,212.2 | **18,133.8** |
| OBBBA mandatory TAM | 937.7 | **910.3** (2,677.5 x 34%) |
| Avg annual TAM | 3,535.4 | 3,022.3 |
| Penetration FY22-27 / FY26-27 | 23.51% / 23.56% | **20.10% / 18.93%** (order flipped: FY26-27 is Columbia-heavy; Outlook lo/hi = MIN/MAX handles it) |
| A/B OBBBA off | 20,274.4 | **17,223.5** (= 18,133.8 - 910.3 exactly) |

SAM total = TAM identity holds; anchor regression (0.518 corpus stat) unchanged
OK; Va FY26 5,389.109 tripwire OK; QA module render-tested.

## Now stale downstream (updates the running list)

- **Consolidated workbook + deck**: every subs-derived hardcode (21.2122 walk
  endpoint -> 18.1338; combined TAM/SAM; work-type buckets scale; penetration
  strips 24.1-25.2% -> ~20-21% Va-Col blended; implied outyears; "35%" copy).
  Combined with the DDG restate: portfolio now DDG 6,421.7 + subs 18,133.8.
- **Subs deck slide_specs**: methodology.md + coefficient_evidence.md reference
  the single 35.0235% applied coefficient and the `bc_supplier_coeff` defined
  name (now _va/_col).
- **Subs wiki**: ch6/ch7 narrative still frames the corpus 35% as the applied
  coefficient.

## Gotchas

- The figure register bakes DEFINED NAMES into the workbook - renaming
  `bc_supplier_coeff` to `_va`/`_col` requires updating _DEFINED, _DN_MEANING,
  and dn_target together (KeyError at build otherwise).
- The subs §1 at-a-glance has the same `_BN_BASE` assert as DDG's `_NB_BASE`:
  adding a row means bumping the constant.
- Penetration window averages can REORDER under per-class coefficients (FY26-27
  is Columbia-heavy); the Outlook lo/hi MIN/MAX absorbs it but slide copy that
  assumed "recent window = high" needs care.
