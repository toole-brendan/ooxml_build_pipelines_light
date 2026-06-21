"""validation_sensitivity - the "Sensitivity" tab (DDG, validation group; one module = one sheet).

Coefficient, MYP, and AP/LLTM sensitivity view. A validation tab, not an inputs tab:
editable knobs stay on Inputs; this sheet only LINKS to them (pure assumption links
are green; derived sensitivities are black).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg.model_tam_build import (
    bc_supplier_coeff_cell as _bc, bc_supplier_coeff_disclosed_cell as _bc_disc,
    outside_yards_corrected_cell as _corr, outside_yards_disclosed_cell as _disc,
    portfolio_tam_cell as _tam, portfolio_bc_tam_cell as _bc_tam,
    portfolio_ap_tam_cell as _ap_tam,
)
from workbook_master_tam.sheets.ddg.inputs_assumptions import (
    ap_supplier_coeff_cell as _ap_co,
    obbba_bc_share_cell as _obbba_share,
)
from workbook_master_tam.sheets.ddg.data_obbba_funding import (
    obbba_gross_cell as _obbba_gross, obbba_bc_base_cell as _obbba_bc,
)
from workbook_master_tam.sheets.ddg.validation_pop_source_audit import masters_dollar_cell, gated_dollar_cell
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "validation"
_TAB = "DDG Sensitivity"
_NCOLS = 2
_Q = '"'


def _make_sensitivity():
    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
        c.blank()

        # §1 Coefficient ladder
        c.banner("§1 - Coefficient ladder (BC coeff vs all-gated outside-yards POP)", n_cols=_NCOLS,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Coefficient", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
        c.write(["BC supplier coeff (applied, MYP-corrected)", f"={_bc()}"],
                styles=[S_BOLD, S_LINK_PCT], outline_level=1)
        r_corr = c.write(["Outside-yards POP, MYP-corrected", f"={_corr()}"],
                         styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
        r_disc = c.write(["Outside-yards POP, disclosed (artifact)", f"={_disc()}"],
                         styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
        c.blank(2)

        # §2 MYP swing
        c.banner("§2 - MYP swing", n_cols=_NCOLS,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
        c.write(["Outside-yards swing (disclosed - corrected)", f"=C{r_disc}-C{r_corr}"],
                styles=[S_BOLD, S_PCT], outline_level=1)
        r_masters = c.write(["MYP masters $M (reconstructed)", f"={masters_dollar_cell()}"],
                            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
        c.write(["Masters as % of gated corpus $", f"=C{r_masters}/{gated_dollar_cell()}"],
                styles=[S_DEFAULT, S_PCT], outline_level=1)
        c.blank(2)

        # §3 TAM sensitivity
        c.banner("§3 - TAM sensitivity (MYP adjustment effect: corrected vs disclosed-only coeff)",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Measure", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
        r_tam = c.write(["Portfolio TAM (applied, MYP-corrected)", f"={_tam()}"],
                        styles=[S_BOLD, S_LINK_NUM], outline_level=1)
        r_disc_tam = c.write(["Portfolio TAM (disclosed-only BC coeff)", f"=C{r_tam}*({_bc_disc()}/{_bc()})"],
                             styles=[S_DEFAULT, S_NUM], outline_level=1)
        r_uplift = c.write(["MYP adjustment uplift on TAM", f"=C{r_tam}-C{r_disc_tam}"],
                           styles=[S_BOLD, S_NUM], outline_level=1)
        c.write(["Memo: masters' embedded content @ 42% band", f"={masters_dollar_cell()}*0.42"],
                styles=[S_DEFAULT, S_NUM], outline_level=1)
        c.blank(2)

        # §4 AP/LLTM knobs
        c.banner("§4 - AP/LLTM stream", n_cols=_NCOLS,
                 style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
        c.write(["AP/LLTM supplier coefficient (P-10 EOQ basis)", f"={_ap_co()}"],
                styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
        c.write(["AP/LLTM stream TAM ($M)", f"={_ap_tam()}"],
                styles=[S_BOLD, S_LINK_NUM], outline_level=1)
        c.write(["Stream TAM at 85% coefficient haircut ($M)", f"=N({_ap_tam()})*0.85"],
                styles=[S_DEFAULT, S_NUM], outline_level=1)
        c.write(["Stream TAM at 70% coefficient haircut ($M)", f"=N({_ap_tam()})*0.70"],
                styles=[S_DEFAULT, S_NUM], outline_level=1)
        c.write(["AP/LLTM share of portfolio TAM", f"=N({_ap_tam()})/({_bc_tam()}+N({_ap_tam()}))"],
                styles=[S_DEFAULT, S_PCT], outline_level=1)
        c.blank(2)

        # §5 OBBBA BC-share sensitivity (the Sec. 20002(17) award has no BC/GFE
        # breakout; the applied share is the assumption under test)
        c.banner("§5 - OBBBA BC-share sensitivity (Sec. 20002(17) BC/GFE split)",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
        r_gross = c.write(["OBBBA gross award FY2026 ($M)", f"={_obbba_gross(2122, 2026)}"],
                          styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
        c.write(["Applied BC share (Assumptions knob)", f"={_obbba_share()}"],
                styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
        r_up = c.write(["OBBBA TAM uplift @ applied share ($M)",
                        f"=N({_obbba_bc(2122, 2026)})*N({_bc()})"],
                       styles=[S_BOLD, S_NUM], outline_level=1)
        r_lo = c.write(["OBBBA TAM uplift @ 55% BC share ($M)", f"=C{r_gross}*0.55*N({_bc()})"],
                       styles=[S_DEFAULT, S_NUM], outline_level=1)
        r_hi = c.write(["OBBBA TAM uplift @ 70% BC share ($M)", f"=C{r_gross}*0.70*N({_bc()})"],
                       styles=[S_DEFAULT, S_NUM], outline_level=1)
        c.write(["Uplift band width (70% - 55%) ($M)", f"=C{r_hi}-C{r_lo}"],
                styles=[S_DEFAULT, S_NUM], outline_level=1)
        c.write(["Uplift as % of portfolio TAM", f"=C{r_up}/N({_tam()})"],
                styles=[S_DEFAULT, S_PCT], outline_level=1)

        ws = worksheet(c.rows, cols=[44, 14],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


SENSITIVITY = _make_sensitivity()
