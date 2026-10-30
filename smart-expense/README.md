# Smart Expense & Budget Management Application
UE24CS341A Software Engineering Mini-Project (Jackfruit) · SRS v1.0 · Team: PES2UG24CS119 / 120 / 122 / 123

Stack (SRS §2.1/§2.4): Python 3.12 · Django 5.2 LTS · PostgreSQL 16 · HTML/CSS/JS · Docker · GitHub Actions (CI) · Jenkins (CD) · SonarQube/SonarCloud.

**Status:** Sprint 1 (19–23 Oct) is the scope of this guide. Sprint 2 items are not required to run the project.

## Quick start (fastest path, about 5 minutes)
Uses SQLite so you do not need PostgreSQL or Docker. Good for a first run and for checking that your setup works.

```bash
git clone https://github.com/<ORG>/<REPO>.git && cd <REPO>
python3 -m venv .venv
source .venv/bin/activate            # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env                 # Windows: copy .env.example .env
```
Open `.env` and set `DB_ENGINE=sqlite`, then paste a secret key into `DJANGO_SECRET_KEY` (see Step 4). Then:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000 and the health check at http://127.0.0.1:8000/healthz/. For the real PostgreSQL setup, follow the full guide below.

---

## Step-by-step guide

### Step 1. Install prerequisites
| Tool | Version | Ubuntu/WSL | macOS (brew) | Windows (winget) |
|---|---|---|---|---|
| Git | 2.40+ | `sudo apt install git` | `brew install git` | `winget install Git.Git` |
| Python | 3.12 | `sudo apt install python3.12 python3.12-venv` | `brew install python@3.12` | `winget install Python.Python.3.12` |
| Docker Desktop / Engine | 24+ | `sudo apt install docker.io docker-compose-v2` | `brew install --cask docker` | `winget install Docker.DockerDesktop` |
| PostgreSQL (only if not using Docker) | 16 | `sudo apt install postgresql` | `brew install postgresql@16` | `winget install PostgreSQL.PostgreSQL.16` |
| GitHub CLI | 2.50+ | `sudo apt install gh` | `brew install gh` | `winget install GitHub.cli` |

Verify (Windows: use `python` instead of `python3`):
```bash
git --version && python3 --version && docker --version && gh --version
```
You should see Python 3.12.x. If Python is older, install 3.12 before continuing.

### Step 2. Get the code
```bash
git clone https://github.com/<ORG>/<REPO>.git
cd <REPO>
```
Check that `manage.py`, `requirements.txt`, `docker-compose.yml` and `.env.example` are in the folder (`ls`).

### Step 3. Create the virtual environment and install packages
```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```
Your prompt should now start with `(.venv)`. `requirements-dev.txt` already includes `requirements.txt`, plus pytest, ruff, bandit, pip-audit and locust.

### Step 4. Configure `.env`
```bash
cp .env.example .env                 # Windows: copy .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```
Paste the printed key into `DJANGO_SECRET_KEY=` in `.env`, and set `DB_PASSWORD` to a password of your choice. Never commit `.env` (it is in `.gitignore`).

| Variable | Purpose | Default / example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Session/CSRF signing; **required outside dev** | generate (command above) |
| `DJANGO_DEBUG` | Debug mode | `true` locally, `false` in CI/prod |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Needed behind an HTTPS proxy | blank locally |
| `TIME_ZONE` | Display time zone | `Asia/Kolkata` |
| `DB_ENGINE` | `postgres` or `sqlite` (quick runs only) | `postgres` |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` | PostgreSQL connection | `smart_expense` / `smart_expense` / *your password* / `localhost` / `5432` |
| `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS` | SEB-SR-001 HTTPS enforcement | `false`, `0` locally; `true`, `31536000` in prod |
| `EMAIL_BACKEND`, `DEFAULT_FROM_EMAIL` | SEB-F-010 alert delivery (sandbox = console) | console backend |
| `BUDGET_ALERT_DEFAULT_THRESHOLD_PERCENT` | Default warning threshold | `80` |
| `LOG_LEVEL` | Logging level (never log secrets, SEB-SR-005) | `INFO` |

### Step 5. Start the database
Pick **one** option.

**Option A: Docker (recommended).**
```bash
docker compose up -d db
docker compose ps                    # db should show "healthy"
```
`DB_PASSWORD` must be set in `.env`, otherwise compose stops with "set DB_PASSWORD in .env".

**Option B: native PostgreSQL.**
```bash
sudo -u postgres psql -c "CREATE USER smart_expense WITH PASSWORD 'your-password';"
sudo -u postgres psql -c "CREATE DATABASE smart_expense OWNER smart_expense;"
# Windows: run the same two statements in SQL Shell (psql) as the postgres user
```
Use the same password in `.env` as `DB_PASSWORD`.

**Option C: SQLite (no database install).** Set `DB_ENGINE=sqlite` in `.env`. Local use only; CI uses PostgreSQL.

### Step 6. Create tables and an admin user
```bash
python manage.py migrate
python manage.py createsuperuser     # admin account for SEB-F-017 testing
```

### Step 7. Run the app
```bash
python manage.py runserver
```
- App: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/healthz/ (should respond OK)
- Admin: http://127.0.0.1:8000/admin/ (log in with the superuser from Step 6)

Stop the server with `Ctrl+C`.

### Step 8. Run the checks (the same commands CI runs)
```bash
pytest                                              # line + branch coverage, report in coverage.xml
ruff check .
bandit -r . -x ./.venv,*/tests -ll
pip-audit -r requirements.txt
python manage.py makemigrations --check --dry-run   # must report "No changes detected"
```
All five should pass before you open a PR. To auto-fix most ruff issues: `ruff check . --fix`.

### Step 9. (Optional) Run the full stack in Docker
```bash
docker compose up --build            # web on :8000, Postgres on :5432
```
The `web` container runs `migrate` and then starts gunicorn. Create an admin in the running container with `docker compose exec web python manage.py createsuperuser`. Stop with `docker compose down` (add `-v` to also wipe the database volume).

---

## Sprint 1 workflow (19–23 Oct)

### Find your Sprint 1 items
`sprint_backlog.csv` lists every item with its sprint, owner, points, requirement IDs and test cases. To list Sprint 1 only:
```bash
python -c "import csv; [print(r['ID'], '|', r['Title'], '|', r['Owner'], '|', r['Points']) for r in csv.DictReader(open('sprint_backlog.csv', encoding='utf-8')) if r['Sprint']=='1']"
```

### Work on an item
```bash
git checkout main && git pull
git checkout -b feature/US-05-category-crud          # feature/<ID>-<short-name>
# ...write code and tests...
pytest && ruff check .
git add . && git commit -m "US-05: add category model"
git push -u origin feature/US-05-category-crud
gh pr create --fill --body "Closes #<issue-number>"
```
Rules:
- Commit format: `US-05: short description`. PR body must contain `Closes #<issue>`.
- Follow the submitted SRS, SAD and Test Plan. Note any deviation so it can be explained in the final demo.
- **Every member must have commits. The assigned member opens the PR; the repo owner reviews and merges.**
- GitHub Actions runs on every PR; it must be green before merging.

### Sprint 1 deliverables checklist
- [ ] All Sprint 1 items merged to `main` through PRs
- [ ] GitHub Actions enabled and passing
- [ ] App runs end to end (Steps 6–7 work on a fresh clone)
- [ ] One-minute video of the working product uploaded to the repo
- [ ] Deviations from the SRS/SAD/Test Plan written down

---

## GitHub setup (once, by the repo owner)
```bash
gh auth login
gh project create --owner <ORG_OR_USER> --title "Smart Expense Board"   # then link it to the repo in Project > Settings
python docs/backlog/create_issues.py <OWNER>/<REPO> "Smart Expense Board" --dry-run   # inspect, then re-run without the flag
```
Then: Settings > Branches > protect `main` (PR required, 1 review, CI must pass) · Settings > Actions > enable · add `SONAR_TOKEN` secret (SonarCloud) · replace owner slots M1–M4 in issues with GitHub handles.

---

## Troubleshooting
| Problem | Fix |
|---|---|
| `set DB_PASSWORD in .env` when running compose | Add `DB_PASSWORD=...` to `.env` |
| `connection refused` on port 5432 | Database is not running: `docker compose up -d db`, or start your local PostgreSQL service |
| `password authentication failed` | `DB_PASSWORD` in `.env` differs from the one the database was created with. For Docker: `docker compose down -v` and start again |
| Port 5432 already in use | A native PostgreSQL is running. Stop it, or use Option B with that instance |
| `ModuleNotFoundError` / `django not found` | Virtual environment not active. Re-run the activate command from Step 3 |
| `DisallowedHost` error | Add the host to `DJANGO_ALLOWED_HOSTS` in `.env` |
| `makemigrations --check` reports changes | Run `python manage.py makemigrations`, commit the new migration files |
| Windows: script activation blocked | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell |

## Layout
`config/` settings · one Django app per SRS module (`accounts categories transactions budgets alerts dashboard reports adminpanel audit`) · `templates/` · `docs/backlog/` · `.github/workflows/ci.yml` · `Jenkinsfile` · `sonar-project.properties`.