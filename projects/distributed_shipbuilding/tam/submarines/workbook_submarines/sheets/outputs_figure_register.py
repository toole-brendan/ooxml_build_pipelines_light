"""outputs_figure_register - the "Figure Register" tab (one module = one sheet).

The deck-facing figure contract (formerly Deck_Outputs): one live cross-sheet link
per registered figure, never a hardcoded value. Mechanical, not reader-facing - the
Executive Summary is the human answer page. Exposes value_cell / source_ref / is_pct
/ REGISTRY (consumed by Number Audit) and publishes the workbook defined names.

Semantic fix: DO-01 and the `portfolio_tam` defined name source from TAM Build's
cumulative TAM producer (tam_build.cumulative_tam_cell), not a TAM value carried on
the SAM tab. Imports its producers across the model / data / validation sheets;
nothing here imports Number Audit (which imports this module), so the at-a-glance
omits the Number Audit fail count (it lives on Number Audit / QA / Executive Summary).
"""
from __future__ import annotations

import re

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM, S_LINK_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.sheets.taxonomy import BUCKETS, BUCKET_KEYS
from workbook_submarines.sheets.validation_sib_excluded import sib_total_cell
from workbook_submarines.sheets.model_tam_build import (
    cumulative_tam_cell, va_bc_supplier_coeff_cell, col_bc_supplier_coeff_cell,
    ap_lltm_supplier_coeff_cell,
    total_weighted_coeff_cell, avg_annual_tam_cell, tam_total_cell,
    tam_obbba_total_cell, cumulative_bc_base_cell, cumulative_obbba_base_cell,
    cumulative_obbba_tam_cell, removal_cell, n_years_cell, FY_COLUMNS,
)
from workbook_submarines.sheets.data_obbba_funding import (
    obbba_gross_total_cell, obbba_capacity_total_cell,
)
from workbook_submarines.sheets.model_sam_build import (
    bucket_tam_cell, unbucketed_tam_cell, sam_cell, avg_annual_sam_cell,
    scenario_keys_ordered,
)
from workbook_submarines.sheets.data_entity_master import addressable_total_cell
from workbook_submarines.sheets.validation_pop_source_audit import gated_dollar_cell, gfe_excluded_dollar_cell
from workbook_submarines.sheets.data_ap_bridge import (
    ap_bridge_gross_cell, ap_bridge_gfe_removed_cell, ap_bridge_in_bc_removed_cell,
    ap_bridge_residual_cell, ap_bridge_base_cell,
)
from workbook_submarines.sheets.model_outlook import (
    penetration_cell, penetration_l6y_cell, penetration_fy2627_cell,
    outyear_low_cell, outyear_high_cell, outyear_low_avg_cell,
    outyear_high_avg_cell, tam_fy2225_avg_cell,
)
from workbook_submarines.sheets.inputs_assumptions import scenario_name
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "outputs"
_TAB = "Figure Register"
_PCT_IDS = {"DO-02", "DO-03", "DO-04"} | {f"DO-{n}" for n in range(63, 71)}
_HEADER_ROW = 15                                 # title(2)+blank+§1(4-10)+2 blanks+§2 banner(13)+blank
_FIRST_DATA = 16
_FR_HEADERS = ["Figure ID", "Slide", "Label", "Value", "Unit", "Source cell", "Producer tab"]


def _registry():
    # Slide numbers follow the 18-slide deck architecture (4 Exec Summary, 7 Basic
    # Construction, 8 TAM Bridge, 9 Annual TAM & SAM, 10 Coefficient Evidence,
    # 11 AP & LLTM Reconciliation, 13 Bucket TAM, 14 SAM Scenarios, 15 Visible
    # Suppliers, 16 SIB Exclusion).
    reg = [
        ("DO-01", 4, "Headline non-nuclear supplier TAM, FY22-27 cumulative $M (AP/LLTM base=0)", cumulative_tam_cell()),
        ("DO-09", 4, "Average annual portfolio TAM $M", avg_annual_tam_cell()),
        ("DO-10", 4, "Average annual broad component-mfg SAM $M", avg_annual_sam_cell("broad")),
        ("DO-02", 10, "Virginia BC supplier coefficient (Block V announced POP)", va_bc_supplier_coeff_cell()),
        ("DO-82", 10, "Columbia BC supplier coefficient (Build I announced POP)", col_bc_supplier_coeff_cell()),
        ("DO-03", 10, "AP/LLTM reference coefficient (not applied; base=0)", ap_lltm_supplier_coeff_cell()),
        ("DO-04", 10, "Total weighted coefficient (corpus)", total_weighted_coeff_cell()),
        ("DO-05", 10, "Gated POP corpus $M", gated_dollar_cell()),
        ("DO-06", 10, "GFE / excluded-scope $M (dropped)", gfe_excluded_dollar_cell()),
        ("DO-07", 15, "Supplier-addressable subaward $M (full corpus)", addressable_total_cell()),
        ("DO-08", 16, "SIB exclusion $M (subaward-level)", sib_total_cell()),
    ]
    bucket_name = {k: name for k, name, _ in BUCKETS}
    for i, k in enumerate(BUCKET_KEYS):
        reg.append((f"DO-1{i+1}", 13, f"Bucket TAM - {bucket_name[k]} $M", bucket_tam_cell(k)))
    reg.append(("DO-18", 13, "Bucket TAM - unbucketed residual $M", unbucketed_tam_cell()))
    for i, sk in enumerate(scenario_keys_ordered()):
        reg.append((f"DO-2{i}", 14, f"SAM - {scenario_name(sk)} $M", sam_cell(sk)))
    for i, sk in enumerate(scenario_keys_ordered()):
        reg.append((f"DO-2{i+5}", 14, f"Avg annual SAM - {scenario_name(sk)} $M", avg_annual_sam_cell(sk)))
    for i, fy in enumerate(FY_COLUMNS):
        reg.append((f"DO-3{i+1}", 9, f"FY{fy} portfolio TAM $M", tam_total_cell(fy)))
    reg.append(("DO-51", 7, "BC construction base $M (FY22-27)", cumulative_bc_base_cell()))
    reg.append(("DO-52", 8, "POP removal (prime/co-prime/GFE) $M", removal_cell()))
    reg.append(("DO-53", 11, "P-10 gross AP top-line $M (FY22-27)", ap_bridge_gross_cell()))
    reg.append(("DO-54", 11, "AP bridge: less GFE/design/weapons $M", ap_bridge_gfe_removed_cell()))
    reg.append(("DO-55", 11, "AP bridge: less already-in-BC $M", ap_bridge_in_bc_removed_cell()))
    reg.append(("DO-56", 11, "AP bridge: less un-itemized Va FY22-23 $M", ap_bridge_residual_cell()))
    reg.append(("DO-57", 11, "AP/LLTM additive base $M (confirmed 0)", ap_bridge_base_cell()))
    reg.append(("DO-58", 8, "OBBBA gross award $M (Sec. 20002(16))", obbba_gross_total_cell()))
    reg.append(("DO-59", 8, "OBBBA mandatory BC base $M (FY22-27)", cumulative_obbba_base_cell()))
    reg.append(("DO-60", 8, "OBBBA mandatory TAM $M (FY22-27)", cumulative_obbba_tam_cell()))
    reg.append(("DO-61", 9, "FY2026 OBBBA mandatory TAM $M", tam_obbba_total_cell(2026)))
    reg.append(("DO-62", 16, "OBBBA capacity / cadence memo $M (excluded)", obbba_capacity_total_cell()))
    # Penetration & outyear outlook (Outlook tab) - slide 9 extension
    for i, fy in enumerate(range(2022, 2028)):
        reg.append((f"DO-{63 + i}", 9, f"Outsourced BC penetration FY{fy}", penetration_cell(fy)))
    reg.append(("DO-69", 9, "Outsourced BC penetration, FY22-27 avg", penetration_l6y_cell()))
    reg.append(("DO-70", 9, "Outsourced BC penetration, FY26-27 avg", penetration_fy2627_cell()))
    for i, fy in enumerate(range(2028, 2032)):
        reg.append((f"DO-{71 + i}", 9, f"Implied Outsourced BC low FY{fy} $M", outyear_low_cell(fy)))
    for i, fy in enumerate(range(2028, 2032)):
        reg.append((f"DO-{75 + i}", 9, f"Implied Outsourced BC high FY{fy} $M", outyear_high_cell(fy)))
    reg.append(("DO-79", 9, "Implied outyear Outsourced BC low $M/yr", outyear_low_avg_cell()))
    reg.append(("DO-80", 9, "Implied outyear Outsourced BC high $M/yr", outyear_high_avg_cell()))
    reg.append(("DO-81", 9, "FY22-25 average annual TAM $M/yr", tam_fy2225_avg_cell()))
    return reg


REGISTRY = _registry()
DECK_ROW = {fid: _FIRST_DATA + i for i, (fid, *_rest) in enumerate(REGISTRY)}
_LAST_DATA = _FIRST_DATA + len(REGISTRY) - 1


def _producer_tab(ref: str) -> str:
    """Parse the sheet name out of a 'Tab'!Cell reference (the figure's producer)."""
    return ref.split("!", 1)[0].strip().strip("'")


def assert_all_links():
    bad = [fid for fid, _s, _l, ref in REGISTRY if "!" not in (ref or "")]
    if bad:
        raise ValueError(f"Figure Register figures without a source link: {bad}")


assert_all_links()


def value_cell(figure_id):
    if figure_id not in DECK_ROW:
        raise ValueError(f"Unknown figure {figure_id!r}")
    return f"'{_TAB}'!E{DECK_ROW[figure_id]}"


def source_ref(figure_id):
    for fid, _s, _l, ref in REGISTRY:
        if fid == figure_id:
            return ref
    raise ValueError(f"Unknown figure {figure_id!r}")


def is_pct(figure_id):
    return figure_id in _PCT_IDS


def _abs(ref):
    return re.sub(r"!\$?([A-Za-z]+)\$?(\d+)$", r"!$\1$\2", ref)


_n_tam = sum(1 for _f, _s, label, _r in REGISTRY if "TAM" in label)
_n_sam = sum(1 for _f, _s, label, _r in REGISTRY if "SAM" in label)
_COVERAGE = [
    ("Headline TAM", sum(1 for f, *_ in REGISTRY if f in {"DO-01", "DO-09"})),
    ("Supplier coefficients", sum(1 for f, *_ in REGISTRY if f in {"DO-02", "DO-03", "DO-04"})),
    ("POP corpus", sum(1 for f, *_ in REGISTRY if f in {"DO-05"})),
    ("Exclusions", sum(1 for f, *_ in REGISTRY if f in {"DO-06", "DO-08"})),
    ("Supplier-addressable base", sum(1 for f, *_ in REGISTRY if f in {"DO-07"})),
    ("Bucket TAM", sum(1 for f, *_ in REGISTRY if f.startswith("DO-1"))),
    ("SAM scenarios", sum(1 for f, *_ in REGISTRY if f.startswith("DO-2"))),
    ("Annual TAM", sum(1 for f, *_ in REGISTRY if f.startswith("DO-3"))),
    ("BC base / POP removal / AP bridge", sum(1 for f, *_ in REGISTRY if f in {"DO-51", "DO-52", "DO-53", "DO-54", "DO-55", "DO-56", "DO-57"})),
    ("OBBBA mandatory", sum(1 for f, *_ in REGISTRY if f in {"DO-58", "DO-59", "DO-60", "DO-61", "DO-62"})),
]
# Headline contract: annual values are primary; cumulative kept as supporting. The
# legacy names portfolio_tam / sam_broad stay as cumulative aliases for the deck
# pipeline until it adopts the *_annual / *_cumulative names.
_DEFINED = [
    "portfolio_tam_annual", "portfolio_tam_cumulative", "portfolio_tam",
    "broad_sam_annual", "broad_sam_cumulative", "sam_broad",
    "fiscal_year_count", "bc_supplier_coeff_va", "bc_supplier_coeff_col",
    "ap_lltm_supplier_coeff",
]
_DN_MEANING = {
    "portfolio_tam_annual": "average annual portfolio TAM (headline)",
    "portfolio_tam_cumulative": "FY22-FY27 cumulative portfolio TAM",
    "portfolio_tam": "cumulative portfolio TAM (alias = portfolio_tam_cumulative)",
    "broad_sam_annual": "average annual broad component-mfg SAM (headline)",
    "broad_sam_cumulative": "FY22-FY27 cumulative broad component-mfg SAM",
    "sam_broad": "broad component-mfg SAM (alias = broad_sam_cumulative)",
    "fiscal_year_count": "number of fiscal years (FY22-FY27)",
    "bc_supplier_coeff_va": "applied Virginia BC coefficient (Block V announced POP)",
    "bc_supplier_coeff_col": "applied Columbia BC coefficient (Build I announced POP)",
    "ap_lltm_supplier_coeff": "AP/LLTM reference coefficient",
}


def _render_figure_register() -> WorksheetSpec:
    n_cols = 7
    dn_target = {
        "portfolio_tam_annual": avg_annual_tam_cell(),
        "portfolio_tam_cumulative": cumulative_tam_cell(),
        "portfolio_tam": cumulative_tam_cell(),
        "broad_sam_annual": avg_annual_sam_cell("broad"),
        "broad_sam_cumulative": sam_cell("broad"),
        "sam_broad": sam_cell("broad"),
        "fiscal_year_count": n_years_cell(),
        "bc_supplier_coeff_va": va_bc_supplier_coeff_cell(),
        "bc_supplier_coeff_col": col_bc_supplier_coeff_cell(),
        "ap_lltm_supplier_coeff": ap_lltm_supplier_coeff_cell(),
    }
    c = RowCursor(2)
    c.banner("Figure Register", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Registered figure contract", n_cols=n_cols, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Registered figures", len(REGISTRY)],
            styles=[S_BOLD, S_DEFAULT])
    c.write(["TAM figures", _n_tam], styles=[S_DEFAULT, S_DEFAULT])
    c.write(["SAM figures", _n_sam], styles=[S_DEFAULT, S_DEFAULT])
    c.write(["Defined names", len(_DEFINED)],
            styles=[S_DEFAULT, S_DEFAULT])
    c.blank(2)

    # §2 Figure registry (native table)
    c.banner("§2 - Figure registry", n_cols=n_cols,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    assert c.at() == _HEADER_ROW, f"registry header at {c.at()}, expected {_HEADER_ROW}"
    c.write(_FR_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER,
                                 S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_LEFT])
    assert c.at() == _FIRST_DATA
    for fid, slide, label, ref in REGISTRY:
        pct = fid in _PCT_IDS
        v_style = S_LINK_PCT if pct else S_LINK_NUM
        c.write([fid, slide, label, f"={ref}", "%" if pct else "$M", ref, _producer_tab(ref)],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, v_style, S_DEFAULT, S_DEFAULT, S_DEFAULT],
                outline_level=1)
    table = ExcelTable(name="tbl_sub_figure_register",
                       ref=f"B{_HEADER_ROW}:{col_letter(len(_FR_HEADERS))}{_LAST_DATA}",
                       headers=_FR_HEADERS)
    c.blank(2)

    # §3 Defined names
    c.banner("§3 - Defined names (workbook-scoped)", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Defined name", "Target cell", "Meaning"], styles=S_HEADER_LEFT)
    for nm in _DEFINED:
        c.write([nm, dn_target[nm], _DN_MEANING[nm]], styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 Register coverage
    c.banner("§4 - Register coverage", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Category", "Figure count"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    for cat, cnt in _COVERAGE:
        c.write([cat, cnt], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    ws = worksheet(c.rows, cols=[18, 7, 42, 14, 8, 38, 22], tab_color=group_color(_GROUP), with_gutter=True)
    defined_names = {nm: _abs(dn_target[nm]) for nm in _DEFINED}
    return WorksheetSpec(ws, tables=[table], defined_names=defined_names)


FIGURE_REGISTER = SheetEntry(_TAB, _GROUP, _render_figure_register)
