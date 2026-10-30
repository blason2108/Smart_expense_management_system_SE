# LLM assistance log

## Recovery session — 30 October 2026

User requested: audit the existing GitHub repository and complete Part 2 backlog/sprints, working implementation, CI and documentation before proceeding to Part 3.

AI assistance: inspected SRS and Test Plan, existing scaffold, PR and issues; implemented registration, owner-scoped category/transaction/budget flows, report filtering and CSV export, dashboard, admin audit, seed command, migration files, tests, CI relocation and recovery documentation. Prepared backlog synchronization for the repository owner because live issue/branch writes returned HTTP 403.

Validation is recorded in `docs/part2/test-summary.md`. All code in this recovery is AI-assisted and must be reviewed. No teammate is represented as having performed an unobserved action. Earlier prompts are unknown; members must add their actual prompts rather than reconstructing fictitious history.

## Understanding to demonstrate

- Bhuvigna: registration validators, password hashing, session/CSRF flow, owner checks, admin/audit permissions.
- Santosh: Decimal amounts, category/type matching, form-scoped querysets, GET confirmation versus POST deletion, safe CSV text.
- Blason: migrations, PostgreSQL environment, budget inclusive periods and live aggregation, seed idempotency and constraints.
- Vishnu: repository-root workflow discovery, CI working-directory, coverage, dashboard totals, filtered reporting summaries.

These are review responsibilities, not claims that review has already happened. Each member adds their real explanation, code-review findings and PR links before submission.
