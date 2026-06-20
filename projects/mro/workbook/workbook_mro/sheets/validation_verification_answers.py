"""Verification Answers

INTENT
    Headline TAM/SAM figures and deck-cited values (plan items 6.1-6.6), every $/% cell
    a live SUMIFS or accessor pull. The 65-PSC TAM denominator (Navy+CG) and the
    top-down anchors come from the Services / OP-5 / MSC-SCN-USCG accessors; the ranked
    PSC / office tables and the PSC 1905 captive block are live SUMIFS over the Awards /
    PSC1905Classified tables. A scaled pull (accessor/1000) is derived black S_NUM; only
    a bare =accessor() link is green.

LAYOUT
    row 2 : title
    B..D  : Item, $M, %
    §1 Navy vs USCG share · §2 top-15 PSCs · §3 top-10 offices · §4 USCG OP-5 equivalent
    · §5 OP-5 private vs FPDS RMC · §6 PSC 1905 captive share
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_LABEL_INDENT_1,
    S_NUM, S_LINK_NUM, S_PCT, S_PCT_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets._crosstab import sumifs_award, sumifs_psc1905
from workbook_mro.sheets.model_op5_navy_topdown import op5_private_cell
from workbook_mro.sheets.model_msc_scn_uscg_topdown import uscg_isvs_floor_cell
from workbook_mro.sheets.model_services import navy_tam_svc_cell, cg_tam_svc_cell

_GROUP = "validation"
_TAB = "Verification Answers"
_NCOLS = 3                      # B..D
_COLS = [42, 14, 10]
_HEADERS = ["Item", "$M", "%"]
_HSTYLE = [S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER]

# 65-PSC MRO TAM denominator (Navy + CG, $M) - the share base for §1/§2/§3.
def _tam():
    return f"({navy_tam_svc_cell()}+{cg_tam_svc_cell()})"


def _mro_psc(psc):
    return f'{sumifs_award("FY2025 Obligation", ("Is MRO", "Y"), ("PSC", psc))}/1000000'


def _mro_office(office):
    return f'{sumifs_award("FY2025 Obligation", ("Is MRO", "Y"), ("Canonical Office", office))}/1000000'


def _mro_offices(offices):
    return "+".join(_mro_office(o) for o in offices)


# §2 - top 15 PSCs by FY25 $ (label exactly as v4.33, including the truncated names).
_TOP15_PSC = [
    ("# 1  J999  Non-Nuclear Ship Repair (West)", "J999"),
    ("# 2  J998  Non-Nuclear Ship Repair (East)", "J998"),
    ("# 3  J059  Maint/Repair - Electrical/Electronic Equ", "J059"),
    ("# 4  J019  Maint/Repair - Ships, Small Craft, Ponto", "J019"),
    ("# 5  J014  Maint/Repair - Guided Missiles", "J014"),
    ("# 6  K058  Modification - Comm/Detection Equipment", "K058"),
    ("# 7  J020  Maint/Repair - Ship and Marine Equipment", "J020"),
    ("# 8  M2CA  Husbanding - Management/Integration Serv", "M2CA"),
    ("# 9  J036  Maint/Repair - Special Industry Machiner", "J036"),
    ("#10  K012  Modification - Fire Control Equipment", "K012"),
    ("#11  K010  Modification - Weapons", "K010"),
    ("#12  N020  Installation - Ship and Marine Equipment", "N020"),
    ("#13  J063  Maint/Repair - Alarm/Signal/Security", "J063"),
    ("#14  N019  Installation - Ships, Small Craft, Ponto", "N019"),
    ("#15  J058  Maint/Repair - Comm/Detection Equipment", "J058"),
]

# §3 - top 10 contracting offices (canonical-alias rollup).
_TOP10_OFFICE = [
    ("# 1  SWRMC", "SWRMC"),
    ("# 2  MARMC", "MARMC"),
    ("# 3  NAVSUP FLC", "NAVSUP FLC"),
    ("# 4  NAVSEA HQ", "NAVSEA HQ"),
    ("# 5  MSC HQ", "MSC HQ"),
    ("# 6  NW RMC / Puget Sound", "NW RMC / Puget Sound"),
    ("# 7  NIWC Atlantic", "NIWC Atlantic"),
    ("# 8  Strategic Systems Programs", "Strategic Systems Programs"),
    ("# 9  NIWC Pacific", "NIWC Pacific"),
    ("#10  NAVAL AIR WARFARE CENTER AIR DIV", "NAVAL AIR WARFARE CENTER AIR DIV"),
]
# §3 subtotal: 5 RMCs + NAVSEA HQ + USCG SFLC (the >=70% concentration test).
_CONC_OFFICES = ["NAVSEA HQ", "SWRMC", "MARMC", "NW RMC / Puget Sound", "SERMC",
                 "USCG SFLC", "Pearl Harbor RMC"]
# §5 critical test: OP-5 private vs the 7 canonical RMC / FDNF buyers.
_RMC_OFFICES = ["SWRMC", "MARMC", "SERMC", "NW RMC / Puget Sound", "Pearl Harbor RMC",
                "SRF-JRMC Yokosuka", "FDRMC Naples"]


def _make():
    P: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    def _qa_header():
        c.write(_HEADERS, styles=_HSTYLE, outline_level=1)

    def _section(text):
        c.blank(2)
        c.banner(text, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()

    def _pct(denom):
        return lambda r: f"=C{r}/{denom}"

    # §1 Navy vs USCG share of FY25 MRO TAM
    c.banner("§1 - Navy vs USCG share of FY25 MRO TAM", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _qa_header()
    c.write(["Navy MRO FY25", f"={navy_tam_svc_cell()}", _pct(_tam())],
            styles=[S_DEFAULT, S_LINK_NUM, S_PCT], outline_level=1)
    c.write(["USCG MRO FY25", f"={cg_tam_svc_cell()}", _pct(_tam())],
            styles=[S_DEFAULT, S_LINK_NUM, S_PCT], outline_level=1)
    c.total(["TOTAL MRO (65 PSCs)", f"={navy_tam_svc_cell()}+{cg_tam_svc_cell()}", 1],
            styles=[S_BOLD, S_NUM, S_PCT_INPUT], n_cols=_NCOLS)

    # §2 Top 15 PSCs by FY25 $ (MRO universe)
    _section("§2 - Top 15 PSCs by FY25 $ (MRO universe)")
    _qa_header()
    psc_rows = {}
    for label, psc in _TOP15_PSC:
        r = c.write([label, f"={_mro_psc(psc)}", _pct(_tam())],
                    styles=[S_DEFAULT, S_NUM, S_PCT],
                    outline_level=1)
        psc_rows[psc] = r
    c.total(["Top 15 PSC subtotal",
             "=" + "+".join(f"C{psc_rows[p]}" for _l, p in _TOP15_PSC),
             _pct(_tam())],
            styles=[S_BOLD, S_NUM, S_PCT], n_cols=_NCOLS,
            outline_level=1)
    c.total(["Depot (J998 + J999) subtotal",
             f"=C{psc_rows['J999']}+C{psc_rows['J998']}", _pct(_tam())],
            styles=[S_BOLD, S_NUM, S_PCT], n_cols=_NCOLS, outline_level=1)
    c.total(["Grand total (all 65 MRO PSCs)",
             f"={navy_tam_svc_cell()}+{cg_tam_svc_cell()}", None],
            styles=[S_BOLD, S_NUM, S_DEFAULT], n_cols=_NCOLS,
            outline_level=1)

    # §3 Top 10 contracting offices (canonical-alias rollup)
    _section("§3 - Top 10 contracting offices (canonical-alias rollup)")
    _qa_header()
    for label, office in _TOP10_OFFICE:
        c.write([label, f"={_mro_office(office)}", _pct(_tam())],
                styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)
    c.total(["5 RMCs + NAVSEA HQ + SFLC subtotal", f"={_mro_offices(_CONC_OFFICES)}",
             _pct(_tam())],
            styles=[S_BOLD, S_NUM, S_PCT], n_cols=_NCOLS,
            outline_level=1)

    # §4 USCG OP-5 Table IV equivalent?
    _section("§4 - USCG OP-5 Table IV equivalent?")
    _qa_header()
    c.write(["Verdict", "NO", None],
            styles=[S_DEFAULT, S_BOLD, S_DEFAULT], outline_level=1)
    c.write(["USCG ISVS floor (from MSC SCN USCG Top-Down)",
             f"={uscg_isvs_floor_cell()}/1000", None],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT], outline_level=1)

    # §5 OP-5 private side vs FPDS RMC-aggregated
    _section("§5 - OP-5 private side vs FPDS RMC-aggregated")
    _qa_header()
    P["op5_priv"] = c.write(
        ["Top-down: OP-5 private side (FY25 Current)", f"={op5_private_cell()}/1000",
         None],
        styles=[S_DEFAULT, S_NUM, S_DEFAULT], outline_level=1)
    P["fpds_rmc"] = c.write(
        ["Bottom-up: FPDS RMC-aggregated private-yard", f"={_mro_offices(_RMC_OFFICES)}",
         None],
        styles=[S_DEFAULT, S_NUM, S_DEFAULT], outline_level=1)
    _op5, _fpds = P["op5_priv"], P["fpds_rmc"]
    c.total(["Gap (top-down minus bottom-up)", f"=C{_op5}-C{_fpds}",
             f"=(C{_op5}-C{_fpds})/C{_op5}"],
            styles=[S_BOLD, S_NUM, S_PCT], n_cols=_NCOLS,
            outline_level=1)

    # §6 PSC 1905 captive share (HII / GDEB / Fluor)
    _section("§6 - PSC 1905 captive share (HII / GDEB / Fluor)")
    _qa_header()
    P["psc1905"] = c.write(
        ["PSC 1905 MRO (all buckets: strong + TAS + probable)",
         f'={sumifs_psc1905("FY2025 Obligation", ("Bucket", "MRO*"))}/1000000', None],
        styles=[S_DEFAULT, S_NUM, S_DEFAULT], outline_level=1)
    base = P["psc1905"]
    pct_base = _pct(f"C{base}")

    def _captive(parents):
        return "+".join(
            f'{sumifs_psc1905("FY2025 Obligation", ("Bucket", "MRO*"), ("Ultimate Parent", p))}/1000000'
            for p in parents)

    P["hii"] = c.write(
        ["HII (Huntington Ingalls / Newport News)", f"={_captive(['*HUNTINGTON*'])}",
         pct_base],
        styles=[S_LABEL_INDENT_1, S_NUM, S_PCT], outline_level=1)
    P["gd"] = c.write(
        ["GD (Electric Boat / General Dynamics)",
         f"={_captive(['*ELECTRIC BOAT*', '*GENERAL DYNAMICS*'])}", pct_base],
        styles=[S_LABEL_INDENT_1, S_NUM, S_PCT], outline_level=1)
    P["fluor"] = c.write(
        ["Fluor", f"={_captive(['*FLUOR*'])}", pct_base],
        styles=[S_LABEL_INDENT_1, S_NUM, S_PCT], outline_level=1)
    P["captive_sub"] = c.total(
        ["Captive subtotal (HII + GD + Fluor)",
         f"=C{P['hii']}+C{P['gd']}+C{P['fluor']}", pct_base],
        styles=[S_BOLD, S_NUM, S_PCT], n_cols=_NCOLS, outline_level=1)
    c.write(["Other primes (not HII / GD / Fluor)",
             f"=C{base}-C{P['captive_sub']}", pct_base],
            styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


VERIFICATION_ANSWERS = _make()
