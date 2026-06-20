"""s02_appendix_evidence_base - show where the workbook's data comes from and how each
source family feeds a different part of the TAM / SAM model, as a four-lane source-to-model
map: source family -> fields captured -> how the model uses it -> example anchors.

Shape-built lane map (no chart, no table). Four horizontal lanes, each reading left to
right through four aligned columns joined by black right-arrows; column headers with a
rule above the lanes. A small provenance-control pod (source IDs / assumption support /
checks) sits bottom-left, with two no-fill commentary findings to its right. No TAM or
SAM result values - this page is about provenance and model routing.

Spec: specs/sea_range_telemetry/s02_appendix_evidence_base.md.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Methodology"
_BREADCRUMB_TOPIC = "Evidence Base"
_TOPIC            = "Evidence Base"
_TAKEAWAY = ("Four source streams anchor distinct model functions before "
             "assumptions fill bounded gaps.")
_SOURCES = ("Sources: (1) USAspending.gov / FPDS award records and SEC EDGAR "
            "filings; (2) DoD FY2027 Budget Justification Books, DOT&E FY2025 "
            "Annual Report, NAVAIR VX-30, NASA Wallops, and Point Mugu Sea Range "
            "EIS / OEIS; (3) QinetiQ FY25 Annual Report, U.K. MOD LTPA / MSCA "
            "releases, DGA EM, CNES / CSG, FMV, Andøya Space, SaxaVord, and "
            "company analysis")

_QUALIFIER = ("Data provenance by source family; current annualized U.S. and Europe "
              "market-sizing workbook")

# Raw sizes with no exact token (style.py allows raw sizes with a note).
_SZ_83 = 830    # 8.3pt: fields-card body
_SZ_82 = 820    # 8.2pt: example-card body
_SZ_8  = 800    # 8pt:   model-use chip text, pod body


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Four lane columns: source | fields | model use | examples, with arrow gutters.
_C1_X, _C1_W = BODY_X, 2_050_000
_C1_R = _C1_X + _C1_W                       # 2_503_079
_C2_X, _C2_W = 2_803_079, 3_750_000
_C2_R = _C2_X + _C2_W                       # 6_553_079
_C3_X, _C3_W = 6_853_079, 2_050_000
_C3_R = _C3_X + _C3_W                       # 8_903_079
_C4_X = 9_203_079
_C4_W = BODY_R - _C4_X                      # 2_532_362

# Top band: qualifier, then column headers + rule, then the lanes.
_QUAL_Y, _QUAL_H = BODY_Y, 220_000
_HDR_Y, _HDR_H   = BODY_Y + 260_000, 160_000          # 1_631_600
_RULE_Y          = _HDR_Y + _HDR_H                     # 1_791_600
_LANE_TOP        = _RULE_Y + 40_000                    # 1_831_600

# Bottom band: provenance pod (left) + two commentary blocks (right).
_BOT_H = 980_000
_BOT_Y = BODY_B - _BOT_H                                # 4_890_000

_LANE_GAP = 70_000
_LANE_H   = (_BOT_Y - _LANE_TOP - 70_000 - 3 * _LANE_GAP) // 4   # 695_000

def _lane_y(i: int) -> int:
    return _LANE_TOP + i * (_LANE_H + _LANE_GAP)

def _lane_mid(i: int) -> int:
    return _lane_y(i) + _LANE_H // 2

# Bottom-band columns.
_POD_X, _POD_W = BODY_X, 4_200_000
_CM1_X, _CM1_W = 4_953_079, 3_150_000
_CM2_X = 8_303_079
_CM2_W = BODY_R - _CM2_X                                # 3_432_362


# ── Content ──────────────────────────────────────────────────────────────────
_HEADERS = [
    (_C1_X, "SOURCE FAMILY"), (_C2_X, "FIELDS CAPTURED"),
    (_C3_X, "HOW MODEL USES IT"), (_C4_X, "EXAMPLE ANCHORS"),
]

# Source family cards: (cap, subline, fill, fg).
_SOURCES_CARDS = [
    ("CONTRACTS", "PIID-level awards and factor tables", BLUE_1, BLACK),
    ("BUDGETS", "Program lines and maritime shares", BLUE_2, BLACK),
    ("EVENTS AND RATES", "Cadence, mission cost, and vessel economics", BLUE_3, WHITE),
    ("EUROPE ANCHORS", "Country and segment spend anchors", BLUE_4, WHITE),
]

# Model-use chips per lane: (list-of-chip-text, fill, fg).
_CHIPS = [
    (["Recognized contract TAM", "Contract-anchored SAM"], BLUE_2, BLACK),
    (["PE maritime slice", "NAVAIR TAM component", "Cross-check anchors"], BLUE_2, BLACK),
    (["Event-derived SAM", "Pacific_MRIS overlap eligibility", "Day-rate support"],
     BLUE_3, WHITE),
    (["Europe TAM", "Europe SAM", "Country / segment cut"], BLUE_4, WHITE),
]

# Example anchor cards (no fill, 1pt black border): one line per anchor.
_EXAMPLES = [
    ["TOTE / Pacific MRIS", "Crowley T-AGOS / T-AGM", "Hornbeck SURTASS-E",
     "J-TECH II and TETRAS II", "Reliance ATR and PMRF primes"],
    ["MDA SBX", "Pacific Collector / Tracker", "NAVAIR 0605864N / 0605863N",
     "Air Force 0605807F", "SBX vessel and OSV categories"],
    ["Aegis BMD", "CPS / LRHW common AUR", "NGI and THAAD", "MACH-TB 2.0 and HTB",
     "SBX, MRIS, OSV rate stack"],
    ["U.K. LTPA and MSCA", "DragonFire", "DGA EM and Monge", "Italy PISQ",
     "Andøya, SaxaVord, CSG, FMV ranges"],
]

# Provenance-pod rows: (label, description).
_POD_ROWS = [
    ("Source IDs", "Resolve in Sources & Glossary"),
    ("Assumption support", "Input-to-source map lives outside editable cells"),
    ("Model checks", "Validate source IDs, basis summaries, and cross-tab tie-outs"),
]

_FINDINGS = [
    ("The evidence streams are not interchangeable.",
     ["Contracts anchor awarded and obligated activity.",
      "Budgets cover spend where contracts are thin.",
      "Events and rates convert cadence into event SAM.",
      "Europe anchors set country and segment spend."]),
    ("Assumptions are bounded and source-mapped.",
     ["Editable knobs sit in the Assumptions tab.",
      "Source-support map lives in Sources & Glossary.",
      "Checks keep source IDs and basis summaries wired."]),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _fields_paras(i):
    """Fields-captured card paragraphs; selected term prefixes bolded per spec."""
    B = lambda t: run(t, size=_SZ_83, bold=True, color=BLACK, font=FONT)
    R = lambda t: run(t, size=_SZ_83, color=BLACK, font=FONT)
    if i == 0:
        return [
            paragraph([R("PIID, vendor, value, value type, period, vessels, agency, "
                         "TAM bucket, source ID")], line_spacing=102_000, space_after=200),
            paragraph([B("TAM factors: "), R("relevance, maritime, instrumentation")],
                      line_spacing=102_000, space_after=120),
            paragraph([B("ASV factors: "), R("vessel share, role share")],
                      line_spacing=102_000),
        ]
    if i == 1:
        return [
            paragraph([R("PE code, title, agency, layer, "), B("FY27 PB"),
                       R(", maritime low/base/high shares, source ID")],
                      line_spacing=102_000, space_after=200),
            paragraph([B("SBX"), R(" decomposition and "), B("NAVAIR"),
                       R(" aviation maritime-range layer")], line_spacing=102_000),
        ]
    if i == 2:
        return [
            paragraph([R("Program, family codes, annual events, vessels per event, "
                         "launch site")], line_spacing=102_000, space_after=200),
            paragraph([B("Per-event cost"), R(", underway days, "), B("vessel share"),
                       R(", "), B("role share"), R(", "), B("overlap group"),
                       R(", day rates")], line_spacing=102_000),
        ]
    return [
        paragraph([R("Country/segment, "), B("floor"), R(" low/high, "), B("modeled"),
                   R(" low/base/high, "), B("vessel share"), R(", "), B("role share"),
                   R(", role category, source ID")], line_spacing=102_000),
    ]


def _source_card(sp_id, i) -> str:
    cap, sub, fill, fg = _SOURCES_CARDS[i]
    return text_box(
        sp_id, "SourceCard", _C1_X, _lane_y(i), _C1_W, _LANE_H,
        [paragraph([run(cap, size=DENSE_BODY_10PT, bold=True, color=fg, font=FONT)],
                   space_after=60, line_spacing=104_000),
         paragraph([run(sub, size=FINEPRINT_8_5PT, italic=True, color=fg, font=FONT)],
                   line_spacing=104_000)],
        fill=fill, anchor="ctr", insets=(80_000, 40_000, 80_000, 40_000))


def _fields_card(sp_id, i) -> str:
    return text_box(sp_id, "FieldsCard", _C2_X, _lane_y(i), _C2_W, _LANE_H,
                    _fields_paras(i), fill=GRAY_1, anchor="ctr",
                    insets=(70_000, 30_000, 70_000, 30_000))


def _chip_stack(base_id, i) -> str:
    chips, fill, fg = _CHIPS[i]
    n = len(chips)
    gap = 40_000
    ch_h = (_LANE_H - (n - 1) * gap) // n
    parts = []
    for j, txt in enumerate(chips):
        y = _lane_y(i) + j * (ch_h + gap)
        parts.append(text_box(
            base_id + j, "ModelUseChip", _C3_X, y, _C3_W, ch_h,
            [paragraph([run(txt, size=_SZ_8, bold=True, color=fg, font=FONT)],
                       align="ctr", line_spacing=100_000)],
            fill=fill, anchor="ctr", insets=(40_000, 14_000, 40_000, 14_000)))
    return "".join(parts)


def _example_card(sp_id, i) -> str:
    lines = _EXAMPLES[i]
    paras = [paragraph([run(t, size=_SZ_82, color=BLACK, font=FONT)],
                       line_spacing=100_000) for t in lines]
    return text_box(sp_id, "ExampleCard", _C4_X, _lane_y(i), _C4_W, _LANE_H, paras,
                    fill=None, line_color=BLACK, line_width=12_700, anchor="ctr",
                    insets=(60_000, 24_000, 60_000, 24_000))


def _lane_arrows(base_id, i) -> str:
    y = _lane_mid(i)
    return (
        connector(base_id, "FlowSourceToFields", _C1_R, y, _C2_X - _C1_R, 0,
                  color=BLACK, width=12_700, arrow=True)
        + connector(base_id + 1, "FlowFieldsToModel", _C2_R, y, _C3_X - _C2_R, 0,
                    color=BLACK, width=12_700, arrow=True)
        + connector(base_id + 2, "FlowModelToExamples", _C3_R, y, _C4_X - _C3_R, 0,
                    color=BLACK, width=12_700, arrow=True))


def _provenance_pod() -> str:
    cap_h = 200_000
    body_y = _BOT_Y + cap_h
    body_h = _BOT_H - cap_h
    row_h = body_h // 3
    bg = text_box(200, "ProvenancePod", _POD_X, _BOT_Y, _POD_W, _BOT_H,
                  [paragraph([])], fill=GRAY_1, anchor="t")
    cap = text_box(
        201, "ProvenanceCap", _POD_X, _BOT_Y, _POD_W, cap_h,
        [paragraph([run("PROVENANCE CONTROL", size=DENSE_BODY_10PT, bold=True,
                        color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5, anchor="ctr", insets=(120_000, 20_000, 120_000, 20_000))
    rows = []
    for j, (label, desc) in enumerate(_POD_ROWS):
        y = body_y + j * row_h
        rows.append(text_box(
            202 + j, "ProvenanceRow", _POD_X, y, _POD_W, row_h,
            [paragraph([run(label, size=FINEPRINT_8_5PT, bold=True, color=BLACK,
                            font=FONT)], space_after=20, line_spacing=100_000),
             paragraph([run(desc, size=_SZ_82, color=BLACK, font=FONT)],
                       line_spacing=100_000)],
            fill=None, line_color=None, anchor="ctr",
            insets=(120_000, 16_000, 120_000, 16_000)))
        if j > 0:
            rows.append(connector(205 + j, "PodDivider", _POD_X + 90_000, y,
                                  _POD_W - 180_000, 0, color=BLACK, width=9_525))
    return bg + cap + "".join(rows)


def _commentary(sp_id, x, w, finding, bullets) -> str:
    paras = [paragraph([run(finding, size=MESSAGE_11PT, bold=True, color=BLACK,
                            font=FONT)], space_after=70)]
    for j, b in enumerate(bullets):
        paras.append(paragraph([run(b, size=LABEL_9PT, color=BLACK, font=FONT)],
                               bullet=True,
                               space_after=(0 if j == len(bullets) - 1 else 50)))
    return text_box(sp_id, "Commentary", x, _BOT_Y, w, _BOT_H, paras,
                    fill=None, line_color=None, anchor="t",
                    insets=(110_000, 20_000, 90_000, 20_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    qualifier = text_box(
        10, "Qualifier", BODY_X, _QUAL_Y, BODY_R - BODY_X, _QUAL_H,
        [paragraph([run(_QUALIFIER, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)

    headers = "".join(
        text_box(11 + k, "ColumnHeader", x, _HDR_Y,
                 (_C2_X - _C1_X) if k == 0 else min(3_000_000, BODY_R - x), _HDR_H,
                 [paragraph([run(text, size=LABEL_9PT, bold=True, color=BLACK,
                                 font=FONT)])],
                 fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
        for k, (x, text) in enumerate(_HEADERS))
    rule = connector(15, "HeaderRule", _C1_X, _RULE_Y, BODY_R - _C1_X, 0,
                     color=BLACK, width=12_700)

    arrows = "".join(_lane_arrows(60 + 3 * i, i) for i in range(4))
    source_cards = "".join(_source_card(20 + i, i) for i in range(4))
    fields_cards = "".join(_fields_card(30 + i, i) for i in range(4))
    chip_stacks = "".join(_chip_stack(100 + 10 * i, i) for i in range(4))
    example_cards = "".join(_example_card(40 + i, i) for i in range(4))

    pod = _provenance_pod()
    commentary = (_commentary(210, _CM1_X, _CM1_W, *_FINDINGS[0])
                  + _commentary(211, _CM2_X, _CM2_W, *_FINDINGS[1]))

    # Paint order: arrows behind the lane cards; headers/rule/pod/commentary after.
    return (arrows + source_cards + fields_cards + chip_stacks + example_cards
            + qualifier + headers + rule + pod + commentary)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
