# Deviation and blocker log

Recorded during Part 2 recovery on 30 October 2026. Approval status: all entries require team/owner review.

| ID | Baseline or expectation | Observed implementation/evidence | Resolution or acceptance needed |
|---|---|---|---|
| D01 | Sprint work completed on scheduled dates | Main had no app; scaffold PR open; backlog created on 30 October | Preserve actual dates; disclose late recovery; seek faculty guidance if required |
| D02 | Assigned member opens PR and owner reviews | Only PR #27 found; recovery uses Santosh's identity and AI assistance | Real member reviews/contributions and owner approval still needed |
| D03 | Submitted SAD followed | No submitted SAD found | Locate original; compare to as-built notes; do not label new notes as submitted SAD |
| D04 | Relational production DB PostgreSQL/MySQL | SQLite used for local automated execution; PostgreSQL CI/Compose configured | Execute PostgreSQL CI and restart validation |
| D05 | At least one portable export in SRS; CSV+PDF in backlog | CSV export implemented; PDF export absent | Accept CSV-only scope or implement/test PDF before closing US-18 |
| D06 | Suitable charts or summaries in SRS; charts in CSV | Category/month tables implemented | Accept summary tables or add charts before closing US-16 |
| D07 | Visible threshold alerts in SRS; email also in CSV | Current live budget warnings on dashboard/list; no sent email or alert history | Accept in-app-only alerts or implement/test email before closing US-14 |
| D08 | Jenkins and Sonar tooling named in guidelines/backlog | Actions lint/tests/Bandit/dependency audit configured; Jenkins pipeline unexecuted; external Sonar not configured | Owner/instructor must approve tool equivalence or provision services |
| D09 | Original two sprint demo recordings | No video found; recovery environment browser download failed | Record working app locally now, label actual date and upload; no fabricated historical video |
| D10 | Freeze after completion | Unresolved process, live CI, NFR and recording gates | Keep release unfrozen until gates close |
| D11 | FND-02 ownership consistent | Shared plan, CSV and live issue disagree | Team confirms ownership without overwriting attribution |
| D12 | NFR and security acceptance executed fully | Automated application checks available; no production deployment, load, browser/UAT or restart evidence | Execute checks and retain actual results before acceptance |

Manual Part 3 test sheets are intentionally not filled with invented results.
