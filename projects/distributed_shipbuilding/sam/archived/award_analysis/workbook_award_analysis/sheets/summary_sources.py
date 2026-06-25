"""summary_sources - the "Sources" tab: provenance, source files, and caveats.

Authored (static) provenance for the corpus the workbook is built on. No
accessors, no native table - the one tab where a one-line context note per item
is the house standard (sheet_guide "Sources is the sole exception").

  §1 Pull log     - the SAM.gov subaward pull, PIID scope, FY date field, vendor
                    keying and classification basis, as-of date and window.
  §2 Source files - the extracted wb_*.csv inventory each tab derives from, and
                    the scripts that regenerate them.
  §3 Source notes - the defensibility caveats (FSRS floors, left-censoring, FFATA
                    lag / FY26 partial, boilerplate award text).

Content is the authored pull log + corpus caveats (see the Re-Buy Methodology
Explainer for the narrative) + the extract-script CSV inventory. Imports only
workbook_core + the local helpers - no sheet dependency.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import S_DEFAULT, S_TITLE_SHEET, S_TITLE_SECTION
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._widths import header_styles
from workbook_award_analysis.sheets._tabs import TAB_SOURCES

_GROUP = "sources"
_TAB = TAB_SOURCES
_NCOLS = 2                                   # content columns B (label), C (text)

_PULL_LOG = [
    ("Source", "SAM.gov Acquisition Subaward Reporting API "
     "(/prod/contract/v1/subcontracts/search), full-history pull per PIID."),
    ("Pull script", "pull_sam_subawards_fullhistory.py (status Published; "
     "Deleted retained for audit)."),
    ("PIID scope", "In-scope shipbuilder-directed new-construction PIIDs from "
     "nc_scope_summary.json - 15 submarine + 24 DDG (GD-BIW + HII-Ingalls)."),
    ("Excluded", "Navy-directed GFE primes, MIB and BlueForge (outside "
     "supplier-lane scope)."),
    ("FY date field", "subAwardDate (the action date, federal FY) - NOT "
     "submittedDate, which carries the 6-18 mo FFATA filing lag."),
    ("Vendor key", "vendor_key = subParentUei or subEntityUei (parent-first); "
     "display name is the dollar-weighted modal name for the key."),
    ("Classification", "Registry-first per vendor UEI "
     "(vendor_evidence_registry.csv), else the classify() NAICS-4 + name-override "
     "ladder; seven mutually-exclusive work-type buckets."),
    ("As of", "2026-05-22 (latest reported subaward action)."),
    ("Window", "≤FY12 through FY26 (subaward action FY; FY26 partial)."),
]

_SOURCE_FILES = [
    ("wb_piid_worktype.csv", "Lane Detail leaf: (program, PIID, work type) x FY "
     "$ and record counts."),
    ("wb_vendor_lane.csv", "Lane Vendors leaf: (program, PIID, work type, vendor) "
     "record count + $M."),
    ("wb_vendor_lane_fy.csv", "Lane Vendor FY leaf: vendor x lane x FY $ + records "
     "+ capability (the sourcing-signal leaf)."),
    ("wb_award_waves.csv", "Award Waves leaf: one row per (program, PIID, work "
     "type, award wave) - start / end / anchor, span, net + positive-gross $, "
     "corrections, modal capability, prime offset."),
    ("wb_wave_vendors.csv", "Wave Vendors leaf: one row per wave-vendor - net + "
     "positive-gross $, records, first/last date in wave, capability, entrant "
     "flag (the 'same vendors / same split each wave?' grain)."),
    ("wb_role_piid.csv", "Role Detail leaf: (program, role, PIID) x FY $ + records "
     "(all roles)."),
    ("wb_prime_calendar.csv", "Prime Awards: per-PIID prime base/last action dates "
     "+ coverage flags."),
    ("wb_annual_worktype.csv", "Work-type bucket roster + full-history order "
     "(Market Views Work type)."),
    ("wb_annual_class.csv", "Class / builder cut roster (Market Views Vessel "
     "basis)."),
    ("wb_annual_piid.csv", "PIID scope meta + data_status + record counts "
     "(Market Views PIID)."),
    ("wb_vendor_fy.csv", "Supplier vendor roster + cut profile + first/last award "
     "(Market Views Vendor)."),
    ("wb_lane_signals.csv", "Per-lane sourcing signals: wave cadence + dispersion, "
     "wave-shape (longest/median span, quiet gap, span/cadence ratio), trailing "
     "activity (last 180/365d $ + records, days-since, recent adds), top-1 names, "
     "second-source FY, incumbent (Indicators / Continuous Sourcing)."),
]

_SOURCE_NOTES = [
    "FSRS first-tier subaward reporting is incomplete (esp. pre-FY22); reported "
    "levels are FLOORS, not ceilings - pool sizes understate.",
    "Entrant left-censoring: a vendor first reported recently may be a long-time "
    "supplier newly reported.",
    "FFATA filing lag (6-18 mo): recent low/zero years (esp. FY26, partial) can be "
    "reporting lag, not a real decline.",
    "Award descriptions are boilerplate (\"See Below\"); classification rides on "
    "the vendor, not the award text.",
    "Regenerated by research/scripts/extract_workbook_cuts.py (the wb_annual_* / "
    "role / vendor / lane cuts) and compute_jumpball_signals.py (wb_lane_signals, "
    "wb_award_waves, wb_wave_vendors, wb_prime_calendar) from the classified "
    "full-history corpus.",
]


def _make_sources():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 - Pull log
    c.banner("§1 - Pull log", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    for field, value in _PULL_LOG:
        c.write([field, value], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 - Source files
    c.banner("§2 - Source files", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["File", "What it carries"],
            styles=header_styles(["File", "What it carries"]))
    for fname, desc in _SOURCE_FILES:
        c.write([fname, desc], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 - Source notes
    c.banner("§3 - Source notes", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    for note in _SOURCE_NOTES:
        c.write([note], styles=[S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[24, 72],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


SOURCES = _make_sources()
