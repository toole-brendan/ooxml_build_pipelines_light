#!/usr/bin/env python3
"""
Scrape HII earnings call transcripts from public sources (Motley Fool, Insider Monkey)
and save to hii_earnings_transcripts/.

For each URL:
  - Fetch with browser User-Agent
  - Strip HTML to plain text (preserve paragraph breaks)
  - Save .txt + .meta.json (with source, URL, FY/Q, fetch date)

Build an index CSV at the end.
"""
import csv
import json
import os
import re
import subprocess
import time
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/submarine_outsourced_work")
OUT = REPO / "hii_earnings_transcripts"
OUT.mkdir(exist_ok=True)
RAW = OUT / "_raw_html"
RAW.mkdir(exist_ok=True)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# (calendar FY, quarter, source, URL, call_date)
# Sourced from WebSearch — Insider Monkey + Motley Fool are scrape-friendly with browser UA
TRANSCRIPT_URLS = [
    # ===== FY2026 =====
    (2026, 1, "fool", "https://www.fool.com/earnings/call-transcripts/2026/05/05/hii-q1-2026-earnings-call-transcript/", "2026-05-05"),
    (2026, 1, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q1-2026-earnings-call-transcript-1754830/", "2026-05-05"),

    # ===== FY2025 =====
    (2025, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2026/02/05/huntington-ingalls-hii-earnings-call-transcript/", "2026-02-05"),
    (2025, 4, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q4-2025-earnings-call-transcript-1690272/", "2026-02-05"),
    (2025, 3, "fool", "https://www.fool.com/earnings/call-transcripts/2025/10/30/huntington-ingalls-hii-earnings-call-transcript/", "2025-10-30"),
    (2025, 2, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q2-2025-earnings-call-transcript-1581886/", "2025-07-31"),
    (2025, 1, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q1-2025-earnings-call-transcript-1523872/", "2025-05-01"),

    # ===== FY2024 =====
    (2024, 4, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q4-2024-earnings-call-transcript-1446124/", "2025-02-06"),
    (2024, 3, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q3-2024-earnings-call-transcript-1384117/", "2024-10-31"),
    (2024, 2, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q2-2024-earnings-call-transcript-1329301/", "2024-08-01"),
    # Q1 2024 — MarketScreener returns 403; Yahoo Finance republishes Insider Monkey
    (2024, 1, "yahoo_partial", "https://finance.yahoo.com/news/huntington-ingalls-industries-inc-nyse-153437306.html", "2024-05-02"),

    # ===== FY2023 =====
    (2023, 4, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q4-2023-earnings-call-transcript-1252909/", "2024-02-01"),
    (2023, 3, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q3-2023-earnings-call-transcript-1216238/", "2023-11-02"),
    (2023, 2, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q2-2023-earnings-call-transcript-1177069/", "2023-08-03"),
    (2023, 1, "insidermonkey", "https://www.insidermonkey.com/blog/huntington-ingalls-industries-inc-nysehii-q1-2023-earnings-call-transcript-1146780/", "2023-05-04"),

    # ===== FY2022 =====
    # No fully-free transcripts found for FY2022 Q1/Q2/Q3 (Seeking Alpha paywall,
    # MarketBeat/MarketScreener paywall, mlq.ai 403). Yahoo has Q4 2022 partial
    # (prepared remarks only — Q&A behind "click to continue" link to Insider Monkey).
    (2022, 4, "yahoo_partial", "https://finance.yahoo.com/news/huntington-ingalls-industries-inc-nyse-193027426.html", "2023-02-09"),

    # ===== Historical (pre-FY22 window) — context only =====
    (2021, 3, "fool", "https://www.fool.com/earnings/call-transcripts/2021/11/06/huntington-ingalls-industries-inc-hii-q3-2021-earn/", "2021-11-05"),
    (2021, 2, "fool", "https://www.fool.com/earnings/call-transcripts/2021/08/05/huntington-ingalls-industries-inc-hii-q2-2021-earn/", "2021-08-05"),
    (2021, 1, "fool", "https://www.fool.com/earnings/call-transcripts/2021/05/07/huntington-ingalls-industries-inc-hii-q1-2021-earn/", "2021-05-06"),
    (2020, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2021/02/11/huntington-ingalls-industries-inc-hii-q4-2020-earn/", "2021-02-11"),
    (2020, 3, "fool", "https://www.fool.com/earnings/call-transcripts/2020/11/05/huntington-ingalls-industries-inc-hii-q3-2020-earn/", "2020-11-05"),
    (2020, 2, "fool", "https://www.fool.com/earnings/call-transcripts/2020/08/06/huntington-ingalls-industries-inc-hii-q2-2020-earn.aspx", "2020-08-06"),
    (2019, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2020/02/13/huntington-ingalls-industries-inc-hii-q4-2019-earn.aspx", "2020-02-13"),
]


class TextExtractor(HTMLParser):
    """Strip HTML to plain text, preserving paragraph structure."""
    def __init__(self):
        super().__init__()
        self.out = []
        self.skip_depth = 0
        self.SKIP_TAGS = {"script", "style", "noscript", "nav", "footer", "header",
                          "aside", "form", "iframe"}

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        elif tag in ("p", "br", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "li"):
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.out.append(data)


def clean_text(html):
    """HTML → clean plain text."""
    p = TextExtractor()
    p.feed(html)
    text = "".join(p.out)
    # Collapse whitespace; preserve paragraph breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def extract_transcript_section(text, source):
    """Trim the bottom of the page (ads, related articles, comments). Do NOT trim the
    top — site headers are small and trimming risks cutting the prepared-remarks
    section.

    The earlier heuristic of starting at the first 'Prepared Remarks' / 'Operator:' /
    'Call participants' was unreliable: those phrases also appear in body text (e.g.,
    "In our prepared remarks, we mentioned..."), causing over-clipping.
    """
    end_markers = [
        r"More\s+From\s+The\s+Motley\s+Fool",
        r"Duration:\s*\d+\s*minutes",
        r"This article is a transcript",
        r"Disclosure:",
        r"Read the original article",
        r"Suggested Articles:",
        r"Click to continue reading",
        r"Click here to see",
        r"Subscribe to Premium",
    ]
    end = len(text)
    for pat in end_markers:
        m = re.search(pat, text, re.I)
        if m and m.start() > 5000:  # only trim if we're past the meaningful content
            end = min(end, m.start())
    return text[:end].strip()


def fetch(url):
    """curl with browser UA. Returns html string or None."""
    try:
        result = subprocess.run(
            ["curl", "-sS", "--max-time", "30", "-L", "-A", UA, url],
            capture_output=True, text=True, timeout=45,
        )
        if result.returncode != 0 or len(result.stdout) < 5000:
            return None
        return result.stdout
    except Exception:
        return None


def main():
    print(f"=== Scraping HII transcripts ===\n")
    saved = []
    failed = []

    for fy, q, source, url, call_date in TRANSCRIPT_URLS:
        key = f"FY{fy}_Q{q}_{source}"
        txt_path = OUT / f"{key}.txt"
        meta_path = OUT / f"{key}.meta.json"
        raw_path = RAW / f"{key}.html"

        if txt_path.exists() and txt_path.stat().st_size > 5000:
            print(f"  [{key}] already saved, skipping")
            saved.append((fy, q, source, url, call_date, txt_path.stat().st_size))
            continue

        print(f"  [{key}] fetching {url[:80]}…", flush=True)
        html = fetch(url)
        if html is None:
            print(f"    ✗ failed")
            failed.append((fy, q, source, url))
            continue

        # Save raw HTML for re-parsing later if needed
        raw_path.write_text(html)
        time.sleep(0.5)  # be polite

        # Extract + clip
        full_text = clean_text(html)
        transcript = extract_transcript_section(full_text, source)
        if len(transcript) < 5000:
            print(f"    ⚠ extracted only {len(transcript)} chars — saving anyway")
        txt_path.write_text(transcript)

        # Build metadata
        # Count program mentions
        prog_mentions = {
            kw: len(re.findall(r"\b" + re.escape(kw) + r"\b", transcript, re.I))
            for kw in ("Virginia", "Columbia", "submarine", "Block IV", "Block V",
                       "Block VI", "CVN", "RCOH", "Electric Boat", "teaming")
        }
        # Find any $ figures near "submarine" keyword
        sub_dollar = []
        for m in re.finditer(r"submarine[^.]*\$[\d,\.]+\s*(?:billion|million|B|M)", transcript, re.I):
            sub_dollar.append(m.group(0)[:200])
        # Also find $ figures near "Virginia" / "Columbia"
        for kw in ("Virginia", "Columbia"):
            for m in re.finditer(re.escape(kw) + r"[^.]*\$[\d,\.]+\s*(?:billion|million|B|M)", transcript, re.I):
                sub_dollar.append(m.group(0)[:200])

        meta = {
            "fy": fy,
            "quarter": q,
            "source": source,
            "url": url,
            "call_date": call_date,
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
            "txt_size": len(transcript),
            "raw_html_size": len(html),
            "program_mention_counts": prog_mentions,
            "submarine_dollar_snippets": sub_dollar[:10],
        }
        meta_path.write_text(json.dumps(meta, indent=2))

        print(f"    ✓ saved {len(transcript):,} chars to {txt_path.name}")
        print(f"      program mentions: Va={prog_mentions['Virginia']} "
              f"Col={prog_mentions['Columbia']} sub={prog_mentions['submarine']} "
              f"CVN={prog_mentions['CVN']}")
        saved.append((fy, q, source, url, call_date, len(transcript)))

    # Write index CSV
    index_path = OUT / "_index.csv"
    with open(index_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["fy", "quarter", "call_date", "source", "url", "txt_size_chars", "filename"])
        for fy, q, source, url, call_date, size in sorted(saved):
            fname = f"FY{fy}_Q{q}_{source}.txt"
            w.writerow([fy, q, call_date, source, url, size, fname])

    print(f"\n=== DONE ===")
    print(f"  Saved {len(saved)} transcripts; {len(failed)} failed")
    print(f"  Index: {index_path}")
    if failed:
        print(f"\n  Failed URLs:")
        for fy, q, src, url in failed:
            print(f"    FY{fy} Q{q} ({src}): {url}")


if __name__ == "__main__":
    main()
