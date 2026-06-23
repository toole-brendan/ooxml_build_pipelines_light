# 2026-06-23 — Structure-Class terminology + workbook-local presentation pass

A presentation/readability pass on `award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`), implementing an external review's recommendations. The
headline change is **terminology**: the annual structure screen on Where to Play drops the
interpretive `Fortress / partner-led … / Open / dynamic` 2×2 labels for a **neutral MECE
classification** that names the underlying math. The rest is a workbook-local presentation pass:
tab-block reorder (model before inputs), percent number formats on the Where-to-Play ratio
columns, semantic column widths + display-header aliases, first-column header labels on the
matrices, and tighter analyst-written visible copy (with the dropped detail preserved in
docstrings).

Workbook stays **21 sheets, 17 native tables**. Build clean (**0 XML errors, 0 error-literal
cells**); house-style linter **0 failures, 0 warnings**; **full headless LibreOffice recalc is
0-error workbook-wide** with every arithmetic invariant satisfied (discharges the standing recalc
gate on the final artifact). Working tree only; **no data CSV or build script touched** — pure
presentation + a label/threshold-vocabulary change.

**One scope decision locked with the user up front:** the plan's §7 (extend `tools/style_audit.py`
with a header-clip / stale-label / generic-copy audit) was **declined** — the user does not want
more audit-tool machinery and asked the agent to verify those properties directly instead. So
`tools/style_audit.py` is **unchanged**; the §7 properties were verified by hand against the built
+ recalced workbook (see Verification). Everything else (§1–§6) was implemented as specified.

---

## 1. Neutral MECE structure classification (the terminology change)

The annual screen combines two binary tests (Parent HHI ≥ 0.40, incumbent-$ ≥ 75%) plus a
low-supplier-count exception. The old labels (`Fortress / partner-led`, `Concentrated / rotating`,
`Broad / relationship-heavy`, `Open / dynamic`, `Thin observation`) read as interpretation; the new
labels name the dimensions directly and stay MECE:

| Label | Definition |
|---|---|
| `Low Count` | Active suppliers < 3 |
| `HHI-H / Inc-H` | Parent HHI ≥ 0.40 and incumbent $ ≥ 75% |
| `HHI-H / Inc-L` | Parent HHI ≥ 0.40 and incumbent $ < 75% |
| `HHI-L / Inc-H` | Parent HHI < 0.40 and incumbent $ ≥ 75% |
| `HHI-L / Inc-L` | Parent HHI < 0.40 and incumbent $ < 75% |

- **NEW `sheets/_structure_classes.py`** — one source of truth: the three thresholds
  (`MIN_ACTIVE_SUPPLIERS=3`, `HIGH_PARENT_HHI=0.40`, `HIGH_INCUMBENT_DOLLAR_SHARE=0.75`), the five
  labels, `STRUCTURE_CLASSES`, and `STRUCTURE_RULES` (label, rule-text) pairs.
- **`sheets/where_to_play.py`** — `_f_structure()` rewritten to emit the five labels from the shared
  constants. The **canonical internal header stays `Observed Structure`** (so the `cols` accessor
  and the Executive-Summary INDEX/MATCH lookup never break); it now **displays as `Structure
  Class`** via `display_headers`. Docstring de-vocabularied.
- **`sheets/guide_methodology.py`** — §5 renders `STRUCTURE_RULES` as a small `Class | Rule`
  definition table (replacing the long Observed-Structure paragraph), so the legend cannot drift
  from the formula.
- **`sheets/executive_summary.py`** — §4 scorecard's last column header → `Class`; the screen note
  and §4-description vocabulary updated. The scorecard still reads the canonical `Observed
  Structure` column.
- **`validate_workbook.py`** — the formula spot-check key `("Where to Play", "Observed Structure")`
  → `("Where to Play", "Structure Class")` (the spot-check matches the *displayed* header).

## 2. Tab-block reorder — model before inputs (workbook-local)

Reader order is now **summary → guide → model → inputs → data**: a reader meets the answer pages,
then the calculations, then the editable mappings/deflators. Done as a **project-local
`GROUP_ORDER` override**, exactly analogous to the existing project-local color override, with **no
edit to the shared `workbook_core/groups.py`**.

- **`lib.py`** — after the palette `update`, a `_LOCAL_GROUP_SEQUENCE` mutates
  `_groups.GROUP_ORDER` in place (`clear()` + `update()`, because `workbook_core.lib` imported the
  same dict object — reassigning would not be seen). Process-scoped; every other pipeline keeps the
  core order. The mapping sheets stay in the **`inputs`** group (olive tabs) — only their position
  moved.
- **`sheets/__init__.py`** — `SHEETS` + the import block reordered to the new sequence; module
  docstring updated (`answer → scope/method → model/calculations → mappings/deflators → evidence`).
- **`validate_workbook.py`** — `EXPECTED_SHEETS` reordered to match (final tab map: 1–5 summary,
  6–7 guide, 8–13 model, 14–17 mapping/deflators, 18–21 data). The packager's group-contiguity
  assertion passes against the overridden order.

## 3. Column widths + display-header aliases (`sheets/_widths.py` + 9 sheets)

Added semantic width constants `W_RATIO=14`, `W_STATUS=18`, `W_METRIC=18`, `W_CLASS=16`. Applied:
- **Where to Play** — `_WIDTHS` rebuilt from the new aliases (ratio/status/metric/class); short
  display headers (`Code`, `Archetype`, `FY`, `Net $M`, `Active UEIs`, `Effective Parents`,
  `Incumbent UEI %`, `First-observed %`, `Reactivated %`, `Structure Class`).
- **Supplier-Year Activity** — visible columns widened (`Distinct subawards` 18, prior/earlier-active
  15/17, status 16) + display aliases (`FY`, `Supplier`, `Parent UEI`, `Net $M`, `Positive $M`,
  `Prior FY Active`, `Earlier FY Active`, `Domain (D)`, `Output (P)`); banner/intro shortened.
- **Mapping - NAICS Defaults / Vendor Overrides / HII Code to SWBS / Deflators / Prime Awards** —
  display aliases instead of wide columns (`Domain (D)` / `Output (P)` / `Status`; `Supplier UEI`;
  `HII Code` / `Subsystem` / `Basis` + widths 12/14/–/18; `Procurement Index` / `FY26 Factor` +
  widths 17/12; Prime's four verbose `$M`/count headers aliased).
- **Domain Concentration** — `Observed Structure` 15→18, `Parent Eff Firms` 13→16, plus minor bumps.
- **Executive Summary** — analytical columns `10 → 13`.
- **Subaward Activity** — distinct-subaward / PIID-pair column (D) `16 → 20`.

Minor deviations from the plan's exact width numbers (e.g. prior/earlier-active 15/17 not 14/16;
Procurement Index 17 not 16) were chosen so each displayed header fits its column — the plan
numbers were guidance and these are within its 14–20 band.

## 4. First-column header labels on the matrices

- **`sheets/domain_concentration.py`** — first `_HEADERS` cell `"" → "Capability Domain"`.
- **`sheets/executive_summary.py`** — `_matrix()` gained a `row_header` param; both header rows now
  name the archetype-label column (`Program` group row, `Capability Domain` / `Primary Output`
  sub-header); the SWBS matrix's first header `"" → "SWBS Group"`.

## 5. Tighter visible copy (rationale kept in docstrings)

Shortened the visible captions/caveats/notes on Executive Summary, Domain Concentration, Where to
Play, Supplier-Year Activity, Subaward Activity, Market Bridge, and the Taxonomy framing intros
(`_taxonomy.py`) — short analyst-oriented statements in cells, **detail preserved in source
docstrings** per the plan's principle:
- Domain Concentration's Observed-Structure threshold definitions → moved into the module docstring.
- Subaward Activity's tier thresholds → already in (and kept in) the module docstring.
- Market Bridge's full disclosed-ledger provenance (the $10.2B / ~$3.4B lineage, contract numbers,
  sources) → moved into the module docstring; the §3 visible rows are one line each.
- `_taxonomy` category **definitions are unchanged** (substantive); only the framing intros tightened.

## 6. Percent number format for the Where-to-Play ratio columns

- **`sheets/_flat.py`** — added a `pct_cols` column type (`S_PCT` / `S_PCT_INPUT` / `S_LINK_PCT`),
  coerced as a decimal and centered like the other numerics; defensive `.get` so a (non-existent)
  pct input-fill can't `KeyError`.
- **`sheets/where_to_play.py`** — the eight ratio columns moved `float_cols → pct_cols`, so
  `Program Share`, `YoY $ Growth`, `Parent Top-1`, the two incumbent shares, retention, first-observed
  and reactivated now render as true percentages (`0.0%`), not bare decimals. (Net $M / Parent HHI /
  Parent Eff Firms stay `float_cols`.)

## 7. (DECLINED) `tools/style_audit.py` extension

Not implemented, by the user's call ("I don't like audit tools… you can determine yourself
instead"). `tools/style_audit.py` is **unchanged**. Context for any future revisit: the plan's
clip-warning heuristic, simulated against the build, fired **146 warnings** — 65 on the three raw
transaction spines (faithful FSRS field names the plan elsewhere says *not* to widen) plus
trivially-fine short headers (`Share`, `HHI`, `Code`) from its `max(10, len+1)` floor — and could
not reach the plan's own "0 warnings" target even with the plan's prescribed widths. The
blank-first-header / missing-row-label-header / stale-label / generic-copy properties it would have
checked were instead verified directly (see below) and are all clean.

---

## Verification (all green, final artifact)

| Check | Result |
|---|---|
| `python3 build_workbook.py` | exit 0, **21 sheets, 17 native tables**, 8 integrity guards pass |
| `python3 validate_workbook.py` | parts 76, **0 XML errors, 0 error-literal cells, 0 structural issues** (sheet set/order, tab palette, formula spot-checks incl. `Structure Class`) |
| `python3 tools/style_audit.py` (existing, unchanged) | **0 hard failures, 0 warnings** |
| **Headless LibreOffice recalc** (soffice 25.8, OOXMLRecalcMode=0) | **0 error cells across all 21 sheets** |
| Structure-class labels (228 active WTP rows) | all valid (one of the 5 MECE classes); Exec §4 scorecard `Class` cells resolve too |
| Invariant: incumbent$ + first-observed$ + reactivated$ = 100% | 0 violations |
| Invariant: retention ≤ 100% | 0 violations |
| Invariant: parent Top-1² ≤ parent HHI ≤ parent Top-1 | 0 violations |
| Invariant: program-share sums to 1.0 (D axis, FY25) | Virginia / Columbia / DDG-51 = 1.0000 |
| Percent columns render as `0.0%` (not decimals) | confirmed on WTP ratio columns |
| Manual §7 checks | no blank/missing first-column headers (matrices labelled); **grep: 0 stale `Fortress`/`Thin observation`/… in source or built workbook**; generic copy removed |
| Tab order | summary(1–5) · guide(6–7) · model(8–13) · inputs(14–17) · data(18–21) |
| `py_compile` | passes on every changed module |

Recalc recipe (no committed harness; throwaway profile forces full recalc on load):
`registrymodifications.xcu` → `/org.openoffice.Office.Calc/Formula/Load OOXMLRecalcMode=0`, then
`soffice --headless -env:UserInstallation=file://<profile> --convert-to xlsx:"Calc MS Excel 2007
XML" --outdir <out> award_classification_refactor.xlsx`, then `openpyxl(data_only=True)` scan for
`#DIV/0|VALUE|REF|NAME|NUM|NULL|N/A`.

## Files

- **New (1):** `sheets/_structure_classes.py`.
- **Engine / wiring (4):** `lib.py` (group-order override), `sheets/__init__.py` (reorder),
  `sheets/_flat.py` (`pct_cols`), `sheets/_widths.py` (semantic width constants).
- **Sheets (10):** `where_to_play.py`, `supplier_year_activity.py`, `executive_summary.py`,
  `domain_concentration.py`, `guide_methodology.py`, `subaward_activity.py`, `market_bridge.py`,
  `_taxonomy.py`, `naics6_archetype_map.py`, `vendor_archetype_overrides.py`, `hii_swbs_crosswalk.py`,
  `deflators.py`, `prime_awards.py`.
- **Gate (1):** `validate_workbook.py` (`EXPECTED_SHEETS` order, `Structure Class` spot-check).
- **Regenerated:** `award_classification_refactor.xlsx`. `tools/style_audit.py` **unchanged**.

## Carry-forward

- **Working tree only** at time of writing.
- The structure-class thresholds + labels now live in **`sheets/_structure_classes.py`** —
  change them there; Where to Play (formula) and Methodology (legend table) both read it, so they
  cannot drift.
- The tab-block order is a **process-local `GROUP_ORDER` override** in `lib.py` (alongside the
  palette override). Do not edit the shared `workbook_core/groups.py`.
- `pct_cols` is now available on `make_flat_sheet` for any future percent column.
- The recalc gate (memory `workbook-recalc-verification`) was re-run on the final artifact and is
  0-error workbook-wide.
- ⚠️ Still do **not** run `scripts/build_archetype_overrides.py` (clobbers the curated
  `vendor_archetype_overrides.csv`).
