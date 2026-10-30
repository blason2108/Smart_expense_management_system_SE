#!/usr/bin/env python3
"""Create labels, milestones and issues from backlog.csv using the GitHub CLI.
Usage:  gh auth login   (once)
        python docs/backlog/create_issues.py OWNER/REPO "Smart Expense Board"   [--dry-run]
"""
import csv, subprocess, sys
from pathlib import Path

repo, project = sys.argv[1], sys.argv[2]
dry = "--dry-run" in sys.argv
run = lambda cmd: print(" ".join(cmd)) if dry else subprocess.run(cmd, check=False)

for ms in ("Sprint 1 (19-23 Oct)", "Sprint 2 (26-30 Oct)"):
    run(["gh", "api", f"repos/{repo}/milestones", "-f", f"title={ms}"])
for lb in ["P0", "P1", "P2", "foundation", "process", "backend", "database", "ci-cd", "security", "testing", "ui",
           "auth", "must", "category", "transactions", "budget", "dashboard", "data-integrity", "docs", "demo",
           "quality", "alerts", "analytics", "reports", "admin", "audit", "nfr", "user-story"]:
    run(["gh", "label", "create", lb, "-R", repo, "--force"])

for r in csv.DictReader(open(Path(__file__).with_name("backlog.csv"))):
    body = (f"**Type:** {r['Type']}\n**Requirement(s):** {r['Req IDs']}\n**Test case(s):** {r['Test Cases']}\n"
            f"**Story points:** {r['Points']}\n**Owner slot:** {r['Owner']} (replace with GitHub handle)\n\n"
            "**Acceptance criteria:** see SRS Section 4/5 and Test Plan Sections 6-8.\n- [ ] Implemented\n"
            "- [ ] Unit tests (line + branch)\n- [ ] PR reviewed by repo owner\n- [ ] RTM row updated")
    cmd = ["gh", "issue", "create", "-R", repo, "--title", f"[{r['ID']}] {r['Title']}", "--body", body,
           "--milestone", "Sprint 1 (19-23 Oct)" if r["Sprint"] == "1" else "Sprint 2 (26-30 Oct)",
           "--label", ",".join([r["Priority"]] + r["Labels"].split(",")), "--project", project]
    run(cmd)
