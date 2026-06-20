# Session Log — submarine_outsourced_work — 2026-05-24 (session 4)

**Handoff doc for the next AI agent.** Picks up from session 3 (DoD POP +
GD 10-K + FPDS POP + methodology slide 2). Read prior logs in order:

1. `logs/2026-05-22_session_log.md` (initial workbook + FPDS/USA/SAM pipelines)
2. `logs/2026-05-23_session_log.md` (new-construction refinement + HII context)
3. `logs/2026-05-24_session_log.md` (cost-funnel reframing + primary sources)
4. `logs/2026-05-24_session_log_2.md` (methodology side deck + full-history SAM)
5. `logs/2026-05-24_session_log_3.md` (DoD POP + GD 10-K + FPDS POP)
6. This file

This session built a project-data workbook from scratch — `submarine_outsourced_construction_workbook.xlsx` — modeled on the older sibling-project workbook at `/Users/brendantoole/projects2/workbook/`. Twelve sheets total. The deck itself was discussed but not changed.

---

## 1. What this session was about

Six threads, executed in sequence:

**A. Spec review (no changes).** User asked how `DECK_BUILD_SPEC.md` should
be updated given everything the project has accumulated. Audited the spec
against the data backbone and the wiki; recommended a rewrite of §5
(slide plan) and §6 (data flow) to fold in the funnel reframing, DoD POP,
HII vs GD divergence, and primary-source backbone. **Did not edit the
spec — was an analytical exercise only.**

**B. Workbook design.** User wanted to build a project workbook (separate
from the deck). Audited research, proposed 17 sheets; user pushed back —
"way fewer, drop POP, want data sheets, look at `/Users/brendantoole/projects2/workbook/`
as architecture pattern." Re-scoped to 8 sheets matching that reference's
3-tier (Front / Data / Out) pattern.

**C. Workbook scaffold + 8-sheet build.** Copied reference's `lib.py` and
`styles.py` verbatim (one filename change). Built all 8 sheets in one
push. Iterative bug-fixes for Python 3.9 union-annotation issues, off-by-
one row refs in cross-sheet formulas, off-by-one in Top_Vendors lookup.

**D. Styling tightening.** User: "x markers shouldn't be on every row,
some cols too narrow, Va/Col/All total cells have weird interior borders."
Removed `S_DEFAULT` "x" cells from data rows (only banner rows should
have the section-collapse marker). Widened FY/PIID columns. Replaced
`S_USD_M_TOTAL` (top border for totals ROWS) with `S_USD_M_BOLD` on the
per-row totals COLUMN inside the body — the top-border style was meant
for a single subtotal row, not for every body row's totals cell.

**E. DoD_POP sheet added (9 sheets).** User: "drop POP" → then "actually
make a DoD_POP sheet." Built it: per-bucket POP rollup (7 TAM-relevant
buckets + TOTAL) and 43 TAM-relevant action detail rows. Updated Cover
tab map + caveat #8.

**F. Font-color audit (audit-trail convention).** User asked to verify
hardcoded vs derived vs cross-sheet links are using correct font colors.
Added new style `S_PCT1_INPUT` (0.0% blue+yellow). Refactored Funnel's
`_funnel_row` to route through `write_row` → auto-applies `LINK_OVERRIDES`
for pure cross-sheet refs (green font). Switched in-sheet derived formulas
to `S_FORMULA` (blue fill). Switched all hardcoded CSV-loaded numeric
values to `*_INPUT` styles (yellow fill + blue font).

**G. Wiki alignment audit + 3 more sheets (12 total).** User asked whether
workbook aligns with `wiki_submarines/` and what's missing. Read the
16-chapter wiki, found 3 gaps (LLTM/AP detail, Prime 10-K segment data,
MIB exclusion audit trail). Built `LLTM_AP`, `MIB_Excluded`, `Prime_10K`
sheets. Updated `sheets/__init__.py` registry and Cover tab map (now 12
rows; calc workflow + caveats shifted down).

**H. Tab order + color audit.** User: tabs in a group should share one
color and be contiguous. Audited; fixed Cover from dark navy to match
References, fixed MIB_Excluded from gold to gray, changed Cover tab-map
tier for Inputs from "Data" to "Editable".

---

## 2. The workbook

### Final state

**Path:** `/Users/brendantoole/projects2/submarine_outsourced_work/submarine_outsourced_construction_workbook.xlsx`
**Size:** 49,926 bytes
**Sheets:** 12

| # | Tab | Group | Color | Source CSVs |
|---|---|---|---|---|
| 1 | Cover | Front | `#2F5573` navy | (none — narrative + audit-trail key + tab map) |
| 2 | References | Front | `#2F5573` navy | `industry_baseline_citations.csv` + `exec_commentary_makebuy.csv` |
| 3 | Inputs | **Editable** | `#A37A29` gold | (none — editable parameters) |
| 4 | SCN_Annual | Data | `#5C5C5C` gray | `cost_funnel_summary.csv` |
| 5 | LLTM_AP | Data | `#5C5C5C` gray | `scn_p10_ap_buckets.csv` |
| 6 | Subaward_Annual | Data | `#5C5C5C` gray | `nc_annual_by_piid.csv` + inline PIID-meta |
| 7 | MIB_Excluded | Data | `#5C5C5C` gray | (hardcoded from wiki Ch 10 + `nc_scope_summary.json`) |
| 8 | Top_Vendors | Data | `#5C5C5C` gray | `nc_lifetime_vendors.csv` + `entity_naics_lookup.csv` |
| 9 | DoD_POP | Data | `#5C5C5C` gray | `dod_announcement_pop.csv` (filtered to TAM-relevant) |
| 10 | Prime_10K | Data | `#5C5C5C` gray | `hii_context.csv` + `edgar_research/gd_marine_systems_segment_reconciled.csv` |
| 11 | Funnel | Out | `#2E7D32` green | (cross-sheet formulas) |
| 12 | Charts | Out | `#2E7D32` green | (stub — title + 1 section banner) |

### Architecture

Mirrors `/Users/brendantoole/projects2/workbook/` exactly:

```
submarine_outsourced_work/
├── build_workbook.py                # launcher
└── workbook/
    ├── __init__.py
    ├── lib.py                       # stdlib OOXML primitives (cell, row,
    │                                  worksheet, banner_row, write_row,
    │                                  build_table, load_csv, package XML
    │                                  builders, build() entry point)
    ├── styles.py                    # CELL_XFS list + constants + LINK_OVERRIDES
    └── sheets/
        ├── __init__.py              # SHEETS = [(name, render_fn), ...]
        ├── a_cover.py
        ├── a_references.py
        ├── d_inputs.py
        ├── d_scn.py
        ├── d_lltm.py                # NEW this session
        ├── d_subawards.py
        ├── d_mib.py                 # NEW this session
        ├── d_vendors.py
        ├── d_pop.py                 # NEW this session (DoD_POP)
        ├── d_prime10k.py            # NEW this session
        ├── o_funnel.py
        └── o_charts.py
```

Naming convention: `a_` (front), `d_` (data), `o_` (output). Matches reference
project.

### Build

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work
python3 build_workbook.py
```

Outputs `submarine_outsourced_construction_workbook.xlsx` at project root.
Stdlib only — no openpyxl, no third-party deps. Zip archive of hand-built
XML. Opens cleanly in LibreOffice and Excel.

### Per-sheet content

**Cover** — orientation, audit-trail key (yellow=input, blue=derived,
green=total, blue-font=hardcoded, green-font=cross-sheet link), tab map
(12 rows with group / tier), 5-step calc workflow, 9-row caveats.

**References** — 30 GAO/CRS/CBO statistics + 21 exec/Navy quotes inline
(Kastner +30% YoY, Navy 10→50%, Novakovic supply-chain gating item).

**Inputs** — BC outsourced band (50/60/65%), HII team-build shares (50%
Va / 22% Col / 30% midpoint for sub portion), FY25 lag uplift (2.0×),
FY26 lag uplift (6.0×), window start/end FY, 8 read-only anchor figures.

**SCN_Annual** — Va + Col blocks, FY20-FY27 cols. Rows: Total Ship Cost
/ Plans / 4× GFE sub-components / Other / Change Orders / Basic
Construction. Multi-vintage reconciled (most-recent-PB-where-FY-is-actual).

**LLTM_AP** — Va (6 buckets) + Col (8 buckets), FY20-FY27 cols. Rows:
Nuclear plant LLTM / Shipbuilder-procured LLTM / Plans-SIB / Missile
compartment LLTM / EOQ / Ordnance LLTM / Electronics LLTM / HM&E LLTM /
Propulsor LLTM. Each block has Total Plus CY AP formula row. Combined
shipbuilder-procured LLTM (Va CFE + Col BC-3/5/7) bottom section — the
wiki's "most addressable supplier bucket." Trajectory matches wiki Ch 5
exactly: $0.7B (FY21) → $2.5B (FY25) → $2.5B (FY27).

**Subaward_Annual** — 15-PIID legend (PIID / class / prime / label) +
per-FY × per-PIID matrix (FY16-FY26 rows × 15 PIID cols). Per-row Va
total / Col total / All-class total = formula (sum of PIIDs by class).
Lifetime totals row at bottom (`=SUM(C27:C37)` etc.).

**MIB_Excluded** — 3 excluded UEIs (BlueForge / Training Modernization
Group / Institute for Advanced Learning and Research, ~$4.25B lifetime).
BlueForge per-FY ramp showing FY23 $1,514M + FY24 $2,659M spike. BPMI
Columbia Class IBI inclusion note ($528M lifetime, distinct from
BlueForge). AML3D as first publicly-named BlueForge downstream
sub-recipient.

**Top_Vendors** — top 50 lifetime vendors with parent-UEI rollup,
lifetime $M, records count, FY count, FY range, PIID count, primary
NAICS, NAICS-4 description, NAICS sector label, country, lookup status.
Autofilter on the header row.

**DoD_POP** — per-bucket $-weighted POP rollup (7 TAM-relevant buckets +
TOTAL = 21.9% EB / 16.2% HII / 51.8% Other-US / 0% foreign). TAM-
relevant action detail (43 rows sorted by $ desc) with Date / $M /
program / work type / prime / PIID / EB% / HII% / Other-US% / Foreign% /
Locations.

**Prime_10K** — HII NNS segment FY19-FY25 (revenue / op income / margin /
implied sub @ 25/30/35% / FFATA-visible HII-as-sub / gap ratio 109× →
9,810×). GD Marine Systems segment FY19-FY25 (revenue / op income /
margin / capex / D&A / identifiable assets).

**Funnel** — Va + Col blocks. Per FY: Total Ship Cost − Plans − GFE
(sum of 4) − Other+CO = Basic Construction → Outsourced Low / Mid / High
(BC × Inputs!band) → FFATA-visible (sum from Subaward_Annual) → Unseen
Δ (Mid − Visible) → FFATA/BC %. All formulas. Editing Inputs!band_mid
ripples through every Funnel + Charts cell.

**Charts** — stub. Title row + 1 section banner ("Block 1 — TBD"). User
hasn't decided which deck charts to build; will add think-cell paste-
ready blocks here when picked.

---

## 3. Style convention (verified across sheet types)

Per the Cover audit-trail key:
- **yellow fill** = Editable input (with blue font)
- **blue fill** = Derived value (formula in cell)
- **green fill** = Row/column total
- **blue font** alone = Hardcoded literal (typed number, not formula)
- **green font** = Cross-sheet link (`=Sheet!Cell`)

Applied throughout:

| Cell type | Style ID | Where |
|---|---|---|
| Hardcoded CSV-loaded numbers | `S_USD_M_INPUT` (16) / `S_INT_INPUT` (23) / `S_PCT1_INPUT` (59) — yellow + blue | SCN_Annual data, Subaward_Annual per-PIID, Top_Vendors numbers, DoD_POP rollup + detail, LLTM_AP buckets, MIB_Excluded, Prime_10K |
| Pure cross-sheet single-cell refs | `S_LINK_USD_M` (30) — green font, no fill, auto via `LINK_OVERRIDES` | Funnel Total Ship Cost / Plans / BC / FFATA-visible rows |
| In-sheet derived formulas | `S_FORMULA` (14) — black font + light blue fill | Funnel GFE, Other+CO, Outsourced Low/Mid/High; Subaward per-row Va/Col/All totals |
| Subtotal / totals rows | `S_USD_M_TOTAL` (19) — bold + top border | Funnel BC row (subtotal of deductions); Subaward Lifetime row; DoD_POP TOTAL row $M; LLTM_AP "Total Plus CY AP" rows; LLTM_AP Combined Va+Col row |
| Subtotal-emphasis (no border) | `S_USD_M_SUBTOTAL` (37) — bold, no fill | Funnel Unseen Δ row |
| FY identifier in narrow cell | `S_BOLD` (1) — plain integer, no comma | Subaward_Annual FY column; Prime_10K FY columns; MIB BlueForge FY column |
| Percentages (computed in-sheet) | `S_PCT` (9) — black 0% | Funnel FFATA/BC % row |

### S_PCT1_INPUT added this session

`CELL_XFS[59]` — 0.0% format with blue font + yellow fill. Didn't exist
before. Needed for the DoD_POP rollup percentages (which preserve 0.1
decimal precision unlike the existing `S_PCT_INPUT` which rounds to whole
percent). Exported via `lib.py` re-export.

### Refactored `_funnel_row`

Previous version called `cell()` directly with explicit style — bypassed
the `LINK_OVERRIDES` auto-detection in `write_row`. Refactored to route
through `write_row(start_col=1, ...)`, which means pure `=Sheet!Cell`
formulas auto-apply the green-font override. In-sheet computations like
`=A+B+C` don't match the LINK_RE regex so they keep the explicit style
the caller passes (e.g., `S_FORMULA` for the GFE sum row).

---

## 4. Files written this session

### Workbook pipeline

| File | Lines | Purpose |
|---|---|---|
| `build_workbook.py` | 11 | Launcher at project root |
| `workbook/__init__.py` | 8 | Package docstring |
| `workbook/lib.py` | ~510 | Copied from reference workbook with one change: `OUT` filename |
| `workbook/styles.py` | ~430 | Copied from reference workbook + added `S_PCT1_INPUT` at index 59 |
| `workbook/sheets/__init__.py` | ~75 | SHEETS registry (12 entries, in tab order) |
| `workbook/sheets/a_cover.py` | ~245 | Cover sheet with 12-row tab map |
| `workbook/sheets/a_references.py` | ~130 | References sheet (30 GAO/CRS + 21 exec quotes) |
| `workbook/sheets/d_inputs.py` | ~200 | Inputs sheet (BC band + HII shares + lag uplift + anchors) |
| `workbook/sheets/d_scn.py` | ~165 | SCN_Annual sheet (Va + Col P-5c blocks) |
| `workbook/sheets/d_lltm.py` | ~205 | LLTM_AP sheet (Va + Col P-10 blocks + Combined) |
| `workbook/sheets/d_subawards.py` | ~210 | Subaward_Annual sheet (legend + FY × PIID matrix) |
| `workbook/sheets/d_mib.py` | ~190 | MIB_Excluded sheet (UEIs + BlueForge ramp + BPMI IBI + AML3D) |
| `workbook/sheets/d_vendors.py` | ~145 | Top_Vendors sheet (top 50 with NAICS + state) |
| `workbook/sheets/d_pop.py` | ~230 | DoD_POP sheet (rollup + TAM detail) |
| `workbook/sheets/d_prime10k.py` | ~165 | Prime_10K sheet (HII NNS + GD MS segment tables) |
| `workbook/sheets/o_funnel.py` | ~305 | Funnel sheet (Va + Col bridge with formulas) |
| `workbook/sheets/o_charts.py` | ~40 | Charts sheet (stub) |

### Logs

- `logs/2026-05-24_session_log_4.md` (this file)

### No CSVs added this session

All sheets consume existing CSVs in `extracted/` and `edgar_research/`.
No new data pulls.

---

## 5. Bugs encountered + fixed this session

| Bug | Symptom | Fix |
|---|---|---|
| Python 3.9 doesn't support `float \| None` syntax | `TypeError: unsupported operand type(s) for \|: 'type' and 'NoneType'` on import | Added `from __future__ import annotations` to d_scn.py + o_funnel.py + d_pop.py + d_lltm.py + d_prime10k.py + d_mib.py |
| Funnel SCN_Annual Col block row refs off by one | Col-block formulas pointed at wrong rows (Total=21 instead of 22, BC=29 instead of 30) | Recounted layout — Va block ends row 17 (after 9-row body), Col block starts row 19 (banner) → Col Total at row 22, Col BC at row 30. Updated constants. |
| Funnel Subaward_Annual data start row off by two | FFATA-visible cells pulled from wrong FY | Subaward matrix has legend rows 5-21, banner 24, header 25, sub-row 26, then FY2016 data at row 27 (not row 29). Fixed `SUB_DATA_START_ROW = 27`. |
| Charts → Top_Vendors first vendor row off by one | Rank 1 (Northrop) missing; Block 2 showed rank 2 (Leonardo) first | Top_Vendors header at row 5, data starts row 6 (not row 7). Changed loop `vendor_row = 5 + i`. |
| `S_USD_M_TOTAL` on every body-row total cell | Va/Col/All total columns had apparent interior borders (single top border per cell) on every row | `S_USD_M_TOTAL` (top border) is for a single totals ROW, not every row's totals COLUMN. Swapped per-row totals to `S_USD_M_BOLD` and later to `S_FORMULA` (blue fill — they're in-sheet computed formulas). Kept `S_USD_M_TOTAL` on the actual Lifetime row at the bottom. |
| `S_INT_INPUT` on FY column gives "2,019" with thousands comma | FY values rendered with comma in Prime_10K / MIB BlueForge ramp | numFmtId=169 (`#,##0`) adds thousands separator. FYs are categorical labels not measurements; switched to `S_BOLD` (plain integer, bold, no number format) for FY columns. |
| Cover row collisions when adding new sheets | Calc workflow banner clashed with Tab map's expanded rows | Each time the tab map grew (8→9→12 rows), shifted calc workflow + caveats section row numbers down accordingly. Final positions: Calc workflow banner at row 27, caveats banner at row 36. |
| "x" markers on every data row | Visual noise — banner-row "x" was being added to body rows too | The `mark_collapsible=True` on `banner_row()` puts "x" in column A (the gutter) as a section-collapse marker. Data rows should NOT have this — they just use `outline_level=1` to join the collapsible group. Removed all `cell(cref(r, 0), value="x", style=S_DEFAULT)` lines from data-row cell lists. |
| Column widths too narrow | PIID column showed "N00024" (cut at 6 chars); Work type "lltm_earl" (cut at 9 chars) | Bumped Subaward col B 6→14 (PIID legend), PIID cols 11→14, total cols 11→14. SCN/Funnel FY cols 12→13. DoD_POP $M cols to fit "$18,104.0M". |
| MIB_Excluded was tab-colored gold (matched Inputs) | Tab color inconsistent with Data tier | Changed `tab_color="A37A29"` → `"5C5C5C"` so it sits visually inside the Data tier alongside the other 6 data sheets. |
| Cover was dark navy (`1F3A5F`) but References was lighter navy (`2F5573`) | Front tier should share one color | Changed Cover `tab_color="1F3A5F"` → `"2F5573"`. |

---

## 6. Caveats specific to this workbook

(Prior session caveats still apply.)

1. **Charts is a stub.** Title row + one section banner. No data blocks
   yet. User hasn't decided which think-cell charts to build.

2. **Funnel formula references are by row number, not by name.** Move a
   row inside SCN_Annual or Subaward_Annual without updating the
   `SCN_VA_TOTAL_ROW = 8` etc. constants in `o_funnel.py` and the
   formulas will silently point at the wrong cell. The constants are
   documented inline with the layout assumption.

3. **DoD_POP TAM gate is selective.** The detail table shows only the 43
   rows where `is_sub_new_construction_tam == 'yes'`. The full 658-row
   `dod_announcement_pop.csv` is preserved unchanged; surfacing the rest
   would require either a new sheet or a relaxed filter.

4. **Wiki Ch 7 cites a 2022-12-21 Columbia LLTM/SIB action at $5.13B
   (75/25/0 split) as the pre-supply-chain-crunch anchor.** That action
   IS in the raw `dod_announcement_pop.csv` but the program classifier
   tagged it `non_sub`, so it falls outside the TAM gate. Wiki treats
   it as Columbia. One-off reclassification would surface it; not
   blocking the workbook.

5. **MIB BlueForge per-FY figures are hardcoded** in d_mib.py from the
   wiki Ch 10 narrative (FY23 $1,514M, FY24 $2,659M, others $0). Not
   computed from raw subaward data. Stable; documented in logs and wiki
   so re-derivation is straightforward if needed.

6. **HII implied submarine portion is computed at 25/30/35% scenarios
   from the NNS segment revenue** — industry-analyst estimate, not
   primary-sourced. The 30% midpoint is the headline; HII does not
   separately disclose submarine-vs-carrier within the NNS segment.

7. **No new sheets reference each other.** LLTM_AP, MIB_Excluded,
   Prime_10K are all self-contained data sheets. Funnel does NOT pull
   from them; they're audit-trail material for the wiki narrative.

8. **`S_PCT1_INPUT` style index = 59.** If `styles.py` `CELL_XFS` is
   re-ordered, this index breaks. Documented inline; the list grows
   append-only.

---

## 7. Open items / next steps

In order of value:

1. **Build out Charts.** User-decision blocker — which deck charts to
   pre-build as think-cell paste-ready blocks. Current stub has the
   structure ready; just need to know which charts.

2. **Reclassify the Dec 2022 Columbia LLTM/SIB action** ($5.13B, currently
   `non_sub`) so DoD_POP includes it. Wiki Ch 7 treats it as the historical-
   trajectory anchor for the pre-supply-chain-crunch era — 75% EB / 25%
   HII / 0% supplier. Pairs with the 2026-05-11 Va Block VI LLTM (0/2/98)
   to show the outsourcing acceleration in two data points. Quick fix in
   `reclassify_dod_action_subrelevance.py`.

3. **Update DECK_BUILD_SPEC.md.** Session covered the analytical audit
   (see Section 1.A above) but didn't edit the spec file. §5 (slide plan)
   and §6 (data flow) need rewrites to fold in the funnel reframing, DoD
   POP, HII vs GD divergence, and primary-source backbone. The workbook
   is now the underlying data layer that a rewritten spec can point at.

4. **Add `--audit` to build_workbook.py.** Currently the build just
   reports sheet sizes. Could add post-build validation: scan for any
   text-color other than 000000 / 0000FF / 009E47, any fill outside the
   approved palette, any numFmt outside the approved list. Catches style
   drift early.

5. **Consider an "Outside-EB %" derived column on DoD_POP rollup.**
   Wiki Ch 7 headlines 78% Outside-EB = 100% − 21.9% EB. Our rollup
   shows the per-bucket components but not the derived figure. One extra
   column, simple addition.

6. **Workbook is reproducible but the input CSVs are not regenerable
   from the workbook itself.** If `extracted/cost_funnel_summary.csv`
   etc. change, the workbook reflects the changes on next build; if the
   workbook is shared without those CSVs, it still opens because all
   values are hardcoded at build time. Acceptable — but the user should
   know the workbook is a SNAPSHOT, not a live view.

7. **Methodology side deck integration.** The standalone
   `deck_methodology/` side deck (5 slides, built 2026-05-24 session 2)
   doesn't reference the workbook. Could add a final slide pointing at
   the workbook + its sheet map. Or update the workbook Cover to
   cross-reference the side deck. Either-or.

---

## 8. Hand-off — re-run and things to NOT do

### To rebuild the workbook from scratch

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work
python3 build_workbook.py
```

Outputs `submarine_outsourced_construction_workbook.xlsx` at project root
(~50KB). Stdlib only.

### To preview without Excel

```bash
soffice --headless --convert-to pdf --outdir /tmp/workbook_preview \
    submarine_outsourced_construction_workbook.xlsx
```

LibreOffice paginates wide sheets across multiple PDF pages — not a true
WYSIWYG of how Excel renders. Use Excel for the canonical view.

### Things to NOT do

- **Don't add `S_DEFAULT` "x" cells to data rows.** "x" is the section-
  collapse marker that goes in column A on banner rows only (via
  `mark_collapsible=True`). Adding it to body rows creates visible
  clutter in the gutter.

- **Don't use `S_USD_M_TOTAL` on every total cell within a body row.**
  It has a top border that creates apparent interior borders across the
  rows. Use it only on the actual single totals row at the bottom of a
  block. For per-row computed totals, use `S_FORMULA` (in-sheet derived)
  or `S_USD_M_BOLD` (just bold).

- **Don't use `S_INT_INPUT` for FY values.** numFmtId=169 (`#,##0`)
  adds a thousands comma → "2,019" instead of "2019". Use `S_BOLD`
  (plain integer, bold, no number format) for categorical FY cells.

- **Don't reorder `CELL_XFS` in styles.py.** Style constants are
  position-based. Only append new entries to the end (with new constants
  numbered accordingly).

- **Don't move rows inside SCN_Annual or Subaward_Annual without
  updating the constants in `o_funnel.py`.** The Funnel sheet's
  cross-sheet formulas hardcode row numbers (e.g., `SCN_VA_BC_ROW = 16`).

- **Don't change tab colors arbitrarily.** The four groups (Front /
  Editable / Data / Out) each share one color. Adding a sheet to a
  group means using that group's color. Adding a new tab outside the
  current groups means picking a NEW unique color and explicitly
  documenting the group.

- **Don't refactor `_funnel_row` to bypass `write_row`.** The whole
  point of routing through `write_row` is to auto-apply `LINK_OVERRIDES`
  for pure cross-sheet refs. If you go back to direct `cell()` calls,
  cross-sheet links lose the green-font convention.

### Memories saved this session that affect future work

None saved — all session-specific findings are in this log + inline
comments in the new sheet modules.

---

## 9. Final state of task list

| # | Subject | Status |
|---|---|---|
| 1 | Scaffold workbook pipeline (lib + styles + sheets/__init__ + launcher) | ✓ completed |
| 2 | Build Cover sheet | ✓ completed |
| 3 | Build References sheet | ✓ completed |
| 4 | Build Inputs sheet | ✓ completed |
| 5 | Build SCN_Annual data sheet | ✓ completed |
| 6 | Build Subaward_Annual data sheet | ✓ completed |
| 7 | Build Top_Vendors data sheet | ✓ completed |
| 8 | Build Funnel output sheet | ✓ completed |
| 9 | Build Charts output sheet | ✓ completed (subsequently stripped to stub) |
| 10 | Run build + verify output | ✓ completed |
| 11 | Build LLTM_AP sheet | ✓ completed |
| 12 | Build Prime_10K sheet | ✓ completed |
| 13 | Build MIB_Excluded sheet | ✓ completed |
| 14 | Update sheet registry + Cover tab map (12 sheets) | ✓ completed |
| 15 | Rebuild + verify all 12 sheets | ✓ completed |

---

## 10. Quick orientation for next agent

**If user asks "where's the workbook":**
`/Users/brendantoole/projects2/submarine_outsourced_work/submarine_outsourced_construction_workbook.xlsx`.
Rebuild with `python3 build_workbook.py` from project root.

**If user asks "what's the workbook architecture":**
Mirror of `/Users/brendantoole/projects2/workbook/` (the older sibling-
project workbook). Stdlib-only raw OOXML. `lib.py` has primitives
(cell, row, worksheet, banner_row, write_row, build_table, load_csv,
package XML builders). `styles.py` has CELL_XFS list + style constants
+ LINK_OVERRIDES. `sheets/__init__.py` registers the 12 tab modules in
tab order. Each `sheets/<file>.py` exports a `render_xxx()` function
returning a worksheet XML string.

**If user asks "what's on each sheet":**
See Section 2 of this log, or open the workbook's Cover sheet — the tab
map is the canonical reference.

**If user asks "does the workbook align with the wiki":**
Yes. Audited in Section 1.G. Workbook covers every wiki chapter that
has tabular data: Ch 2-4 → SCN_Annual; Ch 5 → LLTM_AP; Ch 6 →
Inputs+Funnel; Ch 7 → DoD_POP; Ch 8 → Subaward_Annual; Ch 9 →
Top_Vendors; Ch 10 → MIB_Excluded; Ch 11+15 → Prime_10K; Ch 13-14 →
References (quotes + GAO/CRS citations); Ch 16 → Cover.

**If user asks "what changes Funnel numbers":**
Editing `Inputs!C7-C9` (BC outsourced band Low/Mid/High) ripples
through every Outsourced Low/Mid/High cell on Funnel. Editing any
SCN_Annual data cell ripples through the corresponding Funnel column.
Editing Subaward_Annual per-PIID cells ripples through the per-FY
Va/Col/All totals AND the Funnel's FFATA-visible row.

**If user asks "is the deck built":**
No. The deck (per `DECK_BUILD_SPEC.md`) is still unbuilt. The
methodology side deck at `deck_methodology/` is built (5 slides) and
ships clean. The main deck spec was reviewed analytically this session
but not edited.

**If user asks "what about DoD POP coverage":**
2022-07 → 2026-05 (34 months). 658 paragraphs scraped, 43 TAM-relevant.
Pre-2022 not reachable via available routes (Wayback CDX returns few
defense.gov contract URLs pre-2022). Workbook DoD_POP sheet filters to
TAM-relevant; raw 658-row CSV preserved at
`extracted/dod_announcement_pop.csv`.

**If user asks "what's the next thing to do":**
Either (a) decide which charts to build on Charts sheet, (b) reclassify
the Dec 2022 Columbia LLTM action so DoD_POP includes it, or
(c) update DECK_BUILD_SPEC.md to fold in the data backbone the workbook
now codifies. Section 7 has the prioritized list.
