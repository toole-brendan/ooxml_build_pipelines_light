"""build_swbs_crosswalk - the HII work-item code -> SWBS crosswalk (leaf reference).

The single centralized lookup behind the formula-driven DDG Subaward SWBS sheet, the
SWBS analogue of the NAICS-6 Archetype Map. One row per HII work-item code, giving the
ship-system application (SWBS) that the transaction-grain sheet resolves by INDEX/MATCH
on the code. Two provenance tiers:

  X (observed)  - the code has a deterministic modal SWBS group in the HII code
                  dictionary (i.e. it was seen with an explicit 3-digit SWBS somewhere;
                  no one-to-many conflicts in this pull). 113 codes.
  C (curated)   - a curated inference from the code's component text, vendor evidence and
                  codebook, hand-authored in extracted/swbs_curated_c.csv for high-dollar
                  codes the dictionary left blank.

The SWBS display string ("200 Propulsion Plant > 234 Propulsion gas turbines") is composed
here from swbs_hierarchy.csv + _taxonomy.SWBS_GROUPS, with the three standing code
exceptions (730 -> X00, 351 -> L00). Output: extracted/hii_swbs_crosswalk.csv.

Run:
    python3 scripts/build_swbs_crosswalk.py
"""
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

from _paths import REPO  # noqa: E402
AC = REPO / "projects/distributed_shipbuilding/sam/award_classification"
REFACTOR = AC / "workbook_award_classification_refactor"
EXTRACTED = REFACTOR / "extracted"
PKG = AC / "ddg_hii_swbs_subaward_package"

DICT_CSV = PKG / "hii_ddg_code_dictionary.csv"
HIER_CSV = PKG / "swbs_hierarchy.csv"
CURATED_CSV = EXTRACTED / "swbs_curated_c.csv"
OUT_CSV = EXTRACTED / "hii_swbs_crosswalk.csv"

# Major-group names: single-sourced from the taxonomy leaf (pure-constants module),
# loaded by file path so we don't import the whole sheets package.
_spec = importlib.util.spec_from_file_location(
    "_swbs_taxonomy", REFACTOR / "workbook_award_classification_refactor/sheets/_taxonomy.py")
_tax = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tax)
GROUP_NAME = {code: name for code, name, _ex in _tax.SWBS_GROUPS}

BASIS_X = "X · code crosswalk (observed)"
BASIS_C = "C · curated inference"

HEADERS = ["HII Work-Item Code", "SWBS Subsystem", "SWBS", "SWBS basis", "Evidence"]


def _is3(s: str) -> bool:
    s = (s or "").strip()
    return len(s) == 3 and s.isdigit()


def load_hierarchy() -> dict[str, str]:
    out: dict[str, str] = {}
    with HIER_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            code = (r.get("eswbs_code") or "").strip()
            nom = (r.get("nomenclature") or "").strip()
            if code and nom:
                out.setdefault(code, nom)
    return out


def major_bucket(sg: str) -> tuple[str, str]:
    """3-digit subsystem -> (bucket code, bucket name). Exceptions: 730->X00 (Noise &
    Vibration, cross-cutting, not 700); 351->L00 (legacy); else first-digit group."""
    if sg == "730":
        return "X00", GROUP_NAME["X00"]
    if sg == "351":
        return "L00", GROUP_NAME["L00"]
    code = sg[0] + "00"
    return code, GROUP_NAME.get(code, "")


def nomenclature(sg: str, hier: dict[str, str]) -> str:
    """Navy nomenclature for a 3-digit subsystem, sentence-cased (tries NNN00, NNN0, NNN;
    covers 234->23400 and 730->7300); '' if the codebook has none."""
    for key in (sg + "00", sg + "0", sg):
        nom = hier.get(key)
        if nom:
            return nom.capitalize()
    return ""


def swbs_display(sg: str, hier: dict[str, str]) -> str:
    bcode, bname = major_bucket(sg)
    nom = nomenclature(sg, hier)
    return f"{bcode} {bname} › {sg} {nom}".rstrip()


def build() -> None:
    hier = load_hierarchy()

    # X tier: codes with a deterministic modal SWBS group in the dictionary.
    xwalk: dict[str, dict] = {}
    with DICT_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            code = (r.get("code") or "").strip()
            modal = (r.get("modal_swbs_group") or "").strip()
            if code and _is3(modal):
                xwalk[code] = {"sg": modal, "basis": BASIS_X,
                               "evidence": (r.get("top_components") or "").strip()}

    # C tier: hand-curated codes the dictionary left blank. Never overwrites an X row.
    c_added = c_skipped = 0
    with CURATED_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            code = (r.get("HII Work-Item Code") or "").strip()
            sg = (r.get("SWBS Subsystem") or "").strip()
            if not code or not _is3(sg):
                continue
            if code in xwalk:           # deterministic X wins; flag the redundant curation
                c_skipped += 1
                continue
            ev = (r.get("Rationale") or "").strip()
            xwalk[code] = {"sg": sg, "basis": BASIS_C, "evidence": ev}
            c_added += 1

    rows = []
    for code in sorted(xwalk):
        e = xwalk[code]
        rows.append([code, e["sg"], swbs_display(e["sg"], hier), e["basis"], e["evidence"]])

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADERS)
        w.writerows(rows)

    n_x = sum(1 for v in xwalk.values() if v["basis"] == BASIS_X)
    print("\n==== HII Work-Item SWBS Crosswalk ====")
    print(f"output: {OUT_CSV}")
    print(f"rows (distinct codes)             : {len(rows)}")
    print(f"  X (observed, from dictionary)   : {n_x}")
    print(f"  C (curated)                     : {c_added}")
    if c_skipped:
        print(f"  curated rows skipped (code already X): {c_skipped}")


if __name__ == "__main__":
    build()
