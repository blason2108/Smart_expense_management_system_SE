# Team workflow

An issue is a tracked piece of work, not an error message. Its assignee implements it; points express relative effort, not hours. The PR proposes the code and links the issue. The owner reviews and merges it; only then should completion be recorded.

| Team member | GitHub | Existing primary scope |
|---|---|---|
| Bhuvigna | Bhuviiiii-prog | Authentication, isolation, security, deviation log |
| Santosh | SantoshKumarBollavaram | Categories, income/expense CRUD, transaction tests |
| Blason | blason2108 | Database, budgets, validation, seed data, owner reviews |
| Vishnu | vishnurohit-6300 | CI, UI, dashboard, reporting and analytics |

The shared image assigns FND-02 to Vishnu, the CSV assigns it to M2, while the live issue is assigned to Bhuvigna and the scaffold commit names Bhuvigna. Review this discrepancy as a team. The recovery does not rewrite existing attribution.

## Santosh's concrete steps

1. Restore/push the prepared recovery branch using the handoff commands.
2. Run the app and verify categories, income, expense, edit/delete and CSV search.
3. Open a PR from `recovery/part2-working-product` to `main`, identifying all AI-assisted cross-module work honestly. Reference issues #11–14 and #21 with `Refs`, not `Closes`, until assigned members and owner agree on acceptance.
4. Blason reviews PR #27 and the recovery PR. The recovery branch preserves scaffold history and includes the main README update; merge #27 first, then recheck the recovery diff.
5. Each teammate reviews their own module, makes a substantive verified contribution where needed, and opens their PR using their own account. Do not create fake commits or PRs on someone else's behalf.
6. The owner merges after green CI and review. Close only accepted issues with evidence.

## Member branch example

```bash
git switch main
git pull --ff-only
git switch -c feature/US-05-category-review
# Make and understand a real change, then run checks.
git add smart-expense/categories smart-expense/transactions/tests
git commit -m 'US-05: verify category ownership and validation'
git push -u origin feature/US-05-category-review
gh pr create --base main --title 'US-05: category ownership and validation' --body 'Refs #11. Include actual validation and deviations here.'
```

## Owner board and protection setup

After signing into the GitHub CLI with an account allowed to edit the repository and Project:

```bash
gh auth login
gh auth refresh -s project
python3 scripts/sync_part2_backlog.py --apply --project-owner blason2108
```

The script is a recovery action performed now. It reuses existing issues, preserves their content and assignees, and creates only missing Part 2 items. It deliberately excludes DOC-03, which belongs to the later Part 3 request. It creates/reuses a Project and links the repo. Project access may need the owner's account.

In the board UI, create Status columns Todo / In progress / In review / Done and Number field `Story Points`; copy the `points:N` labels into that field if desired. Filter views by `sprint-1` and `sprint-2`. Labels and issue bodies retain points even before a numeric field is populated.

The owner must enable branch protection on `main`: require PRs, one approving review, resolved conversations, and the CI `test` check after it exists. Do not use an auto-merge shortcut to replace owner review.
