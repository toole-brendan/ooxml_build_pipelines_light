#!/usr/bin/env python3
"""
Pull DoD daily contract announcements with destroyer paragraphs +
place-of-performance percentages.

Source: globalsecurity.org's mirror of war.gov daily DoD contract bulletins.
(war.gov direct returns 403; globalsecurity.org is the working mirror.)

URL pattern:
    daily index:    https://www.globalsecurity.org/military/library/news/YYYY/MM/MM-DD_index.htm
    contract page:  https://www.globalsecurity.org/military/library/news/YYYY/MM/dod-contracts_<war_gov_id>.htm

Coverage limit: globalsecurity.org only mirrors war.gov daily contract pages
starting ~2025. Pre-2025 is NOT available via this path (use Wayback batch
fetcher for 2022-2024).

Process:
    1. For each day in [START, today], fetch the daily index
    2. Grep for href="dod-contracts_<id>.htm" links
    3. Fetch each contract page (cached, resume-safe)
    4. Parse destroyer paragraphs (Arleigh Burke / DDG / Bath Iron Works /
       Ingalls + DDG GFE primes: LM Aegis, Raytheon SPY-6, GE LM2500,
       BAE Mk 45/VLS, NG SPQ-9B, L3Harris CEC, DRS combat systems)
    5. Extract PIID, $, prime, expected completion, POP cities + %
    6. Bucket POP into BIW-sites / Ingalls-sites / Other-US / Foreign / Other-<1%

The cache directory is symlinked to submarine_outsourced_work's cache so
prior pulls don't have to be repeated. Only NEW days since the last sub-pull
will require fresh HTTP fetches.

Outputs (overwritten on each run from cache):
    extracted/dod_announcement_pop.csv
    research_primary_sources/dod_announcement_pop/cache/<war_gov_id>.htm  (raw cache; symlinked)
    research_primary_sources/dod_announcement_pop/<date>_dod-contracts_<id>.txt  (per-action ddg paragraphs)

Re-runnable / resume-safe: cached pages skipped on re-fetch.
"""
import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT_FOLDER = REPO / "research_primary_sources" / "dod_announcement_pop"
CACHE_DIR = OUT_FOLDER / "cache"
OUT_CSV = REPO / "extracted" / "dod_announcement_pop.csv"
SCOPE_JSON = REPO / "extracted" / "nc_scope_summary.json"

OUT_FOLDER.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = date(2025, 1, 1)
END_DATE = date.today()

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
BASE = "https://www.globalsecurity.org/military/library/news"
REQUEST_DELAY_SEC = 0.4

# ---- DESTROYER FILTER ----
# Hits paragraphs likely about DDG-51 program or its GFE primes.
# Includes DDG hull numbers, Arleigh Burke / Flight III class names, the
# two yards by name, and signature DDG GFE systems (Aegis, SPY-6, LM2500,
# Mk 41 VLS, Mk 45 gun). Also captures any N00024 PIID for downstream
# in-scope-PIID matching against the destroyer scope file.
DDG_FILTER = re.compile(
    r"\b("
    r"DDG[- ]?\d{2,3}"
    r"|Arleigh Burke"
    r"|guided[- ]missile destroyer"
    r"|Flight\s+III"
    r"|Bath Iron Works"
    r"|\bBIW\b"
    r"|Ingalls Shipbuilding"
    r"|Huntington Ingalls.{0,40}(?:Pascagoula|Ingalls)"
    r"|Pascagoula"
    r"|Bath,\s*Maine"
    r"|Aegis"
    r"|AN/SPY[- ]?6"
    r"|SPY[- ]?6"
    r"|LM2500"
    r"|Mk[- ]?41\b|MK[- ]?41\b|Vertical Launching System|\bVLS\b"
    r"|Mk[- ]?45\b|MK[- ]?45\b"
    r"|AN/SPQ[- ]?9"
    r"|AN/USG[- ]?[23]"
    r"|Cooperative Engagement Capability|\bCEC\b"
    r"|N00024-\d{2}-[A-Z]-\d{4}"
    r")\b",
    re.I,
)

SENTINEL = re.compile(r"is the contracting activity[^.]*\.\s*(?:\(Awarded[^)]*\)\.\s*)?")

RE_PIID = re.compile(r"\((N\d{5}-\d{2}-[A-Z]-\d{4})\)")
RE_AMOUNT = re.compile(
    r"\$([\d,]+(?:\.\d+)?)\s*(?:cost-plus|firm|fixed|indefinite|undefinitized|modification|undefinitized\s+contract)",
    re.I,
)
RE_AMOUNT_FALLBACK = re.compile(
    r"(?:awarded|valued at|not[- ]to[- ]exceed)\s*(?:a|an)?\s*\$([\d,]+(?:\.\d+)?)",
    re.I,
)
RE_PRIME = re.compile(
    r"^\s*([A-Z][^,]{2,80}?),\s*([A-Z][^,]+?,\s*[A-Z][a-zA-Z .\-]+?),\s+(?:is|was)\s+awarded",
    re.M,
)
RE_EXPECTED = re.compile(r"expected to be completed by\s+([A-Z][a-z]+\s+\d{4})", re.I)
RE_POP = re.compile(r"([A-Z][A-Za-z .\-']+,\s*[A-Z][A-Za-z .\-]+?)\s*\(([\d.<>]+%)\)")
RE_OTHER_BUCKET = re.compile(
    r"(?:all\s+)?other\s+locations?\s+less than 1%\s*\(([\d.<>]+)%\)", re.I
)
RE_VARIOUS_FOREIGN = re.compile(
    r"(?:and\s+)?various\s+foreign\s+locations?\s*\(([\d.<>]+)%\)", re.I
)
# Single-supplier-no-% format: "Work will be performed in <City>, <State>, and is expected"
# This is common for GFE-component actions where the prime is doing all the work
# at a single site. Treat as 100% at that one location.
RE_POP_SINGLE = re.compile(
    r"Work will be performed (?:in|at)\s+([A-Z][A-Za-z .\-']+,\s*[A-Z][A-Za-z .\-]+?),\s+(?:and\s+is|with\s+(?:expected|an\s+expected))",
    re.I,
)

# Destroyer-specific bucket cities. BIW is at Bath, ME. HII-Ingalls is at
# Pascagoula, MS. (NOTE: do NOT confuse with HII Newport News which builds
# CVN + submarines, not destroyers.)
BIW_CITIES = {"bath, maine", "bath,maine", "brunswick, maine"}  # BIW Brunswick is a small auxiliary site
INGALLS_CITIES = {"pascagoula"}


def daterange(d1, d2):
    cur = d1
    while cur <= d2:
        yield cur
        cur += timedelta(days=1)


def fetch(url, out_path, min_size=200):
    """Cached fetch via curl. Returns True on success."""
    out_path = Path(out_path)
    if out_path.exists() and out_path.stat().st_size >= min_size:
        return True
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            ["curl", "-sS", "--max-time", "20", "-A", USER_AGENT, url, "-o", str(out_path)],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        return False
    if r.returncode != 0:
        return False
    return out_path.exists() and out_path.stat().st_size >= min_size


def html_to_text(html_path):
    with open(html_path) as f:
        html = f.read()
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;|&#160;", " ", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = re.sub(r"\s+", " ", text).strip()
    # strip site navigation prefix — jump to "NAVY" section header
    m = re.search(r"\bNAVY\s+([A-Z])", text)
    if m:
        text = text[m.start() + len("NAVY"):]
    return text


def parse_paragraphs(text):
    marked = SENTINEL.sub(lambda m: m.group(0) + "||PARA_BREAK||", text)
    return [p.strip() for p in marked.split("||PARA_BREAK||") if p.strip()]


def bucket_pop(loc_lower):
    if any(s in loc_lower for s in BIW_CITIES):
        return "biw"
    if any(s in loc_lower for s in INGALLS_CITIES):
        return "ingalls"
    return "other_us"


def parse_action(p, action_date, war_gov_id, source_url):
    piid_m = RE_PIID.search(p)
    amt_m = RE_AMOUNT.search(p) or RE_AMOUNT_FALLBACK.search(p)
    prime_m = RE_PRIME.search(p)
    exp_m = RE_EXPECTED.search(p)

    biw = ingalls = other_us = foreign = 0.0
    pop_parts = []
    for loc, pct in RE_POP.findall(p):
        pct_s = pct.strip().rstrip("%").replace("<", "").replace(">", "")
        try:
            pct_f = float(pct_s)
        except ValueError:
            continue
        pop_parts.append(f"{loc.strip()} {pct.strip()}")
        b = bucket_pop(loc.lower())
        if b == "biw":
            biw += pct_f
        elif b == "ingalls":
            ingalls += pct_f
        else:
            other_us += pct_f
    obm = RE_OTHER_BUCKET.search(p)
    if obm:
        try:
            v = float(obm.group(1).replace("<", "").replace(">", ""))
            other_us += v
            pop_parts.append(f"<other-locations-<1%> {v}%")
        except ValueError:
            pass
    vfm = RE_VARIOUS_FOREIGN.search(p)
    if vfm:
        try:
            v = float(vfm.group(1).replace("<", "").replace(">", ""))
            foreign += v
            pop_parts.append(f"<various-foreign> {v}%")
        except ValueError:
            pass
    # If no city-with-% pattern matched, look for the single-supplier-no-% format
    # and assign 100% to that one site.
    if biw + ingalls + other_us + foreign == 0:
        single = RE_POP_SINGLE.search(p)
        if single:
            loc = single.group(1).strip()
            pop_parts.append(f"{loc} 100% [parsed from single-site]")
            b = bucket_pop(loc.lower())
            if b == "biw":
                biw = 100.0
            elif b == "ingalls":
                ingalls = 100.0
            else:
                other_us = 100.0

    return {
        "action_date": action_date,
        "war_gov_id": war_gov_id,
        "source_url": source_url,
        "piid": piid_m.group(1) if piid_m else "",
        "amount_usd": amt_m.group(1).replace(",", "") if amt_m else "",
        "prime": (prime_m.group(1).strip() if prime_m else ""),
        "prime_location": (prime_m.group(2).strip() if prime_m else ""),
        "expected_completion": exp_m.group(1) if exp_m else "",
        "pop_biw_site_pct": round(biw, 2),
        "pop_ingalls_site_pct": round(ingalls, 2),
        "pop_other_us_pct": round(other_us, 2),
        "pop_foreign_pct": round(foreign, 2),
        "pop_locations_detail": " | ".join(pop_parts),
        "paragraph_text": p,
    }


def load_inscope_piids():
    """Returns the set of in-scope DDG PIIDs from nc_scope_summary.json,
    plus hyphenated equivalents (N0002417C2117 → N00024-17-C-2117)."""
    if not SCOPE_JSON.exists():
        return set()
    with open(SCOPE_JSON) as f:
        d = json.load(f)
    raw = d.get("in_scope_piids") or {}
    if isinstance(raw, dict):
        in_scope = set(raw.keys())
    else:
        in_scope = set(raw)
    hyphenated = set()
    for p in in_scope:
        if len(p) >= 13:
            hyphenated.add(f"{p[:6]}-{p[6:8]}-{p[8]}-{p[9:]}")
    return in_scope | hyphenated


def main():
    in_scope = load_inscope_piids()
    print(f"=== DoD daily contracts POP pull (DESTROYER) ===")
    print(f"Date range: {START_DATE} → {END_DATE} ({(END_DATE-START_DATE).days+1} days)")
    print(f"In-scope DDG PIIDs loaded: {len(in_scope)}")

    contract_urls = []  # (date, war_gov_id, daily_idx_url, contract_url)
    fetched_indexes = 0
    indexes_with_contracts = 0

    for d in daterange(START_DATE, END_DATE):
        idx_fname = f"{d.month:02d}-{d.day:02d}_index.htm"
        idx_url = f"{BASE}/{d.year}/{d.month:02d}/{idx_fname}"
        idx_cache = CACHE_DIR / f"index_{d.isoformat()}.htm"
        if not fetch(idx_url, idx_cache, min_size=200):
            continue
        fetched_indexes += 1
        with open(idx_cache) as f:
            idx_html = f.read()
        hits = re.findall(r'href="(dod-contracts_(\d+)\.htm)"', idx_html)
        if hits:
            indexes_with_contracts += 1
        for href, wgid in hits:
            contract_url = f"{BASE}/{d.year}/{d.month:02d}/{href}"
            contract_urls.append((d.isoformat(), wgid, idx_url, contract_url))
        time.sleep(REQUEST_DELAY_SEC)
        if fetched_indexes % 30 == 0:
            print(f"  ...crawled {fetched_indexes} day-indexes, {indexes_with_contracts} have contract pages, {len(contract_urls)} contract URLs queued")

    print(f"\nTotal: {fetched_indexes} day-indexes fetched, {len(contract_urls)} contract pages to fetch + parse\n")

    all_rows = []
    ddg_paragraphs_count = 0

    for action_date, wgid, _idx_url, c_url in contract_urls:
        c_cache = CACHE_DIR / f"dod-contracts_{wgid}.htm"
        if not fetch(c_url, c_cache, min_size=2000):
            print(f"  fetch failed: {c_url}")
            continue
        time.sleep(REQUEST_DELAY_SEC)
        text = html_to_text(c_cache)
        paragraphs = parse_paragraphs(text)
        ddg_paras = [p for p in paragraphs if DDG_FILTER.search(p)]
        if not ddg_paras:
            continue
        ddg_paragraphs_count += len(ddg_paras)
        # Per-action raw paragraph file
        per_file = OUT_FOLDER / f"{action_date}_dod-contracts_{wgid}.txt"
        if not per_file.exists():
            with open(per_file, "w") as f:
                f.write(f"# {action_date} — globalsecurity.org mirror of war.gov article {wgid}\n")
                f.write(f"# Source: {c_url}\n\n")
                for i, p in enumerate(ddg_paras, 1):
                    f.write(f"## Destroyer paragraph {i}\n\n{p}\n\n")
        for p in ddg_paras:
            row = parse_action(p, action_date, wgid, c_url)
            row["in_scope_ddg_piid"] = "yes" if row["piid"] in in_scope else "no"
            all_rows.append(row)

    fields = [
        "action_date", "war_gov_id", "source_url", "piid", "in_scope_ddg_piid",
        "amount_usd", "prime", "prime_location", "expected_completion",
        "pop_biw_site_pct", "pop_ingalls_site_pct", "pop_other_us_pct", "pop_foreign_pct",
        "pop_locations_detail", "paragraph_text",
    ]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in all_rows:
            w.writerow(r)

    print(f"\nWrote {OUT_CSV}")
    print(f"  {len(all_rows)} destroyer action rows ({ddg_paragraphs_count} ddg paragraphs across "
          f"{len(set((r['action_date'],r['war_gov_id']) for r in all_rows))} distinct contract pages)")

    in_scope_rows = [r for r in all_rows if r["in_scope_ddg_piid"] == "yes"]
    print(f"  {len(in_scope_rows)} of {len(all_rows)} actions match the in-scope DDG PIID list ({len(in_scope)} PIIDs)")

    # Top-line summary
    if all_rows:
        print("\nTop 10 actions by $ amount:")
        sorted_rows = sorted(
            all_rows,
            key=lambda r: -(float(r["amount_usd"]) if r["amount_usd"] else 0),
        )
        print(f"  {'date':<11} {'piid':<19} {'$M':>10} {'BIW%':>6} {'Ing%':>6} {'Other%':>7}  in-scope")
        for r in sorted_rows[:10]:
            amt_m = float(r["amount_usd"])/1e6 if r["amount_usd"] else 0
            print(f"  {r['action_date']:<11} {r['piid']:<19} {amt_m:>10.1f} {r['pop_biw_site_pct']:>6} {r['pop_ingalls_site_pct']:>6} {r['pop_other_us_pct']:>7}  {r['in_scope_ddg_piid']}")


if __name__ == "__main__":
    main()
