"""s03_appendix_tam_build - explain how the workbook normalizes heterogeneous source
evidence into one annual TAM spend pool before any ASV addressability filter applies.

Shape-built formula bridge (no chart, no table). Four engine cards on the left -
contracts (recognize and annualize), budgets (slice by maritime instrumentation share),
U.S. segments (bounded low/base/high inputs), Europe anchors (country/segment modeled
spend) - drop into a central collector that flows into a dark TAM output rail on the right
(U.S. TAM, Europe TAM, Total TAM). Arithmetic operators appear only inside formulas. Two
no-fill commentary findings run along the bottom. No market-size values appear.

Spec: specs/sea_range_telemetry/s03_appendix_tam_build.md.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
    CAP_12PT, EXHIBIT_HEADER_13PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Methodology"
_BREADCRUMB_TOPIC = "TAM Build"
_TOPIC            = "TAM Build"
_TAKEAWAY = "Source evidence is normalized into annual spend before ASV filters apply."
_SOURCES = ("Sources: (1) USAspending.gov / FPDS award records and SEC EDGAR "
            "filings; (2) DoD FY2027 Budget Justification Books and U.S. Treasury "
            "/ DoD DWCF TAS 097-4930; (3) QinetiQ FY25 Annual Report, U.K. MOD "
            "LTPA / MSCA releases, DGA EM, CNES / CSG, FMV, Andøya Space, "
            "SaxaVord, and company analysis")

_QUALIFIER = "TAM method only; SAM addressability starts on the next slide"
_LEGEND = "Formula terms shown are model operations, not source categories"

_SZ_92 = 920    # 9.2pt: engine formula terms (style.py allows raw sizes with a note)
_SZ_8  = 800    # 8pt:   engine caveat / example chips
_SZ_95 = 950    # 9.5pt: U.S. bounded-input result line


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_ENGINE_TOP = BODY_Y + 300_000                  # 1_671_600
_COMM_H = 900_000
_COMM_Y = BODY_B - _COMM_H                       # 4_970_000
_ENGINE_BOT = _COMM_Y - 90_000                   # 4_880_000
_CENTER_Y = (_ENGINE_TOP + _ENGINE_BOT) // 2     # 3_275_800

# Two engine rows split by a centre gap where the collector bar runs.
_BAR_GAP = 240_000
_ROW_T_Y = _ENGINE_TOP                            # top-row card top
_ROW_T_B = _CENTER_Y - _BAR_GAP // 2             # 3_155_800
_CARD_H  = _ROW_T_B - _ROW_T_Y                   # 1_484_200
_ROW_B_Y = _CENTER_Y + _BAR_GAP // 2             # 3_395_800

# Two engine columns (spec inch positions, EMU), spine, and the dark output rail.
_COL1_X, _COL_W = 640_080, 2_423_160
_COL1_C = _COL1_X + _COL_W // 2                   # 1_851_660
_COL2_X = 3_337_560
_COL2_C = _COL2_X + _COL_W // 2                   # 4_549_140
_SPINE_X = 6_035_040
_RAIL_X  = 6_720_840
_RAIL_W  = BODY_R - _RAIL_X                       # 5_014_601

# Top band: qualifier (left) + formula mini-legend (right).
_TOP_Y, _TOP_H = BODY_Y, 250_000


# ── Local helpers ────────────────────────────────────────────────────────────
def _engine_card(base, x, y, fill, fg, cap, lines, body_align, result, result_size,
                 chips) -> str:
    """One engine card: rounded fill, a cap + formula/component stack + bold result,
    and an optional row of bottom chips (fill=None -> a no-fill italic caption)."""
    text_h = _CARD_H - (290_000 if chips else 0)
    bg = text_box(base, "EngineCard", x, y, _COL_W, _CARD_H, [paragraph([])],
                  fill=fill, prst="roundRect", geom_adj={"adj": 6_000}, anchor="t")
    paras = [paragraph([run(cap, size=CAP_12PT, bold=True, color=fg, font=FONT)],
                       align="ctr", space_after=300, line_spacing=100_000)]
    for i, ln in enumerate(lines):
        paras.append(paragraph([run(ln, size=_SZ_92, color=fg, font=FONT)],
                               align=body_align, line_spacing=100_000,
                               space_after=(300 if i == len(lines) - 1 else 0)))
    paras.append(paragraph([run(result, size=result_size, bold=True, color=fg,
                                font=FONT)], align="ctr", line_spacing=104_000))
    txt = text_box(base + 1, "EngineBody", x, y, _COL_W, text_h, paras,
                   fill=None, line_color=None, anchor="t",
                   insets=(100_000, 60_000, 100_000, 40_000))
    chip_xml = ""
    if chips:
        n = len(chips)
        gap = 80_000
        cw = (_COL_W - 200_000 - (n - 1) * gap) // n
        cy = y + text_h + 10_000
        ch_h = _CARD_H - text_h - 50_000
        for j, (ctext, cfill, cfg) in enumerate(chips):
            cx = x + 100_000 + j * (cw + gap)
            if cfill is None:
                chip_xml += text_box(
                    base + 2 + j, "EngineCaveat", cx, cy, cw, ch_h,
                    [paragraph([run(ctext, size=_SZ_8, italic=True, color=cfg,
                                    font=FONT)], align="ctr", line_spacing=100_000)],
                    fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
            else:
                chip_xml += text_box(
                    base + 2 + j, "EngineChip", cx, cy, cw, ch_h,
                    [paragraph([run(ctext, size=_SZ_8, italic=True, color=cfg,
                                    font=FONT)], align="ctr", line_spacing=100_000)],
                    fill=cfill, anchor="ctr", insets=(40_000, 16_000, 40_000, 16_000))
    return bg + txt + chip_xml


def _rail() -> str:
    """Dark annual-TAM output rail: cap + three formula bands + a bottom qualifier,
    separated by thin white dividers."""
    cap_h, us_h, eu_h, tot_h = 360_000, 1_000_000, 720_000, 620_000
    y0 = _ENGINE_TOP
    bg = text_box(70, "TamRail", _RAIL_X, y0, _RAIL_W, _ENGINE_BOT - y0,
                  [paragraph([])], fill=BLUE_5, anchor="t")
    cap = text_box(
        71, "TamRailCap", _RAIL_X, y0, _RAIL_W, cap_h,
        [paragraph([run("ANNUAL TAM SPEND POOL", size=EXHIBIT_HEADER_13PT, bold=True,
                        color=WHITE, font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="ctr", insets=(120_000, 20_000, 120_000, 20_000))

    def _band(sp_id, name, by, bh, label, formula):
        return text_box(
            sp_id, name, _RAIL_X, by, _RAIL_W, bh,
            [paragraph([run(label, size=EXHIBIT_HEADER_13PT, bold=True, color=WHITE,
                            font=FONT)], space_after=120, line_spacing=104_000),
             paragraph([run(formula, size=LABEL_9PT, color=WHITE, font=FONT)],
                       line_spacing=110_000)],
            fill=None, line_color=None, anchor="ctr", insets=(130_000, 30_000, 130_000, 30_000))

    us_y = y0 + cap_h
    eu_y = us_y + us_h
    tot_y = eu_y + eu_h
    qual_y = tot_y + tot_h
    us = _band(72, "UsTamBand", us_y, us_h, "U.S. TAM",
               "= vessel-prime + telemetry/range-support + allocated work + NAVAIR "
               "+ commercial / launch")
    eu = _band(73, "EuTamBand", eu_y, eu_h, "Europe TAM",
               "= sum of country / segment modeled annual spend")
    tot = _band(74, "TotalTamBand", tot_y, tot_h, "Total TAM",
                "= U.S. TAM + Europe TAM")
    qual = text_box(
        75, "TamRailQualifier", _RAIL_X, qual_y, _RAIL_W, _ENGINE_BOT - qual_y,
        [paragraph([run("ASV role suitability is not applied until SAM build",
                        size=FINEPRINT_8_5PT, italic=True, color=WHITE, font=FONT)],
                   line_spacing=104_000)],
        fill=None, line_color=None, anchor="ctr", insets=(130_000, 20_000, 130_000, 20_000))
    dividers = "".join(
        connector(76 + k, "TamRailDivider", _RAIL_X + 100_000, dy, _RAIL_W - 200_000, 0,
                  color=WHITE, width=9_525)
        for k, dy in enumerate((us_y, eu_y, tot_y, qual_y)))
    return bg + cap + us + eu + tot + qual + dividers


def _commentary(sp_id, x, w, finding, bullets) -> str:
    paras = [paragraph([run(finding, size=MESSAGE_11PT, bold=True, color=BLACK,
                            font=FONT)], space_after=70, line_spacing=106_000)]
    for j, b in enumerate(bullets):
        paras.append(paragraph([run(b, size=LABEL_9PT, color=BLACK, font=FONT)],
                               bullet=True, line_spacing=106_000,
                               space_after=(0 if j == len(bullets) - 1 else 60)))
    return text_box(sp_id, "Commentary", x, _COMM_Y, w, _COMM_H, paras,
                    fill=None, line_color=None, anchor="t",
                    insets=(110_000, 20_000, 90_000, 20_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    qualifier = text_box(
        10, "Qualifier", BODY_X, _TOP_Y, 6_300_000, _TOP_H,
        [paragraph([run(_QUALIFIER, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    legend = text_box(
        11, "FormulaLegend", 7_000_000, _TOP_Y, BODY_R - 7_000_000, _TOP_H,
        [paragraph([run(_LEGEND, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)], align="r")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)

    # Four engine cards (two columns x two rows).
    contracts = _engine_card(
        20, _COL1_X, _ROW_T_Y, BLUE_1, BLACK, "CONTRACTS",
        ["Reported value", "× relevance", "× maritime", "× instrumentation",
         "÷ years in PoP"], "ctr", "Recognized annual contract TAM", DENSE_BODY_10PT,
        [("Annual rows are not re-divided", None, BLACK)])
    budgets = _engine_card(
        30, _COL1_X, _ROW_B_Y, BLUE_2, BLACK, "BUDGETS",
        ["FY27 PB", "× maritime instrumentation share"], "ctr", "PE maritime slice",
        DENSE_BODY_10PT, [("NAVAIR rows; SBX / Pacific Collector anchors", GRAY_1, BLACK)])
    us_seg = _engine_card(
        40, _COL2_X, _ROW_T_Y, GRAY_1, BLACK, "U.S. SEGMENTS",
        ["Vessel-prime", "Telemetry and range support", "Allocated platform work",
         "Commercial and launch"], "l", "Bounded low / base / high inputs", _SZ_95,
        [("DWCF floor = cross-check only", GRAY_2, BLACK)])
    europe = _engine_card(
        50, _COL2_X, _ROW_B_Y, BLUE_4, WHITE, "EUROPE ANCHORS",
        ["Country / segment modeled annual spend"], "ctr", "Europe TAM", MESSAGE_11PT,
        [("Public-record floors", GRAY_1, BLACK), ("Modeled gap", GRAY_1, BLACK)])
    cards = contracts + budgets + us_seg + europe

    # Central collector: four drops into a horizontal bar, a short spine, and one
    # outbound arrow into the rail.
    drops = (
        connector(60, "ContractsDrop", _COL1_C, _ROW_T_B, 0, _CENTER_Y - _ROW_T_B,
                  color=BLACK, width=12_700)
        + connector(61, "BudgetsDrop", _COL1_C, _ROW_B_Y, 0, _CENTER_Y - _ROW_B_Y,
                    color=BLACK, width=12_700)
        + connector(62, "UsSegDrop", _COL2_C, _ROW_T_B, 0, _CENTER_Y - _ROW_T_B,
                    color=BLACK, width=12_700)
        + connector(63, "EuropeDrop", _COL2_C, _ROW_B_Y, 0, _CENTER_Y - _ROW_B_Y,
                    color=BLACK, width=12_700))
    bar = connector(64, "CollectorBar", _COL1_C, _CENTER_Y, _SPINE_X - _COL1_C, 0,
                    color=BLACK, width=12_700)
    spine = connector(65, "ConvergenceSpine", _SPINE_X, _CENTER_Y - 200_000, 0, 400_000,
                      color=BLACK, width=12_700)
    outbound = connector(66, "ToRail", _SPINE_X, _CENTER_Y, _RAIL_X - _SPINE_X, 0,
                         color=BLACK, width=15_875, arrow=True)
    spine_label = text_box(
        67, "SpineLabel", _SPINE_X + 40_000, _CENTER_Y - 280_000, _RAIL_X - _SPINE_X - 40_000,
        220_000,
        [paragraph([run("Normalize to annual $M", size=_SZ_8, italic=True, color=BLACK,
                        font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    flow = drops + bar + spine + outbound + spine_label

    rail = _rail()

    commentary = (
        _commentary(80, BODY_X, 5_500_000,
                    "TAM is an annual spend pool, not a share assumption.",
                    ["Contracts are filtered for relevance, maritime content, and "
                     "instrumentation content before annualization.",
                     "Budget lines are sliced by maritime instrumentation share "
                     "instead of counted at full program value."])
        + _commentary(81, BODY_X + 5_800_000, BODY_R - (BODY_X + 5_800_000),
                      "The build combines measured anchors with bounded model inputs.",
                      ["U.S. TAM uses explicit segment inputs plus a calculated "
                       "NAVAIR layer.",
                       "Europe TAM uses country / segment modeled annual spend, with "
                       "public-record floors where available."]))

    # Paint order: collector flow behind the cards / rail; commentary independent.
    return flow + cards + rail + qualifier + legend + commentary


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
