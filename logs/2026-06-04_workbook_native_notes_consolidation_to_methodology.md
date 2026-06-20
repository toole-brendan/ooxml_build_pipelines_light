# 2026-06-04 — Workbook native Excel notes: consolidate to Methodology, anchor on the LAST table column (SRT-style)

## Scope

Reshaped the **native Excel Notes** (`ExcelNote` → legacy yellow hover box) in both
workbooks to match the Sea Range Telemetry (SRT) pipeline's vibe: **far fewer notes, all
on one sheet, anchored on the LAST column of the host table** (the basis/definition column),
each a concise one-to-two-sentence hover. Previously both decks scattered notes across many
model/summary/validation sheets, all on column **C** (the value cell).

Sheet modules only — **no `workbook_core` change** (the `ExcelNote`/`WorksheetSpec(notes=…)`
mechanism is untouched). Workspace is not under git / no backup, so the green rebuild of both
workbooks + the DDG validator are the safety net. Note text was drawn from the canonical
`reserve.context` prose in the latest deck slide specs (per user direction), then tightened.

Before → after: **submarines 18 notes / 8 sheets → 4 notes / 1 sheet**; **DDG 16 notes /
6 sheets → 4 notes / 1 sheet**. Each built workbook now ships **1 comments part** (was 8 / 6).

---

## 1. Submarines — Methodology §1 Definitions, column D (Treatment)

`guide_methodology.py`: replaced the 4 existing C-column definition notes with 4 concise
notes on the **last column D (Treatment)** of the §1 Definitions table, keyed off the captured
`_dn[term]` rows (TAM D7, SAM D8, AP/LLTM D11, SIB D13):

- **TAM** — "Opportunity ceiling, not a forecast: BC base x a strict 35.0% supplier coefficient (non-GFE corpus, naval-nuclear GFE excluded)."
- **SAM** — "Scenario cuts of TAM with no capture / win-probability haircut - SAM, not SOM. Buckets overlap, so shares exceed 100% and must not be summed."
- **AP/LLTM** — "Held at $0: supplier LLTM already sits inside Basic Construction, so adding the ~$44.7B P-10 gross would double-count. Reference only."
- **SIB** — "~$4,252M of SIB capacity / workforce / R&D pass-throughs (mostly BlueForge) - future capacity, not component manufacture. Role, not size, decides. (SIB = MIB in earlier files.)"

Stripped the `notes=[…]` block + `ExcelNote` import + reverted `WorksheetSpec(ws, notes=…)`
→ `WorksheetSpec(ws)` on the 7 other note-bearing sheets: `data_ap_bridge`,
`inputs_assumptions`, `model_sam_build`, `model_tam_build`, `validation_sib_excluded`,
`summary_executive_summary`, `validation_sensitivity`.

## 2. DDG — Methodology §2 tables, column D (parity, 4 notes)

DDG's Methodology has **no Term/Definition/Treatment table**, so the equivalent anchors are the
§2 stream/flow tables, last column **D**:
- **§2c "Two-stream TAM"** (`Stream | Coefficient | Definition`): notes on the **BC stream** (D85)
  and **AP/LLTM stream** (D86) Definition cells — captured via `_bc_row`/`_ap_row` returns.
- **§2b "Base → TAM → SAM"** (`Step | What | How`): notes on the **= TAM** (D77) and **= SAM**
  (D79) rows' How cell — captured as `_bt_r0 + 3` / `_bt_r0 + 5`.

`_market()` now returns its 4 `ExcelNote`s; `render_methodology()` collects builder returns
(`if ret: notes += ret`) and passes them to `WorksheetSpec`. Text:
- **= TAM (D77)** — "Opportunity ceiling, not a forecast: non-GFE, non-MIB new-construction supplier $ away from BIW / Ingalls / GFE sites. ~$573M/yr (BC ~$365M + AP/LLTM ~$208M)."
- **= SAM (D79)** — "Overlapping scenario cuts of TAM, no win-probability haircut - SAM, not SOM. Don't sum; broad = all seven buckets, excludes the ~42.9% unbucketed residual."
- **BC stream (D85)** — "Applied coefficient = 12.5% over the non-GFE BC corpus. Keep distinct: ~87% disclosed (an artifact - $-redacted MYP masters drop out), ~32.8% MYP-corrected outside-yards, 12.5% applied."
- **AP/LLTM stream (D86)** — "Additive stream: in-window CY AP x 80% ship-construction share x 85% supplier coefficient = ~$1.25B (~$208M/yr). Both knobs editable on Inputs; coefficient assumed (no FFATA corpus to measure over)."

Stripped notes from the 6 other DDG sheets: `data_ap_bridge`, `model_tam_build` (3 acc-dict
note blocks + the `_co/_my/_tm` render aggregation; also dropped the now-unused `r_comb`
capture), `model_sam_build` (2 acc-dict note blocks + aggregation), `summary_executive_summary`
(the `notes: list = []` init + `notes += […]` block), `validation_sensitivity`,
`validation_pop_source_audit`.

---

## Verification

| Check | Submarines | DDG |
|---|---|---|
| `build_workbook.py` | green — 20 tabs | green — 24 tabs |
| comments parts in built `.xlsx` | **1** (was 8) | **1** (was 6) |
| native notes count / anchor | 4, all col **D** | 4, all col **D** |
| emitted note refs | D7 / D8 / D11 / D13 (Definitions Treatment) | D77 / D79 / D85 / D86 (§2b How, §2c Definition) |
| note text matches the concise spec | yes (verified from `xl/comments2.xml`) | yes |
| `validate_workbook.py` | (no validator) | 55 parts, **0 xml errors**, **0 error-literal cells**, 24 sheets |
| `ExcelNote` / `notes=` outside `guide_methodology.py` | none | none |

Part-count drop on DDG validate (70 → 55) is expected: removing 6 note-bearing sheets dropped
their comments + VML + per-sheet rels parts; the single Methodology note set added 2 back.

## Files touched

- **Submarines (8):** `guide_methodology.py` (rewrite, notes → col D); notes stripped from
  `data_ap_bridge`, `inputs_assumptions`, `model_sam_build`, `model_tam_build`,
  `validation_sib_excluded`, `summary_executive_summary`, `validation_sensitivity`.
- **DDG (7):** `guide_methodology.py` (add 4 notes on col D, builder-return plumbing); notes
  stripped from `data_ap_bridge`, `model_tam_build`, `model_sam_build`,
  `summary_executive_summary`, `validation_sensitivity`, `validation_pop_source_audit`.
- **Rebuilt:** `projects/submarines/20260601_…_vS.xlsx`, `projects/ddg/20260601_…_vS.xlsx`.
- **Not touched:** `workbook_core/*` (notes mechanism unchanged), the decks, the slide specs,
  README, the SRT pipeline in `~/Downloads/new` (reference only).

## Open items / follow-ups

- **Decks unchanged.** This was a workbook-only pass; deck slide specs supplied the source prose
  but were not edited.
- **Number/value integrity unaffected.** No formula/value/row changed — only `ExcelNote`
  declarations and their `WorksheetSpec` wiring. DDG validate shows 0 error-literal cells.
- **`sheet_guide.md` not amended.** If "native notes go on the last table column of the
  Methodology tab, concise hover only" should become a documented house rule, that is a
  `workbook_core` guide edit (locked-core) — raise separately.
