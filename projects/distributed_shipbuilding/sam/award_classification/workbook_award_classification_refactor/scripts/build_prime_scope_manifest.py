"""build_prime_scope_manifest - generate the versioned prime-contract scope manifest.

The manifest (`prime_contract_scope.csv` at the workbook root) is the canonical control
that reviewer finding #1 requires: every prime PIID that the new-construction corpus
queries is listed exactly once, with its class, builder group, a scope_type descriptor,
an include flag (Y/N), a rationale, and a source. `_corpus.load_scope()` reads it and
drops every `include=N` PIID from scope, so an out-of-scope prime cannot reach the
transaction / program-vendor / Supplier-Master CSVs; `_integrity.assert_piids_in_manifest()`
fails the build if any transaction PIID is missing from the manifest or is flagged N.

The "queried" universe = the PIIDs the pipeline actually walks: DDG groups GD-BIW +
HII-Ingalls, submarines the GDEB-directed primes (the same filters in _corpus / the
program-transaction build). Zero-subaward queried primes are listed too, so an omitted
query can never masquerade as a genuine zero.

This generator encodes the curation; the emitted CSV is the source of truth read at build
time. Re-run only to regenerate after a curation change:
    python3 scripts/build_prime_scope_manifest.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from _paths import REPO  # noqa: E402
DDG_SCOPE = REPO / "projects/distributed_shipbuilding/tam/ddg_research/extracted/nc_scope_summary.json"
SUBS_SCOPE = REPO / "projects/distributed_shipbuilding/tam/virginia_columbia_research/extracted/nc_scope_summary.json"
OUT = REPO / "projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/prime_contract_scope.csv"

# --- research/decision-identified out-of-scope primes (2026-06-21 review) ---------------
# These need an explicit, sourced rationale because the call rests on contract research
# (the scope label alone is uninformative) or on a specific dollar-bearing decision.
# piid -> (scope_type, rationale, source)
EXCLUDE_EXPLICIT = {
    "N0002414C4313": ("other-class",
                      "Littoral Combat Ship planning-yard / in-service support - not DDG-51 new construction",
                      "war.gov Contracts 2019-02-07; review 2026-06-21"),
    "N0002419C2322": ("other-class",
                      "DDG-1000 class planning-yard / LMVLS work - not DDG-51 new construction",
                      "sam.gov DDG 1000 Class Planning Yard; review 2026-06-21"),
    "N0002406C2303": ("other-class",
                      "DDG-1000 (Zumwalt) detail design & construction ($3.31B, PSC 1903; SAM program "
                      "'DDG 1000') - not DDG-51 new construction. Zero subawards in corpus, so no dollar "
                      "impact; flipped from a mislabeled include=Y on 2026-06-23",
                      "SAM Contract Awards API (awardeeUniqueEntityId=FREEMCLKFXE3); review 2026-06-23"),
    "N0002411C2306": ("other-class",
                      "DDG-1000 (Zumwalt) COSAL warehousing ($2.55B, PSC 1903, SAM program 'DDG 1000') - "
                      "not DDG-51 new construction. Zero subawards in corpus; flipped from a mislabeled "
                      "include=Y on 2026-06-23",
                      "SAM Contract Awards API (awardeeUniqueEntityId=FREEMCLKFXE3); review 2026-06-23"),
    "N0002419C4452": ("provisioned-material/planning-yard",
                      "Integrated planning-yard provisioned-item orders, maintenance & modernization - not Basic Construction",
                      "war.gov Contracts 2019-02-04; review 2026-06-21"),
    "N0002412C2312": ("design-engineering",
                      "Flight III follow-yard design / test & trials support - not Basic Construction",
                      "govdelivery USDOD 2013-05-16; review 2026-06-21"),
    "N0002420C2120": ("lead-yard-support",
                      "Virginia Lead Yard Support & Design (added 2026-06-21) - lead-yard design/engineering agent work, "
                      "not Basic Construction; removed per 2026-06-21 review decision",
                      "review 2026-06-21"),
    "N0002413C2128": ("design-engineering",
                      "Columbia design-drawings package - design/engineering, not Basic Construction; "
                      "removed per 2026-06-21 review follow-up (consistent with the Virginia lead-yard exclusion)",
                      "review 2026-06-21"),
}

# Work types that are out of scope and excluded uniformly by rule. Any queried prime whose
# scope label classifies to one of these is dropped (most are zero-subaward, so the dollar
# impact beyond EXCLUDE_EXPLICIT is nil - they are excluded for scope consistency).
# IN-SCOPE BY DESIGN: the submarine master / LLTM PIIDs (titled "LONG LEAD TIME MATERIAL")
# carry the shipbuilder-procured non-nuclear AP / LLTM / EOQ we WANT, commingled with Basic
# Construction. "LLTM" is deliberately absent from _scope_type's exclude keywords below - do
# NOT add it, or the submarine long-lead base disappears. (Nuclear-reactor LLTM is dropped
# upstream by the bgroup == "GDEB" filter, which removes the BPMI naval-reactor PIIDs.)
EXCLUDE_TYPES = {"design-engineering", "lead-yard-support", "ship-alteration",
                 "provisioned-material/planning-yard"}


def _scope_type(label: str) -> str:
    """Honest work-type descriptor for a queried prime, from its scope label."""
    u = label.upper()
    if "LEAD YARD SUPPORT" in u:
        return "lead-yard-support"
    if "SHIP ALTERATION" in u:
        return "ship-alteration"
    if "PROVISIONED ITEM" in u or "(PIO)" in u:
        return "provisioned-material/planning-yard"
    if "DESIGN" in u or "CONCEPT" in u:
        return "design-engineering"
    if any(k in u for k in ("CLOSEOUT", "DIACAP", "REALLOCATION", "CANCELLATION")):
        return "new-construction-admin"
    return "new-construction"


def _queried():
    """Yield (piid, program_label, class, builder_group, scope_label) for every queried prime."""
    ddg = json.loads(DDG_SCOPE.read_text())["in_scope_piids"]
    subs = json.loads(SUBS_SCOPE.read_text())["in_scope_piids"]
    for piid, v in ddg.items():
        if v.get("group") in ("GD-BIW", "HII-Ingalls"):
            yield piid, "DDG", v.get("class", ""), v.get("group", ""), v.get("label", "")
    for piid, v in subs.items():
        grp = v.get("group") or v.get("prime") or ""
        if grp == "GDEB":
            yield piid, v.get("class", ""), v.get("class", ""), grp, v.get("label", "")


def main() -> None:
    rows = []
    for piid, program, klass, group, label in _queried():
        if piid in EXCLUDE_EXPLICIT:
            stype, rationale, source = EXCLUDE_EXPLICIT[piid]
            include = "N"
        else:
            stype = _scope_type(label)
            source = "nc_scope_summary.json"
            if stype in EXCLUDE_TYPES:
                include = "N"
                rationale = (f"Out-of-scope work type ({stype}); excluded per the 2026-06-21 scope "
                             "rule (hull-builder new construction only)")
            else:
                include = "Y"
                rationale = ("In-scope hull-builder new construction, incl. shipbuilder-procured "
                             "non-nuclear long-lead / EOQ on the GDEB master / LLTM PIIDs")
        rows.append([piid, program, klass, group, stype, include, rationale, source])

    rows.sort(key=lambda r: (r[1], r[5], r[0]))  # program, include, piid
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["piid", "program", "class", "builder_group", "scope_type",
                    "include", "rationale", "source"])
        w.writerows(rows)
    n_excl = sum(1 for r in rows if r[5] == "N")
    print(f"wrote {OUT} : {len(rows)} primes ({n_excl} excluded)")


if __name__ == "__main__":
    main()
