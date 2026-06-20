"""SAM Build

INTENT
    The SAM scenario engine - converts the TAM atoms + the editable Scenarios matrix
    into the leadership SAM menu, the selected-scenario SAM, drilldowns, and QA. SAM
    is a scenario-selected SUBSET of mutually-exclusive TAM atoms, never a second TAM:
    every scenario SAM sits inside the one Reconciled FPDS-visible MRO TAM.

    The per-atom inclusion cube lives on the TAM Atoms sheet (one Included flag column
    per scenario + an Included(selected) column, each = a product of per-axis SUMIFS
    against the Scenarios matrix - within-axis OR, across-axis AND). This sheet is a
    compact reader: each menu SAM is one SUMPRODUCT(atom Amount, scenario Included);
    drilldowns add a (tag = bucket) factor on the Included(selected) column.

    Scenario outputs are a MENU - they overlap and must NOT be summed. The §2 QA block
    proves the atom layer reconciles (Σ atoms = TAM, all-on = 100%, every scenario ≤
    TAM) and discloses the depot enrichment deltas.

    Accessors (consumed by Summary / Figure Register / ChartData): sam_cell,
    sam_pct_tam_cell, sam_pct_addr_cell, selected_sam_cell, selected_sam_pct_cell,
    atom_total_cell, qa_atom_delta_cell, broad_addressable_cell, scenario_keys_ordered.

LAYOUT
    row 2 : title
    §1 SAM scenario menu · §2 SAM base & QA · §3 selected scenario · §4 selected drilldowns
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_LABEL_INDENT_1,
    S_NUM, S_PCT, S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets import taxonomy_mro as tx
from workbook_mro.sheets.data_tam_atoms import (
    amount_range, included_range, included_selected_range, axis_tag_range, tag_range,
    atom_id_range, n_atoms, distinct_tags,
)
from workbook_mro.sheets.inputs_assumptions import selected_scenario_cell
from workbook_mro.sheets.model_reconciliation import reconciled_mro_tam_cell

_GROUP = "model"
_TAB = "SAM Build"
_NCOLS = 5                       # B label, C $M, D % TAM, E % Addressable, F note
_SCEN_KEYS = tx.SCENARIO_KEYS
_AMT = amount_range()
_INCSEL = included_selected_range()


def _sam(k: str) -> str:
    return f"=SUMPRODUCT({_AMT},{included_range(k)})"


def _drill(tag_rng: str, bucket: str) -> str:
    return f'=SUMPRODUCT({_AMT},{_INCSEL},({tag_rng}="{bucket}"))'


def _make():
    P: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 SAM scenario menu (the headline; do NOT sum these rows)
    c.banner("§1 - SAM scenario menu (a menu of overlapping options - do NOT sum)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario", "SAM $M", "% of TAM", "% of Addressable", "Interpretation"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER,
                    S_HEADER_LEFT])
    menu_first = c.at()
    scen_row = {k: menu_first + j for j, k in enumerate(_SCEN_KEYS)}
    ba_row = scen_row["broad_addressable"]
    for k in _SCEN_KEYS:
        r = scen_row[k]
        c.write([tx.SCENARIO_NAME[k], _sam(k), f"=C{r}/SUM({_AMT})", f"=C{r}/$C${ba_row}",
                 tx.SCENARIO_INTERP[k]],
                styles=[S_DEFAULT, S_NUM, S_PCT, S_PCT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 SAM base & QA
    c.banner("§2 - SAM base & QA", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Check", "Value", "", "", "Status"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_LEFT,
                    S_HEADER_CENTER])
    P["recon"] = c.write(["Reconciled FPDS-visible MRO TAM $M", f"={reconciled_mro_tam_cell()}"],
                         styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    P["atot"] = c.write(["TAM atoms total $M", f"=SUM({_AMT})"],
                        styles=[S_BOLD, S_NUM], outline_level=1)
    P["delta"] = c.write(["Delta (atoms - reconciled) $M", f"=C{P['atot']}-C{P['recon']}"],
                         styles=[S_DEFAULT, S_NUM], outline_level=1)
    recon, atot, delta = P["recon"], P["atot"], P["delta"]

    def _qa(label, value, status):
        c.write([label, value, None, None, status],
                styles=[S_LABEL_INDENT_1, S_NUM, S_DEFAULT, S_DEFAULT, S_DEFAULT],
                outline_level=1)

    _qa("QA-1  atoms tie to reconciled TAM (|Δ|<5)", f"=C{delta}",
        f'=IF(ABS(C{delta})<5,"OK","FAIL")')
    _qa("QA-2  Broad TAM = atoms total (all-on = 100%)", f"=C{scen_row['broad_tam']}",
        f'=IF(ABS(C{scen_row["broad_tam"]}-C{atot})<0.5,"OK","FAIL")')
    _qa("QA-3  Broad Addressable <= reconciled TAM", f"=C{ba_row}",
        f'=IF(C{ba_row}<=C{recon}+0.5,"OK","FAIL")')
    _qa("QA-4  every scenario SAM <= reconciled TAM",
        f"=MAX(C{menu_first}:C{scen_row[_SCEN_KEYS[-1]]})",
        f'=IF(MAX(C{menu_first}:C{scen_row[_SCEN_KEYS[-1]]})<=C{recon}+0.5,"OK","FAIL")')
    _qa("QA-5  atom-id count = expected (no rows dropped)", f"=COUNTA({atom_id_range()})",
        f'=IF(COUNTA({atom_id_range()})={n_atoms()},"OK","FAIL")')
    c.blank()
    # QA-7 disclosures (depot dollar-source deltas; not pass/fail)
    c.banner("§2b - Depot enrichment disclosures (dollars from Awards; tags from J998J999)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    _depot = f'SUMPRODUCT({_AMT},({axis_tag_range("work_segment")}="{tx.DEPOT_SEGMENT}"))'
    P["depot"] = c.write(["Depot atom total (Awards J998/J999) $M", f"={_depot}"],
                         styles=[S_LABEL_INDENT_1, S_NUM], outline_level=1)
    P["j998"] = c.write(["J998/J999 source total (J998J999Data) $M",
                         "=SUM(J998J999Data[FY2025 Obligation])/1000000"],
                        styles=[S_LABEL_INDENT_1, S_NUM], outline_level=1)
    c.write(["J998/J999 $ not in Awards depot universe $M", f"=C{P['j998']}-C{P['depot']}"],
            styles=[S_LABEL_INDENT_1, S_NUM], outline_level=1)
    c.write(["Unmapped depot atoms (no J998J999 tag match) $M",
             f'=SUMPRODUCT({_AMT},({axis_tag_range("buyer_rmc")}="{tx.UNMAPPED}"))'],
            styles=[S_LABEL_INDENT_1, S_NUM], outline_level=1)
    c.blank(2)

    # §3 Selected scenario
    c.banner("§3 - Selected scenario", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Selected SAM scenario", f"={selected_scenario_cell()}"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    P["selsam"] = c.write(["Selected SAM $M", f"=SUMPRODUCT({_AMT},{_INCSEL})"],
                          styles=[S_BOLD, S_NUM], outline_level=1)
    P["selpct"] = c.write(["Selected SAM % of TAM", f"=C{P['selsam']}/SUM({_AMT})"],
                          styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.blank(2)

    # §4 Selected-scenario drilldowns
    c.banner("§4 - Selected-scenario drilldowns", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()

    def _drill_block(sub, tag_rng, buckets):
        c.banner(sub, n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Bucket", "Selected SAM $M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
        first = c.at()
        for b in buckets:
            c.write([b, _drill(tag_rng, b)],
                    styles=[S_LABEL_INDENT_1, S_NUM], outline_level=1)
        c.total(["Total", f"=SUM(C{first}:C{c.at()-1})"],
                styles=[S_BOLD, S_NUM], n_cols=2, outline_level=1)
        c.blank(2)

    # Drilldown buckets come from distinct_tags(axis) so the display can never drift
    # from the atom universe - the depot-only axes carry the n/a / unmapped sentinels,
    # so every axis total ties to selected SAM even for non-depot scenarios.
    _drill_block("§4a - by work segment", axis_tag_range("work_segment"), tx.WORK_SEGMENT_LABELS)
    _drill_block("§4b - by hull group", tag_range("Hull Group"), tx.HULL_GROUP_LABELS)
    _drill_block("§4c - by buyer / RMC (incl. n/a non-depot)", axis_tag_range("buyer_rmc"),
                 distinct_tags("buyer_rmc"))
    _drill_block("§4d - by contractor tier (incl. n/a non-depot)", axis_tag_range("contractor_tier"),
                 distinct_tags("contractor_tier"))

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[52, 14, 12, 16, 60], tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws)

    # accessors
    def sam_cell(k): return f"'{_TAB}'!C{scen_row[k]}"
    def sam_pct_tam_cell(k): return f"'{_TAB}'!D{scen_row[k]}"
    def sam_pct_addr_cell(k): return f"'{_TAB}'!E{scen_row[k]}"
    def atom_total_cell(): return f"'{_TAB}'!C{P['atot']}"
    def qa_atom_delta_cell(): return f"'{_TAB}'!C{P['delta']}"
    def broad_addressable_cell(): return f"'{_TAB}'!C{ba_row}"
    def selected_sam_cell(): return f"'{_TAB}'!C{P['selsam']}"
    def selected_sam_pct_cell(): return f"'{_TAB}'!C{P['selpct']}"
    def scenario_keys_ordered(): return list(_SCEN_KEYS)

    acc = dict(sam_cell=sam_cell, sam_pct_tam_cell=sam_pct_tam_cell,
               sam_pct_addr_cell=sam_pct_addr_cell, atom_total_cell=atom_total_cell,
               qa_atom_delta_cell=qa_atom_delta_cell, broad_addressable_cell=broad_addressable_cell,
               selected_sam_cell=selected_sam_cell, selected_sam_pct_cell=selected_sam_pct_cell,
               scenario_keys_ordered=scenario_keys_ordered)
    return SheetEntry(_TAB, _GROUP, render), acc


SAM_BUILD, _ACC = _make()

sam_cell = _ACC["sam_cell"]
sam_pct_tam_cell = _ACC["sam_pct_tam_cell"]
sam_pct_addr_cell = _ACC["sam_pct_addr_cell"]
atom_total_cell = _ACC["atom_total_cell"]
qa_atom_delta_cell = _ACC["qa_atom_delta_cell"]
broad_addressable_cell = _ACC["broad_addressable_cell"]
selected_sam_cell = _ACC["selected_sam_cell"]
selected_sam_pct_cell = _ACC["selected_sam_pct_cell"]
scenario_keys_ordered = _ACC["scenario_keys_ordered"]
