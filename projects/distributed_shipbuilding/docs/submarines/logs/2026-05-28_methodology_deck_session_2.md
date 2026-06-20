# 2026-05-28 — Methodology side-deck session 2

## Scope

Continuation of the methodology deck buildout (`sub_pptx/`). Started
with 3 of 6 planned slides built (cover, cost funnel, methodology
pipelines) per the prior session log; ended with all 6 slides built,
several rounds of polish on the cost funnel and lens table, and a
structured decision on data-wiring scope (deferred — slides 4 and 5
only when it happens, not all six).

Final state: clean 6-slide deck building from `python build_deck.py`.
Cover · Framing · Scope and Definitions · Cost Funnel · Methodology
(Computation Pipelines) · Meaning and Limits. All XML parses; all
slides render in PowerPoint without obvious breakage.

---

## 1. Context loaded at session start

Reread:
- `sub_work/sub_pptx/` current state (build script, deck_submarines package,
  slide_topics.md, existing slide modules).
- `sub_work/METHODOLOGY.md` — the single-source-of-truth methodology
  doc with 10 guardrails, 4 denominator lenses, the cost-funnel spine,
  the MIB / BlueForge exclusion, and the [Planned] §11 addressability
  layer.
- `sub_work/project_description.txt` — one-line scope (sizing how much
  Va + Col new-construction value is performed outside the assembling
  shipyards).
- `sub_pptx/ooxml_cheat_sheet_pptx.md` (4100 lines) — the OOXML
  reference for raw PowerPoint XML patterns.
- The 2026-05-27 N81 head-to-head styling log for visual-vocabulary
  reference (italic chart titles, per-bar inline unit labels, GRAY_1
  gridlines, no row banding, boxed GRAY_1 caveat strip).

## 2. Design iteration before building

Started with a 5-item design proposal per slide; user came back with
a sharper version that I adopted in full. Key design moves the user's
version landed harder on:

- **Slide 2 framing — radial "same dollar, four lenses" visual**
  instead of my "hero question card + two-column why/output." The
  radial pattern makes the reader *feel* the denominator ambiguity
  instead of reading about it.
- **Slide 3 scope — IN/OUT in adjacent columns** with a shared "label"
  key column instead of separate IN and OUT panels. Keeps the "why
  this is excluded" sitting next to "what's in."
- **Slide 6 meaning — single hero range bar** as *the* anchor with
  triangulation demoted to a quiet evidence row, not three equal-
  weight rows.
- **Codified color role table** (BLUE_5 anchor / BLUE_4 focal /
  BLUE_3 headline / BLUE_2 secondary / BLUE_1 quiet card / GRAY_1
  excluded). Removes ad-hoc palette decisions per slide.
- **Locked title format** `"Topic  |  finding"` with double-space
  pipe separator. No em dashes, no slash separators in prose.
- **Helpers stay slide-local** — don't push to primitives.py.

## 3. OOXML conventions clarified before coding

Cheat-sheet re-read covered most of what was needed but left some gaps.
Asked an external LLM for the rest; folded the answers in as the
working conventions for new slides:

1. **Element order in `p:spTree`** — later children paint on top of
   earlier ones. For overlapping shapes with their own `a:ln` borders,
   shared edges can produce doubled-thickness seams under `algn="ctr"`
   if both sides own the border. Convention: for grids, give fills
   `<a:ln><a:noFill/></a:ln>` and draw separators *once* on top as
   thin filled rectangles or single line shapes.
2. **Vertical / horizontal hairlines** — use a thin filled `p:sp`
   rectangle (e.g., `cx=12700, cy=h`), not `p:cxnSp +
   straightConnector1`. Connector behavior has endpoint semantics and
   the visible width comes from `a:ln/@w` not from the bounding box.
   (Kept the existing `_h_rule` cxnSp pattern on cost_funnel since
   the user said don't retrofit; new slides use filled-rect rules.)
3. **Native `a:tbl` vs layered rectangles** — committed to native
   for any actual tabular data (slide 3 scope grid, slide 4 lens
   ledger after the rewrite). Native gives table semantics,
   accessibility, and table-style inheritance; the user explicitly
   said "we are definitely not going to use shapes to mimic a table."
4. **Circles** — `prstGeom prst="ellipse"` with equal cx and cy.
5. **Full-radius pills** — `prstGeom prst="roundRect"` with
   `<a:gd name="adj" fmla="val 50000"/>`. `adj` is unitless,
   range 0..50000; 50000 = half the shorter side = semicircular ends.
6. **Two stacked labels at one anchor** — two independent single-
   paragraph textboxes per pixel-precise generated chart labels (LLM
   convention). One-textbox-two-paragraphs is for human-editable
   labels.

## 4. GFE-prime list research (resolved a methodology disagreement)

User flagged a discrepancy between METHODOLOGY.md §2 prose
("BPMI, Lockheed Martin, BAE, Rolls-Royce") and a different earlier
spec text ("GDEB, HII, BPMI, LM, NG, and MIB"). Asked which list was
canonical.

Looked at `wiki_submarines/01-scope-and-funnel-framework.md` which
holds the authoritative 15-PIID table. Counted by prime:

| Prime | PIIDs | Count |
|---|---|---|
| GDEB | masters + LLTM + VPM, both Va and Col | **9** |
| BPMI | Naval reactor + Col IB Increase + S9G | **3** |
| Lockheed Martin | Combat systems | **1** |
| BAE | SSN 812 forward subassembly | **1** |
| Rolls-Royce | Va-class rotor | **1** |
| **Total** | | **15** |

Neither earlier list was exactly right:
- The §2 prose understates by omitting GDEB (the construction prime
  that owns 9 of the 15 PIIDs).
- The other version names HII (not a prime — team partner whose work
  flows through GDEB), NG (a GFE category for sonar/EW, not a prime
  on the 15 PIIDs), and MIB (a subaward layer routed through one
  BPMI PIID, not its own prime).

Adopted: **5 primes — GDEB, BPMI, Lockheed Martin, BAE, Rolls-Royce.**
HII and MIB surfaced as footnote annotations on the scope slide
(team-build flows through GDEB; MIB layer routed through BPMI
N0002419C2115).

## 5. Slides built this session

### Slide 2 — `framing.py`

Top BLUE_5 anchor band, central BLUE_4 "Same construction dollar"
tile orbited by four lens tiles (TL/BR BLUE_1 context, TR/BL BLUE_3
headline). Right side: three stacked numbered output cards (BLUE_5
ellipse badges via `prstGeom ellipse`). Bottom: BLUE_5 thin rule +
guardrail caption.

Later refinement (after the critique pass) tightened the orbit:
center-relative tile positions with a 260k EMU gap, plus a quiet
no-fill GRAY_4 `roundRect` (adj=9000) `OrbitFrame` behind the five
tiles so the composition reads as a deliberate diagram rather than
five free-floating shapes.

Sources line added at the end of the same critique pass — the body-
slide chrome rhythm wants one even on a slide that doesn't directly
visualize data.

### Slide 3 — `scope.py` (native `a:tbl`)

Top 3-chip scope strip (Programs BLUE_3 / Cost lines BLUE_1 /
Windows BLUE_1). Left main: native `a:tbl` 3 columns × 5 rows.
Header BLUE_3 white bold with 1.5pt black lnB; data rows white with
1pt black borders. The Contract-set row's IN cell carries a second
italic GRAY_4 paragraph annotating HII team-build and the MIB
routing — the two structural realities that don't fit in the
5-primes list. Right: quiet white decoder panel with 4 grouped
acronym sections (Budget and contract / Data systems / Flow
categories / Timing and procurement).

Sources line cites the SCN J-Books and FAR 52.204-10.

### Slide 6 — `meaning_limits.py`

Top range bar (BLUE_2 fill from 50% to 65%, BLUE_4 base segment
centered on 60%, both `a:ln noFill` per the single-ownership rule
for grids; tick marks and edges drawn once as separate thin filled
rects on top). Two-textbox tick labels (numeric above, category
below — pixel-precise generated-chart pattern). BLUE_5 "Band, not a
point" badge at top-left of the range panel.

Right: BLUE_1 callout with a BLUE_5 top strip "Excluded from
construction outsourcing" + three dollar lines (BlueForge $4.17B /
TMG $77M / IALR $1.5M) + italic note "Capacity grants, not
construction work."

Middle: three equal-width BLUE_1 evidence cards with a small FFFFCC
MODELED chip on the HII team-build card.

Bottom: white outer-bordered caveat ledger with four bold rows
separated by hairlines drawn once on top (single-ownership rule).

Sources line cites GAO/CRS supplier-base reports, GD (CIK 40533) and
HII (CIK 1501585) 10-K filings, SAM FSRS, and SCN J-Books.

### `lib.py` registry

`N_SLIDES_OUT = 6`, imports added for framing / scope / meaning_limits,
`slide_module_renders` reordered to `cover → framing → scope →
cost_funnel → methodology → meaning_limits`.

## 6. Cost funnel diagnostics + fixes

User asked me to look at cost_funnel for issues with a specific
focus on LHS/RHS symmetry. Findings:

| Element | Top y | Bottom y |
|---|---|---|
| LHS funnel (bands 0-3) | 1_375_296 | **4_365_296** |
| RHS lens ledger (original) | 1_375_296 | **5_195_296** |

RHS extended ~830k EMU below LHS — a visible imbalance with LHS
having ~1.2M EMU of dead space below band 3 before the footer.
Root cause: `_LEDGER_H` was hardcoded at 3_820_000; funnel was 4
bands × 620k + 3 gaps × 170k = 2_990_000. Nothing forced them to
match.

Also found:
- Change-orders chip overhang — third chip ended at x=7_143_079,
  main panel ended at 7_103_079. Off by 40k EMU.
- FFATA / Unseen abutting BLUE_5 boxes both with 1pt borders —
  doubled-stroke-seam risk per the LLM convention.
- Sources line cited only SCN J-Books but the slide draws on FPDS,
  FFATA, and DoD announcements too.

### Fixes applied (in order)

1. **LHS/RHS symmetry — first pass.** Tied `_LEDGER_H` to
   `4 * _BAND_H + 3 * _BAND_GAP = 2_990_000`. Row height dropped
   from 857_500 to 650_000; per-row text offsets retuned (50k /
   260k / 440k).
2. **Chip overhang.** Pulled `chip_x` 40k EMU left (offset from
   +220_000 to +180_000). Third chip now ends at exactly the
   main-panel right edge.
3. **Sources line completed.** Now lists all four data feeds:
   SCN J-Books, FPDS Atom, SAM FSRS, DoD daily announcements.
4. **Removed the bottom-row hairline** in the lens table on a
   later round so the ledger reads as open at the bottom.

## 7. Lens ledger conversion to native `a:tbl`

User proposed the ghost-column technique for replicating the
"BLUE_3 stripe + HEADLINE pill on headline rows" visual using a
native table:

> Add 2 new columns on the left. Make the middle one vertically
> merged, size 1 font, 0.00" padding — that becomes a ghost
> divider. The leftmost column is unmerged with 0.00" padding and
> size 1 font — fill that with the bg color on headline rows.

Adopted exactly. Final structure: 3 cols (stripe 91_440 EMU + gap
91_440 EMU vMerged across all 5 rows + content 3_852_962 EMU) × 5
rows (header + 4 data). All cells have `lnL/lnR/lnT/lnB` set to
`noFill`. Row separators and the HEADLINE pills paint on top as
layered overlays.

Iterated on the table's horizontal rules across several rounds of
user feedback:
- Round 1: heavy header rule skipped stripe col; Lens 3 / Lens 4
  hairline also skipped stripe col.
- Round 2 ("gap column is still showing some fill - all horizontal
  borders shown in it"): all rules made content-column-only;
  removed the Lens 2 / Lens 3 hairline from stripe col too. Gap
  column truly clean.
- Round 3 ("residual hairline between Lens 1 and Lens 2 in the
  leftmost column"): removed the last stripe-segment hairline.
  Stripe col now carries zero horizontal rules; BLUE_3 stripe is
  one continuous colored block from Lens 2 top to Lens 3 bottom.
- Final round: gap column also set to `fill=None` (truly transparent,
  not just white-filled).

Final state of horizontal rules in the lens table:

| Boundary | Stripe col | Gap col | Content col |
|---|---|---|---|
| Header → Lens 1 | — | — | 1.5pt heavy |
| Lens 1 → Lens 2 | — | — | hairline |
| Lens 2 → Lens 3 | — | — | hairline |
| Lens 3 → Lens 4 | — | — | hairline |
| Lens 4 → (open) | — | — | — |

## 8. Critique-driven cleanup pass

User shared a critique from another AI agent (with instruction to
disregard #1 because the critic had seen an older build state). Of
the remaining items:

- **Framing orbit tightened** (§5 above already covers the change).
- **Cost-funnel shared column-bottom geometry.** Replaced fixed
  `_BAND_H` / `_BAND_GAP` / `_LEDGER_H` with
  `_COLUMN_BOTTOM = _FOOTER_Y - 220_000`. Both `_BAND_H` (760k) and
  `_LEDGER_H` now derive from `_COLUMN_H`. Funnel and ledger both
  end at the same y (~5_355_000) with a deliberate 220k breathing
  gap before the footer. No more dead space.
- **`_funnel_band` text centering.** Label + detail block now
  centered vertically inside `cy` so the band's text stays aligned
  when band height changes.
- **Chip + Yard-self chip + L3 note centered formulas.** All three
  now use `(_BAND_H - element_h) // 2` rather than fixed offsets.
  `_CHIP_H = 245_000` constant added.
- **Final-split borders to 1.5pt.** Both FFATAFloorBg and
  UnseenLayerBg now use `border_w=19_050` to match the deck's
  focal-anchor convention.
- **Prose cleanup.** `"MIB / BlueForge"` → `"MIB and BlueForge"` in
  scope.py. Two em dashes in meaning_limits.py replaced with colons
  (range caption + caveat header). Sources line added to framing.py.

## 9. Data-wiring exploration (deferred decision)

User pointed me at `sub_workbook/`. Found a substantial pipeline I
hadn't known about:

- **`workbook_submarines/sheets/deckdata.py`** is a sheet explicitly designed
  as the deck-facing contract. 35 figure IDs (DD-S3-01 through
  DD-S6-09) mapped one-to-one to slides 3 through 6, with the
  `derived_cell()` API returning a specific `DeckData!D{row}`
  reference.
- Producer sheets feed DeckData: Inputs (editable assumptions),
  Funnel (per-class per-FY decomposition), Subaward_Annual (FFATA
  floor + per-PIID detail + lag-adjusted view), MIB_Excluded,
  DoD_POP, Top_Vendors, HII_TeamBuild, Prime_10K, LLTM_AP,
  References, Checks.
- Plus **46 CSVs in `extracted/`** — the raw data underneath all of
  the above.

Wire-up is *not* done — the deck slides have hardcoded text
everywhere DeckData expects numbers.

### Pulled the actual numbers per slide

The user then asked which numbers would land where if we wired it
up. Computed the actual values from `extracted/nc_scope_summary.json`
and `cost_funnel_per_class.csv`:

- **Slide 4 (Cost Funnel) FY27 Va+Col combined:**
  - Total Ship Cost: **$21.9B** (Va $11.4B + Col $10.5B)
  - Basic Construction: **$15.7B** (Va $8.9B 77.7% + Col $6.9B 65.4%)
  - Outsourced within BC at Mid 60%: **~$9.4B**
  - FFATA-visible floor cumulative FY16-FY26 MIB-excluded:
    **$6,139M** (note: cumulative, mismatched with FY27 annual
    figures above)
- **Slide 5 (Pipelines) lane outputs:**
  - Lane 1 BC baseline: **$15.7B** FY27
  - Lane 2 FFATA floor: **$6,139M** cumulative
  - Lane 3 modeled outsourced layer: **$7.9B / $9.4B / $10.2B** at
    50% / 60% / 65%
  - Lane 4 outside-EB share: **~70%** $-weighted across sub-relevant
    DoD-announcement work (estimate; exact aggregate would need
    computation from `dod_action_pop_by_worktype.csv`)
- **Slide 6 (Meaning) — values already on slide, would just wire to
  live cells:**
  - Band 50% / 60% / 65% — already matches Inputs IN-01/02/03
  - BlueForge $4,173M / TMG $77M / IALR $1.5M — matches
    DD-S6-04/05/06
  - HII +30% YoY, Navy 10% → 50% — matches DD-S6-07/08/09
- **Slide 3 (Scope) — current text already correct:**
  - 15 in-scope PIIDs (DD-S3-01)
  - 2 out-of-scope PIIDs (DD-S3-02; not currently surfaced on slide)
  - 3 MIB-excluded UEIs (DD-S3-03)
  - 759 unique parent UEIs in scope (not currently surfaced)

### Decision: numbers on slides 4 and 5 only, deferred for now

User pushed back on adding numbers everywhere: "i dont want them all
to have numbers. that is not very 'clean' and can be distracting i
think."

Worked through which slides actually benefit from numbers vs are
hurt by them:

| Slide | Verdict |
|---|---|
| 1 Cover | No numbers — obviously |
| 2 Framing | **Keep clean.** The entire argument is "the answer changes with the denominator." Putting a number here actively undermines the message — readers take whatever they see as "the number." |
| 3 Scope | **Keep current level.** Already has the right anchors (15 PIIDs, line items, FY windows). Adding the 759-vendor count or the $6.1B cumulative floor would muddle the slide's job (define what's IN, not what we found). |
| 4 Cost Funnel | **Add numbers.** This is where numbers earn their keep — the funnel mechanics become tangible. One headline number per band (0/1/2; band 3 stays text because of the annual-vs-cumulative mismatch). |
| 5 Methodology pipelines | **Add numbers.** Currently the four equation lanes are unpopulated. One number per lane output box turns them from "concept of how to compute" to "here's the actual computation." |
| 6 Meaning and Limits | **Same numbers as now.** Wiring would change them from hardcoded literals to live cell references but the rendered slide looks identical. |

Net effect: numbers concentrate on slides 4 and 5. Other slides
stay clean. Roughly 10-12 values to pull from DeckData (or directly
from extracted CSVs) when the wire-up happens, not all 35.

**User then chose to write this log instead of proceeding with the
wiring.** Wire-up is the obvious next step.

## 10. Open questions / things deferred

1. **DeckData wire-up for slides 4 and 5.** Decided what would land
   where (§9). Not built. Two specific labeling decisions need to
   resolve before publishing:
   - **Cumulative-vs-annual mismatch on band 3 of slide 4.** FFATA
     floor is cumulative FY16-FY26; everything else on the slide is
     FY27 annual. Either surface both views with clear labels, or
     pick one frame.
   - **Lens 3 (outside-the-yard) aggregate.** DoD POP data is
     per-action with multiple work types. The single % shown in
     Lane 4 would need to be computed by $-weighting
     `dod_action_pop_by_worktype.csv` across sub-relevant rows.
     Rough estimate is ~70% outside-EB-site, but the actual
     headline number should be confirmed before publishing.
2. **The addressability layer (§11 of METHODOLOGY.md) is still
   [Planned].** Not in scope for the methodology deck; lives in a
   separate deliverable.
3. **Build-pipeline integration with the workbook.** Currently the
   deck is a standalone build (`python build_deck.py` reads no
   external data). Wire-up would read either `extracted/*.csv,json`
   directly or open the rendered `sub.xlsx` via openpyxl. Simpler
   path is the CSVs.
4. **README at `sub_pptx/` root.** Doesn't exist. If anyone else
   picks up the deck they have `slide_topics.md` and the module
   docstrings but no top-level "how to build / extend / what each
   slide does."

## 11. Final state

```
sub_pptx/
├── build_deck.py
├── slide_topics.md
├── sub.pptx                    # built deck, 6 slides, all parse cleanly
├── ooxml_cheat_sheet_pptx.md
├── connector_ooxml.txt
├── schematic_ooxml.txt
├── _extracted/                 # source PPTX parts (chrome, layouts)
├── assets_deck/                # Saronic chrome assets
└── deck_submarines/
    ├── __init__.py
    ├── lib.py                  # N_SLIDES_OUT=6, full registry
    ├── primitives.py           # slide / page_number / cover_layout / divider
    ├── charts.py
    └── slides/
        ├── __init__.py
        ├── cover.py
        ├── framing.py          # NEW — slide 2
        ├── scope.py            # NEW — slide 3 (native a:tbl)
        ├── cost_funnel.py      # heavily revised; native a:tbl for lens ledger
        ├── methodology.py      # unchanged from prior session
        └── meaning_limits.py   # NEW — slide 6
```

Six slides:
1. Cover
2. Framing — "The answer changes with the denominator"
3. Scope and Definitions — "The analysis is narrow by design"
4. Cost Funnel — "Denominator choice determines the reported outsourcing band"
5. Methodology — "Four parallel computations, reported against different denominator lenses"
6. Meaning and Limits — "The result is a defensible band, not a point estimate"

All chrome (breadcrumb, title, Preliminary chip, sources line, page
number) consistent across body slides. Color palette applied per the
codified role table. No em dashes or slashes in rendered prose.

## 12. Conventions worth carrying forward

- **Color role table:** BLUE_5 anchor / BLUE_4 focal inside visual /
  BLUE_3 headline lens or primary chip / BLUE_2 secondary fill /
  BLUE_1 quiet card or panel / GRAY_1 excluded or non-focal / WHITE
  for ledgers / FFFFCC for Preliminary and MODELED chips only.
- **Title format:** `"Topic  |  finding"` (double-space pipe).
- **Prose rules:** no em dashes, no slash separators, no plus or
  arrow separators in prose. Body-slide chrome (breadcrumb / title /
  prelim / sources / page number) locked.
- **Helpers stay slide-local.** primitives.py exposes exactly 4
  public functions (slide / page_number / cover_layout /
  section_divider_layout). Body slides vendor their own
  `_bg_rect / _textbox / _rule / _pill / etc.` private helpers.
- **Grid borders:** for any layout where multiple shapes share an
  edge, set `a:ln noFill` on the underlying fills and draw
  separators once on top as thin filled rectangles.
- **Native `a:tbl` ghost-column pattern** for any "table with a
  colored stripe marker on certain rows": 3 columns (stripe + gap
  vMerged + content), all cells with `lnL/lnR/lnT/lnB noFill`,
  layered overlays on top.
- **Shared column-bottom geometry** for any slide with parallel
  columns of different content (slide 4 funnel + ledger): derive
  both columns' bottoms from one shared constant so they stay
  aligned through future tuning.
- **5 in-scope primes for the 15 PIIDs:** GDEB, BPMI, Lockheed
  Martin, BAE, Rolls-Royce. NOT HII (team partner, work flows
  through GDEB), NOT NG (GFE category for sonar/EW, not a prime),
  NOT MIB (a subaward layer routed through one BPMI PIID).

## References

- Prior session log: `logs/2026-05-28_methodology_deck_session.md`
  (covered cover + cost_funnel + methodology pipelines build).
- Methodology source of truth: `sub_work/METHODOLOGY.md`.
- Canonical 15-PIID table:
  `submarine_outsourced_work/wiki_submarines/01-scope-and-funnel-framework.md`.
- Workbook data layer: `sub_workbook/workbook_submarines/sheets/deckdata.py`
  and the 46 CSVs in `sub_workbook/extracted/`.
- OOXML reference: `sub_pptx/ooxml_cheat_sheet_pptx.md`.
