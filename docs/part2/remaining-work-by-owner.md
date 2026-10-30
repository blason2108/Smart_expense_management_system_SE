# Part 2 remaining work by owner

State checked on 30 October 2026. The application baseline was implemented during the earlier whole-project recovery and merged through PR #30. Future implementation assistance is limited to Santosh's assigned issues. Existing merged changes and genuine author history are retained; no work is reassigned merely to make contributor names appear.

## Santosh's current issues

| Issue | Scope | Existing evidence | Remaining before acceptance |
|---|---|---|---|
| #11 / US-05 | Category CRUD | Model/forms/views and automated CRUD, duplicate and protected-delete tests; category-list screenshot | Verify permitted create/edit/delete flow and explain implementation; owner acceptance |
| #12 / US-06 | Income recording | Automated income test and user screenshot showing income 10000.00 INR | Confirm record/form behavior and owner acceptance |
| #13 / US-07 | Expense recording | Automated tests plus manual add-expense screenshot | Owner acceptance and link evidence to issue |
| #14 / US-08 | Edit/delete own transactions | Manual edit/delete screenshots and automated owner-scoped mutation tests | Owner acceptance |
| #21 / TST-02 | Category/transaction tests | 29 category/transaction workflow test cases in the executed initial suite | Retain final run evidence and explain cases; owner review |
| #34 / US-15 | Search/filter | Shared filtering service and automated date/category/type/text tests | Manual combined-filter check and owner acceptance |
| #44 / NFT-04 | Maintainability review | santosh-maintainability-review.md | Santosh verifies/explains review; independent/owner acceptance |

All seven were still open when inspected. Completion of a code path is distinct from final issue acceptance. No teammate's issue should be closed by this handoff.

## Team-owned remaining gates

| Responsible owner | Work requiring their own verification/contribution |
|---|---|
| Bhuvigna | Board/protection process; authentication/isolation/security acceptance; admin/audit/input-validation checks; deviation log and requirement traceability |
| Blason | Database/seed/budget/validation acceptance; performance and restart measurements; alerts/email scope or approved deviation; deployment tooling; recording coordination; final owner reviews and freeze |
| Vishnu | CI/UI/dashboard/reporting/analytics acceptance; PDF/chart scope or approved deviations; static-analysis tooling; Chrome/Firefox and usability checks |

The current open FND-04 PR #47 is authored by Bhuvigna although the issue is assigned to Vishnu. Preserve that fact. Vishnu needs an actual contribution under his own identity; changing a label or crediting someone else's commit is insufficient.

## Whole-team checklist still pending

- A Project under blason2108 must be natively linked; Santosh's populated personal Project contains the 41 issues but cannot satisfy that native link.
- Review/merge valid pending PRs and run CI on final main.
- Verify each member's substantive implementation contribution and understanding.
- Complete pending report/export, isolation, administrator/audit and NFR acceptance with actual evidence.
- Locate the originally submitted SAD and reconcile documented deviations.
- Record and upload a real one-minute Sprint 1 flow and two-minute integrated Sprint 2 flow using the actual recording dates.
- Approve final documentation and only then freeze the exact accepted commit.

The accidental automated merge identity correction is separately owner-approved maintenance. It must preserve every file tree, other contributors' identities and the AI assistance log. It does not replace an implementation contribution or justify marking unexecuted tests as passed.
