# HII Earnings Call Transcripts

Programmatically scraped from public sources (Motley Fool, Insider Monkey, Yahoo Finance).

**Total: 23 transcripts** covering 19 distinct quarters from Q4 2019 through Q1 2026.

## File naming convention

`FY{YYYY}_Q{N}_{source}.txt` — calendar year of the quarter, quarter number, source site

For each transcript:
- `.txt` — cleaned plain text of the call transcript
- `.meta.json` — fetch metadata: URL, fetch date, file size, keyword counts (Virginia / Columbia / submarine / Block IV-VI / CVN / RCOH / Electric Boat / teaming), and any `$`-near-program snippets
- `_raw_html/<key>.html` — original HTML for re-parsing later

`_index.csv` — master index of all transcripts.

## Coverage

| FY | Q1 | Q2 | Q3 | Q4 | Notes |
|---|---|---|---|---|---|
| 2019 | — | — | — | ✓ Fool | |
| 2020 | — | ✓ Fool | ✓ Fool | ✓ Fool | |
| 2021 | ✓ Fool | ✓ Fool | ✓ Fool | — | |
| 2022 | — | — | — | ⚠ partial | Q1-Q3 not freely available; Q4 prepared remarks only via Yahoo |
| 2023 | ✓ IM | ✓ IM | ✓ IM | ✓ IM | full |
| 2024 | ⚠ partial | ✓ IM | ✓ IM | ✓ IM | Q1 prepared remarks only via Yahoo |
| 2025 | ✓ IM | ✓ IM | ✓ Fool | ✓ Fool + IM | Q4 has 2 sources for redundancy |
| 2026 | ✓ Fool + IM | — | — | — | Q1 only; Q2 will publish ~Aug 2026 |

**Coverage in the FY22-FY26 analysis window** (17 calendar quarters):
- ✓ Full transcript: 12 quarters
- ⚠ Partial (prepared remarks only): 2 quarters (Q4 2022, Q1 2024)
- ✗ Missing: 3 quarters (Q1, Q2, Q3 of 2022)

## Source quality

- **Motley Fool** (`*_fool.txt`): Cleanest format, free, full transcripts including Q&A. Best source when available.
- **Insider Monkey** (`*_insidermonkey.txt`): Full transcripts, free, slightly more ad/nav noise.
- **Yahoo Finance** (`*_yahoo_partial.txt`): Republishes Insider Monkey content but cuts off at Q&A with a "click to continue" link to the full IM page. Only prepared remarks captured.

## What's missing and why

| Quarter | Status | Reason |
|---|---|---|
| FY22 Q1 (May 2022) | None | Free sources behind paywall (Seeking Alpha) or 403 (MarketBeat, mlq.ai) |
| FY22 Q2 (Aug 2022) | None | Same |
| FY22 Q3 (Nov 2022) | None | Same |
| FY22 Q4 (Feb 2023) | Partial | Yahoo has prepared remarks, Q&A behind link |
| FY24 Q1 (May 2024) | Partial | Same — Yahoo paywall Q&A |

For the missing FY22 Q1-Q3, the best free alternative is the 8-K earnings releases we already have in `edgar_research/hii_10k_files/` (each 10-K includes prior 8-K data via summary tables) and the press-release HTMLs from EDGAR (`hiiq{N}2022earningsrelease.htm`). Those don't have the Q&A but do have CFO commentary + program-level color.

## Regenerate

```bash
python3 scripts/scrape_hii_transcripts.py
```

Script caches raw HTML in `_raw_html/`, so re-runs are incremental.

## Quick keyword counts across all transcripts

Run:
```bash
python3 -c "
import json, glob
totals = {}
for f in glob.glob('hii_earnings_transcripts/*.meta.json'):
    d = json.load(open(f))
    for kw, n in d['program_mention_counts'].items():
        totals[kw] = totals.get(kw, 0) + n
for kw, n in sorted(totals.items(), key=lambda x: -x[1]):
    print(f'{kw:20} {n}')
"
```
