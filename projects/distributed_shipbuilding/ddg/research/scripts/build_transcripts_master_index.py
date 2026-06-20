#!/usr/bin/env python3
"""
Walk every *_earnings_transcripts/ dir and build a unified master index CSV.
Columns: ticker, fy, quarter, call_date, source, url, txt_size,
         ddg_mention_count, dollar_snippet_count, filename

Output: extracted/all_transcripts_index.csv
"""
import csv
import json
import re
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT = REPO / "extracted" / "all_transcripts_index.csv"
OUT.parent.mkdir(exist_ok=True)

# Map of dir-name -> ticker label
TICKER_DIRS = {
    "gd_earnings_transcripts": "GD",
    "hii_earnings_transcripts": "HII",
    "lmt_earnings_transcripts": "LMT",
    "rtx_earnings_transcripts": "RTX",
    "noc_earnings_transcripts": "NOC",
    "lhx_earnings_transcripts": "LHX",
    "bae_earnings_transcripts": "BAE",
}

# DDG-mention keywords (across all tickers) — used as a unified relevance metric
DDG_KEYWORDS = (
    "DDG", "destroyer", "Arleigh", "Flight III", "Aegis",
    "Mk 41", "MK 41", "Mk 45", "MK 45", "VLS", "SPY-6",
    "Bath", "BIW", "Ingalls", "Marine Systems",
    "naval", "Navy",
)


def count_ddg_mentions(text):
    total = 0
    for kw in DDG_KEYWORDS:
        total += len(re.findall(r"\b" + re.escape(kw) + r"\b", text, re.I))
    return total


def main():
    rows = []
    for dir_name, ticker in TICKER_DIRS.items():
        d = REPO / dir_name
        if not d.exists():
            continue
        for txt in sorted(d.glob("FY*.txt")):
            if txt.name.startswith("_"):
                continue
            m = re.match(r"FY(\d{4})_Q(\d+)_(\w+)", txt.stem)
            if not m:
                continue
            fy, q, source = int(m.group(1)), int(m.group(2)), m.group(3)
            meta_path = txt.with_suffix(".meta.json")
            url, call_date = "", ""
            dollar_snippets = 0
            if meta_path.exists():
                try:
                    meta = json.loads(meta_path.read_text())
                    url = meta.get("url", "")
                    call_date = meta.get("call_date", "")
                    dollar_snippets = len(meta.get("ddg_dollar_snippets", []))
                except Exception:
                    pass
            try:
                text = txt.read_text(errors="replace")
            except Exception:
                text = ""
            ddg = count_ddg_mentions(text)
            rows.append({
                "ticker": ticker, "fy": fy, "quarter": q,
                "call_date": call_date, "source": source,
                "url": url, "txt_size": len(text),
                "ddg_mention_count": ddg,
                "dollar_snippet_count": dollar_snippets,
                "filename": txt.name,
            })

    rows.sort(key=lambda r: (r["ticker"], r["fy"], r["quarter"]))

    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "ticker", "fy", "quarter", "call_date", "source", "url",
            "txt_size", "ddg_mention_count", "dollar_snippet_count", "filename",
        ])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"Wrote {OUT} ({len(rows)} transcripts)")
    # Brief per-ticker summary
    print("\nPer-ticker counts:")
    by_t = {}
    for r in rows:
        by_t.setdefault(r["ticker"], []).append(r)
    for t, lst in sorted(by_t.items()):
        total_ddg = sum(r["ddg_mention_count"] for r in lst)
        total_chars = sum(r["txt_size"] for r in lst)
        print(f"  {t}: {len(lst)} transcripts  {total_chars:,} chars  {total_ddg} DDG/naval mentions")


if __name__ == "__main__":
    main()
