#!/usr/bin/env python3
"""
Dedupe + relevance-score the cached SAM.gov opportunity pulls into one CSV.

Pure local — no network. Reads sam_opportunities/*.json (pull script output),
dedupes on noticeId, scores ASV/USV relevance from the title + NAICS/PSC, and
writes extracted/opportunities_all.csv sorted by tier then deadline.

Tiers:
  STRONG — title carries an unambiguous unmanned/autonomous-surface-vessel
           phrase (e.g. "unmanned surface", "USV", "uncrewed vessel")
  MEDIUM — title pairs a maritime word with an autonomy word, or the notice
           sits in a vessel NAICS/PSC (336611/336612, PSC 19xx) with an
           autonomy word in the title
  VESSEL — vessel-domain NAICS/PSC but no autonomy signal (crewed boats,
           ship repair, etc.) — context only
  OTHER  — matched a broad keyword sweep but neither maritime nor vessel-coded

Award notices and J&As are pre-awarded/post-award — flagged pre_award=no so
the actionable cut is `pre_award=yes`, which is the point of this dataset.
"""
import csv
import json
import re
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[1]
IN_DIR = RESEARCH / "sam_opportunities"
OUT_DIR = RESEARCH / "extracted"
OUT_DIR.mkdir(exist_ok=True)
OUT_CSV = OUT_DIR / "opportunities_all.csv"

# All matching is word-boundary regex on the lowercased title — plain
# substring checks misfire badly here ("USVI" hits "usv", "portable" hits
# "port", "aircraft" hits "craft").
def _rx(words):
    return re.compile(r"\b(?:" + "|".join(words) + r")\b")

STRONG_RX = _rx([
    "unmanned surface", "autonomous surface", "uncrewed surface",
    "usvs?", "musv", "lusv",
    "unmanned (?:surface )?vessels?", "uncrewed vessels?", "autonomous vessels?",
    "unmanned maritime", "uncrewed maritime", "maritime autonomy",
    "unmanned boats?", "autonomous boats?",
])
MARITIME_RX = _rx([
    "maritime", "naval", "navy", "vessels?", "boats?", "craft",
    "ships?", "shipboard", "warships?", "seabed", "subsea", "undersea",
    "mine countermeasures?", "littoral", "surface warfare", "fleet",
    "ports?", "harbor", "coastal", "sealift", "seas?", "oceans?",
    "ocean floor", "oceanographic", "hydrographic", "bathymetry",
    "waterborne", "watercraft", "coast guard",
])
AUTONOMY_RX = _rx([
    "unmanned", "uncrewed", "autonomous", "autonomy", "robotics?",
    "swarms?", "ai-enabled", "artificial intelligence", "attritable",
])
AIR_RX = _rx(["aircraft", "uas", "suas", "c-uas", "cuas", "uav", "aerial"])
VESSEL_NAICS = {"336611", "336612"}
PRE_AWARD_TYPES = {  # `type` values that are pipeline-side (not yet awarded)
    "Solicitation", "Presolicitation", "Combined Synopsis/Solicitation",
    "Sources Sought", "Special Notice",
}


def tier_for(rec):
    title = (rec.get("title") or "").lower()
    naics = set(rec.get("naicsCodes") or ([rec["naicsCode"]] if rec.get("naicsCode") else []))
    psc = rec.get("classificationCode") or ""
    vessel_coded = bool(naics & VESSEL_NAICS) or psc.startswith("19")
    if STRONG_RX.search(title):
        return "STRONG"
    # Air-domain unmanned (UAS/sUAS/C-UAS) is out of scope unless the title
    # ALSO carries a maritime word — keeps shipboard-UAS notices visible.
    if AUTONOMY_RX.search(title) and (MARITIME_RX.search(title) or vessel_coded) \
            and not (AIR_RX.search(title) and not MARITIME_RX.search(title)):
        return "MEDIUM"
    if vessel_coded:
        return "VESSEL"
    return "OTHER"


def main():
    by_id = {}
    for path in sorted(IN_DIR.glob("*.json")):
        blob = json.loads(path.read_text())
        for rec in blob["records"]:
            nid = rec["noticeId"]
            if nid in by_id:
                by_id[nid]["matched_queries"].add(blob["slug"])
            else:
                rec["matched_queries"] = {blob["slug"]}
                by_id[nid] = rec

    rows = []
    for rec in by_id.values():
        org = rec.get("fullParentPathName") or ""
        rows.append({
            "tier": tier_for(rec),
            "pre_award": "yes" if rec.get("type") in PRE_AWARD_TYPES else "no",
            "type": rec.get("type"),
            "posted": rec.get("postedDate"),
            "deadline": (rec.get("responseDeadLine") or "")[:10],
            "title": rec.get("title"),
            "agency_path": org,
            "naics": ";".join(rec.get("naicsCodes") or []),
            "psc": rec.get("classificationCode") or "",
            "set_aside": rec.get("typeOfSetAside") or "",
            "solicitation_number": rec.get("solicitationNumber") or "",
            "notice_id": rec["noticeId"],
            "ui_link": rec.get("uiLink"),
            "matched_queries": ";".join(sorted(rec["matched_queries"])),
        })

    tier_rank = {"STRONG": 0, "MEDIUM": 1, "VESSEL": 2, "OTHER": 3}
    rows.sort(key=lambda r: (tier_rank[r["tier"]], r["pre_award"] != "yes",
                             r["deadline"] or "9999", r["posted"]))
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    print(f"{n} unique notices -> {OUT_CSV}")
    for t in ("STRONG", "MEDIUM", "VESSEL", "OTHER"):
        sub = [r for r in rows if r["tier"] == t]
        pre = [r for r in sub if r["pre_award"] == "yes"]
        print(f"  {t}: {len(sub)} total, {len(pre)} pre-award")


if __name__ == "__main__":
    main()
