# Session Log — submarine_outsourced_work — 2026-05-24 (session 2)

**Handoff doc for the next AI agent.** This session ran 2026-05-24 evening / overnight,
picking up from the session 1 cost-funnel reframing. Read prior logs first in order:

1. `logs/2026-05-22_session_log.md` (initial workbook build)
2. `logs/2026-05-23_session_log.md` (new-construction refinement + HII context)
3. `logs/2026-05-24_session_log.md` (cost-funnel reframing + primary-source research)
4. This file

This session did two distinct things: (A) built a separate methodology-only PPTX
build pipeline; (B) ran an overnight full-history SAM.gov pull to close the
pre-FY20 visibility gap flagged in the 2026-05-22 caveats.

---

## 1. What this session was about

**Thread A — methodology-only side deck pipeline.** User wanted a personal
4-slide PPTX that documents the methodology (not the findings) of the
submarine outsourcing analysis. Same styling as the main deck spec
(`DECK_BUILD_SPEC.md`) but no numbers, just the framework. Centerpiece: a
MECE tree of program $ → addressable supplier opportunity.

**Thread B — overnight full-history SAM pull.** Removed the FY20-FY26 window
from the SAM subaward script and re-ran for all 17 PIIDs to capture pre-FY20
activity that was invisible to the windowed pull (particularly Virginia Block
IV, which had zero records in the window despite having real pre-FY20
activity per FPDS).

---

## 2. Methodology deck pipeline — what was built

### Directory layout

```
deck_methodology/
├── build.py                  # entrypoint
├── style.py                  # palette + typography tokens (mirror of DECK_BUILD_SPEC §3.1)
├── primitives.py             # text/shape/table/tree primitives + post-process helpers
├── slides/
│   ├── __init__.py
│   ├── s01_framing.py        # MECE tree (5 levels, BC emphasized)
│   ├── s02_sources_scope.py  # 9-row data sources table + scope-rules callout
│   ├── s03_cleaning.py       # 3 callouts: SCN reconciliation / parent-UEI / HII triangulation
│   └── s04_caveats.py        # 8 bulleted caveats with bold leads
└── out/
    ├── methodology_deck.pptx     # the deliverable
    └── preview/methodology_deck.pdf  # auto-generated for visual review
```

### Architectural decision: python-pptx + raw OOXML for the 10%

The main deck spec proposes **pure raw OOXML** (handcrafted template.pptx
shell + hand-written XML slide bodies). This methodology deck is the
**pragmatic version**: python-pptx for the 90% (titles, text boxes, tables,
connectors, tree node rectangles), drop down to raw lxml.etree for the 10%
python-pptx doesn't cleanly expose:

| Layer | Where raw OOXML is used |
|---|---|
| Cell-level borders on tables | `_set_cell_bottom_border`, `_suppress_all_cell_borders` |
| Table theme style override | `_strip_table_theme` (empties `<a:tblPr>` banding flags) |
| Per-shape shadow killing | `_kill_shadow` (empties `<a:effectLst>` on a shape) |
| Global shadow strip post-save | `strip_all_shadows` in build.py (post-process on saved .pptx zip) |

Everything else (titles, footers, text boxes, tables, callouts, connector
lines, tree nodes) goes through python-pptx's high-level API.

### Style discipline (enforced; audits run by default)

Mirrors `DECK_BUILD_SPEC.md` §3.1 / §4 rules:

- **Arial only** on every text run (`<a:latin typeface="Arial"/>`)
- **Black text only** — every `<a:rPr>` has color `000000`; hierarchy from
  weight/size, never color
- **Blue + gray fills/strokes only** — chart-series + callout-border palette
  in `style.py` (COLOR_BLUE_100..900, COLOR_GRAY_100..700)
- **Sharp 90° corners only** — every shape uses `MSO_SHAPE.RECTANGLE`
  (preset `rect`); no `roundRect`, `ellipse`, etc.
- **No shadows / glows / reflections** — `strip_all_shadows` post-process

Build-time audits (in `build.py` or one-off Python):
- font typeface != Arial → fail
- text-run srgbClr != 000000 → fail
- shape `prst` not in {rect, line, straightConnector1} → fail
- any `outerShdw`/`innerShdw`/`prstShdw`/`reflection`/`glow` element → fail

All audits pass on the current build.

### The 4-slide structure (locked)

| # | Title | Content |
|---|---|---|
| 1 | `Framing \| MECE decomposition of program $ from total down to addressable supplier opportunity` | 5-level MECE tree. Root: "FY Allocated SCN Program $". L1: Plans / GFE / Basic Construction (emphasized) / Other-CO. L2 (below BC): Yard self-perf / Outsourced layer. L3 (below Outsourced): FFATA-visible / Unseen layer. L4 (below Unseen): Purchased material / Lower-tier subs / FFATA non-compliance / HII teaming work. Each leaf annotated with data source. |
| 2 | `Data sources & scope \| Federal feeds for $, budget PDFs for structure, transcripts for direction` | 9-row source table (FPDS / USAspending / SAM FSRS / SAM Entity Mgmt / SCN books / EDGAR / public transcripts / GAO+CRS / NewsAPI) with columns: Source / What it gives us / Access pattern / Known gotcha. Right column: scope rules callout (in-scope, out-of-scope, MIB exclusions, window, parent-UEI rollup). |
| 3 | `Cleaning the data \| Most-recent vintage wins, parent UEIs are the right unit, HII gap needs triangulation` | 3 side-by-side callouts: SCN multi-vintage reconciliation / Parent-UEI rollup / HII visibility triangulation. |
| 4 | `What this method does NOT tell you \| Bounded answers, lagging data, no per-hull or per-component attribution` | 8 bulleted caveats with bold leads: make/buy band, FFATA lag, non-compliance, NAICS corporate-primary, geo = registered address, no per-hull/component attribution, pre-FY22 BC incomplete, ~30% vendors unenriched. |

### Style refinements during iteration

User feedback drove these tweaks (now baked into the primitives):
- **No bold on slide titles** — `add_title()` emits both topic and takeaway
  at regular weight. (Initially takeaway was bold.)
- **No blue rule line under titles** — removed the `add_line` call in `add_title`.
- **Middle vertical alignment in table cells** — `_style_cell` sets
  `cell.vertical_anchor = MSO_ANCHOR.MIDDLE`.
- **No vertical borders on tables, no fills, header bottom 1.5pt black, data
  row separators 1pt black, last row no border** — the borders are drawn as
  **explicit line shapes** (`add_line` after table creation, positioned at
  row boundaries) rather than as cell-level borders. Reason: cell-level
  border XML was not rendering reliably across LibreOffice/PowerPoint —
  empty `<a:lnX><a:noFill/></a:lnX>` worked in PowerPoint but vertical lines
  still appeared in LibreOffice. The explicit-line approach is bulletproof
  but requires uniform row heights (set via `header_row_h` / `data_row_h`
  kwargs on `add_table`).
- **Tightened shape heights** on slides 2/3 — reduced empty space inside
  the scope callout (h=3.05") and three cleaning callouts (h=3.15"). Sized
  to longest content; the SCN reconciliation callout has ~0.5" empty
  bottom because its content is shorter than the other two (acceptable for
  visual consistency).
- **Removed shadows globally via post-process** — `strip_all_shadows` walks
  every slide/layout/master/theme XML in the saved .pptx zip and empties
  every `<a:effectLst>` and `<a:effectStyleLst>` child.

### To rebuild

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work/deck_methodology
python3 build.py
open out/methodology_deck.pptx
```

### To preview without opening PowerPoint

```bash
soffice --headless --convert-to pdf --outdir out/preview out/methodology_deck.pptx
# or render a single slide as PNG:
pdftoppm -r 200 -f 2 -l 2 -png out/preview/methodology_deck.pdf /tmp/slide2
```

---

## 3. Full-history SAM pull — what we got

### Script

`scripts/pull_sam_subawards_fullhistory.py` — sibling of the existing
`pull_sam_subawards.py`. Same 17 PIIDs, same API behavior tricks
(lowercase `piid`, `pageSize=1000`, stop on empty page), but:
- `FROM_DATE = "2008-01-01"` (covers full FSRS history; FSRS started ~2010)
- `TO_DATE = today` (per howto: future dates 400)
- Separate output dir: `sam_subawards_fullhistory/`
- Resume-safe: if `<PIID>_subawards.json` already exists, skip it
- Per-PIID file written as each completes (partial run still useful)
- `_progress.json` updated after every PIID for quick status checks
- Timestamped per-line logging

### Run

Kicked off 2026-05-24 01:07:10 in background via:

```bash
nohup python3 scripts/pull_sam_subawards_fullhistory.py \
    > sam_subawards_fullhistory.log 2>&1 &
disown
```

Finished 2026-05-24 06:50:09. **Total elapsed: 5.72 hours. Zero errors.**

### Results — record count + dollar deltas vs FY20-FY26 pull

| PIID | label | FY20-26 recs | fullhist recs | Δ | FY20-26 $M | fullhist $M | Δ $M |
|---|---|---:|---:|---:|---:|---:|---:|
| N0002417C2100 | GDEB Va Block V/VI master | 4,389 | 5,681 | +1,292 | 2,426.2 | 4,175.8 | +1,749.6 |
| N0002417C2117 | GDEB Col Build I+II | 4,150 | 5,208 | +1,058 | 7,143.5 | 7,748.9 | +605.3 |
| N0002412C2115 | GDEB Va Block IV MYP | **0** | **1,622** | +1,622 | 0.0 | 233.7 | +233.7 |
| N0002424C2110 | GDEB Va Block VI LLTM | 367 | 367 | 0 | 417.4 | 417.4 | 0.0 |
| N0002409C2104 | GDEB Va Block II residual | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| N0002413C2128 | GDEB Col Design Drawings | 54 | 608 | +554 | 12.2 | 273.5 | +261.2 |
| N0002419C2125 | GDEB Va Tech Instructions / HPAD | 1,292 | 1,292 | 0 | 240.9 | 240.9 | 0.0 |
| N0002416C2111 | GDEB VPM Vent Valve | 218 | 773 | +555 | 128.6 | 285.3 | +156.8 |
| N0002410C2118 | GDEB VPM Tube Fab | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| N0002411C2109 | GDEB SSBN-R concept | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| N0002420C4312 | GDEB Hartford EOH | 430 | 430 | 0 | 116.4 | 116.4 | 0.0 |
| N0002419C2114 | BPMI Naval Reactor Components | 39 | 49 | +10 | 90.5 | 146.3 | +55.8 |
| N0002419C2115 | BPMI Col Class IBI | 44 | 67 | +23 | 166.2 | 528.0 | +361.8 |
| N0002424C2114 | BPMI S9G reactor | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| N0002410C6266 | LM Va Combat Systems | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| N0002421C4106 | BAE SSN 812 Forward Subassembly | 15 | 15 | 0 | 1.7 | 1.7 | 0.0 |
| N0002421C4111 | RR Va Class Rotor | 7 | 7 | 0 | 4.7 | 4.7 | 0.0 |
| **TOTAL** | | **11,005** | **16,119** | **+5,114** | **10,748.3** | **14,172.6** | **+3,424.3** |

### Headline interpretations

1. **USAspending 2,500-cap math empirically confirmed.** The biggest master
   (N0002417C2100) had 4,389 records in the FY20-FY26 window already — far
   above USA's 2,500 cap. Full-history brings it to 5,681. The ~3,500
   "long-tail" records noted in the 05-22 log are now fully captured.

2. **Virginia Block IV recovered.** N0002412C2115 (Va Block IV MYP) had
   **zero** records in the FY20-FY26 window, despite being a real
   submarine-construction contract with documented activity. Full history:
   1,622 records, $234M. This was the canonical example of the "pre-FY20
   black hole" flagged in the 05-22 caveats. Mostly FY13-FY19 activity.

3. **FY20-FY27 deck numbers do NOT move.** All +5,114 new records are
   pre-FY20 actions (action dates before 2019-10-01). The deck's headline
   `20.2% FY22-FY24` and the cost funnel remain valid as-is.

4. **Pre-FY22 BC gap is partially backfilled (numerator side only).** The
   numerator (visible subaward $ for the pre-FY22 era) now exists. The
   denominator (Basic Construction $ for FY20-FY21) still requires PB20
   and PB21 SCN books which are not on disk.

5. **Some PIIDs returned zero even at full history.**
   - N0002409C2104 (Va Block II residual): 0 records lifetime — likely
     too old / pre-FFATA-maturity era (Block II was FY08-FY13)
   - N0002410C2118 (VPM Tube Fab): 0 — prime never filed FFATA?
   - N0002411C2109 (SSBN-R concept): 0 — small concept work, may not have
     met FFATA threshold
   - N0002424C2114 (BPMI S9G reactor): 0 — recent contract (FY24); subs
     may not be fired yet
   - N0002410C6266 (LM Va Combat Systems): 0 — surprising; LM should have
     subs on a $-large combat-systems prime. Worth investigating (LM may
     report at parent level under a different vehicle).

### Files written this session

| File | Description |
|---|---|
| `scripts/pull_sam_subawards_fullhistory.py` | The pull script |
| `sam_subawards_fullhistory.log` | Full timestamped log of the 5.7-hour run |
| `sam_subawards_fullhistory/N0002*_subawards.json` | One per PIID (17 files), with `published` + `deleted` record arrays plus per-PIID metadata |
| `sam_subawards_fullhistory/_summary.json` | Per-PIID record count + $ totals |
| `sam_subawards_fullhistory/_progress.json` | Final state ("done", index 17/17) |

---

## 4. Open methodology questions / next steps

Picking up from session 1's list (still applies), this session's work adds:

1. **Aggregate the full-history SAM data by parent UEI** to see if any
   pre-FY20 vendors are missing from the current top-50 (which is based on
   FY20-FY26). Likely candidates: vendors that were heavy contributors
   in FY13-FY19 but exited the supplier base by FY20. Quick script
   (~30 min); modeled on `aggregate_sam_subawards.py`.

2. **Investigate why some PIIDs returned 0 records even at full history**:
   - N0002410C6266 (LM Va Combat Systems) is the most suspicious — LM
     should have a long supplier base on this. Could be a FFATA reporting
     issue at LM, or wrong PIID
   - Verify via FPDS that the PIIDs are real and have signed mods

3. **Re-run the aggregator with the wider data** — if we accept that
   pre-FY20 activity is now visible, we could:
   - Build a per-CY (calendar year) view going back to ~2012
   - Show vendor-base evolution all the way through (e.g., when did
     BlueForge first appear? Likely FY23 — which would be a clean
     before/after of the MIB transition)

4. **The deck does not currently reflect this pull.** The headline
   numbers don't change, but if the deck wants to show "we have ground-
   truth pre-FY20 data too," it would need a new appendix slide. Lower
   priority.

5. **BlueForge downstream pull** (alternative the user considered but
   didn't run). Still open. ~1-3 hours. Would close the $4.17B "where
   does it actually go" black box.

6. **Phase 4 (GFE-prime FPDS expansion)** still open from session 1 —
   LM combat sys / NG sonar / Raytheon / Boeing as primes. Becomes more
   urgent if the user wants to extend the funnel methodology to GFE-tier
   visibility, not just GDEB.

---

## 5. Caveats specific to this session

1. **Full-history SAM pull date interpretation.** `subAwardDate` is the
   action date of the subaward, not the prime's funding date or the
   reporting date. Pre-FY20 records may include actions on contracts that
   were originally awarded earlier or that have been re-novated.

2. **FFATA pre-FY15 data is sparse and inconsistent.** FFATA reporting
   maturity ramped through ~2012-2014. Very early records (2010-2012)
   often have placeholder text in descriptions and missing parent UEIs.
   Use with care if extending the analysis pre-FY15.

3. **The methodology deck does not enforce HII visibility.** Slide 1's
   MECE tree shows "HII teaming work" as an L4 sub-leaf of the Unseen
   layer, but the actual quantification of that gap is done via 10-K
   triangulation (Slide 3) — not via the FFATA pull. Don't confuse the
   structural representation with the quantified analysis.

4. **The methodology deck has no numbers by design.** Per user request,
   it documents the framework only. Future versions might add small
   inset numbers as captions if needed for a specific audience.

5. **`deck_methodology/` is NOT the main deliverable deck.** The main
   deck (per `DECK_BUILD_SPEC.md`) is still unbuilt. The methodology
   deck is a personal tool for the user. Both decks share `style.py`
   tokens but have different `slides/` directories and different
   `build.py` (the main deck does not exist yet).

---

## 6. Hand-off — if next agent wants to extend

### To rebuild the methodology deck

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work/deck_methodology
python3 build.py                                # outputs out/methodology_deck.pptx
soffice --headless --convert-to pdf --outdir out/preview out/methodology_deck.pptx
```

### To run a fresh full-history SAM pull

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work
# delete sam_subawards_fullhistory/ to force a re-pull,
# otherwise existing per-PIID JSON files are skipped
nohup python3 scripts/pull_sam_subawards_fullhistory.py \
    > sam_subawards_fullhistory.log 2>&1 &
disown
```

### To aggregate the full-history SAM data

No script yet — would be a sibling of `aggregate_sam_subawards.py`. Easiest
template:

```python
import json, os, glob
from collections import defaultdict

DIR = "sam_subawards_fullhistory"
files = glob.glob(f"{DIR}/N*_subawards.json")
by_parent = defaultdict(float)
by_cy = defaultdict(float)
for fp in files:
    with open(fp) as f:
        data = json.load(f)
    for r in data["published"]:
        amt = float(r.get("subAwardAmount") or 0)
        parent = (r.get("subEntityParentLegalBusinessName") or
                  r.get("subEntityLegalBusinessName") or "UNKNOWN").upper().strip()
        by_parent[parent] += amt
        action_date = (r.get("subAwardDate") or "")[:4]  # CY
        if action_date.isdigit():
            by_cy[action_date] += amt
# top-20 parents lifetime
for p, a in sorted(by_parent.items(), key=lambda kv: -kv[1])[:20]:
    print(f"${a/1e6:,.1f}M  {p}")
print()
for y in sorted(by_cy):
    print(f"CY{y}: ${by_cy[y]/1e6:,.1f}M")
```

### Things to NOT do

- **Don't re-run the SAM pull just to grab a few more PIIDs** — the script
  is resume-safe but the 5.7-hour runtime is real. Add to `SEED_PIIDS` list
  only, then re-run.
- **Don't modify `pull_sam_subawards.py`** to remove the date window — the
  FY20-FY26 windowed cache is what the deck uses; we don't want to
  accidentally re-aggregate against full-history data and have the deck
  numbers drift. The two scripts + two output dirs are intentionally
  separate.
- **Don't add features to the methodology deck without checking style
  audits afterward.** Easy to slip in a non-Arial font or a non-rect
  shape via python-pptx defaults.
- **Don't claim "the deck is updated" after running the full-history
  pull.** The deck does not consume `sam_subawards_fullhistory/` —
  it uses the windowed pull's outputs.

### Memories saved this session that affect future work

None saved (all session-specific findings are in this log).

---

## 7. Quick orientation for next agent

**If user asks "what's in the methodology deck":**
4 slides — Framing (MECE tree of program $), Data sources & scope (table
+ scope callout), Cleaning the data (3 callouts), What this method does
NOT tell you (8 bulleted caveats). No numbers. Same style discipline as
the main deck spec. File: `deck_methodology/out/methodology_deck.pptx`.

**If user asks about the methodology deck build pipeline:**
Mixed-mode — python-pptx for the high-level API, raw lxml OOXML for cell
borders + theme strip + shadow strip. Compared to the main deck spec
(pure raw OOXML), this is the pragmatic version. Style enforced via
post-build audits (font, color, geometry, no-shadows).

**If user asks "did the overnight pull work":**
Yes. 5.7 hours, 17/17 PIIDs, zero errors. +5,114 records (+46%), +$3.4B.
All new records pre-FY20. Headlines in `sam_subawards_fullhistory/_summary.json`.

**If user asks "do the deck numbers change":**
No. All new records are pre-FY20; the deck uses the FY20-FY26 windowed
data which is unchanged.

**If user asks "what's the biggest find from the overnight pull":**
Virginia Block IV (N0002412C2115) had ZERO records in the windowed pull
but 1,622 records lifetime ($234M). That's the pre-FY20 gap the 05-22
caveats explicitly flagged.

**If user asks "what should we do next":**
Either: (a) aggregate the full-history data by parent UEI to see if any
pre-FY20 vendors are missing from the current top-50; or (b) run the
BlueForge downstream pull that was the runner-up overnight option.
