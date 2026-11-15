# Santosh's local verification

- Date: 15 November 2026
- Tested commit from PR #54: be18d8f6a314d05a208db152e27cf4bed2567a1e
- PostgreSQL: 92 tests passed with 97.59% coverage.
- #42 Restart: October CSV data and the authenticated session survived an app process restart.
- #41 Load: 10 simulated users for 30 seconds, 289 requests, zero failures.
  Dashboard p90 was 47 ms and filtered transactions p90 was 40 ms.
- #43 Browser compatibility: Brave and Firefox both passed the automated checks
  for authentication, transactions, budgets, dashboard, CSV and PDF.
- #43 Manual usability walkthrough: A representative user added an expense
  and created a budget successfully. When they entered a threshold of 101,
  the app showed a validation message and prevented the budget from being saved.
