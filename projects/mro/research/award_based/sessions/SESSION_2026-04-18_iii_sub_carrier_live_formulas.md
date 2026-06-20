# Session 2026-04-18 (iii): Sub & Carrier Coverage - remaining hardcodes stripped - v2.73 -> v2.74

## Context

Follow-up to session (ii). That session had converted the reconciliation
headline and Budget Anchors reference table on
`sheets/sub_carrier_coverage.py` to live SUMIFS / named-cell refs
(v2.71). User opened v2.73 and flagged that a ton of the sheet was still
hardcoded - specifically the 5 Top-N PIID tables and the 6 scope-
reconciliation note paragraphs at the bottom. Willing to delete
non-essential content, but wanted the budget-anchor section and all PSC
content kept.

Ended at **v2.74** with every $ cell on the sheet driven by a formula
and the narrative notes removed in favor of a pointer to the existing
methodology doc.

---

## Work completed, in order

### 1. Audit of what was still hardcoded

Read `sheets/sub_carrier_coverage.py` in full and catalogued every
numeric cell. Three sections were already fully live (reconciliation
headline rows 126-288, Budget Anchors refs 291-357, Nuclear Maint
emptiness 360-412). Two sections were not:

- **5 Top-N PIID tables** (~64 rows total). `_write_top_piids` line 448
  wrote FY25 $M as the Python literal
  `(a.get('fy2025_obligation') or 0) / 1e6`. Text columns (PIID, parent,
  hull, description, contracting office) are inherently row-descriptive
  and must stay Python-written.
- **6 Scope Reconciliation Notes** (`_write_scope_reconciliation_notes`,
  lines 457-507). Each note was a paragraph with $ figures baked into
  the prose: "$24.3B sub x 1905", "$9.3B + $6.2B + $3.1B = $18.6B",
  "$424M HII Boise", "$96.6M + $28.5M CVN-68 inactivation", "$318M
  Draper", "$366M BlueForge". Prose + Excel formula doesn't compose.

Confirmed via Read that `services.py:580` uses SUMIFS with a parent-
name filter for its top-N $M cells (with a 8,192-char-limit fallback
to a literal). Precedent established that rank order is frozen at
build time but $ stays live.

Confirmed Awards table columns (`sheets/awards.py:35-76`) expose PIID
(col 2), FY2025 Obligation (col 6), Vessel Type (col 10, from
`vessel_supergroup`) - the filters we need.

### 2. Two user decisions via AskUserQuestion

1. Top-N PIID tables -> **convert $M to SUMIFS-by-PIID**, keep all 5
   tables. (Alt: delete entirely; or keep only the 2 PSC 1905 tables.)
2. Scope reconciliation notes -> **delete all 6**, replace with a
   one-line pointer to METHODOLOGY_CVN_SSN_COVERAGE.md. (Alt: strip
   embedded $ from prose; or leave as-is.)

### 3. Implementation - `sheets/sub_carrier_coverage.py`

Single-file edit. Changes:

- **New helper `_sumifs_piid(piid, vessel_type=None)`** alongside the
  existing `_sumifs_one` / `_sumifs_many` / `_sumifs_vessel_total`.
  Returns a full formula `=SUMIFS(Awards[FY2025 Obligation],
  Awards[PIID],"<esc>",Awards[Vessel Type],"<vt>")/1000000` with
  optional vessel-type filter. Formula length ~90 chars; way under the
  8,192 per-cell limit, no fallback branch needed.
- **`_write_top_piids` gains `vessel_type=None` kwarg.** Line 448 (the
  $M cell) now calls `_sumifs_piid(a.get('piid'), vessel_type=...)`.
- **5 call sites updated:**
  - Sub Newbuild PSC 1905 -> `vessel_type='Submarines'`
  - Sub Services MRO -> `vessel_type='Submarines'`
  - Carrier Newbuild PSC 1905 -> `vessel_type='Aircraft Carriers'`
  - Carrier Services MRO -> `vessel_type='Aircraft Carriers'`
  - PSC 4470 Nuclear Reactors -> `vessel_type=None` (reactor rows
    carry blank `vessel_supergroup`; filtering by vessel type would
    zero the cells out)
- **Why the Vessel Type filter matters**: services PSCs are exploded
  per-hull by `vessel_explode_v2.py`, so a single PIID can appear on
  multiple hull rows in Awards. Python does
  `_platform_rows(all_rows, 'Submarines')` BEFORE sorting, so the
  top-N-picker sees only sub hulls. A bare `SUMIFS(PIID)` in Excel
  would collapse across ALL hulls including non-sub ones. Adding
  `Awards[Vessel Type],"Submarines"` preserves the platform slice.
  For newbuild PSCs (1 row per PIID, no explosion), the filter is
  redundant-but-robust.
- **`_write_scope_reconciliation_notes` deleted** and replaced by
  `_write_narrative_pointer` - a `subsec_band` + single gray-text row
  pointing at `docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md`.
- **Docstrings updated**: module docstring (lines 25-27) no longer
  claims Top-N $ is static; `_write_top_piids` docstring explains the
  rank-frozen / $-live split and the `vessel_type` parameter;
  `create_sub_carrier_coverage` Layout block drops the scope-notes
  bullet.
- **Build print** at the end shortened to `all $ live via formulas`.

### 4. Smoke test

`/tmp/smoke_sub_carrier_v2.py` - builds Awards + Budget Anchors + Sub &
Carrier Coverage into a scratch workbook, then walks column F looking
for `=SUMIFS` strings.

Ran with `PYTHONPATH=. python3 /tmp/smoke_sub_carrier_v2.py` from
`/Users/brendantoole/projects2`. Output:

```
Found 64 SUMIFS formulas in column F
First 3 samples:
  row 34: =SUMIFS(Awards[FY2025 Obligation],Awards[PIID],"N0002417C2100",Awards[Vessel Type],"Submarines")/1000000
  row 35: =SUMIFS(Awards[FY2025 Obligation],Awards[PIID],"N0002417C2117",Awards[Vessel Type],"Submarines")/1000000
  row 36: =SUMIFS(Awards[FY2025 Obligation],Awards[PIID],"N0002424C2110",Awards[Vessel Type],"Submarines")/1000000
Last 3 samples:
  row 111: =SUMIFS(Awards[FY2025 Obligation],Awards[PIID],"N0010425CBA07")/1000000
  row 112: =SUMIFS(Awards[FY2025 Obligation],Awards[PIID],"N4523A25P4113")/1000000
  row 113: =SUMIFS(Awards[FY2025 Obligation],Awards[PIID],"N0002419C2122")/1000000

Vessel Type filter breakdown:
  Submarines:        27
  Aircraft Carriers: 27
  No vessel filter:  10

Narrative pointer OK; old scope-notes block is gone.
```

Counts check: 27 Sub = 15 newbuild + 12 services; 27 Carrier = 15 + 12;
10 no-filter = PSC 4470 reactors; total 64. Matches plan exactly.

Row 34 top-1 PIID is `N0002417C2100` (Electric Boat Columbia MPU) - the
same top-1 PIID the session (ii) log recorded at $9,336M. Correct rank.

### 5. Full build - v2.74

Ran `python3 -m domnann.build_from_data`. v2.73 auto-archived. v2.74
saved. Sheet order unchanged:

```
Overview -> Product Procurement -> Services -> Depot Ship Repair
-> Sub & Carrier Coverage -> Sub Ratios -> Public Comps -> Awards
-> J998 J999 Data -> Subcontract Data -> Budget Anchors -> Vessel Taxonomy
```

Build line for the refactored sheet:

```
Built Sub & Carrier Coverage (277 sub rows $25,941M, 281 carrier rows $1,867M; all $ live via formulas)
```

Same row counts and totals as v2.71 and v2.73 - the refactor did not
change the underlying data, only how the cells are rendered.

---

## Files touched

### Modified

- `sheets/sub_carrier_coverage.py` - single file. New `_sumifs_piid`
  helper, `_write_top_piids` signature change + $M conversion, 5 call
  sites updated, `_write_scope_reconciliation_notes` replaced by
  `_write_narrative_pointer`, docstring + print updates.

### Unchanged (intentionally)

- `sheets/budget_anchors.py` - already correct; all 7 named cells still
  referenced from the coverage sheet.
- `sheets/awards.py`, `sheets/services.py`, `build_from_data.py` - no
  changes needed.
- `deck/SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md` - slide consumes
  reconciliation headline + Budget Anchors, both already live. No
  slide content affected.
- `docs/methodology/METHODOLOGY_CVN_SSN_COVERAGE.md` - pointed to from
  the new pointer row but not edited.

### Scratch (not committed)

- `/tmp/smoke_sub_carrier_v2.py` - isolation smoke test
- `/tmp/test_sub_carrier_v2.xlsx` - output of the smoke test

---

## Key numbers (unchanged from v2.71)

FY2025 FPDS obligations, unified Awards master:

| Platform          | Rows | Total FPDS $M |
|-------------------|-----:|--------------:|
| Submarines        |  277 |       $25,941 |
| Aircraft Carriers |  281 |        $1,867 |

Top-1 PIID per table (all now live-computed from Awards, not Python
literals):

| Table | PIID | Contractor | Approx $M |
|-------|------|------------|-----------|
| Sub Newbuild PSC 1905 | N0002417C2100 | Electric Boat | 9,336 |
| Sub Services MRO | N0003024C6001 | Draper Lab | 318 |
| Carrier Newbuild PSC 1905 | N0002425C2127 + CVN-80/81 | HII | varies |
| Carrier Services MRO | N4523A25F0302 | HII (Puget Sound) | 91 |
| PSC 4470 Reactors | N0002418C2130 | Fluor Marine Propulsion | 1,810 |

---

## Follow-up / future work

1. Open v2.74 in Excel and confirm the 64 Top-N $M cells recompute to
   values matching the v2.71 hardcoded snapshot. Smoke test verifies
   the formula strings are syntactically correct; Excel's evaluation
   is the only thing that confirms the actual numbers match.
2. The 4 open questions from session (ii) remain open: nuclear-
   platform carve-out of the $9.5B public-yard figure, BlueForge SIB
   tagging, Budget Anchors expansion to cover NWCF / OPN / WPN / USCG,
   whether Slide 5 moves into DECK.md. None of these were touched in
   this session.
3. If v2.74 is committed as a milestone, the file needs `git add -f`
   per the `output/archive/` gitignore note in CLAUDE.md. (v2.73 was
   auto-archived by the build script and is also gitignored.)
