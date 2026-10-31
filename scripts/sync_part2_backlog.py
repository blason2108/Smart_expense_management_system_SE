#!/usr/bin/env python3
"""Idempotent, explicit GitHub backlog recovery. Requires gh, authentication and Project write access."""

import argparse
import csv
import json
import subprocess
from pathlib import Path

REPO = "blason2108/Smart_expense_management_system_SE"
OWNERS = {
    "M1": "Bhuviiiii-prog",
    "M2": "SantoshKumarBollavaram",
    "M3": "blason2108",
    "M4": "vishnurohit-6300",
    "All": "blason2108",
}


def gh(*args, json_output=True):
    result = subprocess.run(["gh", *args], text=True, check=False, capture_output=True)
    if result.returncode:
        raise SystemExit(
            result.stderr.strip()
            or result.stdout.strip()
            or "GitHub CLI request failed."
        )
    return (
        json.loads(result.stdout)
        if json_output and result.stdout.strip()
        else result.stdout
    )


def pages(endpoint):
    # Older Ubuntu gh releases lack --slurp. Decode the concatenated JSON pages.
    output = gh("api", "--paginate", endpoint, json_output=False)
    decoder = json.JSONDecoder()
    items = []
    while output.strip():
        page, end = decoder.raw_decode(output.lstrip())
        if not isinstance(page, list):
            raise SystemExit(
                f"Expected a JSON list from {endpoint}, got {type(page).__name__}."
            )
        items.extend(page)
        output = output.lstrip()[end:]
    return items


def api(method, endpoint, data):
    # Send JSON through stdin rather than shell interpolation.
    result = subprocess.run(
        ["gh", "api", "--method", method, endpoint, "--input", "-"],
        input=json.dumps(data),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def link_repository(project_id):
    repository = gh("api", f"repos/{REPO}")
    result = api(
        "POST",
        "graphql",
        {
            "query": """mutation($project:ID!,$repository:ID!){
            linkProjectV2ToRepository(input:{projectId:$project,repositoryId:$repository}){
                clientMutationId
            }
        }""",
            "variables": {"project": project_id, "repository": repository["node_id"]},
        },
    )
    if result.get("errors"):
        raise RuntimeError("; ".join(error["message"] for error in result["errors"]))
    if result.get("data", {}).get("linkProjectV2ToRepository") is None:
        raise RuntimeError("GitHub did not confirm the repository link.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Perform writes; default only shows the plan",
    )
    parser.add_argument("--project-owner", default="blason2108")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    with (root / "smart-expense/docs/backlog/backlog.csv").open(
        encoding="utf-8", newline=""
    ) as f:
        rows = [r for r in csv.DictReader(f) if r["ID"] != "DOC-03"]
    if not args.apply:
        for row in rows:
            print(
                f"Sprint {row['Sprint']} | {row['ID']} | {row['Points']} points | {OWNERS[row['Owner']]}"
            )
        print(
            "No writes performed. Add --apply to sync issues, milestones and Project."
        )
        return
    existing = pages(f"repos/{REPO}/issues?state=all&per_page=100")
    milestones = pages(f"repos/{REPO}/milestones?state=all&per_page=100")
    milestone_by_sprint = {}
    for sprint, due in [("1", "2026-10-23T23:59:59Z"), ("2", "2026-10-30T23:59:59Z")]:
        name = f"Sprint {sprint}"
        found = next((m for m in milestones if m["title"].startswith(name)), None)
        if found is None:
            found = api(
                "POST",
                f"repos/{REPO}/milestones",
                {
                    "title": name,
                    "due_on": due,
                    "description": "Original assignment dates; recovered backlog recorded on actual sync date.",
                },
            )
        milestone_by_sprint[sprint] = found["number"]
    labels = {l["name"] for l in pages(f"repos/{REPO}/labels?per_page=100")}
    needed = (
        {"sprint-1", "sprint-2"}
        | {f"points:{r['Points']}" for r in rows}
        | {r["Priority"] for r in rows}
    )
    for name in sorted(needed - labels):
        api("POST", f"repos/{REPO}/labels", {"name": name, "color": "167D8D"})
    linked = []
    for row in rows:
        ident = row["ID"]
        issue = next(
            (
                i
                for i in existing
                if not i.get("pull_request")
                and (
                    i["title"].startswith(ident + ":")
                    or i["title"].startswith("[" + ident + "]")
                )
            ),
            None,
        )
        wanted = [row["Priority"], f"sprint-{row['Sprint']}", f"points:{row['Points']}"]
        if issue:
            # Preserve authored text and existing owners; update only sprint/point metadata and missing assignment.
            all_labels = {
                l["name"]
                for l in issue["labels"]
                if not l["name"].startswith(("sprint-", "points:"))
            }
            update = {
                "milestone": milestone_by_sprint[row["Sprint"]],
                "labels": sorted(all_labels | set(wanted)),
            }
            if not issue["assignees"]:
                update["assignees"] = [OWNERS[row["Owner"]]]
            issue = api("PATCH", f"repos/{REPO}/issues/{issue['number']}", update)
        else:
            body = (
                f"**ID:** {ident}\n**Sprint:** {row['Sprint']}\n**Story points:** {row['Points']}\n"
                f"**Owner:** {OWNERS[row['Owner']]}\n**Requirement IDs:** {row['Req IDs']}\n"
                f"**Test cases:** {row['Test Cases']}\n\n"
                "Created during Part 2 recovery; actual creation time is authoritative.\n\n"
                "- [ ] Implemented and explained by assigned member\n- [ ] Tests executed with evidence\n"
                "- [ ] PR opened by member and reviewed/merged by owner\n- [ ] RTM and deviations updated\n"
            )
            issue = api(
                "POST",
                f"repos/{REPO}/issues",
                {
                    "title": f"{ident}: {row['Title']}",
                    "body": body,
                    "assignees": [OWNERS[row["Owner"]]],
                    "labels": wanted,
                    "milestone": milestone_by_sprint[row["Sprint"]],
                },
            )
        linked.append((issue["html_url"], float(row["Points"])))
        print(issue["html_url"])
    # Projects operations require Project scope and project-owner access. Failure leaves issue work intact.
    try:
        projects = gh(
            "project",
            "list",
            "--owner",
            args.project_owner,
            "--format",
            "json",
            "--limit",
            "100",
        )["projects"]
        project = next(
            (p for p in projects if p["title"] == "Smart Expense Part 2"), None
        )
        if project is None:
            project = gh(
                "project",
                "create",
                "--owner",
                args.project_owner,
                "--title",
                "Smart Expense Part 2",
                "--format",
                "json",
            )
        number = str(project["number"])
        # gh 2.45 rejects cross-owner links before contacting GitHub. Use the
        # API with the actual repository ID; normal GitHub authorization applies.
        repository_linked = False
        try:
            link_repository(project["id"])
            repository_linked = True
            print("Repository linked to Project.")
        except (subprocess.CalledProcessError, RuntimeError, SystemExit) as exc:
            print("Repository link pending:", getattr(exc, "stderr", None) or str(exc))
            print(
                "Continuing to import issues and story points; repository linking still needs verification."
            )
        fields = gh(
            "project",
            "field-list",
            number,
            "--owner",
            args.project_owner,
            "--format",
            "json",
        )["fields"]
        points = next((f for f in fields if f["name"] == "Story Points"), None)
        if points is None:
            points = gh(
                "project",
                "field-create",
                number,
                "--owner",
                args.project_owner,
                "--name",
                "Story Points",
                "--data-type",
                "NUMBER",
                "--format",
                "json",
            )
        for url, value in linked:
            item = gh(
                "project",
                "item-add",
                number,
                "--owner",
                args.project_owner,
                "--url",
                url,
                "--format",
                "json",
            )
            gh(
                "project",
                "item-edit",
                "--id",
                item["id"],
                "--project-id",
                project["id"],
                "--field-id",
                points["id"],
                "--number",
                str(value),
                json_output=False,
            )
        print(f"Imported/updated {len(linked)} issues and their Story Points.")
        if not repository_linked:
            print(
                "ACTION REQUIRED: Project populated, but native repository link is not confirmed."
            )
            print(
                "The repository owner may need to create/link a Project under their account."
            )
        print(
            "Project:",
            project.get(
                "url",
                f"https://github.com/users/{args.project_owner}/projects/{number}",
            ),
        )
    except (subprocess.CalledProcessError, RuntimeError, SystemExit) as exc:
        print("Issue sync completed, but Project setup is incomplete.")
        print(getattr(exc, "stderr", None) or str(exc))
        print("Rerunning is safe: existing issues and the named Project are reused.")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
