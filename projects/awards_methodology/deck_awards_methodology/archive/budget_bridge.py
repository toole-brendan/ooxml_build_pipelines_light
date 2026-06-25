"""budget_bridge - From appropriation to obligation: how a contract award
joins to the budget. Clean at the appropriation-account + color-of-money + fiscal-year
level; below that the program-level alignment runs through a curated opportunity bridge,
not an automatic TAS-to-line-item key join.

Style + chrome rules: deck_core/slide_guide.md. Built from the imported deck_core
builders (chrome + run/paragraph/text_box/table/connector) on the BODY box.

Visual read (reading order): a left-to-right bridge across the upper band
(BUDGET AUTHORITY -> Treasury Account Symbol pinch -> OBLIGATION ON A CONTRACT),
then the focal key-insight card centered under the TAS hook, then a worked-example
table (lower-left), then a muted funded-demand funnel inset (lower-right). A
money-type discipline rail runs along the bottom.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, tcell, trow, connector,
)
from deck_core.style import (
    BODY_X, BODY_CX, BODY_R, BODY_B,
    BLUE_1, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_5,
    DK, WHITE, BLACK, FONT,
    INSETS_CARD, INSETS_MICRO_CAP, INSETS_ANSWER_CARD, INSETS_LABEL,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
    MESSAGE_11PT, CAP_12PT,
    blue_pair,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"   # body slide; auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Budget alignment"                       # breadcrumb {Section} (bold)
_BREADCRUMB_TOPIC = "Contracts to the budget"                # breadcrumb topic-label variant
_TITLE_TOPIC      = "Aligning contracts to the budget"       # title {Topic}
_TAKEAWAY         = ("the join is clean at the account; the program-level bridge "
                     "is curated, not automatic")            # title {Finding}, sentence case
_SOURCES = ("Sources: (1) President's Budget P-1 (procurement) and R-1 (RDT&E), "
            "PB2027 vintage; (2) USAspending funding endpoint, Treasury Account "
            "Symbol per transaction; (3) internal Army Market Mapping workbook "
            "(budget and award opportunity attribution); then-year dollars")

# Color-of-money palette (one mapping reused by the swatches and the table scan
# column), ordered light -> dark by lifecycle stage.
_CM_RDTE = blue_pair(1)   # (BLUE_2, DK)     development
_CM_PROC = blue_pair(2)   # (BLUE_3, WHITE)  production
_CM_OM   = blue_pair(3)   # (BLUE_4, WHITE)  sustainment

_SSP = GRAY_3             # secondary (light) border color
_SSW = 9_525             # 0.75pt secondary border width


# ── Bridge geometry (upper band) ─────────────────────────────────────────────
_BR_Y, _BR_H = 1_950_000, 1_000_000
_BR_MID = _BR_Y + _BR_H // 2

_LN_X,  _LN_W  = BODY_X, 4_200_000                 # left node
_TAS_X, _TAS_W = 5_244_260, 1_700_000              # center pinch
_RN_X,  _RN_W  = 7_535_441, 4_200_000              # right node (ends at BODY_R)
_LN_R = _LN_X + _LN_W
_TAS_R = _TAS_X + _TAS_W


# ── Worked-example table (lower-left) ────────────────────────────────────────
_TBL_X = BODY_X
_TBL_COLS = [2_250_000, 1_450_000, 1_250_000, 1_450_000]   # sums to 6,400,000
_TBL_W = sum(_TBL_COLS)
_TBL_HEADER = ["Program", "Line item or PE", "Approp (color)", "Bridged opportunity"]
_TBL_BODY = [
    ["MSV(L), Maneuver Support Vessel (Light)", "BLI 8211R01001", "OPA (Procurement)", "OPP-MSVL"],
    ["Army Watercraft ESP (SLEP)",              "BLI 3569M11101", "OPA (Procurement)", "OPP-ESP"],
    ["Project 526, Marine S&T (autonomy and C2)", "PE 0603804A-526", "RDT&E",          "OPP-AWS-AUTONOMY"],
]
_TBL_PT = 9.5
_ROW_H = estimate_row_heights([_TBL_HEADER] + _TBL_BODY, _TBL_COLS,
                              size_pt=_TBL_PT, header_size_pt=_TBL_PT)
_TBL_CAP_Y = 3_900_000
_TBL_Y = 4_150_000

# Funnel inset (lower-right)
_FN_X, _FN_W = 7_100_000, BODY_R - 7_100_000       # ends at BODY_R


# ── Local helpers ────────────────────────────────────────────────────────────
def _swatch(sp_id, x, y, w, h, acronym, stage, pair):
    """Color-of-money swatch chip: bold acronym over an italic lifecycle stage."""
    fill, txt = pair
    return text_box(
        sp_id, f"Tag-{acronym}", x, y, w, h,
        [paragraph([run(acronym, size=LABEL_9PT, bold=True, color=txt, font=FONT)],
                   align="ctr", line_spacing=100_000),
         paragraph([run(stage, size=SOURCES_8PT, italic=True, color=txt, font=FONT)],
                   align="ctr", line_spacing=100_000)],
        anchor="ctr", fill=fill, line_color=_SSP, line_width=_SSW, insets=INSETS_MICRO_CAP)


def _tier(sp_id, x, y, w, h, label, value):
    """One muted funnel tier (centered, decreasing width): label and value."""
    return text_box(
        sp_id, f"FunnelTier-{label}", x, y, w, h,
        [paragraph([run(f"{label} · {value}", size=LABEL_9PT, bold=True,
                        color=DK, font=FONT)], align="ctr", line_spacing=100_000)],
        anchor="ctr", fill=BLUE_1, line_color=_SSP, line_width=_SSW,
        insets=INSETS_MICRO_CAP)


def _label(sp_id, name, x, y, w, h, paras, anchor="t"):
    """No-fill / no-border text label (commentary, captions, units)."""
    return text_box(sp_id, name, x, y, w, h, paras, anchor=anchor,
                    fill=None, insets=INSETS_LABEL)


# Table border specs (rule-skin: no header fill, cascading bottom rules).
_HDR_B = {"color": BLACK, "width": 19_050}   # 1.5pt under header
_ROW_B = {"color": BLACK, "width": 12_700}   # 1pt under body rows


def _hb(bottom):
    """Cell borders: horizontal-only (sides + top off, bottom per arg)."""
    return {"L": "none", "R": "none", "T": "none", "B": bottom}


def _tbl_row(cells, bottom, h):
    prog, li, approp, opp = cells
    af, at = _CM_PROC if approp.startswith("OPA") else _CM_RDTE
    return trow([
        tcell(prog,   bold=True, size=950, color=DK,  align="l", anchor="ctr", borders=_hb(bottom)),
        tcell(li,                size=950, color=DK,  align="l", anchor="ctr", borders=_hb(bottom)),
        tcell(approp, fill=af,   size=950, color=at,  align="l", anchor="ctr", borders=_hb(bottom)),
        tcell(opp,    font="Consolas", size=950, color=DK, align="l", anchor="ctr", borders=_hb(bottom)),
    ], h=h)


# ════════════════════════════════════════════════════════════════════════════
# BODY
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []

    # 1 ── Commentary 1: no-fill finding rail above the bridge ────────────────
    out.append(_label(
        10, "Commentary-JoinKeys", BODY_X, 1_371_600, BODY_CX, 540_000,
        [paragraph([run("The only valid join keys are agency, Treasury Account "
                        "Symbol, and fiscal year.",
                        size=MESSAGE_11PT, bold=True, color=DK, font=FONT)],
                   space_after=300),
         paragraph([run("Budget is not organized by NAICS or PSC, so contract codes "
                        "do not bridge. What the appropriation does tell you is color "
                        "of money: RDT&E for development, Procurement (OPA) for "
                        "production, O&M for sustainment, which reads as a program's "
                        "lifecycle stage.",
                        size=DENSE_BODY_10PT, color=DK, font=FONT)])]))

    # 2 ── Bridge: left node (budget authority) + color-of-money swatches ─────
    out.append(text_box(
        20, "Node-BudgetAuthority", _LN_X, _BR_Y, _LN_W, _BR_H,
        [paragraph([run("BUDGET AUTHORITY", size=CAP_12PT, bold=True, color=DK, font=FONT)],
                   space_after=400),
         paragraph([run("Appropriation account, then budget activity, then line item "
                        "(P-1) or program element (R-1)",
                        size=LABEL_9PT, color=DK, font=FONT)])],
        anchor="t", fill=BLUE_1, line_color=_SSP, line_width=_SSW, insets=INSETS_CARD))

    _sw_w = (_LN_W - 2 * 120_000 - 2 * 80_000) // 3
    _sw_y, _sw_h = _BR_Y + _BR_H - 350_000, 290_000
    _sw_x0 = _LN_X + 120_000
    out.append(_swatch(21, _sw_x0,                       _sw_y, _sw_w, _sw_h, "RDT&E",       "development", _CM_RDTE))
    out.append(_swatch(22, _sw_x0 + (_sw_w + 80_000),    _sw_y, _sw_w, _sw_h, "Procurement", "production",  _CM_PROC))
    out.append(_swatch(23, _sw_x0 + 2 * (_sw_w + 80_000), _sw_y, _sw_w, _sw_h, "O&M",        "sustainment", _CM_OM))

    # 3 ── Bridge: center pinch (Treasury Account Symbol) ─────────────────────
    out.append(text_box(
        30, "Node-TAS", _TAS_X, _BR_Y, _TAS_W, _BR_H,
        [paragraph([run("TREASURY ACCOUNT SYMBOL", size=LABEL_9PT, bold=True, color=DK, font=FONT)],
                   align="ctr", space_after=300),
         paragraph([run("captured on award", size=FINEPRINT_8_5PT, italic=True, color=DK, font=FONT)],
                   align="ctr")],
        anchor="ctr", fill=GRAY_2, line_color=_SSP, line_width=_SSW, insets=INSETS_MICRO_CAP))

    # 4 ── Bridge: right node (obligation on a contract), kept neutral ────────
    out.append(text_box(
        40, "Node-Obligation", _RN_X, _BR_Y, _RN_W, _BR_H,
        [paragraph([run("OBLIGATION ON A CONTRACT", size=CAP_12PT, bold=True, color=DK, font=FONT)],
                   space_after=400),
         paragraph([run("Contract family: PIID or IDV", size=LABEL_9PT, color=DK, font=FONT)],
                   space_after=200),
         paragraph([run("Awards, IDVs, and task orders roll up to a family",
                        size=FINEPRINT_8_5PT, italic=True, color=DK, font=FONT)])],
        anchor="t", fill=GRAY_1, line_color=_SSP, line_width=_SSW, insets=INSETS_CARD))

    # 5 ── Spine connectors (the single thread, arrowheads point downstream) ──
    out.append(connector(50, "Spine-L", _LN_R, _BR_MID, _TAS_X - _LN_R, 0,
                         color=DK, width=19_050, arrow=True))
    out.append(connector(51, "Spine-R", _TAS_R, _BR_MID, _RN_X - _TAS_R, 0,
                         color=DK, width=19_050, arrow=True))

    # 6 ── Key insight card: focal, centered under the TAS hook ───────────────
    _kc_w = 7_200_000
    _kc_x = (BODY_X + BODY_R) // 2 - _kc_w // 2
    out.append(text_box(
        60, "KeyInsight-OpportunityBridge", _kc_x, 3_010_000, _kc_w, 850_000,
        [paragraph([run("The hard part: the TAS resolves the account, not the program.",
                        size=DENSE_BODY_10PT, bold=True, color=WHITE, font=FONT)],
                   space_after=300),
         paragraph([run("A contract's funding_tas lands it in ‘Other Procurement, "
                        "Army, FY-XX’, not in a specific line item or program element. "
                        "We bridge budget and contracts through an analyst-curated "
                        "OPPORTUNITY that both a budget line and a contract family "
                        "attribute to. The TAS is the mechanical hook; the semantic "
                        "alignment is deliberate.",
                        size=DENSE_BODY_10PT, color=WHITE, font=FONT)])],
        anchor="ctr", fill=BLUE_5, line_color=BLACK, line_width=19_050,
        insets=INSETS_ANSWER_CARD))

    # 7 ── Worked-example table (lower-left) ──────────────────────────────────
    out.append(_label(
        70, "TableCaption", _TBL_X, _TBL_CAP_Y, _TBL_W, 220_000,
        [paragraph([run("Worked example: PB2027 lines",
                        size=DENSE_BODY_10PT, bold=True, color=DK, font=FONT)])]))
    rows = [trow([tcell(h, bold=True, size=950, color=DK, align="l", anchor="ctr",
                        borders=_hb(_HDR_B)) for h in _TBL_HEADER], h=_ROW_H[0])]
    for i, body_row in enumerate(_TBL_BODY):
        bottom = _ROW_B if i < len(_TBL_BODY) - 1 else "none"
        rows.append(_tbl_row(body_row, bottom, _ROW_H[i + 1]))
    out.append(table(71, "WorkedExample", _TBL_X, _TBL_Y, _TBL_W, sum(_ROW_H),
                     col_widths=_TBL_COLS, rows=rows))

    # 8 ── Funnel inset (lower-right), muted and supporting ───────────────────
    out.append(_label(
        80, "FunnelTitle", _FN_X, 3_900_000, _FN_W, 200_000,
        [paragraph([run("Funded-demand funnel", size=DENSE_BODY_10PT, bold=True,
                        color=DK, font=FONT)])]))
    out.append(_label(
        81, "FunnelUnits", _FN_X, 4_095_000, _FN_W, 160_000,
        [paragraph([run("Forward FY27–31, then-year $M", size=FINEPRINT_8_5PT,
                        italic=True, color=GRAY_5, font=FONT)])]))

    _tiers = [("Gross funded", "$4,200M", 1.00),
              ("Addressable", "$1,850M", 0.78),
              ("Saronic-serviceable", "$720M", 0.58),
              ("Weighted pursuit", "$310M", 0.42)]
    _t_y, _t_h, _t_gap = 4_275_000, 165_000, 18_000
    for i, (lab, val, frac) in enumerate(_tiers):
        w = int(_FN_W * frac)
        x = _FN_X + (_FN_W - w) // 2
        out.append(_tier(82 + i, x, _t_y + i * (_t_h + _t_gap), w, _t_h, lab, val))

    _mult_y = _t_y + len(_tiers) * (_t_h + _t_gap) + 12_000
    out.append(_label(
        86, "FunnelMultipliers", _FN_X, _mult_y, _FN_W, 150_000,
        [paragraph([run("Tiers apply addressable %, then fit %, then timing, access, "
                        "and win", size=FINEPRINT_8_5PT, italic=True, color=GRAY_5,
                        font=FONT)])]))

    # 9 ── Commentary 3: muted note tied to the funnel ────────────────────────
    out.append(_label(
        90, "Commentary-SeparateLenses", _FN_X, _mult_y + 175_000, _FN_W, 470_000,
        [paragraph([run("Separate lenses, never summed. ",
                        size=LABEL_9PT, bold=True, color=GRAY_5, font=FONT),
                    run("The forward budget spine sizes the market; contract "
                        "obligations measure what has already flowed.",
                        size=LABEL_9PT, color=GRAY_5, font=FONT)])]))

    # 10 ── Money-type discipline rail (bottom method strip) ──────────────────
    out.append(text_box(
        95, "MoneyTypeRail", BODY_X, 5_640_000, BODY_CX, 230_000,
        [paragraph([run("Money-type discipline: ", size=FINEPRINT_8_5PT, bold=True,
                        color=DK, font=FONT),
                    run("PY actual, then CY enacted, then BY request, then outyears. "
                        "Request is request_total only, never summed across types.",
                        size=FINEPRINT_8_5PT, color=DK, font=FONT)], align="l")],
        anchor="ctr", fill=GRAY_1, line_color=_SSP, line_width=_SSW,
        l_ins=140_000, r_ins=140_000, t_ins=45_720, b_ins=45_720))

    return "".join(out)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld> (no page number; auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
