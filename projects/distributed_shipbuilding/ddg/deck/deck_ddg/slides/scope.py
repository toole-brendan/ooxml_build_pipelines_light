"""Scope - two-column boundary ledger defining what the DDG-51 supplier TAM includes and excludes."""
from __future__ import annotations
from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_B,
    BLUE_1, BLUE_5, GRAY_1, GRAY_5,
    BLACK, WHITE, FONT,
    INSETS_NONE, INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT, CAP_12PT,
)
LAYOUT = "slideLayout4"
_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Scope"
_TAKEAWAY = "The analysis sizes non-GFE new-construction supplier work, not total DDG spend"
_SOURCES = "Sources: CRS, Navy DDG-51 and DDG-1000 Destroyer Programs, RL32109; U.S. Navy FY2027 SCN Justification Book, LI 2122; FAR 52.204-10 and 48 C.F.R. Part 45"
def _column_cap(sp_id: int, x: int, y: int, cx: int, label: str, subline: str, *, fill: str, line_w: int) -> str:
    return text_box(
        sp_id, "ScopeColumnCap", x, y, cx, 500_000,
        [
            paragraph([run(label, size=CAP_12PT, bold=True, color=WHITE, font=FONT)], align="ctr", space_after=55),
            paragraph([run(subline, size=LABEL_9PT, italic=True, color=WHITE, font=FONT)], align="ctr"),
        ],
        fill=fill, line_width=line_w, anchor="ctr", insets=INSETS_CARD,
    )
def _ledger_body(sp_id: int, x: int, y: int, cx: int, cy: int, bullets: list[list[str | tuple[str, bool]]], *, fill: str) -> str:
    paras = []
    for i, parts in enumerate(bullets):
        runs = []
        for part in parts:
            if isinstance(part, tuple):
                text, bold = part
                runs.append(run(text, size=DENSE_BODY_10PT, bold=bold, color=BLACK, font=FONT))
            else:
                runs.append(run(part, size=DENSE_BODY_10PT, color=BLACK, font=FONT))
        paras.append(paragraph(runs, bullet=True, space_after=145 if i < len(bullets) - 1 else 0))
    return text_box(
        sp_id, "ScopeColumnBody", x, y, cx, cy,
        paras, fill=fill, anchor="t", insets=INSETS_CARD,
    )
def _boundary_cue(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "BoundaryCue", x, y, cx, 320_000,
        [
            paragraph(
                [
                    run("Boundary cue: ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run("Total DDG spend to non-GFE new-construction base to supplier-addressable TAM to SAM menu", size=MESSAGE_11PT, color=BLACK, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE,
    )
def _body() -> str:
    gap = 220_000
    side = 250_000
    col_w = (BODY_CX - 2 * side - gap) // 2
    col_y = BODY_Y + 180_000
    cap_h = 500_000
    body_h = 3_050_000
    body_y = col_y + cap_h
    left_x = BODY_X + side
    right_x = left_x + col_w + gap
    in_scope = [
        [("DDG-51 Flight III", True), " and Arleigh Burke new construction"],
        [("SCN Line Item 2122", True)],
        [("Basic Construction", True), " supplier work"],
        [("AP/LLTM", True), " supplier-addressable material"],
        ["Work performed away from BIW, Ingalls, GFE prime sites, and excluded Navy-directed flows"],
    ]
    out_scope = [
        [("DDG-1000", True), " and Zumwalt"],
        ["WPN and OPN weapons procurement"],
        ["Aegis, SPY-6, VLS, Mk 45, LM2500, SEWIP, CIWS, and other GFE-heavy prime flows"],
        ["Sustainment, depot, ship repair, design-only, and MIB"],
        ["Contaminants such as IVECO Mk 110 and Thales ESSM artifacts"],
    ]
    return (
        _column_cap(10, left_x, col_y, col_w, "IN SCOPE", "sized in TAM and SAM", fill=BLUE_5, line_w=19_050)
        + _column_cap(11, right_x, col_y, col_w, "OUT OF SCOPE", "not in TAM", fill=GRAY_5, line_w=12_700)
        + _ledger_body(20, left_x, body_y, col_w, body_h, in_scope, fill=BLUE_1)
        + _ledger_body(21, right_x, body_y, col_w, body_h, out_scope, fill=GRAY_1)
        + _boundary_cue(30, BODY_X + side, body_y + body_h + 230_000, BODY_CX - 2 * side)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
