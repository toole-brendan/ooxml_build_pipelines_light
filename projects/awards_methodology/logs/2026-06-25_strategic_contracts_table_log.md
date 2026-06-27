# 2026-06-25 — Session log (deck slide 1 `strategic_contracts_table`: blank template → real recompete watch-list)

Turned the deck's payoff exhibit — slide 1, the manager's **blank "Example Strategic
Contracts Page"** template (every cell a placeholder: `Platform 1/2`, `Contract 1–4`,
`$###M`, `## / ## / 202#`, `Player A–H`) — into a **real 11-row strategic-contracts
recompete watch-list**, grounded in live SAM.gov Contract Awards + USAspending pulls,
the distributed-shipbuilding SWBS subaward analysis, and the army / MRO / Saronic
corpora. Two entry-route sections (Route A direct-award · Route B supply-chain), a
Funding (Treasury Account Symbol) column, and the manager's restored green/grey/red
Budget Alignment RAG. Build stayed green (`python3 build_deck.py` → **6 slides, 0
charts**, no repair). Output: `20260622_Awards Methodology_vS.pptx`.

This is **Saronic's** market scan (memory `[[deck-is-saronic-pov]]`, written this
session) — so Saronic's own awards are deliberately excluded.

---

## 0. Intent (read from the blank template + the user)

The manager built a 7-column skeleton captioned "Recompete dates and budget alignment"
with a green/grey/red "Budget outlook" legend. The job: populate it with a defensible
set of **real** strategic contracts — platforms, contracts, dollars, recompete dates,
incumbents, budget RAG. Confirmed it needs research + data pulls.

## 1. Reframes agreed with the user (these shaped the exhibit)

- **Columns serve intent, not the literal headers.** Final 7: Route · Platform·Vehicle
  · Incumbent · Amount · Recompete/entry signal · **Funding (TAS)** · **Budget Alignment**.
- **Two recompete angles = slide-2's two routes:**
  - **Route A — Direct award** (the bulk): an IDV whose **last-date-to-order has passed
    or is near** → win the successor as prime or OTA. Data-driven (LDO is a hard field).
  - **Route B — Supply chain**: construction locked by a closed prime → time entry into
    **fragmented + big work-type lanes** (DDG-51 by **SWBS**, not the bespoke D# archetype
    — SWBS is the defensible Navy taxonomy and already underpins slide 3).
- **Budget signal split in two:** a factual **Funding / color-of-money** column from the
  award's **Treasury Account Symbol** (USAspending File-C `federal_account`), AND — after
  an interim "posture (Act/Position)" labeling the user rejected — the manager's original
  **green/grey/red Budget Alignment RAG** (Favorable / Unknown / Unfavorable), restored as
  pure colour swatches keyed to the legend.
- **10th+ row:** leadership wants **adjacent big-dollar fields (amphib / auxiliary)**, not
  another USV-lane row.

## 2. Final list — 11 rows (6 Route A · 5 Route B)

**Route A — direct-award recompetes (clock passed/near):**

| Platform | PIID | Incumbent | Amount | Recompete signal | Funding | RAG |
|---|---|---|---|---|---|---|
| Army watercraft ship-repair (TACOM) | W56HZV21DL pool | Bay Ship & Yacht +9 | $416.8M obl | LDO 2026-01-25 — passed | OPA 021-2035 | Unknown |
| Army bridge erection boats | W56HZV19D0093 | Birdon America | $199M ceil | end 2025-08-12 — passed | OPA 021-2035 | Unknown |
| Navy CVN maintenance (Pacific NW) | N0002419D4310 | Metro Machine (GD-NASSCO) | $465M ceil | LDO 2026-03-20 — passed | O&M,N | Favorable |
| Navy small craft (aluminum boats) | N0002417D2209 | Gravois Aluminum Boats | $118M orders | LDO 2023-09-30 — passed; portal-dark | *(blank)* | Unknown |
| Navy USV core (R&D vehicle) | N0002418D6401 | Penn State ARL | $77M orders | clock 2026-09-30 — imminent | RDT&E,N 017-1319 | Favorable |
| Navy patrol boats | N0002421C2201 | Safe Boats Intl | $173.9M obl | sole-source; ends 2027-12-16 | *(blank)* | Unknown |

**Route B — supply / position in big builds:**

| Field | PIID / lane | Incumbent | Amount | Entry signal | Funding | RAG |
|---|---|---|---|---|---|---|
| USCG Offshore Patrol Cutter | 70Z02322C93220001 | Austal USA (won from Eastern) | $3.3B ceil | Stage-2 build to 2030 | USCG PC&I 070-0612 | Favorable |
| DDG-51 Auxiliary (SWBS 500) | HII + BIW locked | 90 subs · top 15.9% | $947.5M subs | HHI 683 — open lane; FY28-32 surge | SCN 017-1611 | Favorable |
| DDG-51 Propulsion (SWBS 200) | HII + BIW locked | GE 34.7% | $957.9M subs | HHI 1905 — team / 2nd-source | SCN 017-1611 | Favorable |
| T-AGOS(X) ocean surveillance | N0002423C2203 | Austal USA | $3.2B ceil | full & open; build to 2033 | SCN 017-1611 | Favorable |
| T-AO John Lewis oiler | N0002416C2229 | NASSCO | $6.0B ceil | full & open; build to 2028 | SCN 017-1611 | Favorable |

## 3. Data pulls (scratchpad scripts against the live APIs; SAM key from repo-root `.env`)

- **USAspending hydration** (`pull_usp.py`) — `spending_by_award` → gid → award `detail`
  + File-C `funding` (TAS) for the USV/craft + MRO rows. No key needed.
- **Coast Guard discovery** (`pull_disc.py`) — `spending_by_award` by recipient under DHS
  for Austal / Eastern / Bollinger → **OPC Stage 2 = `70Z02322C93220001`** (Austal, won
  from the Stage-1 incumbent Eastern `HSCG2314CAPC002`).
- **SAM.gov Contract Awards** (`pull_samca.py`) — `lastDateToOrder`, completion dates,
  `totalBaseAndAllOptionsValue` for the new rows. OPC ceil $3,315M (compl. 2030-10-21);
  T-AGOS ceil $3,197M (compl. 2033-09-30 / ult 2036-03-01); T-AO ceil $6,003M (compl.
  2028-03-22).
- **MRO-corpus mine** (`mine_navy_repair.py`) + SAM CA — to replace the dropped MA PSM
  with a Navy ship-repair IDV whose LDO has actually run (see §4).
- **DDG SWBS HHI recompute** (`swbs_hhi.py`) — from `ddg_subaward_transactions.csv` ×
  `hii_swbs_crosswalk.csv` (HII work-item code → SWBS major group, label's first token),
  replicating `build_ddg_subaward_concentration.py` in tmp (no workbook change, per the
  user). Confirms **500 Auxiliary $947.5M / 90 subs / HHI 683 (open lane)** and **200
  Propulsion $957.9M / 29 subs / HHI 1905 (entrenched)** — Auxiliary is DDG's *only* big
  AND fragmented major group, so the 2nd Route-B row is Propulsion as the "team" contrast.
- **Adjacent-vessel mine** (`scan_adjacent.py`) — MRO + Saronic corpora for amphib/aux
  big-dollar candidates → T-AGOS(X) (Austal $3.2B) + T-AO oiler (NASSCO $6.0B).

## 4. Findings / gotchas worth keeping

- **MA PSM `N0002423D4100` is NOT a live recompete.** Its true `lastDateToOrder` is
  **2030-12-31**; the "2026-03-27" the MRO scan showed was a *delivery-order* end. Dropped
  it and replaced with **`N0002419D4310`** (CVN Pacific-NW private-sector maintenance, Metro
  Machine/GD-NASSCO, **LDO 2026-03-20 — passed**, $465M, single-award IDIQ — also adds the
  single-award archetype). Lesson: hydrate the parent IDV's LDO via SAM CA; the corpus
  End Date is often the child-order end.
- **Gravois + Safe Boats have no File-C TAS** in USAspending (and no IDV children) →
  funding cells left **blank** (user's call; small-craft awards frequently don't report it).
- **Safe Boats `N0002421C2201` is sole-source** (`extentCompeted` = NOT COMPETED) — a
  Route-B "position for the recompete", not an open bid.
- **OPC** is the clean Route-A-flavored story even in Route B: Austal **won the Stage-2
  recompete from the incumbent** Eastern.
- DDG SWBS is a real materialized tag (`hii_swbs_crosswalk.csv`, X observed / C curated);
  HHI-by-SWBS is **not** in the SAM workbook (only D# archetype HHI is) — computed in tmp.

## 5. The build

Full rewrite of `slides/strategic_contracts_table.py` (blank template → data-driven
module): two module-level row tables (`_ROUTE_A`, `_ROUTE_B`) drive a 7-column native
`table()`; the leftmost column is a dark-navy **Route A / Route B** row-span spine
(`rowSpan=6` / `rowSpan=5`); **Budget Alignment** is a colour-only RAG swatch
(`_BFILL = {F:green, U:GRAY_3, X:red}`) keyed to a restored **"Budget outlook:
Favorable / Unknown / Unfavorable"** legend (top-right). First-pass RAG: **7 Favorable /
4 Unknown / 0 Unfavorable**. Title → "Strategic Contracts — Recompete Watch-List";
breadcrumb "Example Output" → "Strategic Contracts"; `prelim_chip()` kept.

## 6. Verification (built artifact, no PNG render — memory `[[awards-deck-visual-qa]]`)

- Build green: 6 slides, 0 charts, no repair.
- XML scan of `ppt/slides/slide1.xml`: **12 rows × 7 grid columns each** (rowSpan 6/5 +
  `vMerge` continuations resolve correctly); **XML well-formed**; **zero leftover
  placeholders**; Budget Alignment header + Favorable/Unknown/Unfavorable legend present;
  interim "posture/Act/Position" jargon absent; Preliminary chip intact.
- Halted for the user's eyeball (no auto-PNG).

## 7. Open items / for the next agent

- **User to set the reds:** which programs are budget-**Unfavorable** (Army watercraft /
  bridge boats are the likeliest), and confirm the Favorable/Unknown splits. RAG is
  analyst-set (first pass), **not** a pulled field — could be grounded in PB/FYDP later.
- **11 rows vs trim T-AO → 10** for breathing room; eyeball for clipping at 0.46" row
  height with two-line platform cells + wrapping signal text.
- Gravois + Safe Boats funding intentionally blank.
- Nothing committed to git. Scratchpad pull/compute scripts (`pull_usp.py`, `pull_disc.py`,
  `pull_samca.py`, `mine_navy_repair.py`, `swbs_hhi.py`, `scan_adjacent.py`,
  `final_rows.json`) live in the session scratchpad, not the repo.

## 8. Files touched

- **`deck_awards_methodology/slides/strategic_contracts_table.py`** — full rewrite
  (blank template → real 11-row watch-list).
- Output rebuilt: **`20260622_Awards Methodology_vS.pptx`**.
- New memory: `[[deck-is-saronic-pov]]`. Memories in play:
  `[[awards-deck-visual-qa]]`, `[[awards-specs-native-terminology]]`,
  `[[ot-awards-need-sam-contract-awards-api]]`, `[[prefers-agent-verification-over-audit-tools]]`.
