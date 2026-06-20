"""data_reference - a plain methodology backup slide: scope, taxonomy, raw fields.

INTENT: a fill-free reference exhibit for the methodology discussion - three
stacked native tables, no cell fills (table_skin="rule", horizontal rules only):

  1. In-scope PIIDs  - the full prime new-construction pull scope, grouped by
                       platform (SSN / SSBN / DDG).
  2. Work types      - the seven mutually-exclusive work-type buckets, their
                       NAICS-4 crosswalk, and a one-line definition each.
  3. Award field     - a sampling of raw FSRS subaward records showing the NATIVE
     sample            pull fields the analysis rides on; program / family / work
                       type are classified downstream, not part of the pull.

Static content (the deck slides are self-contained); the live screens/levers live
in the Award Analysis workbook.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb,
    prelim_chip,
    title_placeholder,
    house_table,
    sources_line,
)
from deck_core.style import BODY_X, BODY_Y, BODY_CX, DENSE_BODY_10PT  # noqa: F401
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers the page

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION = "Award Analysis"
_TOPIC = "Data Reference"
_TAKEAWAY = ("Scope PIIDs, the seven work-type buckets, and the native subaward "
             "fields the analysis reads.")

_SIZE = 800              # 8pt - dense backup exhibit
_GAP = 137_160           # ~0.15in between the stacked tables
_MIN_ROW = 152_400       # let one-line rows sit ~0.23in instead of the 0.30in floor

# ── 1. In-scope PIIDs (full pull scope, grouped by platform) ─────────────────
_PIID_ROWS = [
    ["Platform", "Prime new-construction contract PIIDs"],
    ["SSN · Virginia",
     "N0002417C2100, N0002412C2115, N0002416C2111, N0002424C2110, "
     "N0002421C4106, N0002421C4111, N0002409C2104, N0002410C2118, "
     "N0002424C2114, N0002410C6266"],
    ["SSBN · Columbia",
     "N0002417C2117, N0002413C2128, N0002419C2115, N0002419C2114, "
     "N0002411C2109"],
    ["DDG · DDG-51",
     "N0002418C2307, N0002413C2307, N0002423C2307, N0002411C2307, "
     "N0002411C2309, N0002419C4452, N0002419C2322, N0002413C2305, "
     "N0002414C4313, N0002418C2305, N0002412C2312, N0002423C2305, "
     "N0002402C2303, N0002406C2303, N0002411C2306, N0002411C2305, "
     "N0002412C4311, N0002409C2302, N0002418C2313, N0002412C2313, "
     "N0002403C2306, N0002418C4451, N0002424C2313, N0002402C2304"],
]
_PIID_COLW = [1_500_000, BODY_CX - 1_500_000]

# ── 2. Work types (bucket + NAICS-4 crosswalk + definition) ──────────────────
_WT_ROWS = [
    ["Work type", "NAICS-4", "What it covers"],
    ["Structural fabrication & modules", "3323, 3324, 3366, 3369",
     "hull sections, fabricated structural metal, pre-outfit modules"],
    ["Machining / mechanical / propulsion", "3327, 3336",
     "machine shops, precision machining, mechanical power transmission, "
     "propulsion machinery"],
    ["Castings & forgings", "3312, 3315, 3321",
     "iron / steel forging, steel foundries, cast components"],
    ["Piping / fluid handling", "3329, 3339, 4235",
     "industrial valves, pumps, measuring / dispensing, pipe & fittings"],
    ["Electrical power / distribution / generation", "3353, 3359",
     "switchgear, transformers, turbine generators, motors, ship power "
     "distribution"],
    ["HVAC / ventilation / chilled water", "3334",
     "air-conditioning, warm-air heating, shipboard ventilation"],
    ["Coatings / insulation / decking", "3252, 3259, 3262",
     "rubber / synthetic, composites, coatings & insulation"],
]
_WT_COLW = [3_100_000, 1_250_000, BODY_CX - 3_100_000 - 1_250_000]

# ── 3. Award field sample (NATIVE FSRS subaward pull fields) ─────────────────
_AE_ROWS = [
    ["PIID", "Subawardee", "Subawardee UEI", "Award date", "$M", "NAICS-4",
     "Report ID"],
    ["N0002412C2115", "BAKER SHEET METAL CORPORATION", "RYRLL49HWN65",
     "2016-02-03", "0.085", "3323", "20692413"],
    ["N0002412C2115", "ARNOLD MAGNETICS CORPORATION", "RK6GKSXPC8W7",
     "2016-02-03", "0.134", "3359", "20692322"],
    ["N0002413C2128", "SCOT FORGE COMPANY", "N1PJDANWUJ61",
     "2016-02-18", "1.058", "3321", "20699650"],
    ["N0002411C2307", "WESTLAND TECHNOLOGIES, INC.", "HMBSX7Z72UK4",
     "2013-05-09", "0.106", "3262", "20684452"],
]
_AE_COLW = [1_500_000, 3_050_000, 1_500_000, 1_250_000, 850_000, 1_000_000,
            BODY_CX - 1_500_000 - 3_050_000 - 1_500_000 - 1_250_000
            - 850_000 - 1_000_000]
_AE_ALIGN = ["l", "l", "l", "ctr", "r", "ctr", "l"]

_SOURCE = ("FSRS / SAM.gov first-tier subaward pull, prime new-construction "
           "PIIDs; fields shown are native to the pull. Program, family and work "
           "type are classified downstream from the vendor, not the award text.")


def _body() -> str:
    """Three stacked, fill-free native tables, content-fit row heights."""
    rh1 = estimate_row_heights(_PIID_ROWS, _PIID_COLW,
                               size_pt=_SIZE / 100.0, min_row_h=_MIN_ROW)
    rh2 = estimate_row_heights(_WT_ROWS, _WT_COLW,
                               size_pt=_SIZE / 100.0, min_row_h=_MIN_ROW)
    rh3 = estimate_row_heights(_AE_ROWS, _AE_COLW,
                               size_pt=_SIZE / 100.0, min_row_h=_MIN_ROW)

    y1 = BODY_Y
    y2 = y1 + sum(rh1) + _GAP
    y3 = y2 + sum(rh2) + _GAP

    return (
        house_table(41, "data_ref_piids", BODY_X, y1, _PIID_COLW, _PIID_ROWS,
                    row_h=rh1, table_skin="rule", aligns=["l", "l"],
                    anchor="t", size=_SIZE)
        + house_table(42, "data_ref_worktypes", BODY_X, y2, _WT_COLW, _WT_ROWS,
                      row_h=rh2, table_skin="rule", aligns=["l", "ctr", "l"],
                      anchor="t", size=_SIZE)
        + house_table(43, "data_ref_award_fields", BODY_X, y3, _AE_COLW, _AE_ROWS,
                      row_h=rh3, table_skin="rule", aligns=_AE_ALIGN,
                      anchor="t", size=_SIZE)
    )


def render() -> str:
    """Assemble chrome + body into one <p:sld>, in locked paint order."""
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCE)
    )
