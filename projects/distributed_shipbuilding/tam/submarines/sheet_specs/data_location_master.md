Location Master
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_location_master.py

Purpose
Subaward geography (a hint, not a coefficient input): top states and country split,
with foreign treated as supplier-addressable. Geography is a HINT only - the award-action
scope controls the TAM treatment, not where the $ lands. Subaward $ landing in a
prime-controlled state is distributed-view, not necessarily addressable.

Source
extracted/nc_geo_by_state.csv (state, state_name, amount_M, pct_of_us_total) and
extracted/nc_geo_by_country.csv (country_code, country, amount_M, pct_of_total). Both
sorted $M descending; the state table is capped at the top 15.

Reads
- none (leaf module; loads its own two geography CSVs, depends on no other sheet)
- _PRIME_STATES knob: CT = EB (Groton), RI = EB (Quonset), VA = HII-NNS
  (Newport News), MS = HII-Ingalls - the prime-controlled final-assembly / major-prime
  state map.

Feeds
- none (geography hint; exposes no accessors and registers no defined name)
- Excel table: tbl_sub_location_states

On the sheet
§1  At a glance: subaward geography (hint only)
    - Python-computed rollups (constants, not links): US subaward $M = sum of all state
      amounts; foreign subaward $M = sum of non-US country amounts (addressable); top
      state by $M (name + lifetime $); prime-controlled-state $M = sum of state amounts
      for CT/RI/VA/MS (distributed-view, not auto-addressable).

§2  Top 15 states by subaward $ ($M lifetime)
    - The native table tbl_sub_location_states: State, Name, $M, % of US, Prime-controlled
      site. $M / % are input cells from the CSV; the "Prime-controlled site" column is
      filled from the _PRIME_STATES map where the state matches.

§3  Country distribution (foreign = supplier-addressable)
    - Table: Code, Country, $M, % of total - one row per country from the country CSV;
      non-US rows are the foreign (addressable) geography.

§4  Prime-controlled state flags
    - State -> Site list straight from the _PRIME_STATES knob (CT/RI = Electric Boat,
      VA = HII-Newport News, MS = HII-Ingalls); flags the states where a final-assembly
      yard or major prime site sits.

Notes
- Native cell notes: none.
- Note column: none.
