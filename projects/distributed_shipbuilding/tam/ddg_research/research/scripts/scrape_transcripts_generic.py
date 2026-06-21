#!/usr/bin/env python3
"""
Generalized earnings call transcript scraper, parameterized on ticker.

Reads scripts/transcripts_url_config.json and scrapes a single ticker's URLs:
  python3 scripts/scrape_transcripts_generic.py <ticker>

Per-URL workflow (mirrors scrape_gd_transcripts.py):
  - Fetch with browser User-Agent (curl), 0.5s sleep between fetches
  - Strip HTML to plain text (preserve paragraph breaks)
  - Save .txt + .meta.json with ticker-specific keyword counts
  - Pull dollar snippets near DDG-relevant keywords
  - Index CSV at end

Sources supported: fool, insidermonkey, seekingalpha.
If fetch < 5000 chars or 404, mark as failed and move on.
"""
import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
CONFIG_PATH = REPO / "scripts" / "transcripts_url_config.json"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

DDG_DOLLAR_KEYWORDS = ("DDG", "destroyer", "Arleigh", "Aegis", "Flight III",
                       "naval", "Mk 41", "Mk 45", "VLS", "SPY-6",
                       "Marine Systems", "Ingalls", "Bath", "BIW",
                       "Mission Systems", "Missiles", "Land")


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
    try:
        p.feed(html)
    except Exception:
        # Some HTML may be malformed; salvage what we got
        pass
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
        r"Insider Monkey Stock Picks",
        r"See also \d+",
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


def fetch_pdf_as_text(url):
    """Download a PDF and convert to text via pdftotext (poppler) if available,
    else fall back to plaintext-ish extraction."""
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            pdf_path = tmp.name
        result = subprocess.run(
            ["curl", "-sS", "--max-time", "30", "-L", "-A", UA, url, "-o", pdf_path],
            capture_output=True, timeout=45,
        )
        if result.returncode != 0:
            return None
        size = os.path.getsize(pdf_path)
        if size < 5000:
            return None
        # Try pdftotext (poppler) first
        try:
            txt = subprocess.run(
                ["pdftotext", "-layout", pdf_path, "-"],
                capture_output=True, text=True, timeout=30,
            )
            if txt.returncode == 0 and len(txt.stdout) > 1000:
                # Return as fake HTML so clean_text() pass-through works
                return f"<html><body><pre>{txt.stdout}</pre></body></html>"
        except FileNotFoundError:
            pass
        # Fallback: read raw bytes and salvage text strings
        with open(pdf_path, "rb") as f:
            raw = f.read()
        # Very rough fallback — pdftotext should exist on mac via Homebrew
        return None
    except Exception:
        return None


def fetch_insidermonkey(base_url):
    """Insider Monkey paginates transcripts across multiple pages (/2/, /3/, etc.).
    Concatenate them, dedup by body hash to avoid repeat pages."""
    html_combined = ""
    base = base_url.rstrip("/")
    seen_bodies = set()
    for page in range(1, 11):
        url = base + "/" if page == 1 else f"{base}/{page}/"
        html = fetch(url)
        if html is None:
            if page == 1:
                return None
            break
        # Hash the middle portion to detect pages identical to prior ones
        body_sig = hash(html[len(html)//4:len(html)*3//4])
        if body_sig in seen_bodies:
            break
        seen_bodies.add(body_sig)
        html_combined += html
        if "404" in html[:2000] and page > 1:
            break
        if page > 1 and len(html) < 20000:
            break
        time.sleep(0.3)
    return html_combined if html_combined else None


def scrape_ticker(ticker_key):
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    if ticker_key not in config:
        print(f"ERROR: ticker '{ticker_key}' not in config; available: {list(config.keys())}")
        return 1

    cfg = config[ticker_key]
    ticker = cfg["ticker"]
    keywords = tuple(cfg["keywords"])
    out_dir = REPO / cfg["out_dir"]
    out_dir.mkdir(exist_ok=True)
    raw_dir = out_dir / "_raw_html"
    raw_dir.mkdir(exist_ok=True)

    urls = cfg["urls"]
    print(f"=== Scraping {ticker} ({cfg['company_name']}) — {len(urls)} URLs ===\n", flush=True)

    saved = []
    failed = []

    for entry in urls:
        fy, q, source, url, call_date = entry
        key = f"FY{fy}_Q{q}_{source}"
        txt_path = out_dir / f"{key}.txt"
        meta_path = out_dir / f"{key}.meta.json"
        raw_path = raw_dir / f"{key}.html"

        if txt_path.exists() and txt_path.stat().st_size > 5000:
            print(f"  [{key}] already saved ({txt_path.stat().st_size:,} chars), skipping")
            saved.append((fy, q, source, url, call_date, txt_path.stat().st_size))
            continue

        print(f"  [{key}] fetching {url[:90]}…", flush=True)

        if source == "insidermonkey":
            html = fetch_insidermonkey(url)
        elif source == "pdf" or url.lower().endswith(".pdf"):
            html = fetch_pdf_as_text(url)
        else:
            html = fetch(url)

        if html is None:
            print(f"    FAIL")
            failed.append((fy, q, source, url, "fetch failed / too small / 404"))
            continue

        raw_path.write_text(html)
        time.sleep(0.5)

        full_text = clean_text(html)
        transcript = extract_transcript_section(full_text, source)
        if len(transcript) < 5000:
            print(f"    WARN extracted only {len(transcript)} chars — saving anyway")
            if len(transcript) < 1000:
                failed.append((fy, q, source, url, f"extracted only {len(transcript)} chars"))
                # Still write the .txt so downstream can see what came through
        txt_path.write_text(transcript)

        prog_mentions = {
            kw: len(re.findall(r"\b" + re.escape(kw) + r"\b", transcript, re.I))
            for kw in keywords
        }
        ddg_dollar = []
        for kw in DDG_DOLLAR_KEYWORDS:
            for m in re.finditer(re.escape(kw) + r"[^.]{0,120}\$[\d,\.]+\s*(?:billion|million|B|M)\b", transcript, re.I):
                ddg_dollar.append(m.group(0)[:300])
            for m in re.finditer(r"\$[\d,\.]+\s*(?:billion|million|B|M)\b[^.]{0,120}" + re.escape(kw), transcript, re.I):
                ddg_dollar.append(m.group(0)[:300])

        meta = {
            "ticker": ticker,
            "fy": fy, "quarter": q, "source": source, "url": url, "call_date": call_date,
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
            "txt_size": len(transcript), "raw_html_size": len(html),
            "program_mention_counts": prog_mentions,
            "ddg_dollar_snippets": ddg_dollar[:15],
        }
        meta_path.write_text(json.dumps(meta, indent=2))

        # Print a few headline keyword counts
        top_hits = sorted(prog_mentions.items(), key=lambda x: -x[1])[:5]
        hits_str = " ".join(f"{k}={v}" for k, v in top_hits if v > 0)
        print(f"    OK {len(transcript):,} chars  {hits_str}")
        saved.append((fy, q, source, url, call_date, len(transcript)))

    index_path = out_dir / "_index.csv"
    with open(index_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ticker", "fy", "quarter", "call_date", "source", "url", "txt_size_chars", "filename"])
        for fy, q, source, url, call_date, size in sorted(saved):
            fname = f"FY{fy}_Q{q}_{source}.txt"
            w.writerow([ticker, fy, q, call_date, source, url, size, fname])

    print(f"\n=== {ticker} DONE ===")
    print(f"  Saved {len(saved)} transcripts; {len(failed)} failed")
    print(f"  Index: {index_path}")
    if failed:
        print(f"\n  Failed URLs:")
        for fy, q, src, url, reason in failed:
            print(f"    FY{fy} Q{q} ({src}): {reason}")
            print(f"      {url}")

    return 0 if not failed else 2


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scrape_transcripts_generic.py <ticker_key>")
        print("       ticker_key is one of: lmt rtx noc lhx bae")
        return 1
    ticker_key = sys.argv[1].lower()
    return scrape_ticker(ticker_key)


if __name__ == "__main__":
    sys.exit(main())
