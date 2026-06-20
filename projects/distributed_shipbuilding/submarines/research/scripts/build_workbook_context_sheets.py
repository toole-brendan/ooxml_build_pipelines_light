#!/usr/bin/env python3
"""
Build data inputs for 3 new workbook sheets:
  - Trends:        YoY $, concentration, NAICS mix shift, vendor base growth
  - Geographic:    $ by US state + foreign country
  - HII context:   NNS segment revenue + implied submarine share + FFATA gap

Outputs to extracted/:
  nc_trends.csv
  nc_geo_by_state.csv
  nc_geo_by_country.csv
  hii_context.csv
"""
import csv
import glob
import json
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/submarine_outsourced_work")
OUT = REPO / "extracted"

# Reuse the new-construction scope from the aggregator
IN_SCOPE_PIIDS = {
    "N0002417C2100", "N0002417C2117", "N0002424C2110", "N0002412C2115",
    "N0002409C2104", "N0002413C2128", "N0002411C2109", "N0002416C2111",
    "N0002410C2118", "N0002419C2114", "N0002419C2115", "N0002424C2114",
    "N0002410C6266", "N0002421C4106", "N0002421C4111",
}
MIB_EXCLUDED_UEIS = {"F8PEZKXES8B1", "QLJZVM6XKR71", "TCM3R4JPRKY4"}


def fy_of(date_str):
    if not date_str or len(date_str) < 10:
        return None
    y, m = int(date_str[:4]), int(date_str[5:7])
    return y + 1 if m >= 10 else y


def load_in_scope_records():
    """Read raw SAM JSON, filter to in-scope PIIDs + drop MIB vendors."""
    recs = []
    for f in sorted(glob.glob(str(REPO / "sam_subawards" / "N*.json"))):
        piid = Path(f).stem.split("_")[0]
        if piid not in IN_SCOPE_PIIDS:
            continue
        d = json.load(open(f))
        for r in d.get("published", []):
            uei = (r.get("subParentUei") or r.get("subEntityUei") or "").strip()
            if uei in MIB_EXCLUDED_UEIS:
                continue
            recs.append(r)
    return recs


# ============================================================================
# TRENDS
# ============================================================================

def build_trends(recs, naics_lookup):
    """For each FY:
      - total $
      - YoY % change
      - # records, # unique parent UEIs
      - top-5 vendor share
      - HHI (Herfindahl-Hirschman concentration index)
      - top-2 NAICS-4 work-type buckets (which industries dominate)
    """
    # Group by FY
    fy_vendors = defaultdict(lambda: defaultdict(float))  # fy → {uei: $}
    fy_records = defaultdict(int)
    fy_naics = defaultdict(lambda: defaultdict(float))  # fy → {naics4: $}
    uei_to_naics4 = {}
    for r in naics_lookup:
        if r.get("naics_4digit") and r.get("naics_4digit") not in ("UNKN", ""):
            uei_to_naics4[r["uei"]] = (r["naics_4digit"], r.get("naics_desc", ""))

    for rec in recs:
        fy = fy_of(rec.get("subAwardDate"))
        if fy is None:
            continue
        uei = (rec.get("subParentUei") or rec.get("subEntityUei") or "").strip()
        amt = float(rec.get("subAwardAmount") or 0)
        fy_vendors[fy][uei] += amt
        fy_records[fy] += 1
        if uei in uei_to_naics4:
            n4, _ = uei_to_naics4[uei]
            fy_naics[fy][n4] += amt

    rows = []
    fys = sorted(fy_vendors.keys())
    prev_total = None
    for fy in fys:
        amts = list(fy_vendors[fy].values())
        total = sum(amts)
        if total <= 0:
            continue
        # Top-5 share
        sorted_amts = sorted(amts, reverse=True)
        top5 = sum(sorted_amts[:5])
        top10 = sum(sorted_amts[:10])
        # HHI: sum of squared market shares (×10,000 for the standard scale)
        # Standard HHI: 0-10,000; <1500 = competitive, >2500 = concentrated
        shares = [a / total for a in amts]
        hhi = sum(s * s for s in shares) * 10000

        # Top NAICS-4 industries this FY
        naics_sorted = sorted(fy_naics[fy].items(), key=lambda kv: -kv[1])
        top_naics_str = "; ".join(
            f"{n4}=${amt/1e6:,.0f}M" for n4, amt in naics_sorted[:3]
        )

        yoy_pct = None if prev_total is None else (total / prev_total - 1.0)
        rows.append({
            "fy": fy,
            "total_$M": total / 1e6,
            "yoy_pct": yoy_pct,
            "records": fy_records[fy],
            "unique_parent_ueis": len(amts),
            "top5_share": top5 / total,
            "top10_share": top10 / total,
            "hhi_0_to_10000": hhi,
            "concentration_label": (
                "Highly concentrated" if hhi > 2500
                else "Moderately concentrated" if hhi > 1500
                else "Competitive"
            ),
            "top3_naics4_$": top_naics_str,
        })
        prev_total = total

    with open(OUT / "nc_trends.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {OUT/'nc_trends.csv'} ({len(rows)} rows)")


# ============================================================================
# GEOGRAPHIC
# ============================================================================

def build_geo(recs):
    """Aggregate $ by US state + by country."""
    by_state = defaultdict(lambda: {"amt": 0.0, "n": 0, "vendors": set()})
    by_country = defaultdict(lambda: {"amt": 0.0, "n": 0, "vendors": set()})
    foreign_by_fy = defaultdict(lambda: {"foreign": 0.0, "domestic": 0.0})

    # Country code normalization (records vary in casing/format, e.g. USA vs UNITED STATES,
    # GB vs GBR). Map 3-letter and inconsistent forms to canonical 2-letter ISO + Title-case name.
    COUNTRY_CANON = {
        "USA": ("US", "United States"),
        "US":  ("US", "United States"),
        "UNITED STATES": ("US", "United States"),
        "GB": ("GB", "United Kingdom"),
        "GBR": ("GB", "United Kingdom"),
        "UNITED KINGDOM": ("GB", "United Kingdom"),
        "CA": ("CA", "Canada"),
        "CAN": ("CA", "Canada"),
        "CANADA": ("CA", "Canada"),
        "CH": ("CH", "Switzerland"),
        "DK": ("DK", "Denmark"),
        "BR": ("BR", "Brazil"),
        "CN": ("CN", "China"),
    }

    def canon_country(code, name):
        for key in (code, name and name.upper()):
            if key and key in COUNTRY_CANON:
                return COUNTRY_CANON[key]
        return (code or "??", name or "Unknown")

    for r in recs:
        amt = float(r.get("subAwardAmount") or 0)
        addr = r.get("entityPhysicalAddress") or {}
        raw_country = (addr.get("country") or {}).get("code", "USA")
        raw_country_name = (addr.get("country") or {}).get("name", "United States")
        country, country_name = canon_country(raw_country, raw_country_name)
        state_code = (addr.get("state") or {}).get("code", "")
        state_name = (addr.get("state") or {}).get("name", "")
        uei = r.get("subParentUei") or r.get("subEntityUei") or ""

        # By country
        ck = (country, country_name)
        by_country[ck]["amt"] += amt
        by_country[ck]["n"] += 1
        if uei: by_country[ck]["vendors"].add(uei)

        # By state (US only)
        if country == "US" and state_code:
            sk = (state_code, state_name)
            by_state[sk]["amt"] += amt
            by_state[sk]["n"] += 1
            if uei: by_state[sk]["vendors"].add(uei)

        # FY × foreign/domestic
        fy = fy_of(r.get("subAwardDate"))
        if fy is not None:
            if country == "US":
                foreign_by_fy[fy]["domestic"] += amt
            else:
                foreign_by_fy[fy]["foreign"] += amt

    # Write state CSV
    state_rows = sorted(
        ({"state": k[0], "state_name": k[1],
          "amount_M": v["amt"] / 1e6, "records": v["n"],
          "unique_vendors": len(v["vendors"])} for k, v in by_state.items()),
        key=lambda x: -x["amount_M"],
    )
    total_us = sum(r["amount_M"] for r in state_rows)
    for r in state_rows:
        r["pct_of_us_total"] = r["amount_M"] / total_us if total_us else 0
    with open(OUT / "nc_geo_by_state.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["state", "state_name", "amount_M",
                                           "pct_of_us_total", "records",
                                           "unique_vendors"])
        w.writeheader()
        for r in state_rows:
            w.writerow(r)
    print(f"Wrote {OUT/'nc_geo_by_state.csv'} ({len(state_rows)} rows)")

    # Write country CSV
    country_rows = sorted(
        ({"country_code": k[0], "country": k[1],
          "amount_M": v["amt"] / 1e6, "records": v["n"],
          "unique_vendors": len(v["vendors"])} for k, v in by_country.items()),
        key=lambda x: -x["amount_M"],
    )
    grand_total = sum(r["amount_M"] for r in country_rows)
    for r in country_rows:
        r["pct_of_total"] = r["amount_M"] / grand_total if grand_total else 0
    with open(OUT / "nc_geo_by_country.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["country_code", "country", "amount_M",
                                           "pct_of_total", "records", "unique_vendors"])
        w.writeheader()
        for r in country_rows:
            w.writerow(r)
    print(f"Wrote {OUT/'nc_geo_by_country.csv'} ({len(country_rows)} rows)")

    # Write foreign-share-by-FY
    with open(OUT / "nc_foreign_share_by_fy.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["fy", "domestic_$M", "foreign_$M", "total_$M", "foreign_share"])
        for fy in sorted(foreign_by_fy.keys()):
            v = foreign_by_fy[fy]
            total = v["domestic"] + v["foreign"]
            share = v["foreign"] / total if total else 0
            w.writerow([fy, f"{v['domestic']/1e6:.2f}", f"{v['foreign']/1e6:.2f}",
                        f"{total/1e6:.2f}", f"{share:.4f}"])
    print(f"Wrote {OUT/'nc_foreign_share_by_fy.csv'}")


# ============================================================================
# HII CONTEXT
# ============================================================================

def build_hii_context():
    """Pull NNS segment data + compute implied sub revenue at 25/30/35%."""
    edgar = REPO / "edgar_research" / "hii_nns_segment_reconciled.csv"
    if not edgar.exists():
        print(f"  ⚠ {edgar} missing — run pull_hii_10k_research.py first")
        return

    nns = {}
    with open(edgar) as f:
        for r in csv.DictReader(f):
            fy = int(r["fy_in_note"])
            nns[fy] = {
                "nns_rev": float(r["nns_total_rev_$M"]) if r["nns_total_rev_$M"] else 0,
                "nns_oi": float(r["nns_op_income_$M"]) if r["nns_op_income_$M"] else 0,
                "source_book": int(r["fy_book"]),
            }

    # Pull FFATA-visible HII-NNS sub $ for comparison (from existing aggregation)
    # The visible HII-NNS sub $ in our nc data is the total flowing TO Newport News
    # Shipbuilding when it appears as a sub under a GDEB prime PIID.
    ffata_hii_by_fy = defaultdict(float)
    for f in glob.glob(str(REPO / "sam_subawards" / "N*.json")):
        piid = Path(f).stem.split("_")[0]
        if piid not in IN_SCOPE_PIIDS:
            continue
        d = json.load(open(f))
        for r in d.get("published", []):
            name = (r.get("subEntityParentLegalBusinessName") or
                    r.get("subEntityLegalBusinessName") or "").upper()
            if "NEWPORT NEWS" in name or "HUNTINGTON INGALLS" in name:
                fy = fy_of(r.get("subAwardDate"))
                if fy is not None:
                    ffata_hii_by_fy[fy] += float(r.get("subAwardAmount") or 0)

    rows = []
    for fy in sorted(nns.keys()):
        nns_rev = nns[fy]["nns_rev"]
        ffata = ffata_hii_by_fy.get(fy, 0) / 1e6  # $M
        rows.append({
            "fy": fy,
            "nns_segment_rev_$M": nns_rev,
            "nns_seg_op_income_$M": nns[fy]["nns_oi"],
            "nns_op_margin_pct": nns[fy]["nns_oi"] / nns_rev if nns_rev else 0,
            "implied_sub_rev_low_25pct_$M": nns_rev * 0.25,
            "implied_sub_rev_mid_30pct_$M": nns_rev * 0.30,
            "implied_sub_rev_high_35pct_$M": nns_rev * 0.35,
            "ffata_visible_hii_as_sub_$M": ffata,
            "gap_ratio_30pct_vs_ffata":
                (nns_rev * 0.30) / ffata if ffata > 0 else None,
            "source_book": f"FY{nns[fy]['source_book']} 10-K",
        })

    with open(OUT / "hii_context.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {OUT/'hii_context.csv'} ({len(rows)} rows)")


def load_naics_lookup():
    path = OUT / "entity_naics_lookup.csv"
    if not path.exists():
        return []
    return list(csv.DictReader(open(path)))


def main():
    print("=== Loading in-scope records ===")
    recs = load_in_scope_records()
    print(f"  {len(recs):,} records loaded")
    naics_lookup = load_naics_lookup()
    print(f"  {len(naics_lookup)} NAICS entries loaded\n")

    print("=== Building Trends ===")
    build_trends(recs, naics_lookup)
    print()

    print("=== Building Geographic ===")
    build_geo(recs)
    print()

    print("=== Building HII Context ===")
    build_hii_context()
    print()

    print("=== DONE ===")


if __name__ == "__main__":
    main()
