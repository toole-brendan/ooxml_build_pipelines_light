"""Bucket rules and supplier evidence - define description-led SAM bucket classification logic."""
from __future__ import annotations
# Implementation assumption: top-vendor names are not in the A6 spec, so the
# supplier-evidence column points to Bucket Evidence rather than inferring names.
from deck_core.primitives import (
    slide,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    sources_line,
    run,
    paragraph,
    text_box,
    house_table,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_B,
    GRAY_1,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_MESSAGE,
    LABEL_9PT,
    FINEPRINT_8_5PT,
    DENSE_BODY_10PT,
    CHART_TITLE_10PT,
)
from deck_core.text_metrics import estimate_row_heights
LAYOUT = "slideLayout4"
_SECTION = "Appendix"
_TOPIC = "Bucket Rules"
_TAKEAWAY = "Description-led classification maps subawards into seven target work types"
_SOURCES = "Sources: SAM.gov Acquisition Subaward Reporting Public API; SAM.gov Entity Management API; FAR 52.204-10"
_BREADCRUMB_TOPIC = "Bucket Rules"
_LABEL_Y = BODY_Y + 30_000
_TABLE_Y = BODY_Y + 410_000
_ROWS = [
    ["Bucket", "Description cues", "Scenario use", "Supplier evidence", "Evidence limits"],
    ["Structural fabrication and pre-outfit", "hull sections; structural metal; deckhouse; pre-outfit modules", "Metal; Modular; Broad", "Bucket Evidence top vendors", "mixed fabrication and module descriptions"],
    ["Machining", "machine shops; gears; shafts; bearings; power transmission", "Metal; HM&E; Broad", "Bucket Evidence top vendors", "overlaps metal and HM&E by design"],
    ["Castings and forgings", "forgings; foundries; cast components", "Metal; Broad", "Bucket Evidence top vendors", "small bucket; do not over-interpret precision"],
    ["Piping, valves, and pumps", "valves; pumps; manifolds; piping; fittings; hydraulics", "HM&E; Broad", "Bucket Evidence top vendors", "HM&E descriptions can be ambiguous"],
    ["Electrical and power", "switchgear; cable; power distribution; generators; motors", "Electrical and power; Broad", "Bucket Evidence top vendors", "screen GFE-adjacent electronics"],
    ["HVAC and ventilation", "air conditioning; chilled water; ventilation; AHUs; ductwork", "HM&E; Broad", "Bucket Evidence top vendors", "sparse records and mixed services"],
    ["Coatings and insulation", "coatings; paint; deck covering; insulation; non-skid", "Modular; Broad", "Bucket Evidence top vendors", "low-dollar bucket; description-led"],
    ["Unbucketed and ambiguous", "parent unknown; GFE-adjacent specialty; no clean cue", "Residual, not broad SAM", "Keep explicit", "evidence ambiguity, not zero market"],
]
_COL_W = [2_100_000, 2_730_000, 1_700_000, 1_900_000, 2_852_362]
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=9.0, header_size_pt=9.0)
_TABLE_H = sum(_ROW_H)
_RAIL_Y = min(_TABLE_Y + _TABLE_H + 80_000, BODY_B - 690_000)
# Appendix evidence ledger -> rule skin. Structure carried by the bold first
# column + rule header; only the residual row keeps a muted fill (the old dark
# header and per-column BLUE_1/GRAY_1 fills are dropped).
_RESIDUAL = len(_ROWS) - 1
_CELL_FILLS = {(_RESIDUAL, ci): GRAY_1 for ci in range(len(_COL_W))}
def _rules_table() -> str:
    return house_table(
        20,
        "BucketRulesTable",
        BODY_X,
        _TABLE_Y,
        _COL_W,
        _ROWS,
        row_h=_ROW_H,
        table_skin="rule",
        aligns=["l", "l", "l", "l", "l"],
        size=LABEL_9PT,
        cell_fills=_CELL_FILLS,
    )
def _commentary_rail() -> str:
    return text_box(
        80,
        "BucketRulesCommentary",
        BODY_X,
        _RAIL_Y,
        BODY_CX,
        880_000,
        [
            paragraph(
                [run("Rules: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("SAM scenarios are work-type menus selected from TAM.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
                space_after=80,
            ),
            paragraph(
                [run("Overlap: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("Some buckets appear in more than one scenario, so scenarios are not additive.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
                space_after=80,
            ),
            paragraph(
                [run("Residual: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("Unbucketed and ambiguous remains visible and should not be forced into a named bucket.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
                space_after=80,
            ),
            paragraph(
                [run("Supplier evidence: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("Top-vendor rows should come from Bucket Evidence or Vendors tie-outs, not inference.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
                space_after=80,
            ),
            paragraph(
                [run("Use: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("This is not SOM and no capture probability is applied.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
            ),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        num_cols=2,
        insets=INSETS_MESSAGE,
    )
def _body() -> str:
    label = text_box(
        10,
        "ExhibitTitle",
        BODY_X,
        _LABEL_Y,
        BODY_CX,
        340_000,
        [
            paragraph([run("Bucket rules and evidence limits", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)]),
            paragraph([run("Scale: TAM basis ~$573M per year; seven named buckets ~$327M per year (57.1%); unbucketed and ambiguous residual ~$246M per year (42.9%).", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)]),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
    return label + _rules_table() + _commentary_rail()
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
