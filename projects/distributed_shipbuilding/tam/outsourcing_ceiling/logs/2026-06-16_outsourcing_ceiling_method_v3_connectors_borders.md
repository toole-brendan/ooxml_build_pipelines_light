# 2026-06-16 — Outsourcing Ceiling method v3: connector weight/touching, box alignment, formula border

Slide module: `projects/distributed_shipbuilding/deck_primary/deck_primary/slides/outsourcing_ceiling_method_v3.py`
Deck launcher: `projects/distributed_shipbuilding/deck_primary/build_deck.py`
Deck output:  `projects/distributed_shipbuilding/20260610_Distributed Shipbuilding New Construction_vS.pptx` (12 slides, 7 charts)
Build:  `cd projects/distributed_shipbuilding/deck_primary && python3 build_deck.py`
Probe:  `cd <repo root> && PYTHONPATH=.:projects/distributed_shipbuilding/deck_primary python3 -m deck_core.slide_probe deck_primary.slides.outsourcing_ceiling_method_v3 --text-estimate --out-dir /tmp/probe_v3`

Reference for the target look: v1 = `outsourcing_ceiling_method.py` (sibling in the same slides dir).

## Goal

Polish the v3 slide to match v1's qualities on four user-requested points:
connector weight, connectors touching their from/to shapes, shape sizing /
text fitting / vertical alignment within boxes, and a black exterior border on
every colored-fill shape.

## Changes

- **Connector weight `_CONN_PT` 6350 (½pt) → 9525 (¾pt).** Note: v1 actually codes
  its connectors at ½pt too (`_CONN_W_PT = 6350`), identical to what v3 already had —
  so the source weights were never different. What made v3 *read* lighter is that
  several runs are short stubs (the three vertical ticks are only ~0.2", the dial
  drop ~0.36"), where a med arrowhead swamps a ½pt line. Took them to ¾pt for
  presence, still below the 1pt box-border weight so they stay flow lines, not
  emphasis. (Flagged to the user; revert to ½pt on request.)
- **Connectors now touch both endpoints:**
  - Flow arrows: tail on box *i*'s right edge, arrowhead on box *i+1*'s left edge —
    the full `_BOX_GAP` (380k) is the connector run. Removed the old `_CONN_INSET`
    (40k each side) that floated them mid-gap; deleted the now-unused constant.
  - Dial drop: `_DIAL_DROP_Y = _FLOW_B` (ceiling-box bottom edge, was `+30_000`) and
    `_DIAL_DROP_CY = _FORMULA_Y - _FLOW_B` (lands exactly on the formula top edge).
    Reordered so `_FORMULA_Y` is defined before the dial-drop geometry that uses it.
  - The three ticks already touched (formula bottom → read-card top); unchanged.
- **Box text vertical alignment `anchor="t"` → `"ctr"`** on the four flow boxes,
  matching v1's centered cards (v1 uses `anchor="ctr"` on inputs/engine/reads). The
  old top-anchor left whitespace pooling at the bottom of each box.
- **Sublines breathe:** added a local `_BOX_INSETS = (91_440, 76_200, 91_440, 76_200)`
  (0.1" l/r vs `INSETS_CARD`'s 0.125"; vertical insets unchanged) used only by the
  flow boxes — did NOT touch the shared `INSETS_CARD` (still used by the read cards).
  Box1 dropped from 5 wrapped lines to 4; all four boxes now fit uniformly at 4 lines.
- **Formula node black border:** `BridgeFormula` was the only colored-fill shape with
  `line_color="none"`. Removed that arg so `text_box`'s house auto-border applies
  (filled shape → 1pt black), matching every other box, read card, and guardrail chip.

## Verification

- Deck **builds green** (12 slides, 7 charts).
- Slide-probe confirms:
  - All 7 connectors render at **0.75pt** (was 0.50pt).
  - `BridgeFormula` line = `000000` at **1.00pt** (was `none`); all colored-fill
    shapes now carry the black border.
  - Flow arrows: `Step1to2` x=2,043,079 (Box1 right) → 2,423,079 (Box2 left); same
    pattern for Step2to3 / Step3to4. Dial drop y=2,760,000 (Box4 bottom) →
    3,090,000 (formula top). All touching.
  - Boxes render `anchor=ctr`; text-estimate shows all four at 4 wrapped lines /
    0.551" centered in 0.883" avail, fits=True.

## State / notes

- The narrow four-across box width (1.739") is inherent to v3's design — v1 only has
  three flow cards so it can afford wider boxes; matching v1's box width would require
  a layout redesign, not pursued. Centering + trimmed insets was the in-design fix.
- The probe's `fits=False` on the Breadcrumb chrome element is pre-existing and shared
  across slides (not from this work).
- Reader-facing deck slide; not wired to the workbook (numbers kept in sync by hand,
  per the module docstring).
