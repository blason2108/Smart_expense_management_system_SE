# Executed automated validation

Execution environment: Python 3.12.14, Django 5.2.18, SQLite; local recovery build. These retained local results are supplemented by the live CI evidence below. They do not prove full browser compatibility, production HTTPS or manual user acceptance.

- Pytest: **78 passed**; combined line/branch coverage **97.00%**, over the existing 70% CI threshold.
- Coverage includes accounts, categories, transactions, budgets, dashboard, reports and audit. Test files, migrations and demo management command are excluded. The production command and admin mutation paths require additional review/manual coverage.
- Ruff: passed after formatting and import cleanup.
- Django migrations applied successfully to a fresh local database.
- Bandit medium/high severity gate: passed; one low-severity finding remains (development fallback secret configuration). Production mode rejects that fallback key.
- Dependency audit: `pip-audit -r requirements.txt` completed with `No known vulnerabilities found` in this execution.
- No real browser session was available: Playwright browser download failed with a truncated/invalid archive. No cross-browser or video result is claimed.

Evidence: [JUnit results](evidence/test-results.xml), [coverage XML](evidence/coverage.xml).

Tests exercise valid/invalid registration; duplicate/case-insensitive email; login/logout; password hash; auth/audit events and secret omission; protected routes; admin access denial; CSRF; configured HTTPS redirect/HSTS; category CRUD/duplicate handling/referenced deletion; income/expense CRUD; invalid amounts/dates/type mismatch; cross-user object and category access; budget thresholds/date boundaries/updates/deletion; filters; aggregate summaries; report exports; CSV formula escaping and template escaping.

## Outstanding acceptance

Run final main-branch CI after all accepted changes, performance under defined concurrent load (p90 ≤3 seconds), committed-data restart recovery, Chrome/Firefox core flows, representative-user walkthrough, original SAD comparison and production HTTPS checks. Keep actual outputs and approvals. Do not mark NFRs passed based on configuration or a local unit test alone.

## Reproducing NFR checks

A local restart smoke script is provided. After seeding the `demo` user with your own `DEMO_PASSWORD`, run from the repo root with the application virtual environment active:

```bash
export DB_ENGINE=sqlite
python scripts/check_local_restart.py
```

It starts its own server on port 8765, logs in, compares an authenticated CSV before/after a process restart, and stops only the server it started. A local pass is not proof of PostgreSQL infrastructure recovery.

For a defined academic-load trial, start the app on port 8000, seed demo data, then from `smart-expense/`:

```bash
locust -f tests/load/locustfile.py --host http://127.0.0.1:8000 --headless -u 5 -r 1 -t 30s --csv load-results
```

The workload is five concurrent users reading dashboards and transaction histories. Inspect each endpoint's 90th percentile and failure count in the CSV. This is an explicit proposed trial, not a faculty-approved definition of normal deployment load. Run a separate representative create/update transaction workload for complete performance acceptance.

Executed local restart smoke: PASS — authenticated October CSV and session persisted across restarting the locally started Django server. Production PostgreSQL restart remains pending.

## Subsequent execution evidence

- User's Ubuntu laptop: Python 3.12.3 / Django 5.2.18; **78 passed in 41.33 seconds**, combined coverage **97.00%** (terminal output provided in this session).
- Live PostgreSQL workflow: [successful run 41099229977](https://github.com/blason2108/Smart_expense_management_system_SE/actions/runs/41099229977) at recovery commit `11ec385`. This supersedes the initial state in which no live workflow had run.
- User-provided browser screenshots show persisted Food/Salary categories and a Food budget at **850.00 / 1000.00 INR (85.0%)**, showing **Warning** at the configured 80% threshold. This is a limited browser smoke check, not complete usability/compatibility acceptance.
- Project sync output reports 41 issues imported with Story Points. Native repository linking is still pending and is not counted as passed.

## Manual transaction lifecycle verification — 30 October 2026

Executed by the user in the local browser and checked against the three supplied screenshots. Test data: Salary income 10000.00 INR, initial Food expense 850.00 INR, Food budget 1000.00 INR, warning threshold 80%. These results verify the displayed values and alert state; they do not establish every acceptance criterion for the mapped requirements.

| Check | Action | Expected and observed result | Result | Evidence |
|---|---|---|---|---|
| MAN-01 | Add Food expense 200.00 within budget period | Expenses 1050.00; balance 8950.00; budget 105%; Exceeded | Pass | [Screenshot](evidence/manual/add-expense-exceeded.png) |
| MAN-02 | Edit the added expense from 200.00 to 100.00 | Expenses 950.00; balance 9050.00; budget 95%; Warning | Pass | [Screenshot](evidence/manual/edit-expense-warning.png) |
| MAN-03 | Delete that 100.00 expense | Expenses 850.00; balance 9150.00; budget 85%; Warning; deleted row absent | Pass | [Screenshot](evidence/manual/delete-expense-recalculated.png) |

Requirement mapping: SEB-F-005, SEB-F-006, SEB-F-009, SEB-F-010 and SEB-F-011. The uploaded expanded Test Plan separates transaction edit (TC-TXN-03) and delete (TC-TXN-04); budget monitoring, alerts and dashboard map to TC-BUD-02, TC-ALT-01 and TC-DASH-01 respectively.

Still unverified manually in this session: CSV contents, second-account isolation, admin mutations and their audit entries, full Chrome/Firefox compatibility, performance acceptance, production HTTPS and usability sign-off. Do not copy these three passes into those pending results.

## Duplicate-email administrator setup regression

The user attempted createsuperuser with an email already used by an ordinary account. The case-insensitive email database constraint prevented the duplicate, but the stock command displayed an IntegrityError traceback. A separate create_demo_admin command now validates duplicate emails before creation and reports a clear error for a concurrent identity collision. Ordinary accounts are not promoted.

New local execution after the fix: **81 tests passed in 17.33 seconds**, combined coverage **97.00%**, on Python 3.12.14 / Django 5.2.18 / SQLite. The three added regression cases check exact duplicate email, case-insensitive duplicate email, and separate administrator creation with the existing standard account left unchanged. [JUnit evidence](evidence/admin-command-tests.xml). Management commands remain excluded from the coverage percentage, as documented earlier.

The user's admin login screenshot also confirms that the ordinary account is denied administration access. It does not demonstrate a successful administrator login, admin mutation or audit-entry creation; those manual checks are still pending.
