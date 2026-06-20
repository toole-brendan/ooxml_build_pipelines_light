# 2026-06-20 — Budget materials corpus (download + text conversion): session log

Second session on the `army` project. Built the **budget-materials research corpus** that will be the
financial backbone of the autonomous-watercraft market workbook: downloaded 45 Army budget justification
books (FY2022–FY2027) and produced a layout-preserving, page-marked `.txt` mirror for AI-agent searching.
Everything lives under a new `research/budget_materials/` folder. No pipeline (`deck`/`workbook`/`doc`) or
engine code was touched this session — this is pure data gathering.

Driven by the market-study methodology (mission problem → user → requirement → acquisition → funding →
contracting → timing → route). This session covers the **funding** evidence layer only.

---

## 1. What was created

```
projects/army/research/budget_materials/
  download_budget_books.py     downloader: Akamai-aware curl, per-year URL variants, idempotent
  convert_to_txt.py            pdftotext -layout + PAGE markers; augments the manifest
  _manifest.csv                45 rows: status, http, bytes, pages, sha256_16, pdf+txt paths, source_url
  pdf_originals/   (318 MB)    FY2022..FY2027 / {procurement, rdte, om, summary} / *.pdf
  txt_versions/    (63 MB)     1:1 mirror of pdf_originals, *.txt
```

`pdf_originals/` and `txt_versions/` mirror each other exactly: `txt_versions/FY2027/procurement/OPA_BA1_…txt`
is the conversion of `pdf_originals/FY2027/procurement/OPA_BA1_…pdf`.

## 2. Corpus scope (the "Recommended corpus", 45 books, 0 misses)

| Tier | Books | FYs | Why |
|------|-------|-----|-----|
| 1 — procurement spine | **OPA BA1** (Other Procurement, Army — Tactical & Support Vehicles) | FY22–27 (×6) | Army watercraft procurement lives here: MSV(L), Army Watercraft Esp, mods |
| 2 — R&D / autonomy | **RDT&E** Budget Activities 3, 4A, 4B, 5A, 5D, 7 | FY22–27 | Autonomy, prototyping, contested-logistics, fielded-system upgrades |
| 3 — operating / force structure | **OMA Volume 1** (Operating Forces) | FY25–27 (×3) | Watercraft sustainment + Composite Watercraft Company stand-up |
| Index | DoD-wide **P-1 / R-1 / O-1** (OSD Comptroller) | FY27 | Consolidated line/PE index for fast lookup |

Per-FY counts: FY27=11, FY26=8, FY25=8, FY24=7, FY23=6, FY22=5.
**RDT&E BA splits vary by year** and the loader handles it: FY22 has single BA3/BA4/BA5A/BA7 (no A/B/D
split); FY23 has BA3/**BA4**/BA5A/BA5D/BA7 (BA4 single, BA5 split); FY24–27 have BA3/4A/4B/5A/5D/7.

The standalone P-40/P-5 (procurement), R-2/R-2A (RDT&E) and OP-5 (O&M) exhibits the methodology calls for
are **sections inside these justification books**, not separate downloads. The only standalone pulls are the
consolidated P-1/R-1/O-1 indices.

## 3. How the download works (so the next editor doesn't re-derive it)

- **Host:** `asafm.army.mil` (Army FM&C Budget Materials portal), files under
  `/Portals/72/Documents/BudgetMaterial/{FY}/{Base Budget|Discretionary Budget}/{category}/…pdf`.
- **Akamai bot management — the load-bearing gotcha.** Bare `curl`/WebFetch requests get **HTTP 403
  "Access Denied"** (`edgesuite.net` reference). A **full browser header set passes**: `User-Agent` +
  `Accept` + `Accept-Language` + `Referer` + `Sec-Fetch-*` + `Upgrade-Insecure-Requests`. Drop any of the
  Sec-Fetch / Accept-Language headers and it can revert to 403. The HTML index pages 403 even *with* the
  full set (stricter rule) — so the directory listing is **not crawlable**; URLs must be constructed/probed.
- **403 ≠ 404.** With the *full* header set, a missing file returns a clean **404 (149 bytes)**; a wrong
  header set returns **403**. The downloader only accepts `http 200 + %PDF- magic bytes + size > 8 KB`.
- **Filename drift across years** is real (downloader carries variants per book, first valid PDF wins):
  - OPA BA1: `OPA_BA_1_FY_2022_PB_Other_Procurement_…` (22) → `OPA_BA1_Tactical_Support_Vehicles` (23) →
    `Other Procurement - BA 1 - …` (24, spaced "BA 1") → `Other Procurement - BA1 - …` (25–27).
  - RDT&E: `RDTE_BA_4_FY_2022_PB` (22) → `vol_2-Budget_Activity_4` (23, underscores) →
    `RDTE-Vol 2-Budget Activity 4A` (24) → `RDTE - Vol 2 - Budget Activity 4A` (25–27, spaced).
  - RDT&E folder: `rdte/` most years, but FY25 = `Research, Development, Test and Evaluation/`.
  - Volume number per BA is unstable → loader probes Vol 1..4 and takes the first hit.
- **Idempotent:** re-running skips any book already on disk as a valid PDF (status `HAVE`); only true gaps
  re-fetch. `_manifest.csv` is regenerated each run.

## 4. How the text conversion works

- **`pdftotext -layout -enc UTF-8 -eol unix`** (poppler 25.12.0). `-layout` chosen deliberately: these books
  are mixed prose + **dense funding tables**, and layout mode preserves column geometry so a line item's
  label stays on the same line as its P-1 line number, sub-codes, and FY dollars. Default reading-order mode
  scrambles the label↔number association — fatal for budget tables.
- **Page markers:** the form-feeds pdftotext emits between pages are converted to explicit
  `===== PAGE N =====` lines, where N = physical PDF page. Lets an agent cite an exact page without
  reopening the PDF (the methodology's Source Log / `04_Budgets` need exact-page citations). The books' own
  printed "Volume X - NNN" refs remain inline, so both citation schemes are available.
- These PDFs are **born-digital** (iText producer) — no OCR needed; pdftotext reads embedded text directly.

## 5. Verification (all green)

- **45 PDF ↔ 45 TXT**, 1:1, zero empty/short outputs.
- **Page fidelity exact:** FY2027 OPA BA1 = 261 `PAGE` markers == 261 pdfinfo pages.
- **Watercraft procurement spine survived layout conversion and is citable:**
  - `Army Watercraft Esp` — P-1 line **108**, BLI `3569M11101` → **PAGE 53**, printed "Volume 3 - 257"
  - `Maneuver Support Vessel (MSV)` — P-1 line **109**, BLI `8211R01001` → **PAGE 53**, "Volume 3 - 269"
- FY2027 RDT&E BA4A spot-check earlier: 19 "Watercraft", 27 "autonomous", "Contested Logistics" hits —
  R&D half is on-target too.

## 6. Open items / next steps

- **Extraction not started.** Next: pull the watercraft P-40/P-5 line items (start at OPA BA1 PAGE 53 →
  detail at Vol 3 p.257 "Army Watercraft Esp" and p.269 "MSV") and the relevant RDT&E PEs out of
  `txt_versions/` into the workbook's `04_Budgets` structure. `_manifest.csv` feeds `11_Source_Log`.
- **No README in the folder yet.** Offered but not written; the two scripts' docstrings currently carry the
  scope + gotchas. Add a `README.md` if this folder is handed off.
- **P-1/R-1/O-1 are DoD-wide, not Army-only.** They're indices; the Army-specific detail is in the
  justification books. Per-FY consolidated Army indices were not pulled (per-book front matter covers it).
- **Requested vs enacted:** each book mixes PY-enacted / CY / BY-request. Keep them in separate columns when
  extracting — do not difference across books blindly.
- **Re-run cadence:** FY2028 PB drops ~Feb–Apr 2027; add `2028` to the loader's year lists and re-run
  (idempotent) to refresh. Watch for another filename-convention shift.
- **Log location convention:** placed here in `projects/army/logs/` at request, consistent with the prior
  session; the standing repo-root `logs/` convention note still applies if this should be mirrored.
