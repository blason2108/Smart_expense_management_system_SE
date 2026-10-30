# Smart Expense & Budget Management Application
UE24CS341A Software Engineering Mini-Project (Jackfruit) · SRS v1.0 · Team: PES2UG24CS119 / 120 / 122 / 123

Stack (SRS §2.1/§2.4): Python 3.12 · Django 5.2 LTS · PostgreSQL 16 · HTML/CSS/JS · Docker · GitHub Actions (CI) · Jenkins (CD) · SonarQube/SonarCloud.

## 1. Install prerequisites
| Tool | Version | Ubuntu/WSL | macOS (brew) | Windows (winget) |
|---|---|---|---|---|
| Git | 2.40+ | `sudo apt install git` | `brew install git` | `winget install Git.Git` |
| Python | 3.12 | `sudo apt install python3.12 python3.12-venv` | `brew install python@3.12` | `winget install Python.Python.3.12` |
| PostgreSQL (or use Docker) | 16 | `sudo apt install postgresql` | `brew install postgresql@16` | `winget install PostgreSQL.PostgreSQL.16` |
| Docker Desktop / Engine | 24+ | `sudo apt install docker.io docker-compose-v2` | `brew install --cask docker` | `winget install Docker.DockerDesktop` |
| GitHub CLI | 2.50+ | `sudo apt install gh` | `brew install gh` | `winget install GitHub.cli` |
Verify: `git --version && python3 --version && docker --version && gh --version` (Windows: `python`).

## 2. Get the code and Python environment
```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env                 # Windows: copy .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"   # paste into DJANGO_SECRET_KEY
```

## 3. Environment variables (`.env`)
| Variable | Purpose | Default / example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Session/CSRF signing; **required outside dev** | generate (see above) |
| `DJANGO_DEBUG` | Debug mode | `true` locally, `false` in CI/prod |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Needed behind HTTPS proxy | blank locally |
| `TIME_ZONE` | Display time zone | `Asia/Kolkata` |
| `DB_ENGINE` | `postgres` or `sqlite` (quick tests only) | `postgres` |
| `DB_NAME`/`DB_USER`/`DB_PASSWORD`/`DB_HOST`/`DB_PORT` | PostgreSQL connection | `smart_expense` / `smart_expense` / *your password* / `localhost` / `5432` |
| `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS` | SEB-SR-001 HTTPS enforcement | `false`, `0` locally; `true`, `31536000` in prod |
| `EMAIL_BACKEND`, `DEFAULT_FROM_EMAIL` | SEB-F-010 alert delivery (sandbox = console) | console backend |
| `BUDGET_ALERT_DEFAULT_THRESHOLD_PERCENT` | Default warning threshold | `80` |
| `LOG_LEVEL` | Logging level (never log secrets, SEB-SR-005) | `INFO` |

## 4. Database
**Option A: Docker (recommended).** Set `DB_PASSWORD` in `.env`, then `docker compose up -d db`.
**Option B: native PostgreSQL.**
```bash
sudo -u postgres psql -c "CREATE USER smart_expense WITH PASSWORD 'your-password';"
sudo -u postgres psql -c "CREATE DATABASE smart_expense OWNER smart_expense;"
# Windows: run the same two statements in SQL Shell (psql) as the postgres user
```
Then:
```bash
python manage.py migrate
python manage.py createsuperuser          # admin account for SEB-F-017 testing
python manage.py runserver                # http://127.0.0.1:8000  (health: /healthz/)
```
Quick no-Postgres run: `DB_ENGINE=sqlite python manage.py migrate` (local only; CI uses PostgreSQL).

## 5. Tests, lint, security checks (same commands CI runs)
```bash
pytest                                  # line + BRANCH coverage (pytest.ini); report in coverage.xml
ruff check .
bandit -r . -x ./.venv,*/tests -ll
pip-audit -r requirements.txt
python manage.py makemigrations --check --dry-run
```
## 6. Full stack in Docker
```bash
docker compose up --build               # web on :8000, Postgres on :5432
```
## 7. GitHub setup (once, by repo owner)
```bash
gh auth login
gh project create --owner <ORG_OR_USER> --title "Smart Expense Board"   # then link it to the repo in Project > Settings
python docs/backlog/create_issues.py <OWNER>/<REPO> "Smart Expense Board" --dry-run   # inspect, then re-run without the flag
```
Then: Settings > Branches > protect `main` (PR required, 1 review, CI must pass) · Settings > Actions > enable · add `SONAR_TOKEN` secret (SonarCloud) · replace owner slots M1-M4 in issues with GitHub handles.
Branch/commit convention: `feature/US-05-category-crud`, commits `US-05: add category model`, PR "Closes #<issue>". **Every member must have commits; the assigned member opens the PR and the repo owner reviews/merges.**

## 8. Layout
`config/` settings · one Django app per SRS module (`accounts categories transactions budgets alerts dashboard reports adminpanel audit`) · `templates/` · `docs/backlog/` · `.github/workflows/ci.yml` · `Jenkinsfile` · `sonar-project.properties`.
