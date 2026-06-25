#!/usr/bin/env python3
"""
compute_jumpball_signals - the net-new signals behind the workbook's
"jump ball" tabs (Re-buy Timing, Wave Cadence, Concentration, Source
Diversification), plus the prime award calendar and the empirical
prime-clustering test. The per-wave / per-wave-vendor / wave-pair leaves are NO
LONGER emitted here - the workbook derives those live (Excel-365 spills).

A "jump ball" is a contestable sourcing opportunity for a new entrant. Two
kinds, both screened at the (program, PIID x work-type lane) grain over a
recent window (the deck's FY22-25 basis; COMP_WINDOW overrides):

  1. Multi-source re-buy - the prime already splits the lane across several
     suppliers; surfaced with an estimated NEXT re-buy window.
  2. Concentrated lane - one vendor holds most of the lane's recent supplier
     $ (top-1 share high); contestable on its own. Its dynamic subset is a
     single -> multi split, where a credible second source has recently
     entered while the incumbent (prior top-1) is still present.

WAVE-FIRST (single source of truth). The 90-day award-burst clustering runs
ONCE per lane into an award-WAVE table; every lane-level cadence signal
(n_waves, median wave gap, last wave anchor, next expected) is then DERIVED
from that table, so every wave-derived value reconciles to one clustering pass.
NB: the WORKBOOK now computes these cadence signals LIVE (dynamic-array spills
over the raw award dates); the values here are the validation baseline, and the
workbook reads only the residual composition / transition fields as leaves. The
wave grain answers: how often do
waves recur (cadence), are the same vendors / dollar splits recurring
(composition similarity), and - at low confidence - what a wave is tied to in
the production cycle (capability mix + prime base-award offset).

The wave ANCHOR is the plain (unweighted) median award date of the wave's
records - NOT a dollar-weighted median: ~12% of waves carry a deobligation /
correction (negative-amount) record and ~10 waves net negative, where a
signed-weight median date is ill-defined. The median date is monotonic, always
in range, and immune to corrections.

Most lane counts/shares - and now the wave cadence + dispersion, cross-wave
composition similarity and the window-stable verdict - are computed LIVE in the
workbook (COUNTIFS/MAXIFS/SUMIFS over wb_vendor_lane_fy + dynamic-array spills
over Award Events / Event Dates). This script writes only the residual signals
Excel cannot (yet) do live - top-vendor stability, capability coherence, the
second-source entry FY, the incumbent-still-active flag, active-months %, vendor
adds and prod-cycle confidence - plus the raw award-events leaf and the prime
calendar. The wave / wave-vendor / wave-pair leaves and the window-sensitivity
table are NO LONGER emitted: the workbook re-clusters award waves live from the
raw award dates (the Event Dates leaf), so those are formulas.

TIMING ANCHOR (decided with the user): subaward award cadence + vendor
turnover is the PRIMARY re-buy clock. The prime/block calendar is an overlay
whose predictive value is TESTED here (jumpball_prime_clustering.csv), not
assumed - the outsourced market re-sources on the shipbuilder->supplier
agreement clock, which need not track prime/block awards. The clustering window
(CLUSTER_GAP_DAYS) here is only the extract's default basis for the residual
Lane Signals leaf; the WORKBOOK now re-clusters award waves LIVE from the raw
award dates (the Event Dates leaf), so the clustering window and its sensitivity
windows are live Assumptions controls, not precomputed here.

Outputs (descriptive; no gates, no verdict labels on the leaves):
  workbook_award_analysis/extracted/wb_lane_signals.csv   per-lane signals: the
                                                          live cadence/dispersion
                                                          columns are validated
                                                          against this; the
                                                          residual composition +
                                                          transition fields are
                                                          read from it as leaves
  workbook_award_analysis/extracted/wb_award_events.csv   one row per supplier
                                                          award record (the raw
                                                          leaf the waves build on;
                                                          lets the workbook do live
                                                          trailing-window sums)
  workbook_award_analysis/extracted/wb_prime_calendar.csv per-PIID prime
                                                          award dates + block
  research/extracted/jumpball_prime_clustering.csv        empirical overlay test

These leaves exist so NO signal needs to sit hardcoded as a blue cell on a
model/"calculation" tab: the workbook loads them as explicit data sheets and the
model tabs read them with live formulas (SUMIFS / AVERAGEIFS / XLOOKUP). The
award-wave pipeline itself - clustering, cadence dispersion, cosine allocation
similarity and window re-clustering - is now LIVE in the workbook (Excel-365
dynamic-array spills over Award Events / Event Dates). Python retains only the raw
event extraction, the prime calendar, and the residual Lane Signals composition /
transition fields it cannot (yet) express as formulas.

Pure stdlib. Reuses _corpus (same classified full-history corpus the workbook
cuts derive from), so lane rosters and dollars reconcile to wb_vendor_lane_fy.
"""
from __future__ import annotations

import csv
import glob
import json
import statistics
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import REPO, FY22_25, iter_records, load_registry, scope_meta, fy_of

# ---- bindings ---------------------------------------------------------------
DS = REPO / "projects/distributed_shipbuilding"
WB_OUT = DS / "workbook_award_analysis/extracted"
RESEARCH_OUT = DS / "research/extracted"
SOURCES = ("submarines", "ddg")
PROG_OF = {"submarines": None, "ddg": "ddg"}   # submarines split by vclass below
PROG_ORDER = {"virginia": 0, "columbia": 1, "ddg": 2}
FAMILY = {"virginia": "Submarines", "columbia": "Submarines", "ddg": "DDG-51"}

# ---- screen constants (echoed in the workbook + methodology doc) ------------
# Recent window deliberately runs FY22 -> present (incl. the partial latest FY)
# rather than the scorecard's FY22-25 snapshot: jump balls are about emerging
# second sources, so the newest entrants must be caught (FY26 is partial - a
# documented trade-off, flagged in the workbook + methodology doc).
RECENT_LO, RECENT_HI = FY22_25[0], 2026   # FY22 -> present
CLUSTER_GAP_DAYS = 90                     # award-wave clustering threshold (as-built)
SENS_WINDOWS = (45, 60, 120, 180)         # window-sensitivity (90 is the as-built base)
PROXIMITY_WINDOW_DAYS = 180              # "near a prime action" half-window
# As-of snapshot (= the workbook's Assumptions as-of, latest reported award).
# The trailing-window activity leaves (last 180/365d, days-since, recent adds)
# that feed the Continuous Sourcing tab are computed at this fixed date so the
# always-on read is stable on every open (the workbook holds annualized data and
# cannot recompute a trailing window from raw action dates live).
AS_OF = date(2026, 5, 22)

_EPOCH = date(1899, 12, 30)               # Excel serial day 0 (unused here; ISO out)


def _d(s: str):
    """ISO 'YYYY-MM-DD...' -> datetime.date, or None."""
    s = (s or "")[:10]
    if len(s) != 10:
        return None
    try:
        y, m, dd = int(s[:4]), int(s[5:7]), int(s[8:10])
        return date(y, m, dd)
    except ValueError:
        return None


def _median_int(vals) -> int:
    return int(round(statistics.median(vals))) if vals else 0


def _median_date(dates):
    """Plain (unweighted) median award date of a wave's records. Always in
    range and correction-proof (no dollar weighting - see module docstring)."""
    ords = sorted(d.toordinal() for d in dates)
    return date.fromordinal(int(round(statistics.median(ords))))


def _iqr(vals):
    """Inter-quartile range (days); blank for < 2 gaps (no dispersion)."""
    if len(vals) < 2:
        return ""
    q = statistics.quantiles(sorted(vals), n=4, method="inclusive")
    return int(round(q[2] - q[0]))


def _cv(vals):
    """Coefficient of variation of the gap series; blank for < 2 gaps."""
    if len(vals) < 2:
        return ""
    m = statistics.mean(vals)
    return round(statistics.stdev(vals) / m, 3) if m else ""


def _cosine(a: dict, b: dict) -> float:
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = sum(v * v for v in a.values()) ** 0.5
    nb = sum(v * v for v in b.values()) ** 0.5
    return dot / (na * nb) if na > 0 and nb > 0 else 0.0


def _clusters(dates_sorted, gap_days=CLUSTER_GAP_DAYS):
    """Group sorted dates into bursts; return list of cluster START dates.
    (Kept for the empirical prime-clustering overlay test.)"""
    starts = []
    prev = None
    for dt in dates_sorted:
        if prev is None or (dt - prev).days > gap_days:
            starts.append(dt)
        prev = dt
    return starts


def build_waves(recs, gap_days=CLUSTER_GAP_DAYS):
    """Cluster a lane's supplier records into award waves at `gap_days`.

    recs: list of (date, vendor_key, dollar_m). A new wave starts when a
    record's date is > gap_days after the previous distinct date (the same
    traversal `_clusters` uses, so wave membership is tied to the boundary
    definition - no second algorithm). Returns waves in chronological order,
    each a dict with dates / net $ / negative $ / record count / per-vendor
    accumulation / start / end / anchor (median date)."""
    distinct = sorted({dt for dt, _, _ in recs})
    if not distinct:
        return []
    wmap, idx, prev = {}, -1, None
    for dt in distinct:
        if prev is None or (dt - prev).days > gap_days:
            idx += 1
        wmap[dt] = idx
        prev = dt
    waves = [{"dates": [], "net": 0.0, "neg": 0.0, "pos": 0.0, "nrec": 0,
              "vend": defaultdict(lambda: {"d": 0.0, "dpos": 0.0,
                                           "n": 0, "dates": []})}
             for _ in range(idx + 1)]
    for dt, vk, d in recs:
        w = waves[wmap[dt]]
        w["dates"].append(dt)
        w["net"] += d
        w["nrec"] += 1
        if d < 0:
            w["neg"] += d
        elif d > 0:
            w["pos"] += d
        v = w["vend"][vk]
        v["d"] += d
        if d > 0:
            v["dpos"] += d
        v["n"] += 1
        v["dates"].append(dt)
    for w in waves:
        w["start"], w["end"] = min(w["dates"]), max(w["dates"])
        w["anchor"] = _median_date(w["dates"])
    return waves


def _wave_anchors(recs, gap_days):
    """Just the chronological wave anchor dates at a given window (sensitivity)."""
    return [w["anchor"] for w in build_waves(recs, gap_days)]


# ---- corpus -> per-lane vendor activity ------------------------------------

def _new_vendor():
    return {"first": None, "recent_d": 0.0, "recent_n": 0,
            "prior_d": 0.0, "prior_n": 0}


def collect():
    """Return lanes[(program, piid, work_type)] = {dates:[date], recs:[(date,
    vk, $)], vend:{vk:{...}}} over supplier records, plus a piid->meta map, a
    vk->display-name map, a vk->(naics4, naics_desc) capability map, and the
    flat list of raw supplier award EVENTS (one dict per record - the leaf the
    workbook loads so trailing-window sums can be live).

    `recs` is the raw award stream the wave table is built from; `vend` keeps
    the prior/recent split dollars + counts + first-award date used for the
    recent-window concentration / entry signals. Every supplier record is
    asserted to carry a parseable FY *and* date so the wave leaves reconcile to
    the FY leaf exactly (a future undated record fails the build loudly rather
    than silently un-tying the Checks tab)."""
    registry = load_registry()
    lanes: dict = defaultdict(lambda: {"dates": [], "recs": [],
                                       "vend": defaultdict(_new_vendor)})
    piid_meta: dict = {}
    names: dict = defaultdict(lambda: defaultdict(float))
    naics: dict = defaultdict(lambda: defaultdict(float))
    events: list = []

    for source in SOURCES:
        for p, m in scope_meta(source).items():
            program = ((m.get("class") or "").strip().lower()
                       if source == "submarines" else "ddg")
            piid_meta[p] = {"program": program,
                            "vessel_class": (m.get("class") or "").strip(),
                            "builder": (m.get("group") or m.get("prime")
                                        or "").strip(),
                            "label": " ".join((m.get("label") or "").split())}
        for rec in iter_records(source, registry=registry):
            if rec["role"] != "supplier" or rec["fy"] is None:
                continue
            program = (rec["vclass"].strip().lower()
                       if source == "submarines" else "ddg")
            dt = _d(rec["date"])
            assert dt is not None, f"undated supplier record {rec['report_id']!r}"
            vk, d = rec["vendor_key"], rec["dollar_m"]
            L = lanes[(program, rec["piid"], rec["bucket"])]
            L["dates"].append(dt)
            L["recs"].append((dt, vk, d))
            events.append({
                "program": program, "family": FAMILY[program],
                "piid": rec["piid"], "work_type": rec["bucket"],
                "vendor_uei": vk, "vendor_name": "",      # filled from disp below
                "award_date": dt.isoformat(), "fy": rec["fy"],
                "dollar_m": round(d, 3), "report_id": rec["report_id"],
                "naics4": rec["naics4"] or "", "capability": rec["naics_desc"] or "",
            })
            v = L["vend"][vk]
            if v["first"] is None or dt < v["first"]:
                v["first"] = dt
            if RECENT_LO <= rec["fy"] <= RECENT_HI:
                v["recent_d"] += d
                v["recent_n"] += 1
            elif rec["fy"] < RECENT_LO:
                v["prior_d"] += d
                v["prior_n"] += 1
            names[vk][(rec["parent_name"] or rec["vendor"]).upper()] += d
            naics[vk][(rec["naics4"] or "", rec["naics_desc"] or "")] += d
    disp = {vk: max(d.items(), key=lambda kv: kv[1])[0] for vk, d in names.items()}
    cap = {}
    for vk, d in naics.items():
        items = [kv for kv in d.items() if kv[0] != ("", "")]
        cap[vk] = max(items, key=lambda kv: kv[1])[0] if items else ("", "")
    for e in events:                       # resolve the modal display name per UEI
        e["vendor_name"] = disp.get(e["vendor_uei"], e["vendor_uei"])
    return lanes, piid_meta, disp, cap, events


def _top1_share(vmap, key):
    tot = sum(v[key] for v in vmap.values())
    if tot <= 0:
        return 0.0
    return round(max(v[key] for v in vmap.values()) / tot, 4)


def _wave_cap(vend, cap):
    """Dollar-weighted modal capability (naics_desc, else naics4) of a vendor
    set, using clamped (non-negative) dollars."""
    acc = defaultdict(float)
    for vk, v in vend.items():
        n4, nd = cap.get(vk, ("", ""))
        tag = nd or n4
        if tag:
            acc[tag] += max(v["d"], 0.0)
    return max(acc.items(), key=lambda kv: kv[1])[0] if acc else ""


def process_lane(program, piid, wt, L, disp, cap, prime_base):
    """Build the lane's award waves ONCE, then derive (a) the lane signal row,
    (b) the per-wave rows, (c) the per-wave-vendor rows."""
    recs = L["recs"]
    distinct = sorted(set(L["dates"]))
    gaps = [(b - a).days for a, b in zip(distinct, distinct[1:])]

    waves = build_waves(recs, CLUSTER_GAP_DAYS)
    n_waves = len(waves)
    anchors = [w["anchor"] for w in waves]
    wgaps = [(b - a).days for a, b in zip(anchors, anchors[1:])]
    median_gap = _median_int(wgaps)
    last_anchor = anchors[-1] if anchors else None
    last_award = distinct[-1] if distinct else None
    # forecast origin = the last ACTUAL award (= the last wave's end), not the
    # last wave's median anchor: the median sits ~half a wave-duration earlier, so
    # anchoring on it biases the next-wave forecast early enough to drop lanes
    # whose next wave is imminent. The wave-based median gap is the robustness
    # win; the origin should be the most recent buy. (A stray late record forms
    # its own last wave either way, so the median anchor protects nothing here.)
    next_expected = (last_award + timedelta(days=median_gap)) if wgaps else None

    # ---- wave-shape metrics (continuous-vs-periodic discrimination) ----------
    # Single-linkage chains a continuously-active lane into one multi-year
    # "wave", so a long wave DURATION (not the gap count) is the discriminator.
    # These are blue leaf signals; the periodic/continuous verdict + the
    # expected-window forecast are LIVE workbook formulas over these plus the
    # adjustable Assumptions thresholds.
    wave_durs = [(w["end"] - w["start"]).days for w in waves]
    max_wave_dur = max(wave_durs) if wave_durs else 0
    median_wave_dur = _median_int(wave_durs)
    # quiet gap = prior wave END -> next wave START (the true between-wave lull;
    # median_wave_gap_days above is anchor-to-anchor and is kept for cadence).
    quiet_gaps = [(waves[i + 1]["start"] - waves[i]["end"]).days
                  for i in range(n_waves - 1)]
    median_quiet_gap = _median_int(quiet_gaps)
    dur_gap_ratio = (round(max_wave_dur / median_gap, 3)
                     if median_gap > 0 else "")
    if distinct:
        active_months = {(d.year, d.month) for d in distinct}
        span_months = ((distinct[-1].year - distinct[0].year) * 12
                       + (distinct[-1].month - distinct[0].month) + 1)
        active_frac = (round(len(active_months) / span_months, 4)
                       if span_months else "")
    else:
        active_frac = ""

    # ---- recent / prior concentration + transition (recent-window grain) ----
    recent_v = {vk: v for vk, v in L["vend"].items() if v["recent_n"] > 0}
    prior_v = {vk: v for vk, v in L["vend"].items() if v["prior_n"] > 0}
    recent_top1_uei = recent_top1_name = ""
    if recent_v:
        rt = max(recent_v.items(), key=lambda kv: kv[1]["recent_d"])[0]
        recent_top1_uei, recent_top1_name = rt, disp.get(rt, rt)
    incumbent_uei = incumbent_name = incumbent_active = ""
    if prior_v:
        inc = max(prior_v.items(), key=lambda kv: kv[1]["prior_d"])[0]
        incumbent_uei, incumbent_name = inc, disp.get(inc, inc)
        incumbent_active = "yes" if inc in recent_v else "no"
    new_entrants = [v for vk, v in recent_v.items()
                    if vk not in prior_v and v["first"]]
    second_entry_fy = (min(fy_of(v["first"].isoformat()) for v in new_entrants)
                       if new_entrants else "")

    # ---- trailing-window activity (Continuous Sourcing tab; as-of snapshot) --
    # "Is this lane actively buying now?" - the always-on read. Computed at the
    # fixed AS_OF from raw action dates (Excel can't recompute a trailing window
    # from the annualized leaves), mirroring how dollars_recent is FY-windowed.
    lo180, lo365 = AS_OF - timedelta(days=180), AS_OF - timedelta(days=365)
    d180 = n180 = d365 = n365 = 0
    for dt, _vk, d in recs:
        if dt > AS_OF or dt < lo365:
            continue
        d365 += d
        n365 += 1
        if dt >= lo180:
            d180 += d
            n180 += 1
    days_since = (AS_OF - last_award).days if last_award else ""
    vendor_adds_365 = sum(1 for v in L["vend"].values()
                          if v["first"] and v["first"] >= lo365)

    # ---- cross-wave composition similarity (full history) -------------------
    vsets = [set(w["vend"]) for w in waves]
    retention = [len(vsets[i] & vsets[i - 1]) / len(vsets[i])
                 for i in range(1, n_waves) if vsets[i]]
    def _share_vec(w):
        pos = {vk: max(v["d"], 0.0) for vk, v in w["vend"].items()}
        tot = sum(pos.values())
        return {vk: x / tot for vk, x in pos.items()} if tot > 0 else {}
    vecs = [_share_vec(w) for w in waves]
    alloc = [_cosine(vecs[i], vecs[i - 1])
             for i in range(1, n_waves) if vecs[i] and vecs[i - 1]]
    tvs = [max(w["vend"].items(), key=lambda kv: kv[1]["d"])[0]
           if w["net"] > 0 and w["vend"] else None for w in waves]
    tvs_real = [t for t in tvs if t]
    top_stable = ""
    if tvs_real:
        modal_tv = statistics.mode(tvs_real)
        top_stable = round(sum(1 for t in tvs_real if t == modal_tv)
                           / len(tvs_real), 4)
    wave_caps = [_wave_cap(w["vend"], cap) for w in waves]
    lane_cap = _wave_cap({vk: v for w in waves for vk, v in w["vend"].items()},
                         cap) if waves else ""
    cap_coh = (round(sum(1 for c in wave_caps if c == lane_cap) / n_waves, 4)
               if lane_cap and n_waves else "")

    retention_avg = round(statistics.mean(retention), 4) if retention else ""
    alloc_avg = round(statistics.mean(alloc), 4) if alloc else ""

    # ---- per-PAIR composition (long-form leaf; the averages above roll these up)
    # One row per consecutive wave pair so the workbook can AVERAGEIFS the lane-
    # level retention / allocation similarity LIVE off this leaf instead of
    # reading a hardcoded average. Blank metric where a wave carries no positive
    # dollars (cosine undefined) - mirrors the averaged lists' skip rule.
    fam = FAMILY[program]
    pair_rows = []
    for k in range(1, n_waves):
        ret = (round(len(vsets[k] & vsets[k - 1]) / len(vsets[k]), 4)
               if vsets[k] else "")
        al = (round(_cosine(vecs[k], vecs[k - 1]), 4)
              if (vecs[k] and vecs[k - 1]) else "")
        same_top = ("yes" if (tvs[k] and tvs[k - 1] and tvs[k] == tvs[k - 1])
                    else "no")
        cap_match = ("yes" if (wave_caps[k] and wave_caps[k - 1]
                               and wave_caps[k] == wave_caps[k - 1]) else "no")
        pair_rows.append({
            "program": program, "family": fam, "piid": piid, "work_type": wt,
            "prior_wave_seq": k, "wave_seq": k + 1,
            "vendor_retention": ret, "allocation_similarity": al,
            "same_top_vendor": same_top, "capability_match": cap_match,
        })

    # ---- production-cycle confidence (evidence-backed, non-gating) ----------
    # A descriptive read on the visible evidence columns (capability coherence
    # + composition similarity). Text tokens (hull/build-year/admin) are
    # deferred (would require extending _corpus.iter_records). Never gates.
    if n_waves < 2:
        confidence = "n/a"
    elif (cap_coh != "" and cap_coh >= 0.8 and alloc_avg != "" and alloc_avg >= 0.6
          and retention_avg != "" and retention_avg >= 0.5):
        confidence = "high"
    elif (cap_coh != "" and cap_coh >= 0.6
          and ((alloc_avg != "" and alloc_avg >= 0.4)
               or (retention_avg != "" and retention_avg >= 0.4))):
        confidence = "medium"
    elif cap_coh != "" and cap_coh >= 0.5:
        confidence = "low"
    else:
        confidence = "not-supportable"

    # window sensitivity + window-stable are no longer computed here: the workbook
    # re-clusters award waves live from the raw award dates (the Event Dates leaf
    # flags wave starts at each window), so Wave Sensitivity and the window-stable
    # verdict are live formulas. This script no longer owns that calculation.

    sig = {
        "program": program, "piid": piid, "work_type": wt,
        "n_awards": len(L["dates"]), "n_distinct_dates": len(distinct),
        "median_interaward_days": _median_int(gaps),
        "n_waves": n_waves, "median_wave_gap_days": median_gap,
        "gap_iqr_days": _iqr(wgaps), "gap_cv": _cv(wgaps), "n_gaps": len(wgaps),
        "last_award_date": distinct[-1].isoformat() if distinct else "",
        "last_wave_anchor": last_anchor.isoformat() if last_anchor else "",
        "next_expected": next_expected.isoformat() if next_expected else "",
        "max_wave_duration_days": max_wave_dur,
        "median_wave_duration_days": median_wave_dur,
        "median_quiet_gap_days": median_quiet_gap,
        "n_quiet_gaps": len(quiet_gaps),
        "max_wave_duration_to_gap_ratio": dur_gap_ratio,
        "active_months_frac": active_frac,
        "dollars_recent": round(sum(v["recent_d"] for v in recent_v.values()), 3),
        "dollars_prior": round(sum(v["prior_d"] for v in prior_v.values()), 3),
        "active_vendors_prior": len(prior_v),
        "active_vendors_recent": len(recent_v),
        "top1_share_prior": _top1_share(prior_v, "prior_d"),
        "top1_share_recent": _top1_share(recent_v, "recent_d"),
        "dollars_last180_m": round(d180, 3), "records_last180": n180,
        "dollars_last365_m": round(d365, 3), "records_last365": n365,
        "days_since_last_award": days_since,
        "vendor_adds_last365": vendor_adds_365,
        "recent_top1_uei": recent_top1_uei, "recent_top1_name": recent_top1_name,
        "second_source_entry_fy": second_entry_fy,
        "incumbent_uei": incumbent_uei, "incumbent_name": incumbent_name,
        "incumbent_still_active": incumbent_active,
        "vendor_retention_avg": retention_avg,
        "allocation_similarity_avg": alloc_avg,
        "top_vendor_stable_frac": top_stable,
        "capability_coherence": cap_coh,
        "prodcycle_confidence": confidence,
    }

    # ---- per-wave + per-wave-vendor rows ------------------------------------
    fam = FAMILY[program]
    base = prime_base.get(piid)
    wave_rows, wv_rows, seen = [], [], set()
    for seq, w in enumerate(waves, start=1):
        net = w["net"]
        prior_iv = (w["anchor"] - waves[seq - 2]["anchor"]).days if seq > 1 else ""
        if net > 0:
            tv = max(w["vend"].items(), key=lambda kv: kv[1]["d"])
            top_uei, top_name = tv[0], disp.get(tv[0], tv[0])
            top1 = round(min(max(tv[1]["d"], 0.0) / net, 1.0), 4)
            others = round(1 - top1, 4)
        else:
            top_uei = top_name = ""
            top1 = others = ""
        wave_rows.append({
            "program": program, "family": fam, "piid": piid, "work_type": wt,
            "wave_seq": seq,
            "wave_start": w["start"].isoformat(), "wave_end": w["end"].isoformat(),
            "wave_anchor": w["anchor"].isoformat(),
            "wave_duration_days": (w["end"] - w["start"]).days,
            "prior_wave_interval_days": prior_iv,
            "n_records": w["nrec"], "wave_dollars_m": round(net, 3),
            "wave_dollars_positive_m": round(w["pos"], 3),
            "n_vendors": len(w["vend"]),
            "top_vendor_uei": top_uei, "top_vendor_name": top_name,
            "top1_share": top1, "others_share": others,
            "modal_capability": wave_caps[seq - 1],
            "neg_correction_m": round(w["neg"], 3),
            "prime_base_offset_days": (w["anchor"] - base).days if base else "",
        })
        for vk, v in sorted(w["vend"].items(),
                            key=lambda kv: (-kv[1]["d"], kv[0])):
            n4, nd = cap.get(vk, ("", ""))
            wv_rows.append({
                "program": program, "family": fam, "piid": piid, "work_type": wt,
                "wave_seq": seq, "vendor_uei": vk, "vendor_name": disp.get(vk, vk),
                "naics4": n4, "capability": nd,
                "wave_vendor_dollars_m": round(v["d"], 3),
                "wave_vendor_dollars_positive_m": round(v["dpos"], 3),
                "wave_vendor_share": (round(min(max(v["d"], 0.0) / net, 1.0), 4)
                                      if net > 0 else ""),
                "records": v["n"],
                "first_date_in_wave": min(v["dates"]).isoformat(),
                "last_date_in_wave": max(v["dates"]).isoformat(),
                "entrant_flag": "yes" if vk not in seen else "no",
            })
        seen |= set(w["vend"])
    return sig, wave_rows, wv_rows, pair_rows


def lane_tables(lanes, disp, cap, prime_base):
    """Drive process_lane over every lane; return (lane_signals, award_waves,
    wave_vendors, wave_pairs), each sorted for stable output."""
    sigs, waves, wvs, pairs = [], [], [], []
    for (program, piid, wt), L in lanes.items():
        sig, wave_rows, wv_rows, pair_rows = process_lane(
            program, piid, wt, L, disp, cap, prime_base)
        sigs.append(sig)
        waves.extend(wave_rows)
        wvs.extend(wv_rows)
        pairs.extend(pair_rows)
    sigs.sort(key=lambda r: (PROG_ORDER[r["program"]], r["piid"],
                             -r["active_vendors_recent"]))
    waves.sort(key=lambda r: (PROG_ORDER[r["program"]], r["piid"],
                              r["work_type"], r["wave_seq"]))
    wvs.sort(key=lambda r: (PROG_ORDER[r["program"]], r["piid"], r["work_type"],
                            r["wave_seq"], -r["wave_vendor_dollars_m"]))
    pairs.sort(key=lambda r: (PROG_ORDER[r["program"]], r["piid"],
                              r["work_type"], r["wave_seq"]))
    return sigs, waves, wvs, pairs


# FPDS pulls are floored at these SIGNED_DATE windows (read from the raw files'
# date_window), so a PIID whose true base award predates the floor shows a
# floored base date, NOT the real award - flagged per row so it never reads as
# a true base award. Another reason the prime calendar is overlay, not clock.
FPDS_WINDOW_START = {"submarines": date(2018, 1, 1), "ddg": date(2017, 10, 1)}
_SRC_OF = {"virginia": "submarines", "columbia": "submarines", "ddg": "ddg"}


# ---- prime calendar (FPDS) --------------------------------------------------

def _fpds_records(prog_dir: Path):
    for f in sorted(glob.glob(str(prog_dir / "*_raw.json"))):
        try:
            blob = json.load(open(f, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        recs = blob.get("records") if isinstance(blob, dict) else blob
        for r in (recs or []):
            yield r


def prime_calendar(piid_meta):
    """Per in-scope PIID: base (earliest) + last prime action date, action
    count, base action type. Built from the union of the name/desc-keyed FPDS
    pulls, filtered to the in-scope PIID (the pulls oversweep and are capped,
    so coverage is partial - flagged per row)."""
    inscope = set(piid_meta)
    by_piid = defaultdict(lambda: {"dates": [], "actions": {}})
    for source in SOURCES:
        for r in _fpds_records(DS / source / "research/fpds_raw"):
            p = (r.get("piid") or "").strip()
            if p not in inscope:
                continue
            dt = _d(r.get("signed_date"))
            if dt:
                by_piid[p]["dates"].append(dt)
                by_piid[p]["actions"][dt] = (r.get("contract_action_type")
                                             or "").strip()
    rows = []
    for p, m in sorted(piid_meta.items(),
                       key=lambda kv: (PROG_ORDER[kv[1]["program"]], kv[0])):
        dts = sorted(by_piid[p]["dates"])
        covered = bool(dts)
        floor = FPDS_WINDOW_START[_SRC_OF[m["program"]]]
        floored = covered and (dts[0] - floor).days <= 31
        rows.append({
            "program": m["program"], "piid": p,
            "vessel_class": m["vessel_class"], "builder": m["builder"],
            "block_label": m["label"],
            "prime_base_award_date": dts[0].isoformat() if covered else "",
            "prime_last_action_date": dts[-1].isoformat() if covered else "",
            "n_prime_actions": len(dts),
            "base_action_type": by_piid[p]["actions"].get(dts[0], "") if covered else "",
            "covered": "yes" if covered else "no",
            "base_is_window_floored": "yes" if floored else "no",
        })
    return rows, by_piid


# ---- empirical overlay test -------------------------------------------------

def prime_clustering_test(lanes, piid_meta, by_piid):
    """Does supplier re-sourcing cluster around prime/block AWARDS?

    For every supplier award-burst cluster start in a PIID with prime coverage,
    measure days to (a) the nearest prime action of ANY kind and (b) the PIID's
    BASE award date. (a) is near-trivially small on PIIDs with hundreds of
    administrative mods, so (b) - proximity to the discrete base/block award -
    is the meaningful re-sourcing-wave signal. Diffuse base proximity => the
    prime calendar is context, not the re-buy clock (cadence/turnover lead)."""
    near, base = defaultdict(list), defaultdict(list)
    for (program, piid, wt), L in lanes.items():
        prime_dts = sorted(by_piid.get(piid, {}).get("dates", []))
        if not prime_dts:
            continue
        base_dt = prime_dts[0]
        for cs in _clusters(sorted(set(L["dates"]))):
            near[program].append(min(abs((cs - pd).days) for pd in prime_dts))
            base[program].append(abs((cs - base_dt).days))
    rows = []
    for program in ("virginia", "columbia", "ddg"):
        nd, bd = near.get(program, []), base.get(program, [])
        w = sum(1 for x in bd if x <= PROXIMITY_WINDOW_DAYS)
        rows.append({
            "program": program,
            "n_cluster_starts_tested": len(bd),
            "median_days_to_nearest_prime_action": _median_int(nd),
            "median_days_to_base_award": _median_int(bd),
            f"base_share_within_{PROXIMITY_WINDOW_DAYS}d":
                round(w / len(bd), 4) if bd else 0.0,
        })
    return rows


# ---- write ------------------------------------------------------------------

def _write(path: Path, rows, cols):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


AWARD_EVENT_COLS = ["program", "family", "piid", "work_type", "vendor_uei",
                    "vendor_name", "award_date", "fy", "dollar_m", "report_id",
                    "naics4", "capability"]


def main() -> int:
    lanes, piid_meta, disp, cap, events = collect()
    pc, by_piid = prime_calendar(piid_meta)
    prime_base = {r["piid"]: _d(r["prime_base_award_date"]) for r in pc
                  if r["covered"] == "yes" and r["base_is_window_floored"] == "no"}
    ls, aw, wv, pairs = lane_tables(lanes, disp, cap, prime_base)
    pct = prime_clustering_test(lanes, piid_meta, by_piid)
    events.sort(key=lambda e: (PROG_ORDER[e["program"]], e["piid"],
                               e["work_type"], e["award_date"]))

    # The wave / wave-vendor / wave-pair leaves are NO LONGER emitted: those
    # sheets are now derived LIVE in the workbook (dynamic-array spills over the
    # raw Award Events leaf), so they no longer read a precomputed CSV. This
    # script now writes only the raw award-event stream and the residual lane
    # signals Excel still cannot derive live (cross-wave composition: top-vendor
    # stability + capability coherence; source transition: second-source FY,
    # incumbent / still-active; activity: vendor-adds, active-months %; the
    # prod-cycle confidence token). build_waves still runs to produce THOSE.
    _write(WB_OUT / "wb_lane_signals.csv", ls, list(ls[0].keys()))
    _write(WB_OUT / "wb_award_events.csv", events, AWARD_EVENT_COLS)
    _write(WB_OUT / "wb_prime_calendar.csv", pc, list(pc[0].keys()))
    _write(RESEARCH_OUT / "jumpball_prime_clustering.csv", pct, list(pct[0].keys()))

    n_cov = sum(1 for r in pc if r["covered"] == "yes")
    n_single = sum(1 for r in ls if r["n_waves"] == 1)
    print(f"lanes: {len(ls)}  |  award waves: {len(aw)}  |  wave-vendor rows: "
          f"{len(wv)}  |  single-wave lanes: {n_single}")
    print(f"wave-pair rows: {len(pairs)}  |  award-event rows: {len(events)}")
    print(f"prime PIIDs covered: {n_cov}/{len(pc)}")
    print(f"recent window FY{RECENT_LO % 100}-{RECENT_HI % 100}; "
          f"cluster gap {CLUSTER_GAP_DAYS}d (sensitivity now live in-workbook)")
    print("prime-clustering test (supplier re-buy burst vs prime award; "
          "base-award proximity is the meaningful signal):")
    for r in pct:
        print(f"  [{r['program']:9s}] n={r['n_cluster_starts_tested']:4d}  "
              f"nearest-action={r['median_days_to_nearest_prime_action']:4d}d  "
              f"base-award={r['median_days_to_base_award']:5d}d  "
              f"base within {PROXIMITY_WINDOW_DAYS}d="
              f"{r[f'base_share_within_{PROXIMITY_WINDOW_DAYS}d']:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
