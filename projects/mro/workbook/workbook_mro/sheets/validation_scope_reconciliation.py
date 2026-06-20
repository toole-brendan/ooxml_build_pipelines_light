"""Scope Reconciliation

INTENT
    10-bar waterfall reconciling top-down OMN ship-maintenance budget authority to
    bottom-up FPDS-visible MRO TAM. Every $ cell is a cross-sheet pull through the
    Reconciliation / Services / OP-5 / MSC-SCN-USCG accessors, or intra-sheet arithmetic
    over the captured BAR rows. Green S_LINK_NUM marks a bare =accessor() pull; a scaled
    or combined value (accessor/1000, sums, rebases) is derived black S_NUM.

LAYOUT
    row 2 : title
    B..D  : Step / Component / $M ($M in col D so the =D{bar} waterfall stays stable)
    §1 waterfall map (5-col) · §5 pre/post-rebase (B..E) · §10 think-cell paste
    (B..L, widest, sets _NCOLS)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_LABEL_INDENT_1,
    S_NUM, S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets.model_reconciliation import (
    omn_cell, mro_tas_cell, psc1905_mro_cell, public_shipyard_nwcf_cell,
    reconciled_mro_tam_cell,
)
from workbook_mro.sheets.model_services import navy_tam_svc_cell, cg_tam_svc_cell
from workbook_mro.sheets.model_op5_navy_topdown import (
    op5_total_cell, op5_public_nsy_cell, op5_private_cell,
)
from workbook_mro.sheets.model_msc_scn_uscg_topdown import (
    msc_mr_fy25_transfer_cell, scn_cvn_rcoh_li2086_cell, uscg_isvs_floor_cell,
)

_GROUP = "validation"
_TAB = "Scope Reconciliation"
_NCOLS = 11                     # B..L (the §10 paste block is the widest)
_COLS = [6, 44, 16, 16, 16, 16, 16, 16, 16, 16, 16]
_HDR5 = [S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_LEFT]


def _tam():
    return f"({navy_tam_svc_cell()}+{cg_tam_svc_cell()})"


def _rebased(key):
    """MRO_TAS_<key> rebased to Services TAM: TAS_key * (Navy+CG) / TAS_total."""
    return f"{mro_tas_cell(key)}*{_tam()}/{mro_tas_cell('TOTAL')}"


def _make():
    P: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    def _section(title, n_cols=3):
        # Banner spans the section's own width, not the sheet maximum (_NCOLS=11, set by
        # the §10 paste block). Most sections are 3 cols (Step / Component / $M).
        c.banner(title, n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()

    def _hdr(labels):
        c.write(labels, styles=_HDR5[:len(labels)], outline_level=1)

    def _vrow(step, comp, val, *, bar=False, divider=None, indent=False, link=False, key=None):
        vals = [step, comp, val]
        if divider is None:
            divider = bar          # a lone section bar draws its own subtotal divider
        if divider:
            # Subtotal divider: c.total() upgrades the base styles to the bordered variants
            # so the top medium-border runs continuously across the row.
            r = c.total(vals, styles=[S_BOLD, S_BOLD, S_NUM], n_cols=3, outline_level=1)
        elif bar:
            # An emphasized waterfall bar WITHOUT the top-border divider - used where several
            # bars stack consecutively (§6 addbacks) so they don't read as a wall of heavy
            # lines; the single divider goes on the subtotal below them.
            r = c.write(vals, styles=[S_BOLD, S_BOLD, S_NUM], outline_level=1)
        else:
            lstyle = S_LABEL_INDENT_1 if indent else S_DEFAULT
            vstyle = S_LINK_NUM if link else S_NUM
            r = c.write(vals, styles=[S_DEFAULT, lstyle, vstyle], outline_level=1)
        if key:
            P[key] = r
        return r

    # §1 - Waterfall structure
    _section("§1 - Waterfall structure", n_cols=5)
    _hdr(["Bar #", "Bar Name", "Type", "Basis", "Feeds from"])
    _MAP = [
        ("1", "OMN Ship-Maint Budget Authority", "Start (s)", "Top-down", "Section 2"),
        ("2", "Non-Contract Allocation", "Decrement (d)", "Top-down residual", "Section 4"),
        ("3", "OMN Contracted Slice (CE 928)", "Intermediate (e)", "Top-down", "Section 3"),
        ("4", "+FPDS obligations from OPN", "Addback (s)", "Bottom-up (rebased)", "Section 6"),
        ("5", "+FPDS obligations from USCG", "Addback (s)", "Bottom-up (rebased)", "Section 6"),
        ("6", "+FPDS obligations from RDT&E-DW", "Addback (s)", "Bottom-up (rebased)",
         "Section 6"),
        ("7", "+FPDS obligations - SCN / Navy other / AF / Army / DW other", "Addback (s)",
         "Bottom-up (rebased)", "Section 6"),
        ("8", "Services MRO TAM (FPDS, 65 PSCs, post-excl)", "Intermediate (e)",
         "Bottom-up", "Section 7"),
        ("9", "+PSC 1905 Embedded MRO", "Addback (s)", "Bottom-up (classifier)", "Section 8"),
        ("10", "Reconciled FPDS-visible MRO TAM", "End (e)", "Final", "Section 9"),
    ]
    for row in _MAP:
        c.write(list(row), styles=[S_DEFAULT] * 5, outline_level=1)
    c.blank(2)

    # §2 - OMN ship-maintenance budget authority
    _section("§2 - OMN ship-maintenance budget authority")
    _hdr(["Step", "Component", "$M"])
    _vrow("2.1", "OMN 1B2B - Ship Operational Support & Training (SAG total)",
          f"={omn_cell('1B2B_TOTAL')}/1000")
    _vrow("2.2", "OMN 1B4B - Ship Maintenance (SAG total)",
          f"={omn_cell('1B4B_TOTAL')}/1000")
    _vrow("2.3", "OMN 1B5B - Ship Depot Operations Support (SAG total)",
          f"={omn_cell('1B5B_TOTAL')}/1000")
    _vrow("BAR 1", "OMN Ship-Maintenance Budget Authority (2.1 + 2.2 + 2.3)",
          f"=({omn_cell('1B2B_TOTAL')}+{omn_cell('1B4B_TOTAL')}+{omn_cell('1B5B_TOTAL')})/1000",
          bar=True, key="bar1")
    c.blank(2)

    # §3 - CE 928 by-contract slice
    _section("§3 - CE 928 by-contract slice")
    _hdr(["Step", "Component", "$M"])
    _vrow("3.1", "OMN 1B2B - CE 928 Ship Maintenance By Contract",
          f"={omn_cell('1B2B_CONTRACT')}/1000")
    _vrow("3.2", "OMN 1B4B - CE 928 Ship Maintenance By Contract",
          f"={omn_cell('1B4B_CONTRACT')}/1000")
    _vrow("3.3", "OMN 1B5B - CE 928 Ship Maintenance By Contract",
          f"={omn_cell('1B5B_CONTRACT')}/1000")
    _vrow("BAR 3", "OMN Contracted Slice (CE 928 total across 3 SAGs)",
          f"=({omn_cell('1B2B_CONTRACT')}+{omn_cell('1B4B_CONTRACT')}+{omn_cell('1B5B_CONTRACT')})/1000",
          bar=True, key="bar3")
    c.blank(2)

    # §4 - Non-contract allocation
    _section("§4 - Non-contract allocation")
    _hdr(["Step", "Component", "$M"])
    _vrow("BAR 2", "Non-contract allocation (residual)",
          lambda r: f"=D{P['bar1']}-D{P['bar3']}", bar=True, key="bar2")
    _vrow("4.1", "of which: Public naval shipyard NWCF labor (est.)",
          f"={public_shipyard_nwcf_cell()}", indent=True, link=True)
    _vrow("4.2", "of which: Material, IMA, government support (implied)",
          f"=D{P['bar2']}-{public_shipyard_nwcf_cell()}", indent=True)
    c.blank(2)

    # §5 - FPDS MRO obligations by appropriation
    _section("§5 - FPDS MRO obligations by appropriation", n_cols=4)
    c.write(["Step", "Appropriation", "$M (pre)", "$M (post-rebase)"],
            styles=[S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER],
            outline_level=1)
    _TAS = [
        ("5.1", "OMN (Operation & Maintenance, Navy, 017-1804)", "OMN"),
        ("5.2", "OPN (Other Procurement, Navy, 017-1810)", "OPN"),
        ("5.3", "RDT&E, Defense-Wide (097-0400)", "RDTE_DW"),
        ("5.4", "SCN (Shipbuilding & Conversion, Navy, 017-1611)", "SCN"),
        ("5.5", "Navy - other appropriations (APN/WPN/etc.)", "NAVY_OTHER"),
        ("5.6", "USCG (OE + AC&I, 070-*)", "USCG"),
        ("5.7", "Air Force (057-*)", "AIR_FORCE"),
        ("5.8", "Army (021-*)", "ARMY"),
        ("5.9", "Defense-Wide - other", "DW_OTHER"),
        ("5.10", "Other federal agencies", "OTHER_AGENCY"),
    ]
    first5 = c.at()
    for step, appr, key in _TAS:
        c.write([step, appr, f"={mro_tas_cell(key)}/1000", f"={_rebased(key)}"],
                styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_NUM], outline_level=1)
    last5 = c.at() - 1
    c.write(["5.T", "TAS total (pre-rebase)",
             f"=SUM(D{first5}:D{last5})"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["5.T+", "TAS total (post-rebase = Services TAM)",
             f"=SUM(E{first5}:E{last5})"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["5.R", "Rebase factor (Services TAM / TAS total)",
             f"={_tam()}/({mro_tas_cell('TOTAL')}/1000)"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.blank(2)

    # §6 - Cross-appropriation addbacks
    _section("§6 - Cross-appropriation addbacks")
    _hdr(["Step", "Bar", "$M (rebased)"])
    _vrow("BAR 4", "+FPDS obligations from OPN (Other Procurement, Navy)",
          f"={_rebased('OPN')}", bar=True, divider=False, key="bar4")
    _vrow("BAR 5", "+FPDS obligations from USCG (OE + AC&I)",
          f"={_rebased('USCG')}", bar=True, divider=False, key="bar5")
    _vrow("BAR 6", "+FPDS obligations from RDT&E, Defense-Wide",
          f"={_rebased('RDTE_DW')}", bar=True, divider=False, key="bar6")
    _vrow("BAR 7", "+FPDS obligations - SCN / Navy other / AF / Army / DW other / Other agency",
          f"=({mro_tas_cell('SCN')}+{mro_tas_cell('NAVY_OTHER')}+{mro_tas_cell('AIR_FORCE')}"
          f"+{mro_tas_cell('ARMY')}+{mro_tas_cell('DW_OTHER')}+{mro_tas_cell('OTHER_AGENCY')})"
          f"*{_tam()}/{mro_tas_cell('TOTAL')}",
          bar=True, divider=False, key="bar7")
    _vrow("6.T", "Addback subtotal (BARS 4 + 5 + 6 + 7)",
          lambda r: f"=D{P['bar4']}+D{P['bar5']}+D{P['bar6']}+D{P['bar7']}", divider=True)
    _vrow("6.X", "Cross-check: Services TAM - OMN (post-rebase)",
          f"={navy_tam_svc_cell()}+{cg_tam_svc_cell()}-{_rebased('OMN')}", indent=True)
    c.blank(2)

    # §7 - Services MRO TAM
    _section("§7 - Services MRO TAM")
    _hdr(["Step", "Component", "$M"])
    _vrow("7.1", "Navy services-PSC MRO TAM (65 J/K/N/M/H/L codes, post-exclusion)",
          f"={navy_tam_svc_cell()}", link=True)
    _vrow("7.2", "USCG services-PSC MRO TAM (post-exclusion)",
          f"={cg_tam_svc_cell()}", link=True)
    _vrow("BAR 8", "Services MRO TAM (FPDS, 65 PSCs, post-exclusion)",
          f"={navy_tam_svc_cell()}+{cg_tam_svc_cell()}", bar=True, key="bar8")
    c.blank(2)

    # §8 - PSC 1905 embedded MRO addback
    _section("§8 - PSC 1905 embedded MRO addback")
    _hdr(["Step", "Component", "$M"])
    _vrow("BAR 9", "+PSC 1905 embedded MRO (classifier-locked, Central bound)",
          f"={psc1905_mro_cell('EMBEDDED')}", bar=True, key="bar9")
    _vrow("8.1", "of which Submarines", f"={psc1905_mro_cell('SUBS')}", indent=True, link=True)
    _vrow("8.2", "of which Aircraft Carriers", f"={psc1905_mro_cell('CARRIERS')}",
          indent=True, link=True)
    _vrow("8.3", "of which Surface Combatants", f"={psc1905_mro_cell('SURFCOMBS')}",
          indent=True, link=True)
    _vrow("8.4", "of which Unclassified-vessel", f"={psc1905_mro_cell('UNCL')}",
          indent=True, link=True)
    c.blank(2)

    # §9 - Reconciled FPDS-visible MRO TAM
    _section("§9 - Reconciled FPDS-visible MRO TAM")
    _hdr(["Step", "Component", "$M"])
    _vrow("BAR 10", "Reconciled FPDS-visible MRO TAM (Services + PSC 1905 embedded)",
          f"={reconciled_mro_tam_cell()}", bar=True, key="bar10")
    c.blank(2)

    # §10 - Think-cell waterfall paste block
    _section("§10 - Think-cell waterfall paste block", n_cols=_NCOLS)
    c.write(["Category / Series", "OMN Ship-Maint Auth", "-Non-contract alloc",
             "CE 928 contracted slice", "+OPN", "+USCG", "+RDT&E-DW",
             "+Other (SCN/Navy/AF/Army/DW/Agency)", "Services MRO TAM", "+PSC 1905 Embedded",
             "Reconciled MRO TAM"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 10, outline_level=1)
    _bars = ["bar1", "bar2", "bar3", "bar4", "bar5", "bar6", "bar7", "bar8", "bar9", "bar10"]
    vals = [f"=D{P['bar1']}", f"=-D{P['bar2']}"] + [f"=D{P[b]}" for b in _bars[2:]]
    c.write(["FY2025 $M"] + vals, styles=[S_DEFAULT] + [S_NUM] * 10, outline_level=1)
    c.write(["Bar type", "s", "d", "e", "s", "s", "s", "s", "e",
             "s", "e"], styles=[S_DEFAULT] * 11, outline_level=1)
    c.blank(2)

    # §11 - 2x2 scope matrix
    _section("§11 - 2x2 scope matrix")
    c.write([None, "MRO scope ($M)", "Adjacent scope ($M, not MRO)"],
            styles=[S_DEFAULT, S_BOLD, S_BOLD], outline_level=1)
    c.write(["FPDS-visible", f"={reconciled_mro_tam_cell()}",
             f"=38053-{psc1905_mro_cell('EMBEDDED')}"],
            styles=[S_BOLD, S_LINK_NUM, S_NUM], outline_level=1)
    c.write(["Not FPDS", f"={public_shipyard_nwcf_cell()}", "Non-addressable (out of scope)"],
            styles=[S_BOLD, S_LINK_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §12 - Validation & parity checks
    _section("§12 - Validation & parity checks")
    _hdr(["Check", "Description", "Computed value"])
    c.write(["12.1", "Waterfall closure: BAR 3 + BARS 4-7 + BAR 9 vs BAR 10",
             f"=D{P['bar3']}+D{P['bar4']}+D{P['bar5']}+D{P['bar6']}+D{P['bar7']}+D{P['bar9']}"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["12.2", "Services TAM closure: CE 928 + addbacks (4-7) vs Services MRO TAM",
             f"=D{P['bar3']}+D{P['bar4']}+D{P['bar5']}+D{P['bar6']}+D{P['bar7']}"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["12.3", "CE 928 / MRO_TAS_OMN parity gap (top-down vs bottom-up OMN)",
             f"=D{P['bar3']}-{_rebased('OMN')}"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["12.4", "Public-yard anchor vs non-contract residual (BAR 2)",
             f"=D{P['bar2']}-{public_shipyard_nwcf_cell()}"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["12.5", "Reconciled TAM identity (Services + PSC 1905 embedded)",
             f"={reconciled_mro_tam_cell()}-({navy_tam_svc_cell()}+{cg_tam_svc_cell()}+{psc1905_mro_cell('EMBEDDED')})"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.blank(2)

    # §13 - Dual-narrative bridge reference
    _section("§13 - Dual-narrative bridge reference")
    _hdr(["Check", "Description", "Computed value"])
    c.write(["13.1", "OP-5 Table IV total vs OMN 1B4B SAG total",
             f"={op5_total_cell()}-{omn_cell('1B4B_TOTAL')}"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["13.2", "Top-down partial grand total (sourced components)",
             f"=({op5_total_cell()}+{msc_mr_fy25_transfer_cell()}+{scn_cvn_rcoh_li2086_cell(2025)}+{uscg_isvs_floor_cell()})/1000"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["13.3", "Public NSY structural gap",
             f"={op5_public_nsy_cell()}/1000"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["13.4", "Private-side reconciliation anchor",
             f"={op5_private_cell()}/1000"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)
    c.write(["13.5", "USCG ISVS floor anchor", f"={uscg_isvs_floor_cell()}/1000"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


SCOPE_RECONCILIATION = _make()
