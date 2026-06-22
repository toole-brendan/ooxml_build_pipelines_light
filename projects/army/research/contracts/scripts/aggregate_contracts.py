#!/usr/bin/env python3
"""AGGREGATE — flatten the raw contract pulls into the four tidy workbook CSVs,
following the funding-layer invariants (amount_type money discipline; per-row
provenance: source_system / source_id / extract_run_id / row_hash). Writes to
projects/army/workbook/extracted/ alongside the budget_* facts.

Four tables (the money-discipline boundary is the whole point):
  contract_awards.csv         one row per award (PIID/IDV/TO). Value columns are
                              DISTINCT amount_types (obligation / current_value /
                              ceiling) — never sum across them; this is a register,
                              not a fact table.
  contract_award_actions.csv  one row per modification — THE ONLY SUM-ABLE TABLE.
                              amount_type=obligation, per-mod dollars. Reconciled:
                              FPDS per-mod obligatedAmount WINS; USAspending
                              transactions fill awards FPDS didn't return.
  contract_subawards.csv      first-tier FFATA subs (SAM Stage 4). amount_type=
                              subaward — a SEPARATE money universe; never summed
                              with prime award/budget dollars.
  contract_pipeline_events.csv  pre-award notices (SAM Stage 5). No dollars; the
                              forward half of the recompete radar.

Tie-back hooks (left for the analyst bridges, not guessed here):
  * funding_tas on awards -> appropriation/PE/BLI via the budget line_item keys.
  * capability_node + program columns are emitted BLANK — the capability bridge
    (workbook/analyst/capability_nodes.csv) and the program attribution bridge fill
    them; keeping judgment out of the mechanical aggregate is invariant #2.

Run after Stages 2 (+3 for authoritative actions; 4/5 optional). Idempotent.
"""
from __future__ import annotations

import csv
import datetime
import glob
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as C            # noqa: E402  (canonical materiality + scope + lineage rules)
import mapping_rules as MR    # noqa: E402  (watercraft relevance + customer segment)

ROOT = Path(__file__).resolve().parents[1]                 # research/contracts/
EXTRACT = ROOT / "extracted"
USASPENDING_RAW = ROOT / "usaspending_raw"
FPDS_RAW = ROOT / "fpds_raw"
SAM_SUB = ROOT / "sam_subawards"
CA_AGG_INDEX = EXTRACT / "_contract_awards_agg_index.json"   # Stage 7 hydration index
OUT = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/army/workbook/extracted")
ANALYST = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/army/workbook/analyst")
RUN_ID = "army-contracts-aggregate-2026-06-20"
DOLLARS_BASIS = "then_year"
ASOF_DATE = C.AS_OF                                          # model as-of (data snapshot)


def safe(gid: str) -> str:
    return "".join(c if (c.isalnum() or c in "._-") else "_" for c in gid)


def rhash(*parts) -> str:
    return hashlib.blake2b("|".join("" if p is None else str(p) for p in parts).encode(),
                           digest_size=8).hexdigest()


def dod_fy(date_str):
    if not date_str or len(date_str) < 7:
        return None
    try:
        y, m = int(date_str[:4]), int(date_str[5:7])
    except ValueError:
        return None
    return y + 1 if m >= 10 else y


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def write_csv(path, cols, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ---------- load FPDS per-mod actions, keyed by (piid, referenced_idv_piid) ----------
def load_fpds_actions():
    by_key = {}
    for fp in glob.glob(str(FPDS_RAW / "*.json")):
        if Path(fp).name.startswith("_"):
            continue
        try:
            doc = json.loads(Path(fp).read_text())
        except Exception:
            continue
        for r in doc.get("records", []):
            key = (r.get("piid"), r.get("referenced_idv_piid") or None)
            by_key.setdefault(key, []).append(r)
    return by_key


def to_ord(date_str):
    s = (date_str or "").strip()[:10]
    try:
        return datetime.date.fromisoformat(s).toordinal()
    except ValueError:
        return None


def fam_key(piid, parent_idv):
    return (parent_idv or "").strip() or (piid or "").strip()


def office_of(piid):
    """DoD contracting-office DODAAC = first 6 chars of the PIID (W56HZV, W912BU, ...)."""
    p = (piid or "").strip()
    return p[:6] if len(p) >= 6 else p


def seg_for(psc, naics, piid, recipient, desc):
    return MR.customer_segment(psc, naics, office_of(piid), recipient, desc, "")


def load_ca_agg():
    """Stage-7 SAM Contract Awards aggregation index, keyed by piid (the family key)."""
    if not CA_AGG_INDEX.exists():
        return {}
    out = {}
    for d in json.loads(CA_AGG_INDEX.read_text()):
        if d.get("piid"):
            out[d["piid"]] = d
    return out


def synthesize_idv_rows(award_rows, ca_agg):
    """Hydrate orphan parent IDVs (review #4): a parent_idv_piid referenced by a task
    order but absent as its own Contract Awards record gets a SYNTHESIZED award row from
    the SAM Contract Awards API so the live MAXIFS over pop_*_end_date resolves the
    vehicle's ordering-period end + ceiling. Obligation is 0 (IDVs obligate via their DOs;
    the $ already live on the DO rows) so the family obligation never double-counts."""
    existing_piids = {r["piid"] for r in award_rows}
    referenced_parents = {(r.get("parent_idv_piid") or "").strip()
                          for r in award_rows if (r.get("parent_idv_piid") or "").strip()}
    orphans = sorted(p for p in referenced_parents if p not in existing_piids)
    synth = []
    for p in orphans:
        a = ca_agg.get(p)
        if not a or not a.get("ordering_period_end"):
            continue                      # below pull floor / not in CA API -> leave blank
        order_end = a.get("ordering_period_end")
        synth.append({
            "award_id": f"SAMCA_{p}", "piid": p, "parent_idv_piid": "",
            "idv_type": "IDV (hydrated)", "single_or_multiple_award": None,
            "award_type": None, "award_type_description": None, "category": "idv",
            "recipient_name": a.get("recipient"), "recipient_uei": None,
            "parent_recipient_name": None,
            "obligation_amount": 0.0,                       # IDV obligates via its DOs
            "current_value": None, "ceiling_value": a.get("ceiling_value"),
            "total_outlay": None, "subaward_count": None, "total_subaward_amount": None,
            "date_signed": a.get("date_signed"), "pop_start_date": a.get("pop_start_date"),
            "pop_current_end_date": order_end,             # ordering-period end = vehicle end
            "pop_potential_end_date": a.get("ultimate_completion_date") or order_end,
            "first_action_date": None, "last_action_date": None,
            "extent_competed": None, "extent_competed_description": None,
            "solicitation_procedures": None, "fair_opportunity_limited": None,
            "number_of_offers": None,
            "naics_code": None, "naics_description": None,
            "psc_code": None, "psc_description": None,
            "funding_tas": "", "funding_account_titles": "", "has_tas": None,
            "matched_axes": "idv-hydration",
            "actions_source": "sam_contract_awards",
            "customer_segment": "",
            "program": "", "capability_node": "",
            "dollars_basis": DOLLARS_BASIS,
            "source_system": "sam_contract_awards", "source_id": "SAM-CA-AGG",
            "hydrated": "Y",
            "extract_run_id": RUN_ID,
            "row_hash": rhash(f"SAMCA_{p}", order_end, a.get("ceiling_value")),
        })
    return synth


def _effective_decision(agreement, is_idv, order_end, own_end, cur_end_max):
    """The vehicle RECOMPETE date + its basis + confidence (review #2/#3 - the #1 defect).

    The recompete is when the government loses authority to place new orders - NOT the
    conflated MAX of child task-order performance ends. IDV: prefer the hydrated SAM CA
    ordering-period end, else the vehicle's own base-record PoP end, else (flagged Low) the
    child max. BOA/BPA are master agreements (FAR 16.703/16.702): the nominal end is not a
    guaranteed recompete -> lower confidence. Standalone: its own contract PoP end."""
    if agreement == "BOA":
        return (order_end or own_end or cur_end_max,
                "BOA nominal end - NOT a guaranteed recompete (master agreement)", "Low")
    if agreement == "BPA":
        return (order_end or own_end or cur_end_max,
                "BPA call-period end - orders may continue under the parent schedule", "Medium")
    if is_idv:
        if order_end:
            return order_end, "IDV ordering-period end (hydrated SAM CA)", "High"
        if own_end:
            return own_end, "IDV base-record PoP end (no hydrated ordering end)", "Medium"
        return cur_end_max, "IDV fallback: latest child PoP end (no vehicle end on record)", "Low"
    if cur_end_max:
        return cur_end_max, "Standalone contract PoP end", "High"
    return None, "No PoP end on record", "Low"


def _date_anomaly(eff_date, ceiling, vehicle_end, latest_to_end):
    """Flag implausible timing/ceiling inputs (review #3): a decision date far past the
    horizon (the 2050 BOA W912BU07G0001), an absurd ceiling, or a child order running years
    past the vehicle end (the Birdon ordering-end-vs-2030 case). Empty when clean."""
    flags = []
    horizon = (to_ord(ASOF_DATE) or 0) + int(C.DATE_HORIZON_YEARS * 365.25)
    eo = to_ord(eff_date)
    if eo and eo > horizon:
        flags.append(f"decision date {str(eff_date)[:4]} > As-of+{C.DATE_HORIZON_YEARS}y")
    cv = fnum(ceiling)
    if cv and cv > C.CEILING_ANOMALY:
        flags.append("ceiling > $50B")
    ve, lo = to_ord(vehicle_end), to_ord(latest_to_end)
    if ve and lo and (lo - ve) > C.CHILD_LAG_ANOMALY_DAYS:
        flags.append("child order ends >5y after vehicle end")
    return "; ".join(flags)


def build_award_cohorts(families):
    """Group co-awarded vehicles into MULTIPLE-AWARD cohorts (review #1: a real opportunity
    hierarchy). Vehicles sharing a contracting office + PoP-start window + ordering-end
    window + PSC under one MULTIPLE-AWARD requirement are ONE opportunity (count once), not
    N independent recompetes. SINGLE-award / blank families are NEVER clustered (the
    over-merge guard). Returns {family_key: (cohort_id, cohort_size, cohort_role)}."""
    eligible = [f for f in families
                if f.get("is_multiple_award") == "Y" and f["is_watercraft"] == "Y"
                and f["contracting_office"] and f["psc_code"] and f["pop_start_date"]]
    buckets = defaultdict(list)
    for f in eligible:
        sb = (to_ord(f["pop_start_date"]) or 0) // C.COHORT_START_WINDOW_DAYS
        oe = to_ord(f.get("ordering_period_end"))
        ob = (oe // C.COHORT_ORDEND_WINDOW_DAYS) if oe else "noend"
        buckets[(f["contracting_office"], f["psc_code"], sb, ob)].append(f)
    # Iterate buckets in a deterministic order so cohort ids are stable across runs.
    cohorts = sorted(((k, m) for k, m in buckets.items() if len(m) >= 2),
                     key=lambda km: (km[0][0], km[0][1], km[0][2], str(km[0][3])))
    out = {}
    label_seen = Counter()
    for (office, psc, _sb, _ob), members in cohorts:
        members.sort(key=lambda f: (-(f["selected_measure"] or 0), f["family_key"]))
        base = f"COH-{office}-{psc}-{(members[0]['pop_start_date'] or '')[:4]}"
        # Two cohorts can share that base (same office/PSC/start-year, different ordering-end
        # window); suffix the 2nd+ so every cohort_id is UNIQUE (count-once integrity).
        label_seen[base] += 1
        cid = base if label_seen[base] == 1 else f"{base}-{label_seen[base]}"
        for i, f in enumerate(members):
            out[f["family_key"]] = (cid, len(members),
                                    "Lead vehicle" if i == 0 else "Co-awarded vehicle")
    return out


def build_families(award_rows, action_rows, ca_agg):
    """Canonical per-family fact table (review: single selected measure + reconciliation).

    One row per contract family (key = parent_idv_piid else piid). Carries BOTH the
    award-reported cumulative obligation AND the reconstructed per-mod action sum, their
    coverage ratio/status, the SAM CA third-lens total, the hydrated vehicle dates, and a
    SINGLE selected measure (action sum when coverage is complete, else award-level with
    an explicit fallback flag) used downstream for the materiality floor + ranking."""
    aw_by_fam = defaultdict(list)
    for r in award_rows:
        aw_by_fam[fam_key(r["piid"], r.get("parent_idv_piid"))].append(r)
    ac_by_fam = defaultdict(list)
    for r in action_rows:
        ac_by_fam[fam_key(r["piid"], r.get("parent_idv_piid"))].append(r)

    fams = []
    for key, aws in aw_by_fam.items():
        acts = ac_by_fam.get(key, [])
        dom = max(aws, key=lambda r: (fnum(r.get("obligation_amount")) or 0.0))
        award_obl = sum(fnum(r.get("obligation_amount")) or 0.0 for r in aws)
        action_sum = sum(fnum(r.get("amount")) or 0.0 for r in acts)
        adates = sorted(a["action_date"][:10] for a in acts if a.get("action_date"))
        starts = [r["pop_start_date"][:10] for r in aws if r.get("pop_start_date")]
        curs = [r["pop_current_end_date"][:10] for r in aws if r.get("pop_current_end_date")]
        pots = [r["pop_potential_end_date"][:10] for r in aws if r.get("pop_potential_end_date")]
        agg = ca_agg.get(key, {})

        ratio = (action_sum / award_obl) if award_obl > 0 else None
        if not acts:
            status = "no-actions"
        elif action_sum < 0:
            status = "negative"
        elif ratio is None:
            status = "no-award-$"
        elif C.COVERAGE_COMPLETE_LO <= ratio <= C.COVERAGE_COMPLETE_HI:
            status = "complete"
        elif ratio < C.COVERAGE_COMPLETE_LO:
            status = "partial"
        else:
            status = "over"
        if award_obl > 0 and status == "complete":
            selected, basis = action_sum, "action"
        elif award_obl > 0:
            selected, basis = award_obl, "award (fallback)"
        else:
            selected, basis = max(action_sum, 0.0), "action (no award $)"

        is_idv = any((r.get("parent_idv_piid") or "").strip() == key for r in award_rows)
        relevance = MR.watercraft_relevance(
            dom.get("psc_code"), dom.get("naics_code"), dom.get("recipient_name"),
            dom.get("naics_description"), dom.get("psc_description"))

        # ---- agreement type + award structure (from the family's OWN base record, not the
        # dominant award - which is usually a child order carrying the obligation) --------
        base_rows = [r for r in aws if (r.get("piid") or "").strip() == key]
        idv_raw = next((r.get("idv_type") for r in base_rows if (r.get("idv_type") or "").strip()),
                       None)
        if not idv_raw:
            cnt = Counter((r.get("idv_type") or "").strip() for r in aws
                          if (r.get("idv_type") or "").strip())
            idv_raw = cnt.most_common(1)[0][0] if cnt else ""
        agreement = MR.agreement_type(idv_raw, is_idv, key)
        award_structure = next(
            (r.get("single_or_multiple_award") for r in base_rows
             if (r.get("single_or_multiple_award") or "").strip()),
            dom.get("single_or_multiple_award")) or ""
        is_multiple = any((r.get("single_or_multiple_award") or "").strip().upper()
                          == "MULTIPLE AWARD" for r in aws)

        # ---- effective decision date (review #2): split current-PoP ends into the
        # vehicle's OWN base record vs child task orders, so the recompete is the vehicle
        # authority end, NEVER the conflated MAX of child performance ends ---------------
        child_curs = [r["pop_current_end_date"][:10] for r in aws
                      if (r.get("parent_idv_piid") or "").strip() == key
                      and r.get("pop_current_end_date")]
        own_curs = [r["pop_current_end_date"][:10] for r in aws
                    if (r.get("parent_idv_piid") or "").strip() != key
                    and r.get("pop_current_end_date")]
        latest_to_end = max(child_curs) if child_curs else None
        own_end = max(own_curs) if own_curs else None
        cur_end_max = max(curs) if curs else None        # conflated max (kept for provenance)
        order_end = agg.get("ordering_period_end")
        eff_date, date_basis, date_conf = _effective_decision(
            agreement, is_idv, order_end, own_end, cur_end_max)
        date_anomaly = _date_anomaly(eff_date, agg.get("ceiling_value"),
                                     own_end or order_end, latest_to_end)
        segment = seg_for(dom.get("psc_code"), dom.get("naics_code"), key,
                          dom.get("recipient_name"), dom.get("psc_description"))

        fams.append({
            "family_key": key,
            "vehicle_type": "IDV vehicle" if is_idv else "Standalone",
            "agreement_type": agreement,
            "single_or_multiple_award": award_structure,
            "is_multiple_award": "Y" if is_multiple else "N",
            "cohort_id": "",            # <- back-filled by build_award_cohorts in main()
            "cohort_size": 1,
            "cohort_role": "Standalone",
            "incumbent": dom.get("recipient_name"),
            "recipient_uei": dom.get("recipient_uei"),
            "contracting_office": office_of(key),
            "psc_code": dom.get("psc_code"), "naics_code": dom.get("naics_code"),
            "extent_competed": dom.get("extent_competed_description") or dom.get("extent_competed"),
            "relevance_basis": relevance or "",
            "is_watercraft": "Y" if relevance else "N",
            "customer_segment": segment,
            "saronic_tier": MR.saronic_tier(segment),
            "n_awards": len(aws),
            "n_task_orders": sum(1 for r in award_rows
                                 if (r.get("parent_idv_piid") or "").strip() == key),
            "action_count": len(acts),
            "award_reported_obligation": round(award_obl, 2),
            "reconstructed_action_sum": round(action_sum, 2),
            "sam_family_obligated": agg.get("sam_family_obligated"),
            "coverage_ratio": round(ratio, 4) if ratio is not None else None,
            "coverage_status": status,
            "selected_measure": round(selected, 2),
            "materiality_basis": basis,
            "first_action_date": adates[0] if adates else None,
            "last_action_date": adates[-1] if adates else None,
            "pop_start_date": min(starts) if starts else None,
            "pop_current_end_date": max(curs) if curs else None,
            "pop_potential_end_date": max(pots) if pots else None,
            "ordering_period_end": agg.get("ordering_period_end"),
            "ceiling_value": agg.get("ceiling_value"),
            "effective_decision_date": eff_date,
            "date_basis": date_basis,
            "date_confidence": date_conf,
            "latest_task_order_end": latest_to_end,
            "date_anomaly": date_anomaly,
            "hydrated": "Y" if any(r.get("hydrated") == "Y" for r in aws) else "N",
            "extract_run_id": RUN_ID,
            "row_hash": rhash(key, round(selected, 2), status),
        })
    fams.sort(key=lambda d: -(d["selected_measure"] or 0))
    return fams


def _read_existing_dispositions(path):
    """Preserve analyst lineage dispositions across re-runs, keyed by (pred, succ)."""
    keep = {}
    if path.exists():
        for r in csv.DictReader(open(path)):
            keep[(r.get("predecessor_family"), r.get("successor_family"))] = (
                r.get("analyst_disposition") or "", r.get("review_date") or "",
                r.get("notes") or "")
    return keep


# Validated chains seeded as Confirmed on a FIRST generation only (army lineage log);
# analyst edits in the CSV win on re-run via _read_existing_dispositions.
SEED_DISPOSITIONS = {
    ("W56HZV14C0015", "W56HZV19D0093"): ("Confirmed",
        "seed: validated Birdon C-contract -> IDV follow-on (lineage_detection log)"),
}

# One illustrative CONFIRMED notice<->vehicle link so the Notice Links sheet + the radar's
# In-market signal are non-empty on a fresh build (review #4: the award_number-only signal
# never fires). Keyed by (notice_id, family_key); applied only when analyst_confirmed is
# blank, so a real analyst confirmation/rejection always wins. The aggregate prints the
# top open links each run - swap this for whatever the analyst validates.
SEED_NOTICE_CONFIRMATIONS = {
    # (notice_id, family_key): "Y"   -- populated from the highest-scored open link below.
}


def build_lineage_edges(families):
    """Scored predecessor->successor CANDIDATES (review #5: an evidence score, not a
    verdict). Same-incumbent (UEI) + same-PSC chaining within the temporal window, each
    edge carrying similarity signals + an evidence_score + a blank analyst_disposition.
    Different-vendor successors are Phase 4. Only Confirmed/Probable suppress a
    predecessor downstream - so an UNREVIEWED expired vehicle reads 'Expired - successor
    unresolved', never a definitive 'Superseded'."""
    wc = [f for f in families if f["is_watercraft"] == "Y"
          and f["recipient_uei"] and f["psc_code"]
          and f["pop_start_date"] and f["pop_current_end_date"]]
    groups = defaultdict(list)
    for f in wc:
        groups[(f["recipient_uei"], f["psc_code"])].append(f)

    prior = _read_existing_dispositions(ANALYST / "lineage_edges.csv")
    edges = []
    seen = set()
    for members in groups.values():
        members.sort(key=lambda f: (to_ord(f["pop_start_date"]) or 0,
                                    to_ord(f["pop_current_end_date"]) or 0))
        for i, A in enumerate(members):
            a_end = to_ord(A["pop_current_end_date"])
            best, best_gap = None, None
            for B in members[i + 1:]:
                gap = (to_ord(B["pop_start_date"]) or 0) - (a_end or 0)
                if -C.OVERLAP_DAYS <= gap <= C.GAP_CAP_DAYS:
                    if best_gap is None or abs(gap) < abs(best_gap):
                        best, best_gap = B, gap
            if best is None:
                continue
            pk, sk = A["family_key"], best["family_key"]
            if (pk, sk) in seen:
                continue
            seen.add((pk, sk))
            naics_match = bool(A["naics_code"]) and A["naics_code"] == best["naics_code"]
            office_match = A["contracting_office"] == best["contracting_office"]
            prox = max(0.0, 1.0 - abs(best_gap) / C.GAP_CAP_DAYS)
            score = round(0.40 + 0.30 + (0.15 if naics_match else 0.0) + 0.15 * prox, 3)
            disp, rev, notes = prior.get((pk, sk), ("", "", ""))
            if not disp and (pk, sk) in SEED_DISPOSITIONS:
                disp, notes = SEED_DISPOSITIONS[(pk, sk)]
            edges.append({
                "predecessor_family": pk, "successor_family": sk,
                "same_incumbent": "Y",
                "predecessor_incumbent": A["incumbent"], "successor_incumbent": best["incumbent"],
                "psc_match": "Y", "naics_match": "Y" if naics_match else "N",
                "contracting_office_match": "Y" if office_match else "N",
                "temporal_gap_days": best_gap, "evidence_score": score,
                "analyst_disposition": disp, "review_date": rev, "notes": notes,
                "source": "seed-heuristic",
            })
    edges.sort(key=lambda e: -e["evidence_score"])
    return edges


def write_source_clocks():
    """Per-source data-through dates + reporting-lag notes (review: source modernization).
    Renders on the QA/Overview sheet (Phase 3); persisted here so the data exists now."""
    rows = [
        ("data_snapshot", ASOF_DATE, "", "Date the source data was pulled (a fixed fact about "
         "this build). The EDITABLE model clock is a separate live cell - Timing & Incumbent "
         "Screen $C$6 - which re-clocks every expiry column; see Overview > Model As-of date."),
        ("budget_vintage", "FY2022-FY2027 PB books", "", "Then-year $; 51-book corpus."),
        ("usaspending_awards", "2026-06-20", "~1-2 wk", "Discovery+detail snapshot date."),
        ("usaspending_actions", "2026-06-20", "~1-2 wk", "Per-mod transactions (sum-able)."),
        ("fpds_actions", "2026-06-20", "varies", "Atom feed; authoritative per-mod obligations."),
        ("sam_subawards", "2026-06-20", "6-18 mo", "FFATA first-tier; lags primes."),
        ("sam_opportunities", "2026-06-20", "n/a", "Trailing-363-day active pull."),
        ("sam_contract_awards", "2026-06-20", "DoD 90-day", "REVEALED only: DoD awards signed "
         "<90 days are EXCLUDED (non-federal key). Used for parent-IDV hydration + a "
         "third-lens family total, not as ground truth for obligations."),
    ]
    write_csv(OUT / "source_clocks.csv",
              ["source", "data_through_date", "reporting_lag", "note"],
              [{"source": s, "data_through_date": d, "reporting_lag": l, "note": n}
               for s, d, l, n in rows])


def collapse_pipeline_lifecycle(notices):
    """Collapse per-notice SAM events into ONE row per solicitation lifecycle (review #6):
    a solicitation's amendments + award notice are the SAME opportunity, not separate
    'events' (e.g. W912CH25RA007 posts 20 notices). Keeps first/latest posted, the current
    stage (latest notice type) + deadline, the ultimate award PIID, and an amendment count.
    The raw per-notice records stay in _opportunities_index.json (the audit trail)."""
    groups = defaultdict(list)
    loose = []
    for o in notices:
        sol = (o.get("solicitation_number") or "").strip()
        (groups[sol] if sol else loose).append(o)

    def d10(r, k):
        return (r.get(k) or "")[:10]

    out = []
    for sol, members in groups.items():
        members.sort(key=lambda r: d10(r, "posted_date"))
        latest = members[-1]
        awd = next((m.get("award_number") for m in reversed(members)
                    if (m.get("award_number") or "").strip()), "")
        out.append({
            "notice_id": latest.get("notice_id"), "title": latest.get("title"),
            "solicitation_number": sol, "notice_type": latest.get("notice_type"),
            "base_type": latest.get("base_type"),
            "first_posted_date": d10(members[0], "posted_date"),
            "posted_date": latest.get("posted_date"), "n_notices": len(members),
            "fiscal_year": dod_fy(latest.get("posted_date")),
            "response_deadline": latest.get("response_deadline"),
            "naics_code": latest.get("naics_code"), "psc_code": latest.get("psc_code"),
            "set_aside": latest.get("set_aside"), "department": latest.get("department"),
            "award_number": awd, "matched_term": latest.get("matched_term"),
            "customer_segment": latest.get("customer_segment"), "capability_node": "",
            "source_system": "sam_opportunities", "source_id": "SAM-OPPORTUNITY-LIFECYCLE",
            "extract_run_id": RUN_ID, "row_hash": rhash("LC", sol),
        })
    for o in loose:                               # no solicitation number -> own lifecycle
        out.append({
            "notice_id": o.get("notice_id"), "title": o.get("title"),
            "solicitation_number": "", "notice_type": o.get("notice_type"),
            "base_type": o.get("base_type"), "first_posted_date": d10(o, "posted_date"),
            "posted_date": o.get("posted_date"), "n_notices": 1,
            "fiscal_year": o.get("fiscal_year"), "response_deadline": o.get("response_deadline"),
            "naics_code": o.get("naics_code"), "psc_code": o.get("psc_code"),
            "set_aside": o.get("set_aside"), "department": o.get("department"),
            "award_number": o.get("award_number"), "matched_term": o.get("matched_term"),
            "customer_segment": o.get("customer_segment"), "capability_node": "",
            "source_system": "sam_opportunities", "source_id": "SAM-OPPORTUNITY-LIFECYCLE",
            "extract_run_id": RUN_ID, "row_hash": rhash("LC", o.get("notice_id")),
        })
    return out


def seed_if_absent(path, cols, rows):
    """Write a durable analyst table ONCE. Never clobbers analyst edits on re-run."""
    if path.exists():
        return False
    write_csv(path, cols, rows)
    return True


def ensure_columns(path, cols):
    """Add any MISSING columns to an existing analyst CSV, preserving every existing value
    (so a schema addition doesn't require delete-to-regen and can't lose analyst edits).
    No-op if the file is absent (seed_if_absent will create it with the full schema) or
    already has all columns. New columns are appended blank."""
    if not path.exists():
        return False
    with open(path, newline="") as f:
        rdr = csv.DictReader(f)
        old_cols = rdr.fieldnames or []
        rows = list(rdr)
    missing = [c for c in cols if c not in old_cols]
    if not missing:
        return False
    new_cols = old_cols + missing
    for r in rows:
        for c in missing:
            r.setdefault(c, "")
    write_csv(path, new_cols, rows)
    return True


def reseed_if_seed_only(path, cols, rows):
    """Rewrite a SEED-only analyst table with a new schema/seed. Overwrites ONLY when the
    existing file is entirely source=seed (no analyst edits to lose); otherwise leaves it
    untouched. Used to upgrade the customer_org_map schema in place without clobbering a
    real analyst account map."""
    if path.exists():
        with open(path, newline="") as f:
            existing = list(csv.DictReader(f))
        if any((r.get("source") or "").strip() != "seed" for r in existing):
            return False                              # has analyst edits -> never clobber
    write_csv(path, cols, rows)
    return True


def build_notice_family_links(pipe_rows, families):
    """Candidate notice<->vehicle links (review #6): for each OPEN notice, watercraft
    families that share its PSC (and, when known, its contracting office) - scored, with
    a blank analyst confirmation preserved across re-runs. One notice may map to 0/1/many
    families. The award_number-only signal misses ~42% of notices; this is the richer net."""
    prior = {}
    p = ANALYST / "notice_family_links.csv"
    if p.exists():
        for r in csv.DictReader(open(p)):
            prior[(r.get("notice_id"), r.get("family_key"))] = (
                r.get("analyst_confirmed") or "", r.get("notes") or "")
    wc = [f for f in families if f["is_watercraft"] == "Y" and f["psc_code"]]
    by_psc = defaultdict(list)
    for f in wc:
        by_psc[f["psc_code"]].append(f)
    asof = ASOF_DATE
    links = []
    for o in pipe_rows:
        dl = (o.get("response_deadline") or "")[:10]
        if not (dl and dl >= asof):          # OPEN notices only (the forward signal)
            continue
        psc = (o.get("psc_code") or "").strip()
        noff = office_of(o.get("solicitation_number"))
        for f in by_psc.get(psc, []):
            office_match = bool(noff) and noff == f["contracting_office"]
            score = round(0.5 + (0.3 if office_match else 0.0)
                          + (0.2 if (o.get("naics_code") and o["naics_code"] == f["naics_code"]) else 0.0), 3)
            conf, notes = prior.get((o.get("notice_id"), f["family_key"]), ("", ""))
            if not conf and (o.get("notice_id"), f["family_key"]) in SEED_NOTICE_CONFIRMATIONS:
                conf = SEED_NOTICE_CONFIRMATIONS[(o.get("notice_id"), f["family_key"])]
                notes = notes or "seed: illustrative confirmed link"
            links.append({
                "notice_id": o.get("notice_id"), "solicitation_number": o.get("solicitation_number"),
                "notice_title": o.get("title"), "family_key": f["family_key"],
                "family_incumbent": f["incumbent"], "psc_match": "Y",
                "naics_match": "Y" if (o.get("naics_code") and o["naics_code"] == f["naics_code"]) else "N",
                "contracting_office_match": "Y" if office_match else "N",
                "response_deadline": dl, "evidence_score": score,
                "analyst_confirmed": conf, "notes": notes, "source": "seed-heuristic",
            })
    links.sort(key=lambda e: -e["evidence_score"])
    # NO heuristic auto-confirmation: analyst_confirmed is set ONLY by a human (preserved via
    # `prior`) or by the explicit, curated SEED_NOTICE_CONFIRMATIONS map above. A top-scored
    # candidate must never populate a production "confirmed" field on its own (audit #1) - the
    # In-market signal stays empty until a real disposition, which is the honest default.
    return links


def seed_analyst_tables(families):
    """Create the durable analyst BRIDGE schemas (system of record OUTSIDE the xlsx, so a
    rebuild can't wipe judgments - review #7). Seeded ONCE with a few illustrative rows
    flagged 'seed'; the real analyst pass + Phase-2 wiring populate them. Saronic product
    routes live here (work_package_saronic_route), editable - never hardcoded in code."""
    # recompete_reviews: the durable home of the radar/calendar blue judgment columns,
    # keyed by family_key (seed a blank row per >= $1M watercraft family).
    # planned_* milestones let the analyst record REAL capture/solicitation/award dates that
    # override the calendar's decision-lead estimates (the 90-day notice-by is far too late
    # to BEGIN capture); capture_lead_override_days overrides CAPTURE_LEAD_DAYS per row.
    rr_cols = ["family_key", "window_override", "confidence", "pursuit_access",
               "program", "capability_node",
               "planned_rfi_date", "planned_solicitation_date", "planned_award_date",
               "capture_lead_override_days", "milestone_source", "notes", "review_date"]
    rr_rows = [{"family_key": f["family_key"]}
               for f in families
               if f["is_watercraft"] == "Y" and (f["selected_measure"] or 0) >= C.MIN_OBLIG]
    if not seed_if_absent(ANALYST / "recompete_reviews.csv", rr_cols, rr_rows):
        ensure_columns(ANALYST / "recompete_reviews.csv", rr_cols)   # add new milestone cols

    seed_if_absent(ANALYST / "opportunities.csv",
        ["opportunity_id", "name", "customer_segment", "program", "mission",
         "primary_capability_node", "status", "confidence", "notes", "source"],
        [{"opportunity_id": "OPP-MSVL", "name": "Maneuver Support Vessel (Light) - MSV(L)",
          "customer_segment": C.SEG_ARMY_OPS, "program": "MSV(L)",
          "mission": "Contested distribution / operational maneuver",
          "primary_capability_node": "PLATFORM", "status": "active", "confidence": "Strong",
          "notes": "seed: budget BLI 8211R01001 + Vigor/Birdon contract families", "source": "seed"},
         {"opportunity_id": "OPP-ESP", "name": "Army Watercraft Extended Service Program (ESP)",
          "customer_segment": C.SEG_MRO, "program": "Army Watercraft ESP",
          "mission": "Fleet modernization / SLEP", "primary_capability_node": "PLATFORM",
          "status": "active", "confidence": "Strong",
          "notes": "seed: budget BLI 3569M11101 (LCU/LSV/MCS SLEP, MIBS, HCCC)", "source": "seed"},
         {"opportunity_id": "OPP-AWS-AUTONOMY",
          "name": "Army Watercraft Systems autonomy / C2 (Project 526)",
          "customer_segment": C.SEG_ARMY_RDTE, "program": "PE 0603804A / Project 526",
          "mission": "Autonomy / assured PNT / mission C2",
          "primary_capability_node": "C2", "status": "watch", "confidence": "Inferred",
          "notes": "seed: RDT&E line; Saronic Echelon route", "source": "seed"}])

    seed_if_absent(ANALYST / "budget_opportunity_attribution.csv",
        ["line_item_id", "opportunity_id", "addressable_content_pct", "relationship_type",
         "rationale", "source"],
        [{"line_item_id": "8211R01001", "opportunity_id": "OPP-MSVL",
          "addressable_content_pct": "", "relationship_type": "Direct",
          "rationale": "seed: MSV(L) procurement BLI -> MSV(L) opportunity", "source": "seed"},
         {"line_item_id": "3569M11101", "opportunity_id": "OPP-ESP",
          "addressable_content_pct": "", "relationship_type": "Direct",
          "rationale": "seed: ESP procurement BLI -> ESP opportunity", "source": "seed"},
         {"line_item_id": "RDTE-0603804A-526", "opportunity_id": "OPP-AWS-AUTONOMY",
          "addressable_content_pct": "", "relationship_type": "Enabling",
          "rationale": "seed: Project 526 marine S&T -> autonomy/C2", "source": "seed"}])

    seed_if_absent(ANALYST / "award_opportunity_attribution.csv",
        ["family_key", "opportunity_id", "addressable_content_pct", "relationship_type",
         "rationale", "source"],
        [{"family_key": "W56HZV17D0086", "opportunity_id": "OPP-MSVL",
          "addressable_content_pct": "", "relationship_type": "Direct",
          "rationale": "seed: Vigor MSV(L) construction IDV", "source": "seed"}])

    seed_if_absent(ANALYST / "work_packages.csv",
        ["work_package_id", "opportunity_id", "name", "capability_node",
         "addressable_content_pct", "notes", "source"],
        [{"work_package_id": "WP-MSVL-HULL", "opportunity_id": "OPP-MSVL",
          "name": "MSV(L) hull / platform new-construction", "capability_node": "PLATFORM",
          "addressable_content_pct": "", "notes": "seed", "source": "seed"},
         {"work_package_id": "WP-MSVL-AUTON", "opportunity_id": "OPP-MSVL",
          "name": "MSV(L) autonomy / mission C2 integration", "capability_node": "C2",
          "addressable_content_pct": "", "notes": "seed", "source": "seed"}])

    seed_if_absent(ANALYST / "work_package_capability.csv",
        ["work_package_id", "node_id", "relationship_type", "importance",
         "fit_rating", "gap_severity", "partner_dependency", "notes", "source"],
        [{"work_package_id": "WP-MSVL-HULL", "node_id": "PLATFORM",
          "relationship_type": "Company Capability", "importance": "High",
          "fit_rating": "", "gap_severity": "", "partner_dependency": "", "notes": "seed",
          "source": "seed"},
         {"work_package_id": "WP-MSVL-AUTON", "node_id": "C2",
          "relationship_type": "Company Capability", "importance": "High",
          "fit_rating": "", "gap_severity": "", "partner_dependency": "", "notes": "seed",
          "source": "seed"}])

    # Saronic commercial routes (decision #2: editable analyst input, NOT hardcoded).
    seed_if_absent(ANALYST / "work_package_saronic_route.csv",
        ["work_package_id", "saronic_route", "route_kind", "fit_pct", "win_prob",
         "partner_strategy", "notes", "source"],
        [{"work_package_id": "WP-MSVL-HULL", "saronic_route": "Marauder",
          "route_kind": "vessel-platform", "fit_pct": "", "win_prob": "",
          "partner_strategy": "prime or shipyard-partner", "notes": "seed: 150-class logistics USV",
          "source": "seed"},
         {"work_package_id": "WP-MSVL-AUTON", "saronic_route": "Echelon",
          "route_kind": "autonomy-c2", "fit_pct": "", "win_prob": "",
          "partner_strategy": "autonomy/C2 subsystem", "notes": "seed", "source": "seed"}])

    # Market-sizing knobs (Phase 2): the editable assumptions that turn gross funded
    # budget into Saronic SAM/SOM. Seeded ILLUSTRATIVE (source=seed); the real analyst
    # pass replaces them. Fractions 0-1. primary_line_item + measure key the live SUMIFS.
    seed_if_absent(ANALYST / "market_assumptions.csv",
        ["opportunity_id", "primary_line_item", "measure", "addressable_pct",
         "saronic_fit_pct", "timing_conf", "pursuit_access", "win_prob", "basis_note",
         "source"],
        [{"opportunity_id": "OPP-MSVL", "primary_line_item": "8211R01001",
          "measure": "net_procurement_p1", "addressable_pct": "0.40",
          "saronic_fit_pct": "0.50", "timing_conf": "0.6", "pursuit_access": "0.5",
          "win_prob": "0.3", "basis_note": "seed: manned connector; USV/autonomy + "
          "shipyard-partner share", "source": "seed"},
         {"opportunity_id": "OPP-ESP", "primary_line_item": "3569M11101",
          "measure": "net_procurement_p1", "addressable_pct": "0.15",
          "saronic_fit_pct": "0.30", "timing_conf": "0.5", "pursuit_access": "0.4",
          "win_prob": "0.2", "basis_note": "seed: SLEP/sustainment; small autonomy + "
          "integration addressable", "source": "seed"},
         {"opportunity_id": "OPP-AWS-AUTONOMY", "primary_line_item": "RDTE-0603804A-526",
          "measure": "rdte_cost", "addressable_pct": "0.80", "saronic_fit_pct": "0.80",
          "timing_conf": "0.4", "pursuit_access": "0.5", "win_prob": "0.3",
          "basis_note": "seed: marine autonomy S&T -> Echelon route", "source": "seed"}])

    # Saronic commercial-relevance knobs (review #6: rank on mission/platform/autonomy fit,
    # not historical contract size). Per opportunity, fractions 0-1; the Market Size sheet
    # averages these with the timing/pursuit/win knobs into a live Saronic priority score.
    seed_if_absent(ANALYST / "saronic_relevance.csv",
        ["opportunity_id", "mission_fit", "platform_fit", "autonomy_c2_fit", "notes",
         "source"],
        [{"opportunity_id": "OPP-MSVL", "mission_fit": "0.6", "platform_fit": "0.5",
          "autonomy_c2_fit": "0.7", "notes": "seed: contested distribution; USV/autonomy fit",
          "source": "seed"},
         {"opportunity_id": "OPP-ESP", "mission_fit": "0.3", "platform_fit": "0.4",
          "autonomy_c2_fit": "0.3", "notes": "seed: SLEP/sustainment; limited new-platform fit",
          "source": "seed"},
         {"opportunity_id": "OPP-AWS-AUTONOMY", "mission_fit": "0.8", "platform_fit": "0.4",
          "autonomy_c2_fit": "0.9", "notes": "seed: marine autonomy/C2 - Echelon route",
          "source": "seed"}])

    seed_customer_org_map()


_ORG_COLS = ["org_id", "parent_org_id", "name", "current_official_name", "role",
             "decision_rights", "command", "echelon", "portfolio_program",
             "associated_opportunity_ids", "customer_segment", "geography",
             "contracting_office", "available_pathways", "saronic_relationship_owner",
             "engagement_status", "next_action", "as_of", "notes", "source"]


def _org(org_id, parent, name, official, role, rights, command, echelon, portfolio,
         opps, segment, geo, office, pathways, notes):
    """One customer-org row at the rich schema (engagement fields blank for the analyst)."""
    return {"org_id": org_id, "parent_org_id": parent, "name": name,
            "current_official_name": official, "role": role, "decision_rights": rights,
            "command": command, "echelon": echelon, "portfolio_program": portfolio,
            "associated_opportunity_ids": opps, "customer_segment": segment,
            "geography": geo, "contracting_office": office, "available_pathways": pathways,
            "saronic_relationship_owner": "", "engagement_status": "Not started",
            "next_action": "", "as_of": ASOF_DATE, "notes": notes, "source": "seed"}


def seed_customer_org_map():
    """Rebuild the Customer Map as a relationship GRAPH (review #7): the broader Army
    autonomous-surface-logistics stakeholder chain (user -> requirement/experimentation ->
    program/acquisition -> contracting), wired by parent_org_id, with decision rights,
    current nomenclature, acquisition pathways (FAR/OTA/CSO/prototype/experiment), geography
    and the opportunities each org touches. Citations live in `notes`. SEED-only -> upgraded
    in place via reseed_if_seed_only (a real analyst account map is never clobbered)."""
    rows = [
        _org("ASA-ALT", "", "ASA(ALT)",
             "Assistant Secretary of the Army (Acquisition, Logistics & Technology)",
             "Service acquisition executive", "Milestone decision authority", "HQDA",
             "HQDA", "Army acquisition enterprise", "", "", "Washington DC", "",
             "FAR;OTA", "seed: SAE/MDA; named in the 2025 autonomous ship-to-shore demo"),
        _org("AMC", "", "Army Materiel Command", "U.S. Army Materiel Command",
             "Materiel / logistics enterprise", "Materiel release", "AMC", "ACOM",
             "Materiel & sustainment", "", "", "Redstone Arsenal AL", "", "FAR",
             "seed: parent of Army Contracting Command"),
        _org("AFC", "", "Army Futures Command", "U.S. Army Futures Command",
             "Requirements / modernization", "Capability requirements", "AFC", "ACOM",
             "Modernization (CFTs/CDIDs)", "OPP-AWS-AUTONOMY", C.SEG_ARMY_RDTE, "Austin TX",
             "", "OTA;prototype;experiment",
             "seed: requirements + experimentation home for autonomy"),
        _org("ACC", "AMC", "Army Contracting Command", "U.S. Army Contracting Command",
             "Contracting enterprise", "Contract strategy", "ACC", "MSC",
             "Contracting", "", "", "Redstone Arsenal AL", "", "FAR;OTA;CSO", "seed"),
        _org("ACC-DTA", "ACC", "ACC-Detroit Arsenal",
             "Army Contracting Command - Detroit Arsenal",
             "Contracting office (Army watercraft)", "Contract award", "ACC",
             "Contracting office", "Ground & watercraft systems", "OPP-MSVL;OPP-ESP",
             C.SEG_ARMY_OPS, "Detroit Arsenal MI", "W56HZV", "FAR;OTA;CSO;prototype",
             "seed: ACC-DTA publicly highlights Commercial Solutions Openings (CSO) as a "
             "route for commercial/autonomy capabilities (2026 ACC-DTA brief)"),
        _org("CPE-CS", "ASA-ALT", "CPE Combat Sustainment",
             "Capability Program Executive, Combat Sustainment",
             "Program executive portfolio (new nomenclature; replaces the PEO CS&CSS framing)",
             "Program execution", "ASA(ALT)", "CPE",
             "Transportation/Engineer/Quartermaster/Ordnance", "OPP-MSVL;OPP-ESP", "",
             "Detroit Arsenal MI", "", "FAR;OTA",
             "seed: June 2026 Army article - 'Link assumes helm at CPE Combat Sustainment'"),
        _org("PM-TRANS", "CPE-CS", "PM Transportation Systems",
             "Project Manager Transportation Systems",
             "Program / requirement owner (watercraft)", "Program requirements",
             "CPE Combat Sustainment", "PM", "Army watercraft (MSV(L), LCU/LSV, ESP)",
             "OPP-MSVL;OPP-ESP", C.SEG_ARMY_OPS, "Detroit Arsenal MI", "W56HZV", "FAR;OTA",
             "seed: 2026 ACC-DTA brief places Watercraft under PM Transportation Systems in "
             "the Combat Support & Services Directorate"),
        _org("SUST-CDID", "AFC", "Sustainment CDID",
             "Sustainment Capability Development Integration Directorate",
             "Capability development / requirements", "Requirements shaping",
             "AFC / CASCOM", "CDID", "Sustainment capabilities", "OPP-AWS-AUTONOMY",
             C.SEG_ARMY_RDTE, "Fort Gregg-Adams VA", "", "experiment;prototype",
             "seed: named in the 2025 autonomous ship-to-shore demo"),
        _org("CL-CFT", "AFC", "Contested Logistics CFT",
             "Contested Logistics Cross-Functional Team",
             "Requirements priority (contested logistics)", "Modernization priority",
             "AFC", "CFT", "Contested logistics", "OPP-MSVL;OPP-AWS-AUTONOMY",
             C.SEG_ARMY_RDTE, "", "", "experiment;OTA",
             "seed: named in the 2025 autonomous ship-to-shore demo"),
        _org("USARPAC", "", "U.S. Army Pacific", "U.S. Army Pacific",
             "Theater command / operational user", "Operational demand", "USARPAC",
             "ASCC", "Theater sustainment demand", "OPP-MSVL", C.SEG_ARMY_OPS,
             "INDOPACOM", "", "experiment", "seed: theater demand signal; 2025 demo"),
        _org("8TSC", "USARPAC", "8th Theater Sustainment Command",
             "8th Theater Sustainment Command", "Operational user",
             "Operational requirements / feedback", "USARPAC", "TSC",
             "Theater sustainment", "OPP-MSVL", C.SEG_ARMY_OPS, "Hawaii / INDOPACOM", "",
             "experiment", "seed: 2025 autonomous ship-to-shore demo participant"),
        _org("569-DIVE", "8TSC", "569th Dive Detachment", "569th Engineer Dive Detachment",
             "Operational user (dive & salvage)", "Operational feedback", "8th TSC",
             "Detachment", "Dive & salvage", "", C.SEG_ARMY_OPS, "INDOPACOM", "",
             "experiment", "seed: 2025 autonomous ship-to-shore demo participant"),
        _org("USACE-ERDC", "", "ERDC (Coastal & Hydraulics Lab)",
             "U.S. Army Engineer Research and Development Center", "RDT&E / user",
             "S&T direction", "USACE", "Lab", "Civil-works floating plant + marine S&T",
             "", C.SEG_USACE, "Vicksburg MS", "W912HZ", "FAR;CSO;prototype",
             "seed: civil-works floating plant + marine S&T (ERDC DoDAAC W912HZ; other "
             "USACE districts contract under W912xx)"),
    ]
    reseed_if_seed_only(ANALYST / "customer_org_map.csv", _ORG_COLS, rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ANALYST.mkdir(parents=True, exist_ok=True)
    index = json.loads((EXTRACT / "_detail_index.json").read_text())
    fpds = load_fpds_actions()
    ca_agg = load_ca_agg()

    award_rows, action_rows = [], []
    n_fpds_awards = n_usasp_awards = 0

    for e in index:
        gid = e["generated_internal_id"]
        piid = e.get("piid")
        parent_idv = e.get("parent_idv_piid")
        # FPDS match key: task orders carry the parent IDV as referenced_idv_piid.
        fpds_recs = fpds.get((piid, parent_idv)) or fpds.get((piid, None)) or []

        # ---- awards register row (distinct amount_types as columns) ----
        award_rows.append({
            "award_id": gid, "piid": piid, "parent_idv_piid": parent_idv,
            "idv_type": e.get("idv_type_description"),
            "single_or_multiple_award": e.get("single_or_multiple_award"),
            "award_type": e.get("award_type"),
            "award_type_description": e.get("award_type_description"),
            "category": e.get("category"),
            "recipient_name": e.get("recipient_name"),
            "recipient_uei": e.get("recipient_uei"),
            "parent_recipient_name": e.get("parent_recipient_name"),
            "obligation_amount": e.get("total_obligation"),       # amount_type=obligation
            "current_value": e.get("base_exercised_options"),     # amount_type=current_value
            "ceiling_value": e.get("base_and_all_options"),       # amount_type=ceiling
            "total_outlay": e.get("total_outlay"),
            "subaward_count": e.get("subaward_count"),
            "total_subaward_amount": e.get("total_subaward_amount"),
            "date_signed": e.get("date_signed"),
            "pop_start_date": e.get("pop_start_date"),
            "pop_current_end_date": e.get("pop_current_end_date"),
            "pop_potential_end_date": e.get("pop_potential_end_date"),
            "first_action_date": e.get("first_action_date"),
            "last_action_date": e.get("last_action_date"),
            "extent_competed": e.get("extent_competed"),
            "extent_competed_description": e.get("extent_competed_description"),
            "solicitation_procedures": e.get("solicitation_procedures_description"),
            "fair_opportunity_limited": e.get("fair_opportunity_limited"),
            "number_of_offers": e.get("number_of_offers_received"),
            "naics_code": e.get("naics_code"), "naics_description": e.get("naics_description"),
            "psc_code": e.get("psc_code"), "psc_description": e.get("psc_description"),
            "funding_tas": "; ".join(e.get("funding_federal_accounts") or []),
            "funding_account_titles": "; ".join(e.get("funding_account_titles") or []),
            "has_tas": e.get("has_tas"),
            "matched_axes": e.get("matched_axes"),
            "actions_source": "fpds" if fpds_recs else "usaspending",
            "customer_segment": seg_for(e.get("psc_code"), e.get("naics_code"), piid,
                                        e.get("recipient_name"), e.get("psc_description")),
            "program": "",          # <- program attribution bridge fills
            "capability_node": "",  # <- capability bridge fills (Platform/Sensors/Effectors/C2)
            "hydrated": "N",
            "dollars_basis": DOLLARS_BASIS,
            "source_system": "usaspending+fpds",
            "source_id": "USASP-AWARD-DETAIL",
            "extract_run_id": RUN_ID,
            "row_hash": rhash(gid, e.get("total_obligation"), e.get("pop_current_end_date")),
        })

        # ---- award_actions (THE sum-able table): FPDS wins, USAspending fills ----
        if fpds_recs:
            n_fpds_awards += 1
            for r in fpds_recs:
                ad = r.get("signed_date")
                action_rows.append({
                    "award_id": gid, "piid": piid, "parent_idv_piid": parent_idv,
                    "mod_number": r.get("mod_number"),
                    "recipient_name": r.get("vendor_name") or e.get("recipient_name"),
                    "recipient_uei": r.get("vendor_uei") or e.get("recipient_uei"),
                    "action_date": ad, "fiscal_year": dod_fy(ad),
                    "amount_type": "obligation", "amount": fnum(r.get("this_obligated")),
                    "dollars_basis": DOLLARS_BASIS,
                    "action_type": r.get("contract_action_type"),
                    "pricing_type": r.get("pricing_type"),
                    "extent_competed": r.get("extent_competed"),
                    "contracting_office": r.get("contracting_office"),
                    "funding_office": r.get("funding_office"),
                    "psc_code": r.get("psc"), "naics_code": r.get("naics"),
                    "description": (r.get("description") or "")[:300],
                    "source_system": "fpds", "source_id": "FPDS-ATOM",
                    "extract_run_id": RUN_ID,
                    "row_hash": rhash(gid, r.get("mod_number"), ad, r.get("this_obligated")),
                })
        else:
            n_usasp_awards += 1
            tpath = USASPENDING_RAW / "transactions" / f"{safe(gid)}.json"
            txns = []
            if tpath.exists():
                try:
                    txns = json.loads(tpath.read_text()).get("results", [])
                except Exception:
                    txns = []
            for t in txns:
                ad = t.get("action_date")
                action_rows.append({
                    "award_id": gid, "piid": piid, "parent_idv_piid": parent_idv,
                    "mod_number": t.get("modification_number"),
                    "recipient_name": e.get("recipient_name"),
                    "recipient_uei": e.get("recipient_uei"),
                    "action_date": ad, "fiscal_year": dod_fy(ad),
                    "amount_type": "obligation", "amount": fnum(t.get("federal_action_obligation")),
                    "dollars_basis": DOLLARS_BASIS,
                    "action_type": t.get("action_type_description"),
                    "pricing_type": None, "extent_competed": None,
                    "contracting_office": None, "funding_office": None,
                    "psc_code": e.get("psc_code"), "naics_code": e.get("naics_code"),
                    "description": (t.get("description") or "")[:300],
                    "source_system": "usaspending", "source_id": "USASP-TXN",
                    "extract_run_id": RUN_ID,
                    "row_hash": rhash(gid, t.get("modification_number"), ad, t.get("federal_action_obligation")),
                })

    # ---- hydrate orphan parent IDVs (review #4): synthesized rows so the live MAXIFS
    # over pop_*_end_date resolves a vehicle's ordering-period end + ceiling ----
    synth_idv = synthesize_idv_rows(award_rows, ca_agg)
    award_rows.extend(synth_idv)

    # ---- subawards (SAM Stage 4) ----
    sub_rows = []
    for fp in glob.glob(str(SAM_SUB / "*.json")):
        try:
            doc = json.loads(Path(fp).read_text())
        except Exception:
            continue
        for s in doc.get("published", []):
            ad = s.get("subAwardDate")
            sub_rows.append({
                "prime_piid": doc.get("piid"), "prime_agency_id": doc.get("agency_id"),
                "prime_referenced_idv_piid": doc.get("referenced_idv_piid"),
                "prime_recipient": doc.get("recipient"),
                "sub_award_report_id": s.get("subAwardReportId"),
                "sub_award_number": s.get("subAwardNumber"),
                "amount_type": "subaward", "amount": fnum(s.get("subAwardAmount")),
                "dollars_basis": DOLLARS_BASIS,
                "sub_action_date": ad, "fiscal_year": dod_fy(ad),
                "submitted_date": s.get("submittedDate"),
                "sub_entity_name": s.get("subEntityLegalBusinessName"),
                "sub_entity_uei": s.get("subEntityUei"),
                "sub_parent_uei": s.get("subParentUei"),
                "sub_parent_name": s.get("subEntityParentLegalBusinessName"),
                "sub_description": (s.get("subawardDescription") or "")[:300],
                "prime_naics": (s.get("primeNaics") or {}).get("code") if isinstance(s.get("primeNaics"), dict) else None,
                "capability_node": "",
                "source_system": "sam_subaward", "source_id": "SAM-SUBAWARD",
                "extract_run_id": RUN_ID,
                "row_hash": rhash(s.get("subAwardReportId"), s.get("subAwardAmount")),
            })

    # ---- pipeline_events (SAM Stage 5) ----
    # Scope gate (mirrors the awards' Army+USACE in_scope): the `active` Opportunities
    # pull is title-only (agency-unrestricted), so drop non-Army/USACE departments here.
    # The raw _opportunities_index.json keeps ALL notices for audit.
    def _opp_in_scope(dep):
        d = (dep or "").upper()
        return ("ARMY" in d) or ("CORPS OF ENGINEERS" in d)

    pipe_rows = []
    oidx = EXTRACT / "_opportunities_index.json"
    if oidx.exists():
        for o in json.loads(oidx.read_text()):
            if not _opp_in_scope(o.get("department")):
                continue
            pipe_rows.append({
                "notice_id": o.get("notice_id"), "title": o.get("title"),
                "solicitation_number": o.get("solicitation_number"),
                "notice_type": o.get("type"), "base_type": o.get("base_type"),
                "posted_date": o.get("posted_date"), "fiscal_year": dod_fy(o.get("posted_date")),
                "response_deadline": o.get("response_deadline"),
                "naics_code": o.get("naics"), "psc_code": o.get("psc"),
                "set_aside": o.get("set_aside"), "department": o.get("department"),
                "award_number": o.get("award_number"), "matched_term": o.get("matched_term"),
                "customer_segment": MR.customer_segment(
                    o.get("psc"), o.get("naics"), office_of(o.get("solicitation_number")),
                    o.get("title"), o.get("title"), o.get("department")),
                "capability_node": "",
                "source_system": "sam_opportunities", "source_id": "SAM-OPPORTUNITY",
                "extract_run_id": RUN_ID,
                "row_hash": rhash(o.get("notice_id")),
            })
    # Collapse per-notice events -> one row per solicitation lifecycle (review #6).
    pipe_rows = collapse_pipeline_lifecycle(pipe_rows)

    # Sort open-soonest-first: OPEN (deadline >= as-of, nearest first) -> no-deadline ->
    # CLOSED (most-recently-closed first), so the live opportunities sit at the top.
    _asof = RUN_ID[-10:]
    _dl = lambda r: (r.get("response_deadline") or "")[:10]
    pipe_rows = (sorted((r for r in pipe_rows if _dl(r) and _dl(r) >= _asof), key=_dl)
                 + [r for r in pipe_rows if not _dl(r)]
                 + sorted((r for r in pipe_rows if _dl(r) and _dl(r) < _asof),
                          key=_dl, reverse=True))

    # ---- write ----
    award_cols = list(award_rows[0].keys()) if award_rows else []
    action_cols = ["award_id", "piid", "parent_idv_piid", "mod_number", "recipient_name",
                   "recipient_uei", "action_date", "fiscal_year", "amount_type", "amount",
                   "dollars_basis", "action_type", "pricing_type", "extent_competed",
                   "contracting_office", "funding_office", "psc_code", "naics_code",
                   "description", "source_system", "source_id", "extract_run_id", "row_hash"]
    sub_cols = list(sub_rows[0].keys()) if sub_rows else [
        "prime_piid", "amount_type", "amount", "sub_entity_name", "source_system",
        "extract_run_id", "row_hash"]
    pipe_cols = list(pipe_rows[0].keys()) if pipe_rows else [
        "notice_id", "title", "posted_date", "source_system", "extract_run_id", "row_hash"]

    write_csv(OUT / "contract_awards.csv", award_cols, award_rows)
    write_csv(OUT / "contract_award_actions.csv", action_cols, action_rows)
    write_csv(OUT / "contract_subawards.csv", sub_cols, sub_rows)
    write_csv(OUT / "contract_pipeline_events.csv", pipe_cols, pipe_rows)

    # ---- canonical family table + analyst bridges (reviews #3/#5/#7) ----
    families = build_families(award_rows, action_rows, ca_agg)
    # multiple-award cohorts (review #1): back-fill the cohort columns now that every
    # family exists, so co-awarded vehicles under one requirement count once.
    cohorts = build_award_cohorts(families)
    for f in families:
        cid, csz, crole = cohorts.get(f["family_key"], ("", 1, "Standalone"))
        f["cohort_id"], f["cohort_size"], f["cohort_role"] = cid, csz, crole
    write_csv(OUT / "contract_families.csv",
              list(families[0].keys()) if families else [], families)

    edges = build_lineage_edges(families)
    write_csv(ANALYST / "lineage_edges.csv",
              ["predecessor_family", "successor_family", "same_incumbent",
               "predecessor_incumbent", "successor_incumbent", "psc_match", "naics_match",
               "contracting_office_match", "temporal_gap_days", "evidence_score",
               "analyst_disposition", "review_date", "notes", "source"], edges)

    links = build_notice_family_links(pipe_rows, families)
    write_csv(ANALYST / "notice_family_links.csv",
              ["notice_id", "solicitation_number", "notice_title", "family_key",
               "family_incumbent", "psc_match", "naics_match", "contracting_office_match",
               "response_deadline", "evidence_score", "analyst_confirmed", "notes",
               "source"], links)

    seed_analyst_tables(families)
    write_source_clocks()

    # ---- reconciliation report ----
    sum_actions = sum(a["amount"] or 0 for a in action_rows)
    sum_oblig_awards = sum((a["obligation_amount"] or 0) for a in award_rows)
    print(f"=== aggregate_contracts {RUN_ID}")
    print(f"  contract_awards.csv          {len(award_rows):>6} awards "
          f"(actions source: {n_fpds_awards} FPDS / {n_usasp_awards} USAspending; "
          f"+{len(synth_idv)} hydrated IDV rows)")
    print(f"  contract_award_actions.csv   {len(action_rows):>6} mod actions  "
          f"sum(amount)=${sum_actions/1e6:,.1f}M   [THE sum-able table]")
    print(f"     cross-check awards.obligation sum = ${sum_oblig_awards/1e6:,.1f}M "
          f"(per-mod vs award-level differ by deobligations / FPDS-wins reconciliation)")
    print(f"  contract_subawards.csv       {len(sub_rows):>6} first-tier subs   "
          f"sum=${sum(s['amount'] or 0 for s in sub_rows)/1e6:,.1f}M")
    n_open = sum(1 for r in pipe_rows if _dl(r) and _dl(r) >= _asof)
    print(f"  contract_pipeline_events.csv {len(pipe_rows):>6} Army/USACE notices "
          f"({n_open} open vs as-of {_asof})")

    # family reconciliation summary (review #1/#3)
    cov = Counter(f["coverage_status"] for f in families)
    wc = [f for f in families if f["is_watercraft"] == "Y"]
    radar = [f for f in wc if (f["selected_measure"] or 0) >= C.MIN_OBLIG]
    neg_displayed = [f for f in radar if (f["reconstructed_action_sum"] or 0) < 0]
    seg = Counter(f["customer_segment"] for f in radar)
    print(f"  contract_families.csv        {len(families):>6} families "
          f"({len(wc)} watercraft; {len(radar)} >= ${C.MIN_OBLIG/1e6:.1f}M selected -> radar)")
    print(f"     coverage: " + " ".join(f"{k}={v}" for k, v in cov.most_common()))
    print(f"     radar families with NEGATIVE reconstructed actions (now flagged, "
          f"selected on award fallback): {len(neg_displayed)}")
    print(f"     radar customer segments: " + " | ".join(f"{k}={v}" for k, v in seg.most_common()))
    tier = Counter(f["saronic_tier"] for f in radar)
    print(f"     radar Saronic tiers: " + " | ".join(f"{k}={v}" for k, v in tier.most_common()))
    n_cohorts = len({f["cohort_id"] for f in families if f["cohort_id"]})
    n_in_cohort = sum(1 for f in radar if f["cohort_id"])
    anom = sum(1 for f in radar if f["date_anomaly"])
    dconf = Counter(f["date_confidence"] for f in radar)
    print(f"     multiple-award cohorts: {n_cohorts} ({n_in_cohort} radar families co-awarded); "
          f"date confidence " + " ".join(f"{k}={v}" for k, v in dconf.most_common())
          + f"; {anom} anomaly-flagged")
    conf_edges = sum(1 for e in edges if e["analyst_disposition"] in ("Confirmed", "Probable"))
    conf_links = sum(1 for ln in links if ln["analyst_confirmed"] in ("Y", "Confirmed"))
    print(f"  analyst/lineage_edges.csv    {len(edges):>6} candidate edges "
          f"({conf_edges} Confirmed/Probable -> suppress predecessor)")
    print(f"  analyst/notice_family_links  {len(links):>6} open-notice links "
          f"({conf_links} analyst-confirmed)")
    print(f"  analyst bridges seeded (if absent): recompete_reviews(+milestone cols), "
          f"opportunities, attribution x2, work_packages(+capability,+saronic_route), "
          f"market_assumptions, saronic_relevance, customer_org_map (graph)")
    print(f"  extracted/source_clocks.csv  written")
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
