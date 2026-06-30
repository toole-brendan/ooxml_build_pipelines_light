"""sam_module_bridge - the "SAM-to-Module Bridge Notes" tab (guide group).

A documentation bridge between this workbook's HII production hierarchy (ship -> modules ->
grand blocks -> structural units) and the SAM / subawards workbook's vendor / ship-system / timing
evidence. Its job is to keep the two dimensions distinct: SWBS is a FUNCTIONAL / system taxonomy;
module / grand block / structural unit is a PHYSICAL / production breakdown (a PWBS). Subaward text
supports SWBS / vendor / hull / timing - it usually cannot place a part in a physical module - so
module attribution must not be inferred from subaward text unless the text explicitly says so.
Prose only; no figures (the cost cascade lives on Module Cost).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import S_DEFAULT, S_BOLD, S_NOTE, S_HEADER_LEFT
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from workbook_ddg_module_cost.sheets._layout import RowCursor
from workbook_ddg_module_cost.sheets._italic import S_ITALIC
from workbook_ddg_module_cost.sheets._tabs import (
    TAB_SAM_MODULE_BRIDGE, TAB_STRUCTURAL_HIER, TAB_OUTFIT_CONTEXT,
)

_GROUP = "guide"
_NCOLS = 2
_COLS = [34, 86]


def _kv(c: RowCursor, topic: str, detail: str) -> int:
    return c.write([topic, detail], styles=[S_BOLD, S_DEFAULT])


def _make():
    c = RowCursor(2)
    c.title(TAB_SAM_MODULE_BRIDGE, _NCOLS)
    c.caption("How the SAM subaward evidence relates to HII's physical build hierarchy - and where it does not.")
    c.blank(2)

    # §1 two dimensions ---------------------------------------------------------------
    c.section("§1 - Two different dimensions", _NCOLS)
    c.write(["SWBS and the module hierarchy describe the ship along different axes. A part has "
             "both, but a subaward usually reveals only one."], styles=[S_ITALIC])
    c.blank()
    _kv(c, "SWBS (functional)", "Ship Work Breakdown Structure - a functional / system taxonomy "
                                "(hull structure, propulsion, electric, auxiliary, ...). Answers "
                                "WHICH SYSTEM a part belongs to. The SAM workbook tags HII-DDG "
                                "subawards to SWBS via the HII work-item code crosswalk.")
    _kv(c, "Module / grand block / unit (physical)",
        f"HII's production / product breakdown: how the yard fabricates, outfits, and erects the "
        f"ship (ship -> 4 modules -> 21 grand blocks -> 72 structural units). Answers WHERE in the "
        f"build a piece is assembled. See the {TAB_STRUCTURAL_HIER} tab.")
    _kv(c, "Why they differ", "A pump, valve, cable, or radar component has a ship SYSTEM (SWBS) "
                              "and a vendor, but its physical module / grand block is generally not "
                              "knowable from public subaward text.")
    c.blank(2)

    # §2 what subawards support -------------------------------------------------------
    c.section("§2 - What a SAM subaward can attribute", _NCOLS)
    c.write(["The dimensions the subaward evidence does - and does not - support."],
            styles=[S_ITALIC])
    c.blank()
    c.write(["Dimension", "Subaward support"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for dim, sup in [
        ("Ship system / work type (SWBS)", "Yes - via the HII work-item code crosswalk (HII-DDG only)."),
        ("Vendor", "Yes - the subawardee entity (UEI)."),
        ("Hull", "Often - confidence-scored (see the SAM Hull Mapping Methodology)."),
        ("Timing", "Yes - the subaward action date."),
        ("Physical module / grand block / unit",
         "Rarely - only when the text explicitly names a module, block, zone, unit, or drawing."),
    ]:
        c.write([dim, sup], styles=[S_DEFAULT, S_DEFAULT])
    c.blank(2)

    # §3 attribution rules ------------------------------------------------------------
    c.section("§3 - Attribution rules", _NCOLS)
    c.write(["How to use the subaward evidence without overstating it."], styles=[S_ITALIC])
    c.blank()
    _kv(c, "SWBS first", "Use SWBS as the primary work taxonomy for subaward spend.")
    _kv(c, "Module only on explicit text", "Attribute a subaward to a module / grand block / zone "
                                           "ONLY when its text explicitly references one.")
    _kv(c, "Notional allocation = scenario", "Spreading subaward $ across modules by structural "
                                             "weight is scenario analysis, not factual assignment.")
    _kv(c, "The bridge", "Subaward -> SWBS / work type -> hull -> (later) lifecycle stage. NOT "
                         "usually subaward -> structural unit / grand block.")
    c.write([f"The {TAB_OUTFIT_CONTEXT} tab shows HII-Ingalls subaward $ by SWBS major group as "
             f"context - it is subawardee spend, NOT a structural-unit cost weight."],
            styles=[S_NOTE])
    c.blank(2)

    # §4 the archetype ----------------------------------------------------------------
    c.section("§4 - The archetype (where the hierarchy comes from)", _NCOLS)
    c.write(["The module hierarchy is a production breakdown, not a contract or functional one."],
            styles=[S_ITALIC])
    c.blank()
    _kv(c, "Not Contract WBS", "Module / grand block / unit is not the MIL-STD-881 contract WBS "
                               "(acquisition cost / reporting) nor SWBS (functional). It is a "
                               "product / production breakdown.")
    _kv(c, "PWBS lineage", "Product Work Breakdown Structure / zone-block / group-technology "
                           "shipbuilding - IHI (Ishikawajima-Harima, Japan) origin, transmitted "
                           "into US yards via MARAD / NSRP around 1980 (NSRP-0164, Product Work "
                           "Breakdown Structure, rev. Dec 1982).")
    _kv(c, "DDG-51 tie", "The 1988 MIT thesis (Seubert) ties IHI PWBS and modular shipbuilding to "
                         "the DDG-51 class at Bath Iron Works.")
    c.write(["Sources: NSRP-0164 (HathiTrust, full view); 'Ship Work Breakdown Structures Through "
             "Different Ship Lifecycle Stages' (CWBS / SWBS / PWBS / ZWBS); OSTI biblio 6892557 "
             "(Seubert 1988)."], styles=[S_NOTE])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=False)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_SAM_MODULE_BRIDGE, _GROUP, render)


SAM_MODULE_BRIDGE = _make()
