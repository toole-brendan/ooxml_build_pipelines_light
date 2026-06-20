# Image credits & provenance — consolidated deck

Images live in `deck/images/` and are embedded by `build_pptx` (declared
per-slide via each module's `IMAGES` list + `picture()` calls). Keep this file
**outside** `images/` — the builder copies every top-level file in that
directory into `ppt/media/`, so only real assets belong there. (It does NOT
recurse into subdirs, so `images/_unused/` is excluded from the bundle.)

**Current state:** only **slide 06** uses an image (the submarine photo below).
The brand logos below were wired into slides 04 + 15 and then reverted at the
user's request; the PNGs are parked in `images/_unused/` and remain available to
re-wire.

## Brand logos (parked in `images/_unused/`)
Rasterized to PNG (transparent background) with `rsvg-convert` from SVG sources.
Corporate logos are used **nominatively** to identify named suppliers/primes in
an internal market-sizing/diligence deck; most are trademark and/or
`{{PD-textlogo}}` on Wikimedia Commons. Confirm trademark usage is acceptable
before any external distribution.

| File | Entity | Source SVG |
|------|--------|-----------|
| `general_dynamics.png` | General Dynamics (Bath Iron Works, Electric Boat) | submarines pool / Wikimedia Commons |
| `huntington_ingalls_industries.png` | Huntington Ingalls (Ingalls, Newport News) | submarines pool / Wikimedia Commons |
| `leonardo.png` | Leonardo (DRS) | submarines pool / Wikimedia Commons |
| `northrop_grumman.png` | Northrop Grumman | submarines pool / Wikimedia Commons |
| `rolls_royce_holdings.png` | Rolls-Royce | submarines pool / Wikimedia Commons |
| `curtiss_wright.png` | Curtiss-Wright (Electro-Mechanical) | submarines pool / Wikimedia Commons |
| `austal.png` | Austal | submarines pool / Wikimedia Commons |
| `ge.png` | GE | Wikimedia Commons, `File:General Electric logo.svg` |

"submarines pool" = `projects/submarines/research/image_assets/brand_logos/`.

**Not used:** Johnson Controls — only an *old* logo is on Wikimedia Commons
(current mark is non-free); left as a text chip on slide 15 rather than ship
stale branding. Arctic Slope, Major Tool, Scot Forge, DC Fabricators, Rhoads,
Graham have no readily available free logo and stay as text chips.

## Photo (slide 06)
| File | Subject | Source |
|------|---------|--------|
| `virginia_construction.jpg` | Virginia-class submarine under construction (center-cropped to the slide box) | `projects/submarines/research/image_assets/subject_photos/virginia_new_jersey_launch.jpg` |

⚠️ The original photo's source/license is not documented in the submarines
pool. US Navy / shipyard construction imagery is typically public domain, but
**verify the specific source/license before external use.** The slide caption
and Sources line mark it as illustrative.
