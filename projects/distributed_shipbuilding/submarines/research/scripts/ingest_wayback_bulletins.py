#!/usr/bin/env python3
"""
Ingest Wayback-cached defense.gov bulletin HTML files into
extracted/dod_announcement_pop.csv.

Cached files live at:
  research_primary_sources/dod_announcement_pop/cache_wayback/defense_<YYYY-MM-DD>_<aid>.html

Schema matches what pull_dod_announcements_pop.py produces. Re-running is
safe — existing (action_date, war_gov_id) keys are deduped.
"""
import csv
import json
import os
import re
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/submarine_outsourced_work")
CACHE = REPO / "research_primary_sources" / "dod_announcement_pop" / "cache_wayback"
OUT_FOLDER = REPO / "research_primary_sources" / "dod_announcement_pop"
CSV_PATH = REPO / "extracted" / "dod_announcement_pop.csv"
SCOPE_JSON = REPO / "extracted" / "nc_scope_summary.json"

SUB_FILTER = re.compile(
    r"\b(virginia[- ]class|columbia[- ]class|submarine|electric boat|N00024-\d{2}-[A-Z]-\d{4}|bechtel plant machinery|naval nuclear propulsion)\b",
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
RE_OTHER_BUCKET = re.compile(r"(?:all\s+)?other\s+locations?\s+less than 1%\s*\(([\d.<>]+)%\)", re.I)
RE_VARIOUS_FOREIGN = re.compile(r"(?:and\s+)?various\s+foreign\s+locations?\s*\(([\d.<>]+)%\)", re.I)

EB_CITIES = {"groton", "quonset point", "north kingstown"}
HII_CITIES = {"newport news"}


def html_to_text(path):
    """Returns (body_text_navy_stripped, full_text_with_title)."""
    html = Path(path).read_text(errors="replace")
    html = re.sub(r"<!-- BEGIN WAYBACK TOOLBAR INSERT[\s\S]*?<!-- END WAYBACK TOOLBAR INSERT -->", " ", html)
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;|&#160;", " ", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&rsquo;", "'").replace("&lsquo;", "'").replace("&ldquo;", '"').replace("&rdquo;", '"')
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    full = text
    m = re.search(r"\bNAVY\s+[A-Z]", text)
    if m:
        text = text[m.start() + len("NAVY"):]
    return text, full


def parse_paragraphs(text):
    marked = SENTINEL.sub(lambda mm: mm.group(0) + "||PARA_BREAK||", text)
    return [p.strip() for p in marked.split("||PARA_BREAK||") if p.strip()]


def bucket(loc_lower):
    if any(s in loc_lower for s in EB_CITIES):
        return "eb"
    if any(s in loc_lower for s in HII_CITIES):
        return "hii"
    return "other_us"


def parse_action(p, action_date, war_gov_id, source_url):
    piid_m = RE_PIID.search(p)
    amt_m = RE_AMOUNT.search(p) or RE_AMOUNT_FALLBACK.search(p)
    prime_m = RE_PRIME.search(p)
    exp_m = RE_EXPECTED.search(p)
    eb = hii = other_us = foreign = 0.0
    pop_parts = []
    for loc, pct in RE_POP.findall(p):
        pct_s = pct.strip().rstrip("%").replace("<", "").replace(">", "")
        try:
            v = float(pct_s)
        except ValueError:
            continue
        pop_parts.append(f"{loc.strip()} {pct.strip()}")
        b = bucket(loc.lower())
        if b == "eb": eb += v
        elif b == "hii": hii += v
        else: other_us += v
    obm = RE_OTHER_BUCKET.search(p)
    if obm:
        try:
            v = float(obm.group(1).replace("<", "").replace(">", ""))
            other_us += v
            pop_parts.append(f"<other-locations-<1%> {v}%")
        except ValueError: pass
    vfm = RE_VARIOUS_FOREIGN.search(p)
    if vfm:
        try:
            v = float(vfm.group(1).replace("<", "").replace(">", ""))
            foreign += v
            pop_parts.append(f"<various-foreign> {v}%")
        except ValueError: pass
    return {
        "action_date": action_date,
        "war_gov_id": war_gov_id,
        "source_url": source_url,
        "piid": piid_m.group(1) if piid_m else "",
        "amount_usd": amt_m.group(1).replace(",", "") if amt_m else "",
        "prime": (prime_m.group(1).strip() if prime_m else ""),
        "prime_location": (prime_m.group(2).strip() if prime_m else ""),
        "expected_completion": exp_m.group(1) if exp_m else "",
        "pop_eb_site_pct": round(eb, 2),
        "pop_hii_site_pct": round(hii, 2),
        "pop_other_us_pct": round(other_us, 2),
        "pop_foreign_pct": round(foreign, 2),
        "pop_locations_detail": " | ".join(pop_parts),
        "paragraph_text": p,
    }


def load_inscope():
    if not SCOPE_JSON.exists(): return set()
    d = json.loads(SCOPE_JSON.read_text())
    in_scope = set(d.get("in_scope_piids") or [])
    out = set(in_scope)
    for p in in_scope:
        if len(p) >= 13:
            out.add(f"{p[:6]}-{p[6:8]}-{p[8]}-{p[9:]}")
    return out


def main():
    in_scope = load_inscope()
    with open(CSV_PATH) as f:
        existing_rows = list(csv.DictReader(f))
    existing_keys = {(r["action_date"], r["war_gov_id"], r["paragraph_text"][:120]) for r in existing_rows}
    fields = list(existing_rows[0].keys())

    MONTH_MAP = {m: f"{i:02d}" for i, m in enumerate(
        ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], start=1)}
    RE_DATE_IN_TITLE = re.compile(
        r"Contracts\s+for\s+([A-Z][a-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})", re.I)

    def extract_date(text, fallback_year):
        m = RE_DATE_IN_TITLE.search(text)
        if not m:
            return f"{fallback_year}-01-01"  # crude fallback
        mon = MONTH_MAP.get(m.group(1)[:3].lower())
        if not mon:
            return f"{fallback_year}-01-01"
        return f"{m.group(3)}-{mon}-{int(m.group(2)):02d}"

    new_rows = []
    for fp in sorted(CACHE.glob("defense_*.html")):
        # Two filename formats:
        #   defense_YYYY-MM-DD_<aid>.html (date known from filename)
        #   defense_YYYY_<aid>.html       (only year — extract date from body)
        m_full = re.match(r"defense_(\d{4}-\d{2}-\d{2})_(\d+)\.html$", fp.name)
        m_year = re.match(r"defense_(\d{4})_(\d+)\.html$", fp.name)
        text, full_text = html_to_text(fp)
        if m_full:
            date, aid = m_full.group(1), m_full.group(2)
        elif m_year:
            aid = m_year.group(2)
            # Try date extraction from the FULL text (title is before NAVY marker)
            date = extract_date(full_text, m_year.group(1))
        else:
            continue
        source_url = f"https://www.defense.gov/News/Contracts/Contract/Article/{aid}/  (via web.archive.org)"
        paras = parse_paragraphs(text)
        sub_paras = [p for p in paras if SUB_FILTER.search(p)]
        # Also save per-action txt
        if sub_paras:
            per_file = OUT_FOLDER / f"{date}_dod-contracts_{aid}.txt"
            with open(per_file, "w") as f:
                f.write(f"# {date} — defense.gov article {aid} (fetched via Wayback Machine)\n")
                f.write(f"# Source: {source_url}\n\n")
                for i, p in enumerate(sub_paras, 1):
                    f.write(f"## Submarine paragraph {i}\n\n{p}\n\n")
        kept_this = 0
        for p in sub_paras:
            row = parse_action(p, date, aid, source_url)
            row["in_scope_17_piids"] = "yes" if row["piid"] in in_scope else "no"
            # Fill in any extra columns the existing CSV has (program_primary etc.) with empties
            for col in fields:
                row.setdefault(col, "")
            key = (row["action_date"], row["war_gov_id"], row["paragraph_text"][:120])
            if key in existing_keys:
                continue
            existing_keys.add(key)
            new_rows.append(row)
            kept_this += 1
        print(f"  {date} aid={aid}: {len(sub_paras)} sub paragraphs, {kept_this} new rows appended")

    if not new_rows:
        print("No new rows to add.")
        return

    all_rows = existing_rows + new_rows
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in all_rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"\nAppended {len(new_rows)} new rows. CSV now has {len(all_rows)} total rows.")
    for r in new_rows:
        amt = float(r["amount_usd"])/1e6 if r["amount_usd"] else 0
        print(f"  {r['action_date']} {r['piid']:<19} ${amt:>9.1f}M  EB%={r['pop_eb_site_pct']} HII%={r['pop_hii_site_pct']} Other%={r['pop_other_us_pct']}")


if __name__ == "__main__":
    main()
