# 2026-06-09 — Consolidated deck: front-row "Outsourced BC Overview" walk slide (manager mock 1 of 3)

## Problem / goal

The manager mocked three new slides in a copied version of the consolidated deck
(screenshots: `~/Downloads/Screenshot 2026-06-09 1516{33,04,26}.png`). They reframe the
supplier story around **"Outsourced Basic Construction"** (= what the repo calls supplier
TAM) and will be **front-row**; the existing content slides will become backup (and may be
cut) — that demotion/reorg is deferred until all three are built. This session built
**slide 1**: a per-program waterfall walk *Total Ship Spend → Less GFE → Less Other non-BC
→ Basic Construction → Less Prime BC → Less Prime AP/LLTM → Outsourced BC*, DDG-51 and
Virginia/Columbia side by side, with a Step/Rationale ledger on the right. All values
post-deflator, post-OBBBA (constant FY2026 $, cumulative FY2022–FY2027).

User decisions: extend deck_core (backward-compatible) rather than inline chart-XML hacks;
**whole-number bar labels** (headline/callouts keep 1-decimal $B); slide inserted right
after s02 (Executive Summary section, breadcrumb "Executive Summary / Supplier TAM and
SAM" per the mock).

## Numbers (constant FY2026 $B, cumulative FY22–27; labels = #,##0 rounding)

| Step | DDG exact (label) | Sub exact (label) |
|---|---|---|
| Total Ship Spend, in-year | 36.5921 = 31.1921 P-5c + 5.4 OBBBA (37) | 90.2235 = 85.6235 + 4.6 (90) |
| + AP/LLTM hatch | 1.8349 = 1.2477/0.68 (2) | — |
| Less GFE (incl. OBBBA non-BC remainder) | 12.7681 = 10.7593 + 2.0088 (13) | 19.1685 = 17.2460 + 1.9225 (19) |
| Less Other non-BC | 2.2757 (2) | 10.4895 (10) |
| Basic Construction | 21.5483 + 1.8349 hatch (22 + 2) | 60.5655 (61) |
| Less Prime BC | 18.8448 (19) | 39.3533 (39) |
| Less Prime AP/LLTM | 0.5872 (chip "1") | none (em-dash row) |
| **Outsourced BC** | **3.9513 (4)** | **21.2122 (21)** |

Callouts: "~$0.7B annualized" (658.55M/yr) / "~$3.5B annualized" (3,535.36M/yr). Title
(revised same day to house "Topic | Finding." copy, annualized per the manager's
preference): "Outsourced Basic Construction | Total ship spend narrows to ~$0.7B of
outsourced work per year for DDG-51 and ~$3.5B for submarines, FY2022–FY2027." (The
title is per-year while the walk bars are cumulative; the annualized callouts bridge
them.) DDG ties at label precision
(37+2−13−2 = 24 = 22+2; 24−19−1 = 4). Sub carries a known 1-unit whole-number artifact
(61−39 = 22 vs 21) — accepted per the rounding decision. Deliberate mock deviation: the
AP/LLTM hatch rides on BOTH the Total and BC bars (mock had Total only, which can't tie).

## Changes

### `deck_core/charts.py` — two backward-compatible engine params
- Per-series **`pattern: {"prst","fg","bg"}`** → `<a:pattFill>` in the series spPr (new
  branch beside `no_fill` in `_build_series`; auto label color derives from the pattern
  `bg`). Used for the AP/LLTM hatch (`ltUpDiag`, fg accent1, bg white); slide 2's hatched
  FY28–31 estimate bars will reuse it.
- **`show_value_axis_labels: bool = True`** → False sets valAx `tickLblPos="none"` +
  `majorTickMark="none"`, axis stays present so min/max scaling holds.
- Regression: rebuilt the deck pre-slide and diffed the unzipped package vs baseline —
  every `ppt/charts/chart*.xml` **byte-identical**; only `docProps/core.xml` timestamps and
  embedded-xlsx **zip mtimes** differ (per-build noise, contents identical).

### NEW `deck_consolidated/slides/s03_body_outsourced_bc_overview.py`
- Two native **horizontal** stacked-bar waterfalls via `bar_chart(mode="stacked")` —
  s05's spacer-series recipe rotated 90°: `_Base` no-fill spacer (left offset), `Walk`
  visible series with per-point `data_point_colors`, DDG-only hatched `AP/LLTM` third
  series (values only on Total + BC rows, `None` elsewhere → no bars/labels).
- Fills (mirrored by the ledger): gray accent1 subtotals, accent5→accent4→accent3→accent2
  removals deepening toward the supplier cut, DK (162029) endpoint. Native 9pt non-bold
  ctr labels, format `#,##0`; `hide_label_points=[5]` on DDG + an accent2 chip overlay
  ("1") for the 0.59 sliver; em-dash placeholder on the sub's empty Prime AP/LLTM row.
- Overlays pinned via `plot_layout` (`_plot_geom` math with axes swapped vs s05): shared
  step-label column serving both panels, bordered italic program chips, "In-Year"/"AP/LLTM"
  8.5pt italic captions over the Total bar spans, dashed navy running-total connectors
  (sub's last connector spans the empty row 4→6), bordered annualized callouts
  (14pt bold + 9pt italic), exhibit header + rule.
- Right ledger: low-level `table()`/`trow()`/`tcell()` (NOT `house_table` — needed italic
  "Calculation" cells), step-cell fills matching the bar colors, white text on dark fills,
  `estimate_row_heights(size_pt=8.5, header_size_pt=9.5)`, house cascading bottom rules.
- Registered in `slides/__init__.py` right after s02 → deck is **22 slides, 8 charts**
  (chart numbering reflowed automatically: s03 = chart2+chart3, s05 shifted to chart4/5).

### `workbook_consolidated/sheets/z_chart_data.py` — §11 paste blocks
- "§11 - Outsourced BC walk (dual waterfall)": DDG/Submarine rows in think-cell step
  convention (removals negative, subtotals/endpoint "e", sub Prime AP/LLTM blank).
- "§11b - Outsourced BC walk components": P-5c TSE, OBBBA gross, AP/LLTM base, Total Ship
  Spend, OBBBA non-BC remainder, OBBBA mandatory BC, AP/LLTM outsourced, Outsourced BC —
  the rows that previously had no z_ChartData home. Docstring § index updated.
- **No DDG/submarine workbook changes** — the walk recombines values they already produce.

## Verification

- Deck build: 22 slides / 8 charts, no errors. `xmllint` clean on slide3 + chart2/chart3;
  `pattFill` present in chart2 (DDG) only, as designed.
- Visual (soffice→pdf→pdftoppm vs the mock): bars cascade and tie, hatch renders with its
  "2" label, connectors land on running totals (incl. the sub's long rule over the empty
  row), chip/dash/callouts placed, ledger fills mirror bar colors, "Calculation" rows
  italic. Downstream slides intact after the chart renumber (s05 funnel re-checked).
- Workbook: build + validate → 0 xml errors, 0 error cells; §11 cell positions verified
  via openpyxl (blank in the Prime AP/LLTM column, "e" in Outsourced BC).

## Gotchas / notes for next time

- **Horizontal waterfall** = s05's vertical recipe with x/y swapped: bar row i's center is
  `py + ph*(2i+1)/(2N)`, a value level maps to `x = px + pw*level/axis_max`, and
  connectors are VERTICAL dashed rules at the shared running-total level.
- A row with `None` values in every series renders no bar AND no label — use `None`, not
  0.0, to blank a walk step (0.0 still emits a "0" label).
- `house_table()` cannot italicize individual cells — drop to `table()`/`tcell()` (which
  has `italic=`) and reproduce the cascading border posture by hand.
- LibreOffice renders chart `a:pattFill` fine, so soffice PNG QA covers the hatch look.
- The engine regression diff will always show `docProps/core.xml` + embedded-xlsx binary
  diffs (build timestamps / zip mtimes) — unzip the embeds and diff contents before
  concluding anything changed.

## Open / next

- Slides 2 (annual cadence: FY22–25 avg dashed line, FY28–31 FYDP×penetration estimate
  bars — needs FYDP outyear data, penetration % rows) and 3 (work type by program +
  inline classifier methodology) — later sessions; slide 2 reuses `pattern`.
- Demoting the existing slides to backup / deck reorg — after all three are built.
- Headline figures on the older slides (s02 etc.) still say "supplier TAM" — terminology
  sweep is part of the eventual backup demotion, not done piecemeal.
