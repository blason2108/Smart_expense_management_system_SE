# Part 2 final report draft

Validation date: 15 November 2026. The original sprint dates and the later recovery dates are recorded in the [readiness audit](readiness.md). This report documents the recovered application for team and repository-owner review.

## Delivered product

The Django application keeps each user's categories, transactions, and budgets private. Its dashboard calculates income, expenses, and balance from stored transactions. Budgets recalculate as expenses change and surface warnings or exceeded status. The reports page lists matching transactions, charts expenses by category and month, and exports the filtered records and totals to CSV and PDF. The Django admin uses Django's staff and model permissions. Auditable actions include login, logout, failed login, and administrative user changes.

## Verification

- SQLite and PostgreSQL 16.2 each ran 92 pytest cases and reached 97.59% combined line and branch coverage. Ruff, Django system and migration checks, Bandit's medium/high severity gate, and the runtime dependency audit passed.
- PostgreSQL restart smoke preserved both the authenticated session and the exact October CSV response across a controlled application process restart.
- Firefox 159 and Chromium headless 153 ran the core browser workflows on a disposable local PostgreSQL deployment. The checks covered sign-in and sign-out, expense addition/edit/deletion, dashboard totals, budget warnings, invalid budget feedback, budget creation, date-range reports, chart bars, and opening the downloaded CSV and PDF.
- Locust 2.47 ran 10 simulated users for 30 seconds against the seeded local PostgreSQL deployment. The dashboard p90 was 76 ms and filtered transactions p90 was 41 ms, with zero failed requests out of 289. The target was 3,000 ms. This run used seeded data, one demo login, and a local Django server. Retain separate results if the course requires a different host or load profile. See the [run summary](evidence/2026-11-15-locust.txt).
- The [Sprint 1](../demo/sprint-1.mp4) and [Sprint 2](../demo/sprint-2.mp4) browser recordings are 45 seconds and 103 seconds. They're silent and show recovery data captured on the validation date. Team review and recording acceptance are pending.

## Issue evidence and remaining work

| Issues | Evidence or remaining acceptance |
|---|---|
| #20, #22, #23 | Account/security cases, budget lifecycle and dashboard-vs-records tests passed. Owner reviews the test evidence and merges the completion PR. |
| #24 | Sprint 1 working-product recording supplied. Owner verifies the recording and merges it. |
| #25 | [LLM prompt log](../llm-prompts.md) updated. Each assigned member records the prompts they used and their own explanation, then the owner reviews. |
| #26 | [RTM](rtm.md) and [deviations](deviations.md) updated against the SRS/Test Plan. Compare with the original submitted SAD or record a documented approved deviation. |
| #31 | SonarQube quality gate is wired to Actions. Provision the project, configure variables and secret, and retain the actual gate result. |
| #32 | Jenkins builds and tests before the gated main-branch Compose deployment. Configure the job and a disposable deployment target, then retain the pipeline log. |
| #35–#37 | Charts, month/custom-range reporting, and CSV/PDF verified. Assigned member verifies the results and records their contribution before owner review/merge. |
| #38–#40 | Admin access, timestamped audit history, and input handling verified by the app's automated tests. Assigned member verifies the checks and records their contribution before owner review/merge. |
| #41 | Local benchmark passed. Confirm the accepted environment and load profile, record the run from the target if required, and have the owner approve the result. |
| #42 | PostgreSQL-backed application restart passed. Owner confirms the restart scope and reviews the result. |
| #43 | Firefox and Chromium automation passed. Use Chrome if exact browser branding is required and record the representative-user usability walk-through. |
| #44 | [PR #48](https://github.com/blason2108/Smart_expense_management_system_SE/pull/48) contains the maintainability review. Santosh verifies it and Blason reviews and merges it. |
| #45 | Sprint 2 recording and this report are prepared. Final acceptance, freeze tag and release require all applicable checks and owner approval. |

The [populated Project board](https://github.com/users/SantoshKumarBollavaram/projects/1) was recorded in the prior recovery. Verify the repository's native Project link with Blason before the freeze. The original submitted SAD remains outstanding.

## Service and release commands

Run the checks from a checkout of the reviewed branch:

```bash
cd smart-expense
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
DB_ENGINE=sqlite python manage.py check
DB_ENGINE=sqlite python manage.py makemigrations --check --dry-run
ruff check .
DB_ENGINE=sqlite pytest --cov-fail-under=70
```

For #31, set repository Actions variables `SONAR_HOST_URL`, `SONAR_PROJECT_KEY`, and `SONAR_ORGANIZATION` for SonarQube Cloud. Set the analysis token as the `SONAR_TOKEN` Actions secret. Use a Sonar project that supports the repository's branch/PR analysis. Dispatch CI from the ref containing the workflow and open the run to confirm the Sonar step ran and the quality gate passed:

```bash
gh workflow run ci.yml --repo blason2108/Smart_expense_management_system_SE --ref main
gh run list --repo blason2108/Smart_expense_management_system_SE --workflow ci.yml --branch main --limit 3
```

For #32, set the Jenkins Multibranch Pipeline script path to `smart-expense/Jenkinsfile`. Run it on an agent with Python and Docker Compose v2, with `smart-expense/.env` supplied from the demonstration host configuration. Verify checkout, validation, image build and the approval-gated deployment from `main`, then check `/healthz/` on that deployment. The Docker health check uses the locally accessible HTTP endpoint on port 8000.

After external checks, team sign-offs, demos and decisions on deviations are recorded, the owner can freeze the reviewed default-branch commit from the repository root:

```bash
git fetch origin main
git tag -a part2-freeze origin/main -m "Part 2 submission freeze"
git push origin refs/tags/part2-freeze
gh release create part2-freeze --repo blason2108/Smart_expense_management_system_SE \
  --verify-tag --title "Part 2 submission freeze" --notes-file docs/part2/final-report.md
gh issue close 45 --repo blason2108/Smart_expense_management_system_SE --reason completed
```
