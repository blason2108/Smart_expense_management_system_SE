# As-built architecture

These are recovery architecture notes, not the missing originally submitted SAD.

Django handles server-rendered HTML with session authentication, CSRF middleware, form validation and ORM persistence. PostgreSQL is the deployment database; SQLite is a supported local demonstration/test option. Nine original app directories are preserved; `alerts` and `adminpanel` do not contain separate business implementations. Visible alerts are calculated by Budget and displayed in dashboard/budget templates. Administrative management uses Django admin.

| Layer | Implementation |
|---|---|
| Presentation | Escaped Django templates; semantic forms; responsive CSS; navigation |
| Authentication | Custom User; UserCreationForm validators; LoginView/POST-only LogoutView |
| Authorization | Login decorators; every query/create/update/delete scoped to request.user; category choices scoped in forms |
| Transactions | Positive Decimal money; date fields; protected category FK; model/form validation; DB positivity constraint |
| Budgets | Positive limit; inclusive date range; expense-only category; live aggregate so edits/deletions recalculate |
| Analysis/reporting | Shared selected_transactions and totals services; month/date/category/type/text filters; aggregate tables; CSV export |
| Audit | Auth signal events and admin mutation events; timestamp/actor/event only; read-only admin view |
| Operations | Env settings; opt-in production HTTPS; Docker Compose; root Actions workflow |

## Important boundaries

Users choose a category before recording a transaction. Category deletion is rejected while referenced by a transaction or budget. Category type changes are rejected if they would invalidate existing records. Budget warnings are current state, not historical notifications. Reports always derive from the authenticated user's records, including exports. Untrusted text is template-escaped; CSV formula-prefixed text is neutralized on export.

Views use validated forms. Direct ORM writes remain trusted application code; they must call model validation when introducing new paths. Database constraints enforce positive monetary values, budget date ordering, warning threshold bounds and uniqueness. A future API must use the same ownership and validation rules.

No external banking connection, payments or prediction model is included.
