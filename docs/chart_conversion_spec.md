# Chart conversion spec — adopt the Sea Range Telemetry chart pattern

**Scope:** convert the DDG and submarine deck charts to the visual grammar of the
*Sea Range Telemetry* (SRT) market-sizing deck
(`/Users/brendantoole/projects2/sea_range_telemetry/20260521_Sea Range Telemetry_vS.pptx`).
This is a **slide-module + slide-spec** change only. The shared engine
(`deck_core/charts.py`, `style.py`) is **not** touched — every target type is already
exposed by `column_chart()` / `waterfall_chart()`.

User decisions baked in:
- **(a)** Long category labels on rankings are **shortened** to fit vertical columns (detail moves to data labels / value axis).
- **(b)** `sib_exclusion` (submarines) becomes a **waterfall**, not a table.
- **Colors come from the SRT chart bars themselves** (exact hex below), *not* from the deck's `style.py` ramp. This is deliberate; see §5.

---

## 1. The SRT chart grammar (what we're matching)

SRT has **7 charts, all vertical column family, zero horizontal bars**. Chart type follows the chart's *job*:

| Job of the chart | SRT type | Native factory |
|---|---|---|
| Build a number to a total / derive / reconcile / narrow a funnel | **Waterfall** (its signature — 3 of 7) | `waterfall_chart(steps=…)` |
| Compare a few short-labeled categories | **Clustered column** | `column_chart(mode="clustered")` |
| Breakdown that sums to a total | **Stacked column** | `column_chart(mode="stacked")` |
| Rank a few short-labeled items | **Single-series column** | `column_chart(mode="ranked")` |
| Long labels / many items (e.g. supplier names) | *not charted as columns — kept horizontal or as a table* | `bar_chart` / `house_table` |

**The one structural caveat:** SRT hides the category axis (`tickLblPos=none`) and draws
category labels as think-cell free text. The native engine puts category labels **on the
x-axis**, which is why long labels must be shortened (decision a) — that is the only place
the native conversion can't 1:1 mimic think-cell.

---

## 2. SRT **bar palette** — exact hex (bar fills only)

These are the fills used **on the chart bars/segments**, resolved from theme accents +
explicit grays. (Theme text colors `#162029` / `#44505C` happen to match our deck, but
that's incidental — the bar fills below are what to use.)

| Hex | Name (this spec) | Role on SRT bars |
|---|---|---|
| `#1D4D68` | **Hero navy** | The focal value — emphasis bar, focal group, dark series in a clustered pair, anchor/total pillar in a waterfall |
| `#486D82` | Mid blue | Build segments in waterfalls; ramp step 2 |
| `#89A2B0` | Slate blue | Ramp step 3 |
| `#AFC2CC` | Pale blue | Ramp step 4 |
| `#D8E3EB` | Lightest blue | Ramp step 5 (palest fill) |
| `#79838F` | **Neutral blue-gray** | The non-focal series / "everything else" group |
| `#A1A1A1` | Mid gray | Waterfall connector/base risers; "other"/outlier bars |
| `#BEBEBE` | Light gray | Waterfall **end-total** pillar; de-emphasized bar |
| `#DBDBDB` | Lightest gray | Most-muted bar |

### Color logic (observed, by chart type)

- **Single-series ranked, focal subset** (SRT chart6 "Top Areas"): the focal subset of bars
  = `#1D4D68`, the remainder = `#79838F`. Two-tone, no gradient.
- **Single-series graduated** (SRT chart4 "Vessel Economics"): light→dark blue ramp
  `#D8E3EB → #AFC2CC → #89A2B0 → #486D82 → #1D4D68` across the in-range bars, then **gray
  (`#BEBEBE`, `#A1A1A1`) for the outliers** to mute them.
- **2-series clustered** (SRT chart1 "TAM by Region"): the decision-relevant metric (SAM) is
  `#1D4D68` everywhere; the context metric (TAM) is `#79838F`. Hero color = the metric you
  want read, not the bigger number.
- **Waterfall** (SRT charts 2/3/7): anchor/total pillars `#1D4D68`; build (increase) segments
  walk the blue ramp `#486D82 → #89A2B0 → #AFC2CC`; the closing total pillar is muted to
  `#BEBEBE`; the floating base/connector is gray `#A1A1A1` (in the native engine this is the
  hidden spacer series — leave it `no_fill`).

### Non-color styling constants (from the SRT chart parts)

| Property | SRT value | Native knob |
|---|---|---|
| Font (all chart text) | Arial | theme (already Arial) |
| Bar gap width | `80` | `gap_width=80` (col); waterfall already `60` |
| Stacked overlap | `100` | set by stacked/waterfall automatically |
| Vary colors | off — colors set explicitly per point | use `data_point_colors=[…]` |
| Data labels | shown, **10pt**, color `#44505C`, not bold | `show_value_labels=True, value_label_size_pt=10` |
| Value-axis number format | `#,##0;"-"#,##0` (`#,##0.0` when decimals) | `value_axis_format=…` |
| Value axis | shown (`tickLblPos=nextTo`), 10pt | default |
| Major gridlines | **on** (both axes) | `show_gridlines=True` |
| Category axis labels | **hidden** in SRT (drawn as text) → we **show short labels** | `show_cat_labels=True` |
| Native chart title | **none** (drawn as slide text) — both decks already use a no-fill `CHART_TITLE_10PT` text box; keep that | `title=None` + `_chart_title(...)` |

---

## 3. DDG conversions

Current: **10 charts, 8 horizontal bars.** Target profile below.

| Module / chart | Current | → Target | Color rule (from §2) |
|---|---|---|---|
| `annual_tam_build` | waterfall (V) | **keep** — re-color to SRT waterfall | total `#1D4D68`, increase `#486D82`, end `#BEBEBE` |
| `tam_timing` | stacked column (V) | **keep** — re-color | hero stream `#1D4D68`, others down blue ramp |
| `cost_funnel` | ranked bar (H), 3 cats | **→ waterfall (decreasing)** | start `#1D4D68`; decreases gray `#A1A1A1`; addressable end `#1D4D68` |
| `ffata_visibility_gap` | clustered bar (H), 4 long cats | **→ single-series column** | "Visible flow" bar `#1D4D68` (hero); 3 outsourcing estimates `#79838F` (neutral) |
| `myp_redaction` (comparison) | stacked bar (H) | **→ stacked column** | redacted/hero segment `#1D4D68`; remainder blue ramp |
| `myp_redaction` (distribution) | 100%-stacked bar (H) | **→ stacked column** (drop %-stacked; SRT has none) | same ramp logic |
| `work_type_allocation` | ranked bar (H), 8 long cats | **→ ranked column** (shorten labels) | residual (largest) `#1D4D68`; rest blue ramp → gray tail |
| `sam_scenarios` | ranked bar (H), 5 long cats | **→ ranked column** (shorten labels) | top family `#1D4D68`; rest `#486D82 → #AFC2CC` |
| `supplier_landscape` | ranked bar (H), 10 supplier names | **keep horizontal** (exception — names can't shorten) | top supplier(s) `#1D4D68`; rest `#79838F` |
| `executive_summary` | stacked bar (H) | **REMOVE** — spec already `charts: []` (KPI board); module is behind the spec | — |

**Shortened category tokens (decision a):**

- `work_type_allocation` (% moves to data label; keep canonical "Unbucketed / ambiguous" in
  legend/data, axis token short):
  `Unbucketed` · `Electrical/power` · `Structural` · `Machining` · `Piping/valves` · `HVAC` ·
  `Coatings` · `Castings`
- `sam_scenarios`:
  `Broad components` · `Metal components` · `Electrical/power` · `Modular assy` · `HM&E`
- `ffata_visibility_gap` ($ moves to data label):
  `Visible flow` · `Outsourcing low` · `Outsourcing mid` · `Outsourcing high`

---

## 4. Submarine conversions

Current: **9 charts, 6 horizontal bars.**

| Module / chart | Current | → Target | Color rule (from §2) |
|---|---|---|---|
| `ap_and_lltm` | waterfall (V) | **keep** — re-color to SRT waterfall | total `#1D4D68`, increase `#486D82`, end `#BEBEBE` |
| `basic_construction` | stacked column (V) | **keep** — re-color | hero stream `#1D4D68`; others blue ramp |
| `annual_cadence` | clustered column (V) | **keep** — re-color | TAM `#79838F` (context), broad SAM `#1D4D68` (hero) |
| `coefficient_evidence` | ranked bar (H), 3 cats | **→ ranked column** (easy) | anchor bar `#1D4D68`; others `#79838F` |
| `bucket_tam` | ranked bar (H), 7 long cats | **→ ranked column** (shorten labels) | top bucket `#1D4D68`; rest blue ramp → gray tail |
| `sam_scenarios` | ranked bar (H), 5 long cats | **→ ranked column** (shorten labels) | top family `#1D4D68`; rest `#486D82 → #AFC2CC` |
| `visible_suppliers` | ranked bar (H), 10 names | **keep horizontal** (exception) | top supplier(s) `#1D4D68`; rest `#79838F` |
| `sib_exclusion` | ranked bar (H), 3 org names | **→ waterfall (decreasing)** *(decision b)* | start gross `#1D4D68`; each exclusion gray `#A1A1A1`; counted-TAM end `#1D4D68` |
| `appendix_coefficient_sensitivity` | ranked bar (H), 3 cats | **→ ranked column** (or keep H tornado) | center/base bar `#1D4D68`; ±cases `#79838F` |

**Shortened category tokens (decision a):**

- `coefficient_evidence` / `appendix_coefficient_sensitivity`:
  `POP anchor` · `AP/LLTM ref` · `BC coefficient`
- `bucket_tam`:
  `Electrical/power` · `Structural` · `Piping/valves` · `Castings` · `Coatings` ·
  `Machining` · `HVAC`
- `sam_scenarios`:
  `Broad components` · `Electrical/power` · `Metal components` · `Modular assy` · `HM&E`

**`sib_exclusion` waterfall steps** (replacing `_CATEGORIES`/`_VALUES`; values preserved):
```
start    "Gross flow"      = counted TAM + 4,251.8     #1D4D68
delta    "BlueForge"       = −4,173.3                   #A1A1A1
delta    "TMG"             = −77.0                      #A1A1A1
delta    "IALR"            = −1.5                       #A1A1A1
end      "Counted TAM"     = (running total)            #1D4D68
```
(Keep the existing exclusion-ledger table alongside if the slide has room; the chart now
carries the "role, not size, decides" narrowing visually.)

---

## 5. Implementation notes

- **No core edits.** `column_chart(mode=…)` and `waterfall_chart(steps=…, increase_color, total_color, decrease_color)` already exist. Conversion is per-module:
  - Horizontal → vertical: swap `bar_chart(...)` → `column_chart(...)` (the engine flips
    `horizontal`); apply `data_point_colors=[…]` with the §2 hex; shorten `categories`.
  - Ranked-bar → waterfall: replace the `bar_chart` call with `waterfall_chart(steps=[…])`
    and set `increase_color="486D82"`, `total_color="1D4D68"`, `decrease_color="A1A1A1"`.
- **Colors are raw SRT hex, by user direction** — this intentionally bypasses the
  `style.py` `BLUE_SCALE`/`GRAY_SCALE` tokens. House style normally says "use `style.py`
  tokens," so the durable fix would be to add these nine SRT bar colors as named tokens in
  `style.py` (a **core change — needs sign-off**, out of scope here). Until then the hex
  lives in the slide modules.
- **Two charts are already slated to disappear** in the specs and only need the module to
  catch up: DDG `executive_summary` (`charts: []`) and — note — submarine `sib_exclusion`'s
  spec currently says `charts: []`/table; decision (b) overrides that back to a waterfall, so
  update the spec too.
- **Titles unchanged:** keep the no-fill `CHART_TITLE_10PT` text-box title above each frame
  (both decks already do this); `title=None` stays on the chart object.
- **Per-spec follow-up:** update each affected `slide_specs/*.md` `charts:` block (type,
  shortened category list, color roles) to match — specs are off the build path but are the
  handoff source of truth.

## 6. Net effect

| Chart type | DDG before → after | Subs before → after |
|---|---|---|
| Horizontal bar | 8 → **1** (suppliers) | 6 → **1** (suppliers) |
| Vertical column (clustered/stacked/ranked) | 1 → **6** | 2 → **6** |
| Waterfall | 1 → **2** | 1 → **2** |
| Removed / → other | — → 1 (exec → KPI) | — (sib stays charted, now waterfall) |

Both decks land on the SRT profile: **column family + waterfall signature, monochrome blue
ramp with `#1D4D68` as the single hero color and grays for de-emphasis**, horizontal bars
reserved only for the supplier-name rankings.

---

## 7. APPLIED — 2026-06-04 (as-built)

All module conversions applied; **both decks rebuild green**:
- **DDG:** 25 slides, **9 charts** (was 10 — `executive_summary` chart removed). Emitted:
  8 vertical column-family + 1 horizontal (`supplier_landscape`); **2 waterfalls**
  (`annual_tam_build`, `cost_funnel`). 8/9 charts carry hero navy `#1D4D68`.
- **Submarines:** 27 slides, **9 charts** (unchanged count — `sib_exclusion` stays charted as
  a waterfall). Emitted: 8 vertical column-family + 1 horizontal (`visible_suppliers`);
  **2 waterfalls** (`ap_and_lltm`, `sib_exclusion`).

Colors are raw SRT hex inlined in the modules (per user direction); ranked columns use the
`_SRT_RAMP` `["1D4D68","486D82","89A2B0","AFC2CC","D8E3EB"]` (extended with `BEBEBE`/`DBDBDB`
for 7-8 cat tails). `value_label_size_pt` bumped 9→10 and `gap_width`→80 on converted columns.

**Deviations from the plan above (and why):**
- **`myp_redaction` distribution** kept `mode="percent"` (vertical) rather than dropping to
  raw stacked — a single-bar place-of-performance composition is inherently 100%, so percent
  is the correct grouping. Other-US supplier slice = hero navy.
- **`sib_exclusion`** rendered as an **additive** waterfall (BlueForge → +TMG → +IALR → Total
  excluded). Steps/total are **gray/neutral, not hero navy** — the slide's whole point is that
  these dollars are *excluded* from TAM, so coloring them hero would mislead.
- **`executive_summary`** chart fully removed (its slide-spec already carried `charts: []`);
  `_chart_title` helper + frame deleted, sizing note left at the foot of the right column.

**Needs PowerPoint visual review (orientation flip moved hand-tuned geometry):**
- `ffata_visibility_gap` — the "~20.1% of midpoint" wedge callout was re-aimed at the leftmost
  (visible-flow) column; tip coordinates are best-effort.
- `coefficient_evidence` — the two bar-annotation captions ("Reference only…", "Only input…")
  were repositioned above the middle/right columns; placement is approximate.
- `myp_redaction` distribution — a single 100%-stacked column sits in a wide-short frame
  (chunky); legible but not ideal. Narrow the frame if a slimmer column is wanted.

**Spec reconciliation (follow-up, NOT done here):** each `slide_specs/*.md` carries a full
`charts:` mirror (factory / categories / colors / params). 16 of them now describe the *old*
chart (e.g. `factory: bar_chart`, old labels, `BLUE_*` colors). Only `sib_exclusion.md` was
reconciled here (it actively contradicted the new waterfall — it said `charts: []` + a ledger
table that the module never carried). The other 15 need a mechanical mirror pass.
