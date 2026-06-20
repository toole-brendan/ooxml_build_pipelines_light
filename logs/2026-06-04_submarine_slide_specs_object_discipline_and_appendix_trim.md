# 2026-06-04 — Submarine slide specs: object-count + border discipline pass, appendix trim, and matching deck-module removal

## Scope

A two-part request against the **submarine** deck (`projects/submarines/deck`):

1. **Rewrite the object layer of every submarine slide spec** (`deck/slide_specs/*.md`) to a
   detailed object-discipline standard: make every multi-object helper explicit, fix
   filled-object borders, give each slide a distinct object grammar, and apply a per-slide
   object-set target supplied by the user. Plus trim the appendix set (delete four appendix
   specs, fold one into a body slide).
2. **Remove the four cut appendices from the professional deck for real** — delete their slide
   **modules** and unregister them — then rebuild.

Starting corpus: **26** submarine specs (17 body + 9 appendix), all in the SlideSpec format
authored across the 2026-06-03 sessions. The user directed working from the *current state of the
files* rather than the format/guide docs. Workspace is **not** under git and has **no backup**, so
the irreversible calls were confirmed up front (see Decisions) and the deck rebuild is the safety
net for the code changes (specs are not on any build path; the deck modules are).

---

## 0. Decisions carried in from the user (asked before touching anything)

Three irreversible/ambiguous calls were locked via an in-session question (everything else in the
brief was unambiguous and executed directly):

- **Cut appendices A2 (Model Map & Figure Register) and A9 (QA Reconciliation): delete the spec
  files** outright.
- **A8 (SIB Exclusion Detail): fold into S16** (`sib_exclusion`) and delete A8.
- **A7 (Data Limitations & Unseen Layer): cut** (the body S17 `data_limits` already carries the
  ledger); update S17's cross-reference.

This leaves exactly the user's recommended professional appendix set: **A1 Definitions & Scope,
A3 AP & LLTM Detail, A4 Coefficient Sensitivity, A5 SAM Bucket Crosswalk, A6 Top 25 Visible
Suppliers.** A follow-up message then approved removing the four backing **modules** too (part 2).

## 1. Global rules applied to every edited spec

1. **Object-count discipline.** No vague multi-object helper. Any "N cards via a helper,"
   connector group, tick set, chip strip, or chart-annotation set is now either N individual
   `element_inventory` + `shapes` entries, or **one compound object** whose `shapes` entry
   enumerates the N children and whose `element_inventory.content` states the exact count.
2. **Line-color discipline.** No `line_color: null` on a **filled** object unless intentionally
   borderless (stated in `meaning`). Focal/hero/answer/warning blocks → `line_color: BLACK` +
   `line_width: 19050` (1.5pt); secondary panels/cards/chips/chart-side tables → `GRAY_3`.
3. **Distinct grammar per slide** (encoded in the per-slide targets below).
4. **Kept every `qa:` block;** only the QA *appendix slide* was removed.

Preserved verbatim in every file: `meta` (bar noted cross-ref drops), `chrome`, `story`, the whole
`commentary.reserve`, `data_and_calculations`, and `qa` — no numbers, citations, or reserve prose
changed.

## 2. Per-slide object updates (17 body slides)

| Slide spec | Object-layer change |
|---|---|
| `market_primer` | System map kept; counted-supplier node made the focal object (BLACK + 1.5pt); four excluded lanes thinned to **tags** (not equal-weight cards); connector group states its **5 enumerated arrows**. |
| `sizing_boundary` | Three boundary cards + warning rail, **no arrows/map** (distinct from S2); exact borders (included BLUE_1+GRAY_3, excluded GRAY_2+GRAY_3, context GRAY_1+GRAY_3, **warning rail BLUE_5+BLACK 1.5pt**). |
| `executive_summary` | KPI answer slide; the **two hero KPI cards are the only focal family** (BLACK+1.5pt); four support cards light + GRAY_3; no chart/funnel/Venn. |
| `demand_backdrop` | Five **tick glyphs** made real objects; three theme rails converted to **no-fill rails** (de-card the grid); five milestone cards GRAY_3. |
| `methodology` | Seven step **cards → numbered dot/chevron rail** (`step_dots` + `step_labels` compound objects, 7 each); formula box is the focal object. |
| `basic_construction` | FY2024/FY2027 peak notes **reclassified `callout` → `chart_annotation`** (leader lines); no-fill rail kept. |
| `tam_bridge` | Added an enumerated **4-connector `bridge_bus`** + a **divide-by-6 annotation**; the average-annual card is the only dark hero. |
| `annual_cadence` | Confirmed chart + two peak chips + no-fill note, **no right rail** (distinct from S7). |
| `coefficient_evidence` | **2×3 evidence-card grid → one compact native evidence table** (de-dupes from A4); kept the 3-bar ladder + no-fill read/guardrail. |
| `ap_and_lltm` | Large focal **$0 additive-base warning card** (only filled card); $0 endpoint carried as a **chart_annotation**. |
| `work_type_taxonomy` | Seven bucket cards **enumerated** in the compound grid; residual is the single focal (BLACK+1.5pt). |
| `bucket_tam` | Ranked bar + gray residual strip (focal) + no-fill note; **no rail/table** (simpler than S14/S15). |
| `sam_scenarios` | **Collapsed the separate guardrail strip + note into one combined caveat** (chart + rail + one caveat). |
| `visible_suppliers` | Confirmed chart + chart-side evidence table + floor note; no logos. |
| `sib_exclusion` | **Converted ranked bar → gray three-row exclusion ledger (native table) + focal treatment card**; folded A8's entity/rationale rows + SIB/MIB note + two reserve points (see §4). |
| `data_limits` | Pipe-separated guardrail string **split into four real chip objects**; filled panels given GRAY_3 borders. |
| `implications` | Confirmed scorecard table + no-fill closing note, top-3 rows highlighted. |

## 3. Appendix trim (9 → 5)

- **Deleted specs:** `appendix_model_map_and_figure_register.md` (A2),
  `appendix_qa_reconciliation.md` (A9), `appendix_sib_exclusion_detail.md` (A8),
  `appendix_data_limitations_and_unseen_layer.md` (A7).
- **Kept + edited:** A1 (border tightened, dropped A2 ref), A3 (simplified — stays a native
  reconciliation table, not a second waterfall; warning card focal), **A4 de-carded** (six
  evidence cards → one compact corpus-controls table, mirroring the S10 change), A5
  (`table_skin: dark → light` so the header stops dominating), A6 (evidence chips demoted to
  GRAY_3, dropped A8 ref).

## 4. S16 conversion + A8 fold (detail)

`sib_exclusion` (S16) was the one structural conversion. `charts: []`; added a `house_table`
exclusion ledger (BlueForge $4,173.3M / TMG $77.0M / IALR $1.5M / total $4,251.8M) with a
**Rationale** column and **gray** exclusion fills (GRAY_5 header, GRAY_2/GRAY_1 rows) — never the
counted-TAM/SAM blues. The treatment card is the dominant focal object. `archetype` →
`exclusion_ledger_plus_treatment_card`; `related_appendix: []`; `data_and_calculations.used_in`
repointed chart → table; engine_checks swapped the chart-rId line for a table-fit line; two A8
reserve points appended ("would distort the model — FY2024 BlueForge ~$2.7B ≈ 42% of Columbia BC";
"role, not size, decides"). A stale "three gray bars" phrase in the reserve density guidance was
corrected to "gray three-row exclusion ledger."

## 5. Cross-reference cleanups (after the deletions)

Dropped every reference to the deleted appendices so no spec points at a gone file: A1
`related_appendix` (−A2), A6 `related_appendix` + reserve prose (−A8, now points readers to the
S16 slide), S17 `data_limits` `related_appendix` (−A7), S16 (−A8, self-folded). Sweep confirms
**zero** residual `subs-a2/a7/a8/a9` or deleted-module-name references (only intentional
explanatory comments in S16).

## 6. Execution method

- The 22 spec edits were fanned out to **8 parallel subagents** clustered by section, each given
  the four global rules + its per-file targets + a hard "preserve reserve/data/qa, keep all id
  references mutually consistent" contract.
- Reconciled **dangling `reserve`/`data` bookkeeping** the agents correctly left untouched (the
  preserved blocks referenced regions/shape-ids that the object-layer edits had removed/renamed):
  methodology `step_N` safe_containers → `process_rail` + keep-list + `used_in: step_3_card →
  step_dots`; sam_scenarios `note_strip → caveat_strip`; coefficient_evidence `card_* →
  evidence_table`; tam_bridge keep-list completed to e1–e9; data_limits `used_in: guardrail_1 →
  guardrail_chips`.
- Fixed one **YAML break** an agent introduced in `ap_and_lltm` (partial-quote inside a flow
  mapping: `content: "$0 additive base" endpoint label…` → fully quoted).

## 7. Part 2 — deck-module removal + registry unregister + rebuild

The user then approved removing the four backing modules (the slides still built until then).

- Confirmed only `slides/__init__.py` referenced the four modules (no cross-imports).
- Removed their imports + `SLIDE_RENDERS` tuples and updated the registry docstring (appendix is
  now A1, A3–A6; notes A2/A7/A8/A9 removed and A8 folded into S16).
- Deleted the four module files
  (`appendix_{model_map_and_figure_register,qa_reconciliation,sib_exclusion_detail,data_limitations_and_unseen_layer}.py`).
- **Rebuilt the deck green.**

---

## Verification

| Check | Result |
|---|---|
| All 22 specs parse as YAML | pass (after the `ap_and_lltm` quote fix) |
| Cross-ref integrity (region / element / `safe_container` / `used_in` / `keep` / connector `from_to`) | every reference resolves in all 22 |
| Filled object with a null border | **none** |
| `qa:` block present | all 22 |
| Focal-hero (`line_width: 19050`) counts | sensible — executive_summary 2; chart/table-dominant slides 0 |
| Deleted-appendix references remaining | none (only S16 explanatory comments) |
| Submarine deck build | **exit 0 — 27 slides, 9 charts** (was 31; −4 appendices) |
| Registry import + counts | clean; 27 `SLIDE_RENDERS`, **5 appendix** entries |
| Stale probe/pyc artifacts for removed modules | none |

## Files touched

- **Deleted (specs):** `slide_specs/appendix_{model_map_and_figure_register, qa_reconciliation,
  sib_exclusion_detail, data_limitations_and_unseen_layer}.md`.
- **Edited (specs, 22):** the 17 body specs + the 5 kept appendix specs (`appendix_{definitions_and_scope,
  ap_and_lltm_detail, coefficient_sensitivity, sam_bucket_crosswalk, top_25_visible_suppliers}.md`).
- **Deleted (modules):** the four matching `deck_submarines/slides/appendix_*.py`.
- **Edited (code):** `deck_submarines/slides/__init__.py` (imports, `SLIDE_RENDERS`, docstring).
- **Rebuilt:** `projects/submarines/20260602_Distributed Shipbuilding Submarines_vS.pptx`.
- **Not touched:** `deck_core/*`, the DDG deck, the workbook, `docs/spec_format/*`, the README.

## Open items / follow-ups

- **Appendix letters left non-contiguous** (A1, A3, A4, A5, A6 — gaps where A2/A7/A8/A9 were).
  Renumbering to A1–A5 would mean editing each remaining module's internals + specs; deliberately
  **not** done (scope). Offered to renumber if wanted.
- **Reserve `density_modes` semantics** in a few rewritten specs (e.g. tam_bridge keep-list, the
  `safe_container` remaps) are now valid references but were updated mechanically; the prose
  *meaning* of those density tiers wasn't re-authored against the new object sets — fine for
  build, worth a human pass if the density mechanism is exercised.
- **DDG deck untouched.** The same object-discipline pass + appendix trim has not been applied to
  the DDG specs/modules; a parallel pass would be a separate task.
- **No git / no backup** — all deletions were direct; the green deck rebuild is the only safety net.
