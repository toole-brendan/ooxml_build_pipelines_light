"""Aggregate FPDS place-of-performance per PIID + per vendor slug.

Consumes the FPDS pulls in fpds_raw/ (which now carry pop_state_code,
pop_country_code, pop_city, etc. — added by the patch to
pull_fpds_sub_primes.py on 2026-05-24).

For each PIID, computes:
    - total obligated $
    - distribution across POP state codes ($, records, %)
    - rollup into EB-sites / HII-sites / Other-US / Foreign / Unknown buckets
    - top POP state and top POP city by $

Where:
    - EB-sites := POP city in {GROTON, QUONSET POINT, NORTH KINGSTOWN}
    - HII-sites := POP city = NEWPORT NEWS (with pop_state_code = VA as guard)
    - Other-US := pop_country_code = USA but not EB/HII city
    - Foreign := pop_country_code != USA and non-empty
    - Unknown := pop_country_code or pop_state_code is null/empty

Outputs:
    - extracted/fpds_pop_by_piid_state.csv  (long: piid, state, country, $, records)
    - extracted/fpds_pop_by_piid_rollup.csv (wide per-PIID with bucket % + top city/state)
    - extracted/fpds_pop_by_slug.csv        (per FPDS query slug rollup)

In-scope (15) PIIDs are flagged via nc_scope_summary.json.

Run after the FPDS re-pull completes:
    python3 scripts/aggregate_fpds_pop.py
"""
import csv
import glob
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPDS_DIR = os.path.join(ROOT, "fpds_raw")
SCOPE_JSON = os.path.join(ROOT, "extracted", "nc_scope_summary.json")
OUT_DIR = os.path.join(ROOT, "extracted")

EB_CITIES = {"GROTON", "QUONSET POINT", "NORTH KINGSTOWN"}
HII_CITIES = {"NEWPORT NEWS"}


def bucket(country, state, city):
    city_u = (city or "").strip().upper()
    state_u = (state or "").strip().upper()
    country_u = (country or "").strip().upper()
    if not country_u and not state_u:
        return "unknown"
    if city_u in EB_CITIES:
        return "eb"
    if city_u in HII_CITIES and state_u == "VA":
        return "hii"
    if country_u == "USA":
        return "other_us"
    return "foreign"


def load_inscope_piids():
    if not os.path.exists(SCOPE_JSON):
        return set()
    with open(SCOPE_JSON) as f:
        d = json.load(f)
    return set(d.get("in_scope_piids") or [])


def iter_fpds_records():
    for fp in sorted(glob.glob(os.path.join(FPDS_DIR, "*_raw.json"))):
        slug = os.path.basename(fp).replace("_raw.json", "")
        with open(fp) as f:
            data = json.load(f)
        recs = data.get("records", data) if isinstance(data, dict) else data
        if not isinstance(recs, list):
            continue
        for r in recs:
            yield slug, r


def main():
    in_scope = load_inscope_piids()

    by_piid_state = defaultdict(lambda: {"dollars": 0.0, "records": 0, "country": ""})
    by_piid_total = defaultdict(lambda: defaultdict(float))
    by_piid_records = defaultdict(int)
    by_piid_city_dollars = defaultdict(lambda: defaultdict(float))
    by_piid_state_dollars = defaultdict(lambda: defaultdict(float))
    by_slug = defaultdict(lambda: defaultdict(float))
    by_slug_records = defaultdict(int)

    n_total = 0
    n_null_pop = 0

    for slug, r in iter_fpds_records():
        n_total += 1
        piid = (r.get("piid") or "").strip()
        if not piid:
            continue
        try:
            amt = float(r.get("this_obligated") or 0)
        except (TypeError, ValueError):
            amt = 0.0
        country = (r.get("pop_country_code") or "").strip()
        state = (r.get("pop_state_code") or "").strip()
        city = (r.get("pop_city") or "").strip()
        b = bucket(country, state, city)
        if b == "unknown":
            n_null_pop += 1

        # long form by (piid, state, country)
        key = (piid, state or "NULL", country or "NULL")
        by_piid_state[key]["dollars"] += amt
        by_piid_state[key]["records"] += 1
        by_piid_state[key]["country"] = country or "NULL"

        # rollup
        by_piid_total[piid][b] += amt
        by_piid_total[piid]["total"] += amt
        by_piid_records[piid] += 1
        if city:
            by_piid_city_dollars[piid][(city.upper(), state.upper())] += amt
        if state:
            by_piid_state_dollars[piid][state.upper()] += amt

        # slug rollup
        by_slug[slug][b] += amt
        by_slug[slug]["total"] += amt
        by_slug_records[slug] += 1

    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. Long form: piid x state x country
    out1 = os.path.join(OUT_DIR, "fpds_pop_by_piid_state.csv")
    with open(out1, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["piid", "in_scope_17", "pop_state_code", "pop_country_code", "dollars", "records"])
        for (piid, state, country), v in sorted(by_piid_state.items(), key=lambda kv: (kv[0][0], -kv[1]["dollars"])):
            w.writerow([
                piid,
                "yes" if piid in in_scope else "no",
                state,
                country,
                round(v["dollars"], 2),
                v["records"],
            ])

    # 2. Per-PIID rollup (wide)
    out2 = os.path.join(OUT_DIR, "fpds_pop_by_piid_rollup.csv")
    with open(out2, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "piid", "in_scope_17", "records", "total_dollars",
            "eb_dollars", "eb_pct",
            "hii_dollars", "hii_pct",
            "other_us_dollars", "other_us_pct",
            "foreign_dollars", "foreign_pct",
            "unknown_dollars", "unknown_pct",
            "top_pop_state", "top_pop_state_pct",
            "top_pop_city", "top_pop_city_pct",
        ])
        for piid in sorted(by_piid_total, key=lambda p: -by_piid_total[p]["total"]):
            tot = by_piid_total[piid]["total"] or 1.0
            top_state, top_state_d = max(by_piid_state_dollars[piid].items(), key=lambda kv: kv[1], default=("", 0))
            top_city, top_city_d = max(by_piid_city_dollars[piid].items(), key=lambda kv: kv[1], default=(("", ""), 0))
            def pct(b):
                return round(100.0 * by_piid_total[piid].get(b, 0.0) / tot, 2)
            w.writerow([
                piid,
                "yes" if piid in in_scope else "no",
                by_piid_records[piid],
                round(by_piid_total[piid]["total"], 2),
                round(by_piid_total[piid].get("eb", 0), 2), pct("eb"),
                round(by_piid_total[piid].get("hii", 0), 2), pct("hii"),
                round(by_piid_total[piid].get("other_us", 0), 2), pct("other_us"),
                round(by_piid_total[piid].get("foreign", 0), 2), pct("foreign"),
                round(by_piid_total[piid].get("unknown", 0), 2), pct("unknown"),
                top_state, round(100.0 * top_state_d / tot, 2),
                f"{top_city[0]}, {top_city[1]}" if top_city[0] else "", round(100.0 * top_city_d / tot, 2),
            ])

    # 3. Per-slug rollup
    out3 = os.path.join(OUT_DIR, "fpds_pop_by_slug.csv")
    with open(out3, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "slug", "records", "total_dollars",
            "eb_pct", "hii_pct", "other_us_pct", "foreign_pct", "unknown_pct",
        ])
        for slug in sorted(by_slug, key=lambda s: -by_slug[s]["total"]):
            tot = by_slug[slug]["total"] or 1.0
            def pct(b):
                return round(100.0 * by_slug[slug].get(b, 0.0) / tot, 2)
            w.writerow([
                slug, by_slug_records[slug], round(by_slug[slug]["total"], 2),
                pct("eb"), pct("hii"), pct("other_us"), pct("foreign"), pct("unknown"),
            ])

    print(f"Loaded {n_total} FPDS records ({n_null_pop} with null POP = {100.0*n_null_pop/max(n_total,1):.1f}%)")
    print(f"Wrote {out1}")
    print(f"Wrote {out2}")
    print(f"Wrote {out3}")


if __name__ == "__main__":
    main()
