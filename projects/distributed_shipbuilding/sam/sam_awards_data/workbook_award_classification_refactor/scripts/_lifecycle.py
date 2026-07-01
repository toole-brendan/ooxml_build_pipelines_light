"""_lifecycle - the DDG construction-lifecycle rule, defined ONCE (shared Python source).

The date counterpart to _hull_logic.py. _hull_logic answers WHICH HULL (the A/B/C/D/X family
attribution); this module answers WHICH STAGE a subaward supported and, for the family-level
C/D rows, NARROWS the candidate hull set to the hulls physically in build on the purchase date.
It is pure Python (no live-formula mirror) because the stage is a date-window comparison across a
hull->schedule join that an Excel formula cannot do cleanly - so the stage is MATERIALIZED onto the
transaction sheet by tag_ddg_transactions_lifecycle.py and the C/D candidate / rollup spines are
emitted by build_ddg_cd_lifecycle.py. Both import this module, so the per-row tx columns and the
expanded candidate grain are consistent by construction (the partition integrity check diffs them).

Milestone dates live on the curated DDG Hull Master (extracted/ddg_hull_master.csv): Start
Fabrication / Launch / Delivery + a per-hull Schedule Confidence (Actual / Projected / Estimated).
We have no keel/launch for every hull, so the four stages collapse gracefully: a hull not yet
launched carries no Outfit window and its in-build spend reads as Construction (launch pending).

The wall (briefing §6): narrowing the candidate hulls by build timing is ATTRIBUTION (evidence);
splitting a family dollar across hulls by a formula is ALLOCATION (modeling) and is NOT done here.
This module only narrows the candidate SET and stage-tags it - it never assigns a single C/D hull.
"""
from __future__ import annotations

import csv
import re
from datetime import date

from _paths import EXTRACTED  # noqa: E402

HULL_MASTER_CSV = EXTRACTED / "ddg_hull_master.csv"

# Milestone columns on the Hull Master (curated; "Mon YYYY" text or blank).
COL_START = "Start Fabrication"
COL_LAUNCH = "Launch"
COL_DELIVERY = "Delivery"
COL_CONF = "Schedule Confidence"

# --- stage labels (also the SUMIFS criteria on DDG Hull x Lifecycle Stage; keep EXACT) ---
STAGE_LONGLEAD = "Long-lead"            # purchase before start of fabrication (pre-fab material)
STAGE_CONSTRUCTION = "Construction"     # start fabrication -> launch (or -> delivery if not launched)
STAGE_OUTFIT = "Outfit / test"          # launch -> delivery (post-launch outfitting / activation)
STAGE_POSTDELIVERY = "Post-delivery"    # after delivery to the Navy (outside core build)
STAGE_NODATA = "No schedule data"       # this hull carries no milestone dates

# The active-build stages (the strongest timing signal - distinct from the long-lead confounder, which
# is a real but weaker match). Used to grade a single-candidate narrowing High vs Medium.
ACTIVE_STAGES = frozenset({STAGE_CONSTRUCTION, STAGE_OUTFIT})

# --- narrowing-result buckets (also the SUMIFS criteria on DDG C-D Lifecycle Coverage; keep EXACT) ---
NR_SINGLE = "Single candidate"
NR_FEW = "2-3 candidates"
NR_FAMILY = "Still family-level"
NR_EXCEPTION = "Exception (no window match)"
NR_NODATA = "No schedule data"

# --- lifecycle confidence (its OWN axis, separate from the A/B/C/D/X hull confidence) ---
LC_HIGH = "High"
LC_MEDIUM = "Medium"
LC_LOW = "Low"
LC_FLAGGED = "Flagged"

# A purchase more than this many months BEFORE a hull's start of fabrication is too early to be that
# hull's long-lead material (advance procurement runs ~1-3 yr ahead); it is Pre-program, not a match.
LONGLEAD_MAX_MONTHS = 48

_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}


def parse_month_year(s: str):
    """'Sep 2017' -> date(2017, 9, 1); blank / unparseable -> None. Month name case-insensitive."""
    s = (s or "").strip()
    if not s:
        return None
    m = re.match(r"([A-Za-z]{3,})\.?\s+(\d{4})$", s)
    if not m:
        return None
    mon = _MONTHS.get(m.group(1)[:3].lower())
    return date(int(m.group(2)), mon, 1) if mon else None


def parse_iso(s: str):
    """'2017-09-23' -> date(2017, 9, 23); blank / unparseable -> None (the subaward action date)."""
    s = (s or "").strip()[:10]
    if not s:
        return None
    try:
        y, m, d = (int(x) for x in s.split("-"))
        return date(y, m, d)
    except (ValueError, TypeError):
        return None


def _months_between(a: date, b: date) -> int:
    """Whole-month gap b - a (b later => positive)."""
    return (b.year - a.year) * 12 + (b.month - a.month)


def _hull_num(s: str) -> int:
    return int("".join(ch for ch in str(s) if ch.isdigit()) or 0)


class Window:
    """One hull's build schedule: start fabrication / launch / delivery + curated confidence."""

    __slots__ = ("hull", "start_fab", "launch", "delivery", "conf", "builder")

    def __init__(self, hull, start_fab, launch, delivery, conf, builder):
        self.hull = hull
        self.start_fab = start_fab
        self.launch = launch
        self.delivery = delivery
        self.conf = conf or ""
        self.builder = builder or ""

    @property
    def has_dates(self) -> bool:
        """A usable window needs at least a start-fabrication or a delivery boundary."""
        return self.start_fab is not None or self.delivery is not None


def load_milestones(csv_path=HULL_MASTER_CSV) -> dict[int, Window]:
    """{hull number -> Window} from the curated Hull Master. Hulls with no dates still get a Window
    (has_dates False) so the caller can report 'No schedule data' rather than silently dropping them."""
    out: dict[int, Window] = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            n = _hull_num(r.get("Hull", ""))
            if not n:
                continue
            out[n] = Window(
                hull=n,
                start_fab=parse_month_year(r.get(COL_START, "")),
                launch=parse_month_year(r.get(COL_LAUNCH, "")),
                delivery=parse_month_year(r.get(COL_DELIVERY, "")),
                conf=(r.get(COL_CONF, "") or "").strip(),
                builder=(r.get("Builder", "") or "").strip(),
            )
    return out


def _date_conf(win: Window) -> str:
    """The hull's curated Schedule Confidence, normalized to the Date Source Confidence vocabulary
    (Actual / Projected / Estimated). Blank -> 'Estimated' (treat unknown provenance conservatively)."""
    c = (win.conf or "").strip().title()
    return c if c in ("Actual", "Projected", "Estimated") else "Estimated"


def stage_for(d: date, win: Window) -> tuple[str, bool, str]:
    """(stage, window_match, date_conf) for purchase date `d` against one hull's `win`.

    Four real stages, collapsing gracefully when launch is unknown:
      - before start fabrication            -> Long-lead     (match, unless > 48 mo early -> no match)
      - start fabrication .. launch          -> Construction  (match)
      - launch .. delivery                   -> Outfit / test (match)
      - (launch unknown) start .. delivery   -> Construction  (match)  [no Outfit split yet]
      - after delivery                       -> Post-delivery (no match)
    A hull with no dates is 'No schedule data' (no match). The STAGE is the natural lifecycle phase -
    a KNOWN hull's early purchase is simply its Long-lead, however far ahead. window_match (used ONLY by
    C/D narrowing) goes False for post-delivery / no-data / implausibly-early, so those hulls drop out of
    a family's candidate set. date_conf is the hull's curated provenance (Actual / Projected / Estimated).
    """
    if d is None or not win.has_dates:
        return STAGE_NODATA, False, ""
    dc = _date_conf(win)
    sf, ln, dl = win.start_fab, win.launch, win.delivery

    # before start of fabrication: this hull's long-lead phase. STAGE is always Long-lead; the MATCH
    # flag (narrowing only) goes False when the purchase is implausibly early for THIS hull, so an early
    # buy narrows AWAY the latest family hulls that had not begun procuring yet.
    if sf is not None and d < sf:
        return STAGE_LONGLEAD, _months_between(d, sf) <= LONGLEAD_MAX_MONTHS, dc

    # after delivery: outside the core build (never a narrowing match)
    if dl is not None and d > dl:
        return STAGE_POSTDELIVERY, False, dc

    # between start and delivery: active build. With a launch date, split construction vs outfit/test;
    # without one (not yet launched / not curated), in-build spend reads as Construction.
    if ln is not None and sf is not None:
        return (STAGE_CONSTRUCTION if d < ln else STAGE_OUTFIT), True, dc
    return STAGE_CONSTRUCTION, True, dc


def reason_for(hull: int, stage: str, match: bool, d: date, win: Window) -> str:
    """A short, human reason why a candidate hull is in/out for `d` (the Candidates-sheet 'Reason')."""
    ds = d.strftime("%b %Y") if d else "no date"
    if stage == STAGE_NODATA:
        return f"No schedule dates for DDG {hull}"
    if stage == STAGE_LONGLEAD:
        if match:
            return f"{ds} in DDG {hull} long-lead window (before fabrication start)"
        return f"{ds} too early for DDG {hull} (> {LONGLEAD_MAX_MONTHS} mo before fab start) - excluded"
    if stage == STAGE_CONSTRUCTION:
        return f"{ds} within DDG {hull} construction window"
    if stage == STAGE_OUTFIT:
        return f"{ds} within DDG {hull} outfit / test window (post-launch)"
    if stage == STAGE_POSTDELIVERY:
        return f"{ds} after DDG {hull} delivery - outside core build"
    return f"{ds} vs DDG {hull}"


class Narrowing:
    """The timing analysis of one C/D transaction across its full PIID-family candidate set.

    candidates : [(hull, stage, match, date_conf, reason)] for EVERY family hull (matches + exclusions,
                 so the Candidates sheet shows why each was kept or dropped).
    timing_hulls / count : the family hulls whose window matched the purchase date (the narrowed set).
    stages / consensus    : the distinct matched stages, and whether they all agree.
    narrowing_result      : one of the NR_* buckets (Single / 2-3 / Still family-level / Exception / No data).
    lifecycle_confidence  : one of the LC_* grades (its own axis; never upgrades the C/D hull grade).
    date_conf             : Projected if any matched hull's dates are projected/estimated, else Actual.
    """

    __slots__ = ("candidates", "timing_hulls", "count", "stages", "consensus",
                 "narrowing_result", "lifecycle_confidence", "date_conf", "had_data")

    def __init__(self, candidates):
        self.candidates = candidates
        matched = [(h, st, dc) for (h, st, m, dc, _r) in candidates if m]
        self.timing_hulls = [h for h, _st, _dc in matched]
        self.count = len(matched)
        self.stages = sorted({st for _h, st, _dc in matched})
        self.consensus = len(self.stages) == 1
        self.had_data = any(st != STAGE_NODATA for (_h, st, _m, _dc, _r) in candidates)

        confs = {dc for _h, _st, dc in matched if dc}
        if confs & {"Projected", "Estimated"}:
            self.date_conf = "Projected"
        elif confs:
            self.date_conf = "Actual"
        else:
            self.date_conf = ""

        self.narrowing_result, self.lifecycle_confidence = self._verdict()

    def _verdict(self) -> tuple[str, str]:
        if not self.had_data:
            return NR_NODATA, LC_FLAGGED
        if self.count == 0:
            return NR_EXCEPTION, LC_FLAGGED
        if self.count == 1:
            active = self.stages and self.stages[0] in ACTIVE_STAGES
            if active and self.date_conf == "Actual":
                return NR_SINGLE, LC_HIGH
            return NR_SINGLE, LC_MEDIUM          # single but long-lead, or on projected dates
        if self.count <= 3:
            return NR_FEW, LC_MEDIUM
        return NR_FAMILY, LC_LOW                 # >=4: timing barely narrows


def narrow(family: set[int], d: date, milestones: dict[int, Window]) -> Narrowing:
    """Run the timing analysis for a C/D transaction: expand across the full candidate family,
    stage-tag each hull on the purchase date, and grade the resulting narrowed set."""
    cands = []
    for h in sorted(family):
        win = milestones.get(h)
        if win is None:
            cands.append((h, STAGE_NODATA, False, "", f"No schedule dates for DDG {h}"))
            continue
        stage, match, dc = stage_for(d, win)
        cands.append((h, stage, match, dc, reason_for(h, stage, match, d, win)))
    return Narrowing(cands)


def hull_str(hulls) -> str:
    """Canonical ' / '-joined 'DDG NNN' for a hull iterable (sorted) - matches _hull_logic.hull_str."""
    return " / ".join(f"DDG {n}" for n in sorted(hulls))
