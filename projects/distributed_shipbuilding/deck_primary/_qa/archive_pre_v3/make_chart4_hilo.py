#!/usr/bin/env python3
"""Derive slide03_chart4_hilo.{xml,xlsx} from the verbatim slide03_chart4.xml.

The source v2.0 chart draws each FY28-31 forecast bar as ONE gray "outsourced"
segment cached at the HIGH end of the forecast range, plus a white "retained"
segment that stacks the column to FYDP gross. This script re-splits the two
source series into TWELVE - four per vessel class, mirroring the workbook §4
think-cell scheme (workbook_consolidated/sheets/z_chart_data_outsourced_bc.py):

    "X outsourced"       FY22-27 actuals only (keeps the class accent fill)
    "X outsourced low"   FY28-31 implied low (bottom of the forecast stack)
    "X outsourced high"  FY28-31 increment (high - low), hatched fill
    "X retained spend"   ONE series across both eras -> same segment identity
                         for a class in actual and forecast years

low + increment == the old cached forecast value and retained is reused
verbatim, so every column total (and therefore all bar geometry under the
fixed 0-12 axis) is unchanged - the chrome overlay stays aligned. Per-point
data labels are harvested from the source series and reassigned by slot to
the new owning series. On the forecast LOW segments the numeric label is
replaced by a literal "low-high" range string (think-cell style <c:tx>
rich-text override, e.g. "2.6-3.3", styling copied from the label's own
defRPr) so the high end is read off the bar; the increment segment itself
gets no label - its value alone would mislead - and the bar-top gross totals
are chrome. Everything outside the two <c:ser> blocks is byte-identical.

Also derives slide03_hilo.xml from the verbatim slide03.xml chrome: in the
forecast legend group the three per-class "retained spend" chips (redundant
now that retained is ONE series per class across both eras, already in the
actual-era group) collapse into a single hatched "Outsourced upper range"
chip; everything else is untouched.

The companion .xlsx (row-oriented: series N -> Sheet1 row N+1, slots ->
columns A..AM) replaces the source 2-row .xlsb, which can no longer back the
12-series refs; the module attaches it via editable_bundled_chart(...,
embed_ext="xlsx") so Edit Data keeps working.

Deterministic: rerunning produces identical bytes. Rerun after regen_charts.sh
re-extracts the verbatim chart + chrome.
"""
from __future__ import annotations

import io
import re
import sys
import zipfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_CHART_XML_DIR = _HERE.parent / "deck_primary" / "slides" / "_chart_xml"
sys.path.insert(0, str(_HERE.parents[3]))

from deck_core.charts import (  # noqa: E402
    _EMBED_CONTENT_TYPES,
    _EMBED_ROOT_RELS,
    _EMBED_STYLES,
    _EMBED_WORKBOOK,
    _EMBED_WORKBOOK_RELS,
    _XML_DECL,
    _col_letter,
)

# ── slot map: 39 implicit categories = [DDG, Va, Col, spacer] x 10 FYs ────
_N_SLOTS = 39
_ACTUAL_SLOTS = {  # FY2022-FY2027
    "DDG-51": [0, 4, 8, 12, 16, 20],
    "Virginia": [1, 5, 9, 13, 17, 21],
    "Columbia": [2, 6, 10, 14, 18, 22],  # FY22/23/25 blank in the cache
}
_FORECAST_SLOTS = {  # FY2028-FY2031
    "DDG-51": [24, 28, 32, 36],
    "Virginia": [25, 29, 33, 37],
    "Columbia": [26, 30, 34, 38],
}
_CLASSES = ["DDG-51", "Virginia", "Columbia"]

# ── FY28-31 forecast bounds ($B, FY26 $) ──────────────────────────────────
# Verbatim from workbook §4 (z_chart_data_outsourced_bc.py:222-227,
# _*_OUTYEAR_LO_B / _*_OUTYEAR_HI_B). The HI values are asserted against the
# chart's own cached forecast points below.
_LOW = {
    "DDG-51": [0.552462556, 0.565572572, 0.869625827, 0.895882451],
    "Virginia": [2.551475393, 2.457053457, 2.20937342, 2.245625171],
    "Columbia": [1.27311354, 1.274126532, 1.256646369, 1.259008095],
}
_HIGH = {
    "DDG-51": [0.718201322, 0.735244344, 1.130513575, 1.164647186],
    "Virginia": [3.316918011, 3.194169494, 2.872185446, 2.919312723],
    "Columbia": [1.655047603, 1.656364492, 1.633640279, 1.636710524],
}

# ── fills (series-level; the source styled these via per-point overrides) ──
_LN_NOFILL = "<a:ln><a:noFill/></a:ln>"
_FILL_ACTUAL = {  # the source's actual-era dPt scheme colors
    "DDG-51": '<a:solidFill><a:schemeClr val="accent4"/></a:solidFill>',
    "Virginia": '<a:solidFill><a:schemeClr val="accent3"/></a:solidFill>',
    "Columbia": '<a:solidFill><a:schemeClr val="accent2"/></a:solidFill>',
}
_FILL_LOW = {  # the source's forecast-era grays
    "DDG-51": '<a:solidFill><a:srgbClr val="BEBEBE"/></a:solidFill>',
    "Virginia": '<a:solidFill><a:srgbClr val="BEBEBE"/></a:solidFill>',
    "Columbia": '<a:solidFill><a:srgbClr val="A1A1A1"/></a:solidFill>',
}
_FILL_HIGH = (  # estimate-range hatch, the consolidated deck's idiom
    '<a:pattFill prst="ltUpDiag">'
    '<a:fgClr><a:srgbClr val="486D82"/></a:fgClr>'
    '<a:bgClr><a:srgbClr val="FFFFFF"/></a:bgClr>'
    "</a:pattFill>"
)
_FILL_RETAINED = '<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'


def _fmt(v: float) -> str:
    """Format a derived value like the source caches (<=9 dp, no artifacts)."""
    return f"{v:.9f}".rstrip("0").rstrip(".")


def _parse_pts(ser: str) -> dict[int, str]:
    """Cached points of a series, idx -> exact value string."""
    body = re.search(
        r'<c:val><c:numRef>.*?<c:ptCount val="39"/>(.*?)</c:numCache>', ser
    ).group(1)
    return {
        int(m.group(1)): m.group(2)
        for m in re.finditer(r'<c:pt idx="(\d+)"><c:v>([^<]+)</c:v></c:pt>', body)
    }


def _parse_dlbls(ser: str) -> dict[int, str]:
    """Per-point <c:dLbl> entries of a series, idx -> element (verbatim
    except dark text promoted from tx2 to true black)."""
    return {
        int(re.search(r'<c:idx val="(\d+)"/>', d).group(1)): _black(d)
        for d in re.findall(r"<c:dLbl>.*?</c:dLbl>", ser)
    }


# ── forecast bound labels ──────────────────────────────────────────────────
# Two short numbers per forecast bar, each narrower than one bar width (so
# nothing spills onto neighbors and nothing needs a chip): the LOW keeps its
# numeric in-bar label centered in the gray low segment, and the cumulative
# HIGH floats as a literal label just ABOVE the hatched segment's top, inside
# the empty interior of the dashed retained box - it marks exactly where the
# outsourced range ends without covering any segment boundary, and no chrome
# dash passes through it. Both 10pt tx2 like the chart's other dark numbers.
_AX_MAX = 12.0          # the chart's fixed value-axis max
_HIGH_FLOAT = 0.45      # value-units from the high boundary to the label center
# true black like the chrome bar-top totals (the source's dark labels use the
# theme's gray-navy tx2 instead); white-on-dark-fill labels stay white
_BLACK = '<a:srgbClr val="000000"/>'
_RANGE_RPR_BODY = ('sz="1000" kern="1200">'
                   f"<a:solidFill>{_BLACK}</a:solidFill>"
                   '<a:latin typeface="+mn-lt"/><a:ea typeface="+mn-ea"/>'
                   '<a:cs typeface="+mn-cs"/>')


def _black(entry: str) -> str:
    """Dark chart numbers in true black, not the theme's gray-like tx2."""
    return entry.replace('<a:schemeClr val="tx2"/>', _BLACK)


def _dark(entry: str) -> str:
    """Forecast low labels read on the gray fills: recolor white->black."""
    return entry.replace('<a:schemeClr val="bg1"/>', _BLACK)


def _high_dlbl(entry: str, label: str, y_offset: float) -> str:
    """Clone a source forecast dLbl into the literal floating high-bound
    label: inserts <c:tx><c:rich> right after <c:layout> (the schema slot),
    flips showVal off so only the literal text renders, moves it up by
    y_offset (chart-area fraction, negative = up), and drops the cloned
    c16:uniqueId so ids stay unique across the part."""
    rich = ('<c:tx><c:rich><a:bodyPr wrap="none"/><a:lstStyle/><a:p>'
            f"<a:pPr><a:defRPr {_RANGE_RPR_BODY}</a:defRPr></a:pPr>"
            f'<a:r><a:rPr lang="en-US" {_RANGE_RPR_BODY}</a:rPr>'
            f"<a:t>{label}</a:t></a:r></a:p></c:rich></c:tx>")
    assert ("</c:layout>" in entry and '<c:showVal val="1"/>' in entry
            and len(re.findall(r"<c:y val=", entry)) == 1)
    out = (re.sub(r'<c:y val="[^"]*"/>', f'<c:y val="{y_offset:.6f}"/>',
                  entry, count=1)
           .replace("</c:layout>", "</c:layout>" + rich, 1)
           .replace('<c:showVal val="1"/>', '<c:showVal val="0"/>', 1))
    out, n = re.subn(r'<c:ext uri="\{C3380CC4-5D6E-409C-BE32-E72D297353CC\}"'
                     r"[^>]*>.*?</c:ext>", "", out, count=1)
    assert n == 1, "cloned dLbl kept its c16:uniqueId"
    return out


def _ser_xml(n: int, name: str, fill: str, pts: dict[int, str],
             dlbls: dict[int, str], group_tail: str) -> str:
    row = n + 1
    pts_xml = "".join(
        f'<c:pt idx="{i}"><c:v>{pts[i]}</c:v></c:pt>' for i in sorted(pts)
    )
    dlbls_xml = ""
    if dlbls:
        dlbls_xml = (
            "<c:dLbls>"
            + "".join(dlbls[i] for i in sorted(dlbls))
            + group_tail
            + "</c:dLbls>"
        )
    return (
        "<c:ser>"
        f'<c:idx val="{n}"/><c:order val="{n}"/>'
        f"<c:tx><c:v>{name}</c:v></c:tx>"
        f"<c:spPr>{fill}{_LN_NOFILL}</c:spPr>"
        '<c:invertIfNegative val="0"/>'
        f"{dlbls_xml}"
        f"<c:val><c:numRef><c:f>Sheet1!$A${row}:$AM${row}</c:f>"
        '<c:numCache><c:formatCode>General</c:formatCode>'
        f'<c:ptCount val="{_N_SLOTS}"/>{pts_xml}</c:numCache></c:numRef></c:val>'
        "</c:ser>"
    )


def _build_xlsx(rows_pts: list[dict[int, str]]) -> bytes:
    """Row-oriented Sheet1: series N -> row N+1, slot s -> column s+1."""
    rows_xml = []
    for n, pts in enumerate(rows_pts):
        r = n + 1
        cells = "".join(
            f'<c r="{_col_letter(i)}{r}"><v>{pts[i]}</v></c>' for i in sorted(pts)
        )
        rows_xml.append(f'<row r="{r}">{cells}</row>')
    sheet1 = (
        f"{_XML_DECL}\n"
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        "<sheetData>" + "".join(rows_xml) + "</sheetData></worksheet>"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _EMBED_CONTENT_TYPES)
        zf.writestr("_rels/.rels", _EMBED_ROOT_RELS)
        zf.writestr("xl/workbook.xml", _EMBED_WORKBOOK)
        zf.writestr("xl/_rels/workbook.xml.rels", _EMBED_WORKBOOK_RELS)
        zf.writestr("xl/styles.xml", _EMBED_STYLES)
        zf.writestr("xl/worksheets/sheet1.xml", sheet1)
    return buf.getvalue()


def _patch_chrome() -> None:
    """Derive slide03_hilo.xml: collapse the forecast legend group's three
    per-class "retained spend" chips (redundant - retained is now ONE series
    per class across both eras, already chipped in the actual-era group) into
    a single hatched "Outsourced upper range" chip on the middle row. The
    forecast group sits at x > 9.5in; the actual-era group is untouched."""
    src = (_CHART_XML_DIR / "slide03.xml").read_text(encoding="utf-8")
    sps = re.findall(r"<p:sp>.*?</p:sp>", src)

    def find(pred) -> str:
        hits = [s for s in sps if pred(s)]
        assert len(hits) == 1, f"expected exactly 1 matching shape, got {len(hits)}"
        return hits[0]

    def by_name(n: str) -> str:
        return find(lambda s: f'name="{n}"' in s)

    def forecast_text(t: str) -> str:  # forecast legend column at x=10204450
        return find(lambda s: f"<a:t>{t}</a:t>" in s and
                    int(re.search(r'<a:off x="(\d+)"', s).group(1)) > 9_500_000)

    out = src
    # rows 1 and 3 of the forecast retained column: swatch + text, deleted
    for sp in (by_name("Rectangle 1000"), by_name("Rectangle 1002"),
               forecast_text("Columbia retained spend"),
               forecast_text("DDG-51 retained spend")):
        assert sp in out
        out = out.replace(sp, "")
    # row 2 swatch: white sysDot retained box -> hatched, borderless like the
    # gray outsourced chips (ln copied from Rectangle 896)
    sw = by_name("Rectangle 1001")
    gray_ln = re.search(r"<a:ln w=\"19050\".*?</a:ln>",
                        by_name("Rectangle 896")).group(0)
    new_sw = (sw
              .replace('<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>',
                       _FILL_HIGH, 1)
              .replace(re.search(r"<a:ln w=\"6350\".*?</a:ln>", sw).group(0),
                       gray_ln, 1))
    assert new_sw != sw and _FILL_HIGH in new_sw
    out = out.replace(sw, new_sw)
    # row 2 text: relabel
    txt = forecast_text("Virginia retained spend")
    out = out.replace(txt, txt.replace("<a:t>Virginia retained spend</a:t>",
                                       "<a:t>Outsourced upper range</a:t>", 1))
    (_CHART_XML_DIR / "slide03_hilo.xml").write_text(out, encoding="utf-8")
    print(f"wrote slide03_hilo.xml ({len(out)} chars, legend patched)")


def main() -> None:
    src = (_CHART_XML_DIR / "slide03_chart4.xml").read_text(encoding="utf-8")
    sers = re.findall(r"<c:ser>.*?</c:ser>", src)
    assert len(sers) == 2, f"expected the verbatim 2-series chart, got {len(sers)}"
    out_pts, ret_pts = _parse_pts(sers[0]), _parse_pts(sers[1])
    out_dl, ret_dl = _parse_dlbls(sers[0]), _parse_dlbls(sers[1])
    dlbls_block = re.search(r"<c:dLbls>(.*)</c:dLbls>", sers[0]).group(1)
    group_tail = dlbls_block.rsplit("</c:dLbl>", 1)[-1]
    # inner plot-area fractions of the chart frame, from the plot area's own
    # manual layout (chrome range chips are positioned in this geometry)
    plot = tuple(float(re.search(
        rf'<c:plotArea><c:layout><c:manualLayout>.*?<c:{d} val="([^"]+)"/>',
        src).group(1)) for d in ("x", "y", "w", "h"))

    # ── reconcile the workbook bounds against the chart's own caches ──────
    for cls in _CLASSES:
        for i, slot in enumerate(_FORECAST_SLOTS[cls]):
            cached = float(out_pts[slot])
            assert abs(cached - _HIGH[cls][i]) < 1e-9, (
                f"{cls} forecast slot {slot}: cache {cached} != HI {_HIGH[cls][i]}")
            assert 0 < _LOW[cls][i] < _HIGH[cls][i]

    # ── 12 series: (name, fill, pts, dlbls) ───────────────────────────────
    rows: list[tuple[str, str, dict[int, str], dict[int, str]]] = []
    for cls in _CLASSES:  # bottom of the stack: FY22-27 actuals
        slots = [s for s in _ACTUAL_SLOTS[cls] if s in out_pts]
        rows.append((f"{cls} outsourced", _FILL_ACTUAL[cls],
                     {s: out_pts[s] for s in slots},
                     {s: out_dl[s] for s in slots if s in out_dl}))
    unit_frac = plot[3] / _AX_MAX  # chart-area fraction of one value unit
    for cls in _CLASSES:  # forecast low; numeric label, recolored dark
        rows.append((f"{cls} outsourced low", _FILL_LOW[cls],
                     {s: _fmt(_LOW[cls][i])
                      for i, s in enumerate(_FORECAST_SLOTS[cls])},
                     {s: _dark(out_dl[s])
                      for s in _FORECAST_SLOTS[cls] if s in out_dl}))
    for cls in _CLASSES:  # forecast increment; its own numeric label would
        # mislead, so it carries the literal cumulative HIGH, floated from
        # the hatch center (default) up past the high boundary
        rows.append((f"{cls} outsourced high", _FILL_HIGH,
                     {s: _fmt(_HIGH[cls][i] - _LOW[cls][i])
                      for i, s in enumerate(_FORECAST_SLOTS[cls])},
                     {s: _high_dlbl(
                          out_dl[s], f"{_HIGH[cls][i]:.1f}",
                          -((_HIGH[cls][i] - _LOW[cls][i]) / 2 + _HIGH_FLOAT)
                          * unit_frac)
                      for i, s in enumerate(_FORECAST_SLOTS[cls])
                      if s in out_dl}))
    for cls in _CLASSES:  # top of the stack: retained, ONE series both eras
        slots = [s for s in _ACTUAL_SLOTS[cls] + _FORECAST_SLOTS[cls]
                 if s in ret_pts]
        rows.append((f"{cls} retained spend", _FILL_RETAINED,
                     {s: ret_pts[s] for s in slots},
                     {s: ret_dl[s] for s in slots if s in ret_dl}))

    # ── every source point is consumed exactly once; totals unchanged ─────
    new_by_slot: dict[int, float] = {}
    for _, _, pts, _ in rows:
        for s, v in pts.items():
            new_by_slot[s] = new_by_slot.get(s, 0.0) + float(v)
    old_by_slot = {
        s: float(out_pts.get(s, 0)) + float(ret_pts.get(s, 0))
        for s in set(out_pts) | set(ret_pts)
    }
    assert set(new_by_slot) == set(old_by_slot)
    for s, total in old_by_slot.items():
        assert abs(new_by_slot[s] - total) < 1e-9, f"slot {s} total changed"
    n_labels = sum(len(dl) for _, _, _, dl in rows)
    n_forecast = sum(1 for s in out_dl if s >= 24)  # each becomes low + high
    assert n_forecast == 12, f"expected 12 forecast labels, got {n_forecast}"
    assert n_labels == len(out_dl) + len(ret_dl) + n_forecast, \
        "dropped a data label"

    new_sers = "".join(
        _ser_xml(n, name, fill, pts, dlbls, group_tail)
        for n, (name, fill, pts, dlbls) in enumerate(rows)
    )
    start, end = src.find("<c:ser>"), src.rfind("</c:ser>") + len("</c:ser>")
    out_xml = src[:start] + new_sers + src[end:]

    (_CHART_XML_DIR / "slide03_chart4_hilo.xml").write_text(out_xml, encoding="utf-8")
    xlsx = _build_xlsx([pts for _, _, pts, _ in rows])
    (_CHART_XML_DIR / "slide03_chart4_hilo.xlsx").write_bytes(xlsx)
    print(f"wrote slide03_chart4_hilo.xml ({len(out_xml)} chars, 12 series, "
          f"{n_labels} labels) + slide03_chart4_hilo.xlsx ({len(xlsx)} bytes)")

    # ── RAMPED variant (workbook §4b): NINE series - per class actuals, ONE
    # forecast chunk at the ramped high (penetration grows 1.30^(1/4)-1
    # ~6.8% p.a. from the FY22-25 avg anchored at FY27, reaching x1.30 at
    # FY31, where it ties the flat HIGH), and retained-to-gross. No low/high
    # split, no hatch, no floating literal labels - the gray chunk carries
    # the source's numeric in-bar label (recolored dark) and retained labels
    # re-render their new values. Column totals stay the cached gross, so
    # the chrome overlay fits both variants unchanged.
    def _ramped(cls: str) -> list[float]:
        return [_LOW[cls][i] * 1.30 ** ((i + 1) / 4) for i in range(4)]

    for cls in _CLASSES:
        assert abs(_ramped(cls)[3] - _HIGH[cls][3]) < 1e-8, \
            f"{cls} FY31 ramped high != flat high"

    ramp_rows: list[tuple[str, str, dict[int, str], dict[int, str]]] = []
    for cls in _CLASSES:  # FY22-27 actuals, identical to the hilo variant
        slots = [s for s in _ACTUAL_SLOTS[cls] if s in out_pts]
        ramp_rows.append((f"{cls} outsourced", _FILL_ACTUAL[cls],
                          {s: out_pts[s] for s in slots},
                          {s: out_dl[s] for s in slots if s in out_dl}))
    for cls in _CLASSES:  # single forecast chunk at the ramped high
        ramp_rows.append((f"{cls} outsourced high (ramped)", _FILL_LOW[cls],
                          {s: _fmt(_ramped(cls)[i])
                           for i, s in enumerate(_FORECAST_SLOTS[cls])},
                          {s: _dark(out_dl[s])
                           for s in _FORECAST_SLOTS[cls] if s in out_dl}))
    for cls in _CLASSES:  # retained: actual era verbatim + rest-to-gross
        pts = {s: ret_pts[s] for s in _ACTUAL_SLOTS[cls] if s in ret_pts}
        for i, s in enumerate(_FORECAST_SLOTS[cls]):
            gross = float(out_pts[s]) + float(ret_pts[s])
            pts[s] = _fmt(gross - _ramped(cls)[i])
        ramp_rows.append((f"{cls} retained spend", _FILL_RETAINED, pts,
                          {s: ret_dl[s]
                           for s in _ACTUAL_SLOTS[cls] + _FORECAST_SLOTS[cls]
                           if s in ret_dl}))

    ramp_by_slot: dict[int, float] = {}
    for _, _, pts, _ in ramp_rows:
        for s, v in pts.items():
            ramp_by_slot[s] = ramp_by_slot.get(s, 0.0) + float(v)
    assert set(ramp_by_slot) == set(old_by_slot)
    for s, total in old_by_slot.items():
        assert abs(ramp_by_slot[s] - total) < 1e-8, f"ramp slot {s} total changed"
    n_ramp_labels = sum(len(dl) for _, _, _, dl in ramp_rows)
    assert n_ramp_labels == len(out_dl) + len(ret_dl), "ramp label census off"

    ramp_sers = "".join(
        _ser_xml(n, name, fill, pts, dlbls, group_tail)
        for n, (name, fill, pts, dlbls) in enumerate(ramp_rows))
    ramp_xml = src[:start] + ramp_sers + src[end:]
    (_CHART_XML_DIR / "slide03_chart4_ramp.xml").write_text(ramp_xml, encoding="utf-8")
    ramp_xlsx = _build_xlsx([pts for _, _, pts, _ in ramp_rows])
    (_CHART_XML_DIR / "slide03_chart4_ramp.xlsx").write_bytes(ramp_xlsx)
    print(f"wrote slide03_chart4_ramp.xml ({len(ramp_xml)} chars, 9 series, "
          f"{n_ramp_labels} labels) + slide03_chart4_ramp.xlsx ({len(ramp_xlsx)} bytes)")
    _patch_chrome()


if __name__ == "__main__":
    main()
