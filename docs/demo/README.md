# Demo recording instructions

Both recordings must show the working application. Record now with the actual date; do not imply the recovered build was recorded in the original sprint week. Videos are not present yet. Use your OS screen recorder or OBS, then commit `docs/demo/sprint-1.mp4` and `docs/demo/sprint-2.mp4` through a reviewed PR. Keep private accounts and secrets off screen.

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
