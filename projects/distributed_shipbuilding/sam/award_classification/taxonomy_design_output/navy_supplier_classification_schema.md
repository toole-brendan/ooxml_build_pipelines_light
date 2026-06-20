# Navy shipbuilding supplier work-type schema

## Classification object

Assign one **dominant shipbuilding-relevant operating capability** to each supplier UEI. The label describes what the supplier does or makes; it does not assert that every subaward transaction bought that item. After classification, join the UEI label to `all_subawards.csv` on `entity_uei` so all of the supplier's dollars inherit one category.

## Categories

| ID | Work type | Definition |
|---:|---|---|
| 01 | Electrical power equipment, conversion & distribution | Manufactures equipment that generates, converts, stores, switches, protects, or distributes electrical power aboard the ship or in supporting systems. |
| 02 | Propulsion, engines & mechanical power transmission | Builds or services prime movers and mechanical-drive components: engines, turbines, reduction gears, bearings, shafts, couplings, brakes, and propulsion-unit parts. |
| 03 | Fluid systems, flow control & piping | Produces fluid-handling equipment and metallic piping components: pumps, compressors, valves, actuators, fabricated pipe, and fittings. |
| 04 | Thermal management, HVAC & air handling | Makes heat-transfer, steam/boiler, refrigeration, heating, ventilation, air-purification, and environmental-control equipment. |
| 05 | Structural fabrication, tanks & ship modules | Performs heavy plate, structural, sheet-metal, enclosure, tank, container, and module fabrication, including welded ship structures. |
| 06 | Primary metals, forgings & castings | Melts, refines, rolls, draws, extrudes, forges, or casts ferrous and nonferrous metals and supplies mill forms or near-net-shape metal products. |
| 07 | Precision machining, hardware & metal finishing | Performs machining, turning, forming, heat treatment, plating/coating, or manufactures small precision metal parts, fasteners, springs, and hardware. |
| 08 | Polymers, elastomers, composites & formulated materials | Produces chemicals and nonmetallic engineered materials or parts using compounding, molding, laminating, coating, rubber, plastics, glass/mineral, sealing, and composite processes. |
| 09 | Electronic components, computers, interconnects & cable | Makes electronic parts and assemblies, computing hardware, printed circuits, semiconductors, passive components, connectors, wiring devices, and fiber/electrical cable. |
| 10 | Sensors, instrumentation, controls & communications | Builds system-level sensing, navigation, measurement, test, process-control, radar/sonar, communications, and audio/video equipment. |
| 11 | Industrial machinery, tooling & material handling | Manufactures production equipment, machine tools, jigs/fixtures, welding equipment, cranes/hoists/conveyors, industrial vehicles, and other plant machinery. |
| 12 | Ordnance, launchers & specialized mission hardware | Produces ammunition, explosives, weapons, launch/handling equipment, and other mission hardware whose defining capability is weapons-system manufacture. |
| 13 | Shipyard work, marine integration & outfitting | Performs whole-ship or major marine-system integration, shipyard construction/repair, large-scale outfitting, or marine-module integration rather than a discrete component process. |
| 14 | Engineering, software, R&D & testing | Provides technical design, engineering, software/data, systems integration, scientific R&D, laboratory testing, surveying, or specialized technical consulting as its operating capability. |
| 15 | Installation, construction, maintenance & repair | Installs, constructs, repairs, maintains, remediates, or services equipment/facilities rather than manufacturing the equipment. |
| 16 | Distribution, logistics, rental & commercial supply | Supplies products through wholesale/retail channels or provides transportation, warehousing, freight, rental/leasing, packaging, or commercial supply-chain services. |
| 17 | Business, staffing, training & other support | Provides nontechnical management/administrative, staffing, security, training, utility, financial, healthcare, association, or other support services. |
| 18 | Interiors, safety gear & miscellaneous manufactured products | Manufactures shipboard interiors, furniture/millwork, wood/paper/packaging products, apparel/safety goods, signs, and miscellaneous finished products not captured above. |
| 99 | Unresolved capability / insufficient evidence | Temporary analytical residual for entities lacking enough reliable evidence to assign a work capability without invention. Still gives every UEI exactly one label. |

## Assignment precedence

1. Curated, documented UEI override.
2. Clear business-model primary NAICS (distribution/logistics, contractor/repair, support service).
3. Specific process/product primary NAICS.
4. For missing, generic, or end-market primary codes, use coherent specific secondary NAICS evidence.
5. Resolve conflicts with PSC, entity name, Manufacturer of Goods / organization attributes, owner context, and authoritative external evidence.
6. Use category 99 when evidence remains insufficient.

## Confidence

- **A:** specific primary NAICS.
- **B:** corroborated secondary/process override.
- **C:** curated entity evidence.
- **U:** unresolved.

## Files

- `navy_supplier_work_type_schema.xlsx`: complete workbook, crosswalks, PSC tiebreakers, and review queue.
- `navy_primary_naics_crosswalk.csv`: every primary code observed in the dataset.
- `navy_all_observed_naics_crosswalk.csv`: all 506 codes appearing in suppliers' full NAICS lists.
- `navy_work_type_schema.csv`: category definitions and mapping signals.
