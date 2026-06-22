#!/usr/bin/env python3
"""extract_budget_cuts - mine the OPA watercraft procurement spine into workbook CSVs.

Reads the OPA BA3&4 ("Other Support Equipment & Spares", OPA Volume 3) budget
justification books FY2022-FY2027 from txt_versions/ and emits three collated
CSVs into ../../workbook/extracted/ - the workbook pipeline's data dir, loaded at
build time by workbook_army.lib.load_extracted_csv(). This is the data-mining
half of the build contract: the CSVs are the only thing the workbook reads.

WHY BA3&4 (not BA1): Army watercraft procurement lives in OPA Budget Activity 03
(Other Support Equipment), BSA 55 "Rail Float Containerization Equipment" - NOT
in BA1 (Tactical & Support Vehicles). The BA1 book carries only the
appropriation-wide P-1 *index* line; the funding tables / narrative are in Vol 3.

THE SPINE - three P-1 line items (BLIs stable across all six vintages):
  3569M11101  Army Watercraft Esp                  (ESP: SLEP/MIBS/HCCC mods)
  8211R01001  Maneuver Support Vessel (MSV)        (MSV(L) new-construction)
  9552ML5355  Items Less Than $5.0M (Float/Rail)   (minor float/rail aggregate)

THE EXHIBIT - Exhibit P-40 "Budget Line Item Justification". Its "Resource
Summary" block is a fixed 12-column grammar parameterized by the PB year Y; only
the OCO<->OOC label drifts (immaterial - columns are derived from Y, not labels):

  col  0  Prior Years          (cumulative, pre Y-2)        role=prior_years
  col  1  FY(Y-2)              prior-year actual            role=actual
  col  2  FY(Y-1)              current-year enacted         role=enacted
  col  3  FY(Y) Base           budget-year request, base    role=request_base
  col  4  FY(Y) OCO/OOC        budget-year request, OCO     role=request_oco
  col  5  FY(Y) Total          budget-year request, total   role=request_total
  col  6  FY(Y+1)              FYDP out-year                 role=outyear
  col  7  FY(Y+2)              FYDP out-year                 role=outyear
  col  8  FY(Y+3)              FYDP out-year                 role=outyear
  col  9  FY(Y+4)              FYDP out-year                 role=outyear
  col 10  To Complete          beyond FYDP                   role=to_complete
  col 11  Total                program total                 role=total

Tidy/long output - one row per (line_item x source_book x measure x column) - so
"requested vs enacted" is DERIVABLE in the workbook and is never pre-differenced
across books (the same FY appears as request in its PB book, enacted one book
later, actual two books later; the long shape preserves every vintage's own view).

Cells: "-" -> 0.0 (DoD convention: no funding that year); "Continuing" -> blank
(program continues beyond FYDP, total not stated) - only ever in To Complete /
Total, never in the analytical per-FY columns; numbers strip commas -> float.

Outputs (../../workbook/extracted/):
  budget_line_items.csv      dimension: one row per spine line item (+ analyst tags)
  budget_funding_facts.csv   tidy facts: P-40 Resource Summary, all roles x measures
  source_log.csv             the six OPA BA3&4 books (-> workbook 11_Source_Log)

Console prints a per-book request_total tie-out for hand-checking against the txt.
Re-run after re-downloading/re-converting the corpus. Idempotent (overwrites).
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                       # research/budget_materials/
TXT = HERE / "txt_versions"
MANIFEST = HERE / "_manifest.csv"
OUT = HERE.parents[1] / "workbook" / "extracted"             # projects/army/workbook/extracted/
ACCESS_DATE = "2026-06-20"                                   # corpus download/convert date
BOOK_ID = "OPA_BA34_Other_Support_Equipment"
FYS = [2022, 2023, 2024, 2025, 2026, 2027]

# Provenance + money-semantics spine (added 2026-06-20, schema-adjustments pass;
# see logs/2026-06-20_schema_adjustments_killchain.md). extract_run_id is
# deterministic (tied to the corpus vintage, not wall-clock) so the extractor stays
# idempotent; row_hash is a value-independent identity key so an analyst overlay
# (tags / crosswalk) keyed on it survives a re-extract that corrects a parsed value.
EXTRACT_RUN_ID = f"army-budget-extract-{ACCESS_DATE}"        # bump when corpus re-pulled
DOLLARS_BASIS = "then_year"                                  # DoD justification books are
# then-year (current) dollars; a constant-$ restatement would come from the Green Book
# (National Defense Budget Estimates) deflators, never from the P-/R-forms themselves.

# column_role -> semantic money-kind. Lets the workbook filter/guard "kinds of money"
# (request vs enacted vs actual ...) without enumerating exhibit columns, and is the
# join axis when contract money (its own roles) lands on this spine later. It is NEVER
# valid to sum across distinct amount_type values (the no-double-count invariant).
AMOUNT_TYPE = {
    "prior_years":   "prior_year",
    "actual":        "actual",
    "enacted":       "enacted",
    "request_base":  "request",
    "request_oco":   "request",
    "request_total": "request",
    "outyear":       "outyear_estimate",
    "to_complete":   "to_complete",
    "total":         "total",
}


def row_hash(*parts) -> str:
    """Stable 16-hex identity key for a row, independent of its amount, so an analyst
    overlay keyed on it survives a re-extract that corrects a parsed value."""
    key = "|".join("" if p is None or p == "" else str(p) for p in parts)
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


# ---- the spine: target line items + analyst dimension tags ------------------
# mission_family / product_layer are seed analyst judgments (per the market-study
# taxonomy), flagged confidence=seed so they read as editable, not derived fact.
LINE_ITEMS = {
    "3569M11101": dict(
        title="Army Watercraft Esp",
        program="Army Watercraft Extended Service Program (ESP)",
        mission_family="Fleet modernization",
        product_layer="Platform SLEP/retrofit (LCU, LSV, MCS); C2 & comms refresh (MIBS); C2 & littoral sensing (HCCC)",
        scope_note="SLEP + Modernized Integrated Bridge System (MIBS) + Harbormaster C2 Center (HCCC) "
                   "modernization of legacy Army watercraft; narrative cites autonomous-operations enablement.",
    ),
    "8211R01001": dict(
        title="Maneuver Support Vessel (MSV)",
        program="Maneuver Support Vessel (Light) - MSV(L)",
        mission_family="Contested distribution / Operational maneuver",
        product_layer="Complete vessel (new-construction ship-to-shore connector)",
        scope_note="New-construction landing craft replacing the LCM-8; ship-to-shore / shore-to-shore connector.",
    ),
    "9552ML5355": dict(
        title="Items Less Than $5.0M (Float/Rail)",
        program="Float/Rail items < $5.0M (aggregate)",
        mission_family="Fleet modernization / enabling (minor procurement)",
        product_layer="Mixed minor float & rail items",
        scope_note="Aggregated minor-procurement line for float/rail items under $5.0M each.",
    ),
}

APPROPRIATION = "2035A Other Procurement, Army (OPA)"
BUDGET_ACTIVITY = "03 Other Support Equipment"
BSA = "55 Rail Float Containerization Equipment"

# ---- P-40 Resource Summary measure rows to capture -------------------------
# (exact label prefix as it appears in -layout text) -> (measure key, unit)
MEASURES = [
    ("Procurement Quantity (Units in Each)",        "procurement_qty",            "units"),
    ("Gross/Weapon System Cost ($ in Millions)",    "gross_weapon_system_cost",   "USD_millions"),
    ("Net Procurement (P-1) ($ in Millions)",       "net_procurement_p1",         "USD_millions"),
    ("Total Obligation Authority ($ in Millions)",  "total_obligation_authority", "USD_millions"),
]
N_COLS = 12
PAGE_RE = re.compile(r"^=====\s*PAGE\s+(\d+)\s*=====")
EXHIBIT_RE = re.compile(r"\bExhibit ([PR]-\w+)")   # P-40/P-5/P-21 and R-2/R-2A
BLI_RE = re.compile(r"\b(" + "|".join(map(re.escape, LINE_ITEMS)) + r")\b")
PE_RE = re.compile(r"\bPE\s+(\d{7}[A-Z])\s*/")
CELL_RE = re.compile(r"^-$|^Continuing$|^[\d,]+(?:\.\d+)?$", re.I)

# ---- RDT&E watercraft target (discovered by keyword sweep of all 33 R-2 books)
# The watercraft RDT&E concentrates in ONE program element across all six years:
#   PE 0603804A "Logistics and Engineer Equipment - Adv Dev" (BA4 in FY22-23,
#   BA4A in FY24-27), specifically its Project 526 "Marine Oriented Logistics
#   Equipment - Adv Dev" - AWS engineering, seaworthiness, emergent tech, trade
#   studies / BCA / AoA support. The PE total also carries non-watercraft
#   projects (EW8 Armored Engineer Vehicles, G11 Adv Elec Energy), so Project
#   526 is the watercraft-addressable line; the PE total is context only.
# (MSV(L) has no standalone development PE - it appears only inside the shared
#  AoA PE 0604100A, which funds AoAs for many programs, so it is not extracted.)
RDTE_PE = "0603804A"
RDTE_PROJECT = "526"
RDTE_BOOK = {2022: "RDTE_BA4", 2023: "RDTE_BA4",
             2024: "RDTE_BA4A", 2025: "RDTE_BA4A", 2026: "RDTE_BA4A", 2027: "RDTE_BA4A"}
RDTE_APPROP = "2040 RDT&E, Army"
RDTE_BA = "04 Advanced Component Development & Prototypes (ACD&P)"
RDTE_LINE_ITEMS = {
    "RDTE-0603804A-526": dict(
        title="Project 526 - Marine Oriented Logistics Equipment (Adv Dev)",
        program="PE 0603804A / Project 526 (Army Watercraft Systems S&T)",
        appropriation=RDTE_APPROP, budget_activity=RDTE_BA, bsa="PE 0603804A",
        mission_family="Fleet modernization / enabling capabilities (watercraft S&T)",
        product_layer="Watercraft S&T: hull/seaworthiness/safety engineering, emergent tech, "
                      "trade studies, Business Case Analyses, AoA support",
        scope_note="The watercraft-specific RDT&E project within PE 0603804A; funds AWS "
                   "engineering to close capability gaps and inform future acquisition.",
    ),
    "RDTE-0603804A": dict(
        title="PE 0603804A - Logistics and Engineer Equipment (Adv Dev) [PE total]",
        program="PE 0603804A (PE rollup)",
        appropriation=RDTE_APPROP, budget_activity=RDTE_BA, bsa="PE 0603804A",
        mission_family="Context (PE rollup)",
        product_layer="PE rollup - includes non-watercraft projects EW8 (Armored Engineer "
                      "Vehicles) and G11 (Adv Elec Energy); not watercraft-addressable on its own",
        scope_note="PE-level total carried for context; the watercraft slice is Project 526.",
    ),
}


def col_roles(Y: int):
    """The 12 (observed_fy, role) columns of a PB-year-Y P-40 Resource Summary."""
    return [
        (None,  "prior_years"),
        (Y - 2, "actual"),
        (Y - 1, "enacted"),
        (Y,     "request_base"),
        (Y,     "request_oco"),
        (Y,     "request_total"),
        (Y + 1, "outyear"),
        (Y + 2, "outyear"),
        (Y + 3, "outyear"),
        (Y + 4, "outyear"),
        (None,  "to_complete"),
        (None,  "total"),
    ]


def parse_cell(tok: str):
    """A Resource-Summary cell -> float | None.  '-'->0.0, 'Continuing'->None."""
    if tok == "-":
        return 0.0
    if tok.lower() == "continuing":
        return None
    return float(tok.replace(",", ""))


def parse_value_row(rest: str):
    """Tokenize the post-label part of a measure row into N_COLS cells, or None."""
    toks = rest.split()
    if len(toks) != N_COLS:
        return None
    try:
        return [parse_cell(t) for t in toks]
    except ValueError:
        return None


def extract_book(fy: int):
    """Yield fact dicts for every (target line item, measure, column) in one book.

    A line item's Resource Summary appears once (on its first P-40 page); the
    owner BLI is the nearest target BLI in the ~10 lines above the 'Resource
    Summary' header. Subsequent same-BLI Resource Summaries (if any) are ignored
    with a warning if their values differ.
    """
    path = TXT / f"FY{fy}" / "procurement" / f"{BOOK_ID}.txt"
    lines = path.read_text(encoding="utf-8").splitlines()
    roles = col_roles(fy)
    seen = {}                       # bli -> {measure: cells}  (first block wins)
    facts = []
    cur_page = None
    cur_exhibit = None              # which Exhibit P-XX the current page is
    for i, ln in enumerate(lines):
        m = PAGE_RE.match(ln)
        if m:
            cur_page = int(m.group(1))
            cur_exhibit = None
            continue
        me = EXHIBIT_RE.search(ln)
        if me:
            cur_exhibit = me.group(1)
        if "Resource Summary" not in ln:
            continue
        # only the P-40 carries the full 12-column profile; the P-5 Cost Analysis
        # has its own 6-column "Resource Summary" (no out-years) - skip it.
        if cur_exhibit != "P-40":
            continue
        # identify owner BLI: nearest target BLI in the preceding ~10 lines
        owner = None
        for j in range(i - 1, max(i - 11, -1), -1):
            mb = BLI_RE.search(lines[j])
            if mb:
                owner = mb.group(1)
                break
        if owner is None:
            continue
        # parse the measure rows that follow this Resource Summary header
        block = {}
        block_page = cur_page
        for k in range(i + 1, min(i + 14, len(lines))):
            row = lines[k]
            if "informational purposes only" in row:
                break
            for label, key, _unit in MEASURES:
                if row.lstrip().startswith(label):
                    cells = parse_value_row(row.lstrip()[len(label):])
                    if cells is None:
                        print(f"  WARN FY{fy} {owner} '{key}': bad token count "
                              f"(page {block_page}) - skipped", file=sys.stderr)
                    else:
                        block[key] = cells
                    break
        if not block:
            continue
        if owner in seen:
            if seen[owner] != block:
                print(f"  WARN FY{fy} {owner}: a second differing Resource Summary "
                      f"at page {block_page} - kept the first", file=sys.stderr)
            continue
        seen[owner] = block
        if owner not in LINE_ITEMS:
            continue
        src_id = f"BUD-OPA34-FY{fy}"
        for label, key, unit in MEASURES:
            cells = block.get(key)
            if cells is None:
                continue
            for (obs_fy, role), val in zip(roles, cells):
                obs_s = ("" if obs_fy is None else obs_fy)
                facts.append(dict(
                    line_item_id=owner, source_book_fy=fy, exhibit="P-40",
                    measure=key, unit=unit,
                    observed_fy=obs_s, column_role=role,
                    amount_type=AMOUNT_TYPE[role],
                    amount=("" if val is None else val),
                    dollars_basis=DOLLARS_BASIS,
                    page=block_page, source_id=src_id,
                    extract_run_id=EXTRACT_RUN_ID,
                    row_hash=row_hash(owner, fy, "P-40", key, role, obs_s),
                ))
    missing = [b for b in LINE_ITEMS if b not in seen]
    if missing:
        print(f"  WARN FY{fy}: no Resource Summary found for {missing}", file=sys.stderr)
    return facts


# ===========================================================================
# Exhibit P-5 "Cost Analysis" - sub-line cost-element breakout (child packages)
# ===========================================================================
# The P-5 decomposes each P-1 line item into cost elements (ESP -> LCU SLEP /
# MCS SLEP / MIBS / HCCC / LSV SLEP / ...). Its cost-element table is 6 column
# groups (Prior Years | FY Y-2 | FY Y-1 | FY Y Base | FY Y OCO | FY Y Total) x
# 3 metrics (Unit Cost $K, Qty Each, Total Cost $M) = 18 numeric tokens per row.
# Numbers are anchored by that 18-token run; element NAMES wrap across 2-3 lines,
# reconstructed by a prefix-accumulate + conditional-suffix heuristic (raw text
# context is kept per row for audit). Subtotal: Flyaway Cost == Net P-1 (checked).
P5_NUMTOK = re.compile(r"^-$|^[\d,]+(?:\.\d+)?$")
P5_SECTIONS = {"Flyaway Cost", "Recurring Cost", "Non Recurring Cost"}
P5_NCOLS = 18
FOOTNOTE_RE = re.compile(r"\(?[†‡*]\)?")


def p5_col_roles(Y: int):
    """The 6 (observed_fy, role) column groups of a PB-year-Y P-5 cost table."""
    return [(None, "prior_years"), (Y - 2, "actual"), (Y - 1, "enacted"),
            (Y, "request_base"), (Y, "request_oco"), (Y, "request_total")]


def trailing_nums(line: str, n: int):
    """If `line` ends in exactly n numeric/dash tokens, return (label, run)."""
    toks = line.split()
    run = []
    for t in reversed(toks):
        if P5_NUMTOK.match(t):
            run.append(t)
        else:
            break
    run.reverse()
    if len(run) != n:
        return None, None
    return " ".join(toks[:len(toks) - n]), run


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _strip_footnote(s: str) -> str:
    return _ws(FOOTNOTE_RE.sub(" ", s))


# single capitalized words that are name tails, not the start of a new element
_CONT_WORDS = {"Support", "Cost", "Equipment", "Spares", "Transportation"}


def _is_continuation(s: str) -> bool:
    """A trailing text line that continues the prior element's name."""
    s = s.strip()
    return bool(s) and (s[0] in "(-" or s[0].islower() or s in _CONT_WORDS)


def _is_boilerplate(s: str) -> bool:
    """Page header/footer noise that must not pollute cost-element names."""
    return ("UNCLASSIFIED" in s or "P-1 Line #" in s or s.startswith("LI ")
            or s.startswith("Volume ") or s.startswith("Date:")
            or (s.startswith("Army") and " Page " in s))


def _p5cell(tok: str, dollar: bool):
    """'-' -> 0.0 for dollar cells, '' for unit-cost/qty cells; else float."""
    if tok == "-":
        return 0.0 if dollar else ""
    return float(tok.replace(",", ""))


def collect_p5_events(fy: int):
    """Per target BLI, the ordered (kind, payload, page) stream of its P-5 table."""
    path = TXT / f"FY{fy}" / "procurement" / f"{BOOK_ID}.txt"
    lines = path.read_text(encoding="utf-8").splitlines()
    seq = {b: [] for b in LINE_ITEMS}
    cur_page = cur_ex = cur_bli = None
    collecting = False
    for ln in lines:
        m = PAGE_RE.match(ln)
        if m:
            cur_page, cur_ex, cur_bli, collecting = int(m.group(1)), None, None, False
            continue
        me = EXHIBIT_RE.search(ln)
        if me:
            cur_ex = me.group(1)
        if "/" in ln:
            mb = BLI_RE.search(ln)
            if mb:
                cur_bli = mb.group(1)
        if cur_ex != "P-5" or cur_bli not in LINE_ITEMS:
            continue
        if "Cost Elements" in ln and "($ K)" in ln:   # start of the element table
            collecting = True
            continue
        if not collecting:
            continue
        if "Remarks:" in ln:
            collecting = False
            continue
        s = ln.strip()
        if not s or _is_boilerplate(s):
            continue
        if s in P5_SECTIONS:
            seq[cur_bli].append(("section", s, cur_page))
            continue
        inline, run = trailing_nums(ln, P5_NCOLS)
        if run is not None:
            seq[cur_bli].append(("data", {"inline": inline, "run": run}, cur_page))
        else:
            seq[cur_bli].append(("text", s, cur_page))
    return seq


def extract_p5(fy: int):
    """Assemble P-5 cost-element rows (one per element x column group) for one book."""
    roles = p5_col_roles(fy)
    src = f"BUD-OPA34-FY{fy}"
    rows = []
    for bli, events in collect_p5_events(fy).items():
        section = None
        prefix = []
        i = 0
        while i < len(events):
            kind, payload, page = events[i]
            if kind == "section":
                section, prefix = payload, []
                i += 1
                continue
            if kind == "text":
                prefix.append(payload)
                i += 1
                continue
            # data row: gather following contiguous text lines, then split name
            inline = _strip_footnote(payload["inline"])
            run = payload["run"]
            j = i + 1
            trailing = []
            while j < len(events) and events[j][0] == "text":
                trailing.append(events[j][1])
                j += 1
            if inline == "":
                consumed = 1 if trailing else 0
            else:
                consumed = 1 if (trailing and _is_continuation(trailing[0])) else 0
            suffix = trailing[0] if consumed else ""
            label = _ws(" ".join(prefix + ([inline] if inline else []) +
                                 ([suffix] if suffix else [])))
            raw = " | ".join(prefix + [payload["inline"]] + trailing[:consumed])
            is_sub = "Y" if (label.startswith("Subtotal")
                             or label.startswith("Gross/Weapon System")) else ""
            for g, (obs, role) in enumerate(roles):
                uc, qty, tc = run[3 * g], run[3 * g + 1], run[3 * g + 2]
                obs_s = ("" if obs is None else obs)
                rows.append([
                    bli, fy, "P-5", section or "", is_sub, label,
                    obs_s, role, AMOUNT_TYPE[role],
                    _p5cell(uc, False), _p5cell(qty, False), _p5cell(tc, True),
                    DOLLARS_BASIS, page, src, EXTRACT_RUN_ID, raw,
                    row_hash(bli, fy, "P-5", section or "", label, role, obs_s),
                ])
            prefix = trailing[consumed:]
            i = j
    return rows


def _dedupe_p5(rows):
    """Collapse P-5 parse artifacts (audit #6). Line item 9552ML5355's Recurring-Cost
    subtotal block is emitted TWICE (an interleaved phantom), so the same identity
    (row_hash = bli/fy/section/label/role/obs) appears with a real value and a 0.0 twin.
    Three-step, faithful, never-silent cleanup:
      1. drop exact whole-row duplicates;
      2. for a same-row_hash group, fold a 0.0 'phantom' into its single non-zero twin;
      3. where two DISTINCT non-zero values share an identity (a genuine parse ambiguity,
         e.g. prior_years 192.784 vs 10.131), keep BOTH with a collision-safe row_hash
         suffix and LOG it - never silently pick one.
    Asserts row_hash is unique afterwards."""
    H, TC, LI, FY_, EL, ROLE = 17, 11, 0, 1, 5, 7

    def fnum(s):
        if isinstance(s, (int, float)):
            return float(s)
        try:
            return float((s or "").strip() or 0)
        except (TypeError, ValueError):
            return 0.0

    seen, deduped, n_exact = set(), [], 0
    for r in rows:                                   # 1) exact whole-row duplicates
        t = tuple(r)
        if t in seen:
            n_exact += 1
            continue
        seen.add(t)
        deduped.append(r)

    groups = {}
    for r in deduped:
        groups.setdefault(r[H], []).append(r)
    out, n_phantom, ambiguous = [], 0, []
    for grp in groups.values():
        if len(grp) == 1:
            out.append(grp[0])
            continue
        nonzero = [r for r in grp if fnum(r[TC]) != 0]
        if len({fnum(r[TC]) for r in nonzero}) <= 1:  # 2) one real value (+ 0.0 phantoms)
            out.append(nonzero[0] if nonzero else grp[0])
            n_phantom += len(grp) - 1
        else:                                         # 3) genuine collision -> keep all + flag
            for i, r in enumerate(sorted(grp, key=lambda x: -abs(fnum(x[TC])))):
                rr = list(r)
                if i:
                    rr[H] = f"{r[H]}-{i + 1}"
                out.append(rr)
            g = grp[0]
            ambiguous.append((g[LI], g[FY_], g[EL], g[ROLE],
                              sorted({fnum(r[TC]) for r in nonzero}, reverse=True)))

    print(f"  P-5 dedup: dropped {n_exact} exact-duplicate + {n_phantom} zero-phantom row(s)")
    if ambiguous:
        print(f"  P-5 WARNING: {len(ambiguous)} genuine value-collision(s) kept with a "
              "collision-safe row_hash suffix (parse ambiguity - review the source PDF):")
        for li, fy, el, role, vals in ambiguous:
            print(f"    {li} FY{fy} {el} [{role}]: {vals}")
    hh = [r[H] for r in out]
    assert len(hh) == len(set(hh)), "P-5 row_hash not unique after dedup"
    return out


def build_p5_cost_elements():
    rows = []
    for fy in FYS:
        rows.extend(extract_p5(fy))
    rows = _dedupe_p5(rows)
    header = ["line_item_id", "source_book_fy", "exhibit", "section", "is_subtotal",
              "cost_element", "observed_fy", "column_role", "amount_type", "unit_cost_k",
              "qty_each", "total_cost_m", "dollars_basis", "page", "source_id",
              "extract_run_id", "raw_context", "row_hash"]
    write_csv("budget_p5_cost_elements.csv", header, rows)
    return rows


def tie_out_p5(p5rows, facts):
    """P-5 'Gross/Weapon System Cost' (the grand total) must == P-40 Net P-1.

    Gross = Flyaway + any non-Flyaway categories (e.g. MSV's Support/Training), so
    the grand-total row is the universal anchor; Flyaway alone ties only when there
    are no support categories (as on the ESP line).
    """
    net = {(f["line_item_id"], f["source_book_fy"]): f["amount"] for f in facts
           if f["measure"] == "net_procurement_p1" and f["column_role"] == "request_total"}
    gross = {}
    for r in p5rows:
        bli, fy, _ex, _sec, _sub, label, _obs, role = r[:8]
        if role == "request_total" and label.startswith("Gross/Weapon System"):
            gross[(bli, fy)] = r[11]   # total_cost_m (idx +1 after amount_type col)
    # a $0 net-procurement year has no P-5 cost analysis to reconcile against
    checkable = {k: v for k, v in net.items() if v and v > 0}
    print("\nP-5 tie-out - Gross/Weapon System Cost vs P-40 Net P-1 (request_total, $M):")
    bad = 0
    for (bli, fy), v in sorted(checkable.items()):
        g = gross.get((bli, fy))
        if g is None or abs(g - v) >= 0.05:
            bad += 1
            print(f"  MISMATCH {bli} FY{fy}: P-40 Net P-1={v}  P-5 Gross={g}")
    print(f"  {len(checkable) - bad}/{len(checkable)} funded line-item-books reconcile "
          f"within $0.05M ({len(net) - len(checkable)} zero-funding years have no P-5).")


# ===========================================================================
# Exhibit R-2 / R-2A - RDT&E watercraft program element (same 12-col grammar)
# ===========================================================================
def trailing_cells(line: str, n: int):
    """Last n numeric/'-'/'Continuing' cells of a line, or None if fewer than n."""
    toks = line.split()
    run = []
    for t in reversed(toks):
        if CELL_RE.match(t):
            run.append(t)
        else:
            break
    run.reverse()
    return run[-n:] if len(run) >= n else None


def extract_rdte(fy: int):
    """PE 0603804A 'Total Program Element' (R-2) + Project 526 (R-2A) for one year."""
    book = RDTE_BOOK[fy]
    path = TXT / f"FY{fy}" / "rdte" / f"{book}.txt"
    lines = path.read_text(encoding="utf-8").splitlines()
    roles = col_roles(fy)
    src = f"BUD-{book}-FY{fy}"
    facts = []
    cur_page = cur_pe = cur_ex = None
    got_pe = got_proj = False

    def emit(line_item, exhibit, cells, page):
        for (obs, role), tok in zip(roles, cells):
            val = parse_cell(tok)
            obs_s = ("" if obs is None else obs)
            facts.append(dict(
                line_item_id=line_item, source_book_fy=fy, exhibit=exhibit,
                measure="rdte_cost", unit="USD_millions",
                observed_fy=obs_s, column_role=role,
                amount_type=AMOUNT_TYPE[role],
                amount=("" if val is None else val),
                dollars_basis=DOLLARS_BASIS, page=page, source_id=src,
                extract_run_id=EXTRACT_RUN_ID,
                row_hash=row_hash(line_item, fy, exhibit, "rdte_cost", role, obs_s)))

    for ln in lines:
        m = PAGE_RE.match(ln)
        if m:
            cur_page = int(m.group(1))
            continue
        me = EXHIBIT_RE.search(ln)
        if me:
            cur_ex = me.group(1)
        mp = PE_RE.search(ln)
        if mp:
            cur_pe = mp.group(1)
        if cur_pe != RDTE_PE or cur_ex not in ("R-2", "R-2A"):
            continue
        if not got_pe and ln.lstrip().startswith("Total Program Element"):
            cells = trailing_cells(ln, N_COLS)
            if cells:
                emit("RDTE-0603804A", "R-2", cells, cur_page)
                got_pe = True
        elif not got_proj and re.match(rf"\s*{RDTE_PROJECT}:\s", ln):
            cells = trailing_cells(ln, N_COLS)
            if cells:
                emit("RDTE-0603804A-526", "R-2A", cells, cur_page)
                got_proj = True
    if not (got_pe and got_proj):
        print(f"  WARN FY{fy} {book}: PE total found={got_pe} project526 found={got_proj}",
              file=sys.stderr)
    return facts


# ===========================================================================
# Exhibit OP-5 - O&M watercraft sustainment (NOTES, not a funding profile)
# ===========================================================================
# O&M has NO discrete watercraft line item. Watercraft sustainment lives inside
# OP-5 Subactivity Groups (chiefly BA01/AG11/SAG 113 Echelons Above Brigade for
# the Composite Watercraft Company stand-up, plus depot maintenance / reset /
# strategic-mobility / mariner-training SAGs where watercraft is one of many
# systems). The only watercraft-attributable dollars are bundled program-change
# items (e.g. FY27's $10.5M CSS Force Structure increase = Composite Watercraft
# Company + 3 EOD detachments). So this captures watercraft-relevant O&M program
# items as cited EVIDENCE - SAG context, the (bundled) amount, the narrative, and
# the page - with a relevance flag; it is not summed and not a funding time series.
OMA_BOOK = "OMA_Vol1_Operating_Forces"
OMA_FYS = [2025, 2026, 2027]
OMA_KW = re.compile(r"watercraft|army mariner|landing craft|tugboat|\bLCU\b|\bLSV\b|\bLCM\b", re.I)
OMA_DIRECT = re.compile(r"composite watercraft|army mariner|watercraft compan|"
                        r"watercraft system|watercraft sustain", re.I)
OMA_ITEM = re.compile(r"^\s*(\d+)\)\s+(.*?)\s*\.{3,}\s*\$([\d,]+)\s*$")
OMA_BA = re.compile(r"Budget Activity\s+(\d+):\s*(.+?)\s*$")
OMA_AG = re.compile(r"Activity Group\s+(\d+):\s*(.+?)\s*$")
OMA_SAG = re.compile(r"Detail by Subactivity Group\s+(\w+):\s*(.+?)\s*$")


def extract_oma(fy: int):
    """Watercraft-relevant O&M program items in OMA Vol 1 -> note rows."""
    path = TXT / f"FY{fy}" / "om" / f"{OMA_BOOK}.txt"
    lines = path.read_text(encoding="utf-8").splitlines()
    src = f"BUD-OMA1-FY{fy}"
    page = ba = ag = sag_c = sag_n = None
    item = None                    # (title, amount_k, page, idx)
    rows = []
    captured = set()
    for i, ln in enumerate(lines):
        m = PAGE_RE.match(ln)
        if m:
            page = int(m.group(1))
            continue
        mb = OMA_BA.search(ln)
        if mb:
            ba = f"{mb.group(1)} {mb.group(2)}"
        mg = OMA_AG.search(ln)
        if mg:
            ag = f"{mg.group(1)} {mg.group(2)}"
        ms = OMA_SAG.search(ln)
        if ms:
            sag_c, sag_n = ms.group(1), ms.group(2)
        mi = OMA_ITEM.match(ln)
        if mi:
            item = (_ws(mi.group(2)), int(mi.group(3).replace(",", "")), page, i, sag_c, sag_n, ba, ag)
        if OMA_KW.search(ln) and item and item[3] not in captured and 0 < i - item[3] <= 7:
            captured.add(item[3])
            narrative = _ws(ln)[:300]
            rows.append([
                src, fy, item[6] or "", item[7] or "", item[4] or "", item[5] or "",
                "program_change", item[0], item[1],
                "direct" if OMA_DIRECT.search(ln) else "lists-watercraft",
                "N",                       # amount is bundled, not watercraft-discrete
                narrative, item[2],
                EXTRACT_RUN_ID, row_hash(src, item[4] or "", item[0], item[2]),
            ])
    return rows


def build_oma_notes():
    rows = []
    for fy in OMA_FYS:
        rows.extend(extract_oma(fy))
    header = ["source_id", "source_book_fy", "budget_activity", "activity_group",
              "sag_code", "sag_name", "item_type", "item_title", "amount_k",
              "watercraft_relevance", "amount_is_watercraft_discrete", "narrative", "page",
              "extract_run_id", "row_hash"]
    write_csv("budget_oma_watercraft_notes.csv", header, rows)
    return rows


def write_csv(name, header, rows):
    path = OUT / name
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote {name:28s} {len(rows):4d} rows")
    return path


# book_id -> (source_id prefix, appropriation, exhibits, title template) for cited books
CITED_BOOKS = {
    BOOK_ID: ("OPA34", APPROPRIATION, "P-40 / P-5 (incl. P-1 index, P-21)",
              "Other Procurement, Army - BA 3&4 (Other Support Equipment & Spares), PB {fy}"),
    "RDTE_BA4": ("RDTE_BA4", RDTE_APPROP, "R-2 / R-2A",
                 "RDT&E, Army - Budget Activity 4 (ACD&P), PB {fy}"),
    "RDTE_BA4A": ("RDTE_BA4A", RDTE_APPROP, "R-2 / R-2A",
                  "RDT&E, Army - Budget Activity 4A (ACD&P), PB {fy}"),
    OMA_BOOK: ("OMA1", "2020 O&M, Army", "OP-5",
               "Operation and Maintenance, Army - Volume 1 (Operating Forces), PB {fy}"),
}
# (book_id, fy) pairs actually mined: OPA34 all years; PE 0603804A is in BA4
# (FY22-23) then BA4A (FY24-27); OMA Vol 1 in FY25-27.
CITED_FY = ({(BOOK_ID, fy) for fy in FYS}
            | {("RDTE_BA4", fy) for fy in (2022, 2023)}
            | {("RDTE_BA4A", fy) for fy in (2024, 2025, 2026, 2027)}
            | {(OMA_BOOK, fy) for fy in OMA_FYS})


def build_source_log():
    """Every cited justification book -> source_log.csv (workbook 11_Source_Log).

    Only books actually mined for facts are listed (the RDT&E BA4/BA4A volumes
    that carry PE 0603804A: BA4 in FY22-23, BA4A in FY24-27)."""
    rows = []
    with MANIFEST.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            bid = r["book_id"]
            if bid not in CITED_BOOKS:
                continue
            fy = int(r["fy"])
            if (bid, fy) not in CITED_FY:
                continue
            prefix, approp, exhibits, title_t = CITED_BOOKS[bid]
            rows.append([
                f"BUD-{prefix}-FY{fy}", title_t.format(fy=fy), bid, fy, approp, exhibits,
                r.get("source_url", ""), r.get("sha256_16", ""), r.get("pages", ""),
                r.get("rel_path", ""), r.get("txt_path", ""), ACCESS_DATE,
            ])
    rows.sort(key=lambda x: (x[4], x[3]))
    return write_csv("source_log.csv",
                     ["source_id", "title", "book_id", "fy", "appropriation",
                      "exhibits", "url", "sha256_16", "pdf_pages", "pdf_path",
                      "txt_path", "access_date"], rows)


def build_line_items():
    rows = []
    for bli, d in LINE_ITEMS.items():       # OPA procurement (shared approp/BA/BSA)
        rows.append([
            bli, d["title"], d["program"], APPROPRIATION, BUDGET_ACTIVITY, BSA,
            d["mission_family"], d["product_layer"], "seed", d["scope_note"],
        ])
    for pid, d in RDTE_LINE_ITEMS.items():  # RDT&E (per-item approp/BA/BSA)
        rows.append([
            pid, d["title"], d["program"], d["appropriation"], d["budget_activity"],
            d["bsa"], d["mission_family"], d["product_layer"], "seed", d["scope_note"],
        ])
    return write_csv("budget_line_items.csv",
                     ["line_item_id", "title", "program", "appropriation",
                      "budget_activity", "bsa", "mission_family", "product_layer",
                      "tag_confidence", "scope_note"], rows)


def build_funding_facts():
    facts = []
    for fy in FYS:
        facts.extend(extract_book(fy))       # P-40 procurement
        facts.extend(extract_rdte(fy))       # R-2/R-2A watercraft RDT&E
    header = ["line_item_id", "source_book_fy", "exhibit", "measure", "unit",
              "observed_fy", "column_role", "amount_type", "amount", "dollars_basis",
              "page", "source_id", "extract_run_id", "row_hash"]
    rows = [[f[h] for h in header] for f in facts]
    write_csv("budget_funding_facts.csv", header, rows)
    return facts


def tie_out(facts):
    """Print the budget-year request_total (net P-1) per book x line item."""
    print("\nTie-out - Net Procurement (P-1) request_total, $M (hand-check vs txt):")
    print(f"  {'line item':<34s}" + "".join(f"FY{fy:>6d}" for fy in FYS))
    idx = {}
    for f in facts:
        if f["measure"] == "net_procurement_p1" and f["column_role"] == "request_total":
            idx[(f["line_item_id"], f["source_book_fy"])] = f["amount"]
    for bli, d in LINE_ITEMS.items():
        cells = "".join(f"{idx.get((bli, fy), '-'):>8}" for fy in FYS)
        print(f"  {d['title'][:33]:<34s}{cells}")


def tie_out_rdte(facts):
    """Print the RDT&E watercraft Project 526 request_total per year."""
    idx = {}
    for f in facts:
        if (f["line_item_id"] == "RDTE-0603804A-526" and f["measure"] == "rdte_cost"
                and f["column_role"] == "request_total"):
            idx[f["source_book_fy"]] = f["amount"]
    print("\nRDT&E tie-out - Project 526 (Marine Oriented Logistics) request_total $M:")
    print("  " + "".join(f"PB{str(fy)[2:]:>8}" for fy in FYS))
    print("  " + "".join(f"{idx.get(fy, '-'):>10}" for fy in FYS))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Extracting OPA BA3&4 + RDT&E watercraft cuts -> {OUT}")
    build_line_items()
    facts = build_funding_facts()
    p5rows = build_p5_cost_elements()
    oma = build_oma_notes()
    build_source_log()
    tie_out(facts)
    tie_out_p5(p5rows, facts)
    tie_out_rdte(facts)
    n_items = len(LINE_ITEMS) + len(RDTE_LINE_ITEMS)
    print(f"\nDONE  {len(facts)} funding facts (P-40 + R-2/R-2A) + {len(p5rows)} P-5 "
          f"cost-element rows + {len(oma)} O&M notes across {len(FYS)} years x "
          f"{n_items} line items.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
