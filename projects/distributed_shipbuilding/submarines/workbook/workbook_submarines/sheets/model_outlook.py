"""model_outlook - the "Outlook" tab (submarines, model group; one module = one sheet).

Outsourced BC penetration and the FY2028-FY2031 outyear outlook, per class
(Virginia, Columbia) with the portfolio as the sum. Penetration is the
supplier-addressable share of each year's total ship spend: Outsourced BC TAM
(all streams; the toggled OBBBA stream rides Virginia) / (P-5c Total Ship
Estimate + OBBBA gross award), constant FY2026 $. Window averages are ratios of
sums, not means of annual ratios. Implied outyear Outsourced BC = each class's
PB2027 FYDP gross (FYDP Outyears tab) x that class's penetration assumption:
low = the class FY22-25 average (complete historical years), high = low x
(1 + the Assumptions §9 outsourcing-intent uplift, default 30%, stated industry
intent). Portfolio implied = Virginia + Columbia; the portfolio "effective
blended assumption" rows divide portfolio implied by portfolio FYDP gross.

The OBBBA gross enters the Virginia denominator then-year x deflator, split
FY26/FY27 by the same execution-spillover control the BC base uses, and gated by
the same include-toggle - the A/B (Assumptions §2) moves numerator and
denominator together.

Promoted accessors:
  penetration_cell(fy), va_penetration_cell(fy), col_penetration_cell(fy),
  penetration_l6y_cell(), penetration_fy2225_cell(), penetration_fy2627_cell(),
  total_spend_cell(fy), va_total_spend_cell(fy), col_total_spend_cell(fy),
  assumption_low_cell(), assumption_high_cell(),
  va_assumption_low_cell(), va_assumption_high_cell(),
  col_assumption_low_cell(), col_assumption_high_cell(),
  outyear_gross_cell(fy), outyear_low_cell(fy), outyear_high_cell(fy),
  va_outyear_low_cell(fy), va_outyear_high_cell(fy),
  col_outyear_low_cell(fy), col_outyear_high_cell(fy),
  outyear_low_avg_cell(), outyear_high_avg_cell(), tam_fy2225_avg_cell(),
  va_tam_fy2225_avg_cell(), col_tam_fy2225_avg_cell()
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.sheets.model_tam_build import tam_cell, tam_total_cell
from workbook_submarines.sheets.data_scn_budget import scn_cell
from workbook_submarines.sheets.data_obbba_funding import obbba_gross_cell
from workbook_submarines.sheets.data_fydp_outyears import (
    fydp_gross_cell, fydp_gross_then_cell, fydp_portfolio_gross_cell,
)
from workbook_submarines.sheets.data_deflators import deflator_factor_cell
from workbook_submarines.sheets.inputs_assumptions import (
    include_obbba_stream_cell, obbba_spillover_cell, outlook_intent_uplift_cell,
)
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "model"
_TAB = "Outlook"
_FY = [2022, 2023, 2024, 2025, 2026, 2027]
_OY = [2028, 2029, 2030, 2031]
_FY_COL = {fy: col_letter(2 + i) for i, fy in enumerate(_FY)}     # C..H
_OY_COL = {fy: col_letter(2 + i) for i, fy in enumerate(_OY)}     # C..F
_NCOLS = 1 + len(_FY)
_BASE = 14   # title(2) + blank + §1 banner + blank + header + 5 rows + 2 blanks


def _obbba_gross_formula(fy: int) -> object:
    """OBBBA gross in the spend denominator: then-year award x deflator, split
    FY26/FY27 by the execution-spillover control, gated by the include-toggle."""
    if fy not in (2026, 2027):
        return 0
    g = f"(N({obbba_gross_cell(2013, 2026)})+N({obbba_gross_cell(1045, 2026)}))"
    spill = obbba_spillover_cell()
    share = f"(1-{spill})" if fy == 2026 else spill
    return (f"={g}*{share}*{deflator_factor_cell(fy)}"
            f"*{include_obbba_stream_cell()}")


def _build_body(tab: str, base: int):
    P: dict = {}
    c = RowCursor(base)

    # §2 Penetration by FY (constant FY2026 $, per class + portfolio)
    c.banner("§2 - Outsourced BC penetration by FY (constant FY2026 $, per class)", _NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY))
    P["tam_va"] = c.write(
        ["Virginia Outsourced BC TAM incl. OBBBA stream ($M)"]
        + [f"=N({tam_cell(2013, fy)})" for fy in _FY],
        styles=[S_DEFAULT] + [S_LINK_NUM] * len(_FY), outline_level=1)
    P["tam_col"] = c.write(
        ["Columbia Outsourced BC TAM ($M)"]
        + [f"=N({tam_cell(1045, fy)})" for fy in _FY],
        styles=[S_DEFAULT] + [S_LINK_NUM] * len(_FY), outline_level=1)
    P["pen_num"] = c.write(
        ["Outsourced BC TAM, all streams (portfolio $M)"]
        + [f"=N({tam_total_cell(fy)})" for fy in _FY],
        styles=[S_BOLD] + [S_LINK_NUM] * len(_FY), outline_level=1)
    P["den_va"] = c.write(
        ["Virginia P-5c Total Ship Estimate ($M)"]
        + [f"={scn_cell(2013, fy, 'total')}" for fy in _FY],
        styles=[S_DEFAULT] + [S_LINK_NUM] * len(_FY), outline_level=1)
    P["den_obbba"] = c.write(
        ["plus OBBBA gross award ($M; rides Virginia, toggle-gated, FY27 via spillover)"]
        + [_obbba_gross_formula(fy) for fy in _FY],
        styles=[S_DEFAULT] + [S_LINK_NUM if fy in (2026, 2027) else S_NUM for fy in _FY],
        outline_level=1)
    P["den_va_tot"] = c.write(
        ["Virginia total spend incl. OBBBA ($M)"]
        + [f"={_FY_COL[fy]}{P['den_va']}+N({_FY_COL[fy]}{P['den_obbba']})" for fy in _FY],
        styles=[S_BOLD] + [S_NUM] * len(_FY), outline_level=1)
    P["den_col"] = c.write(
        ["Columbia total spend: P-5c Total Ship Estimate ($M)"]
        + [f"={scn_cell(1045, fy, 'total')}" for fy in _FY],
        styles=[S_BOLD] + [S_LINK_NUM] * len(_FY), outline_level=1)
    P["den"] = c.total(
        ["Total ship spend incl. OBBBA (portfolio $M)"]
        + [f"={_FY_COL[fy]}{P['den_va_tot']}+{_FY_COL[fy]}{P['den_col']}" for fy in _FY],
        styles=[S_BOLD] + [S_NUM] * len(_FY), n_cols=_NCOLS)
    P["pen_va"] = c.write(
        ["Virginia penetration: TAM / total spend"]
        + [f'=IF({_FY_COL[fy]}{P["den_va_tot"]}=0,"",{_FY_COL[fy]}{P["tam_va"]}/{_FY_COL[fy]}{P["den_va_tot"]})'
           for fy in _FY],
        styles=[S_DEFAULT] + [S_PCT] * len(_FY), outline_level=1)
    P["pen_col"] = c.write(
        ["Columbia penetration: TAM / total spend"]
        + [f'=IF({_FY_COL[fy]}{P["den_col"]}=0,"",{_FY_COL[fy]}{P["tam_col"]}/{_FY_COL[fy]}{P["den_col"]})'
           for fy in _FY],
        styles=[S_DEFAULT] + [S_PCT] * len(_FY), outline_level=1)
    P["pen"] = c.write(
        ["Portfolio penetration: TAM / total ship spend"]
        + [f'=IF({_FY_COL[fy]}{P["den"]}=0,"",{_FY_COL[fy]}{P["pen_num"]}/{_FY_COL[fy]}{P["den"]})'
           for fy in _FY],
        styles=[S_BOLD] + [S_PCT] * len(_FY), outline_level=1)
    c.blank(2)

    # §3 Window-average penetration + the per-class outyear assumptions
    c.banner("§3 - Window-average penetration (ratio of sums) + outyear assumptions", _NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["pen_2225_va"] = c.write(
        ["Virginia FY22-25 average (sum TAM / sum spend; complete historical years)",
         f"=SUM(C{P['tam_va']}:F{P['tam_va']})/SUM(C{P['den_va_tot']}:F{P['den_va_tot']})"],
        styles=[S_BOLD, S_PCT], outline_level=1)
    P["pen_2225_col"] = c.write(
        ["Columbia FY22-25 average (sum TAM / sum spend; complete historical years)",
         f"=SUM(C{P['tam_col']}:F{P['tam_col']})/SUM(C{P['den_col']}:F{P['den_col']})"],
        styles=[S_BOLD, S_PCT], outline_level=1)
    P["pen_2225"] = c.write(
        ["Portfolio FY22-25 average (sum TAM / sum spend; memo)",
         f"=SUM(C{P['pen_num']}:F{P['pen_num']})/SUM(C{P['den']}:F{P['den']})"],
        styles=[S_DEFAULT, S_PCT], outline_level=1)
    P["pen_l6y"] = c.write(
        ["Portfolio FY22-27 average (sum TAM / sum spend; memo)",
         f"=SUM(C{P['pen_num']}:H{P['pen_num']})/SUM(C{P['den']}:H{P['den']})"],
        styles=[S_DEFAULT, S_PCT], outline_level=1)
    P["pen_2627"] = c.write(
        ["Portfolio FY26-27 average (sum TAM / sum spend; memo)",
         f"=SUM(G{P['pen_num']}:H{P['pen_num']})/SUM(G{P['den']}:H{P['den']})"],
        styles=[S_DEFAULT, S_PCT], outline_level=1)
    P["uplift"] = c.write(
        ["Outsourcing intent uplift (Assumptions §9)", f"={outlook_intent_uplift_cell()}"],
        styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
    P["assum_lo_va"] = c.write(
        ["Virginia assumption, low (= class FY22-25 average)", f"=C{P['pen_2225_va']}"],
        styles=[S_BOLD, S_PCT], outline_level=1)
    P["assum_hi_va"] = c.write(
        ["Virginia assumption, high (= low x (1 + intent uplift))",
         f"=C{P['assum_lo_va']}*(1+C{P['uplift']})"],
        styles=[S_BOLD, S_PCT], outline_level=1)
    P["assum_lo_col"] = c.write(
        ["Columbia assumption, low (= class FY22-25 average)", f"=C{P['pen_2225_col']}"],
        styles=[S_BOLD, S_PCT], outline_level=1)
    P["assum_hi_col"] = c.write(
        ["Columbia assumption, high (= low x (1 + intent uplift))",
         f"=C{P['assum_lo_col']}*(1+C{P['uplift']})"],
        styles=[S_BOLD, S_PCT], outline_level=1)
    c.write(["Window average = sum of TAM / sum of spend over the window, not the mean of annual ratios."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 Implied outyear Outsourced BC (FY2028-FY2031, per class -> portfolio)
    c.banner("§4 - Implied outyear Outsourced BC (FY2028-FY2031, per class)", _NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_OY),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_OY))
    P["oy_gross_va"] = c.write(
        ["Virginia FYDP gross, constant FY2026 $M"]
        + [f"={fydp_gross_cell(2013, fy)}" for fy in _OY],
        styles=[S_DEFAULT] + [S_LINK_NUM] * len(_OY), outline_level=1)
    P["oy_gross_col"] = c.write(
        ["Columbia FYDP gross, constant FY2026 $M"]
        + [f"={fydp_gross_cell(1045, fy)}" for fy in _OY],
        styles=[S_DEFAULT] + [S_LINK_NUM] * len(_OY), outline_level=1)
    P["oy_gross"] = c.write(
        ["Portfolio FYDP gross (PB2027 request), constant FY2026 $M"]
        + [f"={fydp_portfolio_gross_cell(fy)}" for fy in _OY],
        styles=[S_BOLD] + [S_LINK_NUM] * len(_OY), outline_level=1)
    P["oy_lo_va"] = c.write(
        ["Virginia implied Outsourced BC, low ($M)"]
        + [f"={_OY_COL[fy]}{P['oy_gross_va']}*$C${P['assum_lo_va']}" for fy in _OY],
        styles=[S_DEFAULT] + [S_NUM] * len(_OY), outline_level=1)
    P["oy_hi_va"] = c.write(
        ["Virginia implied Outsourced BC, high ($M)"]
        + [f"={_OY_COL[fy]}{P['oy_gross_va']}*$C${P['assum_hi_va']}" for fy in _OY],
        styles=[S_DEFAULT] + [S_NUM] * len(_OY), outline_level=1)
    P["oy_lo_col"] = c.write(
        ["Columbia implied Outsourced BC, low ($M)"]
        + [f"={_OY_COL[fy]}{P['oy_gross_col']}*$C${P['assum_lo_col']}" for fy in _OY],
        styles=[S_DEFAULT] + [S_NUM] * len(_OY), outline_level=1)
    P["oy_hi_col"] = c.write(
        ["Columbia implied Outsourced BC, high ($M)"]
        + [f"={_OY_COL[fy]}{P['oy_gross_col']}*$C${P['assum_hi_col']}" for fy in _OY],
        styles=[S_DEFAULT] + [S_NUM] * len(_OY), outline_level=1)
    P["oy_lo"] = c.write(
        ["Portfolio implied Outsourced BC, low ($M)"]
        + [f"={_OY_COL[fy]}{P['oy_lo_va']}+{_OY_COL[fy]}{P['oy_lo_col']}" for fy in _OY],
        styles=[S_BOLD] + [S_NUM] * len(_OY), outline_level=1)
    P["oy_hi"] = c.write(
        ["Portfolio implied Outsourced BC, high ($M)"]
        + [f"={_OY_COL[fy]}{P['oy_hi_va']}+{_OY_COL[fy]}{P['oy_hi_col']}" for fy in _OY],
        styles=[S_BOLD] + [S_NUM] * len(_OY), outline_level=1)
    c.write(["Range, high - low ($M)"]
            + [f"={_OY_COL[fy]}{P['oy_hi']}-{_OY_COL[fy]}{P['oy_lo']}" for fy in _OY],
            styles=[S_DEFAULT] + [S_NUM] * len(_OY), outline_level=1)
    c.blank()
    P["oy_lo_avg"] = c.write(
        ["Portfolio implied low, FY28-31 average ($M/yr)", f"=SUM(C{P['oy_lo']}:F{P['oy_lo']})/4"],
        styles=[S_DEFAULT, S_NUM], outline_level=1)
    P["oy_hi_avg"] = c.write(
        ["Portfolio implied high, FY28-31 average ($M/yr)", f"=SUM(C{P['oy_hi']}:F{P['oy_hi']})/4"],
        styles=[S_DEFAULT, S_NUM], outline_level=1)
    P["assum_lo"] = c.write(
        ["Effective blended assumption, low (portfolio implied / FYDP gross)",
         f"=SUM(C{P['oy_lo']}:F{P['oy_lo']})/SUM(C{P['oy_gross']}:F{P['oy_gross']})"],
        styles=[S_DEFAULT, S_PCT], outline_level=1)
    P["assum_hi"] = c.write(
        ["Effective blended assumption, high (portfolio implied / FYDP gross)",
         f"=SUM(C{P['oy_hi']}:F{P['oy_hi']})/SUM(C{P['oy_gross']}:F{P['oy_gross']})"],
        styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.blank(2)

    # §5 FY22-25 average annual TAM (the pre-OBBBA reference line)
    c.banner("§5 - FY22-25 average annual TAM", _NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    _t = [f"N({tam_total_cell(fy)})" for fy in (2022, 2023, 2024, 2025)]
    P["tam_2225_avg"] = c.write(
        ["Average annual TAM, FY22-25 (portfolio $M/yr)", f"=({'+'.join(_t)})/4"],
        styles=[S_BOLD, S_NUM], outline_level=1)
    P["tam_2225_avg_va"] = c.write(
        ["Virginia average annual TAM, FY22-25 ($M/yr)",
         f"=SUM(C{P['tam_va']}:F{P['tam_va']})/4"],
        styles=[S_DEFAULT, S_NUM], outline_level=1)
    P["tam_2225_avg_col"] = c.write(
        ["Columbia average annual TAM, FY22-25 ($M/yr)",
         f"=SUM(C{P['tam_col']}:F{P['tam_col']})/4"],
        styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.blank(2)

    # §6 Checks
    c.banner("§6 - Checks", _NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Status"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    c.write(["Virginia FY27 FYDP gross ties to SCN Budget FY27 TSE (constant)",
             f'=IF(ABS(N({fydp_gross_cell(2013, 2027)})-N({scn_cell(2013, 2027, "total")}))<1,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Columbia FY27 FYDP gross ties to SCN Budget FY27 TSE (constant)",
             f'=IF(ABS(N({fydp_gross_cell(1045, 2027)})-N({scn_cell(1045, 2027, "total")}))<1,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Virginia FY26 FYDP gross ties to PB2027 ($5,389.1M, one boat)",
             f'=IF(ABS(N({fydp_gross_then_cell(2013, 2026)})-5389.109)<1,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Va + Col class TAM sums to portfolio TAM each FY",
             f'=IF(SUMPRODUCT(ABS(C{P["tam_va"]}:H{P["tam_va"]}+C{P["tam_col"]}:H{P["tam_col"]}'
             f'-C{P["pen_num"]}:H{P["pen_num"]}))<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Penetration at or below 100% each FY (portfolio)",
             f'=IF(COUNTIF(C{P["pen"]}:H{P["pen"]},">1")=0,"OK","REVIEW")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Class penetration at or below 100% each FY",
             f'=IF(COUNTIF(C{P["pen_va"]}:H{P["pen_va"]},">1")'
             f'+COUNTIF(C{P["pen_col"]}:H{P["pen_col"]},">1")=0,"OK","REVIEW")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Low assumption at or below high (each class)",
             f'=IF(AND(C{P["assum_lo_va"]}<=C{P["assum_hi_va"]},'
             f'C{P["assum_lo_col"]}<=C{P["assum_hi_col"]}),"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    return c.rows, c.at(), P


# ── Layout pass: body first (backs the accessors) ───────────────────────────
_rows, _after, _P = _build_body(_TAB, _BASE)


def _check_fy(fy: int, grid: dict) -> None:
    if fy not in grid:
        raise ValueError(f"FY {fy!r} outside {sorted(grid)!r}")


def penetration_cell(fy: int) -> str:
    _check_fy(fy, _FY_COL)
    return f"'{_TAB}'!{_FY_COL[fy]}{_P['pen']}"


def va_penetration_cell(fy: int) -> str:
    _check_fy(fy, _FY_COL)
    return f"'{_TAB}'!{_FY_COL[fy]}{_P['pen_va']}"


def col_penetration_cell(fy: int) -> str:
    _check_fy(fy, _FY_COL)
    return f"'{_TAB}'!{_FY_COL[fy]}{_P['pen_col']}"


def penetration_l6y_cell() -> str:
    return f"'{_TAB}'!C{_P['pen_l6y']}"


def penetration_fy2225_cell() -> str:
    return f"'{_TAB}'!C{_P['pen_2225']}"


def penetration_fy2627_cell() -> str:
    return f"'{_TAB}'!C{_P['pen_2627']}"


def total_spend_cell(fy: int) -> str:
    """Per-FY portfolio penetration denominator: TSE + OBBBA gross, constant FY2026 $M."""
    _check_fy(fy, _FY_COL)
    return f"'{_TAB}'!{_FY_COL[fy]}{_P['den']}"


def va_total_spend_cell(fy: int) -> str:
    _check_fy(fy, _FY_COL)
    return f"'{_TAB}'!{_FY_COL[fy]}{_P['den_va_tot']}"


def col_total_spend_cell(fy: int) -> str:
    _check_fy(fy, _FY_COL)
    return f"'{_TAB}'!{_FY_COL[fy]}{_P['den_col']}"


def assumption_low_cell() -> str:
    return f"'{_TAB}'!C{_P['assum_lo']}"


def assumption_high_cell() -> str:
    return f"'{_TAB}'!C{_P['assum_hi']}"


def va_assumption_low_cell() -> str:
    return f"'{_TAB}'!C{_P['assum_lo_va']}"


def va_assumption_high_cell() -> str:
    return f"'{_TAB}'!C{_P['assum_hi_va']}"


def col_assumption_low_cell() -> str:
    return f"'{_TAB}'!C{_P['assum_lo_col']}"


def col_assumption_high_cell() -> str:
    return f"'{_TAB}'!C{_P['assum_hi_col']}"


def outyear_gross_cell(fy: int) -> str:
    _check_fy(fy, _OY_COL)
    return f"'{_TAB}'!{_OY_COL[fy]}{_P['oy_gross']}"


def outyear_low_cell(fy: int) -> str:
    _check_fy(fy, _OY_COL)
    return f"'{_TAB}'!{_OY_COL[fy]}{_P['oy_lo']}"


def outyear_high_cell(fy: int) -> str:
    _check_fy(fy, _OY_COL)
    return f"'{_TAB}'!{_OY_COL[fy]}{_P['oy_hi']}"


def va_outyear_low_cell(fy: int) -> str:
    _check_fy(fy, _OY_COL)
    return f"'{_TAB}'!{_OY_COL[fy]}{_P['oy_lo_va']}"


def va_outyear_high_cell(fy: int) -> str:
    _check_fy(fy, _OY_COL)
    return f"'{_TAB}'!{_OY_COL[fy]}{_P['oy_hi_va']}"


def col_outyear_low_cell(fy: int) -> str:
    _check_fy(fy, _OY_COL)
    return f"'{_TAB}'!{_OY_COL[fy]}{_P['oy_lo_col']}"


def col_outyear_high_cell(fy: int) -> str:
    _check_fy(fy, _OY_COL)
    return f"'{_TAB}'!{_OY_COL[fy]}{_P['oy_hi_col']}"


def outyear_low_avg_cell() -> str:
    return f"'{_TAB}'!C{_P['oy_lo_avg']}"


def outyear_high_avg_cell() -> str:
    return f"'{_TAB}'!C{_P['oy_hi_avg']}"


def tam_fy2225_avg_cell() -> str:
    return f"'{_TAB}'!C{_P['tam_2225_avg']}"


def va_tam_fy2225_avg_cell() -> str:
    return f"'{_TAB}'!C{_P['tam_2225_avg_va']}"


def col_tam_fy2225_avg_cell() -> str:
    return f"'{_TAB}'!C{_P['tam_2225_avg_col']}"


def _render_outlook() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(_TAB, _NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Penetration & outyear outlook", _NCOLS, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Virginia outsourced penetration, FY22-25 (outyear low)", f"=C{_P['pen_2225_va']}"],
            styles=[S_BOLD, S_PCT])
    c.write(["Columbia outsourced penetration, FY22-25 (outyear low)", f"=C{_P['pen_2225_col']}"],
            styles=[S_BOLD, S_PCT])
    c.write(["Implied outyear Outsourced BC, low $M/yr", f"=C{_P['oy_lo_avg']}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Implied outyear Outsourced BC, high $M/yr", f"=C{_P['oy_hi_avg']}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["FY22-25 average annual TAM $M/yr", f"=C{_P['tam_2225_avg']}"],
            styles=[S_DEFAULT, S_NUM])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)

    ws = worksheet(c.rows, cols=[46, 13, 13, 13, 13, 13, 13],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


OUTLOOK = SheetEntry(_TAB, _GROUP, _render_outlook)
