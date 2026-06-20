# Session Log — submarine_outsourced_work — 2026-05-24 (session 7)

**Handoff doc for the next AI agent.** Picks up from session 6 (read +
critique of a pipeline-improvements transcript, no code changes). Read
prior logs in order:

1. `logs/2026-05-22_session_log.md` (initial workbook + FPDS/USA/SAM pipelines)
2. `logs/2026-05-23_session_log.md` (new-construction refinement + HII context)
3. `logs/2026-05-24_session_log.md` (cost-funnel reframing + primary sources)
4. `logs/2026-05-24_session_log_2.md` (methodology side deck + full-history SAM)
5. `logs/2026-05-24_session_log_3.md` (DoD POP + GD 10-K + FPDS POP)
6. `logs/2026-05-24_session_log_4.md` (workbook build, 12 sheets)
7. `logs/2026-05-24_session_log_5.md` (deck batch 1: 7 slides built clean)
8. `logs/2026-05-24_session_log_6.md` (pipeline read + transcript critique)
9. This file

**This session was iterative slide-design refactoring.** Four body slides
were redesigned from "card stacks" into semi-dense infographics with a
shared visual grammar: panel + dark header, lightening internal cells,
number badges, and a thin bottom rule strip. No new data was pulled, no
new artifacts, no new memory entries. The work product is on disk in
`deck/slides/`.

---

## 1. What this session was about

User worked through `deck/` slide-by-slide and prescribed concrete
infographic redesigns for four content slides. For each slide, the
user supplied detailed direction (geometry, content, visual metaphor)
and example code. This agent's job was to apply the direction, build
the deck, run `layout_check`, render the slide to PNG, and verify
visually. After each render the user gave one round of refinement
notes; those were applied as targeted edits in the same session.

Four slides were refactored:

| Slide | Before | After |
|---|---|---|
| 9 — `government_budget_view.py` | Stacked exhibit cards + line-item chips + sub-note + callout | **Budget-book + downstream-visibility-stack** system diagram. Iterated three times (initial, then formula-fit, then z-order + number badges + lighter borders) |
| 6 — `new_construction_scope.py` | Two-column native table + 900k bottom band | **Asymmetric scope gate**: 62% in-scope card grid + 36% out-of-scope rail + thin reading-rule strip |
| 10 — `cost_funnel.py` | Vertical funnel stack + denominator table + sentence callout | **Two-panel system diagram**: cost-funnel panel (with BC as gate) + denominator-lens rail + visibility-rule strip. Refined once (geometry breathing room) |
| 4 — `current_and_future_classes.py` | Timeline of class slots + row-aligned callouts | **Mission-family matrix + new-construction focus stack** + class-filter strip |

---

## 2. Shared visual grammar that emerged

Each redesign reused the same handful of primitives. Treat this as the
project's working design system — when other deck slides get the same
infographic treatment, reach for these patterns first.

### Panel + overlaid header

```
┌──────────────────── DARK HEADER (BLUE_5 or GRAY_5) ─────────────────────┐
│ TITLE CAPS                                                              │
│ Sentence-case subtitle                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  GRAY_1 panel interior with content overlaid                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

Implementation:

- `_panel(sp_id, name, x, y, w, h, title, subtitle, fill)` returns
  `backplate + header` as a single XML blob.
- Backplate fill is **always** `GRAY_1` with 0.75pt black border.
- Header fill is `BLUE_5` (primary panel) or `GRAY_5` (secondary panel).
- Header height of `380_000` EMU gives clean room for 12pt title +
  8.5pt subtitle without feeling squeezed. The earlier `330_000` was
  tight.

Lives in: every refactored slide; copy verbatim when adding more.

### 3-tier border weight

Established in `government_budget_view.py`:

```python
LINE_MICRO = 3_175     # 0.25pt — mini-visual segment dividers
LINE_THIN = 4_762      # 0.375pt — internal card borders
LINE_STD = 9_525       # 0.75pt — outer panels and bottom rule strips
LINE_HEAVY = 19_050    # 1.5pt — "gate" emphasis (Basic Construction, Deck Focus)
```

`LINE_MICRO` only goes on mini-visual segment dividers (P-5c bar
segments, P-10 pills). `LINE_THIN` is the default for cards, badges,
and answer chips. `LINE_STD` is for panel outers, headers, and the
bottom rule strip. `LINE_HEAVY` is reserved for the slide's primary
visual gate (e.g., BC in cost_funnel, deck-focus cards in
current_and_future_classes).

Earlier slides used `LINE_THIN = 6_350` (0.5pt) which read as
grid-heavy when many shapes were nested. The new lighter weights make
the same density feel more designed.

### Connector z-order

Flow connectors **must render before foreground cards**, immediately
after the backplates. Otherwise arrowheads can sit on top of card
borders.

```python
body += _doc_page_bg()
body += _right_panel_bg()

# Connectors next — behind everything else.
for i in range(len(EXHIBITS)):
    body += _flow_connector(400 + i, i)

# Then foreground content.
body += _doc_header()
# ...
```

Also: inset connector endpoints from the panel edges so arrowheads
don't land on borders.

```python
FLOW_INSET = 35_000

def _flow_connector(sp_id, idx):
    y = _row_y(idx) + ROW_H // 2
    x_start = DOC_X + DOC_W + FLOW_INSET
    width = GAP - 2 * FLOW_INSET
    return connector(sp_id, ..., x_start, y, width, 0,
                     color=C_DK1, width=LINE_THIN, arrow=True)
```

### Number badges for ordered stacks

When stacking a small ordered set (visibility layers, focus cards),
use a small dark left badge with white number text **overlaid** on the
card. The card itself has lighter fill.

Two implementations in this session:

- `government_budget_view.py` — layer cards with `LAYER_BADGE_W = 280_000`
  square overlay; body text is indented via `l_ins` to clear the badge.
- `current_and_future_classes.py` — focus cards use a **separate full-height
  left number cell** + body cell. Two-shape composition rather than
  overlay. Slightly different visual ("vertical rail" vs "corner
  badge").

Both are valid. The overlay approach (g.b.v.) is more compact; the
side-by-side approach (c.f.c.) makes the number a structural column.

### Bottom rule strip

Every refactored slide ends with a thin label + explanation strip at
the very bottom:

```text
┌─ DARK LABEL ─┬───── light explanation ──────────────────────────────────┐
│              │                                                          │
└──────────────┴──────────────────────────────────────────────────────────┘
```

- Strip height 340–420k EMU
- Dark BLUE_5 label cell (~1.5–1.85 inches) with all-caps name
- GRAY_1 body cell with sentence explanation
- 80k EMU minimum gap to the sources footer line — codified via
  `MIN_GAP_BAND_TO_SOURCES = 80_000` in `cost_funnel.py`

Pattern is identical in all four slides; copy verbatim.

### Asymmetric two-panel splits

Three of the four slides use ~60/40 or ~66/33 splits:

| Slide | Left % | Right % | What's on each side |
|---|---|---|---|
| g.b.v. | 70 / 30 | | Budget book + downstream visibility stack |
| cost_funnel | 60 / 38 | | Cost funnel + denominator lens rail |
| n.c.s. | 62 / 36 | | In-scope card grid + out-of-scope rail |
| c.f.c. | 66 / 33 | | Mission matrix + focus stack |

The deliberate asymmetry expresses **the analytical thesis**: left is
the analytical object, right is the supporting context. Avoid 50/50
splits — they imply both panels are equally important.

### Mini visuals over prose

When a card describes a structured idea, use a tiny shape diagram, not
a text sentence. In `government_budget_view.py`:

- **P-40 row**: formula strip with mathematical operators
- **P-5c row**: 4-segment horizontal bar (Plans | Basic Construction | GFE | Other)
- **P-10 row**: 4 small bucket pills

Each mini visual fits in a ~3-inch zone and reads instantly. They turn
the slide from "exhibit cards" into "exhibit data."

---

## 3. Iteration pattern

Each slide went through 1–3 rounds:

1. Apply user direction verbatim → build → render
2. User reviews PNG, gives 1–6 specific tweaks
3. Apply tweaks → build → render

Tweaks across the session converged on the same handful of moves:

- Make panel headers slightly taller (330k → 380k)
- Use thinner internal borders (0.5pt → 0.375pt; with 0.25pt for
  mini-visual dividers)
- Move connectors behind foreground (z-order fix)
- Replace dark-on-dark stacks with light cards + small dark badges
- Use cleaner labels ("ANSWERS" → "USE FOR"; "The same word answers
  different questions" → "Outsourcing changes meaning by denominator")
- Add explicit `MIN_GAP_*` constants to validate footer clearance
- Allow more vertical room in the lower panel by lengthening lane
  cards instead of leaving whitespace

---

## 4. Layout_check false positives that recur

Documented in earlier logs but worth restating since they're hit on
every redesigned slide:

| Flag | Cause | Action |
|---|---|---|
| `Breadcrumb` overlaps `prelim.main` | z-order intentional; chip's fill covers breadcrumb | Ignore |
| `Breadcrumb` overfill | placeholder uses `spAutoFit`; static estimator can't see it | Ignore |
| `RowLabel` / `FocusCode` underfill (~15–17% filled) | Vertically-centered short text in tall anchor box | Ignore OR shrink the box height below the 1.0" `--min-box-height-in` threshold (used in `government_budget_view.py`'s `_row_label`) |

Whenever a redesigned slide adds a new vertically-centered-short-text
pattern, expect a new underfill flag. Either shrink the box (cleaner)
or document the false positive (acceptable).

---

## 5. Per-slide notes

### Slide 9 — `government_budget_view.py`

**Final state:** SCN Justification Book document on the left (70%),
downstream visibility stack on the right (30%), bottom analytical-rule
takeaway.

Three iterations:

1. **Initial refactor** — Document panel with 3 exhibit rows (code
   badge + label + mini visual + answer chip), LI tabs overlaid on
   header, right stack of 4 visibility layers (BLUE_5/3/1/GRAY_2),
   subtle 0.5pt connectors.
2. **First tweak** — P-40 formula was wrapping mid-line; shrunk to
   8.5pt. Suppressed RowLabel underfill by shrinking row-label boxes
   to text height (350k EMU) centered in the row.
3. **Second tweak** — Reordered render() to put connectors behind
   foreground; switched to 3-tier border weights (LINE_MICRO/THIN/STD);
   replaced dark layer-card colors with lightening BLUE_2/BLUE_1/GRAY_2
   plus small dark number badges; widened answer chip; "ANSWERS" →
   "USE FOR"; takeaway band 350k → 420k tall.

**Key constants:**

```python
LINE_MICRO = 3_175       # mini-visual dividers
LINE_THIN = 4_762        # internal cards
LINE_STD = 9_525         # outer panels and takeaway
FLOW_INSET = 35_000      # connector endpoint inset
LAYER_BADGE_W = 280_000  # left badge on visibility layers
LAYER_BADGE_INSET = 50_000
LAYER_BODY_GAP = 50_000  # space between badge and body in layer card
```

### Slide 6 — `new_construction_scope.py`

**Final state:** Asymmetric scope gate. Two backplated panels side by
side (62% in-scope grid + 36% out-of-scope rail) plus a thin
reading-rule strip.

In-scope panel: BLUE_1 backplate, BLUE_5 header, 2×4 grid of cards
with KICKER / Bold core item / explanatory line. White card
interiors, thin borders.

Out-of-scope panel: GRAY_1 backplate, GRAY_5 header, 8 stacked chips
in alternating GRAY_1/GRAY_2 — visually quieter than the in-scope
cards.

Reading-rule strip: BLUE_5 "READING RULE" label + GRAY_1 explanation.

**Topic-label fix:** previous module had `topic_label="New-Construction
Scope"` (duplicating the title topic, against the style rule).
Updated to `"Scope Boundary"`.

**Section capitalization:** previous module used "What the Navy is
Building" (lowercase "is"). Aligned to "What the Navy Is Building"
(capital "Is") matching the rest of Section 1 and Title-Case rule.

### Slide 10 — `cost_funnel.py`

**Final state:** Two-panel system diagram with cost funnel left
(60%), denominator-lens rail right (38%), bottom visibility-rule
strip.

Cost-funnel panel: Total Ship Cost at top (GRAY_2 neutral), three
light-blue cost chips (Plans / GFE / Change Orders), **Basic
Construction gate** (BLUE_5 dark with LINE_HEAVY border — the visual
anchor), "INSIDE BASIC CONSTRUCTION" label, 3-over-2 lane grid.

Denominator-lens rail: 4 numbered cards (01 GDEB, 02 SCN, 03 PoP, 04
Private-yard). Cards 02 and 03 get BLUE_5 number cells (the
"Headline" denominators); cards 01 and 04 get GRAY_5 (Reported and
Context).

Visibility-rule strip: BLUE_5 label + 3 alternating GRAY_1/GRAY_2
tiles for Budget books / DoD announcements / FFATA.

Two iterations:

1. **Initial refactor** — Full structure built; passes layout_check.
2. **Geometry refinement** — Panel headers 330k → 380k; band moved up
   slightly to give 80k clearance to sources footer; lane cards
   lengthened to absorb the lower-panel whitespace; subtitle for
   right rail tightened to "Outsourcing changes meaning by
   denominator".

**Codified clearance constants:**

```python
MIN_GAP_MAIN_TO_BAND = 80_000
MIN_GAP_BAND_TO_SOURCES = 80_000
```

Validate uses these — future geometry edits can't accidentally crowd
the footer.

### Slide 4 — `current_and_future_classes.py`

**Final state:** Mission-family matrix + new-construction focus
stack + class-filter strip.

Matrix panel (66%): BLUE_5 header, 3-column grid (LEGACY FLEET / NEW
CONSTRUCTION / CONTEXT), 3 family rows (SSN / SSBN / SSGN). Each
family gets a dark GRAY_5 left label cell. **Virginia-class SSN and
Columbia-class SSBN are the only BLUE_5 cards** with the "DECK
FOCUS" caption and a LINE_HEAVY border. All other cells are BLUE_1
legacy or GRAY_2 context. SSN has 2 stacked mini-cards in legacy;
SSBN and SSGN have single full-height legacy cards.

Focus stack (33%): 3 cards numbered 01 Virginia, 02 Columbia, CTX.
Headline cards have BLUE_5 number cells + white body; CTX card has
GRAY_5 number cell + GRAY_1 body. Visual hierarchy reinforces "two
carry forward, one is context".

Class-filter strip: BLUE_5 "CLASS FILTER" label + GRAY_1 explanation.

**Why this beat the prior timeline layout:** SSBN has only 1 legacy
class (Ohio); SSGN has no like-for-like new-construction program. A
matrix can show those differences without forcing empty timeline
slots. The 3-column structure is more honest about what each family
actually has.

---

## 6. Files created or modified this session

| File | Change |
|---|---|
| `deck/slides/government_budget_view.py` | Full rewrite (3 iterations) |
| `deck/slides/new_construction_scope.py` | Full rewrite |
| `deck/slides/cost_funnel.py` | Full rewrite + 1 refinement pass |
| `deck/slides/current_and_future_classes.py` | Full rewrite |
| `logs/2026-05-24_session_log_7.md` | This file |

No changes to:

- `deck/build.py`
- `deck/style.py`
- `deck/primitives.py`
- `deck/layout_check.py`
- `deck/HANDOFF.md`
- `deck/README.md`
- Any other slide module
- Any data, workbook, or research artifact

---

## 7. Open items / next steps

### High-leverage next moves

1. **Apply the same redesign treatment to the rest of Section 2 and
   Sections 3–4.** `basic_construction.py`, `advance_procurement.py`,
   `prime_and_team_build.py`, `gfe_pipe.py`,
   `industrial_base_layer.py`, `public_data_lenses.py`,
   `award_evidence.py`, `subcontractor_award_map.py` are still in the
   pre-redesign style. The four refactored slides establish the
   visual grammar; applying it consistently across the deck is the
   natural next session.

2. **Section 1 slides not yet redesigned:** `mission_families.py`,
   `historical_reset.py`, `ecosystem_map.py`. Lower priority — they
   already look polished from session 5, but consistency might want
   them aligned to the new grammar.

3. **Encode the visual grammar as shared helpers in
   `deck/primitives.py`.** The `_panel`, `_p`, and bottom-strip
   patterns are repeated in all four refactored modules. Promoting
   them to primitives would (a) shrink each slide module by ~20–30%
   and (b) ensure future slides match the grammar by default. Risk:
   over-abstraction; the user's instinct (see log 6) was that
   primitives should be creative starters, not full templates.
   Suggest a thin shared module like `deck/components.py` that
   slide modules can opt into.

4. **Render PNG previews as part of `build.py`.** Recommendation
   carried over from log 6 (section 3). Still not implemented.
   `soffice --headless --convert-to pdf` is the route used manually
   this session.

### Low-leverage cleanup

- Suppress recurring `RowLabel` / `FocusCode` underfill false
  positives more systematically — either by shrinking the boxes
  below the 1.0" `--min-box-height-in` threshold or by documenting
  exemptions in `layout_check.py`.
- Standardize sp_id allocation across the deck. Each module picks
  its own scheme; some collisions are possible if modules are merged
  or refactored.

### Things to NOT do

- **Don't redesign the four slides further this session-thread.** They
  are at the user-approved state. If a tweak comes up, treat it as a
  micro-edit, not a redesign.
- **Don't change the global `LINE_*` constants in
  `deck/style.py`.** The 3-tier border weights are local to the
  refactored slide modules; pushing them to `style.py` would force
  all unrefactored slides to use them too, which is a separate
  decision.
- **Don't introduce a `<p:grpSp>` group primitive yet.** Log 6
  considered it for diagrammatic slides; we shipped this session
  without it. The Python-side helper-function organization (per-row
  / per-card functions) gives equivalent benefits.
- **Don't reorder the `SLIDES = [...]` list in `build.py`.** Other
  modules may hardcode `_row_y(idx)` constants that assume the
  current order.

---

## 8. Hand-off — re-run and validation

To rebuild and verify all four refactored slides:

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work/deck

python3 build.py
python3 layout_check.py out/submarine_deck.pptx --slide 4
python3 layout_check.py out/submarine_deck.pptx --slide 6
python3 layout_check.py out/submarine_deck.pptx --slide 9
python3 layout_check.py out/submarine_deck.pptx --slide 10
```

Expected output per refactored slide: only the two documented
breadcrumb false positives. Slide 4 also has three `FocusCode`
underfills (documented above).

To preview as PNGs:

```bash
soffice --headless --convert-to pdf --outdir out/preview out/submarine_deck.pptx
pdftoppm -r 180 -f 4 -l 4 -png out/preview/submarine_deck.pdf /tmp/slide4
pdftoppm -r 180 -f 6 -l 6 -png out/preview/submarine_deck.pdf /tmp/slide6
pdftoppm -r 180 -f 9 -l 9 -png out/preview/submarine_deck.pdf /tmp/slide9
pdftoppm -r 180 -f 10 -l 10 -png out/preview/submarine_deck.pdf /tmp/slide10
```

---

## 9. Memory items saved this session

None. All design conventions are codified in the slide modules
themselves and in this log. Future sessions reading from MEMORY.md +
this log will have the full pattern library available.

---

## 10. Quick orientation for next agent

**If user asks "which slides look like the new style":** slides 4
(current_and_future_classes), 6 (new_construction_scope), 9
(government_budget_view), 10 (cost_funnel). All other body slides
are still in the pre-redesign style.

**If user asks for "the same treatment" on another slide:** read
this log §2 (visual grammar) and pick the closest template:

- Document with data rows → `government_budget_view.py`
- Asymmetric scope gate (in / out) → `new_construction_scope.py`
- Vertical funnel + side rail → `cost_funnel.py`
- Multi-dimensional matrix → `current_and_future_classes.py`

**If user asks "what's the design system":** there isn't a formal one;
the patterns in this session's four slides are the working
convention. Border weights, panel structure, badge usage, and the
bottom rule strip are listed in §2.

**If user asks "are the layout_check failures real":** check §4 of
this log first. Three patterns are documented false positives.
Anything else needs investigation.

**If user asks to render the deck:** the `soffice` + `pdftoppm`
sequence in §8 is the manual flow. Adding a `--preview` flag to
`build.py` is still an open item.

**If user asks about pre-redesign body slides:** sessions 5 and 6
built them. They still work — they're just stylistically less dense
than the refactored four. Apply the §2 grammar to bring them in
line when needed.
