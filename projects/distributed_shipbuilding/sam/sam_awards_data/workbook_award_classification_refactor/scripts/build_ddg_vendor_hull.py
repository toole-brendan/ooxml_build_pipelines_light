"""build_ddg_vendor_hull - the vendor x assigned-hull spines (vendor x hull, and vendor x hull x SWBS).

Emits the ROW SPINES (+ static leaf attributes) for two model sheets; every dollar / record / date
column is a live SUMIFS / COUNTIFS / MINIFS / MAXIFS on the DDG Subaward Transactions leaf, so the
values stay blank here:
  - ddg_vendor_hull_exposure.csv : one row per (UEI x Assigned Hull), keyed live on UEI + hull.
  - ddg_vendor_hull_swbs.csv     : one row per (UEI x Assigned Hull x SWBS subsystem), HII-Ingalls
                                   only (GD-BIW carries no SWBS), keyed live on UEI + hull + subsystem.

The hull `Assigned Hull` / `Hull Confidence` are LIVE formulas on the sheet (not in the CSV), so this
script RE-DERIVES them in Python from the materialized regex columns + the curated PIID->Hull map via
the shared scripts/_hull_logic.resolve() - the same rule the formulas reproduce. SWBS subsystem /
major group come from the HII work-item code crosswalk (the CSV's SWBS columns are blank formula
placeholders). Run AFTER tag_ddg_transactions_hulls.py.
"""
from __future__ import annotations

import csv
from collections import defaultdict

from _paths import EXTRACTED  # noqa: E402
from _hull_logic import load_map, hull_set, resolve  # noqa: E402

TX_CSV = EXTRACTED / "ddg_subaward_transactions.csv"
XWALK_CSV = EXTRACTED / "hii_swbs_crosswalk.csv"
OUT_CSV = EXTRACTED / "ddg_vendor_hull_exposure.csv"
OUT_SWBS_CSV = EXTRACTED / "ddg_vendor_hull_swbs.csv"

# vendor x hull: static spine + blank live-formula measures + confidence
VH_HEADERS = ["Subawardee UEI", "Hull", "Subawardee Vendor Name", "Builder", "Predominant SWBS",
              "Assigned $M", "Records", "First Subaward", "Last Subaward", "Confidence"]
# vendor x hull x SWBS: + the SWBS major group / subsystem code / subsystem name
VHS_HEADERS = ["Subawardee UEI", "Hull", "Subawardee Vendor Name", "Builder",
               "SWBS Major Group", "SWBS Subsystem", "SWBS Subsystem Name",
               "Assigned $M", "Records", "First Subaward", "Last Subaward", "Confidence"]


def load_swbs_by_code() -> dict[str, tuple[str, str, str]]:
    """{HII Work-Item Code -> (subsystem code, major-group label, subsystem name)} from the
    crosswalk. SWBS display is 'N00 Group > NNN Subsystem name'; major = before the '>', subsystem
    name = after it. Replicates the lookup the tx sheet does as a live formula."""
    out: dict[str, tuple[str, str, str]] = {}
    with XWALK_CSV.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            code = (r.get("HII Work-Item Code") or "").strip()
            sub = (r.get("SWBS Subsystem") or "").strip()
            disp = (r.get("SWBS") or "").strip()
            if not code:
                continue
            parts = disp.replace(">", "›").split("›")
            major = parts[0].strip()
            name = parts[1].strip() if len(parts) > 1 else sub
            out[code] = (sub, major, name)
    return out


# U00 fallback for an HII row whose code is absent from the crosswalk (matches the tx U00 cells).
_U00 = ("U00", "U00 No SWBS Evidence", "U00 No SWBS Evidence")


def _hull_num(h: str) -> int:
    return int("".join(ch for ch in h if ch.isdigit()) or 0)


def build() -> None:
    fam_info = load_map()
    by_code = load_swbs_by_code()
    with TX_CSV.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    vh: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"vendor": "", "builder": "", "records": 0,
                 "major": defaultdict(int), "conf": set()})
    vhs: dict[tuple[str, str, str], dict] = defaultdict(
        lambda: {"vendor": "", "builder": "", "major": "", "name": "", "records": 0, "conf": set()})

    for r in rows:
        uei = (r.get("Subawardee UEI") or "").strip()
        piid = (r.get("Prime PIID") or "").strip()
        builder = (r.get("Builder") or "").strip()
        direct = hull_set(r.get("Direct Hull Text", ""))
        req = hull_set(r.get("Prime Requirement Hull Text", ""))
        assigned, _scope, _basis, conf = resolve(piid, direct, req, fam_info)
        if not assigned or not uei:
            continue

        # vendor x hull (all builders)
        d = vh[(uei, assigned)]
        d["vendor"] = d["vendor"] or (r.get("Subawardee Vendor Name") or "").strip()
        d["builder"] = d["builder"] or builder
        d["records"] += 1
        if builder == "HII-Ingalls":
            sub, major, _name = by_code.get((r.get("HII Work-Item Code") or "").strip(), _U00)
        else:
            sub, major = "", "n/a (non-HII)"
        d["major"][major] += 1
        if conf:
            d["conf"].add(conf)

        # vendor x hull x SWBS (HII-Ingalls only - GD-BIW carries no SWBS)
        if builder == "HII-Ingalls":
            sub, major, name = by_code.get((r.get("HII Work-Item Code") or "").strip(), _U00)
            s = vhs[(uei, assigned, sub)]
            s["vendor"] = s["vendor"] or (r.get("Subawardee Vendor Name") or "").strip()
            s["builder"] = s["builder"] or builder
            s["major"], s["name"] = major, name
            s["records"] += 1
            if conf:
                s["conf"].add(conf)

    # --- vendor x hull spine ---
    vh_out = []
    for (uei, hull), d in vh.items():
        major = max(d["major"].items(), key=lambda kv: (kv[1], kv[0]))[0] if d["major"] else ""
        vh_out.append((uei, hull, d["vendor"], d["builder"], major,
                       "/".join(sorted(d["conf"])), d["records"]))
    vh_out.sort(key=lambda x: (_hull_num(x[1]), -x[6], x[2]))
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(VH_HEADERS)
        for uei, hull, vendor, builder, major, conf, _rec in vh_out:
            w.writerow([uei, hull, vendor, builder, major, "", "", "", "", conf])

    # --- vendor x hull x SWBS spine ---
    vhs_out = []
    for (uei, hull, sub), s in vhs.items():
        vhs_out.append((uei, hull, s["vendor"], s["builder"], s["major"], sub, s["name"],
                        "/".join(sorted(s["conf"])), s["records"]))
    vhs_out.sort(key=lambda x: (_hull_num(x[1]), -x[8], x[2], x[5]))
    with OUT_SWBS_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(VHS_HEADERS)
        for uei, hull, vendor, builder, major, sub, name, conf, _rec in vhs_out:
            w.writerow([uei, hull, vendor, builder, major, sub, name, "", "", "", "", conf])

    print("\n==== DDG Vendor x Hull spines ====")
    print(f"vendor x hull       : {OUT_CSV}  ({len(vh_out)} rows, "
          f"{len({x[0] for x in vh_out})} vendors, {len({x[1] for x in vh_out})} hulls)")
    print(f"vendor x hull x SWBS: {OUT_SWBS_CSV}  ({len(vhs_out)} rows, HII-Ingalls only)")
    print("all $/record/date columns are formulas on the sheets (blank here).")


if __name__ == "__main__":
    build()
