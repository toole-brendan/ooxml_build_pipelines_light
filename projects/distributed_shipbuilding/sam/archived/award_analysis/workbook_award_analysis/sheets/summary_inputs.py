"""summary_inputs - the "Assumptions" tab: the workbook's live control surface.

The editable knobs the downstream screens read, plus the displayed (read-only)
classification reference:
  §1 Scope            - source / window / programs / as-of (descriptive).
  §2 Thresholds       - LIVE blue controls: concentration cutoff (top-1 share)
                        and the multi-source vendor minimum.
  §3 Time windows     - LIVE blue controls: as-of date, periodic horizon
                        (months), recent-window length N (years) and the
                        derived recent-FY cutoff (=2026-N+1) the window masks
                        compare against; plus the award-wave clustering window
                        (90 days) and the §3b sensitivity windows, now all LIVE
                        controls - the workbook re-clusters award waves live from
                        the raw award dates (Event Dates), so changing a window
                        re-counts the waves with no extract re-run.
  §4 Work type map    - read-only: the 7 work-type buckets + NAICS-4 crosswalk
                        (display only; classification runs upstream in the
                        research extract scripts).
  §5 Vendor overrides - read-only: the vendor-name -> bucket overrides.

Promoted accessors (cell-ref strings the consumer screens embed):
  input_conc_threshold_cell() - top-1 concentration cutoff (Concentration).
  input_multisource_cell()    - multi-source vendor minimum (Supplier Lanes).
  input_asof_cell()           - as-of date serial (Periodic Sourcing).
  input_horizon_cell()        - periodic horizon months (Periodic Sourcing).
  input_recent_fy_cell()      - the DERIVED recent-FY cutoff (Lane Vendor FY
                                window masks; the recent/prior split driver).
  input_wave_window_ref()     - the award-wave clustering window cell (days); now
                                a LIVE control (Event Dates re-clusters off it).
                                Name kept for back-compat with its callers.
  input_periodic_maxdur_cell(),    §2b cadence-applicability knobs: a wave longer
  input_ratio_cap_cell(),          than the max duration (or span/cadence ratio
  input_strong_minwaves_cell(),    over the cap) reads Continuous, not periodic;
  input_strong_cvcap_cell()        min waves + gap-CV cap gate Strong confidence.
  input_alwayson_materiality_cell() - recent-$M floor for an always-on opening
                                (Continuous Sourcing).
  input_active_lookback_cell(),    active-now gate: a continuous lane is only an
  input_active_minrec_cell(),      OPENING if it is still buying at the as-of date
  input_active_mindollar_cell()    (recent last award within the lookback, or
                                last-365d records / $M over the minimums).

This module imports only _taxonomy / _cuts / _widths / _layout / _tabs /
workbook_core - no sheet dependency, so it import-resolves before the screens
that read its accessors (no cycle).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_INT_INPUT, S_NUM_INPUT, S_PCT_INPUT, S_DATE_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import BUCKET_NAME, date_serial
from workbook_award_analysis.sheets._taxonomy import (
    BUCKETS, NAICS4_BUCKET, VENDOR_BUCKET_OVERRIDES,
)
from workbook_award_analysis.sheets._widths import header_styles
from workbook_award_analysis.sheets._tabs import TAB_INPUTS

_GROUP = "inputs"
_TAB = TAB_INPUTS
_NCOLS = 3                                   # content columns B, C, D
_MAX_FY = 2026                               # the corpus' latest FY (cutoff anchor)


def _codes_by_bucket() -> dict:
    """Invert NAICS4_BUCKET -> {bucket: sorted NAICS-4 codes}."""
    out: dict[str, list[str]] = {}
    for naics, b in NAICS4_BUCKET.items():
        out.setdefault(b, []).append(naics)
    return {b: sorted(v) for b, v in out.items()}


def _make_inputs():
    pos: dict[str, int] = {}
    codes = _codes_by_bucket()

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 - Scope
    c.banner("§1 - Scope", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Source", "FSRS reported subaward records (supplier role)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Window", "≤FY12 through FY26 (subaward action FY; FY26 partial)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Programs", "Virginia, Columbia, DDG-51"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["As of", "2026-05-22 (latest reported award; see §3)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 - Thresholds  (LIVE controls)
    c.banner("§2 - Thresholds", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    pos["conc"] = c.write(
        ["Concentration cutoff (top-1 share)", 0.75],
        styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    pos["multi"] = c.write(
        ["Multi-source vendor minimum", 2],
        styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    c.blank(2)

    # §2b - Cadence applicability  (LIVE controls; periodic vs continuous split)
    c.banner("§2b - Cadence applicability", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["A lane gets a dated sourcing forecast only when its award waves are "
             "discrete (periodic). Continuously-active lanes - one wave chains "
             "for years - are routed to Continuous Sourcing instead of a spurious "
             "next-wave date. These knobs set that split and feed the live "
             "Sourcing mode / Cadence applicable formulas."],
            styles=[S_DEFAULT], outline_level=1)
    pos["pmax"] = c.write(
        ["Periodic max wave duration (days)", 365],
        styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    pos["ratio"] = c.write(
        ["Span/cadence ratio cap", 1.25],
        styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    pos["strongn"] = c.write(
        ["Strong-periodic min waves", 3],
        styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    pos["cvcap"] = c.write(
        ["Strong-periodic gap-CV cap", 0.60],
        styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    pos["mater"] = c.write(
        ["Always-on materiality (recent $M)", 50],
        styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    # active-now gate: a continuous lane is only an OPENING if it is still buying
    # at the as-of date (recent records OR a recent last award). Without this a
    # structurally-continuous lane that went quiet still reads "always-on".
    pos["actlook"] = c.write(
        ["Continuous active lookback (days)", 365],
        styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    pos["actrec"] = c.write(
        ["Continuous active minimum records (last 365d)", 1],
        styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    pos["actdol"] = c.write(
        ["Continuous active minimum $M (last 365d)", 0],
        styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    c.blank(2)

    # §3 - Time windows  (LIVE controls + derived cutoff)
    c.banner("§3 - Time windows", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    pos["asof"] = c.write(
        ["As-of date (latest reported award)", date_serial("2026-05-22")],
        styles=[S_DEFAULT, S_DATE_INPUT], outline_level=1)
    pos["horizon"] = c.write(
        ["Periodic horizon (months)", 12],
        styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    pos["n"] = c.write(
        ["Recent window length (years)", 5],
        styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    # Derived: the first FY counted as "recent". General format (S_DEFAULT)
    # renders a fiscal year without a thousands comma; the window masks compare
    # the FY array constant against this cell.
    pos["cut"] = c.write(
        ["Recent-FY cutoff (first recent FY)", f"=2026-C{pos['n']}+1"],
        styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    # LIVE control now: the workbook re-clusters award waves from raw award dates
    # (the Event Dates leaf flags a wave start wherever no earlier award in the
    # lane falls within this window), so changing it re-derives the wave counts
    # live - no extract re-run needed.
    pos["wave_window"] = c.write(
        ["Clustering window (days)", 90],
        styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    c.blank(2)

    # §3b - Sensitivity windows  (LIVE; Wave Sensitivity re-clusters at each)
    c.banner("§3b - Sensitivity windows", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Wave Sensitivity re-clusters the award dates at each of these "
             "windows (the 90-day column reuses the production clustering window "
             "above). Change one to test how robust a lane's wave count is to the "
             "window choice - the counts recompute live from Event Dates."],
            styles=[S_DEFAULT], outline_level=1)
    pos["sens45"] = c.write(["Sensitivity window A (days)", 45],
                            styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    pos["sens60"] = c.write(["Sensitivity window B (days)", 60],
                            styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    pos["sens120"] = c.write(["Sensitivity window C (days)", 120],
                             styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    pos["sens180"] = c.write(["Sensitivity window D (days)", 180],
                             styles=[S_DEFAULT, S_INT_INPUT], outline_level=1)
    c.blank(2)

    # §4 - Work type map  (read-only reference)
    c.banner("§4 - Work type map", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Classification runs upstream in the extract scripts; shown for "
             "reference."], styles=[S_DEFAULT], outline_level=1)
    wt_hdr = ["Work type", "NAICS-4", "Definition"]
    c.write(wt_hdr, styles=header_styles(wt_hdr))
    for key, name, defn in BUCKETS:
        c.write([name, ", ".join(codes.get(key, [])), defn],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §5 - Vendor overrides  (read-only reference)
    c.banner("§5 - Vendor overrides", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    vo_hdr = ["Vendor name key", "Bucket"]
    c.write(vo_hdr, styles=header_styles(vo_hdr))
    for name_key, bucket in VENDOR_BUCKET_OVERRIDES:
        c.write([name_key, BUCKET_NAME.get(bucket, bucket)],
                styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[38, 18, 44],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def input_conc_threshold_cell() -> str:
        return f"'{_TAB}'!$C${pos['conc']}"

    def input_multisource_cell() -> str:
        return f"'{_TAB}'!$C${pos['multi']}"

    def input_asof_cell() -> str:
        return f"'{_TAB}'!$C${pos['asof']}"

    def input_horizon_cell() -> str:
        return f"'{_TAB}'!$C${pos['horizon']}"

    def input_recent_fy_cell() -> str:
        return f"'{_TAB}'!$C${pos['cut']}"

    def input_wave_window_ref() -> str:
        return f"'{_TAB}'!$C${pos['wave_window']}"

    def input_sens_window_cell(w: int) -> str:
        key = {45: "sens45", 60: "sens60", 90: "wave_window",
               120: "sens120", 180: "sens180"}[w]
        return f"'{_TAB}'!$C${pos[key]}"

    def input_periodic_maxdur_cell() -> str:
        return f"'{_TAB}'!$C${pos['pmax']}"

    def input_ratio_cap_cell() -> str:
        return f"'{_TAB}'!$C${pos['ratio']}"

    def input_strong_minwaves_cell() -> str:
        return f"'{_TAB}'!$C${pos['strongn']}"

    def input_strong_cvcap_cell() -> str:
        return f"'{_TAB}'!$C${pos['cvcap']}"

    def input_alwayson_materiality_cell() -> str:
        return f"'{_TAB}'!$C${pos['mater']}"

    def input_active_lookback_cell() -> str:
        return f"'{_TAB}'!$C${pos['actlook']}"

    def input_active_minrec_cell() -> str:
        return f"'{_TAB}'!$C${pos['actrec']}"

    def input_active_mindollar_cell() -> str:
        return f"'{_TAB}'!$C${pos['actdol']}"

    return (SheetEntry(_TAB, _GROUP, render),
            input_conc_threshold_cell, input_multisource_cell,
            input_asof_cell, input_horizon_cell, input_recent_fy_cell,
            input_wave_window_ref, input_periodic_maxdur_cell,
            input_ratio_cap_cell, input_strong_minwaves_cell,
            input_strong_cvcap_cell, input_alwayson_materiality_cell,
            input_active_lookback_cell, input_active_minrec_cell,
            input_active_mindollar_cell, input_sens_window_cell)


(INPUTS, input_conc_threshold_cell, input_multisource_cell,
 input_asof_cell, input_horizon_cell, input_recent_fy_cell,
 input_wave_window_ref, input_periodic_maxdur_cell,
 input_ratio_cap_cell, input_strong_minwaves_cell,
 input_strong_cvcap_cell, input_alwayson_materiality_cell,
 input_active_lookback_cell, input_active_minrec_cell,
 input_active_mindollar_cell, input_sens_window_cell) = _make_inputs()
