"""s10_body_supplier_share_evidence - keep the two programs' supplier-share inputs
visibly separate: DDG solves a redaction problem (restore redacted MYP masters to
read outside-yards POP), submarine solves an evidence-breadth problem (a deliberately
strict 35% view against broader POP anchors). Strict inputs hold TAM conservative,
and the two applied shares feed two separate models - never a blended percentage.

Pattern A: a two-card top badge row (the applied 13% and 35% anchors), a
side-by-side method table (left, rule skin, Program grouped by row span), a no-fill
commentary box (right), and one focal callout strip. The table uses a rule skin (not
the dark-header governing-rule table on s08) so the two tables read differently.

Spec: ds_specs/s10_body_supplier_share_evidence.txt (SLIDE 10 - SUPPLIER-SHARE).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, trow, tcell,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_3, BLUE_4, BLUE_5, GRAY_1,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, MESSAGE_11PT, CAP_12PT, RIBBON_KPI_18PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Sizing Methodology"
_BREADCRUMB_TOPIC = "Supplier Share"
_TOPIC            = "Supplier Share"
_TAKEAWAY = ("Strict inputs hold TAM conservative, but DDG and submarine solve "
             "different evidence problems.")
_SOURCES = ("Sources: (1) DDG MYP redaction correction and outside-yards "
            "place-of-performance evidence; (2) submarine coefficient and AP/LLTM "
            "boundary evidence; (3) Navy SCN and P-5c Basic Construction budget "
            "justification, FY2022–FY2027")

_EVID_95 = 950   # 9.5pt: commentary supporting evidence (style.py allows raw sizes)


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Two share badges (top), a method table (left) with a commentary box (right)
# aligned at the table top, and a focal callout strip below both.
_TABLE_W = 7_150_000                            # ~7.82in (Pattern A)
_GAP_TC  = 280_000
_COMM_X  = BODY_X + _TABLE_W + _GAP_TC          # 7_883_079
_COMM_W  = BODY_R - _COMM_X                     # 3_852_362
_COMM_INSETS = (137_160, 30_000, 137_160, 30_000)

# Badge height holds a 2-line ALL-CAPS cap + the 18pt value + the italic subline.
# (The cap is long bold all-caps - "SUBMARINE APPLIED BC SUPPLIER SHARE" - so it
# wraps to two lines and the box must clear both, or the subline clips.)
_BADGE_Y, _BADGE_H = BODY_Y, 980_000
_BADGE_GAP = 200_000
_BADGE_W   = (_TABLE_W - _BADGE_GAP) // 2        # 3_475_000
_BADGE_X   = [BODY_X, BODY_X + _BADGE_W + _BADGE_GAP]

# Callout pinned ~40k above the body floor; the method table grows to fill the area
# between the badges and the callout (the slide's primary object), so the page reads
# evenly instead of leaving a gap at the bottom.
_CALL_H = 460_000
_CALL_Y = BODY_B - 40_000 - _CALL_H              # 5_370_000

_TABLE_Y  = _BADGE_Y + _BADGE_H + 150_000        # 2_501_600
_HDR_H    = 380_000
_ROW_H    = 584_600                               # body rows sized to fill the area
_TABLE_CY = _HDR_H + 4 * _ROW_H                   # 2_718_400  -> bottom 5_220_000

_COMM_Y, _COMM_H = _TABLE_Y, _TABLE_CY            # top-aligned with the table grid

# Five columns: Program (narrow), Evidence issue (compact), Applied value (model
# input), Broader evidence views (widest), Feeds headline TAM (decision fragment).
_COL_W = [900_000, 1_150_000, 1_700_000, 2_000_000, 1_400_000]   # sum = _TABLE_W

_HDRS = ["PROGRAM", "EVIDENCE ISSUE", "APPLIED VALUE", "BROADER EVIDENCE VIEWS",
         "FEEDS HEADLINE TAM"]
_B15  = {"B": {"color": BLACK, "width": 19_050}}   # 1.5pt under header
_B1   = {"B": {"color": BLACK, "width": 12_700}}   # 1pt under a body row
_BN   = {"B": "none"}                              # no rule under the last row


# ── Content ──────────────────────────────────────────────────────────────────
_BADGES = [
    ("DDG APPLIED BC SUPPLIER SHARE", "13%", "MYP-corrected non-GFE BC stream",
     BLUE_3),                                       # 6E91B1
    ("SUBMARINE APPLIED BC SUPPLIER SHARE", "35%",
     "Strict non-nuclear Basic Construction view", BLUE_4),   # 3D5972
]

_FINDINGS = [
    ("DDG supplier-share evidence starts with a redaction correction.",
     "The model restores $14.6B of redacted multiyear masters to correct the "
     "outside-yards POP read; the applied BC supplier share remains 13%."),
    ("Submarine supplier-share evidence is broad but deliberately constrained.",
     "The 35% input is a strict non-nuclear, yard-excluded view; broader POP "
     "anchors near 52% and 49% stay sensitivity."),
    ("Only the applied shares feed headline TAM.",
     "Broader POP views support the audit record, but 13% for DDG and 35% for "
     "submarine are the TAM bridge inputs."),
]

_CALL_LEAD = "The two programs' shares are inputs to separate models; "
_CALL_BODY = "a single blended supplier-share percentage would mislead."


# ── Local helpers ────────────────────────────────────────────────────────────
def _badge(sp_id: int, x: int, cap: str, value: str, subline: str, fill: str) -> str:
    return text_box(
        sp_id, "ShareBadge", x, _BADGE_Y, _BADGE_W, _BADGE_H,
        [paragraph([run(cap, size=CAP_12PT, bold=True, color=WHITE, font=FONT)],
                   align="ctr", space_after=120),
         paragraph([run(value, size=RIBBON_KPI_18PT, bold=True, color=WHITE, font=FONT)],
                   align="ctr", space_after=90),
         paragraph([run(subline, size=FINEPRINT_8_5PT, italic=True, color=WHITE,
                        font=FONT)], align="ctr")],
        fill=fill, line_width=12_700, anchor="ctr", insets=INSETS_CARD)


def _bcell(text: str, *, fill=None, bold=False, applied=False, borders) -> dict:
    """Body cell: Program/Applied-value cells are 9pt bold; the rest 8.5pt."""
    size = LABEL_9PT if (bold or applied) else FINEPRINT_8_5PT
    return tcell(text, fill=fill, color=BLACK, bold=(bold or applied), size=size,
                 align="l", anchor="ctr", borders=borders)


def _method_table(sp_id: int) -> str:
    header = trow([
        tcell(h, color=BLACK, bold=True, size=LABEL_9PT, align="l", anchor="ctr",
              borders=_B15) for h in _HDRS
    ], h=_HDR_H)
    r1 = trow([
        tcell("DDG", fill=BLUE_1, color=BLACK, bold=True, size=LABEL_9PT, align="l",
              anchor="ctr", row_span=2, borders=_B1),
        _bcell("MYP redaction", borders=_B1),
        _bcell("13% BC supplier share", applied=True, borders=_B1),
        _bcell("Restored $14.6B multiyear masters; corrected outside-yards POP ~32.8%",
               borders=_B1),
        _bcell("13% on the non-GFE BC stream", borders=_B1),
    ], h=_ROW_H)
    r2 = trow([
        _bcell("AP/LLTM", borders=_B1),
        _bcell("85% supplier-share input on 80% ship-construction share",
               applied=True, borders=_B1),
        _bcell("Assumption-driven filtered stream", borders=_B1),
        _bcell("Additive filtered stream, $208M per year", borders=_B1),
    ], h=_ROW_H)
    r3 = trow([
        tcell("Submarine", fill=GRAY_1, color=BLACK, bold=True, size=LABEL_9PT,
              align="l", anchor="ctr", row_span=2, borders=_BN),
        _bcell("POP breadth", borders=_B1),
        _bcell("35% BC supplier share", applied=True, borders=_B1),
        _bcell("All-gated POP anchor ~52%; AP/LLTM reference ~49%", borders=_B1),
        _bcell("35% on non-nuclear BC", borders=_B1),
    ], h=_ROW_H)
    r4 = trow([
        _bcell("AP/LLTM", borders=_BN),
        _bcell("$0 additive base", applied=True, borders=_BN),
        _bcell("Gross AP is large supplier evidence", borders=_BN),
        _bcell("Not additive under the current boundary", borders=_BN),
    ], h=_ROW_H)
    return table(sp_id, "SupplierShareMethodTable", BODY_X, _TABLE_Y, _TABLE_W,
                 _TABLE_CY, col_widths=_COL_W, rows=[header, r1, r2, r3, r4])


def _commentary(sp_id: int) -> str:
    paras = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        last = i == len(_FINDINGS) - 1
        # Parent finding: bold 9.5pt, no bullet. Child evidence: 9.5pt, bulleted -
        # hierarchy via bold + bullet, not a larger parent font.
        paras.append(paragraph(
            [run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
            space_after=90))
        paras.append(paragraph(
            [run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
            bullet=True, space_after=(0 if last else 360)))
    return text_box(sp_id, "Commentary", _COMM_X, _COMM_Y, _COMM_W, _COMM_H,
                    paras, fill=None, line_color=None, anchor="t",
                    insets=_COMM_INSETS)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    badges = "".join(
        _badge(10 + i, _BADGE_X[i], cap, value, subline, fill)
        for i, (cap, value, subline, fill) in enumerate(_BADGES))
    table_xml = _method_table(20)
    commentary = _commentary(30)
    callout = text_box(
        40, "FocalCallout", BODY_X, _CALL_Y, BODY_CX, _CALL_H,
        [paragraph([
            run(_CALL_LEAD, size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
            run(_CALL_BODY, size=MESSAGE_11PT, color=WHITE, font=FONT)],
            align="ctr")],
        fill=BLUE_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)
    return badges + table_xml + commentary + callout


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
