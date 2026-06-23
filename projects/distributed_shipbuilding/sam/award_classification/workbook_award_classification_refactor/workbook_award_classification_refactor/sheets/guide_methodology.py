"""guide_methodology - the "Methodology" tab (guide group; one module = one sheet).

Scope, the classification axes, the assignment rule, and the inputs - the compact
method a reader needs to interpret the figures. Full code definitions live on the
Taxonomy tab (the shared ``_taxonomy`` leaf); this sheet only summarizes them.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_classification_refactor.sheets._layout import RowCursor
from workbook_award_classification_refactor.sheets._tabs import (
    TAB_METHODOLOGY, TAB_SUPPLIER_MASTER, TAB_NAICS_MAP,
    TAB_ARCHETYPE_OVERRIDES, TAB_PRIME_AWARDS, TAB_SWBS_CROSSWALK,
)

_GROUP = "guide"
_NCOLS = 2
_COLS = [34, 84]


def _kv(c: RowCursor, topic: str, detail: str) -> int:
    return c.write([topic, detail], styles=[S_BOLD, S_DEFAULT])


def _p(c: RowCursor, text: str) -> int:
    return c.write([text], styles=[S_DEFAULT])


def _render_methodology() -> WorksheetSpec:
    c = RowCursor(2)
    c.title(TAB_METHODOLOGY, _NCOLS)
    c.caption("Scope, classification axes, assignment rule, and inputs.")
    c.blank(2)

    # §1 Scope
    c.section("§1 - Scope", _NCOLS)
    c.blank()
    _kv(c, "Unit", "The supplier operating entity (UEI), classified per program - not the "
                   "corporate parent or the subaward transaction.")
    _kv(c, "Grain", "UEI x Program: one UEI can carry different labels across DDG-51, Virginia, "
                    "and Columbia.")
    _kv(c, "Included", "Hull-builder new-construction contracts, including shipbuilder-procured "
                       "non-nuclear long-lead / EOQ material (carried on the GDEB master / LLTM "
                       "PIIDs for submarines).")
    _kv(c, "Excluded", "Nuclear-reactor LLTM (BPMI); GFE / component-prime advance procurement "
                       "(GE propulsion, Aegis, etc.); design, lead-yard, ship-alteration, "
                       "planning-yard work; and MIB / BlueForge pass-throughs.")
    _kv(c, "Cross-program", "DDG long-lead is predominantly GFE, so the DDG base captures far "
                            "less AP / LLTM / EOQ than the submarine base - not a like-for-like "
                            "make / buy comparison.")
    _kv(c, "Dollars", "Subaward $ inherit the entity's labels (joined on UEI x program); NAICS "
                      "is a self-reported entity attribute, so transactions carry none of their own.")
    c.blank(2)

    # §2 Classification axes
    c.section("§2 - Classification axes", _NCOLS)
    c.blank()
    _p(c, "Two independent entity axes (one label each, with a forced catch-all) plus a "
          "transaction-level companion. Full code legend: Taxonomy tab.")
    c.blank()
    _kv(c, "Capability Domain (D)", "The technical ship area the entity is competent in. "
                                    "D1-D11, D0. Published.")
    _kv(c, "Primary Output (P)", "The physical form / integration level of what is delivered. "
                                 "P1-P6, P0. Published.")
    _kv(c, "Ship-System Application (SWBS)", "Which ship system a subaward supports; "
                                             "transaction-level, HII-DDG only. 100-900, X00 / L00 / U00.")
    c.blank(2)

    # §3 Assignment
    c.section("§3 - Assignment", _NCOLS)
    c.blank()
    _kv(c, "Precedence", "The curated vendor registry (hand-verified) overrides the NAICS-6 entity "
                         "default; unresolved only when neither resolves.")
    _kv(c, "Rule", "Per UEI x Program, take the most representative recurring output across the "
                   "vendor's contractual boundary, not the most sophisticated item in its portfolio. "
                   "Take the highest integration level only when items ship as one configured system.")
    _kv(c, "Output evidence", "Positive evidence only - an integration-suggestive NAICS never "
                              "auto-assigns a high-integration output.")
    c.blank(2)

    # §4 Inputs
    c.section("§4 - Inputs", _NCOLS)
    c.blank()
    c.write(["Input", "Use"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for src, use in [
        (TAB_SUPPLIER_MASTER, "supplier dimension: one row per UEI x program, with primary NAICS-6"),
        (TAB_NAICS_MAP, "NAICS-6 to D / P default archetype crosswalk (the long-tail mapping)"),
        (TAB_ARCHETYPE_OVERRIDES, "hand-researched (Program, UEI) overrides of the default"),
        ("Subaward Transactions", "the subaward-dollar fact spine (DDG / Virginia / Columbia)"),
        (TAB_PRIME_AWARDS, "in-scope prime contracts (USAspending place-of-performance + obligations)"),
        (TAB_SWBS_CROSSWALK, "HII work-item code to observed SWBS group (HII-DDG only)"),
    ]:
        c.write([src, use], styles=[S_DEFAULT, S_DEFAULT])

    ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                   with_gutter=True, show_outline_symbols=False)
    return WorksheetSpec(ws)


METHODOLOGY = SheetEntry(TAB_METHODOLOGY, _GROUP, _render_methodology)
