"""data_obbba_funding - the "OBBBA Mandatory" tab (one module = one sheet).

OBBBA (PL 119-21, Title II) Sec. 20002 mandatory funding for submarine new
construction, per the FY 2026 Mandatory Funding Allocation Plan. A separate sheet,
never an edit to the SCN Budget P-5c source: of the $29,176.3M section, only
Sec. 20002(16) - the second FY2026 Virginia-class submarine, $4,600.0M - is
new-construction procurement and feeds TAM. The award has no cost-category
breakout, so §3 bridges the gross award to a BC base via the BC-share control on
Assumptions §4 (observed = Virginia FY26 P-5c BC %); the BC base rides the BC
supplier coefficient in TAM Build as its own toggled stream. Submarine-relevant
capacity / workforce / supplier lines are carried as memo evidence (same exclusion
logic as SIB), and repair / nuclear-adjacent lines are memo-excluded.

Double-count basis: every PB vintage (PB22-PB27) reports Virginia FY2026 qty = 1;
the SCN Budget FY26 column (PB2027) is the discretionary boat only, so the
mandatory award is additive. TAM Build §5 pins the Virginia FY26 Total Ship
Estimate to the PB2027 one-boat value ($5,389.1M): if a future vintage refresh
restates FY26 to include the reconciliation boat, that check FAILs and this
stream must be zeroed or re-based before the model is read.

FY treatment: all Sec. 20002 dollars are FY2026 budget authority (FY2027 column is
zero; funds available through 2029-09-30). FY27 receives dollars only via the
Assumptions §4 execution-spillover control (default 0).

Promoted accessors: obbba_gross_cell / obbba_gross_total_cell (then-year inputs),
obbba_bc_base_cell (constant-FY2026 BC base; consumed by TAM Build),
obbba_capacity_total_cell, obbba_excluded_total_cell.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.sheets.data_deflators import deflator_factor_cell
from workbook_submarines.sheets.inputs_assumptions import (
    obbba_bc_share_cell, obbba_spillover_cell,
)
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "OBBBA Mandatory"
_FY = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_COL = {fy: col_letter(2 + i) for i, fy in enumerate(_FY)}       # C..H
_C_FIRST, _C_LAST = col_letter(2), col_letter(1 + len(_FY))
_TOTAL_COL = col_letter(2 + len(_FY))                               # I
_N_COLS = 1 + len(_FY) + 1
_HDR = [S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(_FY) + 1)
_LI_LABEL = {2013: "Virginia (LI 2013)", 1045: "Columbia (LI 1045)"}
_BASE = 13                  # title(2) + blank + §1 at-a-glance(4-10) + 2 blanks

# Sec. 20002(16): second FY2026 Virginia-class submarine, then-year $M.
_GROSS = {(2013, 2026): 4600.0}

# Submarine-relevant Sec. 20002 capacity / cadence lines (memo; excluded from TAM).
_CAPACITY = [
    ("20002(1)", "Accelerated Training in Defense Mfg ($36.1M CLB + $213.9M VCS wage)", 250.0),
    ("20002(2)", "Turbine generators, second supplier (1+2 Columbia/Virginia cadence)", 250.0),
    ("20002(3)", "Additive mfg / weld wire / machining capacity (incl. CLB productivity)", 450.0),
    ("20002(10)", "Advanced mfg techniques at EB and NNS (factory of the future)", 500.0),
    ("20002(13)", "MIB workforce development ($48M CLB + $402M VCS)", 450.0),
    ("20002(14)", "Supplier development, sequence-critical suppliers", 750.0),
    ("20002(15)", "Advanced mfg processes across naval shipbuilding IB", 250.0),
]
_SECTION_TOTAL = 29176.3

# Submarine-adjacent lines outside new-construction scope (memo).
_EXCLUDED = [
    ("20002(11)", "Additional dry-dock capability (Puget Sound DD4)", 500.0, "repair"),
    ("20002(12)", "Cold spray repair technologies", 50.0, "repair"),
    ("20003(8)", "Ohio-class tube conversion for additional missiles", 62.0, "nuclear / GFE"),
]


def _build_body(tab: str, base: int):
    P = {"gross": {}, "bcq": {}, "bcq_const": {}}
    SHARE, SPILL = obbba_bc_share_cell(), obbba_spillover_cell()
    c = RowCursor(base)

    # §2 Source line + then-year award inputs
    c.banner("§2 - Source line (OBBBA Sec. 20002, line 16)", _N_COLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for field, value in [
        ("Authority", "PL 119-21 Title II (OBBBA), Sec. 20002 Shipbuilding, line 16"),
        ("Title", "Second Virginia-class submarine in fiscal year 2026"),
        ("Program", "Virginia class (LI 2013) - one boat, additive to the FY26 discretionary request"),
        ("Funding type", "Mandatory appropriation (reconciliation)"),
        ("Scope", "Full ship procurement (no cost-category breakout)"),
        ("Award timing", "FY2026, alongside the discretionary FY26 boat"),
        ("Obligation availability", "Through 2029-09-30"),
        ("Booking basis", "Budget-year (all in FY2026)"),
    ]:
        c.write([field, value], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank()
    c.write(["Class"] + list(_FY) + ["Total"], styles=_HDR)
    for li in (2013, 1045):
        vals = ([_LI_LABEL[li]] + [_GROSS.get((li, fy), 0) for fy in _FY]
                + [lambda r: f"=SUM({_C_FIRST}{r}:{_C_LAST}{r})"])
        P["gross"][li] = c.write(vals, styles=[S_BOLD] + [S_NUM_INPUT] * len(_FY) + [S_NUM],
                                 outline_level=1)
    g13, g10 = P["gross"][2013], P["gross"][1045]
    P["gross_total"] = c.total(
        ["Total (Va + Col)"]
        + [f"=N({_FY_COL[fy]}{g13})+N({_FY_COL[fy]}{g10})" for fy in _FY]
        + [lambda r: f"=SUM({_C_FIRST}{r}:{_C_LAST}{r})"],
        styles=[S_BOLD] + [S_NUM] * (len(_FY) + 1), n_cols=_N_COLS)
    c.blank(2)

    # §3 BC/GFE bridge (gross award x modeled BC share; FY27 via spillover)
    c.banner("§3 - BC/GFE bridge (gross x BC share, Assumptions §4)", _N_COLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§3a - OBBBA BC base ($M then-year; FY27 = FY26 x spillover)", _N_COLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Class"] + list(_FY) + ["Total"], styles=_HDR)
    c26, c27 = _FY_COL[2026], _FY_COL[2027]
    for li in (2013, 1045):
        g = P["gross"][li]

        def _bcq(fy, g=g):
            if fy == 2026:
                return f"={c26}{g}*{SHARE}*(1-{SPILL})"
            if fy == 2027:
                return f"={c27}{g}*{SHARE}+{c26}{g}*{SHARE}*{SPILL}"
            return f"={_FY_COL[fy]}{g}*{SHARE}"

        vals = ([_LI_LABEL[li]] + [_bcq(fy) for fy in _FY]
                + [lambda r: f"=SUM({_C_FIRST}{r}:{_C_LAST}{r})"])
        P["bcq"][li] = c.write(vals, styles=[S_BOLD] + [S_NUM] * (len(_FY) + 1),
                               outline_level=1)
    b13, b10 = P["bcq"][2013], P["bcq"][1045]
    c.write(["GFE / non-BC remainder ($M; excluded from TAM)"]
            + [f"=N({_FY_COL[fy]}{P['gross_total']})-N({_FY_COL[fy]}{b13})-N({_FY_COL[fy]}{b10})"
               for fy in _FY]
            + [lambda r: f"=SUM({_C_FIRST}{r}:{_C_LAST}{r})"],
            styles=[S_DEFAULT] + [S_NUM] * (len(_FY) + 1), outline_level=1)
    c.blank()
    c.banner("§3b - Constant FY2026 $M (then-year x deflator)", _N_COLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Class"] + list(_FY) + ["Total"], styles=_HDR)
    for li in (2013, 1045):
        vals = ([_LI_LABEL[li]]
                + [f"={_FY_COL[fy]}{P['bcq'][li]}*{deflator_factor_cell(fy)}" for fy in _FY]
                + [lambda r: f"=SUM({_C_FIRST}{r}:{_C_LAST}{r})"])
        P["bcq_const"][li] = c.write(vals, styles=[S_BOLD] + [S_LINK_NUM] * len(_FY) + [S_NUM],
                                     outline_level=1)
    c.blank(2)

    # §4 Capacity / cadence evidence (memo; excluded from TAM)
    c.banner("§4 - Capacity / cadence evidence ($M; memo, excluded from TAM)", _N_COLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Sec. 20002 item", "Description", "$M"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER])
    cap_first = c.at()
    for item, desc, dollars in _CAPACITY:
        c.write([item, desc, dollars], styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT],
                outline_level=1)
    cap_last = c.at() - 1
    P["cap_total"] = c.total(["", "Total capacity / cadence memo", f"=SUM(D{cap_first}:D{cap_last})"],
                             styles=[S_DEFAULT, S_BOLD, S_NUM], n_cols=3)
    c.blank()
    c.write(["20002", "Sec. 20002 total (all shipbuilding)", _SECTION_TOTAL],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT], outline_level=1)
    c.write(["20002(16)", "of which submarine new construction (item 16)",
             f"={_TOTAL_COL}{P['gross_total']}"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.blank(2)

    # §5 Excluded submarine-adjacent lines (memo)
    c.banner("§5 - Excluded submarine-adjacent lines ($M; memo)", _N_COLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Item", "Description", "$M", "Reason"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    exc_first = c.at()
    for item, desc, dollars, reason in _EXCLUDED:
        c.write([item, desc, dollars, reason],
                styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_DEFAULT], outline_level=1)
    exc_last = c.at() - 1
    P["exc_total"] = c.total(["", "Total excluded memo", f"=SUM(D{exc_first}:D{exc_last})", ""],
                             styles=[S_DEFAULT, S_BOLD, S_NUM, S_DEFAULT], n_cols=4)

    return c.rows, c.at(), P


# ── Layout pass: body first (backs the accessors) ───────────────────────────
_rows, _after, _P = _build_body(_TAB, _BASE)


def _check(li, fy):
    if li not in (2013, 1045):
        raise ValueError(f"Unknown LI {li!r}; expected 2013 or 1045")
    if fy not in _FY_COL:
        raise ValueError(f"FY {fy!r} outside {_FY!r}")


def obbba_gross_cell(li: int, fy: int) -> str:
    _check(li, fy)
    return f"'{_TAB}'!{_FY_COL[fy]}{_P['gross'][li]}"


def obbba_gross_total_cell() -> str:
    return f"'{_TAB}'!{_TOTAL_COL}{_P['gross_total']}"


def obbba_bc_base_cell(li: int, fy: int) -> str:
    _check(li, fy)
    return f"'{_TAB}'!{_FY_COL[fy]}{_P['bcq_const'][li]}"


def obbba_capacity_total_cell() -> str:
    return f"'{_TAB}'!D{_P['cap_total']}"


def obbba_excluded_total_cell() -> str:
    return f"'{_TAB}'!D{_P['exc_total']}"


def _render_obbba_funding() -> WorksheetSpec:
    # Full-gross sensitivity needs the BC coefficient - lazy import breaks the
    # data <- model import direction (TAM Build imports this module). The OBBBA
    # boat is a Virginia, so the sensitivity rides the Virginia class coefficient.
    from workbook_submarines.sheets.model_tam_build import va_bc_supplier_coeff_cell
    c = RowCursor(2)
    c.banner(_TAB, _N_COLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Mandatory funding ($M)", _N_COLS, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    b13, b10 = _P["bcq_const"][2013], _P["bcq_const"][1045]
    c.write(["Gross award (Sec. 20002(16)) $M", f"={_TOTAL_COL}{_P['gross_total']}"],
            styles=[S_BOLD, S_NUM])
    c.write(["OBBBA BC base in TAM $M (constant FY2026)",
             f"={_TOTAL_COL}{b13}+{_TOTAL_COL}{b10}"], styles=[S_BOLD, S_NUM])
    c.write(["Full-gross sensitivity $M (reference; not applied)",
             f"={_TOTAL_COL}{_P['gross_total']}*{va_bc_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Capacity / cadence memo $M (excluded)", f"=D{_P['cap_total']}"],
            styles=[S_DEFAULT, S_NUM])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)

    ws = worksheet(c.rows, cols=[46, 10, 10, 10, 10, 10, 10, 12],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


OBBBA_FUNDING = SheetEntry(_TAB, _GROUP, _render_obbba_funding)
