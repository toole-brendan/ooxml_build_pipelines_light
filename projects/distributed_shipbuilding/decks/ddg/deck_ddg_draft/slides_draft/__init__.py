"""Generated DDG slide modules."""
from . import market_primer
from . import executive_summary
from . import scope
from . import cost_funnel
from . import myp_redaction
from . import tam_methodology
from . import annual_tam_build
from . import tam_timing
from . import sam_taxonomy
from . import work_type_allocation
from . import sam_scenarios
from . import supplier_landscape
from . import ffata_visibility_gap
from . import market_direction
from . import implications
from . import appendix_definitions_scope
from . import appendix_tam_calculation
from . import appendix_myp_correction
from . import appendix_ap_lltm_sensitivity
from . import appendix_ffata_limitations
from . import appendix_bucket_rules_supplier_evidence

SLIDE_RENDERS = [
    (market_primer, market_primer.render),
    (executive_summary, executive_summary.render),
    (scope, scope.render),
    (cost_funnel, cost_funnel.render),
    (myp_redaction, myp_redaction.render),
    (tam_methodology, tam_methodology.render),
    (annual_tam_build, annual_tam_build.render),
    (tam_timing, tam_timing.render),
    (sam_taxonomy, sam_taxonomy.render),
    (work_type_allocation, work_type_allocation.render),
    (sam_scenarios, sam_scenarios.render),
    (supplier_landscape, supplier_landscape.render),
    (ffata_visibility_gap, ffata_visibility_gap.render),
    (market_direction, market_direction.render),
    (implications, implications.render),
    (appendix_definitions_scope, appendix_definitions_scope.render),
    (appendix_tam_calculation, appendix_tam_calculation.render),
    (appendix_myp_correction, appendix_myp_correction.render),
    (appendix_ap_lltm_sensitivity, appendix_ap_lltm_sensitivity.render),
    (appendix_ffata_limitations, appendix_ffata_limitations.render),
    (appendix_bucket_rules_supplier_evidence, appendix_bucket_rules_supplier_evidence.render),
]
