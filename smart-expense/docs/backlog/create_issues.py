#!/usr/bin/env python3
"""Use the idempotent repository script instead of the original duplicate-prone importer."""

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parents[3] / "scripts/sync_part2_backlog.py"), run_name="__main__")
