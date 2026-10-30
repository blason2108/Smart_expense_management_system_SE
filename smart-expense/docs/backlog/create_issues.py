#!/usr/bin/env python3
"""Create labels, milestones and issues from backlog.csv using the GitHub CLI.
Usage:  gh auth login   (once)
        python docs/backlog/create_issues.py OWNER/REPO "Smart Expense Board"   [--dry-run]
"""
import csv
import subprocess
import sys
from pathlib import Path

repo, project = sys.argv[1], sys.argv[2]
dry = "--dry-run" in sys.argv
def run(cmd):
    if dry:
        print(" ".join(cmd))
    else:
        subprocess.run(cmd, check=False)


import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parents[3] / "scripts/sync_part2_backlog.py"), run_name="__main__")
