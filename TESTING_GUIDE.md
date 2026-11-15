# Testing Guide

## Purpose
This guide describes the main testing activities for the Smart Expense & Budget Management project.

## Testing Levels

### Unit Testing
Test individual functions, services, and model behavior independently.

### Integration Testing
Verify interactions between views, services, models, and the database.

### Functional Testing
Verify important user workflows, including:

- Creating and viewing transactions.
- Managing expense categories.
- Creating and reviewing budgets.
- Generating reports.
- Exporting reports as CSV and PDF.

## Test Execution

Run the Django system check:

    python manage.py check

Run the automated test suite:

    python -m pytest

Run static analysis:

    python -m ruff check .

## Test Quality

- Include normal, boundary, and invalid-input scenarios.
- Keep tests independent and repeatable.
- Use test data rather than real financial information.
- Investigate failures before considering a change complete.
