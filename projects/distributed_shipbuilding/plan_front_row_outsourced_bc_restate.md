# Plan — Front-row Outsourced BC restate + new per-FY work-type slide

2026-06-10. Source of intent: the manager-edited draft
`projects/consolidated/20260605_Defense Demand Drivers New Construction_vDraft.pptx`
(slides 2-5, with purple note boxes and P1-P4 priority chips). Base of work: the
current deck/workbook sources (which build to `..._v1.0.pptx`) — all existing module
changes are kept; the vDraft is a markup layer on top of them, not a replacement.

Everything the manager flagged is downstream of the 2026-06-10 program-workbook
restates (announced-POP coefficients, P-10 EOQ AP/LLTM stream, class-vintage subs
coefficients, gated FY22-25 work-type vectors). This plan restates the consolidated
deliverables to those numbers, reworks the annual-TAM slide to his new format, and
adds one new slide (work-type mix by FY).

## Decisions already made (user, 2026-06-10)

1. **"Unassigned" is not a new concept** — it is the residual. Keep one hatched
   "Residual" segment/legend entry everywhere; do not add a second cap.
2. **Slide-4 (annual TAM) outline columns**: filled portion = outsourced BC TAM;
   the no-fill outlined extension above = the rest of the **penetration denominator**
   (program total ship spend, constant FY26 $, incl. OBBBA gross) that is not
   outsourced. Confirmed by the manager's own FY22-23 mock values (sub 11.0/11.1,
   DDG 4.0/4.5 ≈ per-FY total-spend denominators).
3. **Historical vs forecast banding**: FY2022-FY2026 = blue/"Historical" (FY26 is
   enacted + OBBBA); FY2027 onward = gray/"Forecasted" (FY27 is the PB request).
   Boxed band labels per the mock ("Historical" over blue, "Forecasted" over gray).
4. **Front-row slide order = the vDraft order**: cover → walk → work type
   (cumulative) → annual TAM → NEW work-type-by-FY → Market Landscape divider.
   (Current registry has annual TAM before work type — swap, then insert the new
   module after s11a.)
5. **New slide FY span = FY2022-FY2025 only** (the measured gated-vector years; no
   assumed-vector columns).
6. **Outlook lo/hi redefinition (program workbooks)**: lower bound = FY22-25
   average penetration (ratio of sums); upper bound = a sourced "USN/market intent"
   assumption. **User will supply the source/number** — likely operationalized off
   HII's stated intent to increase outsourced manhours ~30%.

## Open dependency (blocks final numbers, not the build)

**The upper-bound intent number.** Proposed mechanic, to implement now:

- New Inputs assumption (both program workbooks): "Outsourcing intent uplift vs
  FY22-25 average" = **0.30** (decimal dv), with a gray `S_NOTE` citation slot
  reading "HII stated intent to grow outsourced manhours ~30% — citation TBD".
- Outlook §3: upper bound = FY22-25 avg penetration × (1 + uplift).
- When the user delivers the source, swap the S_NOTE text + add the References
  row/claim; the number stays a visible knob either way.

If the real quote arrives before implementation starts, bake it in directly.

---

## Phase 1 — Program workbooks: Outlook lo/hi redefinition (DDG + subs)

Files: `projects/{ddg,submarines}/workbook/workbook_*/sheets/`

- `inputs_assumptions.py` — add the intent-uplift knob + S_NOTE (per above).
  Watch the promoted-accessor tuple, dv sqrefs, and (subs) the §-numbering — subs
  Assumptions was renumbered twice on 06-10; re-read before editing.
- `model_outlook.py` (both) — §3: replace MIN/MAX(FY22-27 avg, FY26-27 avg) with
  - low = FY22-25 window average (ratio of sums; the FY22-25 column already exists
    structurally — the §3 window rows compute over explicit FY lists),
  - high = low × (1 + uplift), linked to the Inputs knob.
  Relabel rows; keep §6 checks (lo ≤ hi now holds by construction; penetration ≤
  100% check unchanged). §4 implied FY28-31 lo/hi inherit.
- Downstream label/value consumers (both books): Exec Summary §1 KPI rows
  (penetration window labels), `chartdata_z_chart_data.py` §10-§12 outlook blocks
  (assumed lo/hi rows + labels), Figure Register row labels if they name the
  window, Methodology §2c/§2d penetration lines ("lower = FY22-25 avg; upper =
  stated-intent uplift"), Source Index refresh rows unaffected.
- DDG note: FY26 penetration with OBBBA off is the documented REVIEW state —
  unchanged behavior; A/B test it anyway.

Verify: build, validate (0/0), soffice recalc, openpyxl scan, all checks OK,
OBBBA-toggle A/B reproduces documented pre-OBBBA TAMs exactly
(DDG 5,840.3-71? → re-derive; subs 17,223.5).

## Phase 2 — Harvest the restated numbers (single source of truth for everything below)

Rebuild + recalc both program workbooks (headless soffice → openpyxl data_only).
Pull, per program:

- **Walk components (cumulative FY22-27, constant FY26 $B)** — expected from the
  06-10 logs, re-harvest exact: DDG TSE 36.5921 (31.1921 + 5.4 OBBBA), GFE+remainder
  12.7681, other non-BC 2.2757, BC 21.5483, AP/LLTM hatch **1.0423** (P-10 EOQ
  constant; was 1.8349), Prime BC = 21.5483 − 5.3794 = **16.1689**, Prime AP/LLTM =
  **0** (coefficient 1.00), endpoint **6.4217**. Subs: TSE 90.2235, GFE+rem 19.1685,
  other non-BC 10.4895, BC 60.5655, Prime BC = 60.5655 − 18.1338 = **42.4317**,
  endpoint **18.1338**.
- **Annual outsourced BC TAM by FY** (FY22-27 actuals; FY28-31 implied lo/hi under
  the NEW bounds).
- **Annual penetration denominator by FY** (Outlook §2 denominator: SCN 'total'
  constant + OBBBA gross, toggle-gated) — these are the slide-4 outline totals.
  FY28-31 denominator = FYDP gross constant (for the commentary "~$24-25B/yr",
  not drawn as outlines).
- **Penetration % by FY** (FY22-27) + FY22-25 avg (new low) + intent-uplift high,
  per program.
- **FY22-25 avg TAM** per program + combined (the dashed reference line).
- **Work-type buckets, cumulative** (SAM Build): DDG mach 2,260.8 / HVAC 984.2 /
  elec 687.8 / piping 603.9 / struct 371.5 / cast 146.6 / coat 9.7 / residual
  1,357.3; subs elec 5,594.9 / piping 3,711.6 / struct 3,616.2 / coat 963.0 /
  cast 785.8 / mach 708.3 / HVAC 191.5 / residual 2,562.5 ($M; re-harvest exact).
- **Work-type allocation by FY, FY22-25** (NEW need): per program, per FY — bucket
  TAM(fy) = annual TAM(fy) × share(fy, b) and the share vectors themselves
  (Worktype by FY share grids; subs = Va + Col combined at each class's own TAM
  weights — read the SAM Build §4 per-FY allocation rows or compute
  Σ_class TAM(class,fy)×share(class,fy,b); decide at harvest which sheet exposes
  the combined per-FY rows directly).

Identity gates before proceeding: buckets+residual = portfolio TAM per program;
Σ_fy(annual TAM) = cumulative TAM; Σ_fy per-FY work-type = FY22-25 portion of TAM;
walk endpoints = portfolio TAMs.

## Phase 3 — Consolidated workbook, tab 2 only

File: `projects/consolidated/workbook/workbook_consolidated/sheets/z_chart_data_outsourced_bc.py`
(tab 1 `z_chart_data.py` §1-§10 stays stale this pass — it feeds the demoted
back-catalog slides; see Out of scope.)

Paste-only discipline: one bordered rectangle per think-cell chart, slide order,
no memo blocks. Restate + restructure:

| § | Content | Change |
|---|---|---|
| §1 | DDG walk | restate (hatch 1.0423, Prime AP/LLTM **blank** like subs, endpoint 6.4217) |
| §2 | Sub walk | restate (endpoint 18.1338) |
| §3 | Work type per program (cumulative) | restate both columns; keep bucket order; columns must sum to §1/§2 endpoints |
| §4 | Annual TAM w/ outlook | **restructure** for the new chart: rows Sub outsourced / Sub denominator remainder / DDG outsourced / DDG denominator remainder (FY22-27) + Sub implied low / DDG implied low / Range to high (FY28-31). Remainder rows = denominator − outsourced (what the outline segment draws) |
| §5 | FY22-25 avg line | restate (combined; single value) |
| §6 | DDG penetration strip | restate; assumed rows = FY22-25 avg low / intent high |
| §7 | Sub penetration strip | restate; same |
| §8 NEW | Sub work type by FY (FY22-25, 8 series × 4 cats) | new block |
| §9 NEW | DDG work type by FY (FY22-25) | new block |

Docstring § map + `_NCOLS` re-check (FY22-27 + label col fits current 11).
Build + validate (0/0), openpyxl position dump, identity checks (§3 sums = §1/§2
endpoints; §8/§9 column sums = §4 FY22-25 outsourced values).

## Phase 4 — Deck modules

Dir: `projects/consolidated/deck/deck_consolidated/slides/`. House rules: titles
"Topic | Finding." ≤ ~150 chars / 2 lines; no em dashes; sources lines per slide;
re-read each file immediately before editing.

### 4a. `slides/__init__.py` — reorder + register
Front block becomes: cover → s03 (walk) → s03b (work type) → s11a (annual TAM) →
**s03c_body_worktype_by_fy (NEW)** → divider_market_landscape → s02 … (rest
unchanged). Deck goes 24 → 25 slides; chart numbering reflows automatically —
re-verify downstream slides after build.

### 4b. `s03_body_outsourced_bc_overview.py` (walk) — restate
- Title: keep "Outsourced Basic Construction | …" but per the manager's note make
  the figures explicitly annualized: "~$1.1B of outsourced work per year for
  DDG-51 and ~$3.0B for submarines (annualized, FY2022-FY2027)" — exact phrasing
  at impl., char budget ~150.
- Bars: new values/labels (DDG 37+1−13−2 → 22+1; 23−16 → endpoint ~6; subs
  90−19−10 → 61; 61−42 → 19?? — recompute label-precision tie-out at impl. and
  accept ±1 whole-number artifacts as before). DDG hatch = 1.0 ("1"); DDG "Less:
  Prime AP/LLTM" becomes an em-dash row (mirror subs) since the EOQ stream is
  100% outsourced. Axis maxima re-check (sub endpoint dropped 21 → 18; DDG total
  unchanged).
- Connectors/overlays re-derive from `_plot_geom` math — positions follow values.
- Ledger rationale rewrites:
  - Prime BC: "share from announced contract POP: DDG-51 ~25% (FY23-27 masters;
    FY22 vintage 22%), Virginia 34% / Columbia 22% (class construction masters)".
  - Prime AP/LLTM: "AP/LLTM = P-10 Ship Construction EOQ line (vendor-purchased
    material by classification); none retained by the primes" — answers his
    "add a line on how the share" note by removing the 80%/85% construct.
  - Total Ship Spend / AP row: AP figure $1.8B → $1.0B (EOQ).
- Callouts: "~$1.1B annualized" / "~$3.0B annualized".
- Sources: replace the AP/LLTM placeholder with the P-10 cite (PB2027 SCN, LI 2122
  Exhibit P-10, Advance Procurement Requirements Analysis); add DOD award
  bulletins (announced POP) if not present.

### 4c. `s03b_body_worktype_by_program.py` (work type, cumulative) — restate
- Headline: "Electrical power leads the ~$18.1B submarine pool; machining leads
  the ~$6.4B DDG-51 pool." (lead claims still true under new vectors).
- New bucket values; bar ratio is now ~2.8:1 (was 5.4:1) — re-tune the label
  scheme: some DDG segments (machining 2.3, residual 1.4, HVAC 1.0) may now hold
  in-bar labels; keep the leader ladder for the thin ones; sub coatings/castings/
  machining/HVAC re-check thin thresholds. Axis 0-24 → likely 0-20.
- Methodology panel: append the evidence-window statement (his "state methodology
  here" note): shares measured from FY2022-FY2025 yard-prime subawards (gate);
  FY2026-27 allocated at the window vector. One ledger row or a third finding
  line — pick whichever fits without clipping (estimate_row_heights re-check).
- Sources: FFATA line → "FFATA/FSRS subaward records, yard-prime PIIDs,
  FY2022-FY2025 action years".
- Sync-pointer comments → tab-2 §3.

### 4d. `s11a_body_outsourced_bc_annual_tam.py` (annual TAM) — major rework (P1)
New chart geometry (the manager's "cluster stacked bars"):
- **One native stacked column chart, ~21 categories**: per FY two slots
  (Sub, DDG) + a blank spacer between FY groups ("", values None). Native
  category labels OFF; FY labels + per-column program ticks drawn as overlays
  (the pinned `plot_layout` + `_plot_geom` math, as today).
- Series stack (bottom-up):
  1. `Outsourced` — per-point fills (sub accent2 navy on sub slots, DDG accent1
     gray on DDG slots), values FY22-27 actuals; FY28-31 slots carry the implied
     LOW values with tinted per-point fills (existing idiom).
  2. `Sub remainder` — values only on sub slots FY22-27 (= denominator −
     outsourced), `no_fill`, **dashed outline** ~0.5pt dark navy.
  3. `DDG remainder` — DDG slots FY22-27, `no_fill`, **dotted outline** ~0.5pt.
  4. `Range to high` — FY28-31 slots only (= hi − lo), the s03/s11a hatch
     `pattern` idiom.
  Two remainder series exist *because outline style differs per program* —
  series-level line styling, no per-point line hacking.
- **deck_core extension (backward-compatible)**: `charts.py` series option for an
  outlined no-fill box — today `seg_line_color` is solid-only and chart-wide.
  Add per-series `line: {color, width, dash}` (emit `<a:prstDash val="dash|sysDot"/>`
  in the series spPr ln) defaulting to current behavior. Regression-diff the
  rebuilt deck pre-slide-change (expect byte-identical charts, the established
  check).
- Labels: outsourced values inside/at-top of filled segments (9pt non-bold,
  hide+chip where thin); denominator total floats above each outlined column
  (e.g. sub FY22 "11.0"); FY28-31 keep "lo–hi" floats at the high level.
- Penetration strip: ONE row "Outsourced %:" with circled/oval chips under each
  program column (restated values; DDG roughly doubles vs the old strip). FY28-31
  get the spanning assumed pill ("~X-Y% (assumed)").
- Banding: dashed vertical at the FY26|FY27 boundary; boxed band labels
  "Historical" (over FY22-26) and "Forecasted" (over FY27-31) per decision 3.
  Drop the old three-band k=4/k=6 verticals in favor of this two-band cut (the
  FY28-31 estimate framing stays via hatch + dashed frames or hatch only —
  decide at visual QA; the manager's mock keeps the outyear hatch).
- Commentary: replace the three free-text columns with the mock's structured
  rows — Submarines / DDG-51 / "Penetration % methodology", each split
  Historical-band vs Outlook-band:
  - Sub outlook: "(1) PB27 FYDP gross holds near ~$24-25B/yr on serial production
    of 1 Columbia + 2 Virginias from 2028. (2) shipbuilders lack capacity for
    concurrent Columbia and Virginia production 'without strategically
    outsourcing workload to qualified suppliers' (PB27 SCN, COLUMBIA P-10)."
  - DDG outlook: total-spend line from FYDP (DDG ~$4-7B/yr) + the intent quote —
    the HII outsourced-manhours statement covers Ingalls (the dominant DDG FFATA
    yard), which likely answers his "Shipbuilding plan quote?" ask; confirm with
    user when the source lands.
  - Methodology row: "lower bound = FY22-25 average; upper bound = stated
    intent (+30% vs average)" — final wording once sourced.
  - Historical cells: actual avg total spend + avg outsourced % per program.
- Headline restate (post-restate numbers): pre-OBBBA average, FY26 peak, FY28-31
  implied range all re-derive in Phase 2. Keep ≤2 lines.
- Axis: outline totals push the max from 7 to ~max(sub denominator) — likely
  0-20/22, major 2. The filled bars compress; that is the point of the format
  (penetration made visible). Confirm readability at visual QA; if FY26 sub
  denominator (~$19-20B incl OBBBA) crushes everything, fall back = state the
  issue + screenshots, decide with user before shipping.
- Breadcrumb/exhibit header/sources: restate basis + P-10 + bulletins cites.
- s11 (back-catalog cadence slide) stays untouched.

### 4e. NEW `s03c_body_worktype_by_fy.py` (manager's slide 5, P4)
- Chrome: breadcrumb "Executive Summary / Outsourced BC Annual TAM" (per mock);
  title reuses the work-type finding pair — differentiate from s03b, e.g.
  "Outsourced Basic Construction Spend by Work Type | The work-type mix is stable
  across FY2022-FY2025 within each program." (exact finding once the per-FY data
  is in hand — verify the stability claim is true before asserting it; pick the
  honest pattern: stable vs shifting).
- Exhibit header "($B, annual FY2022-FY2025, FY2026 $)".
- **Two charts side by side** (s03/s05 dual-chart precedent): Submarines panel +
  DDG panel, each `column_chart(mode="stacked")`, 4 categories FY22-25, 8 series
  (7 buckets + hatched Residual via `pattern`), per-program axis scale (sub
  ~0-6, DDG ~0-2) so DDG segments stay readable — the mock's shared axis would
  crush DDG.
- Labels: per-segment **% labels** (the share vector; overlay text or native
  labels showing the share, since segment $ are tiny) — implementation choice:
  native labels carry $ values; the mock shows %. Easiest faithful route: native
  labels OFF, overlay % labels via `_plot_geom` (centers known from cumulative
  stack math), leader-ladder for thin segments (s03b idiom). Totals ($B) above
  each column.
- One shared horizontal legend (top, 8 entries incl. hand-built hatch swatch
  `<p:sp>` + `a:pattFill` for Residual — text_box/chart_key are solid-only).
- Sources line = s03b's + the gated-window statement.
- Data from tab-2 §8/§9.

## Phase 5 — Build, QA, log

- Deck: `cd projects/consolidated/deck && python3 build_deck.py` → expect
  **25 slides**; chart count +2 (s03c) ⇒ recount and xmllint new slide + charts.
- Visual QA: soffice → pdf → pdftoppm at 110/200 dpi; side-by-side against the
  vDraft renders (slides 2-5) for format parity, and against pre-change PNGs for
  downstream-slide invariance (chart renumber check: s05 funnel, s11, s12, s13).
- Checklist ties (label precision): walk endpoints ↔ work-type totals ↔ annual
  sums ↔ per-FY work-type sums; penetration chips = filled ÷ outline total at
  displayed rounding; FY22-25 avg line = displayed average.
- Workbooks already verified in Phases 1-3; rerun consolidated build+validate
  last (0 xml errors / 0 error cells).
- Write the session log to `logs/2026-06-10_consolidated_front_row_restate_worktype_by_fy.md`
  (or two logs if Phase 1 ships separately).

## Out of scope this pass (known-stale, deliberate)

- Consolidated tab 1 (`z_chart_data.py` §1-§10) and the demoted back-catalog
  slides (s02, s05, s09, s10, s11, s12, s13, appendix M-pages) — still carry
  pre-restate numbers and 13%/35%/80%/85% copy. Sweep belongs to the eventual
  backup-demotion/terminology pass.
- Program decks, DDG wiki ch12, subs wiki ch6/ch7, deck spec .md files.
- PB2028 tripwires unchanged (Va FY26 TSE 5,389.109 anchors).

## Addendum — Virginia/Columbia class breakdown (goes beyond the manager's mock)

Rationale: the 06-10 subs restates made "Submarines" a blend of two materially
different markets — Virginia 34% vs Columbia 22% penetration (class-vintage
coefficients), genuinely different work-type mixes (window: electrical Va ~32%
vs Col ~45%, coatings 6.8% vs 1.4%, structural 20.6% vs 15.9%), and an outyear
demand story the manager himself frames per class ("1 Columbia + 2 Virginias
from 2028"). A combined sub bar carries composition artifacts (the FY26-27
penetration dip is a Columbia-mix effect, not a behavior change). All per-class
data already exists in the subs workbook: `tam_cell(li, fy)`, per-class constant
TSE (`pos_const`), OBBBA on Virginia, `fydp_gross_cell` per LI,
`class_bucket_tam_cell` (cumulative), and the Worktype-by-FY Va/Col share grids.

Graduated scope (recommended):

- **s03 walk — unchanged** (combined sub waterfall). Per-class shows up only in
  the Prime BC ledger rationale (34%/22%), already planned. Splitting the walk
  would mean three waterfalls and break the mock's side-by-side read.
- **s03b work type cumulative — 3 categories**: DDG-51, Virginia, Columbia
  (was 2). Va + Col columns must sum to the sub walk endpoint (18.1338).
  Label scheme re-tuned for three bars (~6.4 / ~11.6 / ~6.5 $B scale guess —
  harvest exact). Headline may shift to the class contrast if the data leads
  there (e.g. electrical dominance is disproportionately Columbia).
- **s11a annual TAM — class-stack the sub filled bar, keep the manager's
  cluster format**: the sub column's filled portion becomes Va + Col stacked
  segments (two navy tints); ONE sub outline (combined denominator) and ONE
  combined sub penetration chip, so the cluster geometry and chip math stay
  exactly as mocked. FY28-31 implied-low bars likewise split per class
  (the 2-Va + 1-Col serial story made visible). Legend gains a Columbia entry.
- **s03c work type by FY — 3 panels** (Virginia, Columbia, DDG-51), 4 FYs each,
  own axis scales. This is where per-class is most natural: the measured vectors
  are per-class natively; the combined sub vector is a TAM-weighted blend.

Plan impact by phase:

- **Phase 1 grows (subs `model_outlook.py`)**: per-class penetration rows
  (§2: class TAM ÷ class denominator, OBBBA on Va), per-class FY22-25 avg low +
  intent-uplift high (§3), per-class implied FY28-31 (§4: class FYDP gross ×
  class bounds). Portfolio rows stay as sums/blends. One shared intent-uplift
  knob across classes unless the sourced statement is class-specific (HII = NNS
  covers both; flag at sourcing time). DDG side of Phase 1 unchanged.
- **Phase 2 harvest adds**: per-class annual TAM, denominators, penetration,
  implied lo/hi, FYDP gross, cumulative buckets, per-FY work-type grids.
- **Phase 3 tab-2 reshape**: §3 → 3 data columns; §4 → Va outsourced / Col
  outsourced / Sub remainder / DDG outsourced / DDG remainder + per-class
  implied-low rows; §8/§9 → §8 Va / §9 Col / §10 DDG per-FY work-type blocks.
  §6/§7 penetration strips stay program-level (the slide chips are combined-sub
  per the cluster design).
- **Phase 4**: s03b categories 2→3; s11a series list grows (Va, Col, DDG fills +
  2 remainder outlines + per-class implied lows + range hatch); s03c = 3 charts.
- **Phase 5 identities add**: Va + Col = sub totals at every level (cumulative,
  per FY, per bucket, implied outyears).

Caveat to carry on-slide where relevant: the Columbia coefficient rests on a
single announced master (Build I, 22%) — same one-assumption posture as the
OBBBA BC share; the Methodology/§2d basis tables already disclose it.

## Sequencing note

Phases are ordered by dependency: 1 (model change) → 2 (harvest) → 3 (chartdata)
→ 4 (slides) → 5 (QA). The deck_core `line` dash extension (4d) can be built and
regression-checked any time before 4d. If the HII/intent source arrives mid-pass,
slot it into Phase 1's knob + References before final harvest; otherwise ship at
0.30 with the citation-TBD note and flag it in the log.
