# Release Readiness Checklist

Use this checklist before preparing a project release or demonstration. Mark an item complete only after it has been verified for the release candidate.

## Source control

- [ ] Confirm the intended release commit and branch.
- [ ] Review the changes included since the previous release.
- [ ] Confirm there are no accidental local files, credentials, or environment files in the change set.

## Application validation

- [ ] Install dependencies using the project's documented setup instructions.
- [ ] Verify required environment variables are documented and configured outside version control.
- [ ] Run the automated test suite.
- [ ] Run the project's configured linting and static checks.
- [ ] Check database migrations and apply them in the intended environment.
- [ ] Perform a basic end-to-end smoke test of sign-in and the main expense and budget workflows.

## Reporting and exports

- [ ] Verify report filters for the selected date range.
- [ ] Check that displayed totals and category summaries match the underlying transactions.
- [ ] Verify CSV and PDF exports can be opened and contain the expected report data.

## Handover

- [ ] Confirm setup and run instructions are current.
- [ ] Record known limitations and unresolved issues.
- [ ] Obtain the required review and approval before merging or publishing.
