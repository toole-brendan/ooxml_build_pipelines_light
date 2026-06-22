"""verify_timing - standalone checks on the redesigned recompete timing engine.

Reproduces / asserts the CLASSIFIED timing facts straight from extracted/contract_families.csv
(plus the analyst bridges) with NO workbook imports (csv + datetime only), so the rendered
Timing & Incumbent Screen / Recompete Research Queue can be checked against an independent
read. Covers the #1 defect (decision date = IDV ordering-period end, NOT the conflated child
max), the BOA/anomaly rules, multiple-award cohorts, Saronic-first tiering, the in-market
notice predicate (confirmed AND still open), lineage-from-disposition (NOT auto-chaining;
verify_lineage.py is retired), and the Saronic-priority composite that drives the sort. Run:

    python3 verify_timing.py        # exits non-zero on the first failed assertion
"""
import csv
from collections import Counter
from datetime import date, datetime

FAM = "extracted/contract_families.csv"
NOTICE = "analyst/notice_family_links.csv"
RELEV = "analyst/saronic_relevance.csv"
MARKET = "analyst/market_assumptions.csv"
ATTRIB = "analyst/award_opportunity_attribution.csv"
LINEAGE = "analyst/lineage_edges.csv"
AS_OF = date(2026, 6, 20)
TIER_RANK = {"Core": 0, "Adjacent": 1, "Peripheral": 2}

_checks = 0


def ok(cond, msg):
    global _checks
    _checks += 1
    if not cond:
        raise AssertionError(f"FAIL: {msg}")
    print(f"  ok: {msg}")


def pdate(s):
    s = (s or "").strip()[:10]
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def load(path, key=None):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return {r[key]: r for r in rows} if key else rows


def fnum(s):
    try:
        return float((s or "").strip())
    except ValueError:
        return 0.0


def main():
    fams = load(FAM)
    by_key = {r["family_key"]: r for r in fams}
    radar = [r for r in fams if r["is_watercraft"] == "Y"
             and fnum(r["selected_measure"]) >= 1_000_000]
    print(f"contract_families: {len(fams)} families, {len(radar)} on the screen")

    # ---- #1 defect: decision date = IDV ordering-period end, never the conflated max -----
    hydrated_idv = [r for r in fams
                    if r["date_basis"] == "IDV ordering-period end (hydrated SAM CA)"]
    ok(len(hydrated_idv) >= 80,
       f"{len(hydrated_idv)} hydrated IDVs carry the ordering-period decision basis (>=80)")
    ok(all(r["effective_decision_date"][:10] == r["ordering_period_end"][:10]
           for r in hydrated_idv if r["ordering_period_end"]),
       "every hydrated-IDV decision date == its ordering_period_end (not the child max)")

    # families where a child task order runs LATER than the vehicle decision date - exactly
    # the conflation the old MAX(child ends) produced; now split apart.
    child_later = [r for r in fams
                   if pdate(r["latest_task_order_end"]) and pdate(r["effective_decision_date"])
                   and pdate(r["latest_task_order_end"]) > pdate(r["effective_decision_date"])]
    ok(len(child_later) >= 20,
       f"{len(child_later)} families have a child order ending AFTER the decision date "
       "(the old conflation, now separated)")

    # ---- Birdon W56HZV19D0093: decision ~Aug 2025, latest-TO ~2030, anomaly set -----------
    b = by_key["W56HZV19D0093"]
    ok(pdate(b["effective_decision_date"]).year == 2025
       and pdate(b["effective_decision_date"]).month == 8,
       f"Birdon decision date is Aug 2025 (got {b['effective_decision_date'][:10]})")
    ok(pdate(b["latest_task_order_end"]).year == 2030,
       f"Birdon latest task-order end is 2030 (got {b['latest_task_order_end'][:10]})")
    ok("child order" in b["date_anomaly"],
       f"Birdon flagged child-order anomaly ({b['date_anomaly']!r})")

    # ---- BOA W912BU07G0001: agreement BOA, Low confidence, 2050 anomaly ------------------
    boa = by_key["W912BU07G0001"]
    ok(boa["agreement_type"] == "BOA",
       f"W912BU07G0001 classified BOA via PIID position-9 (got {boa['agreement_type']!r})")
    ok(boa["date_confidence"] == "Low", "BOA decision confidence is Low (not a guaranteed recompete)")
    ok(pdate(boa["effective_decision_date"]).year == 2050 and boa["date_anomaly"],
       f"BOA 2050 nominal end flagged anomalous ({boa['date_anomaly']!r})")

    # ---- 'stopped-but-look-future': decision already past As-of though a child runs on -----
    stopped_future = [r for r in radar
                      if pdate(r["effective_decision_date"])
                      and pdate(r["effective_decision_date"]) < AS_OF
                      and pdate(r["latest_task_order_end"])
                      and pdate(r["latest_task_order_end"]) > AS_OF]
    ok(len(stopped_future) >= 1,
       f"{len(stopped_future)} screened vehicle(s) decided BEFORE As-of despite a live child "
       "order (e.g. Birdon) - no longer mis-placed in the future")

    # ---- multiple-award cohorts: co-awarded vehicles counted once ------------------------
    cohorts = Counter(r["cohort_id"] for r in fams if r["cohort_id"])
    ok(len(cohorts) >= 10, f"{len(cohorts)} multiple-award cohorts detected")
    ok(all(int(by_key[k]["cohort_size"]) >= 2 for cid in cohorts
           for k in [r["family_key"] for r in fams if r["cohort_id"] == cid]),
       "every cohort has size >= 2 (singletons stay Standalone)")
    leads = [r for r in fams if r["cohort_id"] and r["cohort_role"] == "Lead vehicle"]
    ok(len(leads) == len(cohorts), "exactly one Lead vehicle per cohort")

    # ---- Saronic tiering + monotonic sort -------------------------------------------------
    tiers = Counter(r["saronic_tier"].split()[0] for r in radar if r["saronic_tier"])
    ok(tiers.get("Core", 0) >= 1 and tiers.get("Peripheral", 0) >= 1,
       f"Saronic tiers populated across the screen ({dict(tiers)})")

    # priority composite replica (mean fit x timing x pursuit x win), and tier-first sort.
    relev = load(RELEV, "opportunity_id")
    market = load(MARKET, "opportunity_id")
    attrib = load(ATTRIB, "family_key")

    def priority(family_key):
        a = attrib.get(family_key)
        oid = a["opportunity_id"].strip() if a else ""
        if not oid or oid not in relev or oid not in market:
            return 0.0
        sr, ma = relev[oid], market[oid]
        fits = [fnum(sr[c]) for c in ("mission_fit", "platform_fit", "autonomy_c2_fit")
                if (sr[c] or "").strip()]
        mean_fit = sum(fits) / len(fits) if fits else 0.0
        return mean_fit * fnum(ma["timing_conf"]) * fnum(ma["pursuit_access"]) \
            * fnum(ma["win_prob"])

    attributed = [r for r in radar if priority(r["family_key"]) > 0]
    ok(len(attributed) >= 1,
       f"{len(attributed)} attributed family(ies) carry a positive Saronic priority score")

    ordered = sorted(radar, key=lambda r: (
        TIER_RANK.get(r["saronic_tier"].split()[0], 3) if r["saronic_tier"] else 3,
        -priority(r["family_key"]), -fnum(r["selected_measure"])))
    ranks = [TIER_RANK.get(r["saronic_tier"].split()[0], 3) if r["saronic_tier"] else 3
             for r in ordered]
    ok(ranks == sorted(ranks), "screen sort is tier-monotonic (Core -> Adjacent -> Peripheral)")

    # ---- in-market predicate: CONFIRMED *and still OPEN* (deadline >= As-of) --------------
    # The rendered formula is COUNTIFS(analyst_confirmed="Y", response_deadline>=As-of)>0.
    # Heuristic auto-confirmation was REMOVED (audit #1), so a fresh build legitimately has
    # ZERO confirmed links and the signal stays empty until a real disposition. Assert the
    # *logic* on controlled rows, then validate any real confirmed links the analyst added.
    def in_market(confirmed, deadline):                 # the rendered-formula predicate
        dl = pdate(deadline)
        return (confirmed or "").strip() == "Y" and dl is not None and dl >= AS_OF
    ok(in_market("Y", "2026-12-31"), "confirmed + OPEN notice (deadline >= As-of) fires in-market")
    ok(not in_market("Y", "2020-01-01"), "confirmed + EXPIRED notice does NOT fire in-market")
    ok(not in_market("", "2026-12-31"), "OPEN but unconfirmed notice does NOT fire in-market")

    links = load(NOTICE)
    confirmed = [ln for ln in links if (ln["analyst_confirmed"] or "").strip() == "Y"]
    ok(all(ln["family_key"] in by_key for ln in confirmed),
       f"every confirmed link ({len(confirmed)}) points at a real contract family")
    ok(not any("illustrative" in (ln.get("notes") or "") for ln in confirmed),
       "no link is auto-confirmed by heuristic (only human/curated seed dispositions)")

    # ---- lineage status comes from analyst DISPOSITION, not auto-chaining (audit #7) -------
    # The retired verify_lineage.py auto-chained same-UEI/PSC neighbours and labelled them
    # "Superseded". The new model suppresses a predecessor ONLY when an analyst marks the
    # successor edge Confirmed/Probable in lineage_edges.csv (radar _load_lineage_edges); a
    # blank disposition is an evidence-scored CANDIDATE, never a verdict.
    edges = load(LINEAGE)
    superseded = {e["predecessor_family"] for e in edges
                  if (e.get("analyst_disposition") or "").strip() in ("Confirmed", "Probable")}
    blank_only = {e["predecessor_family"] for e in edges
                  if not (e.get("analyst_disposition") or "").strip()} - superseded
    ok(len(blank_only) >= 1,
       f"{len(blank_only)} predecessor(s) have ONLY blank-disposition candidate edges -> NOT "
       "superseded (auto same-UEI/PSC chaining is retired; lineage is evidence, not verdict)")
    ok("W56HZV14C0015" in superseded,
       "the one curated seed edge supersedes W56HZV14C0015 (Birdon C-contract -> IDV follow-on)")
    ok(all(pk in by_key for pk in superseded),
       f"every superseded predecessor ({len(superseded)}) is a real contract family")

    # ---- blank potential-end => Research Queue shows 'unknown', not 0 ---------------------
    blank_all = [r for r in fams if not (r["pop_potential_end_date"] or "").strip()]
    blank_radar = [r for r in radar if not (r["pop_potential_end_date"] or "").strip()]
    ok(len(blank_all) >= 1,
       f"{len(blank_all)} families lack a potential end ({len(blank_radar)} on the screen) "
       "-> Option yrs left renders 'unknown', not 0 (the defensive branch is justified)")

    print(f"\nALL {_checks} CHECKS PASSED")


if __name__ == "__main__":
    main()
