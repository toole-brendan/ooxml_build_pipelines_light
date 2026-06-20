"""z_ChartData

INTENT
    Production-support tab (off the analytical read): one think-cell paste block per
    deck chart, laid out as the embedded datasheet wants it - category / step labels
    across the top row, value series beneath - and styled as a copy-paste-ready range
    (pale-yellow fill + thin black perimeter, the S_PASTE_* styles). The z_ prefix
    sorts the tab last. Values are live SUMIFS over Awards / J998J999Data plus the
    producer accessors. The deck-loader chart ids are kept in code (the section titles)
    but stripped from the rendered banner text. Pure consumer (exports no accessors;
    deck-loader leaf).

    think-cell waterfall convention here keeps an explicit "Bar type" row (s/d/e) beneath
    the value row, included inside the paste rectangle so think-cell reads it.

LAYOUT
    row 2 : title
    §1-§13 chart blocks, one paste rectangle per deck exhibit
"""
from __future__ import annotations

import re

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_TITLE_SHEET, S_TITLE_SECTION,
    S_PASTE_HEADER_TL, S_PASTE_HEADER_T, S_PASTE_HEADER_TR,
    S_PASTE_LABEL_L, S_PASTE_LABEL_BL,
    S_PASTE_VAL_INT_M, S_PASTE_VAL_R_M, S_PASTE_VAL_B_M, S_PASTE_VAL_BR_M,
    S_PASTE_VAL_INT_P, S_PASTE_VAL_R_P, S_PASTE_VAL_B_P, S_PASTE_VAL_BR_P,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets._crosstab import WORK_SEGMENTS, PSC_CODES
from workbook_mro.sheets import taxonomy_mro as tx
from workbook_mro.sheets.data_tam_atoms import (
    amount_range, included_selected_range, axis_tag_range,
)
from workbook_mro.sheets.model_sam_build import sam_cell, selected_sam_cell
from workbook_mro.sheets.model_reconciliation import (
    omn_cell, mro_tas_cell, psc1905_mro_cell, reconciled_mro_tam_cell,
    hii_mt_rev_cell, hii_mt_oi_cell,
)
from workbook_mro.sheets.model_services import navy_tam_svc_cell, cg_tam_svc_cell
from workbook_mro.sheets.model_op5_navy_topdown import (
    op5_public_nsy_cell, op5_private_cell,
)
from workbook_mro.sheets.model_msc_scn_uscg_topdown import (
    msc_mr_fy25_transfer_cell, scn_cvn_rcoh_li2086_cell, opn_li1000_cell,
    uscg_isvs_floor_cell,
)

_GROUP = "chartdata"
_TAB = "z_ChartData"
_NCOLS = 25                     # B..Z (the §3 segment x hull cross-tab is the widest)
_COLS = [34] + [14] * 24        # readable paste-block headers (was 11-wide and cramped)
_OBL = "FY2025 Obligation"
_CHART_KEY_RE = re.compile(r"\s*\[[^\]]+\]\s*$")


def _visible_title(title: str) -> str:
    """Strip the trailing deck-loader [chart_key] tag from visible banner text."""
    return _CHART_KEY_RE.sub("", title).rstrip()

_SEG = {name: codes for name, codes in WORK_SEGMENTS}
_DEPOT = _SEG["Depot Ship Repair"]
_HME = _SEG["Hull, Mechanical & Electrical (HM&E)"]
_COMBAT = _SEG["Combat Systems Sustainment"]
_ELEC = _SEG["Electronics & C4ISR Sustainment"]
_PORT = _SEG["Port & Technical Services"]
# Service-PSC segment rows shared by §1/§8 (Nuclear handled per-block).
_SERVICE_SEGS = [
    ("Depot Ship Repair", _DEPOT), ("Hull, Mechanical & Electrical (HM&E)", _HME),
    ("Combat Systems Sustainment", _COMBAT), ("Electronics & C4ISR Sustainment", _ELEC),
    ("Port & Technical Services", _PORT),
]
# Row order for the segment x N blocks (§2/§3/§4/§8): Depot, Nuclear (None sentinel),
# HM&E, Combat, Electronics, Port.
_ROW_ORDER = [_SERVICE_SEGS[0], None] + _SERVICE_SEGS[1:]

_VESSEL_CATS = ["Surface Combatants", "Amphibious Warfare Ships", "Submarines",
                "Combat Logistics Ships", "Aircraft Carriers"]            # §2 (+Other)
_HULLS_22 = ["DDG", "SSBN", "LPD", "SSN", "CVN", "T-AO", "LCS", "LHA", "LHD", "LSD",
             "T-AKE", "CG", "FFG", "ESB", "T-EPF", "T-AOE", "T-AH", "OPC", "AS", "WMSL",
             "WMEC", "WPC"]                                               # §3
_MARAUDER_HULLS = tx.MARAUDER_HULLS                                       # §4
# Taxonomy-owned vocabularies (consolidated in taxonomy_mro so this tab stops
# being the hidden model brain; the SAM atom layer keys off the same strings).
_PRIMES_TAM = tx.PRIMES_TAM
_PRIMES_DEPOT = tx.PRIMES_DEPOT
_RMC_BUCKETS = tx.RMC_BUCKETS
_IDV_SCOPES = tx.IDV_SCOPES
_CONTRACTOR_TIERS = tx.CONTRACTOR_TIER_LABELS


def _arr(codes):
    return "{" + ",".join(f'"{c}"' for c in codes) + "}"


def _seg_total(codes, *crit):
    """SUM(SUMIFS(Awards[FY2025 Obligation],Awards[PSC],{codes}[,col,val]))/1e6."""
    parts = f"Awards[PSC],{_arr(codes)}"
    for col, val in crit:
        parts += f',Awards[{col}],"{val}"'
    return f"SUM(SUMIFS(Awards[{_OBL}],{parts}))/1000000"


def _jdepot(prime, rmcs):
    """Depot (J998/J999) $ for a prime across one or more RMC buckets ($M)."""
    terms = "+".join(
        f'SUM(SUMIFS(J998J999Data[{_OBL}],J998J999Data[PSC],{_arr(_DEPOT)},'
        f'J998J999Data[Corporate Parent],"{prime}",J998J999Data[RMC],"{r}"))'
        for r in rmcs)
    return f"({terms})/1000000"


def _geo(tier, rmcs):
    """Tier $ across one or more RMC buckets ($M) - §7 (plain SUMIFS, no PSC array)."""
    terms = "+".join(
        f'SUMIFS(J998J999Data[{_OBL}],J998J999Data[Contractor Tier],"{tier}",'
        f'J998J999Data[RMC],"{r}")' for r in rmcs)
    return f"({terms})/1000000"


def _scope_net(tier, scopes):
    """In-scope (total - FMS) $ for a tier across IDV scope group(s), blanked if < $0.5M."""
    pos = "+".join(
        f'SUMIFS(J998J999Data[{_OBL}],J998J999Data[Contractor Tier],"{tier}",'
        f'J998J999Data[IDV Scope Group],"{s}")/1000000' for s in scopes)
    neg = "+".join(
        f'SUMIFS(J998J999Data[{_OBL}],J998J999Data[Contractor Tier],"{tier}",'
        f'J998J999Data[IDV Scope Group],"{s}",J998J999Data[Availability Group],'
        f'"Out of Scope (FMS)")/1000000' for s in scopes)
    expr = f"(({pos})-({neg}))"
    return f'IF(ABS({expr})<0.5,"",{expr})'


def _sam_drill_seg(seg):
    """Selected-scenario SAM $M for one work segment (atom SUMPRODUCT)."""
    return (f'=SUMPRODUCT({amount_range()},{included_selected_range()},'
            f'({axis_tag_range("work_segment")}="{seg}"))')


def _rebased(key):
    return f"{mro_tas_cell(key)}*({navy_tam_svc_cell()}+{cg_tam_svc_cell()})/{mro_tas_cell('TOTAL')}"


# --- think-cell paste-range emitter ---------------------------------------
# Per unit, the value-cell styles for {interior, right edge, bottom edge,
# bottom-right corner}. The left column is always a label (S_PASTE_LABEL_*),
# the top row always a header (S_PASTE_HEADER_*), so values never sit on the
# top or left edge.
_VAL_STYLE = {
    "M": {"INT": S_PASTE_VAL_INT_M, "R": S_PASTE_VAL_R_M, "B": S_PASTE_VAL_B_M, "BR": S_PASTE_VAL_BR_M},
    "P": {"INT": S_PASTE_VAL_INT_P, "R": S_PASTE_VAL_R_P, "B": S_PASTE_VAL_B_P, "BR": S_PASTE_VAL_BR_P},
}


def _paste_block(c, title, header, rows, unit):
    """Emit one think-cell paste rectangle: section banner, one blank, then the
    bordered grid (header row + data rows), then two blank rows.

    header: full top row; header[0] is the (blank) corner, header[1:] are the
        across-the-top category / step labels. rows: list of (row_label, [values])
        where row_label fills the left column and values align to header[1:]. A value
        is a formula string ("=..."), a waterfall marker ("s"/"d"/"e"), None (blank),
        or a callable resolved against its row (for self-referential "Other" cells).
    unit: "M" / "P" applied to every value row, or a per-row list of units.
    """
    # Banner spans the block's own width (the header), not the sheet maximum, so a
    # narrow chart block (§1/§5/§10/§12) no longer fills clear across B:Z. The
    # [chart_key] tag is dropped from the visible text but kept in `title` in code.
    c.banner(_visible_title(title), n_cols=len(header),
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    ncol = len(header) - 1
    c.write(header,
            styles=[S_PASTE_HEADER_TL] + [S_PASTE_HEADER_T] * (ncol - 1) + [S_PASTE_HEADER_TR],
            outline_level=1)
    n = len(rows)
    for i, (label, vals) in enumerate(rows):
        last = (i == n - 1)
        u = unit[i] if isinstance(unit, (list, tuple)) else unit
        vs = _VAL_STYLE[u]
        styles = [S_PASTE_LABEL_BL if last else S_PASTE_LABEL_L]
        for j in range(1, ncol + 1):
            if last:
                styles.append(vs["BR"] if j == ncol else vs["B"])
            else:
                styles.append(vs["R"] if j == ncol else vs["INT"])
        c.write([label, *vals], styles=styles, outline_level=1)
    c.blank(2)


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    recon = reconciled_mro_tam_cell()

    # §1 MRO Work Segments (ranked column)
    _paste_block(c, "§1 - MRO Work Segments  [mro_work_segments]",
                 ["Work Segment", "FY2025 $M"],
                 [("Depot Ship Repair", [f"={_seg_total(_DEPOT)}"]),
                  ("Nuclear & Complex Overhauls", [f"={psc1905_mro_cell('EMBEDDED')}"]),
                  ("Hull, Mechanical & Electrical (HM&E)", [f"={_seg_total(_HME)}"]),
                  ("Combat Systems Sustainment", [f"={_seg_total(_COMBAT)}"]),
                  ("Electronics & C4ISR Sustainment", [f"={_seg_total(_ELEC)}"]),
                  ("Port & Technical Services", [f"={_seg_total(_PORT)}"])],
                 "M")

    # §2 TAM Composition (segment x vessel category)
    s2_rows = []
    for item in _ROW_ORDER:
        if item is None:                          # Nuclear & Complex Overhauls row
            s2_rows.append(("Nuclear & Complex Overhauls",
                            [f"={psc1905_mro_cell('SURFCOMBS')}", None,
                             f"={psc1905_mro_cell('SUBS')}", None,
                             f"={psc1905_mro_cell('CARRIERS')}", f"={psc1905_mro_cell('UNCL')}"]))
            continue
        name, codes = item
        cats = [f"={_seg_total(codes, ('Vessel Type', v))}" for v in _VESSEL_CATS]
        other = (lambda r, codes=codes: f"={_seg_total(codes)}-SUM(C{r}:G{r})")
        s2_rows.append((name, cats + [other]))
    _paste_block(c, "§2 - TAM Composition  [tam_composition]",
                 ["Category / Series"] + _VESSEL_CATS + ["Other"], s2_rows, "M")

    # §3 TAM Composition: Hull Program Dominance (segment x 22 hulls + Other + Uncl)
    lo, hi = col_letter(2), col_letter(1 + len(_HULLS_22))   # hull cols C..X
    z_col = col_letter(3 + len(_HULLS_22))                   # (Uncl) -> Z
    s3_rows = []
    for item in _ROW_ORDER:
        if item is None:                          # Nuclear & Complex Overhauls row
            cells = [None] * 22
            cells[_HULLS_22.index("DDG")] = f"={psc1905_mro_cell('DDG')}"
            cells[_HULLS_22.index("SSN")] = f"={psc1905_mro_cell('SSN')}"
            cells[_HULLS_22.index("CVN")] = f"={psc1905_mro_cell('CVN')}"
            cells[_HULLS_22.index("LCS")] = f"={psc1905_mro_cell('LCS')}"
            other = (lambda r: f"={psc1905_mro_cell('EMBEDDED')}-SUM({lo}{r}:{hi}{r})-{z_col}{r}")
            s3_rows.append(("Nuclear & Complex Overhauls",
                            cells + [other, f"={psc1905_mro_cell('UNCL')}"]))
            continue
        name, codes = item
        hulls = [f"={_seg_total(codes, ('Hull Program', h))}" for h in _HULLS_22]
        other = (lambda r, codes=codes: f"={_seg_total(codes)}-SUM({lo}{r}:{hi}{r})-{z_col}{r}")
        uncl = f"={_seg_total(codes, ('Hull Program', ''))}"
        s3_rows.append((name, hulls + [other, uncl]))
    _paste_block(c, "§3 - TAM Composition: Hull Program Dominance  [tam_composition_hull_detail]",
                 ["Work Segment"] + _HULLS_22 + ["Other", "(Uncl)"], s3_rows, "M")

    # §4 Marauder-Like Fleet MRO (segment x 14 marauder hulls)
    s4_rows = []
    for item in _ROW_ORDER:
        if item is None:                          # Nuclear row: blank across all hulls
            s4_rows.append(("Nuclear & Complex Overhauls", [None] * len(_MARAUDER_HULLS)))
            continue
        name, codes = item
        s4_rows.append((name, [f"={_seg_total(codes, ('Hull Program', h))}"
                               for h in _MARAUDER_HULLS]))
    _paste_block(c, "§4 - Marauder-Like Fleet MRO  [marauder_like_fleet_mro]",
                 ["Work Segment / Hull"] + _MARAUDER_HULLS, s4_rows, "M")

    # §5 SAM Scenario Menu (atom-based; sourced from SAM Build - a menu, NOT summed)
    _paste_block(c, "§5 - SAM Scenario Menu  [sam_scenario_menu]",
                 ["Scenario", "FY2025 SAM $M"],
                 [(tx.SCENARIO_NAME[k], [f"={sam_cell(k)}"]) for k in tx.SCENARIO_KEYS],
                 "M")

    # §5b Selected Scenario Drilldown (selected SAM by work segment, from the atoms)
    _paste_block(c, "§5b - Selected Scenario Drilldown  [sam_selected_drilldown]",
                 ["Work Segment", "Selected SAM $M"],
                 [("Selected SAM (total)", [f"={selected_sam_cell()}"])]
                 + [(seg, [_sam_drill_seg(seg)]) for seg in tx.WORK_SEGMENT_LABELS],
                 "M")

    # §6 Depot Spend Structure (tier x IDV scope, FMS-net, blanked < $0.5M)
    _paste_block(c, "§6 - Depot Spend Structure  [depot_spend_structure]",
                 ["Category / Series"] + [lbl for lbl, _ in _IDV_SCOPES],
                 [(label, [f"={_scope_net(tier, scopes)}" for _lbl, scopes in _IDV_SCOPES])
                  for label, tier in _CONTRACTOR_TIERS],
                 "M")

    # §7 Depot Geographic Footprint (tier x RMC bucket)
    _paste_block(c, "§7 - Depot Geographic Footprint  [depot_geographic_footprint]",
                 ["Category / Series"] + [lbl for lbl, _ in _RMC_BUCKETS],
                 [(label, [f"={_geo(tier, rmcs)}" for _lbl, rmcs in _RMC_BUCKETS])
                  for label, tier in _CONTRACTOR_TIERS],
                 "M")

    # §8 Prime Landscape - TAM (segment x prime)
    np = len(_PRIMES_TAM)
    s8_rows = []
    for item in _ROW_ORDER:
        if item is None:                          # Nuclear row: GD / HII / BAE columns
            cells = [None] * np
            cells[0] = f"={psc1905_mro_cell('GD')}"
            cells[1] = f"={psc1905_mro_cell('HII')}"
            cells[2] = f"={psc1905_mro_cell('BAE')}"
            s8_rows.append(("Nuclear & Complex Overhauls", cells))
            continue
        name, codes = item
        s8_rows.append((name, [f"={_seg_total(codes, ('Corporate Parent', crit))}"
                               for _d, crit in _PRIMES_TAM]))
    _paste_block(c, "§8 - Prime Landscape - TAM  [prime_landscape_tam]",
                 ["Category / Series"] + [d for d, _ in _PRIMES_TAM], s8_rows, "M")

    # §9 Prime Landscape - Depot (RMC x prime)
    _paste_block(c, "§9 - Prime Landscape - Depot  [prime_landscape_depot]",
                 ["Category / Series"] + [d for d, _ in _PRIMES_DEPOT],
                 [(rlabel, [f"={_jdepot(crit, rmcs)}" for _d, crit in _PRIMES_DEPOT])
                  for rlabel, rmcs in _RMC_BUCKETS],
                 "M")

    # §10 HII MT Financials (FY2025 segment financials, wired to the model anchors)
    _paste_block(c, "§10 - HII MT Financials  [hii_financials]",
                 ["Metric", "FY2025"],
                 [("Revenue ($M)", [f"={hii_mt_rev_cell()}"]),
                  ("Operating Income ($M)", [f"={hii_mt_oi_cell()}"]),
                  ("Operating Margin (%)", [f"=IFERROR({hii_mt_oi_cell()}/{hii_mt_rev_cell()},0)"])],
                 ["M", "M", "P"])

    # §11 Scope Reconciliation (10-bar waterfall paste block)
    omn_auth = f"({omn_cell('1B2B_TOTAL')}+{omn_cell('1B4B_TOTAL')}+{omn_cell('1B5B_TOTAL')})"
    omn_ce = f"({omn_cell('1B2B_CONTRACT')}+{omn_cell('1B4B_CONTRACT')}+{omn_cell('1B5B_CONTRACT')})"
    other7 = (f"({mro_tas_cell('SCN')}+{mro_tas_cell('NAVY_OTHER')}+{mro_tas_cell('AIR_FORCE')}"
              f"+{mro_tas_cell('ARMY')}+{mro_tas_cell('DW_OTHER')}+{mro_tas_cell('OTHER_AGENCY')})"
              f"*({navy_tam_svc_cell()}+{cg_tam_svc_cell()})/{mro_tas_cell('TOTAL')}")
    _paste_block(c, "§11 - Scope Reconciliation  [scope_reconciliation]",
                 ["Category / Series", "OMN Ship-Maint Auth", "-Non-contract alloc",
                  "CE 928 contracted slice", "+OPN", "+USCG", "+RDT&E-DW",
                  "+Other (SCN / Navy other / AF / Army / DW / Agency)", "Services MRO TAM",
                  "+PSC 1905 Embedded", "Reconciled MRO TAM"],
                 [("FY2025 $M", [f"={omn_auth}/1000", f"=-({omn_auth}-{omn_ce})/1000",
                                 f"={omn_ce}/1000", f"={_rebased('OPN')}", f"={_rebased('USCG')}",
                                 f"={_rebased('RDTE_DW')}", f"={other7}",
                                 f"={navy_tam_svc_cell()}+{cg_tam_svc_cell()}",
                                 f"={psc1905_mro_cell('EMBEDDED')}", f"={recon}"]),
                  ("Bar type", ["s", "d", "e", "s", "s", "s", "s", "e", "s", "e"])],
                 "M")

    # §12 Top-Down Composition (100% stacked: components in $M, think-cell stacks)
    _paste_block(c, "§12 - Top-Down Composition  [tam_top_down_detail]",
                 ["Top-Down Component", "FY2025 $M"],
                 [("Public NSY", [f"={op5_public_nsy_cell()}/1000"]),
                  ("1B4B Private avails", [f"={op5_private_cell()}/1000"]),
                  ("OPN LI 1000", [f"={opn_li1000_cell(2025)}/1000"]),
                  ("SCN LI 2086 RCOH", [f"={scn_cvn_rcoh_li2086_cell(2025)}/1000"]),
                  ("MSC M&R", [f"={msc_mr_fy25_transfer_cell()}/1000"]),
                  ("USCG ISVS", [f"={uscg_isvs_floor_cell()}/1000"])],
                 "M")

    # §13 TAM Top-Down Funnel (waterfall)
    td_sum = (f"{op5_public_nsy_cell()}/1000+{op5_private_cell()}/1000+{opn_li1000_cell(2025)}/1000"
              f"+{scn_cvn_rcoh_li2086_cell(2025)}/1000+{msc_mr_fy25_transfer_cell()}/1000"
              f"+{uscg_isvs_floor_cell()}/1000")
    priv = (f"{op5_private_cell()}/1000+{msc_mr_fy25_transfer_cell()}/1000"
            f"+{scn_cvn_rcoh_li2086_cell(2025)}/1000+{opn_li1000_cell(2025)}/1000"
            f"+{uscg_isvs_floor_cell()}/1000")
    _paste_block(c, "§13 - Top-Down Funnel  [tam_top_down_funnel]",
                 ["Category / Series", "Total Budget-Anchored MRO", "Public NSY",
                  "Non-public-NSY MRO funding"],
                 [("FY2025 $M", [f"={td_sum}", f"=-{op5_public_nsy_cell()}/1000", f"=-({priv})"]),
                  ("Bar type", ["s", "d", "e"])],
                 "M")

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


OUTPUT = _make()
