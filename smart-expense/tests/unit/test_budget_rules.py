from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from budgets.models import Budget
from categories.models import Category


@pytest.mark.parametrize(
    "spent,percentage,status",
    [
        ("0", "0", "On track"),
        ("799.99", "79.999", "On track"),
        ("800", "80", "Warning"),
        ("1000", "100", "Warning"),
        ("1000.01", "100.001", "Exceeded"),
    ],
)
def test_budget_progress_and_status(monkeypatch, spent, percentage, status):
    budget = Budget(limit=Decimal("1000"), threshold=80)
    monkeypatch.setattr(Budget, "spent", property(lambda self: Decimal(spent)))

    assert budget.progress == Decimal(percentage)
    assert budget.status == status


@pytest.mark.parametrize("category_owner,kind", [(2, Category.EXPENSE), (1, Category.INCOME)])
def test_budget_requires_an_owned_expense_category(category_owner, kind):
    category = Category(pk=1, owner_id=category_owner, kind=kind)
    budget = Budget(owner_id=1, category=category)

    with pytest.raises(ValidationError) as error:
        budget.clean()

    assert "category" in error.value.message_dict


def test_budget_rejects_an_end_before_its_start():
    budget = Budget(start_date=date(2026, 10, 2), end_date=date(2026, 10, 1))

    with pytest.raises(ValidationError) as error:
        budget.clean()

    assert "end_date" in error.value.message_dict
