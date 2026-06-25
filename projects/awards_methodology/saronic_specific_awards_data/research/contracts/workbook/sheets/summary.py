"""Summary - the answer page. EVERY headline figure is a live formula off the data
tabs (black = derived); there are no hardcoded constants. The portal coverage, tier
sizing, and coverage-gap that used to be cited inputs now compute off Portal Notices,
Market Tiers, and Award-Opportunity Match.

  §1 The visibility gap - portal coverage off Portal Notices; the same vendor reads as
     $0 conventional vs $374M OT, both off OT Layer.
  §2 Forward signals - the recompete radar and teaming map.
  §3 Market structure - tier sizing off Market Tiers, top-5 prime share off Prime
     Concentration, the coverage gap off Award-Opportunity Match.
  §4 Backtest - the Phase-2 replay, off Backtest Events.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_NUM, S_INT, S_PCT,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from ..helpers import RowCursor, S_ITALIC
from .ot_layer import ot_cols
from .recompete_radar import radar_cols
from .teaming_edges import teaming_cols
from .prime_concentration import conc_cols
from .market_tiers import tiers_cols
from .portal_notices import portal_cols
from .award_opp_match import match_cols
from .backtest_events import bt_cols

_TAB = "Summary"
_GROUP = "summary"
_NCOLS = 4
_COLS = [44, 16, 16, 34]

# Tiers: (key, display). Awards and obligated are computed live off Market Tiers
# (COUNTIF / SUMIF); the top-5 prime share off Prime Concentration.
_TIERS = [
    ("usv_core",       "USV / autonomy"),
    ("small_craft",    "Small craft"),
    ("other_small",    "Other small vessels"),
    ("broad_maritime", "Broad maritime"),
]


def _ot(col: str) -> str:
    return ot_cols(col)


def _kpi(c: RowCursor, label, value, note, *, vstyle, lstyle=S_DEFAULT, sec=None,
         sstyle=S_NUM):
    """One metric row: label · value · optional secondary value · italic note."""
    c.write([label, value, sec, note], styles=[lstyle, vstyle, sstyle, S_ITALIC])


def _make_summary() -> SheetEntry:
    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.title(_TAB, _NCOLS)
        c.caption("Every figure is a live formula off the data tabs (no hardcoded "
                  "constants). Obligations, not ceilings; FY2015-26, pulled 2026-06-23.")
        c.blank(2)

        # ── §1 The visibility gap ───────────────────────────────────────────────
        c.section("§1 - The visibility gap: the same market read three ways", _NCOLS)
        c.blank()
        _kpi(c, "SAM Opportunities portal, USV-relevant notices",
             f'=COUNTIF({portal_cols("_subject")},"usv_autonomy")'
             f'/COUNTA({portal_cols("_subject")})',
             "49 of 669 notices. Source: Portal Notices", vstyle=S_PCT)
        _kpi(c, "SAM Opportunities portal, recurring-sustainment notices",
             f'=(COUNTIF({portal_cols("_subject")},"ship_repair_maintenance")'
             f'+COUNTIF({portal_cols("_subject")},"marine_components_parts"))'
             f'/COUNTA({portal_cols("_subject")})',
             "ship repair and parts. Source: Portal Notices", vstyle=S_PCT)
        c.blank()
        _kpi(c, "Saronic, standard FPDS pull (A-D, IDV), obligated $M",
             f'=SUMIFS({_ot("obligated_$m")},{_ot("vendor")},"SARONIC TECHNOLOGIES",'
             f'{_ot("is_ot")},"no")',
             "conventional awards only; OTs are dropped by the feed",
             vstyle=S_NUM, lstyle=S_BOLD)
        _kpi(c, "Saronic, SAM Contract Awards OT layer, obligated $M",
             f'=SUMIFS({_ot("obligated_$m")},{_ot("vendor")},"SARONIC TECHNOLOGIES",'
             f'{_ot("is_ot")},"yes")',
             "the same vendor, the layer FPDS drops",
             vstyle=S_NUM, lstyle=S_BOLD)
        _kpi(c, "Flagship OT N000242596305 (Navy/PEO-USC), obl / ceiling $M",
             f'=SUMIFS({_ot("obligated_$m")},{_ot("piid")},"N000242596305")',
             "signed 2025-05-16. Source: OT Layer",
             vstyle=S_NUM,
             sec=f'=SUMIFS({_ot("ceiling_$m")},{_ot("piid")},"N000242596305")',
             sstyle=S_NUM)
        c.blank(2)

        # ── §2 Forward signals ──────────────────────────────────────────────────
        c.section("§2 - Forward signals: recompete radar and teaming map", _NCOLS)
        c.blank()
        _kpi(c, "Recompete radar, vehicles surfaced (>= $5M)",
             f'=COUNTA({radar_cols("vehicle_piid")})',
             "clock = FPDS ordering-period end; Mechanism 1", vstyle=S_INT, lstyle=S_BOLD)
        _kpi(c, "   ordering period already closed (overdue, no successor seen)",
             f'=COUNTIF({radar_cols("months_to_clock")},"<0")', None, vstyle=S_INT)
        _kpi(c, "   reaching turnover within 36 months",
             f'=COUNTIFS({radar_cols("months_to_clock")},">=0",'
             f'{radar_cols("months_to_clock")},"<=36")', None, vstyle=S_INT)
        _kpi(c, "   no matching SAM Opportunities notice",
             f'=COUNTIF({radar_cols("portal_notice")},"NONE")'
             f'/COUNTA({radar_cols("portal_notice")})',
             "share with no portal notice", vstyle=S_PCT)
        c.write(["Clocks re-based on FPDS lastDateToOrder (the authoritative ordering-period "
                 "end); the Stage-2 order-PoP clock ran early or late on 33 of 52. 8 recent "
                 "IDVs run beyond 36 months."], styles=[S_ITALIC])
        c.blank()
        _kpi(c, "Teaming map, first-tier subaward edges",
             f'=COUNTA({teaming_cols("prime_piid")})',
             "reported floor; Mechanism 3", vstyle=S_INT, lstyle=S_BOLD)
        _kpi(c, "   subaward dollars, $M",
             f'=SUM({teaming_cols("sub_amount")})', None, vstyle=S_NUM)
        _kpi(c, "   distinct subcontractors",
             f'=SUMPRODUCT(1/COUNTIF({teaming_cols("sub_key")},{teaming_cols("sub_key")}))',
             "distinct sub keys across the edges", vstyle=S_INT)
        c.blank(2)

        # ── §3 Market structure ─────────────────────────────────────────────────
        c.section("§3 - Market structure: addressable tiers and prime gating", _NCOLS)
        c.blank()
        c.write(["Tier", "Awards", "Obligated $M", "Top-5 prime share"],
                styles=[S_BOLD, S_BOLD, S_BOLD, S_BOLD])
        tier_rows = {}
        for key, disp in _TIERS:
            awards = f'=COUNTIF({tiers_cols("tier")},"{key}")'
            obl = f'=SUMIF({tiers_cols("tier")},"{key}",{tiers_cols("award_amount")})'
            top5 = (f'=SUMPRODUCT(LARGE(({conc_cols("tier")}="{key}")*'
                    f'{conc_cols("share_pct")},{{1;2;3;4;5}}))/100')
            tier_rows[key] = c.write([disp, awards, obl, top5],
                                     styles=[S_DEFAULT, S_INT, S_NUM, S_PCT])
        ru, rs, ro = tier_rows["usv_core"], tier_rows["small_craft"], tier_rows["other_small"]
        c.write(["Addressable (excl. broad maritime)",
                 f"=C{ru}+C{rs}+C{ro}", f"=D{ru}+D{rs}+D{ro}", None],
                styles=[S_BOLD, S_INT, S_NUM, S_DEFAULT])
        c.write(["Awards and obligated live off Market Tiers (COUNTIF / SUMIF); "
                 "top-5 share off Prime Concentration."], styles=[S_ITALIC])
        c.blank()
        _kpi(c, "Addressable awards dark in the portal's 12-month window",
             f'=SUMIFS({match_cols("obligation")},{match_cols("in_opps_window")},"yes",'
             f'{match_cols("match_level")},"NONE")'
             f'/SUMIFS({match_cols("obligation")},{match_cols("in_opps_window")},"yes")',
             "share of in-window addressable $ with no notice. Source: Award-Opportunity Match",
             vstyle=S_PCT, lstyle=S_BOLD)
        c.write(["123 of 125 awards; 97 of 99 definitive."], styles=[S_ITALIC])
        c.blank(2)

        # ── §4 Backtest (Phase 2) ───────────────────────────────────────────────
        c.section("§4 - Backtest: would the radar have flagged recompetes early?", _NCOLS)
        c.blank()
        _kpi(c, "Recompete pairs tested (boat-IDIQ builder chains)",
             f'=COUNTA({bt_cols("predecessor")})',
             "point-in-time, no look-ahead", vstyle=S_INT, lstyle=S_BOLD)
        _kpi(c, "   parallel vehicles (predecessor still active, not a recompete)",
             f'=COUNTIF({bt_cols("event_class")},"parallel")',
             "radar correctly stays quiet", vstyle=S_INT)
        _kpi(c, "   true turnovers (predecessor closed around the successor)",
             f'=COUNTIF({bt_cols("event_class")},"<>parallel")', None, vstyle=S_INT)
        _kpi(c, "   of which anticipable at t-12 months",
             f'=COUNTIFS({bt_cols("event_class")},"<>parallel",'
             f'{bt_cols("anticipable_t12")},"Y")', None, vstyle=S_INT)
        _kpi(c, "   predecessor clock extended after t-12 (date-slip)",
             f'=COUNTIF({bt_cols("clock_extended_after_t12")},"Y")', None, vstyle=S_INT)
        c.write(["The recompete clock (FPDS lastDateToOrder) is set at award, so it is on "
                 "record 2-6 years before the portal (which showed none of these). A "
                 "publishable hit-rate needs a solicitationId-linked event set; the builder-"
                 "chain set conflates recompetes with parallel vehicles."], styles=[S_ITALIC])
        c.blank(2)

        # ── Provenance ──────────────────────────────────────────────────────────
        c.write(["Sources: USAspending prime awards and subawards; SAM.gov Contract "
                 "Awards (by awardee UEI); SAM.gov Contract Opportunities. Pulled "
                 "2026-06-23, federal FY2015-26."], styles=[S_ITALIC])

        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


SUMMARY = _make_summary()
