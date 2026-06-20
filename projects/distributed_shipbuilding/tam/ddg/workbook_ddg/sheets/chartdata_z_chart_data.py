"""chartdata_z_chart_data - the "z_ChartData" tab (DDG): think-cell paste blocks.

Production-support tab (off the analytical read): one block per native chart that
renders in the deck, laid out exactly as think-cell's embedded datasheet wants it
- category / step labels across the top row, values in the row(s) beneath - and
styled as a copy-paste-ready range (pale-yellow fill + thin black perimeter, the
S_PASTE_* styles). The z_ prefix sorts the tab last.

Block -> chart (deck slide order; shape = rows x cols of the paste rectangle):
  §1 Cost funnel              waterfall (2x5)      Total ship -> -GFE -> -other -> Basic Construction("e")
  §2 MYP POP distribution     stacked column (6x2) BIW / Ingalls / Other-US / Foreign / Unparsed shares
  §3 MYP outside-yards split  stacked column (2x3) MYP-corrected vs disclosed-artifact share
  §4 Annual TAM build         waterfall (2x6)      BC base -> -non-supplier -> BC stream("e") -> +AP/LLTM -> TAM("e")
  §5 TAM by fiscal year       stacked column (3x7) BC + AP/LLTM stream, FY22-27
  §6 Work-type allocation     ranked column (2x9)  Unbucketed residual + 7 work-type buckets
  §7 SAM scenarios            ranked column (2x6)  five scenario cuts, avg annual SAM
  §8 Supplier landscape       bar (10x2)           top-10 visible suppliers (names down, $ across)
  §9 FFATA visibility gap     column (2x5)         visible flow vs low / mid / high outsourcing bands
  §10 Penetration strip       line/strip (4x11)    Outsourced BC / total ship spend, FY22-27 + assumed FY28-31
  §11 Outyear implied BC      stacked column (3x5) implied low + range-to-high, FY28-31
  §12 FY22-25 average TAM     reference (2x2)      the pre-OBBBA dashed-line level

think-cell waterfall convention: every data cell is a STEP, so a computed
subtotal/total is the literal text marker "e" (think-cell draws a calculated bar
from the prior steps; a numeric subtotal would double-count). Values are live links
to producer cells; avg-annual blocks divide a cumulative producer by the fiscal-year
count, and $B blocks are model $M producers (kept as $M here). FFATA-gap band values
have no model producer, so they are summed from cost_funnel_summary.csv.

Pure consumer (links producers, exports no accessors; deck-loader leaf).
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_TITLE_SHEET, S_TITLE_SECTION,
    S_PASTE_HEADER_TL, S_PASTE_HEADER_T, S_PASTE_HEADER_TR,
    S_PASTE_LABEL_L, S_PASTE_LABEL_BL,
    S_PASTE_VAL_INT_M, S_PASTE_VAL_R_M, S_PASTE_VAL_B_M, S_PASTE_VAL_BR_M,
    S_PASTE_VAL_INT_B, S_PASTE_VAL_R_B, S_PASTE_VAL_B_B, S_PASTE_VAL_BR_B,
    S_PASTE_VAL_INT_P, S_PASTE_VAL_R_P, S_PASTE_VAL_B_P, S_PASTE_VAL_BR_P,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.lib import EXTRACTED
from workbook_ddg.sheets._layout import RowCursor
from workbook_ddg.sheets.model_tam_build import (
    portfolio_bc_base_cell, portfolio_ap_tam_cell, pop_removal_cell, n_years_cell,
    tam_bc_total_cell, tam_ap_total_cell,
    biw_pop_share_cell, ingalls_pop_share_cell, other_pop_share_cell,
    foreign_pop_share_cell, unparsed_pop_share_cell,
    outside_yards_corrected_cell, outside_yards_disclosed_cell,
)
from workbook_ddg.sheets.model_sam_build import (
    bucket_tam_cell, unbucketed_tam_cell, sam_avg_annual_cell,
)
from workbook_ddg.sheets.data_scn_budget import portfolio_scn_cell
from workbook_ddg.sheets.data_entity_master import ent_row_cell, top_supplier_indices
from workbook_ddg.sheets.model_outlook import (
    penetration_cell, assumption_low_cell, assumption_high_cell,
    outyear_low_cell, outyear_high_cell, tam_fy2225_avg_cell,
)

_GROUP = "chartdata"
_TAB = "z_ChartData"
_NCOLS = 11                      # widest paste block (penetration strip, 1 + 10); banners span this
_FYS = list(range(2022, 2028))
_OYS = list(range(2028, 2032))


# --- think-cell paste-range emitter ---------------------------------------
# Per unit, the value-cell styles for {interior, right edge, bottom edge,
# bottom-right corner}. The left column is always a label (S_PASTE_LABEL_*),
# the top row always a header (S_PASTE_HEADER_*), so values never sit on the
# top or left edge.
_VAL_STYLE = {
    "M": {"INT": S_PASTE_VAL_INT_M, "R": S_PASTE_VAL_R_M, "B": S_PASTE_VAL_B_M, "BR": S_PASTE_VAL_BR_M},
    "B": {"INT": S_PASTE_VAL_INT_B, "R": S_PASTE_VAL_R_B, "B": S_PASTE_VAL_B_B, "BR": S_PASTE_VAL_BR_B},
    "P": {"INT": S_PASTE_VAL_INT_P, "R": S_PASTE_VAL_R_P, "B": S_PASTE_VAL_B_P, "BR": S_PASTE_VAL_BR_P},
}


def _paste_block(c, title, header, rows, unit):
    """Emit one think-cell paste rectangle: section banner, one blank, then the
    bordered grid (header row + data rows), then two blank rows.

    header: full top row; header[0] is the (blank) corner, header[1:] are the
        across-the-top category / step labels. rows: list of (row_label, [values])
        where row_label fills the left column ("" for a single-series block; a
        series / item name for a matrix) and values align to header[1:]. A value
        is a formula string ("=..."), the waterfall marker "e", or a numeric literal.
    """
    c.banner(title, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    ncol = len(header) - 1
    vs = _VAL_STYLE[unit]
    c.write(header,
            styles=[S_PASTE_HEADER_TL] + [S_PASTE_HEADER_T] * (ncol - 1) + [S_PASTE_HEADER_TR],
            outline_level=1)
    n = len(rows)
    for i, (label, vals) in enumerate(rows):
        last = (i == n - 1)
        styles = [S_PASTE_LABEL_BL if last else S_PASTE_LABEL_L]
        for j in range(1, ncol + 1):
            if last:
                styles.append(vs["BR"] if j == ncol else vs["B"])
            else:
                styles.append(vs["R"] if j == ncol else vs["INT"])
        c.write([label, *vals], styles=styles, outline_level=1)
    c.blank(2)


def _load_ffata() -> dict:
    """Sum FFATA-gap bands from cost_funnel_summary.csv (LI 2122) - source-backed."""
    keys = {"visible": "ffata_visible_yards_$M", "low": "bc_outsourced_low_$M",
            "mid": "bc_outsourced_mid_$M", "high": "bc_outsourced_high_$M"}
    tot = {k: 0.0 for k in keys}
    with (EXTRACTED / "cost_funnel_summary.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if (r.get("LI") or "").strip() != "2122":
                continue
            for k, col in keys.items():
                try:
                    tot[k] += float((r.get(col) or "0").replace(",", "") or 0)
                except ValueError:
                    pass
    return {k: round(v, 1) for k, v in tot.items()}


def _render_chart_data() -> WorksheetSpec:
    nyr = n_years_cell()
    ffata = _load_ffata()

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 - Cost funnel (waterfall, decreasing): FY2022-FY2027 cumulative total ship
    # estimate -> Basic Construction base (links the SCN Budget §3 portfolio producer).
    _tot = portfolio_scn_cell("total")
    _gfe = portfolio_scn_cell("gfe")
    _oth = portfolio_scn_cell("other_non_bc")
    _paste_block(c, "§1 - Cost funnel (waterfall)",
                 ["", "Total ship", "Less GFE", "Less other", "Basic Construction"],
                 [("", [f"={_tot}", f"=-{_gfe}", f"=-{_oth}", "e"])],
                 "M")

    # §2 - MYP place-of-performance distribution (single 100%-stacked column).
    _paste_block(c, "§2 - MYP POP distribution (stacked column)",
                 ["", "POP share"],
                 [("BIW site", [f"={biw_pop_share_cell()}"]),
                  ("Ingalls site", [f"={ingalls_pop_share_cell()}"]),
                  ("Other-US supplier", [f"={other_pop_share_cell()}"]),
                  ("Foreign", [f"={foreign_pop_share_cell()}"]),
                  ("Unparsed", [f"={unparsed_pop_share_cell()}"])],
                 "P")

    # §3 - MYP outside-yards share: corrected vs disclosed artifact (stacked column).
    _paste_block(c, "§3 - MYP outside-yards split (stacked column)",
                 ["", "MYP-corrected", "Disclosed artifact"],
                 [("Outside-yards share",
                   [f"={outside_yards_corrected_cell()}", f"={outside_yards_disclosed_cell()}"])],
                 "P")

    # §4 - Annual TAM build (waterfall), average annual $M.
    _paste_block(c, "§4 - Annual TAM build (waterfall)",
                 ["", "BC base", "Less non-supplier", "BC stream", "AP/LLTM", "Portfolio TAM"],
                 [("", [f"={portfolio_bc_base_cell()}/{nyr}", f"=-{pop_removal_cell()}/{nyr}",
                        "e", f"={portfolio_ap_tam_cell()}/{nyr}", "e"])],
                 "M")

    # §5 - TAM by fiscal year, stacked by stream (matrix: FY across, stream down).
    _paste_block(c, "§5 - TAM by fiscal year (stacked column)",
                 ["", *[f"FY{fy - 2000}" for fy in _FYS]],
                 [("BC stream", [f"={tam_bc_total_cell(fy)}" for fy in _FYS]),
                  ("AP/LLTM stream", [f"={tam_ap_total_cell(fy)}" for fy in _FYS])],
                 "M")

    # §6 - Work-type allocation (ranked column), average annual $M. Residual first
    # (the hero bar), then the seven named work-type buckets in chart order.
    _wt = [("Unbucketed", unbucketed_tam_cell()), ("Electrical/power", bucket_tam_cell("electrical")),
           ("Structural", bucket_tam_cell("structural")), ("Machining", bucket_tam_cell("machining")),
           ("Piping/valves", bucket_tam_cell("piping")), ("HVAC", bucket_tam_cell("hvac")),
           ("Coatings", bucket_tam_cell("coatings")), ("Castings", bucket_tam_cell("castings"))]
    _paste_block(c, "§6 - Work-type allocation (ranked column)",
                 ["", *[lab for lab, _ in _wt]],
                 [("", [f"={ref}/{nyr}" for _, ref in _wt])],
                 "M")

    # §7 - SAM scenarios (ranked column), average annual SAM $M.
    _sc = [("Broad components", "broad"), ("Metal components", "metal"),
           ("Electrical/power", "electrical"), ("Modular assy", "modular"), ("HM&E", "hme")]
    _paste_block(c, "§7 - SAM scenarios (ranked column)",
                 ["", *[lab for lab, _ in _sc]],
                 [("", [f"={sam_avg_annual_cell(k)}" for _, k in _sc])],
                 "M")

    # §8 - Supplier landscape (horizontal bar): top-10 visible suppliers, names
    # down the left column, lifetime visible flow across (bar = labels-down).
    _sup = top_supplier_indices(10)
    _paste_block(c, "§8 - Supplier landscape (bar)",
                 ["", "Visible flow"],
                 [(f"={ent_row_cell(i, 'vendor')}", [f"={ent_row_cell(i, 'dollar')}"]) for i in _sup],
                 "M")

    # §9 - FFATA visibility gap (single-series column). CSV-summed band inputs
    # (no model producer) - the one block whose values are literals, not links.
    _paste_block(c, "§9 - FFATA visibility gap (column)",
                 ["", "Visible flow", "Outsourcing low", "Outsourcing mid", "Outsourcing high"],
                 [("", [ffata["visible"], ffata["low"], ffata["mid"], ffata["high"]])],
                 "M")

    # §10 - Penetration strip: Outsourced BC TAM / total ship spend per FY
    # (Outlook §2), with the FY28-31 assumed range (Outlook §3) in the outyears.
    _fy_hdr = [f"FY{fy - 2000}" for fy in _FYS + _OYS]
    _paste_block(c, "§10 - Outsourced BC penetration (strip)",
                 ["", *_fy_hdr],
                 [("Actual", [f"={penetration_cell(fy)}" for fy in _FYS] + [None] * 4),
                  ("Assumed low", [None] * 6 + [f"={assumption_low_cell()}"] * 4),
                  ("Assumed high", [None] * 6 + [f"={assumption_high_cell()}"] * 4)],
                 "P")

    # §11 - Implied outyear Outsourced BC (Outlook §4): stacked low + range cap.
    _paste_block(c, "§11 - Implied outyear Outsourced BC (stacked column)",
                 ["", *[f"FY{fy - 2000}" for fy in _OYS]],
                 [("Implied low", [f"={outyear_low_cell(fy)}" for fy in _OYS]),
                  ("Range to high", [f"={outyear_high_cell(fy)}-{outyear_low_cell(fy)}"
                                     for fy in _OYS])],
                 "M")

    # §12 - FY22-25 average annual TAM (Outlook §5): the dashed reference line.
    _paste_block(c, "§12 - FY22-25 average annual TAM (reference line)",
                 ["", "FY22-25 avg"],
                 [("", [f"={tam_fy2225_avg_cell()}"])],
                 "M")

    ws = worksheet(c.rows, cols=[40] + [18] * (_NCOLS - 1),
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


CHART_DATA = SheetEntry(_TAB, _GROUP, _render_chart_data)
