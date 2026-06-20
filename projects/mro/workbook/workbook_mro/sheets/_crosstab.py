"""_crosstab - shared axis constants + structured-ref SUMIFS builders for the native
MRO model sheets.

The Services / Depot Ship Repair / Output sheets build their cross-tabs as Python loops
that emit `SUMIFS(Awards[...],Awards[col],"val",...)` formulas against the native data
tables (``Awards`` / ``J998J999Data`` / ``PSC1905Classified``); structured references are
position-independent, so a loop here reproduces the cross-tab formulas exactly (the
soffice tie-out is the numeric backstop).

The axis constants below are the canonical lists (the 65 services-MRO PSCs, the vessel
types, the Navy / Coast Guard hull programs, the work-segment partition), held as static
literals. Generating §1/§2/§3 with `sumifs_award` over them reproduces all 4,290 cross-tab
formulas - see qa/verify_crosstab.py.
"""
from __future__ import annotations

# §1 row axis: the 65 services-MRO PSCs (code, description), in deck order.
# Identical across Services §1 (vessel type), §2 (Navy hull), §3 (CG hull).
PSC_ROWS = [
    ('J998', 'Non-Nuclear Ship Repair (East)'),
    ('J999', 'Non-Nuclear Ship Repair (West)'),
    ('J010', 'Maint/Repair - Weapons'),
    ('J012', 'Maint/Repair - Fire Control Equipment'),
    ('J013', 'Maint/Repair - Ammunition and Explosives'),
    ('J014', 'Maint/Repair - Guided Missiles'),
    ('J017', 'Maint/Repair - Aircraft Launching/Landing'),
    ('J019', 'Maint/Repair - Ships, Small Craft, Pontoons'),
    ('J020', 'Maint/Repair - Ship and Marine Equipment'),
    ('J029', 'Maint/Repair - Engine Accessories'),
    ('J030', 'Maint/Repair - Mechanical Power Transmission'),
    ('J035', 'Maint/Repair - Service and Trade Equipment'),
    ('J036', 'Maint/Repair - Special Industry Machinery'),
    ('J039', 'Maint/Repair - Materials Handling Equipment'),
    ('J041', 'Maint/Repair - Refrigeration/AC'),
    ('J043', 'Maint/Repair - Pumps and Compressors'),
    ('J047', 'Maint/Repair - Pipe, Tubing, Hose, Fittings'),
    ('J048', 'Maint/Repair - Valves'),
    ('J049', 'Maint/Repair - Maintenance Shop Equipment'),
    ('J052', 'Maint/Repair - Measuring Tools'),
    ('J056', 'Maint/Repair - Construction/Building Materials'),
    ('J058', 'Maint/Repair - Comm/Detection Equipment'),
    ('J059', 'Maint/Repair - Electrical/Electronic Equipment'),
    ('J061', 'Maint/Repair - Electric Wire/Power Distribution'),
    ('J063', 'Maint/Repair - Alarm/Signal/Security'),
    ('J066', 'Maint/Repair - Instruments/Laboratory'),
    ('J091', 'Maint/Repair - Fuels/Lubricants/Oils'),
    ('J099', 'Maint/Repair - Miscellaneous Equipment'),
    ('K010', 'Modification - Weapons'),
    ('K012', 'Modification - Fire Control Equipment'),
    ('K014', 'Modification - Guided Missiles'),
    ('K019', 'Modification - Ships, Small Craft, Pontoons'),
    ('K020', 'Modification - Ship and Marine Equipment'),
    ('K034', 'Modification - Metalworking Machinery'),
    ('K058', 'Modification - Comm/Detection Equipment'),
    ('K059', 'Modification - Electrical/Electronic Equipment'),
    ('K099', 'Modification - Miscellaneous Equipment'),
    ('N010', 'Installation - Weapons'),
    ('N012', 'Installation - Fire Control Equipment'),
    ('N014', 'Installation - Guided Missiles'),
    ('N019', 'Installation - Ships, Small Craft, Pontoons'),
    ('N020', 'Installation - Ship and Marine Equipment'),
    ('N025', 'Installation - Vehicular Equipment'),
    ('N056', 'Installation - Construction/Building Materials'),
    ('H119', 'QC - Ships, Small Craft, Pontoons'),
    ('H120', 'QC - Ship and Marine Equipment'),
    ('H219', 'Equip Testing - Ships, Small Craft, Pontoons'),
    ('H220', 'Equip Testing - Ship and Marine Equipment'),
    ('H319', 'Inspection - Ships, Small Craft, Pontoons'),
    ('H320', 'Inspection - Ship and Marine Equipment'),
    ('H919', 'Other QC/Inspect - Ships, Small Craft, Pontoons'),
    ('H920', 'Other QC/Inspect - Ship and Marine Equipment'),
    ('L019', 'Tech Rep - Ships, Small Craft, Pontoons'),
    ('L020', 'Tech Rep - Ship and Marine Equipment'),
    ('M1ED', 'Operation - Ship Construction/Repair Facilities'),
    ('M2AA', 'Husbanding - Communications Services'),
    ('M2AB', 'Husbanding - Force Protection'),
    ('M2AC', 'Husbanding - Removal Services'),
    ('M2AD', 'Husbanding - Material Handling'),
    ('M2AE', 'Husbanding - Purchasing Services'),
    ('M2AF', 'Husbanding - Incidental Services'),
    ('M2BA', 'Husbanding - Transportation Services'),
    ('M2BB', 'Husbanding - Fuel Services'),
    ('M2BZ', 'Husbanding - Other Port Services'),
    ('M2CA', 'Husbanding - Management/Integration Service'),
]

PSC_CODES = [code for code, _desc in PSC_ROWS]

# Work-segment partition of the 65 PSCs (Services §5/§9/§12/§13/§14, Output).
# Verified disjoint and exhaustive (union == the 65 PSC_CODES).
WORK_SEGMENTS = [
    ("Depot Ship Repair", ['J998', 'J999']),
    ("Combat Systems Sustainment",
     ['J010', 'J012', 'J013', 'J014', 'J017', 'K010', 'K012', 'K014', 'N010', 'N012', 'N014']),
    ("Hull, Mechanical & Electrical (HM&E)",
     ['J019', 'J020', 'J029', 'J030', 'J035', 'J036', 'J039', 'J041', 'J043', 'J047', 'J048',
      'J049', 'J052', 'J056', 'J091', 'J099', 'K019', 'K020', 'K034', 'K099', 'N019', 'N020',
      'N025', 'N056']),
    ("Electronics & C4ISR Sustainment",
     ['J058', 'J059', 'J061', 'J063', 'J066', 'K058', 'K059']),
    ("Port & Technical Services",
     ['H119', 'H120', 'H219', 'H220', 'H319', 'H320', 'H919', 'H920', 'L019', 'L020', 'M1ED',
      'M2AA', 'M2AB', 'M2AC', 'M2AD', 'M2AE', 'M2AF', 'M2BA', 'M2BB', 'M2BZ', 'M2CA']),
]

# §1 column axis: 17 vessel types (last is the "" Unclassified bucket).
VESSEL_TYPES = [
    'Surface Combatants', 'Amphibious Warfare Ships', 'Submarines', 'Combat Logistics Ships',
    'Aircraft Carriers', 'Multi-class', 'Cutters', 'Expeditionary & Seabasing Ships',
    'Support Crafts', 'Auxiliary Ships', 'Salvage Ships & Fleet Ocean Tugs',
    'Combatant Crafts', 'Mine Warfare', 'Boats', 'Unmanned Maritime Platforms',
    'Surveillance Ships', 'Unclassified',
]

# §2 column axis: 29 Navy hull programs (last is Unclassified).
HULL_PROGRAMS_NAVY = [
    'DDG', 'LPD', 'T-AO', 'SSBN', 'CVN', 'LCS', 'LSD', 'LHD', 'LHA', 'T-AKE', 'ESB', 'T-EPF',
    'AS', 'T-AH', 'CG', 'MCM', 'T-AOE', 'T-ARS', 'SSN', 'LCAC', 'LCC', 'T-ARC', 'WPC', 'T-ESB',
    'T-ATF', 'T-AKR', 'WMSL', 'T-AGS', 'Unclassified',
]

# §3 column axis: 16 Coast Guard hull programs (last is Unclassified).
HULL_PROGRAMS_CG = [
    'WPC', 'WMSL', 'WAGB', 'WMEC', 'WLB', 'WLM', 'WLBB', 'CG', 'WLR', 'WLIC', 'WTGB', 'WYTL',
    'MCM', 'WLI', 'SSBN', 'Unclassified',
]

# The axis cells whose criterion is the empty string "" (the catch-all bucket).
_EMPTY_CRIT = "Unclassified"


def axis_crit(label: str) -> str:
    """The SUMIFS criterion value for an axis label ("Unclassified" -> "")."""
    return "" if label == _EMPTY_CRIT else label


def _sumifs(table: str, value_col: str, crit) -> str:
    """SUMIFS(<table>[<value_col>], <table>[col],"val", ...) - exact v4.33 string form."""
    pairs = "".join(f',{table}[{col}],"{val}"' for col, val in crit)
    return f"SUMIFS({table}[{value_col}]{pairs})"


def sumifs_award(value_col: str, *crit) -> str:
    """SUMIFS over the ``Awards`` table. crit = (column_header, value) pairs."""
    return _sumifs("Awards", value_col, crit)


def sumifs_j(value_col: str, *crit) -> str:
    """SUMIFS over the ``J998J999Data`` table. crit = (column_header, value) pairs."""
    return _sumifs("J998J999Data", value_col, crit)


def countifs_j(*crit) -> str:
    """COUNTIFS over the ``J998J999Data`` table. crit = (column_header, value) pairs."""
    pairs = ",".join(f'J998J999Data[{col}],"{val}"' for col, val in crit)
    return f"COUNTIFS({pairs})"


def sumifs_psc1905(value_col: str, *crit) -> str:
    """SUMIFS over the ``PSC1905Classified`` table. crit = (column_header, value) pairs."""
    return _sumifs("PSC1905Classified", value_col, crit)
