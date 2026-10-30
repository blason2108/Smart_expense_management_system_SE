# Executed automated validation

Execution environment: Python 3.12.14, Django 5.2.18, SQLite; local recovery build. This does not prove the PostgreSQL GitHub Actions run, browser compatibility, production HTTPS or manual user acceptance.

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

Run the PostgreSQL workflow, dependency audit, performance under defined concurrent load (p90 ≤3 seconds), committed-data restart recovery, Chrome/Firefox core flows, representative-user walkthrough, original SAD comparison and production HTTPS checks. Keep actual outputs and approvals. Do not mark NFRs passed based on configuration or a local unit test alone.

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
