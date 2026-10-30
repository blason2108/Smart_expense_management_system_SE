#!/usr/bin/env python3
"""Create GitHub issues for Sprint 1 items from sprint_backlog.csv using the gh CLI.

Usage:
    python create_sprint1_issues.py OWNER/REPO --dry-run
    python create_sprint1_issues.py OWNER/REPO --project 1 \
        --assign M1=handle1 M2=handle2 M3=handle3 M4=handle4

Safe to re-run: issues whose title already starts with the item ID are skipped.
"""
import argparse
import csv
import json
import subprocess
import sys

SPRINT = "1"
MILESTONE = "Sprint 1"
MILESTONE_DUE = "2026-10-23T23:59:59Z"
PRIORITY_COLORS = {"P0": "b60205", "P1": "d93f0b", "P2": "fbca04"}


def run(cmd, check=True):
    result = subprocess.run(cmd, capture_output=True, text=True)  # noqa: S603
    if check and result.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd)}\n{result.stderr.strip()}")
    return result


def build_body(row):
    lines = [
        f"**ID:** {row['ID']}",
        f"**Type:** {row['Type']}",
        f"**Priority:** {row['Priority']}",
        f"**Story points:** {row['Points']}",
        f"**Owner:** {row['Owner']}",
        f"**Requirement IDs:** {row['Req IDs'] or '-'}",
        f"**Test cases:** {row['Test Cases'] or '-'}",
        "",
        "### Definition of done",
        "- [ ] Implemented per SRS / SAD / Test Plan",
        "- [ ] Tests written and passing (`pytest`, `ruff check .`)",
        "- [ ] PR opened with `Closes #<this issue>` and reviewed by the repo owner",
        "- [ ] Any deviation from the submitted documents noted in the deviation log",
    ]
    return "\n".join(lines)


def label_names(row):
    labels = [x.strip() for x in row["Labels"].split(",") if x.strip()]
    labels += [row["Priority"], f"type:{row['Type'].lower()}", f"points:{row['Points']}", "sprint-1"]
    return sorted(set(labels))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", help="OWNER/REPO")
    parser.add_argument("--csv", default="sprint_backlog.csv")
    parser.add_argument("--project", type=int,
                        help="Project NUMBER to add issues to (see: gh project list --owner OWNER; "
                             "needs: gh auth refresh -s project)")
    parser.add_argument("--assign", nargs="*", default=[], help="Owner mapping, e.g. M1=handle M2=handle")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    owners = dict(pair.split("=", 1) for pair in args.assign)

    with open(args.csv, encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["Sprint"].strip() == SPRINT]
    print(f"Found {len(rows)} Sprint {SPRINT} items in {args.csv}")

    if args.dry_run:
        for row in rows:
            who = owners.get(row["Owner"], "(unassigned)")
            print(f"[dry-run] {row['ID']}: {row['Title']} | {row['Priority']} | {row['Points']} pts | "
                  f"{row['Owner']} -> {who} | labels={label_names(row)}")
        print("Dry run only. Nothing was created.")
        return

    # Labels (idempotent) and milestone (ignore 'already exists')
    all_labels = {name for row in rows for name in label_names(row)}
    for name in sorted(all_labels):
        color = PRIORITY_COLORS.get(name, "ededed")
        run(["gh", "label", "create", name, "--repo", args.repo, "--color", color, "--force"])
    run(["gh", "api", f"repos/{args.repo}/milestones", "-f", f"title={MILESTONE}", "-f", f"due_on={MILESTONE_DUE}"],
        check=False)

    existing = json.loads(run(["gh", "issue", "list", "--repo", args.repo, "--state", "all",
                               "--limit", "500", "--json", "title"]).stdout)
    existing_titles = [i["title"] for i in existing]

    created = skipped = 0
    for row in rows:
        title = f"{row['ID']}: {row['Title']}"
        if any(t.startswith(f"{row['ID']}:") for t in existing_titles):
            print(f"skip   {row['ID']} (already exists)")
            skipped += 1
            continue
        cmd = ["gh", "issue", "create", "--repo", args.repo, "--title", title, "--body", build_body(row),
               "--milestone", MILESTONE]
        for name in label_names(row):
            cmd += ["--label", name]
        handle = owners.get(row["Owner"])
        if handle:
            cmd += ["--assignee", handle]
        url = run(cmd).stdout.strip()
        print(f"create {row['ID']} -> {url}")
        if args.project:
            added = run(["gh", "project", "item-add", str(args.project), "--owner", args.repo.split("/")[0],
                         "--url", url], check=False)
            if added.returncode != 0:
                print(f"  warning: could not add to project: {added.stderr.strip()}")
        created += 1

    print(f"Done. Created {created}, skipped {skipped}.")


if __name__ == "__main__":
    main()
