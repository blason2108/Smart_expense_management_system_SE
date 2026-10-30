The default branch contained the SRS/Test Plan but no runnable application. The unmerged scaffold also placed Actions under a subdirectory where GitHub would not discover it. This recovery adds a working expense tracker and moves CI to repository root with the correct application working directory.

Implements registration/authentication, private categories and income/expense CRUD, live budget progress and visible alerts, dashboard totals, date/category/type/text filtering, month/range reports, CSV export, user administration and credential-free audit events. Adds migrations, a deterministic demo seed, tests, requirement traceability, deviation log and backlog recovery tooling.

Validation: 78 local pytest tests passed, 97.00% combined line/branch coverage; Ruff and Django checks passed, migration drift check passed, Bandit medium/high gate passed, and pip-audit reported no known vulnerabilities. Local seeded pages/CSV and authenticated data/session preservation across a server process restart were checked. PostgreSQL Actions, real browser flows, deployed HTTPS, load acceptance and owner review remain pending.

This is AI-assisted recovery work, recorded on its actual date. It does not establish timely completion of either sprint or substitute for each member's own contribution/PR. The original submitted SAD was not available. Both demo recordings and owner-approved freeze remain outstanding; Part 3 manual sheets are not claimed complete. See docs/part2/readiness.md and deviations.md.

Preserves the existing scaffold history from PR #27 and merges the current main README change. Owner should review/merge #27 first, then recheck this diff.

Refs #1, #2, #3, #4, #5, #6, #7, #8, #9, #10, #11, #12, #13, #14, #15, #16, #17, #18, #19, #20, #21, #22, #23, #25, #26. Do not close items until their assigned-member and acceptance requirements are met.
