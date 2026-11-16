# Unit test coverage

Measured on 16 November 2026 with Python 3.12 and coverage.py 7.17.3.
Tested commit `7a9d33c2fa4858365d27c8056b08ac2516f60971`.
The run executed `smart-expense/tests/unit/` without a database connection.

| Metric | Result |
|---|---:|
| Unit tests passed | 23 |
| Statement coverage | 201/449 · 44.77% |
| Branch coverage | 10/62 · 16.13% |
| Combined coverage | 41.29% |

## Tests by area

| Suite | Passed |
|---|---:|
| Budget thresholds and validation | 8 |
| Report scales and CSV formatting | 9 |
| Transaction category rules and filters | 6 |

## Coverage by file

Paths are relative to `smart-expense/`. The table includes files with measured statements.

| File | Statements covered | Branches covered | Combined coverage |
|---|---:|---:|---:|
| `accounts/admin.py` | 9/15 | — | 60.00% |
| `accounts/apps.py` | 4/4 | — | 100.00% |
| `accounts/forms.py` | 0/13 | 0/2 | 0.00% |
| `accounts/models.py` | 8/8 | — | 100.00% |
| `accounts/urls.py` | 0/5 | — | 0.00% |
| `accounts/views.py` | 0/15 | 0/2 | 0.00% |
| `audit/admin.py` | 9/12 | — | 75.00% |
| `audit/apps.py` | 6/6 | — | 100.00% |
| `audit/models.py` | 8/8 | — | 100.00% |
| `audit/signals.py` | 9/12 | — | 75.00% |
| `budgets/apps.py` | 4/4 | — | 100.00% |
| `budgets/forms.py` | 0/12 | — | 0.00% |
| `budgets/models.py` | 32/33 | 3/4 | 94.59% |
| `budgets/urls.py` | 0/4 | — | 0.00% |
| `budgets/views.py` | 0/22 | 0/4 | 0.00% |
| `categories/apps.py` | 4/4 | — | 100.00% |
| `categories/forms.py` | 0/15 | 0/6 | 0.00% |
| `categories/models.py` | 16/21 | 0/4 | 64.00% |
| `categories/urls.py` | 0/4 | — | 0.00% |
| `categories/views.py` | 0/32 | 0/4 | 0.00% |
| `dashboard/apps.py` | 4/4 | — | 100.00% |
| `dashboard/urls.py` | 0/4 | — | 0.00% |
| `dashboard/views.py` | 0/12 | — | 0.00% |
| `reports/apps.py` | 4/4 | — | 100.00% |
| `reports/pdf.py` | 6/17 | 0/4 | 28.57% |
| `reports/urls.py` | 0/4 | — | 0.00% |
| `reports/views.py` | 21/50 | 0/10 | 35.00% |
| `transactions/apps.py` | 4/4 | — | 100.00% |
| `transactions/forms.py` | 24/27 | 2/2 | 89.66% |
| `transactions/models.py` | 23/23 | 5/6 | 96.55% |
| `transactions/services.py` | 6/22 | 0/10 | 18.75% |
| `transactions/urls.py` | 0/4 | — | 0.00% |
| `transactions/views.py` | 0/25 | 0/4 | 0.00% |

## Reproduce

With the project virtual environment active, run from the repository root.

```bash
cd smart-expense
bash scripts/unit-coverage.sh
xdg-open unit-results/html/index.html
```

The [GitHub CI artifact](https://github.com/blason2108/Smart_expense_management_system_SE/actions/runs/43801364986/artifacts/14196880585) contains the interactive HTML report, coverage XML, and test results for the tested commit.
