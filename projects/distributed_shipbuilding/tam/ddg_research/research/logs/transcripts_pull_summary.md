# Earnings transcripts pull — summary
Total: **134 transcripts**, **7,173,026 chars** across 7 primes (GD, HII, LMT, RTX, NOC, LHX, BAE).

| Ticker | Discovered | Saved | Failed | Chars | DDG/naval mentions |
|---|---:|---:|---:|---:|---:|
| BAE | 3 | 3 | 0 | 208,974 | 9 |
| GD | 22 | 22 | 0 | 1,034,613 | 230 |
| HII | 23 | 23 | 0 | 1,113,198 | 814 |
| LHX | 21 | 21 | 0 | 1,174,526 | 41 |
| LMT | 21 | 21 | 0 | 1,182,027 | 85 |
| NOC | 23 | 23 | 0 | 1,229,340 | 40 |
| RTX | 21 | 21 | 0 | 1,230,348 | 37 |

## Top-3 DDG-relevant transcripts per new ticker (DDG/naval mention count)
- **LMT**: FY2025 Q2 (fool, 9 mentions); FY2024 Q2 (fool, 7 mentions); FY2025 Q4 (fool, 7 mentions)
- **RTX**: FY2025 Q3 (fool, 5 mentions); FY2024 Q1 (fool, 4 mentions); FY2021 Q4 (fool, 3 mentions)
- **NOC**: FY2020 Q3 (fool, 11 mentions); FY2025 Q3 (fool, 5 mentions); FY2026 Q1 (fool, 5 mentions)
- **LHX**: FY2020 Q4 (fool, 10 mentions); FY2021 Q3 (fool, 7 mentions); FY2022 Q1 (pdf, 5 mentions)
- **BAE**: FY2025 Q1 (insidermonkey, 4 mentions); FY2025 Q4 (insidermonkey, 4 mentions); FY2024 Q1 (insidermonkey, 1 mentions)

## Notes & gaps
- **LMT** (21/21): Q1 2022, Q1 2023 not on Motley Fool — gap left intentionally.
- **RTX** (21/21): No Q1-Q3 2020 — RTX ticker only exists post 2020-04-03 UTC/Raytheon merger.
- **NOC** (23/23): Full quarterly coverage FY2020 Q1 through Q1 2026, all Motley Fool.
- **LHX** (21/21): Mixed sources — Motley Fool (8), official L3Harris PDFs via q4cdn/l3harris.com (9), Insider Monkey (4). Gaps: Q2 2020, Q3 2020, Q2 2022, Q3 2022 — not surfaced.
- **BAE** (3/3): Semi-annual reporter, not quarterly. Motley Fool does NOT cover BAE. Insider Monkey only surfaces 2024-2025: H1 2024, H1 2025, H2 2025. Pre-2024 BAE commentary will need 20-F SEC filings or BAE IR site.

## Artifacts
- `{lmt,rtx,noc,lhx,bae}_earnings_transcripts/` — `.txt` + `.meta.json` per call, `_index.csv` per ticker
- `extracted/all_transcripts_index.csv` — unified master index (134 rows incl. GD/HII)
- `scripts/scrape_transcripts_generic.py` + `scripts/transcripts_url_config.json` — re-runnable scraper
- `scripts/build_transcripts_master_index.py` — rebuild master
- `pull_logs/{lmt,rtx,noc,lhx,bae}_transcripts.log` — per-ticker run logs
