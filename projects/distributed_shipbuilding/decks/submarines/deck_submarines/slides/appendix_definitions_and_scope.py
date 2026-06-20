"""definitions_and_scope - define model terms and boundary guardrails for diligence readers."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.style import *
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

# --- chrome (unchanged from the original main module) ---
_SECTION = "Appendix"
_TOPIC = "Definitions and Scope"
_TAKEAWAY = "Key terms define the model boundary and prevent double counting"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books; (2) FAR 52.204-10; (3) FAR Part 45"


def _txt(text: str, *, size: int = DENSE_BODY_10PT, bold: bool = False,
         italic: bool = False, color: str = BLACK, align: str = "l") -> str:
    return paragraph([run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)], align=align)


def _note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str,
          *, size: int = FINEPRINT_8_5PT, bold_lead: str | None = None,
          italic: bool = True, align: str = "ctr") -> str:
    if bold_lead and text.startswith(bold_lead):
        rest = text[len(bold_lead):].lstrip()
        paras = [paragraph([
            run(bold_lead, size=size, bold=True, italic=False, color=BLACK, font=FONT),
            run((" " + rest) if rest else "", size=size, italic=italic, color=BLACK, font=FONT),
        ], align=align)]
    else:
        paras = [_txt(text, size=size, italic=italic, color=BLACK, align=align)]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=None, line_color=None,
                    insets=INSETS_NONE, anchor="ctr")


def _widths(total: int, ratios: list[float]) -> list[int]:
    s = float(sum(ratios))
    vals = [int(total * r / s) for r in ratios]
    vals[-1] += total - sum(vals)
    return vals


_ROWS = [
    ["Term", "Model role", "Treatment", "Guardrail"],
    ["TAM", "Non-GFE, non-SIB new-construction supplier opportunity", "In model", "Inside P-5c Basic Construction; opportunity ceiling, not forecast"],
    ["SAM", "Portion of TAM in targeted work-type buckets", "In model", "Scenario menu, not capture share or SOM"],
    ["Basic Construction", "P-5c construction-contract denominator (GFE-free)", "In model", "Not total ship cost"],
    ["GFE and GFP", "Government-furnished equipment and property", "Excluded", "Do not add to component TAM"],
    ["SIB", "Submarine industrial base capacity grants and workforce funding", "Excluded", "Context only; not current component delivery"],
    ["AP/LLTM", "Advance procurement and long-lead-time material reference stream", "Reference", "Additive base = $0; already inside Basic Construction"],
    ["FFATA and FSRS", "First-tier subaward visibility under FAR 52.204-10", "Evidence", "Named-vendor floor, not the full supplier layer"],
    ["POP", "Place-of-performance evidence", "Evidence", "Drives the supplier coefficient"],
]


def _body() -> str:
    out = []
    out.append(_note(10, "Setup", BODY_X, BODY_Y, BODY_CX, 260_000,
        "Scope anchor: these definitions mirror the model's Methodology boundary; they are an interpretation aid, not a new boundary.",
        size=DENSE_BODY_10PT, bold_lead="Scope anchor:", italic=False, align="l"))
    table_y = BODY_Y + 340_000
    guard_y = BODY_B - 530_000
    col_w = _widths(BODY_CX, [1.2, 2.6, 1.4, 2.7])
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=9.0, header_size_pt=9.0, min_row_h=274_320)
    fills = {(1, 0): BLUE_1, (2, 0): BLUE_1, (3, 0): BLUE_1, (4, 0): GRAY_2, (5, 0): GRAY_2, (6, 0): GRAY_1, (7, 0): GRAY_1, (8, 0): GRAY_1}
    bold = {(r, 0): True for r in range(1, 9)}
    out.append(house_table(20, "GlossaryMatrix", BODY_X, table_y, col_w, _ROWS, row_h=row_h, table_skin="dark", size=900,
                           aligns=["l", "l", "l", "l"], cell_fills=fills, cell_bold=bold))
    out.append(text_box(30, "Guardrail", BODY_X, guard_y, BODY_CX, 460_000,
        [paragraph([run("NO SOM IS MODELED. ", size=CAP_12PT, bold=True, color=BLACK, font=FONT),
                    run("SAM is a scenario menu, not capture share or revenue forecast. AP/LLTM additive base = $0.", size=MESSAGE_11PT, color=BLACK, font=FONT)], align="ctr")],
        fill=GRAY_2, line_color=BLACK, line_width=19_050, insets=INSETS_MESSAGE, anchor="ctr"))
    return "".join(out)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
