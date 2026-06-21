#!/usr/bin/env python3
"""Write logs/transcripts_pull_summary.md — concise morning-read artifact."""
import csv
import json
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
INDEX = REPO / "extracted" / "all_transcripts_index.csv"
OUT = REPO / "logs" / "transcripts_pull_summary.md"


def main():
    rows = list(csv.DictReader(open(INDEX)))
    by_ticker = defaultdict(list)
    for r in rows:
        by_ticker[r["ticker"]].append(r)

    cfg = json.load(open(REPO / "scripts" / "transcripts_url_config.json"))
    cfg_counts = {v["ticker"]: len(v["urls"]) for k, v in cfg.items()
                  if isinstance(v, dict) and "urls" in v}

    lines = []
    lines.append("# Earnings transcripts pull — summary")
    lines.append(f"Total: **{len(rows)} transcripts**, **{sum(int(r['txt_size']) for r in rows):,} chars** "
                 f"across 7 primes (GD, HII, LMT, RTX, NOC, LHX, BAE).")
    lines.append("")
    lines.append("| Ticker | Discovered | Saved | Failed | Chars | DDG/naval mentions |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for t in sorted(by_ticker):
        lst = by_ticker[t]
        disc = cfg_counts.get(t, len(lst))
        saved = len(lst)
        failed = max(0, disc - saved) if t in cfg_counts else 0
        chars = sum(int(r["txt_size"]) for r in lst)
        ddg = sum(int(r["ddg_mention_count"]) for r in lst)
        lines.append(f"| {t} | {disc} | {saved} | {failed} | {chars:,} | {ddg} |")
    lines.append("")
    lines.append("## Top-3 DDG-relevant transcripts per new ticker (DDG/naval mention count)")
    for t in ("LMT", "RTX", "NOC", "LHX", "BAE"):
        lst = sorted(by_ticker[t], key=lambda r: -int(r["ddg_mention_count"]))
        lines.append(f"- **{t}**: " + "; ".join(
            f"FY{r['fy']} Q{r['quarter']} ({r['source']}, {int(r['ddg_mention_count'])} mentions)"
            for r in lst[:3]))
    lines.append("")
    lines.append("## Notes & gaps")
    lines.append("- **LMT** (21/21): Q1 2022, Q1 2023 not on Motley Fool — gap left intentionally.")
    lines.append("- **RTX** (21/21): No Q1-Q3 2020 — RTX ticker only exists post 2020-04-03 UTC/Raytheon merger.")
    lines.append("- **NOC** (23/23): Full quarterly coverage FY2020 Q1 through Q1 2026, all Motley Fool.")
    lines.append("- **LHX** (21/21): Mixed sources — Motley Fool (8), official L3Harris PDFs via q4cdn/l3harris.com (9), Insider Monkey (4). Gaps: Q2 2020, Q3 2020, Q2 2022, Q3 2022 — not surfaced.")
    lines.append("- **BAE** (3/3): Semi-annual reporter, not quarterly. Motley Fool does NOT cover BAE. Insider Monkey only surfaces 2024-2025: H1 2024, H1 2025, H2 2025. Pre-2024 BAE commentary will need 20-F SEC filings or BAE IR site.")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- `{lmt,rtx,noc,lhx,bae}_earnings_transcripts/` — `.txt` + `.meta.json` per call, `_index.csv` per ticker")
    lines.append("- `extracted/all_transcripts_index.csv` — unified master index (134 rows incl. GD/HII)")
    lines.append("- `scripts/scrape_transcripts_generic.py` + `scripts/transcripts_url_config.json` — re-runnable scraper")
    lines.append("- `scripts/build_transcripts_master_index.py` — rebuild master")
    lines.append("- `pull_logs/{lmt,rtx,noc,lhx,bae}_transcripts.log` — per-ticker run logs")

    OUT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT}  ({len(lines)} lines)")


if __name__ == "__main__":
    main()
