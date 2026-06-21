# Slides archived — 2026-05-25

Cleared `deck/slides/` for a rebuild. Preserved the prior cut as a
reference snapshot.

## What moved

Created `deck/archive/` and moved every `.py` file out of
`deck/slides/` into it (16 files):

```
__init__.py
s00_cover.py
s01_answer_in_one_page.py
s02_cost_funnel.py
s03_production_baseline.py
s04_divider_sizing.py
s05_dod_pop_corpus.py
s06_visibility_gap.py
s07_top_vendors.py
s08_divider_layers.py
s09_aegis_spy6.py
s10_other_gfe.py
s11_divider_direction.py
s12_hii_outsourcing.py
s13_navy_50pct.py
s14_method_sources.py
```

`deck/slides/` is now empty.

## Build state

`deck/build.py:67-83` still imports `s00_cover` ... `s14_method_sources`
from `slides`, so `python3 build.py` now fails with
`ModuleNotFoundError` until either:

  (a) new slide modules + a fresh `slides/__init__.py` are added, or
  (b) the `from slides import (...)` block and the `SLIDES = [...]`
      list in `build.py` are pruned.

No other deck files touched. `_extracted/`, `_schema/`, `_docs/`,
`assets_deck/`, `out/`, and the top-level modules (`build.py`,
`builder.py`, `primitives.py`, `style.py`, `validate.py`,
`layout_check.py`, `ooxml_lookup.py`, `README.md`) are unchanged.
