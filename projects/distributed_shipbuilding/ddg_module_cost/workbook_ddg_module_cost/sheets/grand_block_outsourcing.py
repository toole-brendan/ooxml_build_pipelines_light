"""grand_block_outsourcing - the "DDG Grand-Block Outsourcing" tab (guide group).

The concrete evidence behind the SAM-to-Module Bridge argument. That tab says a
subaward can be placed in a physical grand block ONLY when its text explicitly
names one - and that this is rare. This tab is the case where it happens: for the
FY2018-22 multi-year buy, three yards fabricated whole grand blocks under subaward,
and their statement-of-work descriptions name the block ("GB B15", "GB A16 & A21",
"C15GB", "GRAND BLOCK", "(D52)").

  §1 Direct evidence  - the verbatim descriptions that name a block.
  §2 DDG 137 by block - the one full-coverage hull, net $ per named grand block.
  §3 By yard          - the three outsourcing yards, then-year $ net of credits.
  §4 Cost anchor      - observed outsourced structural fabrication per block vs the
                        Module Cost model's per-grand-block Basic-Construction split
                        (live = Assumptions numerator / grand-block count). The first
                        bottom-up sanity check on the top-down cascade.

Evidence values are then-year $M (net of credits), transcribed from the SAM.gov FSRS
subaward corpus and styled as inputs (like Outfit Context). The §2 / §3 totals are
live SUM() formulas, so a transcription slip fails recalc. The §4 model figure is a
live cross-sheet formula - it is NOT a value on this tab.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_NOTE, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_INT, S_PCT, S_LINK_NUM, S_NUM_INPUT, S_INT_INPUT,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from workbook_ddg_module_cost.sheets._layout import RowCursor
from workbook_ddg_module_cost.sheets._italic import S_ITALIC
from workbook_ddg_module_cost.sheets._tabs import (
    TAB_GRAND_BLOCK_OUT, TAB_SAM_MODULE_BRIDGE,
)
from workbook_ddg_module_cost.sheets import assumptions as A

_GROUP = "guide"
_NCOLS = 5   # widest table (§2): B block · C yard · D $M · E actions · F description

# §1 - the money quotes: descriptions that explicitly name a grand block / zone.
_QUOTES = [
    '"DDG 137 SOW UNIT OUTSOURCING (GB B15)"  -  BAE Systems Jacksonville, $17.7M (2 actions)',
    '"DDG 137 SOW UNIT OUTSOURCING (GB A16 & A21)"  -  Gulf Copper, $5.4M',
    '"DDG 137 SOW UNIT OUTSOURCING (GB B43 & B13)"  -  Gulf Copper, $5.0M',
    '"DDG 137 C15GB UNIT OUTSOURCING"  -  Eastern Shipbuilding, $5.3M',
    '"DDG 139 SOW UNIT OUTSOURCING (GB D52)"  -  Gulf Copper, $4.7M',
    '"DDG 137 GRAND BLOCK"  -  Gulf Copper, $0.7M',
]

# §2 - DDG 137, net then-year $M per named block (high -> low). Actions counts all
# subaward records incl. credits; descriptions are verbatim.
_DDG137 = [
    ("B15",             "BAE Jax",     17.72, 2, '"DDG 137 SOW UNIT OUTSOURCING (GB B15)"'),
    ("D52",             "Gulf Copper", 10.88, 5, '"DDG 137 SOW UNIT OUTSOURCING (D52)"'),
    ("A16 & A21",       "Gulf Copper",  5.37, 4, '"DDG 137 SOW UNIT OUTSOURCING (GB A16 & A21)"'),
    ("C15",             "Eastern",      5.31, 1, '"DDG 137 C15GB UNIT OUTSOURCING"'),
    ("B43 & B13",       "Gulf Copper",  5.01, 1, '"DDG 137 SOW UNIT OUTSOURCING (GB B43 & B13)"'),
    ("D41 / D42",       "Gulf Copper",  2.51, 3, '"DDG 137 SOW UNIT OUTSOURCING (D41/D42)"'),
    ("D11 / D21 / D31", "Gulf Copper",  1.68, 1, '"DDG 137 SOW UNIT OUTSOURCING (D11, D21, D31)"'),
    ("(unlabeled)",     "Gulf Copper",  0.74, 1, '"DDG 137 GRAND BLOCK"'),
]

# §3 - the three outsourcing yards (net then-year $M, actions, hulls touched).
_YARDS = [
    ("Gulf Copper & Mfg",        31.59, 17, "135, 137, 139"),
    ("BAE Systems Jacksonville", 17.72,  2, "137"),
    ("Eastern Shipbuilding",      5.65,  3, "135, 137, 139"),
]

_LARGEST_BLOCK = 17.72   # §4 anchor: BAE GB B15, the largest single outsourced block.


def _make():
    P: dict = {}
    c = RowCursor(2)
    c.title(TAB_GRAND_BLOCK_OUT, _NCOLS)
    c.caption("Outsourced grand-block fabrication - the subawards that name a physical block")
    c.blank(2)

    # §1 Direct evidence --------------------------------------------------------------
    c.section("§1 - Direct evidence: subawards that name a grand block", _NCOLS)
    c.blank()
    c.write([f"For the FY2018-22 multi-year buy, three yards fabricated whole grand blocks "
             f"under subaward. Unlike routine component supply, their statement-of-work "
             f"descriptions name the block - the rare explicit-text case the "
             f"{TAB_SAM_MODULE_BRIDGE} tab (§2-§3) calls for."],
            styles=[S_ITALIC])
    c.blank()
    for quote in _QUOTES:
        c.write([quote], styles=[S_NOTE])
    c.blank()
    c.write(["3 yards  |  22 subaward actions  |  hulls DDG 135 / 137 / 139  |  "
             "$55.0M then-year (net of credits)"], styles=[S_BOLD])
    c.blank(2)

    # §2 DDG 137 by grand block -------------------------------------------------------
    c.section("§2 - DDG 137 by grand block (the full-coverage hull)", _NCOLS)
    c.blank()
    c.write(["Grand block", "Yard", "Net $M", "Actions", "Description (verbatim)"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    b0 = c.at()
    for blk, yard, dollars, acts, desc in _DDG137:
        c.write([blk, yard, dollars, acts, desc],
                styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_INT_INPUT, S_ITALIC])
    b1 = c.at() - 1
    P["ddg137_total"] = c.total(
        ["DDG 137 grand-block total", "", f"=SUM(D{b0}:D{b1})", f"=SUM(E{b0}:E{b1})", ""],
        styles=[S_BOLD, S_DEFAULT, S_NUM, S_INT, S_DEFAULT], n_cols=_NCOLS)
    c.write(["D52 is net of a -$7.2M Oct-2025 rescope (partial deobligation of an $8.2M award); "
             "the (unlabeled) row's SOW reads only \"GRAND BLOCK\"."], styles=[S_NOTE])
    c.blank(2)

    # §3 By yard ----------------------------------------------------------------------
    c.section("§3 - By yard (all hulls, then-year $ net of credits)", _NCOLS)
    c.blank()
    c.write(["Yard", "Net $M", "Actions", "Hulls"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    y0 = c.at()
    for yard, dollars, acts, hulls in _YARDS:
        c.write([yard, dollars, acts, hulls],
                styles=[S_DEFAULT, S_NUM_INPUT, S_INT_INPUT, S_DEFAULT])
    y1 = c.at() - 1
    P["yards_total"] = c.total(
        ["Grand-block outsourcing, 3 yards", f"=SUM(C{y0}:C{y1})", f"=SUM(D{y0}:D{y1})", ""],
        styles=[S_BOLD, S_NUM, S_INT, S_DEFAULT], n_cols=4)
    c.write(["By hull: DDG 137 $49.2M · DDG 139 $4.8M · DDG 135 $0.9M. All on the FY2018-22 "
             "block-buy; all read in-build (post-keel) on the SAM timing axis."],
            styles=[S_NOTE])
    c.blank(2)

    # §4 Cost anchor ------------------------------------------------------------------
    c.section("§4 - Cost anchor: outsourced fabrication vs the model", _NCOLS)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["model_block"] = c.write(
        ["Model allocation per grand block (even split)",
         f"={A.numerator_cell()}/{A.count_cell('blocks')}"],
        styles=[S_DEFAULT, S_LINK_NUM])
    P["b15"] = c.write(
        ["Largest outsourced block (BAE, GB B15)", _LARGEST_BLOCK],
        styles=[S_DEFAULT, S_NUM_INPUT])
    c.write(["  as share of the model per-block allocation",
             f"=C{P['b15']}/C{P['model_block']}"],
            styles=[S_DEFAULT, S_PCT])
    c.blank()
    c.write(["Outsourced work is bare structural fabrication (steel + welding) of a grand "
             "block - a FLOOR on that block's cost. Observed per block runs ~$1.7M-$17.7M, "
             "roughly 2-24% of the model's fully-burdened Basic-Construction allocation; "
             "erection, outfitting, systems integration and test stay at the prime yard."],
            styles=[S_NOTE])
    c.write(["The model figure is an even split; the outsourced hull-structure blocks (A/B/C/D "
             "zones) are likely below-average-cost blocks, so read this as an order-of-magnitude "
             "band, not a precise ratio. Then-year $ vs the model's const FY2026 $ differ ~2-4% "
             "here - immaterial to the band."], styles=[S_NOTE])
    c.blank(2)

    c.write(["Source: SAM.gov FSRS first-tier subaward records, DDG-51 program; grand-block rows "
             "are those whose description explicitly names a PWBS block / zone (GB A16, GB B15, "
             "C15GB, D52, ...). Then-year $M, net of credits. Captured 2026-07-01."],
            styles=[S_NOTE])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[40, 20, 12, 11, 56],
                       tab_color=group_color(_GROUP), with_gutter=True,
                       show_outline_symbols=False)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_GRAND_BLOCK_OUT, _GROUP, render)


GRAND_BLOCK_OUTSOURCING = _make()
