SLIDE 02 - Subaward Activity as the Period-of-Performance Proxy
Type: Body (methodology)

Slide's purpose:
  FFATA/FSRS subaward records carry no period-of-performance field, so engagement depth cannot be
  read directly. This slide documents the proxy built in its place: two observed axes - Duration
  (first-to-last reported-action span, the PoP stand-in) and Breadth (distinct subaward numbers) -
  each cut into a 0-3 tier and collapsed into an Observed Activity Profile by the higher of the two
  tiers. The 4x4 matrix shows the joint vendor distribution (n = 1102 vendors). The slide must also
  state the honest limits: spans are reporting-based lower bounds, later blocks are right-censored,
  and the tier thresholds are analyst-defined, not contractual.

TITLE
-----
Copy:
  Subaward Activity | With no period-of-performance field, observed span and breadth proxy engagement depth.

HIGH-LEVEL LAYOUT
-----------------
Pattern C - measured exhibit left, commentary right, definitions below.
  - Title band, then a tier caption (italic) directly under it.
  - Left (~58% width): the 4x4 Breadth x Duration vendor-count matrix (heatmap), with an "All"
    total column and row, and the grand-total cell (1102) at the corner.
  - Right (~38% width): commentary rail - three bold findings, each with non-bold bullets.
  - Bottom (full width, below the matrix): a compact tier-scale definition strip (Breadth /
    Duration / Profile) plus a one-line churn pointer.
  - Source note at the foot.
The matrix is the one heavy/filled object family on the slide; commentary and the tier strip stay
no-fill so the heatmap reads as the focal exhibit.

COMMENTARY COPY, IF NEEDED
--------------------------
Commentary 1
  Copy:
    FFATA/FSRS subaward records carry no period-of-performance field.
    - First-to-last reported-action span (years) is the closest available proxy for engagement duration.
    - Distinct subaward numbers (deduped) give the second, breadth axis.
  Text / shape treatment:
    No-fill, no-border rail. Bold finding sentence 11 pt, black; bullets 9 pt regular, black.

Commentary 2
  Copy:
    The Observed Activity Profile takes the higher of the two tiers.
    - Profile = CHOOSE(MAX(breadth tier, duration tier)): Single / one-time, Limited, Established, High / sustained activity.
    - One axis alone misleads, so the matrix keeps both visible rather than only the collapsed label.
  Text / shape treatment:
    Same rail, one blank line above the bold finding. "CHOOSE(MAX(...))" is a formula, so the
    parentheses read as a formula, not shorthand.

Commentary 3
  Copy:
    Observed span is a lower bound, not contractual PoP.
    - Later blocks and MYPs are right-censored, so spans and continuity understate the truth.
    - Same-date first and last actions read as 0; Span / Prime PoP only says whether a vendor tracks the prime's PoP window.
  Text / shape treatment:
    Same rail, one blank line above the bold finding. This is the load-bearing caveat - keep all
    of it even when trimming.

OTHER VISIBLE COPY, IF NEEDED
-----------------------------
Copy:
  Tier-scale definition strip (bottom, full width) - three mini-scales:
    Breadth (distinct subawards):  0 = 1 sub  |  1 = 2-3  |  2 = 4-9  |  3 = 10+
    Duration (reported span, yrs): 0 = none   |  1 = <2   |  2 = 2-6  |  3 = >=6
    Profile (higher tier wins):    Single / one-time  ->  Limited  ->  Established  ->  High / sustained activity

  Churn pointer (one italic line under the strip):
    The same span data drives block-to-block churn: each block's vendors split into First observed,
    Reactivated (seen in an earlier block but not the immediate predecessor), and Continued from prior.

Text / visual treatment:
  - Tier strip: three labeled rows of small chips/segments, 9 pt. The Breadth and Duration scales
    are gray segments (F2F2F2 -> D9D9D9 -> BFBFBF -> 7F7F7F) rising with tier; the Profile scale
    ramps blue (E2E9EF -> B6C8D8 -> 6E91B1 -> 3D5972, white text on the last two) to echo the
    matrix intensity. The "|" separators are dividers, the "->" on the Profile row is an ordered
    flow (allowed).
  - Churn pointer: 8.5 pt italic, no fill, no border. It is a pointer to a related use, not the
    focus - it must be the first thing cut if space is tight.

CHART, IF NEEDED
----------------
None. The matrix (a count table with heatmap fills) carries the quantitative shape; see TABLE.

TABLE, IF NEEDED
----------------
THE MATRIX - Breadth x Duration vendor-count matrix (the metric made visible)

Copy / rows / columns:
  Corner header: Breadth \ Duration
  Column headers: Dur 0 (none) | Dur 1 (<2y) | Dur 2 (2-6y) | Dur 3 (>=6y) | All
  Row headers:    Breadth 0 (1 sub) | Breadth 1 (2-3) | Breadth 2 (4-9) | Breadth 3 (10+) | All
  Cells: vendor counts (live COUNTIFS over the vendor rollup tier columns).
  Margins: an "All" total column (row sums) and an "All" total row (column sums).
  Grand-total cell (corner of the margins): 1102.

Purpose:
  Show both proxy axes at once and how the 1102 vendors distribute across them - the upper-right
  (high breadth, long duration) is the deep-engagement corner; the lower-left is single, one-time
  activity. Demonstrates the Profile is a real distribution, not a label asserted.

Structure:
  4x4 count matrix plus margins. Both axes ordered ascending (tier 0 -> 3), so intensity rises
  toward the bottom-right. Cells are counts; the two "All" margins and the grand total reconcile
  (row "All" sums = column "All" sums = 1102).

Cell / table treatment:
  - Counts centered in every cell.
  - Heatmap: cell fill ramps blue by count magnitude - low E2E9EF -> high 263746; cells dark
    enough (from 6E91B1 up) take white text. This is the slide's one filled object family.
  - Column and row headers: 9 pt bold, no fill (carried by the rule), left/center as fits.
  - "All" margin row and column: bold counts, light-gray F2F2F2 fill to separate totals from the body.
  - Grand-total cell (1102): dark fill 263746, white bold - the anchor number.
  - Rules: 1.5 pt under the column-header row, 1 pt above the "All" total row; otherwise let the
    heatmap fills carry the grid (avoid a full interior lattice).
  - Watch row height vs the 9-14 pt counts - keep rows tight so the matrix does not look airy.

Fit behavior:
  All 16 body cells + both margins + the 1102 grand total must stay visible. Shorten the threshold
  text inside the row/column headers first (e.g. "2-6y" stays, "(2-6y)" parens can drop). Do not
  add a dollars axis or a third dimension to this matrix.

OBJECT NOTES, IF NEEDED
-----------------------
  - The matrix reads bottom-right = most intense engagement; keep that orientation (do not flip
    either axis to descending).
  - The grand-total cell (1102) must reconcile to the vendor count (UEI grain) - it is the
    cross-check, so it should be visually unmissable (dark anchor cell).
  - Commentary rail bullets hang on their bold finding; keep one blank line between the three
    finding groups so the bold lines, read alone, are the three takeaways.
  - Do not promote churn (First observed / Reactivated / Continued) to its own table here - this
    slide is the engagement-depth proxy, not the churn slide; the one-line pointer is enough.

TYPOGRAPHY HIERARCHY (Arial throughout)
---------------------------------------
  - Title "Topic | Finding.": 20 pt. Topic ("Subaward Activity") bold; Finding regular, sentence
    case, ending in a period.
  - Tier caption (under title): 8.5 pt italic - it is a qualifier ("analyst-defined, not contractual").
  - Matrix column/row headers: 9 pt bold.
  - Matrix body counts: 9 pt regular; the "All" margin counts and the grand total: 14 pt bold
    (compact numeric value treatment, so the totals and the 1102 anchor stand out).
  - Commentary finding sentences: 11 pt bold; commentary bullets: 9 pt regular.
  - Tier-scale strip labels: 9 pt (the row label "Breadth" / "Duration" / "Profile" 9 pt bold,
    the segment text 9 pt regular).
  - Churn pointer: 8.5 pt italic.
  - Source note: 8 pt.
  Hierarchy logic: bold carries the takeaways (the three finding sentences) and the value cells
  (margin totals, 1102); italic marks the two caveats (tier caption, churn pointer); the 14 pt
  totals are the only numerics promoted above body size, so the eye lands on the reconciling
  numbers.

BACKGROUND / FILL COLOR
-----------------------
  - Slide background: white (FFFFFF), no fill.
  - Matrix body cells: blue heatmap ramp by count - E2E9EF, B6C8D8, 6E91B1, 3D5972, 263746 from
    low to high; white text from 6E91B1 (third step) upward. 1 pt black border on filled cells, or
    rely on tight rules - keep it to one border family.
  - Matrix margins ("All" row/column): light-gray F2F2F2 fill, black bold text, to read as totals.
  - Grand-total cell (1102): dark 263746 fill, white bold - the single darkest anchor.
  - Tier strip: Breadth and Duration segments ramp GRAY (F2F2F2 -> D9D9D9 -> BFBFBF -> 7F7F7F,
    white text on 7F7F7F) to signal "descriptive, not the headline"; the Profile segments ramp
    BLUE (E2E9EF -> B6C8D8 -> 6E91B1 -> 3D5972, white text on the last two) to tie back to the
    matrix. 1 pt black border on each filled segment.
  - Commentary rail, tier caption, churn pointer, source: no fill, no border (interpretive text).
  - Fill rule honored: fill marks semantic weight only - count intensity (heatmap), totals
    (gray margins), the reconciling anchor (dark 1102), and the ordered tier scales. Findings and
    caveats stay no-fill. Dark fills always take white text.
  - No pale-yellow placeholder (FFFFCC) is needed - the matrix has live data.

SOURCES
-------
Copy:
  FFATA/FSRS subaward transactions (USAspending); prime period-of-performance from SAM.gov prime
  awards. Tiers are analyst-defined descriptive thresholds, not contractual. Matrix grain = vendor
  (UEI), n = 1102.
