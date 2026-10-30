# Publishing the prepared recovery

The connected GitHub account reported repository push permission, but the integration rejected issue creation and branch creation with HTTP 403. No live backlog changes, commits, PRs or merge are claimed by this recovery session.

The owner should check that the connected GitHub app has write access to this repository, including Issues and Contents, and reconnect if appropriate. Project permissions are separate; branch-protection changes require the repository owner/admin. Alternatively, use the following commands on your own authenticated computer.

The handoff ZIP contains source and a Git bundle preserving existing history plus the recovery branch. Extract the ZIP, open a terminal in the extracted package folder, then:

```bash
git clone --branch recovery/part2-working-product part2-recovery.bundle Smart_expense_management_system_SE
auth_repo=Smart_expense_management_system_SE
cd "$auth_repo"
git remote set-url origin https://github.com/blason2108/Smart_expense_management_system_SE.git
gh auth login
gh auth setup-git
git push -u origin recovery/part2-working-product
python3 scripts/sync_part2_backlog.py --apply --project-owner blason2108
gh pr create --base main --head recovery/part2-working-product --title 'Part 2: working expense tracker and recovery evidence' --body-file docs/part2/pr-description.md
```

Use the account that is actually performing the work. Project setup may need Blason's account. Do not change authors to invent team contributions. If the repo has changed since this snapshot, fetch current branches, review and resolve conflicts, and rerun tests before merging. Do not force-push over teammates' work.

Blason then reviews PR #27 and the recovery PR, confirms real contributor evidence, checks Actions, verifies demos and documentation, and approves the release only when the checklist is satisfied.
