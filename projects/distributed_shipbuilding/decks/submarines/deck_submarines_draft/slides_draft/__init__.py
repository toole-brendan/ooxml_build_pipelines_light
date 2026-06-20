from . import market_primer
from . import sizing_boundary
from . import executive_summary
from . import demand_backdrop
from . import methodology
from . import basic_construction
from . import tam_bridge
from . import annual_cadence
from . import coefficient_evidence
from . import ap_and_lltm
from . import work_type_taxonomy
from . import bucket_tam
from . import sam_scenarios
from . import visible_suppliers
from . import sib_exclusion
from . import data_limits
from . import implications
from . import appendix_definitions_and_scope
from . import appendix_ap_and_lltm_detail
from . import appendix_coefficient_sensitivity
from . import appendix_sam_bucket_crosswalk
from . import appendix_top_25_visible_suppliers

SLIDE_RENDERS = [
    (market_primer, market_primer.render),
    (sizing_boundary, sizing_boundary.render),
    (executive_summary, executive_summary.render),
    (demand_backdrop, demand_backdrop.render),
    (methodology, methodology.render),
    (basic_construction, basic_construction.render),
    (tam_bridge, tam_bridge.render),
    (annual_cadence, annual_cadence.render),
    (coefficient_evidence, coefficient_evidence.render),
    (ap_and_lltm, ap_and_lltm.render),
    (work_type_taxonomy, work_type_taxonomy.render),
    (bucket_tam, bucket_tam.render),
    (sam_scenarios, sam_scenarios.render),
    (visible_suppliers, visible_suppliers.render),
    (sib_exclusion, sib_exclusion.render),
    (data_limits, data_limits.render),
    (implications, implications.render),
    (appendix_definitions_and_scope, appendix_definitions_and_scope.render),
    (appendix_ap_and_lltm_detail, appendix_ap_and_lltm_detail.render),
    (appendix_coefficient_sensitivity, appendix_coefficient_sensitivity.render),
    (appendix_sam_bucket_crosswalk, appendix_sam_bucket_crosswalk.render),
    (appendix_top_25_visible_suppliers, appendix_top_25_visible_suppliers.render),
]
