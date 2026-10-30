# Smart Expense and Budget Management

Django mini-project for UE24CS341A. SRS and original Test Plan remain unchanged at repository root.

**Recovery status:** application code is on `recovery/part2-working-product`; owner review, team contribution checks, live board setup, video uploads and freeze approval remain open. This is not a claim of completion during the originally scheduled sprint dates.

## Run the recovered application

```bash
git clone https://github.com/blason2108/Smart_expense_management_system_SE.git
cd Smart_expense_management_system_SE
git switch recovery/part2-working-product
cd smart-expense
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export DB_ENGINE=sqlite
export DJANGO_DEBUG=true
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

Open http://127.0.0.1:8000/accounts/register/ and register. Create income/expense categories, add transactions and a category budget, then inspect dashboard and reports. SQLite is for local demonstrations; PostgreSQL remains the deployment database.

Optional deterministic demo data (use a password of your choice):

```bash
read -rsp 'Demo password (at least 12 characters): ' DEMO_PASSWORD
export DEMO_PASSWORD
python manage.py seed_demo
unset DEMO_PASSWORD
```

The demo username is `demo`. The command does not change the password of an existing demo account. Use `python manage.py createsuperuser` separately for an administrator; there is no shared default administrator password.

## Verification

From `smart-expense/` with the virtual environment active:

```bash
export DB_ENGINE=sqlite
ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run
pytest --cov-fail-under=70
bandit -r accounts categories transactions budgets dashboard reports audit config -x '*/tests/*' -ll
pip-audit -r requirements.txt
```

The repository-root `.github/workflows/ci.yml` runs the PostgreSQL validation job on pushes and PRs. A local pass does not prove a live Actions pass.

## Part 2 handoff

- [Readiness audit and remaining actions](docs/part2/readiness.md)
- [Team workflow and issue instructions](docs/part2/team-workflow.md)
- [Sprints and backlog](docs/part2/sprints.md)
- [As-built architecture](docs/part2/architecture.md)
- [Deviations](docs/part2/deviations.md)
- [Requirement traceability](docs/part2/rtm.md)
- [Executed automated test summary](docs/part2/test-summary.md)
- [One-minute and two-minute recording scripts](docs/demo/README.md)
- [LLM assistance log](docs/llm-prompts.md)

Part 3 manual test-case expansion and final evaluation are intentionally not claimed as finished.
