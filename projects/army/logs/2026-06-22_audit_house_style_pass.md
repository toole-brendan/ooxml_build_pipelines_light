# 2026-06-22 — Audit response: house-style pass (the 10-item presentation review)

Session log AND handoff. Continues the same workbook after the release-gate fixes
(`2026-06-21_audit_response_release_gates.md`). A second audit judged the workbook
"structurally strong and technically clean" — the deviations were **presentation and
authoring discipline**, not OOXML mechanics. This session executed all 10 recommendations
in eight gates, keeping the build green and `verify_timing.py` passing throughout.

Build is green: **22 sheets, 17 native tables, 2 note parts, 0 error cells.** Output:
`projects/army/20260620_US Army Market Mapping_vS.xlsx`. Verification: **`verify_timing.py`
25/25**, **new `lint_style.py` PASS (22 sheets, 5 documented exceptions)**, **0 `t="e"`,
0 `#REF!`/`#NAME?`/`#DIV0!`/`#VALUE!`/`#N/A`**, all worksheet + styles XML well-formed,
conditionalFormatting before tableParts on every decision sheet.

## The one architectural decision (audit #2)
The audit said "choose one model" for the editable surface. Took the **preferred** path —
dedicated **input tabs** in the `inputs` group, with model sheets linking green — over the
report-only alternative. Decomposed it to avoid a duplicate editable surface mid-stream:
Market Assumptions (numeric knobs) migrated in Gate 2; the per-family `recompete_reviews`
relocation folded into Gate 6 (the screen split), where those sheets were re-columned anyway.

---

## Gate 1 — percentage & coverage formatting (#1)
- `_flat.make_flat_sheet`: new `pct_cols=` — a 0-1 fraction coerced like a float but rendered
  with the italic percent styles (S_PCT / S_PCT_INPUT / S_LINK_PCT) so a stored 0.85 reads
  "85.0%". (Also added `header_labels=` + `validations=` here, used by later gates.)
- Market Size: the 8 % / fit knobs + Saronic priority → percent styles.
- Timing Screen Coverage → S_PCT, Saronic priority score → S_LINK_PCT; Queue Coverage →
  S_LINK_PCT; Contract Families `coverage_ratio` → S_PCT_INPUT.
- Result: **2,392 percent-styled cells** where there were **0** (the audit's headline defect).

## Gate 2 — centralize market knobs (#2, part 1)
- New **`Market Assumptions`** input tab (`input_market_assumptions.py`), inputs group:
  mirrors `market_assumptions.csv` + `saronic_relevance.csv` per opportunity (24 blue % inputs,
  humanized headers, source column).
- Market Size: the 8 knobs are now **green INDEX/MATCH links** into that tab (keyed on the
  opportunity name). Market Size blue inputs: **24 → 0**.

## Gate 3 — blue text + data validation (#7, #8, part 1)
- New `primitives.data_validation()` (shared engine) + `_validate.py` (canonical dropdown
  vocabularies + spec builders) + `make_flat_sheet(validations=)`.
- Customer Map: blue restricted to the 5 CRM fields (owner / status / next action / as-of /
  notes) — identity/command/geography/source/official-name now black (~169 → 65 blue text
  cells); machine headers humanized (`org_id` → "Org ID", …).
- Validations: Market Assumptions (8× decimal 0-1), Customer Map (engagement-status dropdown
  + as-of date), Notice Links (Y/N + date). The recompete_reviews dropdowns landed in Gate 6.

## Gate 4 — prose + titles + section labels (#3, #9)
- Intro captions cut to one line; footer essays replaced by compact `§2 - Method & caveats`
  blocks (Market Size) or short rows; stopped explaining formatting ("BLUE inputs", "LIVE"),
  stopped exposing CSV paths / field names, de-capped emphasis.
- Overview title `U.S. Army - … - Overview` → **Overview**; section labels shortened
  (`§1 - Market size`, `§2 - Contract evidence`, `§3 - Analyst readiness`, Notice Links
  `§1 - Notice-family review`, O&M `§1 - O&M evidence`, QA `§4 - Historical obligations`,
  Queue `§1 - Research queue`). Readiness "Source CSV" column → plain "Where to fill" labels.

## Gate 5 — Scope & Assumptions redesign (#4)
- Rebuilt the 140-wide one-column essay into a structured `§1 - Purpose` … `§6 - Sources &
  freshness` sheet with a **Topic / Rule / Where-enforced** table (cols 22 / 46 / 24). Longest
  visible text **1,096 → 80 chars**.

## Gate 6 — split the two decision sheets (#5) + #2 part 2
- New **`Recompete Reviews`** input tab (`input_recompete_reviews.py`): the per-family analyst
  judgment surface (window / confidence / pursuit / program / capability / milestones /
  capture override / notes), 1,582 blue inputs + 8 validations (the deferred Gate 3 dropdowns).
- **Timing & Incumbent Screen** narrowed **43 → 15 columns** (Family, Incumbent, Segment, Tier,
  Selected $M, Coverage, Decision date, Months, Decision window, Date confidence, In-market,
  Opportunity, Priority, Confidence, Pursuit access). Confidence / Pursuit link Recompete
  Reviews; Selected $M / Coverage / Decision date link Contract Families. Blue inputs: **0**
  (As-of cell excepted). The shared selection+sort is computed ONCE (`_screened()` →
  `SCREENED`, exposed) so the screen and detail share row order.
- New **`Timing Detail`** sheet (`model_timing_detail.py`, 29 cols): the moved provenance —
  relevance basis, PSC/NAICS, cohort, the reconciliation lenses, four end-date lenses, lineage
  candidates, action counts, anomaly. Same row order as the screen (verified: both start
  `W56HZV17D0086`).
- **Recompete Research Queue** narrowed **33 → 25 columns**: kept the capture-oriented fields,
  moved planned milestones + reconciliation + anomaly out; Confidence / Pursuit / Notes /
  Capture-lead link Recompete Reviews. Blue inputs: **0** (only "Incumbent since", a
  build-baked chain-root value, stays blue — excepted).

## Gate 7 — styled ranges (#6)
- Dropped the native tables on Budget Market + Market Size (fixed model rows, not filterable
  lists); kept the styled header / body / total. Native tables **17 → 15** at that step (back
  to 17 after the two new input tabs + Timing Detail). Cross-sheet accessors unaffected
  (they use absolute ranges, not the table).

## Gate 8 — style linter + signature-aware probe (#10)
- New **`lint_style.py`** (standalone, mirrors `verify_timing.py`): renders every registered
  sheet and asserts TITLE_MISMATCH, UNNUMBERED_SECTION, VISIBLE_TEXT_OVER_180,
  COLUMN_WIDTH_OVER_LIMIT, PERCENT_HEADER_USING_NUM_STYLE, BLUE_INPUT_OUTSIDE_INPUTS_GROUP,
  MODEL_NATIVE_TABLE, CATEGORICAL_INPUT_WITHOUT_VALIDATION. Per-sheet `EXCEPTIONS` keep
  deliberate deviations visible. It caught 10 real stragglers (long data-leaf intros, Budget
  Market footer, Overview/QA widths) — all fixed. 5 documented exceptions remain (the three
  filterable decision screens keep native tables; the As-of + Incumbent-since blue inputs).
  - VISIBLE_TEXT skips cells inside a native-table range (raw source descriptions are faithful
    evidence under the no-wrap rule, not authored captions).
- **`sheet_probe.py` file mode** now resolves each cellXf by **signature** (resolved numFmt /
  font / fill / border / alignment), not by numeric index — so a workbook Excel opened +
  re-saved (which renumbers the style table) is still labelled by what each style IS. Proven
  against a reversed style table: signature → 24 inputs (correct), naive index → 0 (the old bug).

---

## Verification
1. `python3 build_workbook.py` → 22 sheets, 17 tables, 2 notes, green guards.
2. `python3 verify_timing.py` → **ALL 25 CHECKS PASSED** (unchanged — it reads the data layer,
   independent of the rendered columns).
3. `python3 lint_style.py` → **STYLE LINT PASSED (22 sheets, 5 excepted)**.
4. XML scans over the built `.xlsx`: 0 `t="e"`, 0 error tokens, all XML well-formed.

## New / changed files
- New sheets: `input_market_assumptions.py`, `input_recompete_reviews.py`,
  `model_timing_detail.py`. New helpers: `_validate.py`. New gate: `lint_style.py`.
- Engine (workbook_core): `primitives.data_validation()`; `sheet_probe.py` signature-aware
  file-mode style resolution.
- Tab order now: Overview · Scope & Assumptions · **Market Assumptions** · **Recompete
  Reviews** · Customer Map · Budget Market · Market Size · Timing & Incumbent Screen ·
  Recompete Research Queue · **Timing Detail** · (data leaves) · QA · Data Freshness · Source Log.

---

# HANDOFF — what remains

## A. The analyst pass (human; structures wired, values blank/seed)
Unchanged from 2026-06-21. The editable surface is now consolidated on the **inputs** tabs:
- **Market Assumptions** — replace the seed % / fit knobs with sourced values (drives every
  market $ via the green links).
- **Recompete Reviews** — fill confidence / pursuit / window / program / capability node /
  planned RFI-solicitation-award milestones / capture override per family (the Screen + Queue
  link to it). Dropdowns enforce the vocabularies.
- **Customer Map** — engagement status / owner / next action.
- `analyst/lineage_edges.csv`, `analyst/notice_family_links.csv` — disposition as before.

## B. Deferred coding (unchanged from the prior log)
1. Bottom-up work-package serviceability bridge (give work packages their own sheet).
2. Low/base/high scenarios on Market Size.
3. P-5 line item `9552ML5355` duplicate Recurring-Cost block (flagged in the extract log).
4. FPDS Atom → SAM Contract Awards API migration (recent-DoD dollar completeness).

## C. Style discipline is now a build-time gate
`lint_style.py` is the style analogue of `verify_timing.py` — run it (and the verify) after any
sheet change. New deliberate deviations go in its `EXCEPTIONS` table (with a reason), never by
weakening a rule. The `sheet_probe.py` file-mode probe is now safe to run against an
Excel-touched copy of the workbook.
