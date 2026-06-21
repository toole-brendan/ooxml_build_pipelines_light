# Session Log — submarine_outsourced_work — 2026-05-24 (session 6)

**Handoff doc for the next AI agent.** Picks up from session 5 (first
batch of main deck — cover + Section 1 divider + 5 body slides + ecosystem
map). Read prior logs in order:

1. `logs/2026-05-22_session_log.md` (initial workbook + FPDS/USA/SAM pipelines)
2. `logs/2026-05-23_session_log.md` (new-construction refinement + HII context)
3. `logs/2026-05-24_session_log.md` (cost-funnel reframing + primary sources)
4. `logs/2026-05-24_session_log_2.md` (methodology side deck + full-history SAM)
5. `logs/2026-05-24_session_log_3.md` (DoD POP + GD 10-K + FPDS POP)
6. `logs/2026-05-24_session_log_4.md` (workbook build, 12 sheets)
7. `logs/2026-05-24_session_log_5.md` (deck batch 1: 7 slides built clean)
8. This file

**This session was research / discussion, not code.** No files in
`deck/`, `workbook/`, or anywhere else were created or modified. The
session produced (a) a fresh full-pipeline orientation, and (b) a
written critique of an external AI-agent transcript proposing pipeline
improvements. No build was run; the deck on disk is unchanged from end
of session 5.

The value of this log: distill the critique so the next agent can act
on it (or push back further) without re-reading the transcript.

---

## 1. What this session was about

Two threads, in sequence:

**A. Full read of `deck/`.** User asked me to read everything in the
`deck/` directory and focus on understanding the build pipeline. I read:

- `deck/README.md`
- `deck/HANDOFF.md` (refactor notes from python-pptx → raw OOXML)
- `deck/build.py` (~480 lines: packager)
- `deck/style.py` (~290 lines: design tokens)
- `deck/primitives.py` (~975 lines: OOXML emitters + chrome composition)
- `deck/layout_check.py` (~320 lines: static layout validator)
- `deck/slides/__init__.py`
- `deck/slides/cover.py`
- `deck/slides/divider_what_navy_is_building.py`
- `deck/slides/mission_families.py`
- `deck/slides/current_and_future_classes.py`

Did NOT read every slide module — the goal was pipeline understanding,
not slide-by-slide audit. Summary I gave the user is reproduced in
Section 2 below for next agent's orientation.

**B. Reviewed a transcript of the user's chat with a different AI
agent** about how to improve the pipeline. User's stated symptoms:
agent-generated slides look wonky — shapes massively underfilled,
text-box spacing non-existent, page not fleshed out. User's instinct:
the primitives are meant to be **starters** the agent can creatively
combine. Concern: would the other agent's proposed compositions /
templates cause AI agents to overfit?

The other agent gave two rounds. Round 1 leaned heavily on full-slide
compositions (`evidence_cards`, `comparison_columns`, `kpi_row`, etc.).
Round 2 walked it back to **smart components + layout grammar + polish
check + auto-nudge**, after the user pushed back on the overfitting
risk.

My critique (Section 3 below) accepts most of round 2 but reorders
priorities and adds one critical missing recommendation: a
**render-to-PNG screenshot loop** so agents can visually inspect their
own output.

---

## 2. Pipeline orientation (compressed)

For the next agent who hasn't read `deck/` end-to-end. (Full detail
lives in `deck/README.md` and `deck/HANDOFF.md`; read both.)

**Architecture.** Raw OOXML emission, not python-pptx. Slide modules
return XML strings; `build.py` zips them into a `.pptx` alongside
Saronic chrome (slide master, layouts 1–6, theme, logo, embeddings)
staged at `/Users/brendantoole/projects2/_extracted/` and
`/Users/brendantoole/projects2/assets_deck/`. Chrome lives outside the
deck dir so multiple decks can share it. `build.py` fails fast if
either dir is missing.

**Build flow** (`build.py:build`):
1. Pre-flight checks (chrome + assets present).
2. Render each module in `SLIDES = [...]` → XML string via
   `module.render(*, page_num, total_pages)`.
3. Assemble parts dict: `[Content_Types].xml`, root `.rels`, docProps,
   presentation + rels, presProps/viewProps/tableStyles/theme/master/
   handoutMaster/tags read verbatim from `_extracted/`, slide layouts
   1–6 + rels verbatim, per-slide rels, media + embeddings copied from
   `assets_deck/`.
4. Zip deterministically (`[Content_Types].xml` first, then sorted).
5. Post-process `strip_all_shadows()` re-opens the zip and empties
   every `effectLst` / `effectStyleLst` so it renders flat across
   PowerPoint, Keynote, LibreOffice.

**Slide-module contract.**
```python
LAYOUT = "slideLayout1"   # cover/divider only; content omits → default slideLayout4

def render(*, page_num, total_pages):
    return slide(<chrome XML> + <body XML>)
```
`slide_rels_xml(n)` picks the layout in this priority:
`SLIDE_RELS_OVERRIDES[n]` → `SLIDES[n-1].LAYOUT` → `slideLayout4`.
**#1 gotcha** (per `HANDOFF.md`): forget `LAYOUT` on cover/divider and
the Saronic branded design vanishes — you get a white "Light Blank"
slide.

**Three slide types.**

| Helper | Layout | Binds to |
|---|---|---|
| `cover_layout(title, subtitle, footer=)` | slideLayout1 | body idx=12 (28pt bold title + 20pt italic subtitle stacked); title placeholder = small footer ("May 2026") |
| `section_divider_layout(section, subtitle)` | slideLayout2 | body idx=11 (28pt bold), idx=12 (20pt italic) |
| `base_chrome(section, topic_label, title_topic, title_takeaway, sources=, prelim=)` | slideLayout4 | idx=10 breadcrumb + title placeholder + optional sources line + optional pale-yellow Preliminary chip; page # auto from master's slidenum |

**Text-style rules** (from `style.py` top docstring + `HANDOFF.md`):
- Title format: `Topic | Finding` (Title-Case topic, sentence-case finding).
- Breadcrumb: bold `{Section}` + ` / ` + non-bold `{Topic Label}`.
- NO em dashes (—). NO `×`, `+`, `→`, `/` as separators. Spell out
  ("and" not "+", "money" not "$", "descending" not "desc").
- En dashes (–) OK only for number ranges. Standard prose `$XXM`,
  `$XXB`, `~`, `%` are fine.

**Hard style rules** (binding, enforced by convention not code):
- Arial, black text default (`C_DK1`), sharp corners (`prst="rect"`).
- Blue/gray fills MUST come from `BLUE_1..5` / `GRAY_1..5` — no ad-hoc
  hex. Use `blue_pair(i)` / `gray_pair(i)` to get matched (fill, text).
- Filled shapes need explicit border: `line_color="000000"`,
  `line_width=12700` (1pt). Borderless: `line_color=None`.
- Every chart needs interpretive text commentary.
- Charts are externally authored — drop `chart_placeholder()` dashed
  rectangles; grep `CHART PLACEHOLDER` to audit. Same for
  `image_placeholder()` / `IMAGE PLACEHOLDER`.

**Units.** EMU (914,400/in), 1/100 pt for font sizes, 1/1000 for line
spacing, hex strings for colors. Canvas 12,192,000 × 6,858,000 EMU
(13.33" × 7.5"). `LEFT_MARGIN=453_079`, `CONTENT_W=11_282_362`.

**Verify.** `python3 layout_check.py out/submarine_deck.pptx` — uses
python-pptx read-only. Flags overlaps + over/underfilled text boxes
using `char_count × font_size × 0.5` heuristic. Known false positives:
breadcrumb overlaps Prelim chip (z-order intentional); breadcrumb
overfill (`spAutoFit` invisible to static estimator).

**Current deck (20 slides registered in `build.py`):**
cover → 4 sections each opened by a divider:
- **What the Navy Is Building**: mission_families,
  current_and_future_classes, historical_reset, new_construction_scope,
  ecosystem_map
- **How Funded**: government_budget_view, cost_funnel, basic_construction,
  advance_procurement
- **Who Controls**: prime_and_team_build, gfe_pipe, industrial_base_layer
- **Award Visibility**: public_data_lenses, award_evidence,
  subcontractor_award_map

Note: session 5 log said 7 slides built; the current `build.py` SLIDES
list has 20. Either sessions in between built the rest, or the
in-between work happened outside the session-log thread. Slides on
disk reflect the 20-slide list.

---

## 3. Transcript critique (my distilled version)

The other agent diagnosed the pipeline as "good style atoms, missing
composition molecules." Round 1 proposed mandatory full-slide templates
(`evidence_cards_slide`, `chart_with_commentary_slide`, etc.). Round 2
walked it back to: layout regions + smart components + density modes +
polish checker + auto-nudge transforms + SlideBrief planning step +
optional recipes.

### Where the other agent is right

**Region / grid helpers.** Strongly agree. Look at
`current_and_future_classes.py:91-117`: it manually derives `ROW_Y0,
ROW_H, ROW_GAP, BODY_BOTTOM_Y, CALLOUT_X, CALLOUT_W` from scratch,
then guards them with `_validate_layout()`. Sophisticated, but it's a
lot of arithmetic for an agent to do correctly every time. A small
`Region` API (`body.split_cols([0.7, 0.3]).split_rows(3)`) would
remove an error class without restricting layout invention.

**Polish checker is the single highest-leverage code change.** The
user's three named symptoms — underfilled shapes, missing padding,
unfleshed pages — are all measurable. `layout_check.py:194` already
flags underfill but at a 30% threshold and only for boxes >1" tall —
too lenient. Tighten thresholds, add inset checks ("filled shape with
`l_ins < 91_440` is probably wrong"), add body-occupancy check ("less
than 50% of BODY region covered"), wire into `build.py` so it can't be
skipped.

**Smart component wrappers** (`card`, `callout_band`, etc.) — agree if
kept minimal. `text_box()` defaults to `l_ins=91440, t_ins=45720` —
fine for inline labels, terrible for a card. Either change defaults
(risky — breaks existing slides) or add 4–5 thin wrappers that
pre-set `INSETS_CARD` and require minimum content. Position as "the
easy path," not as templates.

### Where I'd push back

**SlideBrief / planning ceremony — drop.** Existing slides already
encode intent in a module docstring (see `mission_families.py:1-14`).
A formal `SlideBrief` dataclass adds typing overhead without changing
behavior unless something validates against it — and the user's
agents probably won't fill it in deeply anyway.

**Density modes (`executive`/`analytical`/`appendix`) — skip.** AI
agents will set this somewhat randomly, and the polish checker can
directly measure occupancy without needing the agent to declare
intent. One more parameter that fakes structure.

**Auto-nudge transforms — be careful.** Silent post-render edits
("snap near-aligned edges", "equalize card heights") will mask bugs
and produce surprising diffs. Better: checker says "these three top
edges are within 80k EMU but not aligned — pick one" and the agent
fixes it. Auto-snapping breaks the agent's mental model of what XML
it emitted.

**Mandatory full-slide compositions — agree with user, drop.** User's
overfitting concern is real. Don't even ship `recipes.py` initially.

### What BOTH transcript agents missed

**1. Render-to-PNG feedback loop is the biggest unlock for AI
agents.** First round mentioned it briefly ("export each slide to PNG
and run a vision-based review"), then both rounds dropped it. Humans
iterate by *looking at* slides; agents can't unless we render. If
`build.py --preview` rendered each slide to PNG (via LibreOffice
headless: `soffice --headless --convert-to png deck.pptx`), the agent
could view its own output and self-correct. **No amount of
static-analysis polish checks substitutes for actually seeing the
slide.** This is more important than any other recommendation in the
transcript.

**2. Diagnosis is unverified.** Neither agent asked "show me a wonky
slide and we'll figure out the root cause." The slides I read
(`mission_families`, `current_and_future_classes`) are actually
polished — careful insets, validated geometry, paired contrast. If
new agent-generated slides look bad, the question isn't "what helpers
are missing?" — it's "why aren't agents modeling after the good
slides that already exist?" Points at:
   - No enforced exemplar pattern (agents start cold without reading
     existing slides)
   - No vision-back loop (point 1)
   - Maybe just thin defaults on `text_box()`

**3. Explicit invariant guards inside slide modules are
underused.** `current_and_future_classes.py:132-147` has
`_validate_layout()` that raises if geometry breaks. That pattern is
more powerful than any framework-level check because it's specific
to the slide. The README should explicitly encourage every
non-trivial slide to add one. Cheap, agent-readable, fail-fast.

**4. "Page not fleshed out enough" is partly a content problem, not a
framework problem.** No Python helper makes an agent decide to add a
secondary callout or supporting evidence. That's a prompting /
agent-instruction problem — the README's authoring guidance needs to
say "if your body region is <50% covered, you haven't finished the
slide" as a *design* rule, not just a checker output.

---

## 4. Recommended action order (if user wants to proceed)

Highest leverage first:

1. **Add PNG rendering to `build.py`** (`--preview` flag, LibreOffice
   headless). Agents can read PNGs back via their own vision. Single
   biggest win. Implementation outline:
   ```python
   # after strip_all_shadows()
   if preview:
       subprocess.run([
           "soffice", "--headless", "--convert-to", "png",
           "--outdir", str(OUT_DIR / "preview"), str(out_path),
       ], check=True)
   ```
   `soffice` produces one PNG per slide; name them
   `submarine_deck-<n>.png` or similar.

2. **Beef up `layout_check.py` into `polish_check.py`**: stricter
   underfill thresholds, inset checks on filled shapes, body-occupancy
   minimum, run by default in `build.py`. Make output suggest specific
   fixes ("Card 'X' is 18% filled; shrink the card height or add a
   second body sentence").

3. **Add a thin `layout.py` with `Region`** + `.split_cols`,
   `.split_rows`, `.grid`, `.inset`. Optional helper, not mandatory.

4. **Add 4–5 smart components** (`card`, `callout_band`, `kpi_tile`,
   `chart_panel`, `text_panel`) that pre-set padding/typography. Don't
   add more — risk of fragmentation.

5. **Update README** to: name 2–3 reference slides as exemplars ("for
   3-column cards, model after `mission_families.py`"), encourage
   `_validate_layout()` guards on non-trivial slides, state the
   body-occupancy rule as a design rule (not just a checker output).

6. **Skip**: SlideBrief, density modes, auto-nudge, recipes,
   mandatory compositions, manifest-driven deck config (that's a
   different concern from polish anyway and the user's existing
   `SLIDES = [...]` list in `build.py` is fine for now).

The user's instinct that "primitives = creative starters" is sound.
Don't restrict creativity with templates. The fix is **feedback +
better building blocks + clearer defaults**, not more rigid
scaffolding.

---

## 5. Files created / modified this session

**None.** This session was read + discussion only. Deck state on disk
unchanged from end of session 5 (plus whatever in-between sessions
built — the current 20-slide `SLIDES` list is well beyond session 5's
7-slide manifest).

---

## 6. Quick orientation for next agent

**If user asks "what was the last session about":** Pipeline read +
critique of an external transcript proposing pipeline improvements. No
code changes. Section 3 of this log has the critique distilled;
Section 4 has the recommended action order.

**If user wants to act on the critique:** Start with item 1
(render-to-PNG). It's the highest-leverage change and unblocks the
agent's ability to self-evaluate. Items 2–5 can run in any order
after that.

**If user wants to push back on the critique:** the slides I sampled
(`mission_families.py`, `current_and_future_classes.py`) looked
polished to me, not wonky. The "agent slides look bad" diagnosis
isn't independently verified in this session. Could be worth pulling
a specific wonky slide into the discussion to ground the next round
of changes.

**If user asks "where's the deck":**
`/Users/brendantoole/projects2/submarine_outsourced_work/deck/out/submarine_deck.pptx`.
Rebuild with `python3 build.py` from `deck/`.

**If user asks "what's the pipeline":** See Section 2 above, or read
`deck/HANDOFF.md` directly (it's the authoritative refactor doc).

**Memory updates this session:** none made. Nothing in the
conversation rose to the "save to memory" bar — the critique is
specific to *this* pipeline so it lives here in the log, not in
cross-session memory.
