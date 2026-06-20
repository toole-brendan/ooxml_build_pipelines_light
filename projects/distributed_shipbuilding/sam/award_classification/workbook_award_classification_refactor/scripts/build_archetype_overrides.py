"""build_archetype_overrides - emit the Vendor Archetype Overrides leaf table.

One row per researched subawardee UEI x program carrying the hand-assigned Capability
Domain (D) and Primary Output (P) - the overrides that take precedence over the NAICS-6
crosswalk default on the program-vendor sheets. This pulls the SAME D/P codes + evidence
that build_program_vendors used to fold inline into each program-vendor CSV, but lifts
them into one standalone (Program, UEI) table so the program-vendor D/P cells can become
override-first formulas instead of hardcoded leaves.

Source: extracted/<program>_archetype_results.csv (the research pulls). A UEI is kept
only if it is also present in extracted/<program>_program_vendors.csv (i.e. the override
actually applies to a vendor on that program). The per-axis evidence note is composed the
way build_program_vendors originally folded it onto the Basis cells (reasoning, blank
line, then the source URLs one per line) so the hover Notes are byte-identical to before.

Output: extracted/vendor_archetype_overrides.csv
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

EXTRACTED = Path(__file__).resolve().parent.parent / "extracted"
PROGRAMS = [("ddg", "DDG"), ("virginia", "Virginia"), ("columbia", "Columbia")]

OUT_HEADERS = ["Program", "Subawardee UEI", "Capability Domain (D)",
               "Primary Output (P)", "Capability Domain Note", "Primary Output Note"]


def fmt_note(reasoning: str, urls: str) -> str:
    """One Basis hover Note: free-text reasoning, a blank line, then source URLs one per
    line. Mirrors the original build_program_vendors Basis-note composition exactly."""
    reasoning = (reasoning or "").strip()
    raw = (urls or "").strip()
    found = [u.rstrip(".,);") for u in re.findall(r"https?://[^\s|;,]+", raw)]
    url_block = "\n".join(found) if found else raw
    return "\n\n".join(p for p in (reasoning, url_block) if p)


def _members(program: str) -> set[str]:
    """The set of subawardee UEIs that appear on this program's vendor sheet."""
    path = EXTRACTED / f"{program}_program_vendors.csv"
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return {(r.get("Subawardee UEI") or "").strip()
                for r in csv.DictReader(fh)} - {""}


def build() -> None:
    rows: list[list[str]] = []
    for program, label in PROGRAMS:
        members = _members(program)
        path = EXTRACTED / f"{program}_archetype_results.csv"
        with path.open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                uei = (r.get("Subawardee UEI") or "").strip()
                d = (r.get("Capability Domain (D)") or "").strip()
                p = (r.get("Primary Output (P)") or "").strip()
                if not uei or uei not in members or not (d or p):
                    continue
                d_note = fmt_note(r.get("Capability Domain Basis"),
                                  r.get("Capability Domain URLs"))
                p_note = fmt_note(r.get("Primary Output Basis"),
                                  r.get("Primary Output URLs"))
                rows.append([label, uei, d, p, d_note, p_note])

    out = EXTRACTED / "vendor_archetype_overrides.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(OUT_HEADERS)
        w.writerows(rows)
    print(f"wrote {out}  ({len(rows)} override rows across "
          f"{len(set((r[0], r[1]) for r in rows))} UEI x program)")


if __name__ == "__main__":
    build()
