#!/usr/bin/env python3
"""
Search NewsAPI.ai (Event Registry) for press articles containing executive
quotes about HII Ingalls + GD-BIW outsourcing / supplier content / vertical
integration / distributed shipbuilding.

Endpoint:  https://eventregistry.org/api/v1/article/getArticles
Auth:      apiKey in POST body
Docs:      https://newsapi.ai/documentation

Strategy: run a small set of targeted queries, save full raw responses, then
post-filter article BODY text for actual quote sentences. Output to:
  news_research/<slug>.json    Full raw API response per query
  news_research/_quotes.csv    Extracted quote-bearing sentences
  news_research/_quotes.md     Human-readable digest
"""
import csv
import json
import re
import socket
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# IPv4 monkeypatch (consistent with our SAM scripts)
_orig = socket.getaddrinfo
socket.getaddrinfo = lambda host, port, family=0, type=0, proto=0, flags=0: \
    _orig(host, port, socket.AF_INET, type, proto, flags)

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT = REPO / "news_research"
OUT.mkdir(exist_ok=True)

ENDPOINT = "https://eventregistry.org/api/v1/article/getArticles"
HDRS = {"User-Agent": "ddg-research/1.0", "Content-Type": "application/json"}


def load_key():
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith("NEWSAPI_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("NEWSAPI_KEY not in .env")


def post_json(url, payload, tries=2):
    body = json.dumps(payload).encode("utf-8")
    for attempt in range(tries):
        try:
            req = Request(url, data=body, headers=HDRS, method="POST")
            with urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")[:500]
            print(f"  HTTP {e.code}: {err_body}", flush=True)
            if attempt == tries - 1:
                return {"_error": f"HTTP {e.code}: {err_body}"}
            time.sleep(2)
        except Exception as e:
            if attempt == tries - 1:
                return {"_error": str(e)}
            time.sleep(2)
    return {"_error": "exhausted retries"}


# Queries — kept small to conserve API tokens. Each query is run separately so
# we get focused results per topic. NewsAPI charges per article returned.
QUERIES = [
    # Round 2 — target authoritative content-share disclosures
    ("ingalls_suppliers_count", {
        "keyword": ["Ingalls", "suppliers"],
        "keywordOper": "and",
        "lang": "eng",
        "articlesSortBy": "rel",
        "articlesCount": 30,
    }),
    ("hii_supplier_base_size", {
        "keyword": ["Huntington Ingalls", "supplier base"],
        "keywordOper": "and",
        "lang": "eng",
        "articlesSortBy": "rel",
        "articlesCount": 30,
    }),
    ("hii_small_business", {
        "keyword": ["Huntington Ingalls", "small business"],
        "keywordOper": "and",
        "lang": "eng",
        "articlesSortBy": "rel",
        "articlesCount": 30,
    }),
    ("bath_iron_supplier_count", {
        "keyword": ["Bath Iron Works", "suppliers"],
        "keywordOper": "and",
        "lang": "eng",
        "articlesSortBy": "rel",
        "articlesCount": 30,
    }),
    ("destroyer_supply_chain", {
        "keyword": ["destroyer", "supply chain"],
        "keywordOper": "and",
        "lang": "eng",
        "articlesSortBy": "rel",
        "articlesCount": 30,
    }),
    ("ddg51_industrial_base", {
        "keyword": ["DDG", "industrial base"],
        "keywordOper": "and",
        "lang": "eng",
        "articlesSortBy": "rel",
        "articlesCount": 30,
    }),
    ("csis_destroyer_supplier", {
        "keyword": ["CSIS", "destroyer", "supplier"],
        "keywordOper": "and",
        "lang": "eng",
        "articlesSortBy": "rel",
        "articlesCount": 30,
    }),
    ("congressional_research_destroyer", {
        "keyword": ["Congressional Research Service", "DDG"],
        "keywordOper": "and",
        "lang": "eng",
        "articlesSortBy": "rel",
        "articlesCount": 30,
    }),
]


# Patterns to identify high-value quote sentences in article bodies
QUOTE_PATTERNS = [
    ("outsource_pct", re.compile(r"outsourc[a-z]*[^.]{0,200}\d+\s*(?:percent|%)", re.I)),
    ("pct_outsource", re.compile(r"\d+\s*(?:percent|%)[^.]{0,80}(?:outsourc|supplier|supply chain|subcontract|vendors?)", re.I)),
    ("supplier_pct", re.compile(r"\b(?:supplier|suppliers|supply chain|sub[-]?tier|subcontract|subcontractor)[^.]{0,200}\d+\s*(?:percent|%)", re.I)),
    ("supplier_dollar", re.compile(r"(?:supplier|supply chain|subcontract|vendors?)[^.]{0,150}\$\s*[\d,\.]+\s*(?:billion|million|B|M)\b", re.I)),
    ("dollar_supplier", re.compile(r"\$\s*[\d,\.]+\s*(?:billion|million|B|M)[^.]{0,80}(?:supplier|supply chain|subcontract|vendors?)", re.I)),
    ("vertical_integration", re.compile(r"vertical[a-z]* integrat", re.I)),
    ("ddg_supplier_count", re.compile(r"\d+(?:,\d+)?\s+(?:suppliers|subcontractors|vendors|small businesses)", re.I)),
    ("hours_outsourced", re.compile(r"\d[\d,.]*\s*(?:million|thousand)?\s*hours?[^.]{0,80}(?:outsourc|distributed|subcontract)", re.I)),
    ("distributed_ship", re.compile(r"distributed\s+shipbuilding", re.I)),
]


def extract_quotes(article):
    """Return list of quote-rich snippets from an article body."""
    body = article.get("body") or ""
    if not body:
        return []
    snippets = []
    for cat, pat in QUOTE_PATTERNS:
        for m in pat.finditer(body):
            start = max(0, m.start() - 200)
            end = min(len(body), m.end() + 400)
            snippet = body[start:end].strip()
            # Trim to sentence boundaries
            fp = snippet.find(". ")
            if 0 < fp < 200:
                snippet = snippet[fp+2:]
            lp = snippet.rfind(".")
            if lp > 0:
                snippet = snippet[:lp+1]
            snippets.append({
                "category": cat,
                "matched": m.group(0)[:200],
                "snippet": snippet[:800],
            })
    return snippets


def main():
    api_key = load_key()
    print(f"NewsAPI key prefix: {api_key[:8]}...")
    print()

    all_quotes = []
    for slug, query in QUERIES:
        print(f"[{slug}] query: {query['keyword']}")
        payload = {
            **query,
            "resultType": "articles",
            "includeArticleBody": True,
            "includeArticleConcepts": False,
            "includeArticleCategories": False,
            "includeArticleImage": False,
            "apiKey": api_key,
        }
        data = post_json(ENDPOINT, payload)
        out_path = OUT / f"{slug}.json"
        with open(out_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

        if "_error" in data:
            print(f"  ERROR: {data['_error']}")
            continue

        # NewsAPI returns either {"articles": {"results": [...]}} or sometimes {"articles": [...]}
        articles_obj = data.get("articles", {})
        if isinstance(articles_obj, dict):
            articles = articles_obj.get("results", [])
            total = articles_obj.get("totalResults", "?")
        else:
            articles = articles_obj if isinstance(articles_obj, list) else []
            total = len(articles)

        print(f"  -> {len(articles)} articles returned (total available: {total})")

        for a in articles:
            snips = extract_quotes(a)
            for s in snips:
                all_quotes.append({
                    "query_slug": slug,
                    "article_title": a.get("title", "")[:200],
                    "article_date": a.get("date", ""),
                    "article_source": (a.get("source") or {}).get("title", ""),
                    "article_url": a.get("url", ""),
                    **s,
                })
        print(f"  -> {sum(1 for q in all_quotes if q['query_slug']==slug)} total quotes extracted")
        time.sleep(0.5)

    # Write CSV
    if all_quotes:
        csv_path = OUT / "_quotes.csv"
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=[
                "query_slug", "article_date", "article_source", "article_title",
                "article_url", "category", "matched", "snippet"
            ])
            w.writeheader()
            for q in all_quotes:
                w.writerow(q)
        print(f"\nWrote {csv_path}  ({len(all_quotes)} quote snippets)")

        # Markdown digest
        md = ["# News quotes on DDG outsourcing / supplier content\n\n"]
        md.append(f"Auto-mined from NewsAPI.ai. {len(all_quotes)} snippets across {len(QUERIES)} queries.\n\n")
        # Group by category
        from collections import defaultdict
        by_cat = defaultdict(list)
        for q in all_quotes:
            by_cat[q["category"]].append(q)
        for cat in ("outsource_pct", "pct_outsource", "supplier_pct", "supplier_dollar",
                    "dollar_supplier", "hours_outsourced", "vertical_integration",
                    "ddg_supplier_count", "distributed_ship"):
            hits = by_cat.get(cat, [])
            if not hits: continue
            md.append(f"## {cat} ({len(hits)} hits)\n\n")
            seen = set()
            for q in hits:
                key = q["snippet"][:100]
                if key in seen: continue
                seen.add(key)
                md.append(f"### {q['article_source']} — {q['article_date']}\n")
                md.append(f"**{q['article_title']}**\n\n")
                md.append(f"> {q['snippet']}\n\n")
                md.append(f"[link]({q['article_url']}) — matched: `{q['matched']}`\n\n---\n\n")

        md_path = OUT / "_quotes.md"
        md_path.write_text("".join(md))
        print(f"Wrote {md_path}")

        # Stats
        from collections import Counter
        print(f"\nBy category: {dict(Counter(q['category'] for q in all_quotes).most_common())}")
        print(f"By source: {dict(Counter(q['article_source'] for q in all_quotes).most_common(8))}")


if __name__ == "__main__":
    main()
