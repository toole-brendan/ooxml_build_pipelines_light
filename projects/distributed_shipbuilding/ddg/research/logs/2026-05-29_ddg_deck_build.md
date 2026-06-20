# Session Log — destroyer_outsourced_work — 2026-05-29 (deck build: ddg_pptx)

**Handoff doc for the next AI agent.** This session built the destroyer deck as a
new, self-contained raw-OOXML pipeline (`ddg_pptx/`), realizing `DECK_SPEC_v3.md`
in the polished aesthetic of `deck_v2/` (minus its dark hero bands), driven by the
workbook's computed source-of-truth numbers. The deck builds to a valid 16-slide
`.pptx` that opens in PowerPoint without a repair prompt.

Read prior logs for context:
1. `logs/2026-05-28_methodology_overhaul.md` (headline framing, funnel, scope cleanup, spec docs)
2. This file.

---

## 1. TL;DR — what exists now

- **New pipeline:** `ddg_pptx/` — a verbatim copy of the `sub_pptx/` raw-OOXML engine,
  renamed to the **`deck_ddg`** package. Same "granular" engine: 4 public primitives
  (`slide`, `page_number`, `cover_layout`, `section_divider_layout`), each slide
  composed from **file-private helpers** (no shared `_helpers.py`).
- **Deliverable:** `ddg_pptx/20260528_Distributed Shipbuilding Destroyers_vS.pptx`
  — **16 slides**, builds clean, XML well-formed, opens in PowerPoint (repair bug fixed, §6).
- **Build:** `cd ddg_pptx && python3 build_deck.py` (works on system Python 3.9 — all
  modules carry `from __future__ import annotations`).
- **Aesthetic:** ported `deck_v2`'s component idioms (white body, light cards,
  flow arrows, range/dumbbell + stacked-bar charts, split takeaway/guardrail bands,
  snapshot strips) **minus the full-width dark BLUE_5 hero/emphasis bands** the user
  dislikes. Emphasis is carried by **light fills (BLUE_1/BLUE_2/GRAY) + heavy borders
  + bold dark type on white**; dark (BLUE_4/5) is reserved for small caps only.
- **Numbers:** the workbook is the source of truth and **supersedes the spec's
  back-of-envelope 87/33/78** (see [[project_ddg_workbook]] memory and §3).

---

## 2. How the build is wired

- `ddg_pptx/build_deck.py` → `from deck_ddg.lib import build`.
- `ddg_pptx/deck_ddg/lib.py` — orchestrator. `N_SLIDES_OUT = 16`; the
  `slide_module_renders` list inside `build()` is the registry (slot → module →
  `mod.render(page_num=…, total_pages=…)`). Every slide module (cover, body, divider)
  exposes `render(*, page_num, total_pages) -> str`. Cover/divider modules also
  declare `LAYOUT = "slideLayout1"`/`"slideLayout2"`; body slides default to
  `slideLayout4`.
- `deck_ddg/primitives.py` + `charts.py` — copied verbatim from `deck_sub` (generic;
  only the package name changed). `charts.py` is unused so far (no native charts in
  this deck — all visuals are hand-built `<p:sp>` shapes).
- Infrastructure copied verbatim from `sub_pptx`: `_extracted/` (Saronic
  master/layouts/theme/labelinfo), `assets_deck/` (chrome media), `tools/slide_probe.py`,
  OOXML cheat-sheet docs.
- To add/move a slide: edit the import block + the `slide_module_renders` list +
  `N_SLIDES_OUT` in `lib.py`. (There is an `assert len(...) == N_SLIDES_OUT`.)

---

## 3. The numbers used (workbook source of truth)

These came from the finished workbook (`destroyer_outsourced_construction_workbook.xlsx`,
`ddg_workbook/`) and **replace the spec/methodology 87/33/78**:

| Figure | Value | Role on the deck |
|---|---|---|
| Funnel cost-share, outsourced % of total ship cost (FY16-27 avg, Mid) | **~58%** (58.3) | supporting headline |
| MYP-corrected outside-yards POP | **46.8%** | honest geography (lens 3) |
| Disclosed-corpus outside-yards POP | **84.8%** | redaction artifact — **never headline** |
| Entrant SAM (yard-side first tier, modeled) | **~$1.8B/yr** (band $1.4–2.2B) | **deck headline** |
| FFATA-visible floor | **~$286M/yr** (~15% of SAM) | the floor |
| GFE layer | **~$5B/yr** (~33% of ship cost) | TAM context, out of SAM |
| In-scope FFATA-visible (cumulative) | **$11.2B / 73 PIIDs / 1,554 vendors** | cleaned scope |
| BIW de-capped prime obligations | **$13.6B** | two-yard scale |
| FFATA filed ÷ prime: BIW vs Ingalls | **~1.3% vs ~21%** | under-reporting tell |
| FY23-27 MYP masters | **~$14.58B** (BIW ~$6.4B, Ingalls ~$8.18B) | folded back for 46.8% |
| FY24 funnel | TSE $5.49B → BC $3.32B/60.5%; GFE $1.81B/32.9%; Plans $83M/1.5%; Other $280M/5.1% | cost-funnel slide |

**Framing choice:** the deck leads with the **entrant SAM (~$1.8B/yr yard-side)** and
frames **GFE as TAM context, not the wedge** (sole-source Navy-prime at named sites) —
deck_v2's sharper thesis — while honoring all `METHODOLOGY.md §12` guardrails (never
headline 84.8%; three numbers travel together; band not point; two yards; FFATA is the floor).

---

## 4. The 16-slide arc

1. Cover (slideLayout1) — "DDG-51 Outsourced Construction"
2. Executive summary — SAM ~$1.8B; SAM/TAM/wedge cards; WHY-THIS-HOLDS + GEOGRAPHY guardrail bands
3. Divider: Overview
4. Scope and the two yards — snapshot strip, BIW/Ingalls cards, GFE-primes card, out-of-scope strip
5. What "outsourced" means — four lens cards (headline lenses 2 and 3 emphasized) + reporting-rule band
6. Cost funnel — vertical light-band funnel + flow arrows + TAKEAWAY split band
7. Divider: Sizing
8. The GFE layer — Aegis/SPY-6 megabuckets + small-multiples + guardrail
9. Where the work happens (POP) — two stacked bars, 84.8 → 46.8 MYP fold-back, context chips, guardrail
10. The visibility gap (FFATA) — floor-vs-flow two bars, cleaned top-vendors card, cleaned-scope band
11. Hidden yard-side layer — dumbbell/range chart (Method 1 / Method 2 / Combined vs FFATA floor) + READ band
12. Two yards compared — BIW vs Ingalls compare table (1.3% vs 21% row emphasized) + entrant-question band
13. Divider: Outlook
14. Direction of travel — 10%→50% growth callout + 3 driver cards + guardrail
15. Where to play — SAM/TAM/wedge strip + yard-side vs GFE channels + bottom line + capability-heat-map placeholder
16. Method and sources — three measurement-stream cards + caveats + cleaned-scope band

Section dividers use the Saronic divider layout (intentionally dark — that is the
template's divider, not a content-slide hero band).

---

## 5. Aesthetic conventions (carry these)

- **White body background.** Focal emphasis = light fill (usually BLUE_1 or BLUE_2) +
  **heavy 1.5pt border** (BLUE_5 or BLACK) + big bold dark text. **No full-width dark
  hero/emphasis bands on content slides** (the user explicitly dislikes them).
- Recurring file-private idioms (re-implemented per module, never shared): `_box`
  (the core filled/transparent text rect — the deck_v2 `s.text()` equivalent), `_para`/
  `_run`/`_para_runs`, `_card`, `_split_band` (small dark cap + light GRAY_1 message),
  `_label`, `_arrow_down`/`_arrow_right` (connector flow cues), `_bar`/`_seg`/
  `_range_row` (chart shapes).
- Locked chrome per `body_template.py`: breadcrumb (id 2), title (id 3, "Topic | Finding"),
  Preliminary chip (id 4), sources line (id 9999), `page_number()` (id 4500). Breadcrumb
  sections: **Overview / Sizing / Outlook / Appendix**.
- Style rules honored: Arial everywhere; no em dashes; no `/ + × →` as separators;
  `$XXB`/`%`/`~` kept.

---

## 6. The PowerPoint "repair" bug (fixed)

Symptom: PowerPoint showed a repair dialog on open (LibreOffice opened it fine — it is
more lenient). Two PowerPoint-strict validity violations:

1. **Empty `<p:txBody>`** (no `<a:p>`) on graphic-only shapes (bars, rules, frames) —
   PowerPoint requires ≥1 paragraph per text body. Hit slides 9, 10, 11, 14.
2. **Duplicate `<p:cNvPr id>` within a slide** — slide 9 (fold-arrow vs a bar frame at
   id 190) and slide 11 (an axis label vs the READ band at id 181). IDs must be unique
   per slide (cross-slide reuse is fine).

Fixes:
- Hardened every module's `_box` to emit `<a:p/>` when there is no text:
  `{("".join(paragraphs) or "<a:p/>")}`. This makes the bug unrecurrable in any module.
- Renumbered the two colliding IDs (pop_geography 190/191 → 230/231; hidden_yard_layer
  axis-label base 161 → 200).

Validation (all green): `zipfile.testzip()` OK; every XML part parses; a per-slide scan
shows **0 empty text bodies and 0 duplicate IDs** across all 16 slides; all 16 render
via `soffice --convert-to pdf` + `pdftoppm`.

**Diagnostic to re-run after edits** (catches both classes):
```python
import zipfile, re
z = zipfile.ZipFile("ddg_pptx/20260528_Distributed Shipbuilding Destroyers_vS.pptx")
for n in sorted(x for x in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", x)):
    xml = z.read(n).decode()
    empties = sum(1 for m in re.finditer(r"<p:txBody>(.*?)</p:txBody>", xml, re.S) if "<a:p" not in m.group(1))
    ids = re.findall(r'<p:cNvPr id="(\d+)"', xml)
    dups = {i for i in ids if ids.count(i) > 1}
    if empties or dups: print(n, empties, dups)
```

---

## 7. Files created / modified

**Created (`ddg_pptx/`):** `build_deck.py`; `deck_ddg/{__init__,lib,primitives,charts}.py`;
`deck_ddg/slides/{__init__,body_template,cover,executive_answer,div_overview,scope,
denominators,cost_funnel,div_sizing,gfe_layer,pop_geography,visibility_gap,
hidden_yard_layer,two_yards,div_outlook,direction_of_travel,where_to_play,methodology}.py`;
copied `_extracted/`, `assets_deck/`, `tools/`, OOXML docs; output `.pptx`; this log.

**Untouched references:** `DECK_SPEC_v3.md`, `METHODOLOGY.md`, `deck_v2/` (the aesthetic
reference — do not edit), `sub_pptx/`, `deck/`, all data pulls and `extracted/`.

**Stray build artifact:** building `deck_v2` for study wrote
`/Users/brendantoole/projects2/20260526_DDG Outsourced Construction_v2.pptx` (use
`python3.12`, not 3.9 — deck_v2 lacks future imports). Safe to delete.

---

## 8. Things to NOT do

- **Don't add a shared `_helpers.py` / external helper module.** Helpers are file-private
  per slide by design (user directive + `body_template.py` docstring). Duplication is intended.
- **Don't reintroduce full-width dark BLUE_5 hero/emphasis bands** on content slides.
- **Don't leave an empty `<p:txBody>`** (no `<a:p>`) or **reuse a shape id within a slide** —
  both trigger PowerPoint repair. The `_box` guard handles the first; keep id ranges disjoint.
- **Don't headline the 84.8% POP** (redaction artifact); keep the three numbers traveling
  together (84.8 artifact / 46.8 corrected / ~58 funnel).
- **Don't edit `deck_v2/`** — it is the reference deck.
- **Don't build deck_v2 with Python 3.9** (needs 3.10+); the `ddg_pptx` deck builds on 3.9.

---

## 9. Open items / next steps (in order of value)

1. **Swap modeled/placeholder figures for exact workbook cells** where finer numbers exist
   — per-FY funnel decomposition, GFE annual $, per-yard yard-side ($1.13B / $0.69B are
   METHODOLOGY §9 modeled). The slide docstrings note which numbers are modeled.
2. **Slide 15 (Where to play):** add the capability-scored addressability heat map once
   the **entrant's capability profile** is supplied (currently a placeholder note).
3. **Optional cosmetic:** the bottom-right page number renders twice — `page_number()`
   "N / total" plus the slide master's bare `slidenum` field. This is inherited from the
   reference pipeline (sub deck does it too). One-line fix: remove the `sldNum` placeholder
   from `_extracted/ppt/slideMasters/slideMaster1.xml`.
4. **Optional:** drop the DDG subject photos in `image_assets/ddg_subject_photos/` onto the
   cover / GFE slides (lib.py auto-copies an `images/` folder into `ppt/media/`; wire a
   `<p:pic>` + per-slide rel).
5. Bump the output filename date (`20260528_…`) when re-issuing.
6. Regenerate `tools/slide_probe.py` inventories if geometry docs are wanted (not run this session).

---

## 10. Quick orientation for next agent

- **Build:** `cd ddg_pptx && python3 build_deck.py` → `20260528_Distributed Shipbuilding Destroyers_vS.pptx`.
- **Render to images:** `soffice --headless --convert-to pdf --outdir /tmp/x "<pptx>"` then
  `pdftoppm -png -r 110 /tmp/x/*.pdf /tmp/x/s`.
- **Registry:** `deck_ddg/lib.py` (`N_SLIDES_OUT`, `slide_module_renders`).
- **Slides:** `deck_ddg/slides/*.py` — each self-contained (file-private helpers + inline chrome).
- **Aesthetic reference:** `deck_v2/` (build with `python3.12`); **style/numbers truth:**
  `METHODOLOGY.md` + the workbook ([[project_ddg_workbook]]).
- **"Why does it look like deck_v2 but lighter?"** → deliberate: deck_v2 polish minus the
  dark hero bands (§5).
- **"Repair dialog again?"** → run the §6 diagnostic; almost always an empty txBody or a
  duplicate per-slide shape id.

## 11. Memory
No new cross-session memory written this session. Relevant existing memories:
[[feedback_deck_prose_style]] (transparent prose, fills only for emphasis) and
[[project_ddg_workbook]] (the 58.3/46.8/84.8 source-of-truth numbers).
