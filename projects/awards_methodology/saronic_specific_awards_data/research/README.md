# Saronic USV — SAM.gov solicitations pipeline (pre-award)

Forward-pipeline opportunity data for an autonomous-surface-vessel maker:
active solicitations / presolicitations / sources-sought / special notices
from the SAM.gov **Get Opportunities** API. This is the pre-award complement
to the FSRS subaward (already-awarded) corpora in `projects/{submarines,ddg}`.

Canonical API field guide: `projects/ddg/research/SAM_GOV_HOWTO.md` (key
setup, quotas, IPv4 monkeypatch). This README covers only what's specific to
the Opportunities API, live-verified 2026-06-12.

## API quick reference

- Endpoint: `https://api.sam.gov/opportunities/v2/search` — **no `/prod/`
  segment** (unlike the subaward API).
- Auth: `api_key=` query param; key in repo-root `.env` (`SAM_API_KEY=`,
  entity-role tier, 1,000 calls/day, resets midnight UTC).
- Required: `postedFrom` / `postedTo`, `MM/dd/yyyy`, **max 1-year span**.
- Free text: `title=` only — phrase-substring match on TITLE, no description
  search. Broad single words + client-side scoring beat precise phrases.
- Other filters: `ncode` (NAICS), `ccode` (PSC), `ptype`, `solnum`,
  `organizationName`, `rdlfrom/rdlto`, `limit` (max 1000), `offset`.
- `status` values (live 400 message): `Activelatest / Activeall / Archived /
  Cancelled / Deleted` — NOT the lowercase set the docs claim. Default is
  active-only. **`status=Archived` 500s on every filter combination tried**
  (server-side bug) — recently-closed pulls are not possible today.
- The ~60s/call latency documented in the HOWTO (2026-05) is gone: ~1-2s/call.
- `description` in responses is a URL; text costs one extra call per notice
  via `https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=…`
  (this one DOES carry `/prod/`).
- `postedDate` = last-modified date — long-running BAAs without recent
  amendments are invisible to a recent posted window.
- "No results" returns HTTP 404, not an empty 200.

## Layout / regeneration

```
scripts/pull_sam_opportunities.py   # 13 cached queries (title/NAICS/PSC sweeps)
scripts/summarize_opportunities.py  # dedupe by noticeId + tier scoring -> CSV
scripts/fetch_descriptions.py       # description text for the shortlist
sam_opportunities/<slug>.json       # raw responses, skip-if-exists resume
extracted/opportunities_all.csv     # 669 unique notices, tiered, sorted
descriptions/<noticeId>.json        # shortlist description cache
```

Re-run order: pull → summarize → fetch_descriptions (each is resumable;
delete the cached JSON to force a re-fetch; bump the posted window in the
pull script first).

Tiers are a research-side screen (STRONG / MEDIUM / VESSEL / OTHER from
title + NAICS/PSC), not a verdict — see header of
`scripts/summarize_opportunities.py`. `pre_award=yes` excludes award notices.

## Coverage caveats

- Title-only search → generically-titled notices with USV content in the
  description body are invisible to keyword sweeps (mitigated by the
  NAICS 336611/336612 and PSC 1940/1905 sweeps, partly).
- Active-only: the archived-status bug means no recently-closed context.
- Programs of record (MUSV/LUSV etc.) often run through consortia/OTAs or
  restricted channels and may never appear on SAM.gov; DIU CSOs post on
  diu.mil, SOFWERX events partially cross-post (the two in this pull did).
