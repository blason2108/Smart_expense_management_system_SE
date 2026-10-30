# Two sprint plan and recovery status

The sprint dates are the assignment dates, not a claim about when work was actually completed. The repository's original CSV is retained as the planning source; no dates, commit authors or past activity are fabricated.

## Sprint 1 — 19 to 23 October 2026

Goal: an authenticated user can privately record income/expenses and see correct balances and budgets.

Scope: FND-01–06, US-01–13, TST-01–04, DOC-01, DOC-02 and DOC-05. These correspond to existing issues #1–26. Owner mapping remains in `smart-expense/docs/backlog/backlog.csv` and live issues. The large original sprint commitment was not supported by completed evidence in main at audit time.

Exit evidence: reviewed merged PRs, passing Actions, runnable product, one-minute video, RTM and deviations. Recovery implementation is available for review; exit is not yet approved.

## Sprint 2 — 26 to 30 October 2026

Goal: integrated alerts, analysis, filtering, reports/export, admin/audit and validated release candidate.

Scope: US-14–21; SNR-01/JEN-01 tooling; NFT-01–04 validation; DOC-04 video/documentation/freeze. CSV-plus-PDF, email, chart styling and external quality/deployment tools are broader CSV commitments; documented SRS-compliant summaries, visible alerts and CSV are currently implemented. Review those differences explicitly.

Exit evidence: two-minute recording, green integrated CI, completed NFR checks, updated documents, owner-approved freeze. DOC-03 manual test expansion is deferred to Part 3 per the current request.

## Recovery tracking rules

Track pending, review and accepted states honestly. An automated test pass is not a replacement for owner approval, manual compatibility testing, original sprint recordings or each member's contribution. Do not close all issues just because the recovery branch implements several modules.
