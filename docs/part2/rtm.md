# Requirement traceability

Source: original SRS Section 8 and Test Plan Sections 6–8. Paths below are relative to `smart-expense/`. Automated checks do not replace manual acceptance or owner sign-off.

| Requirement | Feature | Code | Baseline test | Current evidence/status |
|---|---|---|---|---|
| SEB-F-001 | Registration | accounts/forms.py; accounts/views.py | TC-AUTH-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-002 | Login/logout | accounts/urls.py | TC-AUTH-02 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-003 | Password hashing | config/settings.py | TC-SEC-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-004 | Income | transactions/views.py | TC-TXN-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-005 | Expense | transactions/views.py | TC-TXN-02 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-006 | Transaction edits/deletes | transactions/views.py | TC-TXN-03 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-007 | Category CRUD | categories/views.py | TC-CAT-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-008 | Budget creation | budgets/forms.py; budgets/models.py | TC-BUD-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-009 | Budget monitoring | budgets/models.py | TC-BUD-02 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-010 | Visible budget alerts | budgets/models.py; templates/dashboard/home.html | TC-ALT-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-011 | Dashboard | dashboard/views.py | TC-DASH-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-012 | Analysis summaries | reports/views.py | TC-ANL-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-013 | Search/filter | transactions/services.py | TC-SRCH-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-014 | Reports | reports/views.py | TC-RPT-01 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-015 | CSV export | reports/views.py | TC-RPT-02 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-016 | Isolation | owner-scoped views/forms in all data apps | TC-SEC-02 | Implemented; local automated regression passed; owner acceptance pending |
| SEB-F-017 | Admin users | accounts/admin.py | TC-ADM-01 | Implemented; auth/admin access automated checks passed; admin mutation manual acceptance pending |
| SEB-F-018 | Audit events | audit/signals.py; accounts/admin.py | TC-AUD-01 | Implemented; auth/admin access automated checks passed; admin mutation manual acceptance pending |
| SEB-NF-001 | Performance | Cross-cutting | TC-PERF-01 | Load execution pending |
| SEB-NF-002 | Reliability | Cross-cutting | TC-REL-01 | Restart execution pending |
| SEB-NF-003 | Usability | Cross-cutting | TC-UX-01 | Responsive forms provided; representative-user execution pending |
| SEB-NF-004 | Maintainability | Cross-cutting | TC-MNT-01 | Modular source documented; independent review pending |
| SEB-NF-005 | Compatibility | Cross-cutting | TC-COMP-01 | Chrome/Firefox execution pending |
| SEB-NF-006 | Data integrity | Cross-cutting | TC-DATA-01 | Form/DB constraints; local automated checks passed |
| SEB-SR-001 | HTTPS | Cross-cutting | TC-SEC-03 | Configured redirect/HSTS unit check passed; deployed TLS test pending |
| SEB-SR-002 | Hashing | Cross-cutting | TC-SEC-01 | Local automated check passed |
| SEB-SR-003 | Authorization | Cross-cutting | TC-SEC-02 | Local cross-user/admin tests passed |
| SEB-SR-004 | Input protection | Cross-cutting | TC-SEC-04 | Invalid-input, ORM search, template/CSV escaping checks passed |
| SEB-SR-005 | Log hygiene | Cross-cutting | TC-SEC-05 | Credentials omitted in auth event/log test; deployment inspection pending |
