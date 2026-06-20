Methodology
Tab color: 2C6E6E (teal)  ·  group: Guide & scope
Module: guide_methodology.py

Purpose
Concise method + scope reference (prose + crosswalk tables, no formulas) that
sits behind the answer sheet. Description-led classification is the DDG signal.
The bucket vocabulary + classify() live in the _taxonomy leaf; this module imports
them only to display the taxonomy tables.

Reads
- none (prose + crosswalk reference; no cross-sheet links, no accessors, no formulas)

Feeds
- none

On the sheet
§1  Overview (TAM / SAM definitions)
    §1a Scope & governing rule: outsourced new-construction supplier market for DDG-51
        Flight III (SCN LI 2122), yards BIW + Ingalls; TAM = non-GFE/non-MIB new-
        construction $ away from prime/co-prime/GFE sites; SAM = TAM in targetable
        buckets, shown as a scenario menu (not a probability haircut).
    §1b TAM - two cost streams: BC stream (P-5c base x MYP-corrected BC coeff) and
        AP/LLTM stream (P-10 advance procurement x AP coeff), with stream definitions.
    §1c SAM - scenario menu (not a formula): allocate TAM to 7 buckets, SAM_k =
        SUMPRODUCT(bucket_$, scenario_flags); no SOM haircut; description-led for DDG.
    §1d The MYP correction guardrail: the two $-redacted MYP masters (BIW 2305 ~$6.40B,
        Ingalls 2307 ~$8.18B) make the disclosed-only corpus read ~87% outside-yards
        (a redaction artifact); folding the masters back corrects to ~33%. Never present
        the 87%; always travel the numbers together.
    §1e Exclusions (action-level scope_class): GFE/weapons/sensors/Navy-directed, MIB,
        sustainment, depot, design-only; DDG contaminants (IVECO Mk110, DDG-1000 LI 2119,
        Thales ESSM); entity/location are hints, the award-action scope controls.
    §1f Audit-trail color key: blue = input, black = derived, green = cross-sheet link;
        Arial 8pt, no fills/merges/gridlines, number/percent/dash formats.
    §1g Data caveats: single-vintage SCN (FY27 PB), FFATA ~15% coverage floor, FPDS
        de-cap requirement, POP as a where-performed proxy.

§2  Market (TAM = BC base x BC coeff + AP/LLTM base x AP coeff; stream bases)
    §2a Governing rule: TAM = available outside-supplier $; SAM = targetable subset
        (scenario menu, no win-probability haircut); headlines use POP-based supplier TAM.
    §2b Base -> TAM -> SAM crosswalk table: Base (P-5c BC + P-10 AP/LLTM net exclusions)
        -> x coeff (supplier+foreign POP share) -> = TAM (TAM Build) -> allocate (SAM
        Build bucket allocation) -> = SAM (SUMPRODUCT(bucket$, flags)).
    §2c Two-stream TAM table: BC coefficient (other-US+foreign away from both yards,
        MYP-corrected) vs AP/LLTM coefficient (long-lead / advance procurement / EOQ).
    §2d SAM = scenario menu (not a formula): SAM_scenario[k] = SUMPRODUCT(bucket_$,
        scenario_flag[k]) with flag in {0,1}; no capability_fit / addressability / SOM.
    §2e In / out of TAM table: in (BC, AP/LLTM/EOQ, component work, off-yard work) vs
        out (GFE/Aegis/SPY-6/VLS, MIB, sustainment/depot/design-only, on-site work,
        DDG-1000 / IVECO Mk110 / Thales ESSM).

§3  Exclusions (MYP redaction, GFE / MIB, Navy-directed flows)
    §3a Governing principle: an award is excluded when its action scope is GFE/weapons/
        Navy-directed, MIB, sustainment, depot, or design-only - even on a covered hull.
    §3b scope_class vocabulary table (POP Corpus): INCLUDE_BC / INCLUDE_AP_LLTM /
        INCLUDE_EOQ (in TAM) vs EXCLUDE_GFE / _MIB_IB / _SUSTAINMENT / _DEPOT /
        _DESIGN_ONLY / _REVIEW (out), with stream + meaning + DDG use.
    §3c DDG exclusion categories + named contaminants table: GFE combat systems,
        WPN/OPN weapons, DDG-1000 (LI 2119), IVECO Mk110 (~$707M), Thales ESSM (~$4.2B);
        each applied ONCE (gated out of POP AND decremented in the bridge; validation tabs tie).

§4  Taxonomy (work-type buckets + unbucketed / ambiguous)
    §4a Work-type buckets table: the 7 buckets (structural, machining, castings, piping,
        electrical, hvac, coatings) + the explicit unbucketed/ambiguous residual, each
        with key/name/definition (rendered from the _taxonomy BUCKETS list).
    §4b Description-keyword -> bucket table (DDG PRIMARY arbiter): the substring keyword
        list per bucket (from DESC_BUCKET).
    §4c NAICS-4digit -> bucket table (fallback when description is thin): the NAICS4_BUCKET
        crosswalk, sorted by code.

§5  Rules (classification precedence ladder, first match wins)
    §5a Arbiter principle: subawards seed observed shares but the visible mix is never
        assumed equal to hidden TAM mix (modeled share adjusted transparently); DDG is
        description-led.
    §5b Precedence ladder table (first match wins): 1 prime/co-prime name -> 2 GFE name ->
        3 description keyword (DDG primary) -> 4 vendor-name override -> 5 NAICS-4 fallback ->
        6 service/non-component NAICS -> 7 residual (unbucketed), with result + example each.
    §5c Override artifacts table: where description/NAICS mislead (3364 "aircraft parts",
        5511 holding companies, thin descriptions, Rolls-Royce/propulsion) and the fix.

Notes
- Native cell notes: none.
- Note column: none.
