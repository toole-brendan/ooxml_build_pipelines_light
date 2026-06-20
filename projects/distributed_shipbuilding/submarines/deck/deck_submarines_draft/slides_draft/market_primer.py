from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table, connector,
)
from deck_core.style import *

LAYOUT = "slideLayout4"

GAP = 91_440
TITLE_BAND_H = 190_000
NOTE_H = 360_000
CAVEAT_H = 520_000


def _txt(text: str, *, size: int = DENSE_BODY_10PT, bold: bool = False,
         italic: bool = False, color: str = DK, align: str = "l") -> str:
    return paragraph([run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)], align=align)


def _line(lead: str, body: str = "", *, lead_size: int = DENSE_BODY_10PT,
          body_size: int = LABEL_9PT, lead_color: str = DK, body_color: str = DK,
          align: str = "l", space_after: int = 0, bullet: bool = False,
          italic_body: bool = False) -> str:
    runs = [run(lead, size=lead_size, bold=True, color=lead_color, font=FONT)]
    if body:
        runs.append(run(" " + body, size=body_size, italic=italic_body, color=body_color, font=FONT))
    return paragraph(runs, align=align, space_after=space_after, bullet=bullet)


def _note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, text: str,
          *, size: int = FINEPRINT_8_5PT, bold_lead: str | None = None,
          italic: bool = True, align: str = "ctr") -> str:
    if bold_lead and text.startswith(bold_lead):
        rest = text[len(bold_lead):].lstrip()
        paras = [paragraph([
            run(bold_lead, size=size, bold=True, italic=False, color=DK, font=FONT),
            run((" " + rest) if rest else "", size=size, italic=italic, color=DK, font=FONT),
        ], align=align)]
    else:
        paras = [_txt(text, size=size, italic=italic, color=DK, align=align)]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=None, line_color=None,
                    insets=INSETS_NONE, anchor="ctr")


def _card(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, title: str,
          lines: list[str], *, fill: str = BLUE_1, color: str = DK,
          line_color=GRAY_3, line_width: int = 12_700,
          title_size: int = CAP_12PT, body_size: int = DENSE_BODY_10PT,
          title_align: str = "ctr", body_bullets: bool = False,
          insets=INSETS_CARD, anchor: str = "t") -> str:
    paras = [_txt(title, size=title_size, bold=True, color=color, align=title_align)]
    for i, line in enumerate(lines):
        paras.append(_txt(line, size=body_size, color=color, align="l"))
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=line_color,
                    line_width=line_width, insets=insets, anchor=anchor)


def _kpi(sp_id: int, name: str, x: int, y: int, cx: int, cy: int,
         label: str, value: str, qualifier: str, *, fill: str, color: str,
         line_color=BLACK, line_width: int = 19_050, value_size: int = HERO_32PT,
         label_size: int = CAP_12PT, qualifier_size: int = LABEL_9PT,
         insets=INSETS_ANSWER_CARD) -> str:
    paras = [
        _txt(label, size=label_size, bold=True, color=color, align="ctr"),
        _txt(value, size=value_size, bold=True, color=color, align="ctr"),
        _txt(qualifier, size=qualifier_size, italic=True, color=color, align="ctr"),
    ]
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill, line_color=line_color,
                    line_width=line_width, insets=insets, anchor="ctr")


def _chart_title(sp_id: int, text: str, x: int, y: int, cx: int) -> str:
    return text_box(sp_id, "ChartTitle", x, y, cx, TITLE_BAND_H,
                    [_txt(text, size=CHART_TITLE_10PT, italic=True, color=DK, align="l")],
                    fill=None, line_color=None, insets=INSETS_NONE, anchor="t")


def _widths(total: int, ratios: list[float]) -> list[int]:
    s = float(sum(ratios))
    vals = [int(total * r / s) for r in ratios]
    vals[-1] += total - sum(vals)
    return vals


def _grid_x(n: int, *, start: int = BODY_X, total: int = BODY_CX, gap: int = GAP):
    w = (total - (n - 1) * gap) // n
    return [start + i * (w + gap) for i in range(n)], w


def _grid_y(n: int, *, start: int = BODY_Y, total: int = BODY_CY, gap: int = GAP):
    h = (total - (n - 1) * gap) // n
    return [start + i * (h + gap) for i in range(n)], h


def _render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )

render = _render


_SECTION = "Market and Scope"
_TOPIC = "Ecosystem primer"
_TAKEAWAY = "Submarine construction is a layered procurement ecosystem"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibit P-5c; (2) General Dynamics Corporation FY2021 Form 10-K; (3) GAO-25-106286"


def _body() -> str:
    out = []
    thesis_h = 380_000
    thesis_y = BODY_Y
    node_y = BODY_Y + 600_000
    node_h = 850_000
    second_y = node_y + node_h + 500_000
    tag_y = BODY_Y + 3_080_000
    tag_h = 520_000
    legend_y = BODY_B - 360_000

    navy_x, navy_w = BODY_X, 2_050_000
    gdeb_x, gdeb_w = BODY_X + 2_950_000, 2_820_000
    supplier_x, supplier_w = BODY_X + 6_700_000, 3_600_000
    hii_x, hii_w = gdeb_x + 200_000, 2_650_000
    bucket_x, bucket_w = supplier_x + 250_000, 3_200_000

    # Connectors first so they paint behind nodes.
    axis_y = node_y + node_h // 2
    out.append(connector(80, "NavyToGDEB", navy_x + navy_w, axis_y, gdeb_x - (navy_x + navy_w), 0,
                         color=BLACK, width=12_700, arrow=True))
    out.append(connector(81, "GDEBToSupplier", gdeb_x + gdeb_w, axis_y, supplier_x - (gdeb_x + gdeb_w), 0,
                         color=BLACK, width=12_700, arrow=True))
    out.append(connector(82, "GDEBToHII", gdeb_x + gdeb_w // 2, node_y + node_h, 0, second_y - (node_y + node_h),
                         color=BLACK, width=9_525, arrow=True))
    out.append(connector(83, "SupplierToBuckets", supplier_x + supplier_w // 2, node_y + node_h, 0, second_y - (node_y + node_h),
                         color=BLACK, width=9_525, arrow=True))
    out.append(connector(84, "NavyToGFE", navy_x + navy_w // 2, node_y + node_h, 0, tag_y - (node_y + node_h),
                         color=BLACK, width=9_525, arrow=True))

    out.append(text_box(10, "Thesis", BODY_X, thesis_y, BODY_CX, thesis_h,
        [_txt("We size the supplier-addressable component layer inside Basic Construction, not total ship cost.", size=MESSAGE_11PT, bold=True, color=DK, align="ctr")],
        fill=BLUE_1, line_color=GRAY_3, insets=INSETS_MESSAGE, anchor="ctr"))
    out.append(_card(11, "NavyNode", navy_x, node_y, navy_w, node_h, "NAVY and SCN budget authority",
        ["P-5c Total Ship Estimate", "P-10 AP and LLTM timing"], fill=GRAY_1, body_size=FINEPRINT_8_5PT))
    out.append(_card(12, "GDEBNode", gdeb_x, node_y, gdeb_w, node_h, "GDEB prime construction contracts",
        ["Basic Construction base", "Prime of record for Virginia and Columbia"], fill=BLUE_1, body_size=FINEPRINT_8_5PT))
    out.append(_card(13, "SupplierNode", supplier_x, node_y, supplier_w, node_h, "COUNTED SUPPLIER LAYER",
        ["Non-nuclear components and subcontracts", "In TAM and SAM candidate"], fill=BLUE_5, color=WHITE, line_color=BLACK, line_width=19_050,
        title_size=CAP_12PT, body_size=DENSE_BODY_10PT, insets=INSETS_ANSWER_CARD, anchor="ctr"))
    out.append(_card(14, "HIINode", hii_x, second_y, hii_w, 720_000, "HII Newport News",
        ["Team-build workshare via GDEB prime", "Context and yard layer"], fill=GRAY_1, body_size=FINEPRINT_8_5PT))
    out.append(_card(15, "BucketNode", bucket_x, second_y, bucket_w, 720_000, "Work-type buckets",
        ["Structural, electrical, piping", "machining, castings, HVAC, coatings"], fill=BLUE_1, body_size=FINEPRINT_8_5PT))

    xs, tag_w = _grid_x(4, start=BODY_X, total=BODY_CX, gap=GAP)
    tags = [
        ("GFE and GFP", "Combat systems, sonar, weapons", "Excluded"),
        ("Nuclear and BPMI", "Reactor plant", "Excluded"),
        ("SIB capacity flows", "Grants and BlueForge-type funding", "Excluded"),
        ("Depot and sustainment", "Overhauls and maintenance", "Excluded"),
    ]
    for i, (title, a, b) in enumerate(tags):
        out.append(_card(20+i, f"ExclusionTag{i+1}", xs[i], tag_y, tag_w, tag_h, title, [a, b],
                         fill=GRAY_2, title_size=LABEL_9PT, body_size=FINEPRINT_8_5PT))
    out.append(_note(30, "Legend", BODY_X, legend_y, BODY_CX, 260_000,
        "Legend: dark blue is the counted sizing path; light blue is related component logic; gray is context or excluded lanes.",
        size=FINEPRINT_8_5PT, italic=True, align="ctr"))
    return "".join(out)
