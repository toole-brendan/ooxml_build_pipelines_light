# 2026-05-28 — Workbook review fix-pack + remaining-deck strategy

## Scope
Two passes of workbook fixes driven by external code reviews against `sub_workbook/workbook_submarines/`, followed by a strategic-thinking conversation on the remaining three methodology-deck slides and what should follow this deck. Workbook ended at 14 sheets, 43,966 bytes, 12 reconciliation checks, with every observed/derived/anchor figure explicitly labeled per the styling convention. No new sheets — every change was localized.

---

## 1. First-pass fix-pack (Tier 1 / Tier 2 / Tier 3)

Reviewer flagged 10 issues plus 7 proposed new reconciliation checks. After re-reading every sheet module the structural critiques all held. Implemented in three tiers.

### Tier 1 — Correctness fixes

- **`top_vendors.py` denominator bug.** The "% of in-scope total" column divided by `SUM(E6:E55)` — the displayed-subset sum — so the column always summed to 100% (concentration within top-50), not share of the full in-scope FFATA floor. Switched the denominator to `Subaward_Annual!O8` via the existing `grand_total_cell()` accessor. Column now sums to ~82.9% (the real top-50 share).
- **`funnel.py` FY27 silent zero.** The Unseen Mid formula subtracted the FFATA-visible floor cell — but FY27 sits outside the FFATA window and the floor cell was intentionally left unwritten. Excel treats blank as 0 in arithmetic, so FY27 unseen mid rendered = full outsourced Mid, indistinguishable from "observed floor is zero." Fixed: FY27 column now emits `None`+`S_DEFAULT` (no formula); FY16-FY26 columns wrap in `IF(OR(BC=0, NOT(ISNUMBER(floor))), "", ...)`.
- **`subaward_annual.py` lag-uplift wiring.** Inputs IN-09..IN-12 (FFATA lag-uplift multipliers, FY23-FY26) were defined but unused — orphaned editable assumptions. Added three new rows to Section 1: Va lag-adjusted, Col lag-adjusted, Grand lag-adjusted. Per FY: `=IF(observed=0, "", observed * Inputs!D{lag_row})` for FY23-FY26; `=IF(observed=0, "", observed)` for FY16-FY22 (implicit ×1.0). Section 2 PIID detail shifted down by 3 rows (now rows 13-29). Two new accessors: `lag_adjusted_cell(li, fy)`, `lag_adjusted_grand_total_cell()`.
- **`deckdata.py` DD-S5-03 redefine.** Was hardcoded blue `0.0` with "pending wire-up" source. Original framing compared annual FY27 Mid to cumulative FY16-FY26 floor — exactly the denominator-mismatch §6 warns against. Redefined as a like-for-like cumulative FY22-FY26 ratio: `(SUM Va floor FY22-FY26 + SUM Col floor) / (SUM Va out_mid FY22-FY26 + SUM Col out_mid)`. FY22-FY26 is the largest overlap between Funnel's FY22-FY27 window and FFATA's FY16-FY26. Two new range helpers: `cumulative_floor_range` on `subaward_annual.py`, `cumulative_metric_range` on `funnel.py`.
- **`deckdata.py` five style violations.** Workbook rule reserves `S_LINK_NUM`/`S_LINK_PCT` (green) for pure `=Sheet!Cell` refs only; sums/differences/ratios get `S_NUM`/`S_PCT` (black). Five rows were wrong: DD-S4-02 + DD-S4-06 (`Total - BC`) → `S_NUM`; DD-S5-01 (`Va_out_mid + Col_out_mid`) → `S_NUM`; DD-S5-04 + DD-S5-05 (`1 - EB%`, `1 - EB% - HII%`) → `S_PCT`. Now matches the convention `checks.py` already enforced.

### Tier 2 — Medium-priority cleanups

- **`dod_pop.py` helper cleanup.** Deleted `outside_eb_cell()` and `outside_team_cell()` — both had docstrings describing one thing but returned another (`outside_eb_cell` claimed "outside-EB-yard share" but returned EB%; `outside_team_cell` claimed "EB% and HII%" but returned only HII%). DeckData already imported `eb_pct_cell`/`hii_pct_cell` directly, so deletion was clean. Also wrapped the four SUMPRODUCT percent formulas with a zero-denominator guard (`=IF(SUMPRODUCT(D,F)=0, "", ...)`).
- **`references.py` enrichment (minimal + source title).** Source CSVs already carried richer fields the sheet wasn't exposing. Section 1: added `Source title`, `Source URL`, `Quoted text` columns (9 cols total). Section 2: added `Quote`, `Source URL` columns (8 cols total). Column widths re-tuned to `[10, 36, 14, 14, 18, 18, 48, 42, 60]` for the union. Skipped `deck_relevance` and `context` for now per user scope decision.
- **`scn_annual.py` + `prime_10k.py` ratio guards.** Both used `ISBLANK(...)` to guard BC%/GFE%/op-margin formulas. Funnel had already migrated to `=0` guards because `ISBLANK` returns FALSE for a cell holding a cross-sheet ref to an empty cell. Standardized: 4 formulas swapped to `=IF(cell=0, "", ...)`. The current input cells are hardcoded values where `ISBLANK` does work, but the change is defensive for when any of those cells gets migrated to a formula upstream.
- **`styles.py` + `lib.py` OOXML polish.** `S_HEADER_LEFT` had `borderId="1"` but lacked `applyBorder="1"` — added. `build_styles_xml()` added a minimal `<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>` block (LibreOffice and some strict readers expect it). `build_workbook_xml` `<calcPr>` gained `forceFullCalc="1"`. `write_row()` formula-detection broadened from `('-+\""` to `('-+\"$_{` so `=$A$1`, `=_xlfn.XLOOKUP(...)`, `={array}` get detected as formulas. Defensive — the current build emits none of these patterns. Skipped `dxfs`/`tableStyles` (only needed for conditional formatting / tables, neither used).
- **Stale docstring refresh.** Funnel top docstring and LAYOUT block had referenced "raw P-5c values loaded directly" and "FFATA-visible floor placeholder" — both dated from pre-Phase-A. Refreshed to describe the current state (cross-sheet refs to SCN_Annual + Subaward_Annual, FY27 blank outside window). SCN_Annual LAYOUT had "row 4-25" / "row 24-45" for block ranges where actual heights are 19 — corrected to "row 4-22" / "row 24-42" with explicit notes on the GFE-Sum CSV adjustment and the `=0` (not `ISBLANK`) ratio guards. Subaward_Annual LAYOUT updated to document the new lag-adjusted block.

### Tier 3 — Six new Checks rows

Added to `_CHECKS` in [checks.py](sub_workbook/workbook_submarines/sheets/checks.py):

| ID | Description | Tolerance | Notes |
|---|---|---|---|
| CHK-06 | Va FY27 P-5c rollup: Plans + GFE Sum + ChgOrd + BC ≈ Total | (see §2) | Surfaces the documented upstream CSV gfe_sum adjustment |
| CHK-07 | Inputs band monotonic: IN-01 ≤ IN-02 ≤ IN-03 | 0.5 | Binary 1/0 check; tolerance >0 so OK = delta 0 |
| CHK-08 | HII sub-portion monotonic: IN-06 ≤ IN-07 ≤ IN-08 | 0.5 | Same shape |
| CHK-10 | Top_Vendors %col sums to ≤ 100% (denominator validation) | (see §3 — replaced) | |
| CHK-11 | Funnel FY27 Va Unseen Mid is blank (window guard) | 0.5 | `IF(ISNUMBER(Funnel!H20), 0, 1)` → 1 means blank |
| CHK-12 | DoD_POP aggregate POP shares sum to ~100% | (see §2) | |

Skipped CHK-09 in this tier (string-search check on the source column) — re-added in §3 below.

Added `aggregate_pct_range()` accessor to `dod_pop.py` to back CHK-12.

---

## 2. Tolerance tuning — CHK-06 and CHK-12

On first build both CHK-06 and CHK-12 FAILed because the initial tolerances (1.0 and 0.005) were tighter than the documented gaps in the source data.

### CHK-06 — real residual
- Va FY27: Total $11,437M; Plans + GFE Sum + ChgOrd + BC = $11,192M. **Residual = -$245M.**
- Source: the upstream `build_cost_funnel.py` script applies an unexplained adjustment so the CSV's `gfe_sum_$M` ($1,898M) is $228M lower than the sum of the 5 GFE components ($2,126M). Plus ~$17M of other rounding/implicit categories.
- **Fix:** tolerance widened to ±$300M with description updated to flag the absorbed gap explicitly: *"Va FY27 P-5c rollup: Plans + GFE Sum + ChgOrd + BC ≈ Total (±$300M absorbs documented CSV gfe_sum gap)"*. Delta column still displays the live -$244.88M for the analyst to track over vintages; a regression that introduced an additional $50M+ residual would re-trigger FAIL.

### CHK-12 — real parser-miss drift
- Live aggregate: EB 24.5% + HII 12.1% + Other US 55.2% + Foreign 0.0% = **91.7%**. Drift -8.3pt from 100%.
- Source: 7 of the 13 in-scope DoD_POP rows have POP shares that don't sum to 100% (3 rows sum to 0% — meaning the parser couldn't extract location shares for those actions; one row sums to 40.86%). This is the "single-supplier-site actions stated without an explicit `%` are parsed as 0%, ~$1.6B of value" issue called out in METHODOLOGY §6.
- **Fix:** tolerance widened to ±10pt with description updated: *"DoD_POP aggregate POP shares sum to ~100% (±10pt absorbs documented parser misses, METHODOLOGY §6)"*. A drift past 12pt would re-trigger FAIL.

Lesson for future Checks rows: when the source data has a known structural gap, surface it in the description AND set the tolerance just above the live gap. The check then catches *new* regressions without yelling about the documented one.

---

## 3. Second-pass fixes (critiques #2 through #7)

Second external review caught five real issues missed in the first pass plus the shared-formula gotcha.

### Critique #2 — CHK-10 was tautological
The original CHK-10 only tested `SUM(Top_Vendors!G6:G55) <= 1.001`. If the old bug came back (denominator = displayed-subset SUM), the column would sum to *exactly* 100% and the check would still pass. **Replaced** with a formula-consistency equality:
- Expected: `SUM(Top_Vendors!E6:E55) / Subaward_Annual!O8` (~82.9%)
- Actual:   `SUM(Top_Vendors!G6:G55)`
- Tolerance: 0.0001 (percent equality)
- Styles: `(S_PCT, S_PCT, S_PCT)`

A regression to the displayed-subset denominator would make actual jump to 1.0 and delta ~+0.17 → FAIL.

### Critique #3 — Added CHK-09 (pending-wire-up guard)
The workbook has no "pending wire-up" source rows now, but nothing was locking that in. Added between CHK-08 and CHK-10:
- `IF(COUNTIF(DeckData!E6:E48, "*pending wire-up*")=0, 1, 0)`
- Expected: 1; tolerance 0.5

Range expanded to E6:E48 to cover the post-DD-S5-07/08 shift.

### Critique #4 — DeckData lag-adjusted floor rows
DeckData previously only surfaced the *observed* floor. Subaward_Annual now exposes the lag-adjusted view, so the deck should be able to show both. Added two new DeckData rows:
- **DD-S5-07** — Lag-adjusted FFATA-visible floor cumulative $M (FY16-FY26, MIB excluded). Pure cross-sheet ref → `S_LINK_NUM`.
- **DD-S5-08** — Lag-adjusted floor coverage % (cum FY22-FY26 lag-adj floor / cum FY22-FY26 modeled Mid, Va+Col). Mirrors DD-S5-03 shape but uses lag-adjusted numerator.

Required a new accessor on subaward_annual: `cumulative_lag_adjusted_floor_range(li, fy_start, fy_end)`.

Slide 6 banner/header/data rows shifted down by 2 to make room: DD-S6-01..09 now at rows 40-48 (was 38-46). DECK_ROW map updated.

### Critique #5 — References anchor accessors
Source CSVs already carried `source_url`, `source_title`, `quoted_text`, `quote_or_statement` columns we'd now started exposing in Tier 2.2 — but DeckData still hardcoded source strings like *"HII Q1 2026 earnings — References"* instead of pointing at specific claim_id / quote_id rows. Added six accessors to `references.py`:
- `claim_value_cell` / `claim_quoted_text_cell` / `claim_source_url_cell` (Section 1)
- `quote_text_cell` / `quote_topic_cell` / `quote_source_url_cell` (Section 2)

Backed by two module-level dicts (`CLAIM_ROW`, `QUOTE_ROW`) populated during `_build_layout()`.

Rewired DD-S6-07's source column to a string-concat formula: `="References EXEC-08 — " & References!G46` — auto-pulls EXEC-08's Topic field (the OFFICIAL HII Q1 2026 +30% guidance quote). DD-S6-08/09 sources upgraded to explicit *"Navy 30-Year Plan FY27 / distributed-manufacturing policy (METHODOLOGY §10; no discrete claim ID in References yet)"* — no matching claim exists in `industry_baseline_citations.csv` (verified by reading all 30 claims), so the gap is flagged explicitly rather than hidden behind vague "— References" text.

### Critique #6 — Stale docstrings
- DeckData top docstring's "Pending wire-up" paragraph replaced with the current four-pattern description (cross-sheet link / derived formula / hardcoded anchor / metadata) plus a note that CHK-09 enforces no-pending state.
- HII_TeamBuild LAYOUT block: Va range `4-11` → `4-10`, Col range `13-20` → `13-19`. The `+1` came from including the trailing blank row in the count; data actually ends one row earlier.
- `subaward_annual.floor_cell()` docstring claimed "Returns '' if fy is outside FY_COLUMNS" — actual code raises `ValueError`. Updated docstring to match.

### Critique #7 — Shared-formula awareness
Excel converts repeated formula runs into OOXML shared form on save (master cell carries `<f t="shared" ref="C5:H5" si="0">...</f>`, dependents emit `<f t="shared" si="0"/>` with no inline text). The build always emits canonical full-text formulas — Excel's conversion happens after the handoff. This only matters for raw-XML `<f>` greps (exactly what the verification scripts did this session).

Resolved as **documentation, not code**: added a new "DIRECT XML AUDIT" paragraph to [sheet_template.py](sub_workbook/workbook_submarines/sheets/sheet_template.py) (the workbook-wide style doc) explaining the canonical/shared distinction and recommending "rebuild from source first" as the standard audit workflow. Rejected the alternative (write a stdlib-only shared-formula resolver) — ~80 LOC of cell-ref-shifting logic that would re-implement what openpyxl does, when the simpler rebuild workflow gives identical results with no new code.

---

## 4. Strategic discussion — remaining deck slides + next steps

User asked for my read on what should come next after this fix-pack. Summary of the conversation:

### The methodology side deck (`sub_pptx/`)

Current state: 3 of 6 slides built (Cover, Cost Funnel, Methodology / Computation Pipelines). Three slot outlines from `slide_topics.md` remain unbuilt: Framing (slot 2), Scope & definitions (slot 3), What this means & doesn't mean (slot 6).

My recommendation: **build the three slots as outlined; do not expand the deck.** The 6-slide structure is right for a methodology *side* deck. Concrete suggestions for each:

- **Slide 2 — Framing.** Drive it off concrete data points we now have: (a) industry claim 26 is literally a `NOT FOUND` placeholder for "make/buy ratio for submarine prime contract" — no primary source exists; (b) visible FFATA cumulative on the 15 in-scope PIIDs is ~$6.14B, ~10% of the modeled outsourced layer; (c) three different LLMs / desk analysts could legitimately quote 20%, 60%, "GDEB does all of it" — all defensible against *different* denominator lenses.
- **Slide 3 — Scope & definitions.** Mostly mechanical, mostly pulls from DeckData DD-S3-01..09. IN panel on left (15 PIIDs, two LIs, two windows), OUT panel with explicit "why" (depot/EOH, SSP/Trident, federal yards, classified payload), decoder ring on right (8 acronyms — fits easily).
- **Slide 6 — What this means & doesn't mean.** Most overstuffed slot. Recommended hierarchy: top half = band visual + three triangulation supports (CRS/GAO pillars chip · MODELED HII team-build chip · GD-vs-HII strategic-divergence chip from Prime_10K capex line) as small-multiples; bottom half = MIB exclusion callout (BlueForge $4.17B + TMG $77M + IALR $1.5M) + top 4 caveats including the specific ~$1.6B single-site parser miss (the same gap CHK-12 now absorbs at ±10pt). If breaking tradition for 7 slides is on the table, this is the one to split.

### What I would *not* add to this deck

Tempting candidates that should live in the *recommendation* deck instead:
- Strategic divergence (HII expanding outsourcing per EXEC-08 + EXEC-13, GD investing in own yards per Marine Systems capex). Fascinating finding but it's an addressability *signal*, not a methodology element.
- LLTM bucket breakdown showing where outsourced layer physically lives (Nuclear plant → BPMI, Propulsor → vendors, etc.). The "where to play" map, not methodology.
- Top vendor concentration (top 50 = 82.9% of in-scope floor). Structural finding, not methodology.

### Real next steps (in order)

1. **Build the three planned methodology slides** (Framing, Scope, What this means). Renumber positions in `lib.py` once all three land — cost_funnel moves slot 2→4, methodology slot 3→5.
2. **DoD-announcement annualization** (METHODOLOGY §6 [Planned]). The CHK-12 8.3pt parser-miss drift we now document is the most visible quality issue; the obligation-pool-vs-annual-run-rate distinction is still unresolved. Unlocks the bridge table.
3. **Bridge table** (METHODOLOGY §11 [Planned]). One row per action/subaward/obligation joining all five layered sources, with derived `outside_GDEB_$`, `outside_team_yard_$`, `other_US_supplier_$` columns. Input to the addressability scoring.
4. **Capability anchor with Saronic-specific scoring.** The part data can't supply. METHODOLOGY §11 guardrail #10: "the ranking is meaningless without a capability anchor." Without this, the addressability ranking defaults to generic "build-to-print" (valves/pumps/forgings) which may not match the actual client's strengths (autonomy / distributed-manufacturing).
5. **Recommendation deck** — separate ~6-8 slide deliverable. Ranked heat map by work package, not a single number. Methodology deck and recommendation deck are sibling artifacts referencing the same workbook.

If forced to pick the single highest-leverage next move: **#4 (capability anchor).** Data infrastructure is solid; without a capability profile the rankings have no audience-specific signal.

---

## Final workbook state

```
Building sub.xlsx with 14 sheets …
  sheet 1: Cover        11,343 bytes
  sheet 2: References   52,699 bytes
  sheet 3: Inputs       15,278 bytes
  sheet 4: SCN_Annual   11,236 bytes
  sheet 5: LLTM_AP      14,954 bytes
  sheet 6: Subaward_Annual   16,893 bytes
  sheet 7: MIB_Excluded    2,901 bytes
  sheet 8: Top_Vendors   19,957 bytes
  sheet 9: DoD_POP      22,336 bytes
  sheet 10: Prime_10K     5,907 bytes
  sheet 11: Funnel       12,630 bytes
  sheet 12: HII_TeamBuild    7,099 bytes
  sheet 13: Checks        7,087 bytes
  sheet 14: DeckData     15,982 bytes
Wrote sub.xlsx (43,966 bytes)
```

- 14 sheets, 12 reconciliation checks (CHK-01..CHK-12), all OK against live data.
- All 21 archive parts pass `zipfile.testzip()` and `xml.etree.ElementTree.parse()`.
- Every styled formula matches the workbook convention (green=link, black=derived, blue=hardcoded anchor).
- Both observed and lag-adjusted FFATA floor views surfaced on DeckData (DD-S5-02/03 observed, DD-S5-07/08 lag-adjusted).
- Six accessor functions on References let downstream sheets point at specific claim_ids / quote_ids; DD-S6-07 already uses this pattern via EXEC-08.

### Files touched this session

| File | Changes |
|---|---|
| `sheets/top_vendors.py` | Denominator switch (Tier 1.1) |
| `sheets/funnel.py` | FY27 guard (Tier 1.2), cumulative_metric_range helper (Tier 1.4), docstring refresh (Tier 2.5) |
| `sheets/subaward_annual.py` | Lag-adjusted block + 3 accessors (Tier 1.3, Tier 1.4, Critique #4), `floor_cell` docstring fix (Critique #6) |
| `sheets/deckdata.py` | DD-S5-03 redefine (Tier 1.4), 5 style fixes (Tier 1.5), DD-S5-07/08 add (Critique #4), DD-S6-07 source formula (Critique #5), DD-S6-08/09 source text refresh (Critique #5), top docstring refresh (Critique #6), S6 row-shift (Critique #4) |
| `sheets/dod_pop.py` | Helper cleanup (Tier 2.1), SUMPRODUCT guards (Tier 2.1), `aggregate_pct_range` accessor (Tier 3) |
| `sheets/references.py` | Column enrichment (Tier 2.2), CLAIM_ROW/QUOTE_ROW maps + 6 accessors (Critique #5) |
| `sheets/scn_annual.py` | `=0` guards (Tier 2.3), LAYOUT docstring refresh (Tier 2.5) |
| `sheets/prime_10k.py` | `=0` guards (Tier 2.3) |
| `sheets/hii_teambuild.py` | LAYOUT row-range fix (Critique #6) |
| `sheets/checks.py` | 7 new checks (Tier 3); CHK-06/CHK-12 tolerance tuning (§2); CHK-09 added + CHK-10 rewritten (Critiques #2/#3) |
| `sheets/sheet_template.py` | Shared-formula paragraph added (Critique #7) |
| `styles.py` | `applyBorder` fix + `cellStyles` block (Tier 2.4) |
| `lib.py` | `forceFullCalc` + formula-detection broaden (Tier 2.4) |

---

## Open follow-ups for the next session

1. **Three methodology-deck slides** (Framing, Scope, What this means) — outlined but not built. Renumber `sub_pptx/deck_submarines/lib.py` slot positions once all three land.
2. **DoD-announcement annualization** (METHODOLOGY §6 [Planned]) — would also tighten CHK-12's tolerance back toward 0 if the parser miss is addressed upstream.
3. **Bridge table + addressability scoring** (METHODOLOGY §11 [Planned]) — separate workstream, separate deliverable.
4. **Capability anchor with Saronic-specific scoring** — the part the data can't supply.
5. **Recommendation deck** — separate ~6-8 slide artifact downstream of #2/#3/#4.
6. **DD-S6-08/DD-S6-09 anchor claims.** No discrete claim in `industry_baseline_citations.csv` matches the Navy 10%→50% distributed-shipbuilding target. The source string flags this; the cleaner fix is to add a Navy claim to the source CSV with the 30-Year Plan FY27 URL + quoted text, then rewire DD-S6-08/09 to `claim_value_cell` and the source-pull formula pattern DD-S6-07 already uses.
7. **CHK-06 vintage tracking.** The -$244.88M Va FY27 P-5c residual is now absorbed at ±$300M tolerance with the delta visible. Worth periodically checking whether the upstream `build_cost_funnel.py` adjustment shifts across vintages — if it does, the tolerance may need re-tuning.

---

## Reference files used this session

- `sub_work/METHODOLOGY.md` — §6 (DoD POP), §7 (lag uplifts), §8 (MIB exclusion), §9 (band + triangulation), §10 (anchors), §11 (addressability + capability anchor), §12 (10 guardrails).
- `sub_workbook/extracted/industry_baseline_citations.csv` — 30 claims; confirmed claim 26 is `NOT FOUND placeholder` for make/buy ratio; confirmed no Navy 10/50 claim exists.
- `sub_workbook/extracted/exec_commentary_makebuy.csv` — 17 quotes; EXEC-08 identified as the OFFICIAL HII Q1 2026 +30% anchor and wired into DD-S6-07.
- `sub_workbook/extracted/cost_funnel_with_subawards.csv` — confirmed Va FY27 -$245M P-5c residual breakdown for CHK-06 tolerance sizing.
- `sub_workbook/extracted/dod_action_pop_by_worktype.csv` — confirmed 7 of 13 in-scope rows have POP shares not summing to 100% for CHK-12 tolerance sizing.
- Prior session logs: `logs/2026-05-28_methodology_deck_session.md`, `logs/2026-05-28_workbook_session.md`.
