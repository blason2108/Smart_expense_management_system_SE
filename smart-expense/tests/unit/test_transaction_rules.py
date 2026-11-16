from datetime import date

import pytest
from django.core.exceptions import ValidationError

from accounts.models import User
from categories.models import Category
from transactions.forms import FilterForm
from transactions.models import Transaction


def test_transaction_accepts_a_matching_category():
    category = Category(pk=1, owner_id=1, kind=Category.EXPENSE)
    Transaction(owner_id=1, category=category, kind=Category.EXPENSE).clean()


@pytest.mark.parametrize(
    "category_owner,transaction_kind,expected",
    [
        (2, Category.EXPENSE, "Choose your own category."),
        (1, Category.INCOME, "Category type must match transaction type."),
    ],
)
def test_transaction_rejects_an_invalid_category(category_owner, transaction_kind, expected):
    category = Category(pk=1, owner_id=category_owner, kind=Category.EXPENSE)
    transaction = Transaction(owner_id=1, category=category, kind=transaction_kind)

    with pytest.raises(ValidationError) as error:
        transaction.clean()

    assert error.value.message_dict == {"category": [expected]}


def test_filter_accepts_an_inclusive_single_day():
    form = FilterForm({"start": "2026-10-01", "end": "2026-10-01"}, user=User(pk=1))

    assert form.is_valid(), form.errors
    assert form.cleaned_data["start"] == form.cleaned_data["end"] == date(2026, 10, 1)


def test_filter_rejects_a_reversed_range():
    form = FilterForm({"start": "2026-10-02", "end": "2026-10-01"}, user=User(pk=1))

    assert not form.is_valid()
    assert form.non_field_errors() == ["Start date must be on or before end date."]


def test_filter_parses_a_report_month():
    form = FilterForm({"month": "2026-10"}, user=User(pk=1))

    assert form.is_valid(), form.errors
    assert form.cleaned_data["month"] == date(2026, 10, 1)
