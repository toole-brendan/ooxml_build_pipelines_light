# 2026-06-07 — Sea Range Telemetry deck: PowerPoint "Repair" on open — root cause + investigation

## Symptom

Opening `projects/sea_range_telemetry/20260607_Sea Range Telemetry_vS.pptx` in **PowerPoint** triggers the
"PowerPoint found a problem with content … Repair" dialog. The same file opens **without complaint in
LibreOffice and loads cleanly in `python-pptx`**, which is what made this slow to pin down: the most common
validators all tolerate the defect.

The deck is the four new appendix methodology slide modules
(`s01_appendix_scope_evidence_boundary`, `s02_appendix_evidence_base`, `s03_appendix_tam_build`,
`s04_appendix_sam_build`) built this session and registered in
`deck_sea_range_telemetry/slides/__init__.py`. Build is green (`python build_deck.py` → 4 slides / 0 charts).

## Root cause (confirmed)

**A stray package part `ppt/media/.gitkeep` with an undeclared content type — an Open Packaging
Conventions (OPC) violation.** PowerPoint enforces OPC strictly and "repairs" any package containing a part
whose extension is neither declared as a `<Default Extension=…>` nor covered by an `<Override PartName=…>`
in `[Content_Types].xml`.

Confirmed end-to-end:

1. **The part is in the package.** Members of `ppt/media/` in the built pptx:
   ```
   ppt/media/.gitkeep      <-- stray
   ppt/media/image1.emf  image2.svg  image3.svg  image4.svg  image5.svg  image8.emf
   ```
2. **It has no declared content type.** `[Content_Types].xml` declares Defaults for exactly
   `bin, emf, jpeg, jpg, png, rels, svg, xml`. There is **no `Default Extension="gitkeep"`** and **no
   `Override PartName="/ppt/media/.gitkeep"`**. → invalid package.
3. **Source of the file.** The freshly-scaffolded deck's image dir contains only a 0-byte placeholder:
   ```
   projects/sea_range_telemetry/deck/images/.gitkeep   (0 bytes)
   ```
   (The `.gitkeep` exists so the otherwise-empty `images/` dir survives in git.)
4. **Mechanism.** `deck_core/lib.py` `build_pptx()` copies *every* file in the deck `images/` dir into
   `ppt/media/` with no dotfile/extension filter:
   ```python
   if images and Path(images).is_dir():
       for f in Path(images).iterdir():
           if f.is_file():
               parts[f"ppt/media/{f.name}"] = f.read_bytes()
   ```
   `lib.py` (`deck_sea_range_telemetry/lib.py`) passes `images = IMAGES if IMAGES.is_dir() else None`, and the
   scaffold `images/` dir *does* exist, so the loop runs and copies `.gitkeep` → `ppt/media/.gitkeep`.
5. **Why no other deck hits this.** The working decks' `images/` dirs hold real assets and no `.gitkeep`
   (e.g. consolidated has `virginia_construction.jpg` only). Their packages therefore never gain a stray
   undeclared part. This defect is specific to a **newly-scaffolded deck whose `images/` dir still contains
   only the `.gitkeep` placeholder** — i.e. this deck.

This is the defect that **survived the two earlier fixes below**: it lives in the packaging of the `images/`
dir, not in any slide's XML, so slide-level validation (schema, IDs, table geometry) never surfaced it.

## Recommended fix (NOT applied — logging only, per request)

Two independent options; either resolves it. The first is local to this project; the second is the durable
fix but touches a shared core file, so it is the maintainer's call.

- **Local / trivial:** remove the placeholder so nothing stray is packaged —
  `rm projects/sea_range_telemetry/deck/images/.gitkeep`. The empty `images/` dir then yields no media (build
  still green). Caveat: an empty dir does not persist in git; if the dir must stay tracked, prefer the durable
  fix or replace the keep-file with a real asset. (A `.gitignore`-style keep that PowerPoint won't choke on is
  not possible here because *any* extension absent from the Defaults list, including no extension, is invalid.)
- **Durable / shared:** harden `deck_core/lib.py`'s two media-copy loops (deck `images/` **and**
  `assets/media/`) to skip dotfiles, e.g. `if f.is_file() and not f.name.startswith('.')`. Optional belt-and-
  suspenders: before zipping, assert every packaged part's extension is in the content-types Default set (or has
  an Override) and raise loudly — this would have failed the build instead of producing a repairable pptx.
  This is a real latent bug in the shared pipeline that will bite any future freshly-scaffolded deck; flagged
  here, not changed, because the standing instruction this session was to leave the shared core files alone.

### Quick verification command (reproduces the finding)

```python
import zipfile, re
z = zipfile.ZipFile('projects/sea_range_telemetry/20260607_Sea Range Telemetry_vS.pptx')
ct = z.read('[Content_Types].xml').decode()
defaults = set(re.findall(r'Default Extension="([^"]+)"', ct))
overrides = set(re.findall(r'Override PartName="([^"]+)"', ct))
for n in z.namelist():
    ext = n.rsplit('.', 1)[-1].lower() if '.' in n.rsplit('/', 1)[-1] else ''
    if ext not in defaults and ('/' + n) not in overrides:
        print('UNDECLARED PART:', n)   # -> ppt/media/.gitkeep
```

## Investigation trail (what was ruled out, in order)

The repair dialog gives no part/line detail, so this was narrowed by elimination. Each step below was checked
against the built pptx and, where decisive, against the known-good `consolidated` deck.

1. **Well-formedness** — all four `ppt/slides/slideN.xml` parse (`xml.dom.minidom`, `lxml`). OK.
2. **Duplicate shape IDs** *(found + fixed; real but not the trigger)* — `s04` emitted `p:cNvPr id="47"`
   twice (an overlap-sidecar divider and the sidecar tie connector collided). PowerPoint requires
   slide-unique `cNvPr/@id`. Fixed: tie connector → `id="48"`. Re-scanned all four slides: unique. Repair
   persisted → not the (only) cause.
3. **Dangling relationships** — slides declare no `CHARTS`/`IMAGES` and use no `r:embed`/`r:id`; all `.rels`
   resolve. OK.
4. **OOXML schema validity** — validated each slide against `infra/ooxml_reference/schema/pml.xsd` with
   `lxml.etree.XMLSchema`: **all four VALID**. So the defect is a semantic/OPC constraint the XSD doesn't
   model, not malformed slide markup.
5. **Zero / negative extents & offsets** — present (`<a:ext cx="0" cy="0">` group node, 1-D connector
   extents) but **identical in the working consolidated deck**, so not the cause.
6. **Table cell insets exceeding column width** *(found + fixed; real but not the trigger)* — both native
   tables used **60,000 EMU "ghost band" columns** for the semantic side-bands, but every table cell carries
   default `marL=marR=45720` (91,440 total) → **negative content-box width** in 21 cells. Cross-deck scan
   confirmed this was unique to this deck (working decks: min gridCol ≥ ~500,000 EMU, 0 over-inset cells;
   mine: min 60,000, 21/66 over-inset). This is a legitimate PowerPoint repair trigger and was fixed by
   removing the ghost columns and carrying the orientation as **light full-cell tints on the real data
   columns** (the idiom the working `s20` crosswalk uses):
   - `s01` ledger → 3 cols (`Dimension | Included | Excluded`); Included tinted `E2E9EF`, Excluded `D9D9D9`.
   - `s04` crosswalk → 3 cols (`Activity | Treatment | Why`); Treatment column tinted per row
     (Counted `B6C8D8` / Discounted `F2F2F2` / Excluded `D9D9D9`).
   Re-validated: 0 over-inset cells, min gridCol 1,110,000–1,150,000, schema OK. Repair **still persisted**
   → not the (only) cause.
7. **`roundRect` via `text_box(prst="roundRect", geom_adj=…)`** — suspected as a novel construct; ruled out
   by confirming the working consolidated deck uses `prst="roundRect"` 7× in slide bodies and opens fine.
8. **Package-skeleton diff vs working deck** *(decisive)* — normalized part-name diff of my pptx against
   `consolidated`'s pptx. Shared skeleton parts (`theme1`, `slideMaster1` + rels, `tableStyles`, `presProps`,
   `viewProps`, `slideLayout4`, `LabelInfo`) are **byte-identical** (both copied from `infra/template` via
   `lib.py` `_ex()`), and non-slide content-type overrides match. The **only** structural difference:
   **`ppt/media/.gitkeep` present in mine, absent in the working deck.** That led directly to the OPC root
   cause above.

Note on the user's earlier hypotheses (dangling `slideLayout7+` rels; template `ppt/media` not copied):
checked against the *actual* `infra/template` and **did not apply** — the template has exactly 6 layouts
(`slideLayout1..6`), `slideMaster1.xml.rels` references only `oleObject1.bin` + the 6 layouts (all packaged),
and the layout/master `r:embed` media (`image1.emf`, `image2.svg`…`image5.svg`) all resolve to files present
in `infra/assets/media`. No core packaging change was warranted on those grounds, and none was made.

## State at end of session

- **Root cause identified, not yet fixed** (per request): `ppt/media/.gitkeep` undeclared part.
- **Hardening already applied this session and worth keeping** (both are genuine, independent PowerPoint
  repair triggers, just not the one that survived): the `s04` duplicate `id="47"` (step 2) and the 21
  over-inset ghost-band table cells across `s01`/`s04` (step 6).
- Slides remain schema-valid, unique-ID, no dangling rels, no over-inset cells; tables re-rendered and read
  correctly (light tints on the value/treatment columns, fit clears the commentary bands).
- Build command: `cd projects/sea_range_telemetry/deck && python build_deck.py`.

## One-line takeaway

A 0-byte `images/.gitkeep` scaffold placeholder is copied verbatim to `ppt/media/.gitkeep`; its `gitkeep`
extension is undeclared in `[Content_Types].xml`, making the OPC package invalid and forcing PowerPoint's
Repair dialog. Remove the placeholder (or filter dotfiles in `lib.py`'s media copy) to resolve.
