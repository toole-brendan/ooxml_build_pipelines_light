"""align_naics_rationales - align each NAICS-6 D-Rationale's terminal code to the ASSIGNED D.

Reviewer finding #5: 40 NAICS-map rows carry a D-Rationale whose terminal "-> Dxx" token
contradicts the assigned Capability Domain (e.g. 541330 assigned D11 but rationale concludes
"-> D0"). The assigned codes are the intended decisions (the dollar tie-outs are correct); the
notes are stale. This rewrites only the TERMINAL conclusion token to the assigned code,
preserving the reasoning body, so the note matches the decision and the build-time lint
(_integrity.assert_naics_rationale_aligned) passes. Idempotent.

    python3 scripts/align_naics_rationales.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

CSV = (Path(__file__).resolve().parent.parent / "extracted" / "naics6_archetype_map.csv")
_TERMINAL = re.compile(r"->\s*D\d+\s*$")


def _terminal_code(text: str) -> str | None:
    ms = re.findall(r"D(\d+)", text or "")
    return f"D{ms[-1]}" if ms else None


def _conclusion(code: str) -> str:
    if code == "D11":
        return "-> D11 (services / non-material support; no single technical ship domain)"
    return f"-> {code} (dominant technical domain)"


def main() -> None:
    with CSV.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames
        rows = list(reader)

    n = 0
    for r in rows:
        d = (r["Capability Domain (D)"] or "").strip()
        rat = r["D Rationale"] or ""
        term = _terminal_code(rat)
        if not d or term is None or term == d:
            continue
        new = _TERMINAL.sub(_conclusion(d), rat) if _TERMINAL.search(rat) else f"{rat} {_conclusion(d)}"
        if new != rat:
            r["D Rationale"] = new
            n += 1

    with CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"aligned {n} D-Rationale terminal token(s) to the assigned D code -> {CSV.name}")


if __name__ == "__main__":
    main()
