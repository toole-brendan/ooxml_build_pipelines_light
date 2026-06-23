# 2026-06-23 — Closed the concentration-accessor layout-drift hazard (RowCursor named anchors)

Review session on `award_classification/workbook_award_classification_refactor`
(`award_classification_refactor.xlsx`). The ask was a design review of the workbook's **data
dependency graph** and whether the **flow / formulas** could be made top-notch (keeping
row-position A1 refs, **no named ranges**). The review concluded the architecture is **already
top-tier** and surfaced exactly **one** genuine structural hazard — a silent layout-drift hole
in the two hand-built concentration sheets' cross-sheet accessors — which this session **fixed**
(the **Tier 2** option: guard + unify, delete the magic constants). Per the user's call, the
**live formulas were left untouched** (already near-optimal; remaining complexity is irreducible
domain logic).

Workbook stays **21 sheets**, **15 native tables**. Build clean (**0 XML errors, 0 error-literal
cells**). The three touched sheets emit **byte-identical** worksheet XML vs the pre-change build
(verified by SHA) — the fix changes *when* rows are built, not *what* is emitted.

Everything is **uncommitted** (working tree only).

---

## The hazard (confirmed real by an adversarial design panel)

The workbook records "where my rows landed so a downstream formula can point at them" **four**
ways, all encoding one idea — *derive the downstream ref from the same value used to write the
row, never let a second computation drift.* **Three self-validate:** `Cols` on flat sheets
(bounds from CSV length); `_program_vendors.py:181` `assert (cols.first,cols.last)==(_first,_last)`;
`deflators.py:72` `assert _FFIRST==_FIRST_DATA_ROW`. **Two did not:**

- `sheets/domain_concentration.py` — `domain_conc_range()` from hand-counted
  `_FIRST_DOMAIN_ROW = 9`, `_PROGRAM_STRIDE = len(DOMAINS) + 5`.
- `sheets/parent_concentration.py` — `parent_conc_range()`, `_PROGRAM_STRIDE = len(DOMAINS) + 4`.

The **`+5` vs `+4`** difference is load-bearing (Domain has a `c.total` row, Parent doesn't) and
hand-maintained. **Nothing tied either constant to what `render()` actually emits.** Add a caveat
line / blank / total to a concentration `render()` and the accessor window shifts one row onto the
**text header row** (silently ignored by `MAXIFS`/`MATCH`) while dropping the last real domain →
`executive_summary._concentration_headlines` (the front-door §3 headline) names the **wrong**
"most concentrated material domain" with a **wrong-but-valid** value and **no `#REF!` anywhere**.

**Nothing catches it today:** `lib.build()`'s seven `_integrity` asserts are CSV-universe checks,
not layout; `validate_workbook.py` (openpyxl, post-build) only flags `#REF!`-style literals, and a
valid-but-wrong range produces a plausible number, not an error. There is **no test suite**.

A 4-agent design panel (workflow `wf_766848d2-b32`) **adversarially tried to refute** the hazard
and **failed** — it traced the exact path (one extra caveat line → window 9:20 → 8:19 → argmax
over 11 of 12 domains + a header cell → wrong §3 headline, no error literal). It recommended
**Tier 2** and was explicit about what to leave alone.

---

## Decisions locked this session

- **Scope = Tier 2** (guard **and** unify): add a single named-anchor mechanism to `RowCursor`,
  capture each concentration block's real first/last data row during the write walk, read the
  accessor off those anchors, and **delete** the magic constants — same structural guarantee
  `Cols` already gives flat sheets. (Tier 1 = assert-only was the conservative floor; Tier 3 =
  also collapse `subaward_activity`'s dual-walk + a dependency-graph framework was **declined** —
  the dual-walk is a working guard for an irreducible forward-reference, and Python import already
  enforces acyclicity.)
- **Formulas left as-is** (user's pick). The worst array math is already staged into hidden helper
  columns on the flat sheets; `domain_concentration` F (domain-constrained `INDEX/MATCH`) and
  `subaward_activity` §4 (distinct-count `SUMPRODUCT`) are irreducible. No formula changed.

---

## What changed (3 files, +111 / −68)

### `sheets/_layout.py` — `RowCursor` gains named anchors (purely additive)
- `self.marks: dict[str,int]` in `__init__`; new keyword-only `mark="name"` on
  `write()` / `banner()` / `total()` records the emitted row (`self.marks[mark] = r0`) **after**
  emit; `marked(name)` reader. **Return values unchanged**, params keyword-only with defaults —
  every existing call site (every sheet flows through `RowCursor`) is untouched.

### `sheets/domain_concentration.py` + `sheets/parent_concentration.py` — eager build, capture, delete constants
- Restructured to the **`make_flat_sheet` shape**: the row walk now runs **at import** (inside the
  `_make_*` factory), so anchors exist **before** the Executive Summary renders. This was the
  load-bearing ordering fact — Exec Summary is `SHEETS[0]` and *calls* the accessor inside its own
  `render()`, which runs **earlier** in `SHEETS` order than the concentration sheets'; anchors
  captured during *their* `render()` would not exist yet. (Same trick `Cols` and
  `subaward_activity`'s `_ACTIVITY_REFS` already use.)
- Each program block tags its first/last domain row as the cursor writes it
  (`mark=f"{prog}:first"` / `f"{prog}:last"`). `_make_*` now returns `(SheetEntry, anchors)`;
  `render()` is a thin closure wrapping the already-built `c.rows`.
- `domain_conc_range` / `parent_conc_range` read `_ANCHORS[f"{program}:first/last"]` (column
  letter still from `_HEADERS.index` — still positional A1, no named ranges) with a cheap
  `assert last == first + len(DOMAINS) - 1` belt-and-suspenders.
- **Deleted** `_FIRST_DOMAIN_ROW`, `_PROGRAM_STRIDE` (`+5` and `+4`), `_PROGRAM_INDEX` — confirmed
  none remain. The `+5`-vs-`+4` asymmetry simply disappears; the cursor records whichever rows
  were actually written.

---

## Verification (all green)

| Check | Result |
|---|---|
| `python3 build_workbook.py` | exit 0, **21 sheets, 15 tables** |
| Worksheet XML — sheet1 (Exec Summary), sheet2 (Domain Conc), sheet3 (Parent Conc) vs pre-change baseline | **byte-identical** (matching SHAs) — no emitted formula changed |
| `python3 validate_workbook.py` | parts 73, **0 XML errors, 0 error-literal cells** |
| §3 ref sanity | `Executive Summary!C22` → `INDEX('Domain Concentration'!$D$9:$D$20, MATCH(…))`; `Domain Concentration!B9`=`D1 Hull…`, `B20`=`D0 Unresolved` (Virginia block, 12 domains, rows 9-20) ✓ |
| **Drift test (the payoff)** | injected a stray `c.blank()` into the Domain Conc build → block moved 9:20 → **10:21** (`B9` empty, `B10`=`D1 Hull…`, `B21`=`D0 Unresolved`), and `Executive Summary!C22`'s range **followed automatically** to `$D$10:$D$21`. Under the old constants it would have stayed pinned at `9:20` and silently read the wrong cells. **Reverted**; rebuild confirmed byte-identical to baseline again. |

---

## Build / verify

```
python3 build_workbook.py        # -> 21 sheets, 15 native tables, exit 0
python3 validate_workbook.py     # 0 xml errors, 0 error-literal cells
# byte-equivalence: unzip xl/worksheets/sheet{1,2,3}.xml before/after -> identical SHAs
# drift proof: add a stray c.blank() in domain_concentration build -> exec §3 range tracks it (then revert)
```

## Files

- **Modified (engine helper):** `workbook_award_classification_refactor/sheets/_layout.py`
  (`RowCursor` named-anchor capture — additive, keyword-only).
- **Modified (sheets):** `sheets/domain_concentration.py`, `sheets/parent_concentration.py`
  (eager-import build, anchor capture, magic constants deleted, accessor reads anchors).
- **No data regen**; regenerated `award_classification_refactor.xlsx` (identical worksheet bytes).

## Carry-forward

- **Nothing committed** — all changes are in the working tree only.
- **Intentionally left alone** (already self-validating or irreducible — do **not** "unify" them):
  `Cols` on flat sheets; `_program_vendors.py` / `deflators.py` asserts; `subaward_activity.py`'s
  dual-walk + `assert c.at()==anchor` lines (a working guard for the §1→§2 / §4→§3 forward-ref);
  the two hard live formulas; the `_integrity` universe guards; the import-order dependency graph.
- **New reusable capability:** `RowCursor.mark=` / `marked()` is now the one documented way for a
  *hand-built* sheet to expose row positions to another sheet without a parallel hand-counted
  constant. Future referenced multi-section sheets should use it rather than re-deriving layout.
- **Formula simplification was explicitly deferred** (the one candidate the panel found — staging a
  hidden "material Top-1 share" helper column on Domain Concentration so Exec §3's `MAXIFS` +
  boolean-product `MATCH` collapses to `MATCH(MAX(col),col,0)`, also killing a float-equality tie
  risk). Revisit only if §3's formula or that tie case becomes a problem; gate behind a built-
  workbook formula diff since there are no tests.
- Plan file for this session: `~/.claude/plans/please-review-this-wise-wave.md`.
