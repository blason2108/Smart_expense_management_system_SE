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
        return 0
    return subprocess.run(cmd, check=False)


for ms in ("Sprint 1 (19-23 Oct)", "Sprint 2 (26-30 Oct)"):
    run(["gh", "api", f"repos/{repo}/milestones", "-f", f"title={ms}"])
for lb in [
    "P0",
    "P1",
    "P2",
    "foundation",
    "process",
    "backend",
    "database",
    "ci-cd",
    "security",
    "testing",
    "ui",
    "auth",
    "must",
    "category",
    "transactions",
    "budget",
    "dashboard",
    "data-integrity",
    "docs",
    "demo",
    "quality",
    "alerts",
    "analytics",
    "reports",
    "admin",
    "audit",
    "nfr",
    "user-story",
]:
    run(["gh", "label", "create", lb, "-R", repo, "--force"])

for row in csv.DictReader(open(Path(__file__).with_name("backlog.csv"), encoding="utf-8")):
    body = (
        f"**Type:** {row['Type']}\n**Requirement(s):** {row['Req IDs']}\n**Test case(s):** {row['Test Cases']}\n"
        f"**Story points:** {row['Points']}\n**Owner slot:** {row['Owner']} (replace with GitHub handle)\n\n"
        "**Acceptance criteria:** see SRS Section 4/5 and Test Plan Sections 6-8.\n- [ ] Implemented\n"
        "- [ ] Unit tests (line + branch)\n- [ ] PR reviewed by repo owner\n- [ ] RTM row updated"
    )
    cmd = [
        "gh",
        "issue",
        "create",
        "-R",
        repo,
        "--title",
        f"[{row['ID']}] {row['Title']}",
        "--body",
        body,
        "--milestone",
        "Sprint 1 (19-23 Oct)" if row["Sprint"] == "1" else "Sprint 2 (26-30 Oct)",
        "--label",
        ",".join([row["Priority"]] + row["Labels"].split(",")),
        "--project",
        project,
    ]
    run(cmd)
