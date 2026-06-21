"""outputs_figure_register - the "Figure Register" tab (DDG, outputs group; one module = one sheet).

The mechanical deck-facing figure contract - one cross-sheet link per slide figure
(no manual numbers), as a native no-format table (a flat, deck-facing contract).
Stays separate from Executive Summary (the human-readable answer page).

It also declares the workbook defined names, repointed to PRODUCER cells: the
headline ``portfolio_tam`` (and DO-01) source from TAM Build (the true TAM
producer), not the SAM allocation layer. The defined-name strings are preserved so
the downstream deck contract is unaffected.

Promoted accessors:
  REGISTRY, value_cell, source_ref, is_pct
"""
from __future__ import annotations

import re

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM, S_LINK_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._taxonomy import BUCKETS, BUCKET_KEYS
from workbook_master_tam.sheets.ddg.model_tam_build import (
    portfolio_tam_cell as _tam_portfolio_tam,
    bc_supplier_coeff_cell, ap_lltm_supplier_coeff_cell,
    outside_yards_corrected_cell, outside_yards_disclosed_cell,
    portfolio_bc_tam_cell, portfolio_ap_tam_cell, avg_annual_tam_cell, n_years_cell,
    per_hull_tam_cell, per_hull_bc_tam_cell, tam_cell, portfolio_bc_base_cell,
    pop_removal_cell,
)
from workbook_master_tam.sheets.ddg.model_sam_build import (
    addressable_total_cell, bucket_tam_cell, unbucketed_tam_cell, sam_cell,
    sam_avg_annual_cell, scenario_keys_ordered,
)
from workbook_master_tam.sheets.ddg.validation_pop_source_audit import (
    gated_dollar_cell, gfe_excluded_dollar_cell, masters_dollar_cell,
)
from workbook_master_tam.sheets.ddg.data_scn_budget import portfolio_scn_cell
from workbook_master_tam.sheets.ddg.model_outlook import (
    penetration_cell, penetration_l6y_cell, penetration_fy2627_cell,
    outyear_low_cell, outyear_high_cell, outyear_low_avg_cell,
    outyear_high_avg_cell, tam_fy2225_avg_cell,
)
from workbook_master_tam.sheets.ddg.inputs_scenarios import scenario_name
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "outputs"
_TAB = "DDG Figure Register"
_HEADERS = ["Figure ID", "Slide", "Label", "Value", "Source cell"]
_HEADER_ROW = 6                  # title(2)+blank+§1 banner(4)+blank+header(6)
_FIRST_DATA = 7


def _make_deck_outputs():
    bucket_name = {k: name for k, name, _ in BUCKETS}

    def _build_registry():
        bks = scenario_keys_ordered()
        # (slide, label, source-ref, is_pct) - DO ids assigned sequentially below.
        # Annual headline first; slide numbers track the 16-slide DDG deck.
        rows = [
            # slide 3 - executive summary headline (annual first, cumulative backup)
            (3, "Average annual portfolio TAM $M/yr", avg_annual_tam_cell(), False),
            (3, "Average annual broad component SAM $M/yr", sam_avg_annual_cell("broad"), False),
            (3, "Portfolio TAM (FY22-27 cumulative) $M", _tam_portfolio_tam(), False),
            (3, "Broad component SAM (FY22-27 cumulative) $M", sam_cell("broad"), False),
            (3, "BC-stream TAM (FY22-27) $M", portfolio_bc_tam_cell(), False),
            (3, "AP/LLTM-stream TAM (FY22-27) $M", portfolio_ap_tam_cell(), False),
            (3, "Fiscal years in window (n)", n_years_cell(), False),
            # slide 5 - cost funnel (FY22-27 portfolio)
            (5, "FY22-27 total ship estimate $M", portfolio_scn_cell("total"), False),
            (5, "FY22-27 Basic Construction base $M", portfolio_scn_cell("basic"), False),
            (5, "FY22-27 GFE / directed equipment $M", portfolio_scn_cell("gfe"), False),
            (5, "FY22-27 other non-BC categories $M", portfolio_scn_cell("other_non_bc"), False),
            # slide 6 - MYP redaction trapdoor
            (6, "Outside-yards POP, MYP-corrected", outside_yards_corrected_cell(), True),
            (6, "Outside-yards POP, disclosed artifact", outside_yards_disclosed_cell(), True),
            (6, "MYP masters reconstructed $M", masters_dollar_cell(), False),
            (6, "Gated POP corpus $M (incl. masters)", gated_dollar_cell(), False),
            (6, "GFE / Navy-directed scope dropped $M", gfe_excluded_dollar_cell(), False),
            # slide 7 - supplier-addressable base
            (7, "Supplier-addressable subaward $M (full corpus)", addressable_total_cell(), False),
            # slide 8 - annual TAM build / bridge
            (8, "BC construction base (SCN P-5c, FY22-27) $M", portfolio_bc_base_cell(), False),
            (8, "POP removal - prime / co-prime / GFE $M", pop_removal_cell(), False),
            (8, "BC supplier coefficient (MYP-corrected)", bc_supplier_coeff_cell(), True),
            (8, "AP/LLTM supplier coefficient", ap_lltm_supplier_coeff_cell(), True),
            (8, "Supplier TAM per in-window hull $M", per_hull_tam_cell(), False),
            (8, "BC TAM per in-window hull $M", per_hull_bc_tam_cell(), False),
        ]
        # slide 9 - TAM by fiscal year
        for fy in range(2022, 2028):
            rows.append((9, f"TAM FY{fy-2000} $M", tam_cell(2122, fy), False))
        # slide 11 - work-type bucket TAM allocation (incl. residual)
        for k in BUCKET_KEYS:
            rows.append((11, f"Bucket TAM - {bucket_name[k]} $M", bucket_tam_cell(k), False))
        rows.append((11, "Bucket TAM - unbucketed residual $M", unbucketed_tam_cell(), False))
        # slide 12 - SAM scenario menu (cumulative + annual)
        for sk in bks:
            rows.append((12, f"SAM - {scenario_name(sk)} (cumulative) $M", sam_cell(sk), False))
        for sk in bks:
            rows.append((12, f"SAM avg-annual - {scenario_name(sk)} $M/yr", sam_avg_annual_cell(sk), False))
        # slide 9 extension - penetration & outyear outlook (Outlook tab)
        for fy in range(2022, 2028):
            rows.append((9, f"Outsourced BC penetration FY{fy-2000}", penetration_cell(fy), True))
        rows.append((9, "Outsourced BC penetration, FY22-27 avg", penetration_l6y_cell(), True))
        rows.append((9, "Outsourced BC penetration, FY26-27 avg", penetration_fy2627_cell(), True))
        for fy in range(2028, 2032):
            rows.append((9, f"Implied Outsourced BC low FY{fy-2000} $M", outyear_low_cell(fy), False))
        for fy in range(2028, 2032):
            rows.append((9, f"Implied Outsourced BC high FY{fy-2000} $M", outyear_high_cell(fy), False))
        rows.append((9, "Implied outyear Outsourced BC low $M/yr", outyear_low_avg_cell(), False))
        rows.append((9, "Implied outyear Outsourced BC high $M/yr", outyear_high_avg_cell(), False))
        rows.append((9, "FY22-25 average annual TAM $M/yr", tam_fy2225_avg_cell(), False))
        return [(f"DO-{i:02d}", slide, label, ref, pct)
                for i, (slide, label, ref, pct) in enumerate(rows, start=1)]

    REGISTRY = _build_registry()
    DECK_ROW = {fid: _FIRST_DATA + i for i, (fid, *_rest) in enumerate(REGISTRY)}
    _PCT = {fid: pct for fid, _s, _l, _r, pct in REGISTRY}

    bad = [fid for fid, _s, _l, ref, _p in REGISTRY if "!" not in (ref or "")]
    if bad:
        raise ValueError(f"Deck Outputs figures without a source link: {bad}")

    def value_cell(fid):
        if fid not in DECK_ROW:
            raise ValueError(f"Unknown figure {fid!r}")
        return f"'{_TAB}'!E{DECK_ROW[fid]}"

    def source_ref(fid):
        for f, _s, _l, ref, _p in REGISTRY:
            if f == fid:
                return ref
        raise ValueError(f"Unknown figure {fid!r}")

    def is_pct(fid):
        return _PCT.get(fid, False)

    def _abs(ref):
        return re.sub(r"!\$?([A-Za-z]+)\$?(\d+)$", r"!$\1$\2", ref)

    _DEFINED_NAMES = {
        # Explicit annual vs cumulative (preferred for new deck code).
        "portfolio_tam_annual": _abs(avg_annual_tam_cell()),       # avg annual TAM $M/yr
        "portfolio_tam_cumulative": _abs(_tam_portfolio_tam()),    # FY22-27 cumulative TAM
        "broad_sam_annual": _abs(sam_avg_annual_cell("broad")),    # avg annual broad SAM $M/yr
        "broad_sam_cumulative": _abs(sam_cell("broad")),           # FY22-27 cumulative broad SAM
        "fiscal_year_count": _abs(n_years_cell()),                 # years in window (n)
        # Backward-compatible aliases (cumulative); prefer the *_cumulative names above.
        "portfolio_tam": _abs(_tam_portfolio_tam()),       # TAM Build producer, not SAM
        "portfolio_bc_tam": _abs(portfolio_bc_tam_cell()),
        "portfolio_ap_tam": _abs(portfolio_ap_tam_cell()),
        "bc_supplier_coeff": _abs(bc_supplier_coeff_cell()),
        "sam_broad": _abs(sam_cell("broad")),
    }

    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.banner(_TAB, n_cols=len(_HEADERS), style=S_TITLE_SHEET)
        c.blank()
        c.banner("§1 - Deck figures (one cross-sheet link per slide figure)",
                 n_cols=len(_HEADERS), style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        header_row = c.write(_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT,
                                               S_HEADER_CENTER, S_HEADER_LEFT])
        assert header_row == _HEADER_ROW, f"deck header at {header_row}, expected {_HEADER_ROW}"
        for fid, slide, label, ref, pct in REGISTRY:
            v = S_LINK_PCT if pct else S_LINK_NUM
            c.write([fid, slide, label, f"={ref}", ref],
                    styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, v, S_DEFAULT], outline_level=1)
        last_data = c.at() - 1
        table = ExcelTable(name="tbl_ddg_deck_figures",
                           ref=f"B{header_row}:{col_letter(len(_HEADERS))}{last_data}",
                           headers=_HEADERS)
        ws = worksheet(c.rows, cols=[10, 7, 48, 14, 40], tab_color=group_color(_GROUP), with_gutter=True)
        # Master-workbook namespacing: defined names are workbook-unique, so the
        # DDG register registers its set under a "ddg_" prefix.
        return WorksheetSpec(ws, tables=[table],
                             defined_names={"ddg_" + k: v for k, v in _DEFINED_NAMES.items()})

    return SheetEntry(_TAB, _GROUP, render), REGISTRY, value_cell, source_ref, is_pct


(FIGURE_REGISTER, REGISTRY, value_cell, source_ref, is_pct) = _make_deck_outputs()
