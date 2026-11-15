# Demo recording instructions

Both clips were captured from the working application with seeded demonstration data on 15 November 2026. They are silent browser recordings with no narrator or participant attribution.

- [Sprint 1 recording](sprint-1.mp4), 45 seconds. Sign in, view categories, add/edit/delete a Food expense, and verify the dashboard balance and budget warning.
- [Sprint 2 recording](sprint-2.mp4), 1 minute 43 seconds. Trigger a budget overrun, filter transactions, validate and create a budget, run a dated report and start the CSV/PDF downloads, then inspect user administration and audit history.

The scripts below are available for a team-narrated retake, if the owner needs one for the submission.

## Preparation

Run the root README setup. Use `seed_demo` or register your own disposable demo account. Demo seed has October 2026 salary 30000, food expense 850 and a Food budget 1000 at 80%, so the initial balance is 29150 and Food displays Warning. This is artificial demonstration data, not a benchmark.

## Sprint 1 — 60 seconds

| Time | Screen/action | Explanation |
|---|---|---|
| 0–10 s | Login and dashboard | Session authentication and private financial overview |
| 10–20 s | Categories | Income and expense categories owned by the signed-in user |
| 20–35 s | Add an expense of 100 dated 2026-10-20 in Food | Required fields, positive Decimal amount and server validation |
| 35–45 s | Edit 100 to 120, then delete that demo record | Owner-only CRUD; totals recalculate |
| 45–55 s | Dashboard and budgets | Income 30000, expenses 850, balance 29150 after deletion; Food warning at 85% |
| 55–60 s | Repository PR/CI page | Show actual state; do not claim green CI before a successful run |

## Sprint 2 — 120 seconds

| Time | Screen/action | Explanation |
|---|---|---|
| 0–15 s | Dashboard and October budget | Integrated current totals and threshold warning |
| 15–35 s | Add Food expense 200 in October | Spending 1050 exceeds 1000; visible exceeded alert |
| 35–55 s | Transaction filters | Filter October, expense, Food; search description |
| 55–80 s | Reports | Generate October summary and a custom range; compare category/month totals |
| 80–95 s | CSV download | Open downloaded CSV and compare records/totals; no other user's data |
| 95–110 s | Separate admin account | User management and timestamped audit log; standard account cannot access admin |
| 110–120 s | Documentation and freeze checklist | Show actual validation and remaining deviations, or approved freeze tag if gates passed |

For the admin segment create a local superuser using `python manage.py createsuperuser`. Do not show its password. Record on a clean dataset or adjust narration to the actual visible totals. A video showing only slides does not meet the working-product requirement.
