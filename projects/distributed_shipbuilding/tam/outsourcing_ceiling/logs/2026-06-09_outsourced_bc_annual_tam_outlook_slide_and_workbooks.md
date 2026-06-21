# 2026-06-09 — Outsourced BC Annual TAM outlook: workbook layer + new slide s11a

## What

Built the manager's "Outsourced Basic Construction (Annual TAM)" slide (evolution
of s11, as its OWN slide — s11 untouched) and the workbook analysis behind it.
Four asks: (1) dashed line at the FY22–25 average TAM; (2) FY2028–FY2031 implied
Outsourced BC = PB2027 FYDP gross × historical penetration, shown as a range
between two assumptions; (3) per-program per-FY penetration % strips (Outsourced
BC ÷ total ship spend); (4) three-band commentary (history / FY26–27 / outlook)
with evidence for future penetration. Headline rewritten post-OBBBA: FY2026
($6.2B) is the peak, and FY28–31 implies $5.1–5.8B/yr.

User-confirmed methodology: penetration denominator = constant-FY26 Gross/Weapon
System Cost (P-5c TSE) + OBBBA gross (toggle-coherent on both sides); window
averages = ratio of sums; low/high = MIN/MAX(FY22–27 avg, FY26–27 avg); estimate
bars = tinted low-assumption stacks + hatched range cap + dashed-outline frames.

## Key data findings (no new extraction needed)

- `extracted/scn_li_resource_summary.csv` (both programs, research mirrors
  identical) ALREADY carries the PB2027 P-40 FY2028–FY2031 columns. Gross
  ($M then-year): DDG 4,026.2 / 4,209.4 / 6,613.2 / 6,964.2 (qty 1/1/2/2);
  Virginia 11,284.8 / 11,098.4 / 10,196.6 / 10,594.2 (2/2/2/2); Columbia
  10,137.1 / 10,361.0 / 10,441.0 / 10,693.1 (1/1/1/1). Tie-outs: DDG "FY 2027
  Total" = workbook FY27 TSE (4,256.914); Virginia FY26 = the 5,389.109 tripwire
  anchor.
- Green Book FY25 Table 5-4 Procurement runs through FY2029 (106.43 / 108.67);
  FY2030–31 extrapolated at 2.1%/yr (Table 5-3 steady-state purchases inflation):
  110.95 / 113.28. Factors to FY26: "0.96" / "0.94" / "0.92" / "0.90".
- Evidence quote for the outlook penetration floor (added as claim 32 to
  `industry_baseline_citations.csv`, both copies): PB2027 SCN, COLUMBIA P-10,
  Strategic Outsourcing ($25M FY27): "Shipbuilders do not have sufficient
  capacity to accommodate CLB and VIRGINIA Class (VCS) concurrent production
  without strategically outsourcing workload to qualified suppliers…"

## Workbook changes

- `workbook_core/deflators.py`: FY_RANGE → 2022–2031; PROCUREMENT_TOA +4 years;
  `EXTRAPOLATED_FYS = {2030, 2031}`; `GREEN_BOOK_EXTRAP_CITE`. Both
  `data_deflators.py` twins: new "Basis" column (Green Book Table 5-4 vs
  Extrapolated @ 2.1%/yr) + §2 extrapolation source row. FY22–27 rows/refs
  unchanged (new rows append after FY2027); no model `_FY_COLUMNS` touched.
- NEW `sheets/data_fydp_outyears.py` ("FYDP Outyears", data group, after AP
  Bridge; both programs): §1 P-40 provenance fields + then-year grid FY2025–2031
  (gross / qty / Net P-1 memo / TOA memo; `_apnum` DictReader parsing — NOT
  `load_extracted_csv`, which keeps thousands commas); §2 constant FY2026 rows.
  Accessors `fydp_gross_then_cell` / `fydp_gross_cell` / `fydp_qty_cell`
  (+ subs `fydp_portfolio_gross_cell`). Sheet specs added.
- NEW `sheets/model_outlook.py` ("Outlook", model group, after SAM Build; both):
  import-time body + render-time §1 at-a-glance (`assert c.at() == _BASE`, =14).
  §2 penetration by FY = N(tam_total_cell) ÷ (scn 'total' const + OBBBA gross,
  both gated by include_obbba_stream_cell; subs OBBBA term = then-year ×
  deflator, FY26/27 split by the spillover control — DDG's obbba_gross_cell is
  already constant-$, subs' is then-year, a real asymmetry); §3 window averages
  (ratio of sums) + MIN/MAX assumptions; §4 implied FY28–31 lo/hi/range + FY28–31
  averages; §5 FY22–25 avg TAM; §6 checks (FY27 FYDP↔SCN TSE tie per class,
  Virginia FY26 5,389.109 anchor, penetration ≤ 100%, lo ≤ hi). Eleven promoted
  accessors. Sheet specs added.
- Program chartdata (`chartdata_z_chart_data.py`, both): §10 penetration strip
  (actual ×6 + assumed lo/hi ×4), §11 implied outyear stacked low + range cap,
  §12 FY22–25 avg; `_NCOLS` → 11 (cols list widened to match).
- Bookkeeping (both): Exec Summary §1 +4 KPI rows (penetration L6Y, implied
  lo/hi $M/yr, FY22–25 avg); Figure Register rows (DDG sequential; subs
  DO-63..DO-81, `_PCT_IDS` extended); Methodology §2d (DDG) / §2c (subs)
  "Penetration & outyear outlook" + §3 flow row; Source Index lineage / budget
  exhibit + refresh rows ("refresh at PB2028; re-tie Va FY26 = 5,389.109");
  DDG References CITE-07 (Green Book Tables 5-3/5-4 + extrapolation) and CITE-08
  (PB2027 P-40 vintage); subs References budget-exhibit count 4 → 5.
- Consolidated `z_chart_data.py`: §12 "Outsourced BC annual TAM with outlook"
  (Sub/DDG actuals + per-program implied low + combined range-to-high), §13
  penetration strip (per program: actual + assumed lo/hi), §14 FY22–25 average
  (DDG / Sub / Combined); `_NCOLS` → 11; docstring outlook-basis paragraph.
  Hardcoded full-precision from the recalc'd program workbooks.

## Numbers (recalc-verified via soffice, constant FY2026 $)

| Metric | DDG | Submarines |
|---|---|---|
| Penetration FY22–27 | 6.0 / 7.2 / 7.6 / 8.1 / **28.9** / 8.0 % | 24.1 / 24.6 / 24.5 / 19.6 / 21.9 / 25.2 % |
| FY22–27 avg (low) | 10.80% | 23.51% |
| FY26–27 avg (high) | 20.10% | 23.56% |
| Implied FY28–31 lo/hi avg $M/yr | 544.6 / 1,013.7 | 4,636.4 / 4,646.5 |
| FY22–25 avg TAM $M/yr | 491.5 | 2,816.2 |

Combined: FY22–25 avg $3.31B/yr (the dashed line); outyear totals lo
5.25/5.17/5.12/5.18, hi 5.62/5.55/5.70/5.77 $B — slide labels "5.3–5.6" …
"5.2–5.8"; axis max 7 holds. The submarine lo/hi window averages are nearly
identical (23.51 vs 23.56%), so the range band is almost entirely DDG-driven.

Verification: builds (DDG 24→26 tabs, subs 20→22, group-contiguity asserts
passed), validate (0 xml errors, 0 error cells, all programs + consolidated),
soffice recalc + openpyxl scans, Outlook §6 checks all OK, penetration ∈ (0,1].
A/B toggle: OBBBA off → DDG portfolio TAM 3,525.80 / subs 20,274.42 exactly
(documented pre-OBBBA values); numerator AND denominator drop together; DDG FY26
penetration 4.0× flags the designed REVIEW (denominator collapses to the ~$306M
discretionary-only TSE while AP/LLTM TAM remains) — OK at defaults.

## Deck — NEW slide `s11a_body_outsourced_bc_annual_tam.py` (s11 untouched)

Registered after s11 (deck 22→23 slides, 9 charts; chart numbering downstream
shifts automatically). One stacked `column_chart`, 10 categories FY2022–FY2031:
- Program series carry actuals ×6 + implied-LOW ×4 with per-point tints
  (sub accent2→accent3, DDG accent1→accent5), `hide_label_points` on estimate
  years (+ thin DDG actual caps, which get the accent chips).
- "Range to high" third series = None×6 + (hi−lo)×4 with the s03 hatch idiom
  (`pattern ltUpDiag`, fg accent3 / bg white). Zero deck_core changes.
- Overlays via the pinned `_PLOT_LAYOUT` + `_plot_geom()` math: stack totals
  ("lo–hi" floated at the HIGH level on estimate years); dashed verticals at
  category boundaries k=4 and k=6 spanning plot-top → BODY_B (fencing strips +
  commentary into the three bands); FY22–25 avg dashed line full plot width
  (label "FY22–25 avg: 3.3"); dashed-outline frames around the four estimate
  bars (hi top → baseline, `_bar_half_w` from gap_width math).
- Slide-local 3-entry legend (chart_legend geometry + a dashed white swatch for
  "FY28–31 estimate" — chart_legend can't draw dashed swatches).
- Penetration strips: right-aligned two-line row labels ("DDG-51 / outsourced
  %"), one program-color-outlined roundRect pill per actual FY, and one spanning
  pill per row across the outlook band ("11–20% (assumed)" / "~24% (assumed)").
- Commentary: three columns with edges derived from the band x's; outlook column
  quotes the Strategic Outsourcing narrative (attributed PB2027 SCN, COLUMBIA
  P-10). Sources line carries the estimate-methodology footnote.
- Module asserts: list lengths, totals↔labels (±0.051 for the 6.053→6.1-style
  roundings), range > 0, `max(hi) ≤ axis_max − 0.6`.

QA: build_deck.py → soffice PDF → pdftoppm at 110/200/300 dpi. Hatch caps,
dashed frames, verticals, avg line, pills, chips, legend, three-band commentary
all render; s11 (slide 12) and s12 (slide 14) unchanged. One iteration: the two
strip-row labels collided — fixed by opening the row pitch (4_405k / 4_640k) and
trimming the label boxes.

## Gotchas / notes for next time

- `scn_li_resource_summary.csv` already had FY28–31 — check it before writing a
  new P-40 extractor.
- Parse it with the `data_ap_bridge._apnum` pattern; `load_extracted_csv` keeps
  thousands commas and "-" placeholders.
- Extending `deflators.FY_RANGE` is safe: the Deflators tabs loop it (rows
  append after FY2027) and every other consumer calls `deflator_factor_cell(fy)`
  on its own FY22–27 list. Never extend a model sheet's `_FY_COLUMNS`.
- The DDG-vs-subs OBBBA gross asymmetry (constant-$ vs then-year + spillover)
  must be mirrored in any ratio that puts OBBBA in a denominator.
- DDG FY26 penetration (28.9%) is structurally high: AP/LLTM-driven TAM over a
  ship-cost denominator. With OBBBA off it exceeds 100% — that's the documented
  REVIEW state, not a bug.
- The estimate-bar recipe with zero engine work: per-point tints + a None-padded
  hatched topper series (s03 idiom) + dashed text_box frames and connector
  verticals pinned to `plot_layout`; band boundaries sit at exact k/N fractions
  regardless of gap_width.
- PB28 tripwire now has three teeth: TAM Build §5 (subs), Outlook §6 FY27/FY26
  ties (both), Source Index refresh rows. On a PB2028 refresh, re-base the FYDP
  outyears and restate the OBBBA overlay before reading the model.

## Open

- The penetration strip and outyear figures exist only on the new slide; the
  DDG/sub program decks (if rebuilt) don't carry an Outlook slide — separate
  decision.
- Slide estimate-bar styling shipped with BOTH cues (hatch + dashed frames) per
  user choice; if it reads busy in review, delete the four `_est_frames` shapes.
