"""inputs_assumptions - the "Assumptions" tab (one module = one sheet).

The SINGLE edit surface for model behaviour. It owns the run settings, the stream
include-toggles (moved here from the TAM model), the AP/LLTM additive base + gross
reference, the OBBBA mandatory-overlay controls, the target-scenario inclusion
matrix (moved here from the SAM model), the bucket-share adjustments, the
default-scenario selector, and the Outlook outyear penetration bounds (§9,
the intent uplift behind each class's high assumption). The bucket adjustments
(§8) apply uniformly to BOTH class share vectors; the modeled per-class per-FY
shares themselves are produced on SAM Build from the gated Worktype by FY
evidence + these adjustments.

Why the AP/LLTM additive base is held at 0: P-10 Advance Procurement is extracted but
NOT additive to P-5c Basic Construction - supplier LLTM is already inside BC, so
adding the P-10 gross (~$10-20B) would double-count. The gross is shown as reference
only; see the LLTM AP reconciliation bridge.

OBBBA mandatory controls (§4): the award dollars themselves live on the OBBBA
Mandatory data sheet; this section holds the behaviour levers. The BC share
bridges the Sec. 20002(16) gross award (no cost-category breakout) to a BC base
(observed = Virginia FY26 P-5c BC % of Total, adjustable). The FY2027 execution
spillover is 0 by default because the allocation plan is FY2026 budget authority
with no FY2027 column - moving dollars into FY27 requires an explicit award/outlay
profile, not a default.

Layout: the body (positions that back the accessors) is built once at IMPORT time via
a cursor, so cross-sheet accessors resolve regardless of render order. The only
back-reference to SAM Build (the §4 selector display row) is built at RENDER time via
a lazy import and spliced into the body, so there is no assumptions_controls <->
sam_build import cycle.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, banner_row, write_row, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT,
    S_PCT_INPUT, S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
    S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._bind import EXTRACTED
from workbook_master_tam.sheets.submarines.taxonomy import BUCKETS, BUCKET_KEYS
from workbook_master_tam.sheets.submarines.data_deflators import deflator_factor_cell
from workbook_master_tam.sheets.submarines.data_scn_budget import scn_cell as _scn
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "inputs"
_TAB = "Sub Assumptions"

FY_COLUMNS = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_COL_INDEX = {fy: 2 + i for i, fy in enumerate(FY_COLUMNS)}   # B=label, C=FY22..
_LI_LABEL = {2013: "Virginia (LI 2013)", 1045: "Columbia (LI 1045)"}
_BUCKET_NAME = {k: name for k, name, _ in BUCKETS}

# Target-scenario membership (moved from the former sam_sheets) - seeds the matrix.
# NOTE: `modular` is ENTITY-driven - its SAM is computed in SAM Build from the registry
# modular flag (per operating entity), NOT from a bucket union. The sentinel set keeps
# its flag-matrix column all-zero; SAM Build special-cases it.
_MODULAR_ENTITY = {"_entity"}
SCENARIOS = [
    ("metal", "Metal components", {"structural", "castings", "machining"}),
    ("hme", "HM&E components", {"piping", "hvac", "machining", "electrical"}),
    ("electrical", "Electrical / power", {"electrical"}),
    ("modular", "Modular assemblies", _MODULAR_ENTITY),
    ("broad", "Broad component mfg", set(BUCKET_KEYS)),
]
_SHORT = {"metal": "Metal", "hme": "HM&E", "electrical": "Electrical",
          "modular": "Modular", "broad": "Broad"}
SCENARIO_KEYS = [s[0] for s in SCENARIOS]
_SCEN_COL = {k: 2 + i for i, k in enumerate(SCENARIO_KEYS)}      # Metal=C .. Broad=G


def _fy_col(fy): return col_letter(_FY_COL_INDEX[fy])


def _f(x) -> float:
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def _load_p10_gross_ap() -> dict[tuple[int, int], float]:
    """{(li, fy): latest-vintage P-10 'TOTAL: Advance Procurement' $M} for FY22-27."""
    best: dict[tuple[int, int], tuple[str, float]] = {}
    with (EXTRACTED / "scn_p10_ap_long.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if "TOTAL: Advance Procurement" not in (r.get("category") or ""):
                continue
            li = int(_f(r.get("li")))
            fy = int(_f(r.get("fy")))
            if fy not in _FY_COL_INDEX or li not in (2013, 1045):
                continue
            pb = (r.get("pb_year") or "").strip()
            val = _f(r.get("value_$M"))
            k = (li, fy)
            if k not in best or pb > best[k][0]:
                best[k] = (pb, val)
    return {k: v for k, (pb, v) in best.items()}


_GROSS = _load_p10_gross_ap()
_FY_HDR_7 = [S_HEADER_LEFT] + [S_HEADER_CENTER] * len(FY_COLUMNS)


def _build_body(tab: str):
    """Build the body at import time; capture every accessor-backing row in P.

    Returns (rows_before_selector, selector_row, rows_after_selector, P, next_row).
    The §4 selector data row is deferred (SAM Build links resolved lazily at render).
    """
    P = {}
    c = RowCursor(4)

    # §1 Run settings
    c.banner("§1 - Run settings", n_cols=7, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Setting", "Value"], styles=S_HEADER_LEFT)
    c.write(["Program", "Submarine"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    P["fy_start"] = c.write(["FY range start", 2022],
                            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    P["fy_end"] = c.write(["FY range end", 2027],
                          styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Units", "Constant FY2026 $M (then-year source retained)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    P["default_scen"] = c.write(["Default SAM scenario", "Broad component mfg"],
                                styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Stream controls
    c.banner("§2 - Stream controls", n_cols=7, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Control", "Value"], styles=S_HEADER_LEFT)
    P["incl_bc"] = c.write(["Include BC stream", 1],
                           styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    P["incl_ap"] = c.write(["Include AP/LLTM stream", 1],
                           styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    P["incl_obbba"] = c.write(["Include OBBBA mandatory (Sec. 20002(16)) stream", 1],
                              styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    c.write(["Prior-year AP credit treatment", "none (credits = 0)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 AP/LLTM additive base
    c.banner("§3 - AP/LLTM additive base ($M, confirmed 0)", n_cols=7,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Class"] + list(FY_COLUMNS), styles=_FY_HDR_7)
    P["ap_base"] = {}
    _AP_NOTE = ("Held at 0: P-10 supplier LLTM already sits inside P-5c BC (an additive "
                "base would double-count). The AP/LLTM coefficient is corpus-measured "
                "(~48.5%) but reference-only - see TAM Build §3a and AP Bridge.")
    for li in (2013, 1045):
        P["ap_base"][li] = c.write(
            [_LI_LABEL[li]] + [0] * len(FY_COLUMNS),
            styles=[S_BOLD] + [S_NUM_INPUT] * len(FY_COLUMNS),
            outline_level=1)
    P["notes"] = [(f"B{P['ap_base'][2013]}", _AP_NOTE)]
    rb13, rb10 = P["ap_base"][2013], P["ap_base"][1045]
    c.total(["Total (Va + Col)"] + [f"=N({_fy_col(fy)}{rb13})+N({_fy_col(fy)}{rb10})" for fy in FY_COLUMNS],
            styles=[S_BOLD] + [S_NUM] * len(FY_COLUMNS), n_cols=7)
    c.blank()
    # §3b Constant-FY2026 AP base (then-year x Green Book Procurement deflator). Backs
    # ap_lltm_base_cell. The submarine base is confirmed 0, so the conversion is a no-op
    # numerically; the row exists for symmetry with DDG and so a future nonzero base would
    # be deflated correctly with no further code change.
    c.banner("§3b - Constant FY2026 $M (then-year x deflator)", n_cols=7,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Class"] + list(FY_COLUMNS), styles=_FY_HDR_7)
    P["ap_base_const"] = {}
    for li in (2013, 1045):
        P["ap_base_const"][li] = c.write(
            [_LI_LABEL[li]]
            + [f"={_fy_col(fy)}{P['ap_base'][li]}*{deflator_factor_cell(fy)}" for fy in FY_COLUMNS],
            styles=[S_BOLD] + [S_LINK_NUM] * len(FY_COLUMNS), outline_level=1)
    c.blank()
    c.banner("§3a - P-10 gross AP reference ($M, overlaps BC)", n_cols=7,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Class"] + list(FY_COLUMNS), styles=_FY_HDR_7)
    P["ap_gross"] = {}
    for li in (2013, 1045):
        P["ap_gross"][li] = c.write([_LI_LABEL[li]] + [_GROSS.get((li, fy)) for fy in FY_COLUMNS],
                                    styles=[S_BOLD] + [S_NUM_INPUT] * len(FY_COLUMNS),
                                    outline_level=1)
    c.blank(2)

    # §4 OBBBA mandatory controls (award dollars live on the OBBBA Mandatory tab)
    c.banner("§4 - OBBBA mandatory controls (Sec. 20002(16))", n_cols=7,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Control", "Value"], styles=S_HEADER_LEFT)
    P["obbba_spill"] = c.write(["FY2027 execution spillover (share of FY26 award)", 0],
                               styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    c.blank()
    c.write(["Measure", "Observed", "Adjustment", "Modeled"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    P["obbba_bc_share"] = c.write(
        ["OBBBA BC share of award (Virginia FY26 P-5c)",
         f"={_scn(2013, 2026, 'bc_pct')}", 0, lambda r: f"=C{r}+D{r}"],
        styles=[S_DEFAULT, S_LINK_PCT, S_PCT_INPUT, S_PCT], outline_level=1)
    c.blank(2)

    # §5 Construction-master announced POP (class-vintage BC coefficients)
    c.banner("§5 - Construction-master announced POP (class-vintage BC coefficients)",
             n_cols=7, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Master", "PIID", "$M", "EB %", "HII %", "Other-US %", "Foreign %"],
            styles=[S_HEADER_LEFT] * 2 + [S_HEADER_CENTER] * 5)
    _VM_NOTE = ("Announced POP of the construction contracts funding the in-window boats. "
                "Virginia Block V (DoD announcement 2019-12-02, article 2030017, "
                "$22,209.9M, nine boats FY19-23): 'Newport News (25%); Quonset Point (21%); "
                "Groton (20%); Sunnyvale (8%); named cities 3%; other US below 1% (22%); "
                "outside US below 1% (1%)'. Columbia Build I (2020-11-05, article 2406922, "
                "$9,473.5M, SSBN 826 + 827): 'Groton (36%); Newport News (25%); Quonset "
                "Point (17%); other US sites each less than 1% (22%)'. Below-1% aggregates "
                "count as other-US (corpus parse convention). Each class coefficient = "
                "other-US + foreign of its own master (TAM Build §3a). Block VI "
                "construction is unawarded; restate the Virginia row on its announcement.")
    P["vintage"] = {}
    for key, label, piid, master, eb, hii, oth, frn in [
        ("va", "Virginia Block V (FY19-23 boats)", "N00024-17-C-2100",
         22209.893, 41, 25, 33, 1),
        ("col", "Columbia Build I (SSBN 826 + 827)", "N00024-17-C-2117",
         9473.511, 53, 25, 22, 0),
    ]:
        P["vintage"][key] = c.write(
            [label, piid, master, eb / 100, hii / 100, oth / 100, frn / 100],
            styles=[S_BOLD, S_DEFAULT, S_NUM_INPUT, S_PCT_INPUT, S_PCT_INPUT, S_PCT_INPUT,
                    S_PCT_INPUT],
            outline_level=1)
    P["notes"].append((f"B{P['vintage']['va']}", _VM_NOTE))
    c.blank(2)

    # §6 Scenario selector - banner + header at import; data row deferred to render
    c.banner("§6 - Scenario selector", n_cols=7, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Selected scenario", "Cumulative SAM $M", "% of TAM", "Avg annual SAM $M"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    rows_before = list(c.rows)
    sel_row = c.at()
    c.blank()          # reserve the selector data row
    c.blank(2)         # gap before §5
    c.rows = []        # subsequent rows belong to the 'after' bucket

    # §7 Target scenario matrix
    c.banner("§7 - Target scenario matrix (1 = targets bucket)", n_cols=7,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario key:  " + "   ·   ".join(f"{_SHORT[k]} = {name}" for k, name, _s in SCENARIOS)],
            styles=[S_DEFAULT])
    c.write(["Bucket"] + [_SHORT[k] for k, _n, _s in SCENARIOS],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(SCENARIOS))
    P["matrix_first"] = c.at()
    for k in BUCKET_KEYS:
        flags = [(1 if k in s else 0) for _k, _n, s in SCENARIOS]
        c.write([_BUCKET_NAME[k]] + flags,
                styles=[S_DEFAULT] + [S_NUM_INPUT] * len(SCENARIOS), outline_level=1)
    c.blank(2)

    # §8 Bucket share adjustments (applied to both class vectors on SAM Build)
    c.banner("§8 - Bucket share adjustments (applied to both class share vectors -> SAM Build)",
             n_cols=7, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket", "Adjustment"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["adj"] = {}
    for k in BUCKET_KEYS:
        P["adj"][k] = c.write([_BUCKET_NAME[k], 0],
                              styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    c.blank(2)

    # §9 Outlook outyear penetration bounds (Outlook §3 links here; both classes)
    c.banner("§9 - Outlook outyear penetration bounds", n_cols=7,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Knob", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["intent_uplift"] = c.write(
        ["Outsourcing intent uplift vs FY22-25 average", 0.30],
        styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    P["notes"].append((
        f"C{P['intent_uplift']}",
        "Outlook upper bound = each class's FY22-25 average penetration x (1 + this "
        "uplift). Basis: stated industry intent to grow outsourced manhours ~30% "
        "(HII statement; citation pending - swap in the source when confirmed)."))

    return rows_before, sel_row, list(c.rows), P, c.at()


# ── Import-time layout pass ───────────────────────────────────────────────────
_rows_before, _SEL_ROW, _rows_after, _P, _after_body = _build_body(_TAB)


# ── Accessors (load-bearing; consumed by TAM Build / SAM Build / LLTM AP / QA) ─

def fy_range_start_cell(): return f"'{_TAB}'!C{_P['fy_start']}"
def fy_range_end_cell(): return f"'{_TAB}'!C{_P['fy_end']}"
def n_years_count_formula(): return f"'{_TAB}'!C{_P['fy_end']}-'{_TAB}'!C{_P['fy_start']}+1"
def selected_sam_scenario_cell(): return f"'{_TAB}'!C{_P['default_scen']}"
def include_bc_stream_cell(): return f"'{_TAB}'!C{_P['incl_bc']}"
def include_ap_lltm_stream_cell(): return f"'{_TAB}'!C{_P['incl_ap']}"
def include_obbba_stream_cell(): return f"'{_TAB}'!C{_P['incl_obbba']}"
def obbba_spillover_cell(): return f"'{_TAB}'!C{_P['obbba_spill']}"
def obbba_bc_share_cell(): return f"'{_TAB}'!E{_P['obbba_bc_share']}"


def vintage_master_pop_cell(cls: str, field: str) -> str:
    """A §5 construction-master announced-POP cell ('va'/'col'; master $ or a POP %)."""
    cols = {"master": "D", "eb": "E", "hii": "F", "other_us": "G", "foreign": "H"}
    if cls not in _P["vintage"]:
        raise ValueError(f"Unknown class {cls!r}; expected 'va' or 'col'")
    if field not in cols:
        raise ValueError(f"Unknown field {field!r}; expected one of {sorted(cols)}")
    return f"'{_TAB}'!{cols[field]}{_P['vintage'][cls]}"


def ap_lltm_base_cell(li: int, fy: int) -> str:
    if li not in _P["ap_base_const"]:
        raise ValueError(f"Unknown LI {li!r}; expected 2013 or 1045")
    if fy not in _FY_COL_INDEX:
        raise ValueError(f"FY {fy!r} outside {FY_COLUMNS!r}")
    return f"'{_TAB}'!{_fy_col(fy)}{_P['ap_base_const'][li]}"


def ap_gross_cell(li: int, fy: int) -> str:
    if li not in _P["ap_gross"]:
        raise ValueError(f"Unknown LI {li!r}; expected 2013 or 1045")
    if fy not in _FY_COL_INDEX:
        raise ValueError(f"FY {fy!r} outside {FY_COLUMNS!r}")
    return f"'{_TAB}'!{_fy_col(fy)}{_P['ap_gross'][li]}"


def scenario_keys(): return list(SCENARIO_KEYS)


def scenario_name(k):
    for key, name, _s in SCENARIOS:
        if key == k:
            return name
    raise ValueError(f"Unknown scenario {k!r}")


def _matrix_last(): return _P["matrix_first"] + len(BUCKET_KEYS) - 1


def scenario_flag_range(k):
    if k not in _SCEN_COL:
        raise ValueError(f"Unknown scenario {k!r}")
    c = col_letter(_SCEN_COL[k])
    return f"'{_TAB}'!{c}{_P['matrix_first']}:{c}{_matrix_last()}"


def scenario_flag_cell(k, bucket):
    if k not in _SCEN_COL:
        raise ValueError(f"Unknown scenario {k!r}")
    if bucket not in BUCKET_KEYS:
        raise ValueError(f"Unknown bucket {bucket!r}")
    c = col_letter(_SCEN_COL[k])
    return f"'{_TAB}'!{c}{_P['matrix_first'] + BUCKET_KEYS.index(bucket)}"


def bucket_adjustment_cell(bucket):
    if bucket not in _P["adj"]:
        raise ValueError(f"Unknown bucket {bucket!r}")
    return f"'{_TAB}'!C{_P['adj'][bucket]}"


def outlook_intent_uplift_cell():
    return f"'{_TAB}'!C{_P['intent_uplift']}"


# ── Render ───────────────────────────────────────────────────────────────────

def _render_assumptions_controls() -> WorksheetSpec:
    # Scenario selector display - lazy SAM Build link breaks the import cycle.
    from workbook_master_tam.sheets.submarines import model_sam_build as _sam
    sel = write_row(_SEL_ROW,
                    [f"=C{_P['default_scen']}", f"={_sam.selected_sam_cell()}",
                     f"={_sam.selected_sam_pct_cell()}", f"={_sam.selected_avg_annual_sam_cell()}"],
                    styles=[S_DEFAULT, S_LINK_NUM, S_LINK_PCT, S_LINK_NUM],
                    start_col=1, outline_level=1)
    title = banner_row(2, _TAB, n_cols=7, style=S_TITLE_SHEET, with_gutter=True)
    rows = [title] + _rows_before + [sel] + _rows_after
    # Data-validation dropdowns on the editable controls (Value column = C).
    _ds, _ib, _ia, _io = _P["default_scen"], _P["incl_bc"], _P["incl_ap"], _P["incl_obbba"]
    _scen_list = ",".join(scenario_name(k) for k in SCENARIO_KEYS).replace("&", "&amp;")
    dvs = [
        f'<dataValidation type="list" allowBlank="1" showInputMessage="1" showErrorMessage="1" '
        f'sqref="C{_ds}"><formula1>"{_scen_list}"</formula1></dataValidation>',
        f'<dataValidation type="list" allowBlank="1" showInputMessage="1" showErrorMessage="1" '
        f'sqref="C{_ib}"><formula1>"0,1"</formula1></dataValidation>',
        f'<dataValidation type="list" allowBlank="1" showInputMessage="1" showErrorMessage="1" '
        f'sqref="C{_ia}"><formula1>"0,1"</formula1></dataValidation>',
        f'<dataValidation type="list" allowBlank="1" showInputMessage="1" showErrorMessage="1" '
        f'sqref="C{_io}"><formula1>"0,1"</formula1></dataValidation>',
        f'<dataValidation type="decimal" operator="between" allowBlank="1" showErrorMessage="1" '
        f'sqref="E{_P["vintage"]["va"]}:H{_P["vintage"]["col"]}">'
        f'<formula1>0</formula1><formula2>1</formula2></dataValidation>',
        f'<dataValidation type="decimal" operator="between" allowBlank="1" showErrorMessage="1" '
        f'sqref="C{_P["intent_uplift"]}">'
        f'<formula1>0</formula1><formula2>1</formula2></dataValidation>',
    ]
    ws = worksheet(rows, cols=[40, 16, 12, 14, 14, 12, 12],
                   tab_color=group_color(_GROUP), with_gutter=True, data_validations=dvs)
    return WorksheetSpec(ws, notes=[ExcelNote(ref, text) for ref, text in _P["notes"]])


ASSUMPTIONS = SheetEntry(_TAB, _GROUP, _render_assumptions_controls)
