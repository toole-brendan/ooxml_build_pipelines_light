"""verify_lineage - standalone replica of the Recompete Radar lineage derivation.

Reproduces the predecessor<->successor chaining over extracted/contract_awards.csv
with NO workbook imports (csv + datetime only), so the rendered Lineage status column
can be checked against an independent computation. Run:  python3 verify_lineage.py
"""
import csv
from collections import defaultdict
from datetime import date

CSV = "extracted/contract_awards.csv"
MIN_OBLIG = 1_000_000.0
GAP_CAP_DAYS = 913   # 30 mo
OVERLAP_DAYS = 548   # 18 mo
AS_OF = date(2026, 6, 20)

WC_PSC = {"1905", "1915", "1925", "1930", "1935", "1940", "1945", "1990", "2090"}
WC_NAICS = {"336611", "336612"}
WC_PRIMES = ["VIGOR", "BIRDON", "BAY SHIP", "COLONNA", "CONRAD",
             "EASTERN SHIPBUILDING", "THOMA-SEA", "METAL TRADES"]
WC_DESC = ["SHIP BUILD", "SHIP REPAIR", "BOAT", "VESSEL", "WATERCRAFT", "DREDG",
           "BARGE", "LANDING CRAFT", "TUG", "PONTOON", "LIGHTER", "MARINE"]


def wc_reason(g, row):
    psc = (g(row, "psc_code") or "").strip()
    naics = (g(row, "naics_code") or "").strip()
    name = (g(row, "recipient_name") or "").upper()
    nd = (g(row, "naics_description") or "").upper()
    pd = (g(row, "psc_description") or "").upper()
    if psc in WC_PSC:
        return f"PSC {psc}"
    if naics in WC_NAICS:
        return f"NAICS {naics}"
    for p in WC_PRIMES:
        if p in name:
            return f"prime: {p.title()}"
    for t in WC_DESC:
        if t in nd or t in pd:
            return f"desc: {t.lower()}"
    return None


def pdate(s):
    s = (s or "").strip()
    if not s:
        return None
    y, m, d = (int(p) for p in s[:10].split("-"))
    return date(y, m, d)


def main():
    with open(CSV, newline="") as fh:
        r = csv.reader(fh)
        headers = next(r)
        rows = list(r)
    ix = {h: i for i, h in enumerate(headers)}

    def g(row, c):
        j = ix[c]
        return row[j] if j < len(row) else ""

    def oblig(row):
        v = (g(row, "obligation_amount") or "").strip()
        return float(v) if v else 0.0

    fams = defaultdict(list)
    for row in rows:
        key = g(row, "parent_idv_piid") or g(row, "piid")
        if key:
            fams[key].append(row)

    attrs = {}            # key -> dict (relevant families only, FULL universe)
    for key, frows in fams.items():
        reason = next((x for x in (wc_reason(g, a)
                       for a in sorted(frows, key=oblig, reverse=True)) if x), None)
        if reason is None:
            continue
        dom = max(frows, key=oblig)
        starts = [d for d in (pdate(g(a, "pop_start_date")) for a in frows) if d]
        ends = [d for d in (pdate(g(a, "pop_current_end_date")) for a in frows) if d]
        attrs[key] = {
            "key": key, "reason": reason, "total": sum(oblig(a) for a in frows),
            "uei": (g(dom, "recipient_uei") or "").strip(),
            "psc": (g(dom, "psc_code") or "").strip(),
            "incumbent": g(dom, "recipient_name"),
            "start": min(starts) if starts else None,
            "end": max(ends) if ends else None,
        }

    # chain within (uei, psc): A(earlier) -> B(later), closest gap wins
    groups = defaultdict(list)
    for a in attrs.values():
        if a["uei"] and a["psc"] and a["start"] and a["end"]:
            groups[(a["uei"], a["psc"])].append(a)

    successor = {}        # A.key -> (B.key, gap_days)
    for members in groups.values():
        members.sort(key=lambda a: (a["start"], a["end"]))
        for i, A in enumerate(members):
            best, best_gap = None, None
            for B in members[i + 1:]:
                gap = (B["start"] - A["end"]).days
                if -OVERLAP_DAYS <= gap <= GAP_CAP_DAYS:
                    if best_gap is None or abs(gap) < abs(best_gap):
                        best, best_gap = B, gap
            if best is not None and (A["key"] not in successor
                                     or abs(best_gap) < abs(successor[A["key"]][1])):
                successor[A["key"]] = (best["key"], best_gap)

    predecessor = {}      # B.key -> (A.key, gap_days)
    for a_key, (b_key, gap) in successor.items():
        if b_key not in predecessor or abs(gap) < abs(predecessor[b_key][1]):
            predecessor[b_key] = (a_key, gap)

    def status(a):
        if a["key"] in successor:
            return "Superseded"
        if a["end"] and a["end"] < AS_OF:
            return "Overdue"
        return "Active"

    shown = sorted((a for a in attrs.values() if a["total"] >= MIN_OBLIG),
                   key=lambda a: -a["total"])

    print(f"total families:      {len(fams)}")
    print(f"watercraft-relevant: {len(attrs)}")
    print(f"shown (>= $1M):      {len(shown)}")
    counts = defaultdict(int)
    for a in shown:
        counts[status(a)] += 1
    print(f"split: OVERDUE {counts['Overdue']} | SUPERSEDED {counts['Superseded']} "
          f"| ACTIVE {counts['Active']}  (sum {sum(counts.values())})")

    # below-floor successor diagnostic
    below = 0
    for a in shown:
        if status(a) == "Superseded":
            succ_key = successor[a["key"]][0]
            if attrs.get(succ_key, {}).get("total", 0) < MIN_OBLIG:
                below += 1
    print(f"superseded-by-a-below-floor-successor: {below} of {counts['Superseded']}")

    print("\nnamed chains:")
    for k in ["W56HZV14C0015", "W56HZV19D0093", "W56HZV17D0086", "W912BU23C0020"]:
        a = attrs.get(k)
        if not a:
            print(f"  {k}: (not a relevant family)")
            continue
        succ = successor.get(k)
        pred = predecessor.get(k)
        print(f"  {k}: status={status(a)} psc={a['psc']} "
              f"start={a['start']} end={a['end']} "
              f"pred={pred[0] if pred else '-'} succ={succ[0] if succ else '-'}"
              + (f" (gap {succ[1]}d)" if succ else ""))


if __name__ == "__main__":
    main()
