# 2026-06-10 — Front-row text polish + z_ChartData_OutsourcedBC think-cell layout fixes

## Deck (deck_consolidated/slides/) — TEXT-ONLY edits, no chart/geometry changes

### fr1_body_outsourced_bc_walk.py (deck slide 2)
- **Ledger overflow fixed**: the step/rationale table ran 5,257,800 EMU in a
  4,498,400 EMU body zone (~0.6" past BODY_B). Rationale copy tightened row by
  row (GFE merged to one bullet, Prime BC / Other non-BC compressed); table now
  4,297,680 EMU with ~200k slack. 9pt kept.
- **Takeaway de-parenthesized** (user: no parens in title headings; rephrase,
  don't just strip): "Across FY22–FY27, total ship spend narrows to an
  annualized ~$1.1B of outsourced work for DDG-51 and ~$3.0B for submarines."
- **Less: Prime AP/LLTM rationale rewritten** to resolve user confusion (both
  programs show an em-dash for different reasons): now two lead-in bullets —
  DDG-51: P-10 EOQ base is vendor-purchased material, primes retain none, $0
  removed, full $1.0B flows to Outsourced BC; Submarines: no AP/LLTM stream
  exists. Supersedes the manager's stale 80%/85% draft note (pre-restate).

- **Ledger borders restyled** to the manager's vDraft table rules (deck_mini
  slide04_tables.xml): 0.5pt gray 808080 horizontal rules only, same weight
  under the header, none under the last row (was 1.5pt/1pt black).

### fr2_body_worktype_by_program.py (deck slide 3)
- Takeaway now carries both pool sizes per the manager's draft framing, with
  restated numbers: "Electrical power leads the ~$18.1B submarine pool;
  machining leads the ~$6.4B DDG-51 pool."
- **Methodology ledger synced to the same-day yard-gate restate**: stage 2
  "PIID scope" → "PIID gate" ("Gate to yard construction PIIDs per program
  (BIW / Ingalls; GDEB); GFE chains drop out") — the old copy described the
  pre-gate corpus where GFE/combat-system chains voted; stage 7 now says the
  shares are "per class and per FY". Stages 1/3-6 and the findings were
  already accurate. Finding 1's evidence bullet dropped (redundant with
  stages 2-4, and the findings block was running into the sources line).

### fr3_body_outsourced_bc_annual_tam.py (deck slide 4)
- `_SECTION` "Market Sizing" → "Executive Summary" (matches the manager's
  breadcrumb and the other three front-row slides).
- `_TOPIC` "Outsourced Basic Construction (Annual TAM)" → "Outsourced Basic
  Construction Annual TAM" (no parens in title headings).
- Takeaway hedges the outlook per the manager's draft: "... and is expected to
  hold $4.3–5.7B a year through FY2031."

fr4 unchanged (its annual-specific takeaway supersedes the manager's
copy-pasted cumulative one; legend "Unassigned" from the draft is folded into
Residual under the gated-vector methodology).

## Workbook (workbook_consolidated/sheets/z_chart_data_outsourced_bc.py)

- **§1 DDG walk split to two series rows**: "In-year" 36.5920922 base +
  "AP/LLTM (P-10 EOQ)" 1.04233 stacked on the Total Ship Spend column (its own
  row = its own think-cell color, the slide's hatched slice); "e" subtotals
  cumulate both rows so BC (22.5907) and the endpoint (6.4217) are unchanged.
  §2 submarine walk stays single-row (no AP/LLTM stream).
- **§3 column order** → DDG-51, Columbia, Virginia (user-requested submarine
  swap; slide modules intentionally NOT changed).
- **§4 restructured to the think-cell column-per-bar idiom** (per the
  manager's vDraft slide-4 embedded datasheet: columns = bars, rows = stacked
  series), then iterated per user across several rounds (spacer columns
  added then removed; implied-low+range split → single high chunk → final
  low/high split below). FINAL layout: 30 contiguous slots = [DDG-51,
  Virginia, Columbia] per FY x 10 FYs, NO spacer columns (cluster gaps set in
  think-cell); FY label over each cluster's middle (Virginia) column. Rows:
  FOUR per class, grouped Columbia / Virginia / DDG-51, stack order = row
  order (first datasheet row = bottom segment, confirmed from the manager's
  vDraft chart OOXML):
    "X outsourced"      FY22-27 actuals;
    "X outsourced low"  FY28-31 implied low (bottom of forecast bars);
    "X outsourced high" FY28-31 INCREMENT (high - low), its own
                        color-codable segment - suppress its data label
                        (it reads the increment) and use the side table's
                        lo-hi strings;
    "X retained spend"  ONE row, both eras: FY22-27 remainder + FY28-31
                        rest-to-FYDP-gross (gross = implied low /
                        assumed-low penetration) - no "FYDP"/"estimate"
                        qualifiers in labels (the slide's "Forecasted" box
                        carries that context).
  Verified: Va FY28 stacks 2.551 + 0.765 + 7.517 = 10.833 = FYDP gross;
  FY28 bar totals 3.865 DDG / 10.833 Va / 9.732 Col; historicals still total
  ship spend (FY24: 5.712 / 11.833 / 11.116). An UNHIGHLIGHTED side table
  (plain cells, 2 columns right of the rectangle; `_paste_block` grew an
  `annex` option) carries the FY28-31 "lo–hi" label strings per class for
  both outsourced and retained spend. `_NCOLS` 11 → 31.
- **§8-§10 merged into ONE §8 table** (first reordered DDG/Col/Va as three
  blocks, then merged on user request "1 table for 1 chart", then iterated
  through class-grouped and FY-clustered absolute-$ layouts; both read badly
  - Columbia's biennial gap punches holes and the 3-6x class scale spread
  crushes the small vessels' mix). FINAL design (recommended, user approved):
  **100% stacked mix chart** - 9 bars vessel-grouped DDG-51 FY22-25 |
  Virginia FY22-25 | Columbia FY2024 ONLY (unfunded years omitted, no
  placeholder holes), one blank spacer column between vessel groups; rows =
  the eight buckets in absolute $B (think-cell 100% mode normalizes and
  computes % segment labels; zero cells blank). Row order = stack order:
  the seven named buckets DESCEND by total dollars (Electrical 3.02, Piping
  2.63, Structural 2.32, Machining 1.81, HVAC 0.67, Coatings 0.59, Castings
  0.53) with **Residual pinned last = top cap on every column** (2.39; one
  global order per chart - per-column re-sorting is impossible in a stacked
  series; do NOT use think-cell segment sorting). Annex side table carries
  the bar $B totals (= column label values; a 100% chart shows no absolute
  height). Bar sums tie to the §4 annual fills.
- **§7 restated per class** (was the pre-fr3 blended submarine strip, which
  matches nothing on the slide): Virginia actual 23/24/27/19/20/26%, assumed
  24–31%; Columbia actual 13/—/15/14% (blank unfunded years), assumed 13–17%.
  Actuals = §4's own fill/(fill+remainder); low = class FY22–25 dollar-weighted
  average; high = low x 1.30. Ties to fr3's strip labels exactly.

## Verification

- Workbook build clean after every iteration; 0 xml errors; openpyxl dumps
  confirm §1 walk rows, §3 order, §4 stack arithmetic, §7 per-class
  penetration, §8 bar sums and bucket ordering.
- All blocks cross-checked numerically against fr1–fr4 module data
  (walk endpoints 6.4217 / 18.1338; §3 = fr2 buckets; §4 = fr3 fills /
  remainders / hi-lo bounds; §5 = 3.4902; §8 = fr4 matrices). Only §7 was
  stale at session start.
- Deck build clean (25 slides, 13 charts); slides 2–5 rendered to PNG — ledger
  inside the body zone, titles/breadcrumbs as above.
- NOTE: the workbook §3/§4/§8 layouts now differ from the fr2/fr3/fr4
  native-chart slide modules by design (user: charts will be rebuilt in
  think-cell from the workbook; do not update the slide chart modules). The
  fr4 slide is still the absolute-$ three-panel view while workbook §8 is the
  100% mix design; a fr4 title for the mix view was proposed but NOT applied
  ("Outsourced Basic Construction Work-Type Mix | Machining anchors a third
  or more of DDG-51 demand every year, while the submarine lead rotates among
  structural, electrical, and piping work with award timing").
