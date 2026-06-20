"""chartdata_z_chart_data - the "z_ChartData" tab (submarines): think-cell paste blocks.

Production-support tab (off the analytical read): one block per native chart that
renders in the deck, laid out exactly as think-cell's embedded datasheet wants it
- category / step labels across the top row, values in the row(s) beneath - and
styled as a copy-paste-ready range (pale-yellow fill + thin black perimeter, the
S_PASTE_* styles). The z_ prefix sorts the tab last.

Block -> chart (deck slide order; shape = rows x cols of the paste rectangle):
  §1 Basic Construction     stacked column (3x7) Virginia + Columbia BC by FY22-27 ($B)
  §2 Annual cadence         clustered column (3x7) annual TAM vs broad SAM by FY22-27 ($B)
  §3 Coefficient evidence   ranked column (2x4)  POP anchor / AP-LLTM ref / Applied BC (%)
  §4 AP and LLTM bridge     waterfall (2x6)      Gross AP -> -GFE -> -inside BC -> -overlap -> base("e") ($B)
  §5 Work-type (bucket) TAM ranked column (2x8)  seven work-type buckets, avg annual ($M)
  §6 SAM scenarios          ranked column (2x6)  five scenario cuts, avg annual SAM ($M)
  §7 Visible suppliers      bar (10x2)           top-10 visible suppliers (names down, $ across)
  §8 SIB exclusion          waterfall (2x5)      BlueForge + TMG + IALR -> total excluded("e") ($M)
  §9 Coefficient sensitivity ranked column (2x4) appendix coefficient ladder (%)
  §10 Penetration strip     line/strip (4x11)    Outsourced BC / total ship spend, FY22-27 + assumed FY28-31
  §11 Outyear implied BC    stacked column (3x5) implied low + range-to-high, FY28-31 ($M)
  §12 FY22-25 average TAM   reference (2x2)      the pre-OBBBA dashed-line level ($M)

think-cell waterfall convention: every data cell is a STEP, so a computed
subtotal/total is the literal text marker "e" (think-cell draws a calculated bar
from the prior steps; a numeric subtotal would double-count). Values are live links
to producer cells. $B blocks divide the model's $M producers by 1000 to match the
deck chart's displayed magnitude; avg-annual blocks divide a cumulative producer by
the fiscal-year count. AP-bridge removal cells are already signed negative.

Pure consumer (links producers, exports no accessors; deck-loader leaf).
"""
from __future__ import annotations

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
from workbook_submarines.sheets._layout import RowCursor
from workbook_submarines.sheets.model_tam_build import (
    n_years_cell, tam_total_cell, FY_COLUMNS,
    va_bc_supplier_coeff_cell, col_bc_supplier_coeff_cell,
    ap_lltm_supplier_coeff_cell, primary_tam_coeff_cell,
)
from workbook_submarines.sheets.model_sam_build import (
    bucket_tam_cell, avg_annual_sam_cell, annual_broad_sam_cell,
)
from workbook_submarines.sheets.data_scn_budget import scn_cell
from workbook_submarines.sheets.data_ap_bridge import (
    ap_bridge_gross_cell, ap_bridge_gfe_removed_cell,
    ap_bridge_in_bc_removed_cell, ap_bridge_residual_cell,
)
from workbook_submarines.sheets.data_entity_master import ent_row_cell, top_supplier_indices
from workbook_submarines.sheets.validation_sib_excluded import sib_entity_dollar_cell
from workbook_submarines.sheets.model_outlook import (
    penetration_cell, assumption_low_cell, assumption_high_cell,
    outyear_low_cell, outyear_high_cell, tam_fy2225_avg_cell,
)

_GROUP = "chartdata"
_TAB = "z_ChartData"
_NCOLS = 11                      # widest paste block (penetration strip, 1 + 10); banners span this
_OYS = list(range(2028, 2032))

# POP anchor / AP-LLTM reference / applied class BC coefficients (chart order).
_COEFF = [("POP anchor", primary_tam_coeff_cell()),
          ("AP/LLTM ref", ap_lltm_supplier_coeff_cell()),
          ("Applied BC - Va", va_bc_supplier_coeff_cell()),
          ("Applied BC - Col", col_bc_supplier_coeff_cell())]


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


def _render_chart_data() -> WorksheetSpec:
    nyr = n_years_cell()
    fy_hdr = [f"FY{fy}" for fy in FY_COLUMNS]

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 - Basic Construction by FY and class (stacked column matrix), $B.
    _paste_block(c, "§1 - Basic Construction (stacked column)",
                 ["", *fy_hdr],
                 [("Virginia", [f"={scn_cell(2013, fy, 'basic')}/1000" for fy in FY_COLUMNS]),
                  ("Columbia", [f"={scn_cell(1045, fy, 'basic')}/1000" for fy in FY_COLUMNS])],
                 "B")

    # §2 - Annual cadence: TAM vs broad SAM by FY (clustered column matrix), $B.
    _paste_block(c, "§2 - Annual cadence (clustered column)",
                 ["", *fy_hdr],
                 [("TAM", [f"={tam_total_cell(fy)}/1000" for fy in FY_COLUMNS]),
                  ("Broad SAM", [f"={annual_broad_sam_cell(fy)}/1000" for fy in FY_COLUMNS])],
                 "B")

    # §3 - Coefficient evidence (ranked column), %.
    _paste_block(c, "§3 - Coefficient evidence (ranked column)",
                 ["", *[lab for lab, _ in _COEFF]],
                 [("", [f"={ref}" for _, ref in _COEFF])],
                 "P")

    # §4 - AP/LLTM bridge to a $0 additive base (waterfall), $B. Removal cells are
    # already signed negative on the AP Bridge tab, so they link straight through.
    _paste_block(c, "§4 - AP and LLTM bridge (waterfall)",
                 ["", "Gross AP", "GFE design weapons", "Inside BC", "Overlap", "Additive base"],
                 [("", [f"={ap_bridge_gross_cell()}/1000", f"={ap_bridge_gfe_removed_cell()}/1000",
                        f"={ap_bridge_in_bc_removed_cell()}/1000", f"={ap_bridge_residual_cell()}/1000",
                        "e"])],
                 "B")

    # §5 - Work-type (bucket) TAM (ranked column), average annual $M.
    _bk = [("Electrical/power", "electrical"), ("Structural", "structural"),
           ("Piping/valves", "piping"), ("Castings", "castings"), ("Coatings", "coatings"),
           ("Machining", "machining"), ("HVAC", "hvac")]
    _paste_block(c, "§5 - Work-type (bucket) TAM (ranked column)",
                 ["", *[lab for lab, _ in _bk]],
                 [("", [f"={bucket_tam_cell(k)}/{nyr}" for _, k in _bk])],
                 "M")

    # §6 - SAM scenarios (ranked column), average annual SAM $M.
    _sc = [("Broad components", "broad"), ("Electrical/power", "electrical"),
           ("Metal components", "metal"), ("Modular assy", "modular"), ("HM&E", "hme")]
    _paste_block(c, "§6 - SAM scenarios (ranked column)",
                 ["", *[lab for lab, _ in _sc]],
                 [("", [f"={avg_annual_sam_cell(k)}" for _, k in _sc])],
                 "M")

    # §7 - Visible suppliers (horizontal bar): top-10, names down / $ across.
    _sup = top_supplier_indices(10)
    _paste_block(c, "§7 - Visible suppliers (bar)",
                 ["", "Visible subaward $M"],
                 [(f"={ent_row_cell(i, 'vendor')}", [f"={ent_row_cell(i, 'dollar')}"]) for i in _sup],
                 "M")

    # §8 - SIB exclusion (additive waterfall), $M. Three capacity-development
    # pass-throughs build to the total excluded ("e").
    _paste_block(c, "§8 - SIB exclusion (waterfall)",
                 ["", "BlueForge", "TMG", "IALR", "Total excluded"],
                 [("", [f"={sib_entity_dollar_cell(0)}", f"={sib_entity_dollar_cell(1)}",
                        f"={sib_entity_dollar_cell(2)}", "e"])],
                 "M")

    # §9 - Coefficient sensitivity (appendix ranked column), %. Same ladder as §3.
    _paste_block(c, "§9 - Coefficient sensitivity (ranked column)",
                 ["", *[lab for lab, _ in _COEFF]],
                 [("", [f"={ref}" for _, ref in _COEFF])],
                 "P")

    # §10 - Penetration strip: Outsourced BC TAM / total ship spend per FY
    # (Outlook §2), with the FY28-31 assumed range (Outlook §3) in the outyears.
    _strip_hdr = [f"FY{fy}" for fy in FY_COLUMNS] + [f"FY{fy}" for fy in _OYS]
    _paste_block(c, "§10 - Outsourced BC penetration (strip)",
                 ["", *_strip_hdr],
                 [("Actual", [f"={penetration_cell(fy)}" for fy in FY_COLUMNS] + [None] * 4),
                  ("Assumed low", [None] * 6 + [f"={assumption_low_cell()}"] * 4),
                  ("Assumed high", [None] * 6 + [f"={assumption_high_cell()}"] * 4)],
                 "P")

    # §11 - Implied outyear Outsourced BC (Outlook §4): stacked low + range cap.
    _paste_block(c, "§11 - Implied outyear Outsourced BC (stacked column)",
                 ["", *[f"FY{fy}" for fy in _OYS]],
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
