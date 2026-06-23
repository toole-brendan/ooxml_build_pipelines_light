"""rebuild_all - regenerate the workbook's extracted/ artifacts in dependency order, then build.

build_workbook.py only PACKAGES whatever is already in extracted/; it does not regenerate the
inputs. This orchestrator declares the generated-artifact order so a full rebuild is one
command. The build-stopping integrity checks in lib.build() are preserved (they run as the
final build stage) - this script never bypasses them.

Stages, in dependency order:

  [network] pull_prime_awards          -> extracted/prime_awards.csv              (SAM API; gated behind --pull)
  [offline] build_prime_scope_manifest -> prime_contract_scope.csv                (from tam scope summaries)
  [offline] build_swbs_crosswalk       -> hii_swbs_crosswalk.csv                  (HII work-item code -> SWBS)
  [offline] tag_ddg_transactions_swbs  -> DDG SWBS transaction tags
  [offline] build_program_transactions -> {ddg,virginia,columbia}_subaward_transactions.csv
  [offline] build_program_vendors      -> {ddg,virginia,columbia}_program_vendors.csv  (research-prep + row spine)
  [offline] build_supplier_master      -> supplier_master.csv                     (the dimension; imports NAICS precedence from build_program_vendors)
  [offline] build_subaward_activity    -> subaward_activity.csv
  [offline] build_ddg_swbs_rollup      -> ddg_swbs_by_subsystem.csv
  [build]   build_workbook             -> award_classification_refactor.xlsx      (runs the 7 integrity asserts)

Hand-maintained inputs (NOT regenerated here): extracted/deflators.csv,
extracted/naics6_archetype_map.csv, extracted/swbs_curated_c.csv, and
extracted/vendor_archetype_overrides.csv. These are hand-curated sources of truth - edit
them by hand. In particular do NOT run scripts/build_archetype_overrides.py: its archetype
columns now read from blank placeholders, so it silently overwrites the curated
vendor_archetype_overrides.csv with a near-empty table. It is intentionally excluded from
this orchestrator.

Usage:
    python3 scripts/rebuild_all.py          # offline stages + build
    python3 scripts/rebuild_all.py --pull   # also re-pull prime awards (network)
    python3 scripts/rebuild_all.py --list   # print the stage plan and exit
"""
from __future__ import annotations

import os
import subprocess
import sys

from _paths import REPO, REFACTOR, SCRIPTS

PY = sys.executable

# (key, is_network, argv) - run in this order.
STAGES = [
    ("pull_prime_awards",          True,  [PY, str(SCRIPTS / "pull_prime_awards.py")]),
    ("build_prime_scope_manifest", False, [PY, str(SCRIPTS / "build_prime_scope_manifest.py")]),
    ("build_swbs_crosswalk",       False, [PY, str(SCRIPTS / "build_swbs_crosswalk.py")]),
    ("tag_ddg_transactions_swbs",  False, [PY, str(SCRIPTS / "tag_ddg_transactions_swbs.py")]),
    ("build_program_transactions", False, [PY, str(SCRIPTS / "build_program_transactions.py")]),
    ("build_program_vendors:ddg",      False, [PY, str(SCRIPTS / "build_program_vendors.py"), "ddg"]),
    ("build_program_vendors:virginia", False, [PY, str(SCRIPTS / "build_program_vendors.py"), "virginia"]),
    ("build_program_vendors:columbia", False, [PY, str(SCRIPTS / "build_program_vendors.py"), "columbia"]),
    ("build_supplier_master",      False, [PY, str(SCRIPTS / "build_supplier_master.py")]),
    ("build_subaward_activity",    False, [PY, str(SCRIPTS / "build_subaward_activity.py")]),
    ("build_ddg_swbs_rollup",      False, [PY, str(SCRIPTS / "build_ddg_swbs_rollup.py")]),
    ("build_workbook",             False, [PY, str(REFACTOR / "build_workbook.py")]),
]


def main(argv: list[str]) -> int:
    do_pull = "--pull" in argv
    if "--list" in argv:
        for key, net, _cmd in STAGES:
            tag = "network" if net else "offline"
            skip = "   (skipped unless --pull)" if net and not do_pull else ""
            print(f"  [{tag}] {key}{skip}")
        return 0

    # build_workbook needs workbook_core (REPO) and the package (REFACTOR) importable.
    env = {**os.environ, "PYTHONPATH": f"{REPO}{os.pathsep}{REFACTOR}"}
    for key, net, cmd in STAGES:
        if net and not do_pull:
            print(f"== skip {key} (network; pass --pull to include) ==")
            continue
        print(f"== {key} ==")
        r = subprocess.run(cmd, cwd=str(REFACTOR), env=env)
        if r.returncode != 0:
            print(f"!! stage {key} failed (exit {r.returncode}); stopping.")
            return r.returncode
    print("\nrebuild_all: done.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
