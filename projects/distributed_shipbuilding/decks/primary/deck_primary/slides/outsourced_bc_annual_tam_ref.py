"""outsourced_bc_annual_tam_ref - the self-contained native-chart reference for
the annual outsourced-BC TAM slide (deck_primary slide 3), for AI agents.

This is the flattened, single-file version of the staged chart_ref -> layers ->
data progression. One module, no import chain. It teaches, top to bottom:

  1. NATIVE CHART, not faked shapes. The chart stays a real <c:chart> part
     (slide03_chart4.xml) with its original binary .xlsb bundled, so "Edit Data"
     works. A SEMANTIC MIRROR (CHART_POINTS / CHART_STYLE / CHART_SERIES) sits
     above it so an agent can reason about the bars as data.
  2. The pinned annotation overlay is split into 8 NAMED LAYERS
     (slide03_<layer>.xml) so a layer can be located and edited on its own.
  3. The penetration layer is DATA-DRIVEN: regenerated from CHART_POINTS via
     templates lifted verbatim from the export (only id/position/text vary), so
     its % text is sourced, not transcribed.

Render path (z-stack): band-commentary table -> native chart frame -> the 8
overlay layers (7 read from files, penetration generated). Visually identical to
the verbatim port. The native chart + .xlsb are never touched.

Pinned-on-purpose: forecast_framing (80 think-cell shapes) is pure geometry with
no semantic value - it stays a pinned file forever. To make another layer
data-driven, copy the penetration pattern below (verbatim template + a data
model), and verify the regenerated layer's {name,x,y,text} set matches the file.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape as _esc

from deck_core.primitives import slide
from deck_core.charts import graphic_frame, editable_bundled_chart

LAYOUT = "slideLayout4"
_XML = Path(__file__).parent / "_chart_xml"

_ID = [9000]
def _nid() -> int:
    _ID[0] += 1
    return _ID[0]

def _read(name: str) -> str:
    return (_XML / name).read_text(encoding="utf-8")

def _read_bytes(name: str) -> bytes:
    return (_XML / name).read_bytes()


# ════════════════════════════════════════════════════════════════════════════
# 1. NATIVE CHART  — the real chart part + semantic mirror
# ════════════════════════════════════════════════════════════════════════════
CHART_NODE = dict(
    chart_xml="slide03_chart4.xml",     # native <c:chartSpace> (bundled verbatim)
    workbook="slide03_chart4.xlsb",     # original embedded workbook ("Edit Data")
    sp_id=337, name="Chart 36",
    x=646113, y=1574800, cx=11126787, cy=2470150, rId="rId2",
)
CHART_STYLE = dict(
    kind="stacked_column",          # barDir=col, grouping=stacked
    gap_width=0, overlap=100,
    y_min=0, y_max=15, y_major=5,
    major_gridlines=False,
    cat_tick_labels="none",         # FY labels are drawn in the overlay, not the axis
    units="$B per year, FY26 $",
)
PROGRAMS = {
    "ddg51":    dict(label="DDG-51",   actual_fill="accent4", forecast_fill="BEBEBE"),
    "virginia": dict(label="Virginia", actual_fill="accent3", forecast_fill="A1A1A1"),
    "columbia": dict(label="Columbia", actual_fill="accent2", forecast_fill="000000"),
}
CHART_SERIES = [
    dict(id="outsourced", row="Sheet1!$A$1:$AM$1", segment="lower",
         note="visible outsourced bar; per-point fill = program colour (forecast = grey/black)"),
    dict(id="retained",   row="Sheet1!$A$2:$AM$2", segment="upper",
         note="stacks to the FY total; its data labels carry the total text"),
]
# Mirror of chart4.xml's data cache. 27 points, stride-4 FY grid (+0 ddg51,
# +1 virginia, +2 columbia, +3 spacer). total_label / penetration are DERIVED.
CHART_POINTS = [
    dict(slot=0,  year="FY2022", program="ddg51",    outsourced=0.474365, retained=4.005805, total_label="4.5",  penetration="11%"),
    dict(slot=1,  year="FY2022", program="virginia", outsourced=1.779598, retained=5.827735, total_label="7.6",  penetration="23%"),
    dict(slot=4,  year="FY2023", program="ddg51",    outsourced=1.233632, retained=7.272376, total_label="8.5",  penetration="15%"),
    dict(slot=5,  year="FY2023", program="virginia", outsourced=1.853724, retained=5.904396, total_label="7.8",  penetration="24%"),
    dict(slot=8,  year="FY2024", program="ddg51",    outsourced=0.873987, retained=4.838037, total_label="5.7",  penetration="15%"),
    dict(slot=9,  year="FY2024", program="virginia", outsourced=3.207421, retained=8.625327, total_label="11.8", penetration="27%"),
    dict(slot=10, year="FY2024", program="columbia", outsourced=1.454273, retained=9.662091, total_label="11.1", penetration="13%"),
    dict(slot=12, year="FY2025", program="ddg51",    outsourced=1.236388, retained=6.779602, total_label="8.0",  penetration="15%"),
    dict(slot=13, year="FY2025", program="virginia", outsourced=1.847245, retained=7.843299, total_label="9.7",  penetration="19%"),
    dict(slot=16, year="FY2026", program="ddg51",    outsourced=1.929240, retained=3.776885, total_label="5.7",  penetration="34%"),
    dict(slot=17, year="FY2026", program="virginia", outsourced=1.976853, retained=8.012256, total_label="10.0", penetration="20%"),
    dict(slot=18, year="FY2026", program="columbia", outsourced=1.575149, retained=9.169168, total_label="10.7", penetration="15%"),
    dict(slot=20, year="FY2027", program="ddg51",    outsourced=0.674118, retained=3.497658, total_label="4.2",  penetration="16%"),
    dict(slot=21, year="FY2027", program="virginia", outsourced=2.961918, retained=8.246377, total_label="11.2", penetration="26%"),
    dict(slot=22, year="FY2027", program="columbia", outsourced=1.477665, retained=8.798977, total_label="10.3", penetration="14%"),
    dict(slot=24, year="FY2028", program="ddg51",    outsourced=0.589914, retained=3.275239, total_label="3.9",  penetration="15%"),
    dict(slot=25, year="FY2028", program="virginia", outsourced=2.724440, retained=8.108991, total_label="10.8", penetration="25%"),
    dict(slot=26, year="FY2028", program="columbia", outsourced=1.359418, retained=8.372177, total_label="9.7",  penetration="14%"),
    dict(slot=28, year="FY2029", program="ddg51",    outsourced=0.644852, retained=3.312022, total_label="4.0",  penetration="16%"),
    dict(slot=29, year="FY2029", program="virginia", outsourced=2.801472, retained=7.631048, total_label="10.4", penetration="27%"),
    dict(slot=30, year="FY2029", program="columbia", outsourced=1.452728, retained=8.286610, total_label="9.7",  penetration="15%"),
    dict(slot=32, year="FY2030", program="ddg51",    outsourced=1.058742, retained=5.025357, total_label="6.1",  penetration="17%"),
    dict(slot=33, year="FY2030", program="virginia", outsourced=2.689841, retained=6.691043, total_label="9.4",  penetration="29%"),
    dict(slot=34, year="FY2030", program="columbia", outsourced=1.529927, retained=8.075794, total_label="9.6",  penetration="16%"),
    dict(slot=36, year="FY2031", program="ddg51",    outsourced=1.164647, retained=5.103149, total_label="6.3",  penetration="19%"),
    dict(slot=37, year="FY2031", program="virginia", outsourced=2.919313, retained=6.615494, total_label="9.5",  penetration="31%"),
    dict(slot=38, year="FY2031", program="columbia", outsourced=1.636711, retained=7.987063, total_label="9.6",  penetration="17%"),
]

CHARTS = [editable_bundled_chart(_read(CHART_NODE["chart_xml"]),
                                 _read_bytes(CHART_NODE["workbook"]))]


# ════════════════════════════════════════════════════════════════════════════
# 2. OVERLAY  — 8 named layers (paint order). 7 are pinned files; penetration
#    is generated (see section 3). The two CHART_POINTS-linked layers carry a
#    read-only `mirrors=` cross-ref.
# ════════════════════════════════════════════════════════════════════════════
OVERLAY_PAINT_ORDER = [
    "chrome", "forecasted_chip", "forecast_framing", "fy_labels",
    "value_labels", "dollar_callouts", "legend", "penetration",
]
OVERLAY_LAYERS = {
    "chrome":           dict(src="slide03_chrome.xml", shapes=5,
                             role="breadcrumb, title, Preliminary chip, sources, units caption"),
    "forecasted_chip":  dict(src="slide03_forecasted_chip.xml", shapes=1,
                             role="'Forecasted' program chip"),
    "forecast_framing": dict(src="slide03_forecast_framing.xml", shapes=80,
                             role="think-cell retained-spend outlines + bracket connectors "
                                  "- PURE GEOMETRY, pinned forever (do not regenerate)"),
    "fy_labels":        dict(src="slide03_fy_labels.xml", shapes=10,
                             role="FY2022-FY2031 axis labels (the chart hides its own category labels)"),
    "value_labels":     dict(src="slide03_value_labels.xml", shapes=32,
                             role="bar total labels + base decimals",
                             mirrors="CHART_POINTS[i].total_label"),
    "dollar_callouts":  dict(src="slide03_dollar_callouts.xml", shapes=4,
                             role="$2.3B / $3.1B / $5.5B / $3.1B peak callouts"),
    "legend":           dict(src="slide03_legend.xml", shapes=18,
                             role="9 colour swatches + 9 labels (PROGRAMS x outsourced/est/retained)"),
    "penetration":      dict(src=None, generated=True, shapes=24,
                             role="penetration-% strip - GENERATED from CHART_POINTS (section 3)",
                             mirrors="CHART_POINTS[i].penetration"),
}


# ════════════════════════════════════════════════════════════════════════════
# 3. DATA-DRIVEN PENETRATION LAYER  — templates lifted verbatim from the export
#    (only id/off/text vary); % text sourced from CHART_POINTS, "n/a" automatic.
# ════════════════════════════════════════════════════════════════════════════
_T_OVAL = ('<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="PenOval"></p:cNvPr><p:cNvSpPr txBox="1"/>'
           '<p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="520000" cy="175000"/>'
           '</a:xfrm><a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="FFFFFF"/>'
           '</a:solidFill><a:ln w="12700"><a:solidFill><a:srgbClr val="000000"/></a:solidFill></a:ln></p:spPr>'
           '<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/><a:lstStyle/>'
           '<a:p><a:pPr algn="ctr"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc><a:buNone/></a:pPr>'
           '<a:r><a:rPr lang="en-US" sz="850" i="1"><a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
           '<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
           '<a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>')

_T_LABEL = ('<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="StripLabel"></p:cNvPr><p:cNvSpPr txBox="1"/>'
            '<p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="976921" cy="220000"/>'
            '</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
            '<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/><a:lstStyle/>'
            '<a:p><a:pPr algn="r"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc><a:buNone/></a:pPr>'
            '<a:r><a:rPr lang="en-US" sz="800" b="1" i="1"><a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
            '<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
            '<a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>')

_T_PILL = ('<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="PenPillRange"></p:cNvPr><p:cNvSpPr txBox="1"/>'
           '<p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="5104156" cy="175000"/>'
           '</a:xfrm><a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 50000"/></a:avLst>'
           '</a:prstGeom><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:ln w="12700"><a:solidFill>'
           '<a:srgbClr val="000000"/></a:solidFill></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" '
           'tIns="0" rIns="0" bIns="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"><a:lnSpc>'
           '<a:spcPct val="115000"/></a:lnSpc><a:buNone/></a:pPr><a:r><a:rPr lang="en-US" sz="850" i="1">'
           '<a:solidFill><a:srgbClr val="000000"/></a:solidFill><a:latin typeface="Arial"/><a:ea typeface="Arial"/>'
           '<a:cs typeface="Arial"/></a:rPr><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>')

_T_HEADER = ('<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="StripHeader"></p:cNvPr><p:cNvSpPr txBox="1"/>'
             '<p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="251637" cy="1322801"/>'
             '</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
             '<p:txBody><a:bodyPr vert="vert270" wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t" '
             'anchorCtr="0"/><a:lstStyle/><a:p><a:pPr algn="l"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc>'
             '<a:buNone/></a:pPr><a:r><a:rPr lang="en-US" sz="800" b="1" i="1"><a:solidFill><a:srgbClr val="000000"/>'
             '</a:solidFill><a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
             '<a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>')

_T_COLNOTE = ('<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="ColumbiaNote"></p:cNvPr><p:cNvSpPr txBox="1"/>'
              '<p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="4480560" cy="120000"/>'
              '</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
              '<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/><a:lstStyle/>'
              '<a:p><a:pPr algn="l"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc><a:buNone/></a:pPr>'
              '<a:r><a:rPr lang="en-US" sz="800" i="1"><a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
              '<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
              '<a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>')

_T_FCNOTE = ('<p:sp><p:nvSpPr><p:cNvPr id="{id}" name="ForecastNoteStrip"></p:cNvPr><p:cNvSpPr txBox="1"/>'
             '<p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="2800000" cy="120000"/>'
             '</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
             '<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/><a:lstStyle/>'
             '<a:p><a:pPr algn="ctr"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc><a:buNone/></a:pPr>'
             '<a:r><a:rPr lang="en-US" sz="800" i="1"><a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
             '<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
             '<a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>')

PEN_ROWS = [
    dict(program="ddg51",    label="DDG-51 %",   oval_y=4118005, pill="14–19% (assumed)"),
    dict(program="virginia", label="Virginia %", oval_y=4353005, pill="24–31% (assumed)"),
    dict(program="columbia", label="Columbia %", oval_y=4588005, pill="13–17% (assumed)"),
]
PEN_ACTUAL_YEARS = ["FY2022", "FY2023", "FY2024", "FY2025", "FY2026"]   # FY27-31 -> the assumed pills
PEN_COL_X = {"FY2022": 1165285, "FY2023": 2258806, "FY2024": 3352327, "FY2025": 4445849, "FY2026": 5539370}
PEN_X_OVERRIDE = {("ddg51", "FY2025"): 4434912}    # the export nudges this one oval ~0.012in left
PEN_LABEL_X = 9737
PEN_LABEL_DY = -22500            # strip label sits 22500 EMU above its oval row
PEN_PILL_X = 6512891
PEN_HEADER = dict(text="Outsourced penetration %", x=149796, y=3691687)
PEN_NOTES = [
    (_T_COLNOTE, "Note: Columbia had no hull authorized in FY22/23/25 (hull costs shown in year of authorization)", 406859, 4830373),
    (_T_FCNOTE,  "FY26/FY27 budgets known, penetration assumed.", 4965793, 4800172),
]

def _pen_pct(program: str, year: str) -> str:
    for p in CHART_POINTS:
        if p["program"] == program and p["year"] == year:
            return p["penetration"]
    return "n/a"

def _emit(tpl: str, x: int, y: int, text: str) -> str:
    return tpl.format(id=_nid(), x=x, y=y, text=_esc(text))

def _penetration() -> str:
    out = [_emit(_T_HEADER, PEN_HEADER["x"], PEN_HEADER["y"], PEN_HEADER["text"])]
    for row in PEN_ROWS:
        y = row["oval_y"]
        out.append(_emit(_T_LABEL, PEN_LABEL_X, y + PEN_LABEL_DY, row["label"]))
        out.append(_emit(_T_PILL, PEN_PILL_X, y, row["pill"]))
        for yr in PEN_ACTUAL_YEARS:
            x = PEN_X_OVERRIDE.get((row["program"], yr), PEN_COL_X[yr])
            out.append(_emit(_T_OVAL, x, y, _pen_pct(row["program"], yr)))
    for tpl, text, x, y in PEN_NOTES:
        out.append(_emit(tpl, x, y, text))
    return "".join(out)


# ════════════════════════════════════════════════════════════════════════════
# render  — band table -> native chart -> overlay layers
# ════════════════════════════════════════════════════════════════════════════
def _chart_frame() -> str:
    n = CHART_NODE
    return graphic_frame(sp_id=n["sp_id"], name=n["name"], x=n["x"], y=n["y"],
                         cx=n["cx"], cy=n["cy"], rId=n["rId"])

def _layer(name: str) -> str:
    """One overlay layer's XML - the editing handle. penetration is generated."""
    if name == "penetration":
        return _penetration()
    return _read(OVERLAY_LAYERS[name]["src"])

def _overlay() -> str:
    return "".join(_layer(g) for g in OVERLAY_PAINT_ORDER)

def _body() -> str:
    return _read("slide03_tables.xml") + _chart_frame() + _overlay()

def render() -> str:
    return slide(_body())
