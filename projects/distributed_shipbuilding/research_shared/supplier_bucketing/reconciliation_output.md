# Supplier Work-Type Bucketing - Reconciliation (Tasks E & F)

Control totals (signed): DDG $11,202M, Subs $6,139M

### View 1 - Status quo (current workbook classification logic)
_DDG = description-led record level (incl. 3364->electrical artifact); Subs = NAICS-led (3364->electrical) applied to the signed-record universe. The live Subs workbook computes its shares over the 150-vendor lifetime lookup; here the same logic is applied to signed records for like-for-like comparison._

| Category | DDG $M | DDG % | Subs $M | Subs % |
|---|--:|--:|--:|--:|
| Total visible subaward flow | 11,202 | 100.0% | 6,139 | 100.0% |
| Physical HM&E base (bucketed supplier) | 6,038 | 53.9% | 4,802 | 78.2% |
| Excluded: mission_systems | 0 | 0.0% | 0 | 0.0% |
| Excluded: service / holding / IT | 408 | 3.6% | 163 | 2.7% |
| Excluded: foreign / FMS | 0 | 0.0% | 0 | 0.0% |
| Dropped: prime / GFE | 460 | 4.1% | 75 | 1.2% |
| Residual (unbucketed supplier - a FLOOR) | 4,295 | 38.3% | 1,099 | 17.9% |

| Bucket | DDG $M | DDG share | Subs $M | Subs share |
|---|--:|--:|--:|--:|
| structural | 1,848 | 17.9% | 1,036 | 17.6% |
| machining | 1,188 | 11.5% | 169 | 2.9% |
| castings | 64 | 0.6% | 233 | 3.9% |
| piping | 250 | 2.4% | 858 | 14.5% |
| electrical | 2,458 | 23.8% | 2,125 | 36.0% |
| hvac | 178 | 1.7% | 103 | 1.7% |
| coatings | 51 | 0.5% | 277 | 4.7% |

| Scenario (overlapping) | DDG $M | DDG %base | Subs $M | Subs %base |
|---|--:|--:|--:|--:|
| metal | 3,100 | 51.3% | 1,439 | 30.0% |
| hme | 1,617 | 26.8% | 1,130 | 23.5% |
| electrical | 2,458 | 40.7% | 2,125 | 44.3% |
| modular | 1,899 | 31.5% | 1,313 | 27.3% |
| broad | 6,038 | 100.0% | 4,802 | 100.0% |

### View 2 - Revised physical base, VLS launch-control OUT (base case)
| Category | DDG $M | DDG % | Subs $M | Subs % |
|---|--:|--:|--:|--:|
| Total visible subaward flow | 11,202 | 100.0% | 6,139 | 100.0% |
| Physical HM&E base (bucketed supplier) | 4,005 | 35.8% | 4,779 | 77.8% |
| Excluded: mission_systems | 2,665 | 23.8% | 246 | 4.0% |
| Excluded: service / holding / IT | 1,741 | 15.5% | 175 | 2.9% |
| Excluded: foreign / FMS | 359 | 3.2% | 185 | 3.0% |
| Dropped: prime / GFE | 405 | 3.6% | 92 | 1.5% |
| Residual (unbucketed supplier - a FLOOR) | 2,027 | 18.1% | 663 | 10.8% |

| Bucket | DDG $M | DDG share | Subs $M | Subs share |
|---|--:|--:|--:|--:|
| structural | 343 | 5.7% | 920 | 16.9% |
| machining | 2,352 | 39.0% | 180 | 3.3% |
| castings | 107 | 1.8% | 233 | 4.3% |
| piping | 326 | 5.4% | 1,030 | 18.9% |
| electrical | 347 | 5.7% | 2,031 | 37.3% |
| hvac | 375 | 6.2% | 94 | 1.7% |
| coatings | 156 | 2.6% | 292 | 5.4% |

| Scenario (overlapping) | DDG $M | DDG %base | Subs $M | Subs %base |
|---|--:|--:|--:|--:|
| metal | 2,801 | 70.0% | 1,333 | 27.9% |
| hme | 3,400 | 84.9% | 3,334 | 69.8% |
| electrical | 347 | 8.7% | 2,031 | 42.5% |
| broad | 4,005 | 100.0% | 4,779 | 100.0% |
| modular | 70 | 1.8% | 618 | 12.9% |

### View 3 - VLS launch-control sensitivity IN (boundary launcher equipment -> electrical)
| Category | DDG $M | DDG % | Subs $M | Subs % |
|---|--:|--:|--:|--:|
| Total visible subaward flow | 11,202 | 100.0% | 6,139 | 100.0% |
| Physical HM&E base (bucketed supplier) | 5,683 | 50.7% | 4,779 | 77.9% |
| Excluded: mission_systems | 987 | 8.8% | 245 | 4.0% |
| Excluded: service / holding / IT | 1,741 | 15.5% | 175 | 2.9% |
| Excluded: foreign / FMS | 359 | 3.2% | 185 | 3.0% |
| Dropped: prime / GFE | 405 | 3.6% | 92 | 1.5% |
| Residual (unbucketed supplier - a FLOOR) | 2,027 | 18.1% | 663 | 10.8% |

| Bucket | DDG $M | DDG share | Subs $M | Subs share |
|---|--:|--:|--:|--:|
| structural | 343 | 4.4% | 920 | 16.9% |
| machining | 2,352 | 30.5% | 180 | 3.3% |
| castings | 107 | 1.4% | 233 | 4.3% |
| piping | 326 | 4.2% | 1,030 | 18.9% |
| electrical | 2,025 | 26.3% | 2,031 | 37.3% |
| hvac | 375 | 4.9% | 94 | 1.7% |
| coatings | 156 | 2.0% | 292 | 5.4% |

| Scenario (overlapping) | DDG $M | DDG %base | Subs $M | Subs %base |
|---|--:|--:|--:|--:|
| metal | 2,801 | 49.3% | 1,333 | 27.9% |
| hme | 5,078 | 89.4% | 3,335 | 69.8% |
| electrical | 2,025 | 35.6% | 2,031 | 42.5% |
| broad | 5,683 | 100.0% | 4,779 | 100.0% |
| modular | 1,748 | 30.8% | 619 | 12.9% |

### View 4 - All visible yard-side flow (full ledger; mission systems shown separately)

| Category | DDG $M | DDG % of total | Subs $M | Subs % of total |
|---|--:|--:|--:|--:|
| Physical HM&E base | 4,005 | 35.8% | 4,779 | 77.8% |
| Mission systems (combat/electronics) | 2,665 | 23.8% | 246 | 4.0% |
| Service / holding / IT | 1,741 | 15.5% | 175 | 2.9% |
| Foreign / FMS | 359 | 3.2% | 185 | 3.0% |
| Prime / GFE | 405 | 3.6% | 92 | 1.5% |
| Residual (unresolved supplier) | 2,027 | 18.1% | 663 | 10.8% |
| **Total** | **11,202** | 100% | **6,139** | 100% |

### View 5 - Residual before vs after the tail entity-resolution pass

| | DDG $M | DDG % | Subs $M | Subs % |
|---|--:|--:|--:|--:|
| Residual BEFORE tail pass (45-entity registry) | 2,929 | 26.1% | 1,176 | 19.2% |
| Residual AFTER tail pass (136-entity registry) | 2,027 | 18.1% | 663 | 10.8% |
| **Residual resolved by tail pass** | **902** | | **512** | |


# Task F - Final checks

## F1 - Top-25 moved entities by absolute $ impact (status-quo bucket/role -> revised)

| $M | Entity | Status-quo (role/bucket) | Revised (role/bucket) |
|--:|---|---|---|
| 1,006 | LEONARDO SPA | supplier/structural | mission_systems/UNBUCKETED |
| 998 | ARCTIC SLOPE REGIONAL CORPORAT | supplier/unbucketed | holding/UNBUCKETED |
| 672 | LEONARDO SPA | supplier/electrical | mission_systems/UNBUCKETED |
| 333 | GENERAL ELECTRIC COMPANY | supplier/electrical | supplier/machining |
| 169 | CAES SYSTEMS LLC | supplier/electrical | mission_systems/UNBUCKETED |
| 152 | EXTREME ENGINEERING SOLUTIONS, | supplier/unbucketed | service/UNBUCKETED |
| 151 | NORTHROP GRUMMAN CORPORATION | supplier/electrical | mission_systems/UNBUCKETED |
| 146 | SUPERIOR ELECTROMECHANICAL COM | supplier/structural | supplier/machining |
| 138 | IN-DEPTH ENGINEERING CORPORATI | supplier/unbucketed | service/UNBUCKETED |
| 115 | JOHNSON CONTROLS INTERNATIONAL | supplier/unbucketed | supplier/hvac |
| 106 | HANWHA TECHWIN CO., LTD. | supplier/unbucketed | foreign_fms/UNBUCKETED |
| 98 | NORTHROP GRUMMAN CORPORATION | supplier/electrical | mission_systems/UNBUCKETED |
| 93 | MERRILL TECHNOLOGIES GROUP, IN | supplier/structural | supplier/machining |
| 89 | THE GRAHAM CORPORATION | supplier/structural | supplier/piping |
| 88 | GOLDEN STAR TECHNOLOGY INC | supplier/unbucketed | service/UNBUCKETED |
| 84 | ROSYTH ROYAL DOCKYARD LIMITED | supplier/structural | foreign_fms/UNBUCKETED |
| 82 | INDRA SISTEMAS, SOCIEDAD ANONI | service/UNBUCKETED | foreign_fms/UNBUCKETED |
| 79 | COBHAM PLC | supplier/unbucketed | mission_systems/UNBUCKETED |
| 79 | ESCO TECHNOLOGIES INC. | supplier/unbucketed | supplier/piping |
| 72 | SENER GRUPO DE INGENIERIA SOCI | supplier/unbucketed | foreign_fms/UNBUCKETED |
| 72 | L3 TECHNOLOGIES, INC. | supplier/unbucketed | mission_systems/UNBUCKETED |
| 69 | TELEDYNE INSTRUMENTS INC | supplier/electrical | mission_systems/UNBUCKETED |
| 68 | ULTRA ELECTRONICS HOLDINGS PLC | supplier/electrical | mission_systems/UNBUCKETED |
| 63 | UNITED TECHNOLOGIES CORPORATIO | supplier/unbucketed | residual/UNBUCKETED |
| 63 | SEYER INDUSTRIES, INC. | supplier/structural | supplier/machining |

## F2 - Bucket-share bridge (old -> new), share of supplier-addressable

**DDG**

| Bucket | Old $M | Old share | New $M | New share |
|---|--:|--:|--:|--:|
| structural | 1,848 | 17.9% | 343 | 5.7% |
| machining | 1,188 | 11.5% | 2,352 | 39.0% |
| castings | 64 | 0.6% | 107 | 1.8% |
| piping | 250 | 2.4% | 326 | 5.4% |
| electrical | 2,458 | 23.8% | 347 | 5.7% |
| hvac | 178 | 1.7% | 375 | 6.2% |
| coatings | 51 | 0.5% | 156 | 2.6% |

**Subs**

| Bucket | Old $M | Old share | New $M | New share |
|---|--:|--:|--:|--:|
| structural | 1,036 | 17.6% | 920 | 16.9% |
| machining | 169 | 2.9% | 180 | 3.3% |
| castings | 233 | 3.9% | 233 | 4.3% |
| piping | 858 | 14.5% | 1,030 | 18.9% |
| electrical | 2,125 | 36.0% | 2,031 | 37.3% |
| hvac | 103 | 1.7% | 94 | 1.7% |
| coatings | 277 | 4.7% | 292 | 5.4% |

## F3 - Residual composition after tail pass (top unresolved supplier entities)

Total residual = $2,690M across 1688 entities. Top 15:

| $M | Entity (UEI) |
|--:|---|
| 63 | UNITED TECHNOLOGIES CORPORATION (CBMZJ3Z5SC89) |
| 53 | GMT CORPORATION (YKYBK6MSAKX5) |
| 31 | HANSOME ENERGY SYSTEMS, INC. (UHXFGP3DCRK7) |
| 26 | PON HOLDINGS B.V. (SSD8KRDXKG46) |
| 23 | MERRILL AVIATION, INC. (DLLCKA14LMZ5) |
| 21 | ESI ACQUISITION CORP. (LR2HQKYJLDZ7) |
| 20 | CATERPILLAR INC. (C9C6HPQLL4A8) |
| 19 | L3HARRIS TECHNOLOGIES, INC. (PTMFLMD2CUB4) |
| 19 | HONEYWELL INTERNATIONAL INC (LXR8CJQ8J9J7) |
| 18 | TRIDENT MARITIME SYSTEMS UK LIMITED (E9DKKLZNCQS9) |
| 18 | RIVERSIDE MACHINE AND ENGINEERING, INC (H8EMU1KBTBE7) |
| 17 | DYNALEC CORPORATION (SKKACASET588) |
| 17 | SANMINA-SCI CORPORATION (M5HBU5ZXNN81) |
| 17 | GENERAL TOOL COMPANY (FWF8QBPCGLG3) |
| 17 | VIDEO DISPLAY CORP (D99JMB845P75) |

## F4 - VLS launch-control sensitivity (out vs in)

| | DDG physical $M | Subs physical $M |
|---|--:|--:|
| Base case (VLS OUT) | 4,005 | 4,779 |
| Sensitivity (VLS IN) | 5,683 | 4,779 |
| Delta (VLS launch-control) | 1,678 | 1 |

## F5 - Headline TAM vs allocation shares (from Task A)

The headline modeled TAM is **invariant** to reclassification. TAM = exogenous budget base (`data_scn_budget`) x a supplier coefficient computed from the **POP corpus** (`data_pop_corpus`); neither input reads the subaward role/bucket classification. Reclassification moves only the **within-TAM allocation** (bucket shares -> `model_sam_build` bucket TAM -> scenario SAM). See `model_tam_build.py` (DDG :312 / subs :254) and `model_sam_build.py` (DDG :144,180 / subs :117,141).
