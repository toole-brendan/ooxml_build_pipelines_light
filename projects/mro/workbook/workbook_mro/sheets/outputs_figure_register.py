"""Figure Register

INTENT
    Deck-facing figure contract: one cross-sheet link per slide figure (no manual
    numbers), as a native table. Each Value cell is a pure =accessor() link into a
    producer / model cell; value_cell(fid) is the deck contract. Kept separate from
    Verification Answers (the human-readable answer page).

    Accessors: REGISTRY, value_cell, source_ref, is_pct.

LAYOUT
    row 2 : title
    row 6 : header (title + blank + §1 banner + blank)
    row 7+: §1 deck figures (native tbl_mro_deck_figures)
    B..E  : Figure ID, Slide, Label, Value
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM, S_LINK_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets.model_reconciliation import (
    reconciled_mro_tam_cell, psc1905_mro_cell, public_shipyard_nwcf_cell,
    hii_mt_rev_cell, hii_mt_oi_cell, hii_mt_svc_mix_cell,
)
from workbook_mro.sheets.model_services import navy_tam_svc_cell, cg_tam_svc_cell
from workbook_mro.sheets.model_tam_bridge import (
    topdown_total_cell, bottomup_total_cell, bridge_gap_cell,
)
from workbook_mro.sheets.model_private_addressable import (
    budget_pot_cell, nonpublic_nsy_crosscheck_cell, crosscheck_delta_cell,
)
from workbook_mro.sheets import taxonomy_mro as tx
from workbook_mro.sheets.model_sam_build import (
    sam_cell, sam_pct_tam_cell, selected_sam_cell, selected_sam_pct_cell,
    broad_addressable_cell,
)
from workbook_mro.sheets._layout import RowCursor

_GROUP = "outputs"
_TAB = "Figure Register"
_HEADERS = ["Figure ID", "Slide", "Label", "Value"]
_HEADER_ROW = 6                  # title(2)+blank+§1 banner(4)+blank+header(6)
_FIRST_DATA = 7


def _make_deck_outputs():
    def _build_registry():
        # (slide, label, source-ref, is_pct) - DO ids assigned sequentially below.
        rows = [
            # S05 - TAM sizing / headline
            ("S05", "Reconciled FPDS-visible MRO TAM $M", reconciled_mro_tam_cell(), False),
            ("S05", "Navy services-MRO TAM (65 PSC) $M", navy_tam_svc_cell(), False),
            ("S05", "USCG services-MRO TAM (65 PSC) $M", cg_tam_svc_cell(), False),
            ("S05", "Embedded PSC 1905 MRO (total) $M", psc1905_mro_cell("EMBEDDED"), False),
            # S06 - budget pot vs reconciled MRO TAM bridge
            ("S06", "Budget-anchored MRO funding pot $M", topdown_total_cell(), False),
            ("S06", "Reconciled MRO TAM (bridge bottom-up) $M", bottomup_total_cell(), False),
            ("S06", "Budget pot minus TAM gap $M", bridge_gap_cell(), False),
            ("S06", "Public naval shipyard NWCF $M", public_shipyard_nwcf_cell(), False),
            # S07 - non-public-NSY cross-check
            ("S07", "Non-public-NSY funding cross-check $M", nonpublic_nsy_crosscheck_cell(), False),
            ("S07", "Budget-anchored MRO funding pot $M", budget_pot_cell(), False),
            ("S07", "Non-public-NSY cross-check delta (~$540M) $M", crosscheck_delta_cell(), False),
            # S17 - prime landscape (captive embedded MRO)
            ("S17", "Embedded PSC 1905 MRO - Huntington Ingalls $M", psc1905_mro_cell("HII"), False),
            ("S17", "Embedded PSC 1905 MRO - General Dynamics $M", psc1905_mro_cell("GD"), False),
            ("S17", "HII Mission Technologies FY25 revenue $M", hii_mt_rev_cell(), False),
            ("S17", "HII Mission Technologies FY25 operating income $M", hii_mt_oi_cell(), False),
            ("S17", "HII Mission Technologies FY25 service-revenue mix (% pts)", hii_mt_svc_mix_cell(), False),
        ]
        # S08 - SAM scenario menu (subset of TAM atoms; a menu - not summed)
        rows += [
            ("S08", "Selected SAM $M", selected_sam_cell(), False),
            ("S08", "Selected SAM % of TAM", selected_sam_pct_cell(), True),
            ("S08", "Broad Addressable SAM $M", broad_addressable_cell(), False),
        ]
        rows += [("S08", f"SAM ({tx.SCENARIO_NAME[k]}) $M", sam_cell(k), False)
                 for k in tx.SCENARIO_KEYS]
        rows += [("S08", f"SAM % TAM ({tx.SCENARIO_NAME[k]})", sam_pct_tam_cell(k), True)
                 for k in tx.SCENARIO_KEYS]
        return [(f"DO-{i:02d}", slide, label, ref, pct)
                for i, (slide, label, ref, pct) in enumerate(rows, start=1)]

    REGISTRY = _build_registry()
    DECK_ROW = {fid: _FIRST_DATA + i for i, (fid, *_rest) in enumerate(REGISTRY)}
    _PCT = {fid: pct for fid, _s, _l, _r, pct in REGISTRY}

    bad = [fid for fid, _s, _l, ref, _p in REGISTRY if "!" not in (ref or "")]
    if bad:
        raise ValueError(f"Figure Register figures without a source link: {bad}")

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

    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.banner(_TAB, n_cols=len(_HEADERS), style=S_TITLE_SHEET)
        c.blank()
        c.banner("§1 - Deck figures",
                 n_cols=len(_HEADERS), style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        header_row = c.write(_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT,
                                               S_HEADER_CENTER])
        assert header_row == _HEADER_ROW, f"deck header at {header_row}, expected {_HEADER_ROW}"
        for fid, slide, label, ref, pct in REGISTRY:
            v = S_LINK_PCT if pct else S_LINK_NUM
            c.write([fid, slide, label, f"={ref}"],
                    styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, v], outline_level=1)
        last_data = c.at() - 1
        table = ExcelTable(name="tbl_mro_deck_figures",
                           ref=f"B{header_row}:{col_letter(len(_HEADERS))}{last_data}",
                           headers=_HEADERS)
        ws = worksheet(c.rows, cols=[10, 8, 52, 14], tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[table])

    return SheetEntry(_TAB, _GROUP, render), REGISTRY, value_cell, source_ref, is_pct


(FIGURE_REGISTER, REGISTRY, value_cell, source_ref, is_pct) = _make_deck_outputs()
