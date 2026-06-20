#!/usr/bin/env python3
"""
Scrape General Dynamics earnings call transcripts from public sources (Motley Fool)
and save to gd_earnings_transcripts/.

For each URL:
  - Fetch with browser User-Agent (curl)
  - Strip HTML to plain text (preserve paragraph breaks)
  - Save .txt + .meta.json with DDG/BIW/Marine-Systems keyword counts
  - Pull dollar snippets near "DDG", "Bath", "BIW", "destroyer", "Aegis", "Marine Systems"

Build an index CSV at the end.

URL pattern: https://www.fool.com/earnings/call-transcripts/YYYY/MM/DD/general-dynamics-gd-qN-YYYY-earnings-{call-transcript,transcript}/
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

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT = REPO / "gd_earnings_transcripts"
OUT.mkdir(exist_ok=True)
RAW = OUT / "_raw_html"
RAW.mkdir(exist_ok=True)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# (calendar FY, quarter, source, URL, call_date) — URLs verified via search 2026-05-23.
# Filed quarterly; Q1=late Apr, Q2=late Jul, Q3=late Oct, Q4=late Jan.
TRANSCRIPT_URLS = [
    # FY2026
    (2026, 1, "fool", "https://www.fool.com/earnings/call-transcripts/2026/04/29/general-dynamics-gd-q1-2026-earnings-transcript/", "2026-04-29"),
    # FY2025
    (2025, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2026/01/28/general-dynamics-gd-q4-2025-earnings-transcript/", "2026-01-28"),
    (2025, 2, "fool", "https://www.fool.com/earnings/call-transcripts/2025/08/05/general-dynamics-gd-q2-2025-earnings-transcript/", "2025-08-05"),
    # FY2024
    (2024, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2025/01/29/general-dynamics-gd-q4-2024-earnings-call-transcri/", "2025-01-29"),
    (2024, 3, "fool", "https://www.fool.com/earnings/call-transcripts/2024/10/23/general-dynamics-gd-q3-2024-earnings-call-transcri/", "2024-10-23"),
    (2024, 2, "fool", "https://www.fool.com/earnings/call-transcripts/2024/07/24/general-dynamics-gd-q2-2024-earnings-call-transcri/", "2024-07-24"),
    (2024, 1, "fool", "https://www.fool.com/earnings/call-transcripts/2024/04/24/general-dynamics-gd-q1-2024-earnings-call-transcri/", "2024-04-24"),
    # FY2023
    (2023, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2024/01/24/general-dynamics-gd-q4-2023-earnings-call-transcri/", "2024-01-24"),
    (2023, 3, "fool", "https://www.fool.com/earnings/call-transcripts/2023/10/25/general-dynamics-gd-q3-2023-earnings-call-transcri/", "2023-10-25"),
    (2023, 2, "fool", "https://www.fool.com/earnings/call-transcripts/2023/07/26/general-dynamics-gd-q2-2023-earnings-call-transcri/", "2023-07-26"),
    # Q1 2023 transcript URL not surfaced in search — leave gap; can hand-add later
    # FY2022
    (2022, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2023/01/25/general-dynamics-gd-q4-2022-earnings-call-transcri/", "2023-01-25"),
    (2022, 3, "fool", "https://www.fool.com/earnings/call-transcripts/2022/10/26/general-dynamics-gd-q3-2022-earnings-call-transcri/", "2022-10-26"),
    (2022, 2, "fool", "https://www.fool.com/earnings/call-transcripts/2022/07/27/general-dynamics-gd-q2-2022-earnings-call-transcri/", "2022-07-27"),
    (2022, 1, "fool", "https://www.fool.com/earnings/call-transcripts/2022/04/27/general-dynamics-gd-q1-2022-earnings-call-transcri/", "2022-04-27"),
    # FY2021
    (2021, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2022/01/26/general-dynamics-gd-q4-2021-earnings-call-transcri/", "2022-01-26"),
    (2021, 3, "fool", "https://www.fool.com/earnings/call-transcripts/2021/10/28/general-dynamics-gd-q3-2021-earnings-call-transcri/", "2021-10-28"),
    (2021, 2, "fool", "https://www.fool.com/earnings/call-transcripts/2021/07/29/general-dynamics-gd-q2-2021-earnings-call-transcri/", "2021-07-29"),
    (2021, 1, "fool", "https://www.fool.com/earnings/call-transcripts/2021/04/28/general-dynamics-gd-q1-2021-earnings-call-transcri/", "2021-04-28"),
    # FY2020
    (2020, 4, "fool", "https://www.fool.com/earnings/call-transcripts/2021/01/27/general-dynamics-gd-q4-2020-earnings-call-transcri/", "2021-01-27"),
    (2020, 3, "fool", "https://www.fool.com/earnings/call-transcripts/2020/10/28/general-dynamics-gd-q3-2020-earnings-call-transcri/", "2020-10-28"),
    (2020, 2, "fool", "https://www.fool.com/earnings/call-transcripts/2020/07/30/general-dynamics-gd-q2-2020-earnings-call-transcri.aspx", "2020-07-29"),
    (2020, 1, "fool", "https://www.fool.com/earnings/call-transcripts/2020/04/29/general-dynamics-corp-gd-q1-2020-earnings-call-tra.aspx", "2020-04-29"),
]


class TextExtractor(HTMLParser):
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
    p = TextExtractor()
    p.feed(html)
    text = "".join(p.out)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def extract_transcript_section(text, source):
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
        if m and m.start() > 5000:
            end = min(end, m.start())
    return text[:end].strip()


def fetch(url):
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


KEYWORDS = ("DDG", "destroyer", "Arleigh", "Flight III", "Aegis",
            "Bath", "BIW", "Marine Systems", "Electric Boat", "NASSCO",
            "Virginia", "Columbia", "submarine", "backlog")


def main():
    print(f"=== Scraping GD transcripts ===\n")
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

        raw_path.write_text(html)
        time.sleep(0.5)

        full_text = clean_text(html)
        transcript = extract_transcript_section(full_text, source)
        if len(transcript) < 5000:
            print(f"    ⚠ extracted only {len(transcript)} chars — saving anyway")
        txt_path.write_text(transcript)

        prog_mentions = {
            kw: len(re.findall(r"\b" + re.escape(kw) + r"\b", transcript, re.I))
            for kw in KEYWORDS
        }
        ddg_dollar = []
        for kw in ("DDG", "destroyer", "Bath", "BIW", "Marine Systems"):
            for m in re.finditer(re.escape(kw) + r"[^.]*\$[\d,\.]+\s*(?:billion|million|B|M)", transcript, re.I):
                ddg_dollar.append(m.group(0)[:200])

        meta = {
            "fy": fy, "quarter": q, "source": source, "url": url, "call_date": call_date,
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
            "txt_size": len(transcript), "raw_html_size": len(html),
            "program_mention_counts": prog_mentions,
            "ddg_dollar_snippets": ddg_dollar[:10],
        }
        meta_path.write_text(json.dumps(meta, indent=2))

        print(f"    ✓ saved {len(transcript):,} chars to {txt_path.name}")
        print(f"      mentions: DDG={prog_mentions['DDG']} destroyer={prog_mentions['destroyer']} "
              f"Bath={prog_mentions['Bath']} Marine Systems={prog_mentions['Marine Systems']}")
        saved.append((fy, q, source, url, call_date, len(transcript)))

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
