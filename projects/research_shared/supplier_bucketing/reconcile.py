#!/usr/bin/env python3
"""Tasks E & F - reconciliation bridge + final checks (standalone, reproducible).

Reads both projects' nc_records_long.csv (SIGNED $) plus the extended evidence
registry, applies the planned entity-grain classify ladder (registry by
sub_entity_uei -> prime/gfe name -> vendor override -> NAICS4 crosswalk WITHOUT
3364/3344 -> service -> 5511 holding -> residual), and prints:

  E. the 5-view reconciliation bridge (DDG + subs)
  F. final checks: top-25 movers, bucket-share old->new, residual composition,
     VLS out-vs-in sensitivity, and the TAM-vs-shares note.

Status-quo (View 1) uses the LIVE project taxonomies (imported by path) so the
baseline matches today's workbooks. No build code is modified.
"""
from __future__ import annotations
import csv, importlib.util
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/brendantoole/projects2")
REPO = ROOT / "ooxml_build_pipelines_light"
REG_FULL = ROOT / "vendor_evidence_registry.csv"
REG_V1 = ROOT / "vendor_evidence_registry_v1_45.csv.bak"
PROJ = {"DDG": REPO / "projects/ddg", "Subs": REPO / "projects/submarines"}
RECORDS = {b: PROJ[b] / "workbook/extracted/nc_records_long.csv" for b in PROJ}
ENRICH = {b: PROJ[b] / "workbook/extracted/entity_naics_lookup.csv" for b in PROJ}

BUCKETS = ["structural", "machining", "castings", "piping", "electrical", "hvac", "coatings"]
UNB = "UNBUCKETED"
# NEW (Task D) scenario sets; modular handled via explicit per-entity flag.
SCEN_NEW = {"metal": {"structural", "castings", "machining"},
            "hme": {"machining", "piping", "electrical", "hvac"},
            "electrical": {"electrical"}, "broad": set(BUCKETS)}
SCEN_OLD = {"metal": {"structural", "castings", "machining"},
            "hme": {"piping", "hvac", "machining"},
            "electrical": {"electrical"},
            "modular": {"structural", "coatings"}, "broad": set(BUCKETS)}
# NAICS crosswalk WITHOUT 3364/3344 (revised)
NAICS4_NEW = {"3323": "structural", "3324": "structural", "3366": "structural", "3369": "structural",
              "3327": "machining", "3336": "machining",
              "3321": "castings", "3315": "castings", "3312": "castings",
              "3329": "piping", "3339": "piping", "4235": "piping",
              "3353": "electrical", "3359": "electrical", "3351": "electrical", "3352": "electrical",
              "3334": "hvac", "3252": "coatings", "3259": "coatings", "3262": "coatings"}
SERVICE_NAICS4 = {"5413", "5415", "5416", "5417", "5132", "6114", "4885", "4247", "2362",
                  "4236", "8113", "5418", "5614", "5612", "5419", "5611", "5621", "541", "488"}
PRIME_KEYS = ["BATH IRON WORKS", "ELECTRIC BOAT", "GENERAL DYNAMICS", "HUNTINGTON INGALLS",
              "INGALLS SHIPBUILDING", "INGALLS OPERATIONS", "NEWPORT NEWS"]
GFE_KEYS = ["LOCKHEED", "RAYTHEON", "RTX", "NORTHROP GRUMMAN SYSTEMS", "BLUEFORGE"]


def _f(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def load_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DDG_TAX = load_by_path("ddg_tax", PROJ["DDG"] / "workbook/workbook_ddg/sheets/_taxonomy.py")
SUB_TAX = load_by_path("sub_tax", PROJ["Subs"] / "workbook/workbook_submarines/sheets/taxonomy.py")


def load_enrichment():
    enr = {}
    for b in PROJ:
        with ENRICH[b].open(encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                u = (r.get("uei") or "").strip()
                if u:
                    enr[u] = (r.get("naics_4digit") or "").strip()
    return enr


def load_registry(path, only_ueis=None):
    reg = {}
    with path.open(encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            u = (r.get("uei") or "").strip()
            if not u or (only_ueis is not None and u not in only_ueis):
                continue
            role = (r.get("role") or "").strip()
            # normalize v1 vocab on the fly
            role = {"mission": "mission_systems", "mission_vls": "mission_systems",
                    "foreign": "foreign_fms"}.get(role, role)
            flags = (r.get("scenario_flags") or "")
            reg[u] = {"role": role, "bucket": (r.get("bucket") or "").strip() or UNB,
                      "modular": "modular" in flags, "vls": "vls_boundary" in flags}
    return reg


def load_records():
    """yield dict rows per book with signed $M, names, ueis, naics4."""
    enr = load_enrichment()
    out = {b: [] for b in PROJ}
    for b in PROJ:
        with RECORDS[b].open(encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                eu = (r.get("sub_entity_uei") or "").strip()
                pu = (r.get("sub_parent_uei") or "").strip()
                out[b].append({
                    "vendor": (r.get("sub_name") or "").strip(),
                    "eu": eu, "pu": pu, "naics4": enr.get(eu) or enr.get(pu) or "",
                    "desc": (r.get("description_of_requirement") or "").strip(),
                    "foreign": bool((r.get("foreign") or "").strip()),
                    "amt": _f(r.get("subAwardAmount_$")) / 1e6,
                })
    return out


# ── revised entity-grain ladder ──────────────────────────────────────────────
def classify_revised(rec, reg, vls_in=False):
    hit = reg.get(rec["eu"]) or reg.get(rec["pu"])
    if hit:
        if hit["vls"]:
            # base case: VLS launch-control excluded (mission); sensitivity-in -> electrical
            if vls_in:
                return ("supplier", "electrical", True)  # boundary launcher equipment
            return ("mission_systems", "", False)
        return (hit["role"], hit["bucket"], hit["modular"])
    up = rec["vendor"].upper()
    if any(k in up for k in PRIME_KEYS):
        return ("prime", "", False)
    if any(k in up for k in GFE_KEYS):
        return ("gfe", "", False)
    n = rec["naics4"]
    if n in NAICS4_NEW:
        return ("supplier", NAICS4_NEW[n], False)
    if n == "5511":
        return ("holding", "", False)
    if n[:3] in ("541", "488", "561") or n in SERVICE_NAICS4:
        return ("service", "", False)
    if rec["foreign"] and not n:
        return ("foreign_fms", "", False)
    return ("supplier", UNB, False)


# ── status-quo ladder (live taxonomies) ──────────────────────────────────────
def classify_status_quo(rec, book):
    if book == "DDG":
        role, bucket, _ = DDG_TAX.classify(rec["vendor"], rec["naics4"], rec["desc"])
    else:
        role, bucket, _ = SUB_TAX.classify(rec["vendor"], rec["naics4"])
    bucket = bucket or UNB
    # old modular = structural OR coatings
    return role, bucket, bucket in ("structural", "coatings")


# ── aggregation into the bridge categories ───────────────────────────────────
SUPPLIER_ROLES = {"supplier"}
PRIME_ROLES = {"prime", "co_prime", "gfe", "gfe_mib", "gfe_sib"}
MISSION_ROLES = {"mission_systems", "mission", "mission_vls"}
SERVICE_ROLES = {"service", "holding"}
FOREIGN_ROLES = {"foreign_fms", "foreign"}


def aggregate(records, classifier):
    """returns per-book dict of category $ + bucket $ + modular $."""
    res = {}
    for b in records:
        cat = defaultdict(float)
        buck = defaultdict(float)
        modular = 0.0
        total = 0.0
        for rec in records[b]:
            role, bucket, mod = classifier(rec, b)
            amt = rec["amt"]
            total += amt
            if role in SUPPLIER_ROLES:
                if bucket in BUCKETS:
                    cat["physical"] += amt
                    buck[bucket] += amt
                    if mod:
                        modular += amt
                else:
                    cat["residual"] += amt
            elif role in MISSION_ROLES:
                cat["mission"] += amt
            elif role in SERVICE_ROLES:
                cat["service_holding"] += amt
            elif role in FOREIGN_ROLES:
                cat["foreign"] += amt
            elif role in PRIME_ROLES:
                cat["prime_gfe"] += amt
            else:
                cat["residual"] += amt
        res[b] = {"total": total, "cat": dict(cat), "buck": dict(buck),
                  "modular": modular,
                  "addressable": cat["physical"] + cat["residual"]}
    return res


def scen_dollars(buck, modular, scen_sets, with_modular):
    out = {}
    for k, s in scen_sets.items():
        out[k] = sum(buck.get(x, 0.0) for x in s)
    if with_modular:
        out["modular"] = modular
    return out


# ── formatting helpers ───────────────────────────────────────────────────────
def money(x):
    return f"{x:,.0f}"


def pct(x, d):
    return f"{(100*x/d):.1f}%" if d else "-"


def print_view(title, agg, scen_sets, note=""):
    print(f"\n### {title}")
    if note:
        print(f"_{note}_\n")
    print("| Category | DDG $M | DDG % | Subs $M | Subs % |")
    print("|---|--:|--:|--:|--:|")
    rows = [("Total visible subaward flow", "total"),
            ("Physical HM&E base (bucketed supplier)", "physical"),
            ("Excluded: mission_systems", "mission"),
            ("Excluded: service / holding / IT", "service_holding"),
            ("Excluded: foreign / FMS", "foreign"),
            ("Dropped: prime / GFE", "prime_gfe"),
            ("Residual (unbucketed supplier - a FLOOR)", "residual")]
    for label, key in rows:
        if key == "total":
            d, s = agg["DDG"]["total"], agg["Subs"]["total"]
        else:
            d, s = agg["DDG"]["cat"].get(key, 0.0), agg["Subs"]["cat"].get(key, 0.0)
        print(f"| {label} | {money(d)} | {pct(d, agg['DDG']['total'])} | {money(s)} | {pct(s, agg['Subs']['total'])} |")
    # bucket table
    print("\n| Bucket | DDG $M | DDG share | Subs $M | Subs share |")
    print("|---|--:|--:|--:|--:|")
    for k in BUCKETS:
        d, s = agg["DDG"]["buck"].get(k, 0.0), agg["Subs"]["buck"].get(k, 0.0)
        print(f"| {k} | {money(d)} | {pct(d, agg['DDG']['addressable'])} | {money(s)} | {pct(s, agg['Subs']['addressable'])} |")
    # scenarios
    sd = {b: scen_dollars(agg[b]["buck"], agg[b]["modular"], scen_sets, "modular" not in scen_sets and True)
          for b in agg}
    keys = list(scen_sets.keys()) + (["modular"] if "modular" not in scen_sets else [])
    print("\n| Scenario (overlapping) | DDG $M | DDG %base | Subs $M | Subs %base |")
    print("|---|--:|--:|--:|--:|")
    for k in keys:
        d, s = sd["DDG"].get(k, 0.0), sd["Subs"].get(k, 0.0)
        print(f"| {k} | {money(d)} | {pct(d, agg['DDG']['cat'].get('physical', 0))} | {money(s)} | {pct(s, agg['Subs']['cat'].get('physical', 0))} |")


def main():
    records = load_records()
    reg_full = load_registry(REG_FULL)
    v1_ueis = {r["uei"].strip() for r in csv.DictReader(REG_V1.open(encoding="utf-8-sig"))}
    reg_v1 = load_registry(REG_FULL, only_ueis=v1_ueis)  # upgraded rows, limited to the original 45

    print("# Supplier Work-Type Bucketing - Reconciliation (Tasks E & F)")
    print(f"\nControl totals (signed): DDG ${money(sum(r['amt'] for r in records['DDG']))}M, "
          f"Subs ${money(sum(r['amt'] for r in records['Subs']))}M")

    # View 1 - status quo (live taxonomies)
    agg_sq = aggregate(records, classify_status_quo)
    print_view("View 1 - Status quo (current workbook classification logic)",
               agg_sq, SCEN_OLD,
               note="DDG = description-led record level (incl. 3364->electrical artifact); Subs = NAICS-led "
                    "(3364->electrical) applied to the signed-record universe. The live Subs workbook computes "
                    "its shares over the 150-vendor lifetime lookup; here the same logic is applied to signed "
                    "records for like-for-like comparison.")

    # View 2 - revised, VLS out (base)
    agg_base = aggregate(records, lambda rec, b: classify_revised(rec, reg_full, vls_in=False))
    print_view("View 2 - Revised physical base, VLS launch-control OUT (base case)",
               agg_base, SCEN_NEW)

    # View 3 - VLS sensitivity in
    agg_in = aggregate(records, lambda rec, b: classify_revised(rec, reg_full, vls_in=True))
    print_view("View 3 - VLS launch-control sensitivity IN (boundary launcher equipment -> electrical)",
               agg_in, SCEN_NEW)

    # View 4 - all visible flow, mission shown separately (same classification as base; full ledger)
    print("\n### View 4 - All visible yard-side flow (full ledger; mission systems shown separately)")
    print("\n| Category | DDG $M | DDG % of total | Subs $M | Subs % of total |")
    print("|---|--:|--:|--:|--:|")
    order = [("Physical HM&E base", "physical"), ("Mission systems (combat/electronics)", "mission"),
             ("Service / holding / IT", "service_holding"), ("Foreign / FMS", "foreign"),
             ("Prime / GFE", "prime_gfe"), ("Residual (unresolved supplier)", "residual")]
    for label, key in order:
        d, s = agg_base["DDG"]["cat"].get(key, 0.0), agg_base["Subs"]["cat"].get(key, 0.0)
        print(f"| {label} | {money(d)} | {pct(d, agg_base['DDG']['total'])} | {money(s)} | {pct(s, agg_base['Subs']['total'])} |")
    print(f"| **Total** | **{money(agg_base['DDG']['total'])}** | 100% | **{money(agg_base['Subs']['total'])}** | 100% |")

    # View 5 - residual before vs after tail pass
    agg_before = aggregate(records, lambda rec, b: classify_revised(rec, reg_v1, vls_in=False))
    print("\n### View 5 - Residual before vs after the tail entity-resolution pass")
    print("\n| | DDG $M | DDG % | Subs $M | Subs % |")
    print("|---|--:|--:|--:|--:|")
    for label, agg in [("Residual BEFORE tail pass (45-entity registry)", agg_before),
                       ("Residual AFTER tail pass (136-entity registry)", agg_base)]:
        d, s = agg["DDG"]["cat"].get("residual", 0.0), agg["Subs"]["cat"].get("residual", 0.0)
        print(f"| {label} | {money(d)} | {pct(d, agg['DDG']['total'])} | {money(s)} | {pct(s, agg['Subs']['total'])} |")
    dd = agg_before["DDG"]["cat"].get("residual", 0) - agg_base["DDG"]["cat"].get("residual", 0)
    ds = agg_before["Subs"]["cat"].get("residual", 0) - agg_base["Subs"]["cat"].get("residual", 0)
    print(f"| **Residual resolved by tail pass** | **{money(dd)}** | | **{money(ds)}** | |")

    # ── Task F final checks ──────────────────────────────────────────────────
    print("\n\n# Task F - Final checks")

    # F1 top-25 movers by absolute $ impact (status quo -> revised), by entity
    print("\n## F1 - Top-25 moved entities by absolute $ impact (status-quo bucket/role -> revised)")
    by_ent_sq = defaultdict(lambda: defaultdict(float))   # uei -> (role,bucket)->$
    by_ent_rv = defaultdict(lambda: defaultdict(float))
    name_of = {}
    for b in records:
        for rec in records[b]:
            u = rec["eu"] or rec["pu"] or "-"
            name_of.setdefault(u, rec["vendor"])
            r1, b1, _ = classify_status_quo(rec, b)
            r2, b2, _ = classify_revised(rec, reg_full, vls_in=False)
            by_ent_sq[u][(r1, b1 or UNB)] += rec["amt"]
            by_ent_rv[u][(r2, b2 or UNB)] += rec["amt"]
    movers = []
    for u in set(by_ent_sq) | set(by_ent_rv):
        sq = max(by_ent_sq[u].items(), key=lambda kv: kv[1], default=(("", ""), 0))
        rv = max(by_ent_rv[u].items(), key=lambda kv: kv[1], default=(("", ""), 0))
        tot = sum(by_ent_sq[u].values())
        if sq[0] != rv[0]:
            movers.append((abs(tot), u, name_of.get(u, "")[:30], sq[0], rv[0], tot))
    movers.sort(reverse=True)
    print("\n| $M | Entity | Status-quo (role/bucket) | Revised (role/bucket) |")
    print("|--:|---|---|---|")
    for amt, u, nm, sq, rv, tot in movers[:25]:
        print(f"| {money(tot)} | {nm} | {sq[0]}/{sq[1]} | {rv[0]}/{rv[1]} |")

    # F2 bucket-share bridge old -> new
    print("\n## F2 - Bucket-share bridge (old -> new), share of supplier-addressable")
    for b in records:
        print(f"\n**{b}**\n")
        print("| Bucket | Old $M | Old share | New $M | New share |")
        print("|---|--:|--:|--:|--:|")
        for k in BUCKETS:
            od, nd = agg_sq[b]["buck"].get(k, 0.0), agg_base[b]["buck"].get(k, 0.0)
            print(f"| {k} | {money(od)} | {pct(od, agg_sq[b]['addressable'])} | {money(nd)} | {pct(nd, agg_base[b]['addressable'])} |")

    # F3 residual composition after tail pass (top residual entities)
    print("\n## F3 - Residual composition after tail pass (top unresolved supplier entities)")
    resid = defaultdict(float)
    rname = {}
    for b in records:
        for rec in records[b]:
            r2, b2, _ = classify_revised(rec, reg_full, vls_in=False)
            if (r2 == "supplier" and (b2 or UNB) == UNB) or r2 == "residual":
                u = rec["eu"] or rec["pu"] or "-"
                resid[u] += rec["amt"]
                rname.setdefault(u, rec["vendor"])
    top = sorted(resid.items(), key=lambda kv: -kv[1])[:15]
    print(f"\nTotal residual = ${money(sum(resid.values()))}M across {len(resid)} entities. Top 15:\n")
    print("| $M | Entity (UEI) |")
    print("|--:|---|")
    for u, d in top:
        print(f"| {money(d)} | {rname.get(u,'')[:38]} ({u}) |")

    # F4 VLS sensitivity table
    print("\n## F4 - VLS launch-control sensitivity (out vs in)")
    print("\n| | DDG physical $M | Subs physical $M |")
    print("|---|--:|--:|")
    print(f"| Base case (VLS OUT) | {money(agg_base['DDG']['cat']['physical'])} | {money(agg_base['Subs']['cat']['physical'])} |")
    print(f"| Sensitivity (VLS IN) | {money(agg_in['DDG']['cat']['physical'])} | {money(agg_in['Subs']['cat']['physical'])} |")
    print(f"| Delta (VLS launch-control) | {money(agg_in['DDG']['cat']['physical']-agg_base['DDG']['cat']['physical'])} | {money(agg_in['Subs']['cat']['physical']-agg_base['Subs']['cat']['physical'])} |")

    # F5 TAM-vs-shares note
    print("\n## F5 - Headline TAM vs allocation shares (from Task A)")
    print("\nThe headline modeled TAM is **invariant** to reclassification. TAM = exogenous budget base "
          "(`data_scn_budget`) x a supplier coefficient computed from the **POP corpus** "
          "(`data_pop_corpus`); neither input reads the subaward role/bucket classification. "
          "Reclassification moves only the **within-TAM allocation** (bucket shares -> `model_sam_build` "
          "bucket TAM -> scenario SAM). See `model_tam_build.py` (DDG :312 / subs :254) and "
          "`model_sam_build.py` (DDG :144,180 / subs :117,141).")


if __name__ == "__main__":
    main()
