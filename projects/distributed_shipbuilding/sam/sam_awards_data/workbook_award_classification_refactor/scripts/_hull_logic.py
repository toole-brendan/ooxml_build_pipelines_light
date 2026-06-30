"""_hull_logic - the DDG hull-attribution rule, defined ONCE (shared Python source).

The hull family + direct-text regex + conflict-aware assignment used by the offline scripts:
tag_ddg_transactions_hulls.py (materializes the regex columns + writes the exception log) and
build_ddg_vendor_hull.py (enumerates the vendor x hull and vendor x hull x SWBS spines). The
SAME rule is ALSO expressed as live Excel formulas on the DDG Subaward Transactions sheet
(sheets/_hulls.py) so edits to the curated PIID->Hull map flow through the workbook; this module
is the Python counterpart for the build-time artifacts that cannot be a live formula (the regex
evidence, the exception log, the generated spines). The two implementations must stay in lockstep -
the recalc QA in the build verification diffs the live Assigned Hull against this module's resolve().

Canonical hull form is "DDG NNN" everywhere.
"""
from __future__ import annotations

import csv
import re

from _paths import EXTRACTED  # noqa: E402

MAP_CSV = EXTRACTED / "ddg_piid_hull_map.csv"

# DDG hull numbers in the Flight IIA/III window (so "DDG-51 class" / "DDG 1000" are never hulls).
HULL_LO, HULL_HI = 100, 160

# A DDG hull token: "DDG 128", "DDG-128", "DDG128", "DDGs 128".
_DDG_TOKEN = re.compile(r"\bDDGs?[\s\-]?(\d{3})\b", re.I)
# A DDG token immediately followed by a shorthand list of more 3-digit hulls: "DDG 128/129",
# "DDG 128, 129 and 131", "DDG 128 & 129". (No numeric-range expansion - "DDG 117-125" does not
# occur in the corpus and range semantics are builder-sequence-dependent.)
_DDG_LIST = re.compile(r"\bDDGs?[\s\-]?(\d{3}(?:\s*(?:/|,|&|and)\s*\d{3})+)\b", re.I)


def _valid(n: int) -> bool:
    return HULL_LO <= n <= HULL_HI


def parse_hulls(*texts: str) -> set[int]:
    """The set of valid DDG hull numbers named across `texts` (single tokens + shorthand lists)."""
    found: set[int] = set()
    for t in texts:
        t = t or ""
        for m in _DDG_TOKEN.finditer(t):
            n = int(m.group(1))
            if _valid(n):
                found.add(n)
        for m in _DDG_LIST.finditer(t):
            for x in re.findall(r"\d{3}", m.group(1)):
                n = int(x)
                if _valid(n):
                    found.add(n)
    return found


def hull_str(hulls) -> str:
    """Canonical " / "-joined "DDG NNN" string for a hull set (sorted)."""
    return " / ".join(f"DDG {n}" for n in sorted(hulls))


def hull_set(text: str) -> set[int]:
    """The hull numbers in an already-materialized "DDG NNN / ..." string (e.g. Direct Hull Text),
    so a consumer of the regex columns reconstructs the set without re-running the full parser."""
    return {int(x) for x in re.findall(r"DDG\s*(\d{3})", text or "") if _valid(int(x))}


def load_map() -> dict[str, dict]:
    """{Prime PIID -> {family:set[int], kind:str, candidates:str}} from the curated PIID map."""
    out: dict[str, dict] = {}
    with MAP_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            piid = (r.get("Prime PIID") or "").strip()
            if not piid:
                continue
            cand = (r.get("Candidate Hulls") or "").strip()
            fam = {int(x) for x in re.findall(r"DDG\s*(\d{3})", cand) if _valid(int(x))}
            out[piid] = {"family": fam, "kind": (r.get("Exact or Family") or "").strip(),
                         "candidates": cand}
    return out


def resolve(piid: str, direct: set[int], req: set[int], fam_info: dict):
    """(assigned, scope, basis, confidence) for one row, conflict-aware.

    A is an official single-ship exact; B an in-family single direct hull; C a hull seen only in
    the prime requirement text; D PIID-family-only; X a conflict (out-of-family direct hull) or a
    multi-hull row. `Assigned Hull` is non-blank ONLY for A and B. This is the canonical rule; the
    Excel formulas in sheets/_hulls.py reproduce it cell-for-cell."""
    info = fam_info.get(piid)
    if info is None:
        return "", "Unassigned", "Unassigned", ""
    family, kind = info["family"], info["kind"]
    dcount = len(direct)

    if kind == "single-ship":
        ship = next(iter(family))
        if dcount >= 1 and ship not in direct:        # text names a DIFFERENT hull -> conflict
            return "", "Conflict", "Out-of-family direct text", "X"
        return f"DDG {ship}", "Exact hull", "Single-ship PIID", "A"

    # multi-hull / option-ship family
    if dcount == 1:
        h = next(iter(direct))
        if h in family:
            return f"DDG {h}", "Exact hull", "Subaward text", "B"
        return "", "Conflict", "Out-of-family direct text", "X"
    if dcount > 1:
        return "", "Multi-hull", "Multiple hulls in subaward text", "X"
    if req:                                            # hull only in the prime requirement text
        return "", "PIID family", "Prime requirement text", "C"
    return "", "PIID family", "PIID family", "D"
