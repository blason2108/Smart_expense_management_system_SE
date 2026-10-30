from decimal import Decimal

import pytest

from budgets.models import Budget
from categories.models import Category
from transactions.models import Transaction

pytestmark = pytest.mark.django_db


def budget_data(c, **changes):
    d = {"category": c.pk, "start_date": "2026-10-01", "end_date": "2026-10-31", "limit": "1000", "threshold": 80}
    d.update(changes)
    return d


@pytest.mark.parametrize(
    "change",
    [
        {"limit": "0"},
        {"limit": "-10"},
        {"threshold": 0},
        {"threshold": 101},
        {"end_date": "2026-09-30"},
        {"start_date": "invalid"},
        {"category": ""},
    ],
)
def test_invalid_budget(auth, category, change):
    assert auth.post("/budgets/new/", budget_data(category, **change)).status_code == 200
    assert not Budget.objects.exists()


def test_income_budget_denied(auth, user):
    c = Category.objects.create(owner=user, name="Salary", kind="income")
    assert auth.post("/budgets/new/", budget_data(c)).status_code == 200


def test_budget_lifecycle(auth, user, category):
    assert auth.post("/budgets/new/", budget_data(category)).status_code == 302
    b = Budget.objects.get()
    assert b.spent == 0 and b.status == "On track"
    t = Transaction.objects.create(owner=user, category=category, kind="expense", date="2026-10-20", amount="800")
    assert b.status == "Warning" and b.progress == Decimal("80")
    assert b"Warning" in auth.get("/").content
    t.amount = Decimal("1001")
    t.save()
    assert b.status == "Exceeded"
    assert b"Exceeded" in auth.get("/budgets/").content
    t.date = "2026-11-01"
    t.save()
    assert b.spent == 0
    t.date = "2026-10-01"
    t.amount = Decimal("500")
    t.save()
    assert b.spent == 500
    t.delete()
    assert b.spent == 0
    assert auth.get(f"/budgets/{b.pk}/edit/").status_code == 200
    assert auth.post(f"/budgets/{b.pk}/edit/", budget_data(category, limit="2000")).status_code == 302
    b.refresh_from_db()
    assert b.limit == 2000
    assert auth.get(f"/budgets/{b.pk}/delete/").status_code == 200
    assert auth.post(f"/budgets/{b.pk}/delete/").status_code == 302
    assert not Budget.objects.exists()


def test_budget_preserves_category_type(auth, user, category):
    auth.post("/budgets/new/", budget_data(category))
    assert auth.post(f"/categories/{category.pk}/edit/", {"name": "Food", "kind": "income"}).status_code == 200


def test_other_users_expenses_not_counted(auth, user, other, category):
    b = Budget.objects.create(owner=user, category=category, start_date="2026-10-01", end_date="2026-10-31", limit=1000)
    private = Category.objects.create(owner=other, name="Food", kind="expense")
    Transaction.objects.create(owner=other, category=private, kind="expense", amount=900, date="2026-10-20")
    assert b.spent == 0
