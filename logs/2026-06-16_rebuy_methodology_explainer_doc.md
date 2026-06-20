# 2026-06-16 — Re-buy methodology explainer (Word doc): deep-dive confirmation, data-fidelity section, markdown-clean styling

Page module: `projects/distributed_shipbuilding/doc/doc_distributed_shipbuilding/pages/rebuy_methodology_explainer.py`
Build:   `python3.12 build_doc.py` (from `projects/distributed_shipbuilding/doc/`)
Output:  `projects/distributed_shipbuilding/20260615_Distributed Shipbuilding_Build Spec_vS.docx`
Inspect: `python3.12 docx_core/doc_probe.py doc_distributed_shipbuilding.pages.rebuy_methodology_explainer`

All edits this session were **inline in the page module — no `docx_core` changes** (the core
files were authored yesterday and are treated as not-yet-hardened; the user asked to keep
changes inline). The whole arc: confirm the re-buy methodology against the workbook source,
repurpose the explainer, then a styling pass.

## 1. Deep-dive: confirmed the explainer against the workbook source

Traced the plain-language explainer claim-by-claim through the Award Analysis workbook
(`workbook_award_analysis/workbook_award_analysis/sheets/`) and the upstream compute script.
**The explainer is accurate.** Key mappings:
- Lane = (program, PIID, work type): `compute_jumpball_signals.py` keys lanes on
  `(program, piid, bucket)`; the screen formulas key on each row's PIID(C)+Work Type(D)
  (`data_rebuy_timing.py`).
- Active suppliers = COUNTIFS(rec_recent>0); Top-1 share = MAXIFS/SUMIFS over recent $;
  **Others'/"shared %"** = 1 − Top-1 (`data_rebuy_timing.py`).
- Cadence = 90-day burst clustering (`CLUSTER_GAP_DAYS=90`, `_clusters()`), median gap of
  cluster-START-to-START (`median_cluster_gap_days`); Next = last + gap (`next_f`).
- Re-buy due = COUNTIFS(next in [as-of, EDATE(as-of, horizon)]) (`rb_due_count`).
- Both "honest limits" are real: the prime-overlay timing test (`prime_clustering_test`,
  diffuse) and dollar-share (not head-count) concentration.

Corrections found and folded into the doc:
- "within 12 months of **today's date**" → the **frozen as-of date (2026-05-22) + a horizon
  control (default 12 mo)** — reproducible, not `TODAY()`.
- "shared %" is a **sort/filter dial**, the hard gate is **≥2 active suppliers**.
- **cadence is full-history; the shared test is recent-window** — a lane must pass both.
- a lane needs **≥2 buy waves** to get a cadence (single-wave lanes blank out, not flagged).
- the tab is now **"Recompete Timing"** (the Indicators screens were split into their own tabs
  per `_tabs.py`), so the source line was updated from "Re-buy Timing screen".

## 2. Subaward data fidelity (investigated via `research/scripts/_corpus.py`)

Source = SAM/FSRS **full-history** subaward pulls (`sam_subawards_fullhistory/N*_subawards.json`,
one file per PIID), loaded by `_corpus.iter_records()` (27 fields/record). Supplier-role
universe (reconciles to the workbook tie-out): **subs 13,006 (Va 7,725 + Col 5,281), DDG 5,741.**

Fidelity of the fields the re-buy read uses (strong where it matters):
- `subAwardDate`: **100%** present & parseable → the cadence clock has no gaps.
- `subAwardAmount`: positive **94.3% subs / 99.8% DDG**; ~818 subs records are negative
  (de-obligations, netted), 2 exact zeros.
- `vendor_key`: **100%** carry a UEI; parent-rolled **60% subs / 71% DDG**, else entity UEI.
- `naics4` capability tag: **68% subs / 63% DDG** (a secondary leaf lens, not in the lane/share
  logic).

What's available but deliberately unused — `subawardDescription` (the component field two
external LLMs wanted to parse): 100% populated but low-signal —
- **subs: 74% are "SEE …" pointers** (SEE BELOW / SEE COMPLETE DESCRIPTION / SEE REMARKS …);
  only ~26% carry a real component word.
- **DDG: 82% are yard line-item/spec codes** (`01021-01 STRUCTURAL DOORS`).
- The "SEE …" points to the report's **other** free-text field, `descriptionOfRequirement` —
  itself only **115 distinct values across 14,381** subs "SEE" records: usually a boat/build
  label (`SSN 792 CONSTRUCTION (BOAT 1, FY14)`) or a mod/admin/billing/adjudication action,
  only occasionally the actual part (sometimes appended on a 2nd line, e.g. `HEAT EXCHANGER
  NOZZLE`).
- → confirms the methodology: classify work type on the **vendor** (registry + NAICS), not the
  award text.

## 3. Doc content changes (plain-language, single-audience)

- **Jump-ball context up top**: new H2 "Three kinds of sourcing opening" names re-buy/recompete
  (the focus), concentration, source diversification — one line each — then the page focuses on
  re-buy. (User chose plain-language depth; no under-the-hood mechanics section.)
- The five corrections above folded into the body and Table 1.
- **New section "What the analysis reads from the data"** + **Table 2** (RuleTable): what each
  ingredient reads + how complete it is, then a paragraph on the description field's
  unreliability and the "SEE …" → contract/boat-label / admin-action color.

## 4. Pagination fix (`_rule_table` helper, inline)

The first render showed Table 1 splitting **mid-row across a page break** with no header on the
continuation. Fix: post-process the table XML to inject `<w:cantSplit/>` into every row so a row
never breaks mid-cell; the primitive already sets `<w:tblHeader/>`, so a table that crosses a
page now **repeats its header**. Captions got `keep_next=True`. (Tried full keep-together first —
intact tables but big white gaps — and reverted to cantSplit + header-repeat, which fills pages.)

## 5. Markdown-clean text hierarchy / styling pass (no blue)

- **Headings**: kept black (house ask: no blue font at all) and added a **thin gray bottom rule**
  under H1 (`sz=12`, `#7F7F7F`) and H2 (`sz=6`, `#BFBFBF`) via `_HRULE` — hierarchy now reads
  through divider + size ramp instead of color.
- **Inline list system** (`_list` / `_olist` / `_list_para`) drawn by hand (glyph run + `<w:tab/>`
  + per-level hanging indent matching the workbook list geometry: glyph at 0.25/0.5/0.75in, text
  0.25in further): **`•` disc → `◦` circle → `▪` square**, 2pt between items, **6pt breather after
  each list** (was missing — lists used to collide with the next paragraph).
- **Sub-bullet restructuring**: "Three kinds" (kind → description) and "Two honest limits"
  (headline → elaboration) now nest parent→child; supplier-lane components got bold lead terms;
  the cadence numbered list became a manual `_olist` (`1.`/`2.`…) sharing the same geometry +
  breather so the spacing contract is uniform.

### Tradeoff (flagged to user)
The lists are now **P_LIST-styled paragraphs with hand-drawn glyphs, not native `numPr` lists**
(probe: "list paragraphs: 0", ListBody 23). Visually identical and they paginate fine; the only
loss is Word's list-UI affordances (promote/demote, auto-renumber) — irrelevant for a generated
doc. Reverting to real Word lists (native `•`/`o`/`▪`) is a one-liner if ever wanted.

## Verification

- Build green every step; final `document.xml` ~26.9KB. Probe: **1 page, 2 tables (both 6×3
  RuleTable), 8×H2 + 1×H1, 52 paragraphs**, 0.75in L/R margins, source line present.
- Rendered docx→pdf (LibreOffice `soffice --headless`) → png (`pdftoppm -r 150`) and eyeballed
  all 4 pages each iteration (user authorized PNG for this task). Confirmed: gray dividers under
  every heading, `•`/`◦` glyphs render correctly (the `◦` is a true circle, not a box), tables
  intact with repeating headers, no blue anywhere. **PNGs deleted (`/tmp/docrender` removed).**
- The doc paginates to 4 pages in LibreOffice; did NOT micro-tune to force 3 pages (LibreOffice
  vs Word paginate differently — the structural fixes are renderer-independent, exact break
  positions are not).

## Files

- **Edited:** `doc_distributed_shipbuilding/pages/rebuy_methodology_explainer.py` (all of the
  above: content, `_rule_table`, `_HRULE` + `_h`, `_list`/`_olist`/`_list_para`, list/heading
  conversions, docstring).
- No other files changed. `docx_core/` untouched; the Award Analysis workbook and
  `compute_jumpball_signals.py` were read-only (deep-dive + fidelity stats), not modified.

## Open / easy follow-ups

- Section numbering deliberately skipped (8-section explainer; dividers carry structure). Manual
  `1 / 2 / 3` on H2s is a cheap add if cross-references are wanted later.
- If the per-heading dividers feel busy, dial back to H1-only or major-section breaks.
- If real Word lists are preferred over the inline glyph system, swap `_list`/`_olist` back to
  `bullets()`/`numbered()` (accepts the native `•`/`o`/`▪`).
