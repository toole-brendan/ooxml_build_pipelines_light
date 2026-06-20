# 2026-06-07 — Consolidated deck: three new appendix methodology slides + two polish passes

## Scope

Built **three new appendix slide modules** for the consolidated deck
(`projects/consolidated/deck/deck_consolidated/slides`) from the `alternative_v3` methodology specs,
registered them in narrative order in the appendix tail, then ran **two surgical polish passes** across the
four equation-bearing appendix slides. The deck builds **green at 29 slides / 4 charts** throughout. Two
labeled snapshot copies of the five appendix modules were dropped at the projects3 root
(`updated_slides/`, `updated2_slides/`).

Standing constraint honored all session: **internal M-series step codes (M1–M5) never appear in visible
slide copy** — reworded to descriptive references ("the budget-base step", "the supplier-share step", "the
allocation step", "supplier-share conversion"). See memory `no-m-series-codes-in-visible-slide-copy` and
`deck-rendered-text-conventions`.

## What was built

### Three new slide modules (specs → modules)

- **`appendix_tam_budget_base_scope_gates.py`** (spec `appendix_tam_budget_base_scope_gates_spec.md`,
  "TAM Budget Base"). Table-left / program-rail-right "retained-base proof": caption + full-width output
  chip; one native retained-base ledger (5 steps, dark `263746` header, AP/LLTM row `E2E9EF`, handoff row
  `F2F2F2`); a stacked DDG (`6E91B1`) / submarine (`3D5972`) treatment rail with a commentary mini-block;
  and a full-width AP/LLTM incrementality strip with two arithmetic chains (DDG additive example, submarine
  zero-base bridge).
- **`appendix_supplier_share_pop_conversion.py`** (spec `appendix_supplier_share_pop_conversion_spec.md`,
  "Supplier-Share Method"). Calculation-machine: definition strip + right-aligned workbook-term chip; a POP
  "formula machine" (5 cards joined by `× = ÷ =`); two program lanes (DDG additive, submarine
  reference-only) each = ribbon + white body of two formula rows + colored total + evidence chips; one dark
  combined fixed-TAM output card; two no-fill commentary findings. The DDG lane carries a `+` between its
  two rows; submarine has a gray reference row + italic subnote and no `+`.
- **`appendix_sam_classification_field_audit.py`** (spec `appendix_sam_classification_field_audit_spec.md`,
  "SAM Classifier"). Three-zone field-audit console: caption + light output chip; a 7-node rounded-pill
  evidence spine joined by right-facing arrows (+ a connector note under the UEI→entity arrow); a middle
  field-audit zone = native classification ledger (7 stages) on the left + a 9-row "first clean match wins"
  precedence ladder and an 8-chip work-type cluster on the right; a bottom zone = DDG/submarine
  evidence-volume cards + a shape-built examples board, with two commentary findings above a thin rule.

Registration in `slides/__init__.py` — appendix tail order is now: methodology roadmap → **TAM budget base**
→ **supplier-share conversion** → **SAM classifier** → SAM allocation. (Each new slide was inserted
"immediately after the one just created", per the three successive requests.)

### Polish pass 1 (four files; roadmap left alone)

- **Removed gray operator-chip boxes** — `_op` / `_operator_chip` / `_math_operator` in supplier-share,
  allocation, and TAM-budget now return only the centered black `mathMultiply`/`mathEqual`/`mathDivide`/
  `mathPlus`/`mathMinus` AutoShape (per `~/projects2/ooxml_arithmetic_shapes_conventions.md`). `chip_id` is
  retained (`_ = chip_id`) so call sites / id spacing don't move.
- **Classifier precedence ladder** — folded the number into an inline bold `"N. "` run; deleted the
  separate `PrecedenceBadge` square + `_BADGE_SZ`.
- **TAM-budget rail commentary** — `_ZONE_B = _STRIP_Y - 130_000` (was −66k) + shorter copy → the
  commentary→strip gap went 66k → 130k (no more crowding).
- Tightened two output-chip vertical insets; allocation scenario-card breathing room (`_GAP_VAL` 150→100,
  cut/broad insets); classifier spine pill height 392k→… (later 410k).
- Removed now-unused imports (`INSETS_CARD` in allocation; `GRAY_2` + `INSETS_CARD` in TAM-budget).

### Polish pass 2 (four files) + a mid-pass correction

- **Display rounding** — noisy multi-decimal `$B` → one decimal (`$1.833B`→`$1.8B`, `$6.027B`→`$6.0B`,
  `$23.28B`→`$23.3B`), percentages → whole (`12.546%`→`13%`, `48.486%`→`48%`).
  **CORRECTION mid-pass:** user reversed the "table to $B" idea — **values already in `$M` stay in `$M`**.
  Reverted the over-conversions: allocation table back to `$M` (`$1,263M`, `$93M`, `$596M`, …); `$573M`,
  `$381M`, `$664.8M` preserved. Counts (`22,867`, `154`, `929`) and `$0` sentinels untouched.
- **Broad SAM card breathing room** — `ScenarioBroad` 540k→640k, insets 40k→80k. Side effect: squeezed two
  cut cards into overflow; fixed by compacting the cut cards (value 12.5pt→11pt, insets 38k→22k) so **all
  four cut sublines stay intact** and the broad card keeps its room.
- **Classifier bottom-rule clearance** — added `_BOTTOM_RULE_CLEARANCE = 40_000`; the rule now sits with
  **exactly 40k above and 40k below**. That shortened the bottom zone, which would clip the 5-line evidence
  cards → set evidence body to 7.5pt (in-spec) with 100%-spacing / no space_after so all 5 stats still fit
  and pin to `BODY_B`.
- **Em-dash hygiene** — every visible `—` separator → colon across the four files (ribbons, rail/precedence
  headers, ledger labels, work-type header, strip title, allocation table label, submarine subnote). Final
  sweep: **0 em dashes** in rendered text on slides 26–29.
- **Black equation cards** were applied (white→black fill, black→white text on equation text cards only,
  operators/totals/output/broad/cut untouched) — **then reverted in a follow-up** at the user's request
  back to white fill / black text (submarine reference row restored to `F2F2F2`/`GRAY_1`). Net: equation
  cards are back to their original colors.

## Verification

`build_deck.py` → **29 slides, 4 charts, green** after every change. QA via
`deck_core/slide_probe.py <pptx> --slide N --table-fit --text-estimate`:

- **No content overflow > 0.02 in** on slides 26–29 after each pass (only sub-0.005 in sub-pixel flags on
  the intentionally-empty operator AutoShapes and the locked-chrome breadcrumb remain).
- Zone geometry collision-checked from the probe JSON each time: ledgers clear their field-audit zones,
  rails/work-type chips close at their boundaries, commentary clears the bottom zone, bottom objects pin to
  `BODY_B`.
- Final fill audit: equation cards `FFFFFF` (+ submarine ref row `F2F2F2`) with `000000` text; non-equation
  semantic fills intact (`263746` / `6E91B1` / `3D5972` / `E2E9EF` / `B6C8D8` / `D9D9D9`).
- Final M-code sweep + em-dash sweep of rendered `<a:t>`: clean on 26–29.

## Gotchas hit this session

- **Dense canvas, repeatedly.** All three slides are at the limit of one 16:9 body. The classifier (7-row
  table + 9-row ladder + 8 chips + 2 evidence cards + examples board + commentary) needed hard cell-fragment
  trimming — the ledger first rendered at **2.94 in** vs a ~2.3 in zone (estimate_row_heights) and had to be
  cut to ~1-line fragments; the rail/table balance and the bottom region were then tuned by probe.
- **Coupled geometry.** Growing the broad card directly shrinks the allocation cut cards (the cut height is
  derived to fill the exhibit zone); the classifier clearance edit directly shrinks the evidence-card body.
  Both required a compensating change (cut compaction; 7.5pt evidence) — neither was a one-line edit.
- **`estimate_row_heights` honesty.** Native tables use the local `_tc` helper forcing **100% line spacing**
  so authored row heights match the estimator (house 115% cells render ~15% taller — memory
  `ooxml-house-table-rowheight-gotcha`). The probe flags the header row as "short" only because its
  `min_row_h` floor (274,320) exceeds a compact 1-line caps header — cosmetic.
- **Probe false-positives** to ignore: empty operator AutoShapes report a phantom endParaRPr line height;
  the locked breadcrumb chrome always reads slightly over its short placeholder. Filter `chrome_role` and
  empty text in the overflow scan.
- **`paragraph()` `space_after` is points (1/100 pt), not EMU** — small contributor to box height, easy to
  over-budget against if mistaken for EMU.

## Current state / how to resume

- **Green, 29 slides.** Three new appendix modules registered and probe-clean; allocation slide carries the
  pass-1/pass-2 polish (bare operators, rounded `$B`/`$M`-preserved values, broad-card room, white equation
  cards).
- **Snapshot copies at projects3 root** (verbatim copies of the 5 appendix modules incl. the untouched
  roadmap; still wired to `deck_core`, so reference snapshots — not runnable from those folders):
  - `~/projects3/updated_slides/updated_appendix_*.py` (state after polish pass 1 + start of pass 2)
  - `~/projects3/updated2_slides/updated2_appendix_*.py` (latest — after the black-card revert)
- Roadmap (`appendix_methodology_roadmap.py`) deliberately **untouched** — its inline-bold-operator formula
  treatment was already the clean pattern.

```
cd projects/consolidated/deck
/usr/bin/python3 build_deck.py        # -> 29 slides, 4 charts
cd ../../..
/usr/bin/python3 deck_core/slide_probe.py \
    "projects/consolidated/20260605_Distributed Shipbuilding Consolidated_vS.pptx" \
    --slide 28 --table-fit --text-estimate --out-dir /tmp/probe   # 26=TAM base 27=supplier 28=classifier 29=allocation
```
