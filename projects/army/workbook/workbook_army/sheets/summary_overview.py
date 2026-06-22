"""summary_overview - the executive market-size dashboard (the front page).

The decision summary: the Gross Funded -> Addressable -> Saronic-Serviceable (SAM) ->
Weighted Pursuit (SOM) bridge surfaced as GREEN single-source links to the Market Size
totals, plus the evidence base (live counts/sums over Contract Families) and the data-
freshness + caveat pointers. Color discipline holds: a single cross-sheet value is GREEN
(S_LINK_*), an in-sheet aggregation is BLACK (COUNTIFS/SUMIFS), nothing is baked.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_INT, S_NUM, S_LINK_NUM, S_DATE_LINK,
    S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_OVERVIEW, AS_OF_CELL
from workbook_army.sheets._analyst import ANALYST_DIR
from workbook_army.sheets.data_contract_families import families_cols
from workbook_army.sheets.model_market_size import TOTAL_REFS as MS
from workbook_army.sheets.model_budget_market import TOTAL_REFS as BM
from workbook_army.sheets import config as CFG

_GROUP = "summary"
_TAB = TAB_OVERVIEW
_NCOLS = 3
_COLS = [46, 18, 46]
_FLOOR = "1000000"
_EXTRACTED_DIR = ANALYST_DIR.parent / "extracted"


def _read(dirpath, name):
    """A CSV under dirpath as a list of dict rows (empty if absent)."""
    path = dirpath / f"{name}.csv"
    if not path.exists():
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _fnum(s):
    try:
        return float((s or "").strip())
    except (TypeError, ValueError):
        return 0.0


def _readiness():
    """Build-time analyst-layer completeness counts (x, y) - a snapshot read of the analyst
    CSVs, NOT a live formula (the values change only when the analyst edits + the build runs).
    Honest by construction: reads low until the analyst pass fills the durable bridges."""
    as_of = str(CFG.AS_OF)[:10]
    screened = [r for r in _read(_EXTRACTED_DIR, "contract_families")
                if (r.get("is_watercraft") or "").strip() == "Y"
                and _fnum(r.get("selected_measure")) >= 1_000_000]
    core = [r for r in screened if (r.get("saronic_tier") or "").split()[:1] == ["Core"]]
    forward = [r for r in screened
               if (r.get("effective_decision_date") or "").strip()[:10] >= as_of]
    attrib = {(r.get("family_key") or "").strip()
              for r in _read(ANALYST_DIR, "award_opportunity_attribution")
              if (r.get("opportunity_id") or "").strip()}
    reviews = {(r.get("family_key") or "").strip(): r
               for r in _read(ANALYST_DIR, "recompete_reviews")}

    def reviewed(k):
        r = reviews.get(k) or {}
        return bool((r.get("confidence") or "").strip()
                    or (r.get("pursuit_access") or "").strip())

    orgs = _read(ANALYST_DIR, "customer_org_map")
    edges = _read(ANALYST_DIR, "lineage_edges")
    assum = _read(ANALYST_DIR, "market_assumptions")
    return {
        "core_attr": (sum((r.get("family_key") or "").strip() in attrib for r in core),
                      len(core)),
        "fwd_rev": (sum(reviewed((r.get("family_key") or "").strip()) for r in forward),
                    len(forward)),
        "orgs_owned": (sum(((o.get("engagement_status") or "").strip() not in ("", "Not started")
                            or bool((o.get("saronic_relationship_owner") or "").strip()))
                           for o in orgs), len(orgs)),
        "edges_disp": (sum(bool((e.get("analyst_disposition") or "").strip()) for e in edges),
                       len(edges)),
        "assum_src": (sum(bool((a.get("source") or "").strip())
                          and "seed" not in (a.get("source") or "").lower() for a in assum),
                      len(assum)),
    }


def _make_overview():
    ISW = families_cols("is_watercraft")
    SEL = families_cols("selected_measure")
    SEG = families_cols("customer_segment")
    VT = families_cols("vehicle_type")
    HYD = families_cols("hydrated")
    AWO = families_cols("award_reported_obligation")
    radar = f'{ISW},"Y",{SEL},">="&{_FLOOR}'

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Market sizes, the contract evidence behind them, and analyst-layer readiness. "
             "Seed estimates until the analyst pass."], styles=[S_ITALIC])
    c.blank(2)

    def kv(label, value, style, note=""):
        c.write([label, value, note], styles=[S_DEFAULT, style, S_ITALIC])

    c.banner("§1 - Market size", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "$M", "Definition"],
            styles=header_styles(["Measure", "$M", "Definition"]))
    kv("Gross funded market (FY27-31)", f"={MS['gross']}", S_LINK_NUM,
       "funded demand: FY27 request + FY28-31 outyears (PB2027)")
    kv("Addressable market", f"={MS['addressable']}", S_LINK_NUM,
       "Gross x addressable %")
    kv("Saronic-serviceable market (SAM)", f"={MS['serviceable']}", S_LINK_NUM,
       "Addressable x Saronic fit %")
    kv("Weighted pursuit value (SOM)", f"={MS['weighted']}", S_LINK_NUM,
       "Serviceable x timing x pursuit x win")
    kv("Budget Market forward spine (cross-check)", f"={BM['forward']}", S_LINK_NUM,
       "should equal Gross funded - same source")
    c.blank()
    c.write(["Then-year $M on seed assumptions - not a validated estimate, and not additive "
             "to the historical obligations below."], styles=[S_ITALIC])

    c.blank(2)
    c.banner("§2 - Contract evidence", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "Value", "Note"], styles=header_styles(["Metric", "Value", "Note"]))
    kv("Screened universe (watercraft families >= $1.0M)", f"=COUNTIFS({radar})", S_INT,
       "the screened decision set")
    kv("Army operational watercraft families",
       f'=COUNTIFS({radar},{SEG},"Army operational watercraft & bridging")', S_INT,
       "the Saronic-relevant operational core")
    kv("USACE civil-works families",
       f'=COUNTIFS({radar},{SEG},"USACE floating plant / civil works")', S_INT,
       "different buyer/mission - not the same market")
    kv("IDV vehicles with hydrated parent end",
       f'=COUNTIFS({radar},{VT},"IDV vehicle",{HYD},"Y")', S_INT,
       "SAM Contract Awards API hydration")
    kv("Historical obligations represented ($M, award-reported)",
       f"=SUMIFS({AWO},{radar})/1000000", S_NUM,
       "SEPARATE lens - evidence of spend, never added to budget")

    c.blank(2)
    c.banner("§3 - Analyst readiness", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Readiness", "Filled / total", "Where to fill"],
            styles=header_styles(["Readiness", "Filled / total", "Where to fill"]))
    rd = _readiness()
    rk = lambda label, key, note: c.write(
        [label, f"{rd[key][0]} / {rd[key][1]}", note], styles=[S_DEFAULT, S_DEFAULT, S_ITALIC])
    rk("Core families attributed to an opportunity", "core_attr", "Opportunity attribution")
    rk("Forward pursuits reviewed (confidence / pursuit)", "fwd_rev", "Recompete reviews")
    rk("Customer organizations owned (beyond 'Not started')", "orgs_owned", "Customer map")
    rk("Lineage candidates dispositioned", "edges_disp", "Lineage dispositions")
    rk("Market assumptions independently sourced", "assum_src", "Market Assumptions")
    c.blank()
    c.write(["Build-time snapshot; reads low until the analyst pass fills the bridges. "
             "Re-run the build to refresh."], styles=[S_ITALIC])

    c.blank(2)
    c.banner("§4 - Freshness", n_cols=_NCOLS, style=S_TITLE_SECTION)
    c.blank()
    kv("Model As-of date", f"={AS_OF_CELL}", S_DATE_LINK,
       "editable on Timing & Incumbent Screen; re-clocks every expiry column")
    c.write(["Detail: Market Size, Budget Market, Timing Screen + Research Queue, Notice "
             "Links + Pipeline, QA, Data Freshness, Scope, Source Log."],
            styles=[S_DEFAULT])
    c.write(["Caveats: SAM Contract Awards is Revealed-only (DoD < 90 days excluded); market "
             "knobs are seed; lineage + notice links are candidate evidence, not verdicts."],
            styles=[S_ITALIC])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


OVERVIEW = _make_overview()
