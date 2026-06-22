# 2026-06-21 — Hunting the "missing" HII Newport News Virginia/Columbia workshare (9-method data forensics)

User-driven investigation: *find HII Newport News Shipbuilding's Virginia/Columbia new-construction
workshare in the federal award data — it appears "nearly all missing," suspected to be the GDEB↔HII
teaming arrangement.* Read-only research across already-pulled data + live FPDS/USAspending/SAM
queries. **No workbook or pull-pipeline changes.** Net deliverable = a definitive negative result +
edits to `award_classification/DOMAIN_SHARE_CONCENTRATION_CAVEAT.md`.

Inputs read first: `projects3/Federal_Award_API_Research_Methodology.docx` (the API playbook),
`.env` `SAM_API_KEY` (entity-role, 1,000/day), the two reference-prior-analysis lessons docs, and a
transcript of another agent's advice (search GDEB prime PIIDs, all HII UEIs, Published+Deleted).

---

## Verdict (held up across all 9 methods)

**HII Newport News's Virginia/Columbia *new-construction* workshare is genuinely not in any public
transactional database.** Not a direct prime, not an FSRS subaward, not in deleted records, not
under any of HII's six registered identities.

| Channel | What's actually there |
|---|---|
| FSRS/SAM subawards under the GDEB primes | **Virginia ≈ $75–90M** (3 EB POs + tiny Newport News Nuclear GFE); **Columbia $0** |
| Direct Navy prime to HII | carriers **$51.8B** + submarine **maintenance/overhaul $4.2B** — **no new construction** |
| True HII co-build role (CRS / issuer-disclosed) | Virginia ~50% (Block V cumulative **disclosed ≈ $10.2B**, May 2023); Columbia ~22–23% |

The reported HII footprint is **<$100M on Virginia, exactly $0 on Columbia**, against a true
co-build workshare in the **tens of billions**.

---

## The 9 methods and what each returned

1. **SAM/FSRS raw scan, published + deleted** (`submarine_subaward_code_package/raw_json/`, 17 sub
   primes). HII only on Virginia EB primes **C2100 (27 recs)** + **C2111 (4 recs)**; **0 on Columbia**
   (C2117 5,208 recs / C2128 608 recs). **Deleted arrays: 1 record total across all 17** (Rolls-Royce,
   not HII) → the "Published-then-Deleted" lead is a **dead end**.
2. **USAspending cross-prime subaward search** by recipient (UEI + names). Only EB→HII on C2100,
   C2111, and one prime not in our pull — **N0002420C2120** (~$14M). All else = ATI/ONR ManTech R&D or
   the Ingalls DDG strut castings. Columbia prime never lists HII.
3. **USAspending direct-prime, UEI `WMXDDH6HJNA5`** — 300 awards: $51.8B carriers, $4.2B sub
   maintenance/overhaul, ~$0.7B misc-sub (planning/SSBN maint), $12.5B blank. No construction workshare.
4. **USAspending direct-prime, other UEIs** — `JK19LLUJCCF3` (legacy NN Shipbuilding Inc): 14 awards,
   all 2000–2005, ~$1.4B engineering/early-build; `CR39JL3216G7` (Newport News Nuclear): 0; parent
   `F9SDJAZFTLG6`: same universe.
5. **FPDS vendor "NEWPORT NEWS SHIPBUILDING"** + Navy + >$50M — 107 PIIDs; sub-matching ones all
   pre-2008.
6. **FPDS vendor "NORTHROP GRUMMAN SHIPBUILDING"** + Navy + >$50M (pre-2011 ownership name) — 225
   PIIDs; same picture.
7. **FPDS PIID-direct** description confirmation — the big early PIIDs (N0002498C2104, N0002404C2118,
   N0002406C2115…) are TAS-string-coded NAICS-336611 SUPSHIP-NN primes, **all pre-FY2008**; carrier vs.
   early-Virginia-co-build not cleanly separable, but none modern.
8. **FPDS recipient-agnostic NAICS-336611 + Navy + >$300M + signed≥2012** — 49 PIIDs. **Every [SUB]
   prime belongs to Electric Boat** (C2100 $34.2B, C2115 $16.6B, C2104 $6.8B, C2110 $4.4B, Hartford
   EOH, VACL materials); HII holds only carriers, DDG-51 (Ingalls), and LPD/LHA amphibs. *(Columbia
   master C2117 absent here only because it's NAICS-coded 541330 "Engineering Services," not 336611 —
   classification quirk; still EB's.)*
9. **SAM Entity API enumeration of all HII registrations** — caught a previously-unsearched identity
   **`P3FPNF7WGWL8`** (CAGE 10SX4, "Huntington Ingalls Inc," Goose Creek SC) → **0 prime, 0 subs**;
   `C3NLZNSMU254` = Ingalls/Pascagoula (DDG prime, already known); `JK19LLUJCCF3` now deregistered;
   "Newport News Shipbuilding" name search → only a **credit union** (BayPort).

**Smoking gun for the gap:** on the same Columbia prime **N0002417C2117**, EB reports **$7.75B** of
subawards (BlueForge $1.5B+, Northrop Grumman, DRS Naval Power, Precision Custom Components, UK
Rosyth) — EB reports subs diligently; only the HII workshare is missing.

---

## Mechanism (stated carefully)

Build runs under a **Navy-directed teaming/co-production arrangement**, GDEB sole prime; prime
announcements name HII NNS as *major subcontractor* (Block V) / co-designer (Columbia, 12.7% PoP).
**But a teaming agreement does not by itself exempt a subcontract from FAR 52.204-10** — HII *itself*
calls these EB **contracts and subcontract modifications**, and the clause normally requires
amount/date/description/subcontract-number/prime-PIID. So the public absence is an **unexplained
reporting / data-treatment gap, not proof no reportable subcontract existed** (revised from an
earlier "clean teaming carve-out" framing after a second-opinion review).

---

## Methodology gotchas (cost real time — captured so they aren't relearned)

Source of the fixes: `projects/army/research/contracts/scripts/_common.py` +
`tam/{ddg,virginia_columbia}_research/research/SAM_GOV_HOWTO.md`.
- **macOS IPv6 hang on `api.sam.gov` (~225s/request).** My hand-rolled SAM call hung for 4+ min until
  killed. Fix = force IPv4 via the `socket.getaddrinfo` monkeypatch in `_common.py`. Reuse `_common`,
  don't re-roll.
- **SAM Entity API:** query **by `ueiSAM`** (≈0.3s). A `legalBusinessName`/unfiltered search triggers a
  full-dataset scan and effectively hangs. **`size` ≤ 10** (else HTTP 400 "Size Cannot Exceed 10").
- **Python stdout block-buffers to a file** → a "stuck" run may just be unbuffered output. Use
  `python3 -u` + `flush`.
- USAspending & FPDS need **no key**; only SAM is quota-limited. This session spent only a handful of
  SAM calls (entity lookups); USAspending/FPDS did the heavy lifting.

---

## Document edits (committed to working tree, not git-committed)

`award_classification/DOMAIN_SHARE_CONCENTRATION_CAVEAT.md` — confirmed this is a **sibling** caveat
(it warns the *present* domain shares are concentrated; the HII finding is the deeper first-order
problem that the *largest builder is absent from the population entirely*). Added:
1. Section **"The deeper caveat: the largest co-builder (HII Newport News) is absent…"** — table of
   present vs. true workshare, mechanism, the 9 methods, and the consequence that every D share is
   **"% of GDEB-reported subcontracted scope," not "% of total boat construction."**
2. Section **"Recommended paths forward"** (7 items: reframe labels; derived CRS-split memo line;
   complete EB denominator; HII 10-K segment bound; CRS/GAO corroboration; NAVSEA FOIA/PIEE-EDA;
   methodology hygiene).
3. **Second-opinion addition** — "Preferred path: issuer-disclosed subcontract ledger": HII-announced
   award amounts (Block V cumulative **≈ $10.2B** as of 2023-05-24; itemized Columbia mods), a separate
   amount-basis-typed table schema, a 4-tier source hierarchy, two targeted NAVSEA FOIA requests
   (incl. the **FAR 52.204-10 CO-direction question**), and PIEE/EDA. Plus a revised mechanism
   paragraph and two dated provenance-footer notes.

---

## Carry-forward

- **Data forensics is exhausted — do NOT re-run** additional UEIs, deleted records, or USAspending
  variants. The core HII workshare is not in the FFATA feed, full stop.
- **Pull gaps to close** (denominator completeness, for EB): add **N0002420C2120** (EB "Lead Yard
  Support," $4.3B, NAICS 336611, ~$14M EB→HII subs); verify Virginia Block VI / AP coverage.
- **To actually quantify HII workshare:** (a) issuer-disclosed ledger from HII announcements + SEC
  10-K (CIK 1501585) — use Block V **$10.2B** for the historical headline; (b) NAVSEA FOIA on
  `N00024-17-C-2100` and `N00024-17-C-2117` for subcontract number/lineage/cumulative value + the
  FAR 52.204-10 CO-direction record; (c) PIEE/EDA (gov-side) for pricing memos / workshare schedules.
- **When reframing the workbook:** label all submarine domain shares as share of *GDEB-reported
  first-tier subcontracted scope*, excluding the FFATA-invisible HII co-build.
- **Reproducibility note:** the live-query scripts ran from `/tmp` (ephemeral, not saved to repo). If
  re-running, build on `army/research/contracts/scripts/_common.py` (IPv4 patch + helpers) rather than
  hand-rolling urllib.
- **Open tension in the caveat doc:** upper table cites CRS "~50%" Virginia; new section cites
  issuer-disclosed ~25% PoP / $10.2B. Currently reconciled by label-by-basis + a "prefer the disclosed
  figure" note; could be hard-reconciled in the upper table if these get published.
