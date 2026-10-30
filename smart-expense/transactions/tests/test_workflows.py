from datetime import date
from decimal import Decimal

import pytest
from django.db import IntegrityError, transaction

from budgets.models import Budget
from categories.models import Category
from transactions.models import Transaction

pytestmark = pytest.mark.django_db


def payload(cat, **changes):
    result = {
        "category": cat.pk,
        "kind": cat.kind,
        "amount": "125.50",
        "date": "2026-10-20",
        "description": "Lunch",
    }
    result.update(changes)
    return result


def make_transaction(user, category, amount="125.50", when=date(2026, 10, 20)):
    return Transaction.objects.create(
        owner=user, category=category, kind=category.kind, amount=amount, date=when, description="Lunch"
    )


def test_category_crud(auth, user):
    assert auth.post("/categories/new/", {"name": "Food", "kind": "expense"}).status_code == 302
    cat = Category.objects.get(owner=user)
    assert auth.get("/categories/").status_code == 200
    assert auth.get(f"/categories/{cat.pk}/edit/").status_code == 200
    auth.post(f"/categories/{cat.pk}/edit/", {"name": "Groceries", "kind": "expense"})
    cat.refresh_from_db()
    assert cat.name == "Groceries"
    assert auth.get(f"/categories/{cat.pk}/delete/").status_code == 200
    auth.post(f"/categories/{cat.pk}/delete/")
    assert not Category.objects.exists()


@pytest.mark.parametrize("data", [{"name": "", "kind": "expense"}, {"name": "X", "kind": "bad"}])
def test_invalid_category(auth, data):
    assert auth.post("/categories/new/", data).status_code == 200
    assert not Category.objects.exists()


def test_duplicate_category(auth, category):
    assert auth.post("/categories/new/", {"name": "FOOD", "kind": "expense"}).status_code == 200
    assert Category.objects.count() == 1


@pytest.mark.parametrize("kind", ["income", "expense"])
def test_create_transaction(auth, user, kind):
    c = Category.objects.create(owner=user, name="Test", kind=kind)
    assert auth.post("/transactions/new/", payload(c)).status_code == 302
    t = Transaction.objects.get()
    assert t.owner == user and t.amount == Decimal("125.50")
    assert auth.get("/transactions/").status_code == 200
    r = auth.get("/")
    assert r.context[kind] == Decimal("125.50")


@pytest.mark.parametrize(
    "changes",
    [
        {"amount": "0"},
        {"amount": "-1"},
        {"amount": "NaN"},
        {"amount": "1.001"},
        {"amount": "999999999999999"},
        {"date": "not-date"},
        {"date": "2026-02-30"},
        {"category": ""},
        {"kind": "income"},
        {"amount": ""},
        {"description": "x" * 251},
    ],
)
def test_reject_invalid_transactions(auth, category, changes):
    assert auth.post("/transactions/new/", payload(category, **changes)).status_code == 200
    assert not Transaction.objects.exists()


def test_foreign_category_rejected(auth, other):
    c = Category.objects.create(owner=other, name="Private", kind="expense")
    assert auth.post("/transactions/new/", payload(c)).status_code == 200
    assert not Transaction.objects.exists()


@pytest.mark.parametrize("app", ["categories", "transactions", "budgets"])
@pytest.mark.parametrize("action", ["edit", "delete"])
def test_foreign_object_denied(auth, other, app, action):
    c = Category.objects.create(owner=other, name="Private", kind="expense")
    b = Budget.objects.create(owner=other, category=c, start_date="2026-10-01", end_date="2026-10-31", limit="500")
    t = make_transaction(other, c)
    pk = {"categories": c.pk, "transactions": t.pk, "budgets": b.pk}[app]
    url = f"/{app}/{pk}/{action}/"
    assert auth.get(url).status_code == 404
    assert auth.post(url, {}).status_code == 404


def test_edit_delete_transaction(auth, user, category):
    t = make_transaction(user, category)
    url = f"/transactions/{t.pk}"
    assert auth.get(url + "/edit/").status_code == 200
    assert auth.post(url + "/edit/", payload(category, amount="25.00")).status_code == 302
    assert auth.get("/").context["expense"] == Decimal("25")
    assert auth.get(url + "/delete/").status_code == 200
    assert Transaction.objects.filter(pk=t.pk).exists()
    assert auth.post(url + "/delete/").status_code == 302
    assert auth.get("/").context["expense"] == 0


def test_protected_category(auth, user, category):
    make_transaction(user, category)
    auth.post(f"/categories/{category.pk}/delete/")
    assert Category.objects.filter(pk=category.pk).exists()
    assert auth.post(f"/categories/{category.pk}/edit/", {"name": "Food", "kind": "income"}).status_code == 200
    category.refresh_from_db()
    assert category.kind == "expense"


def test_negative_database_constraint(user, category):
    with pytest.raises(IntegrityError), transaction.atomic():
        make_transaction(user, category, "-1")


def test_escaped_description(auth, user, category):
    evil = "<script>alert(1)</script>"
    auth.post("/transactions/new/", payload(category, description=evil))
    page = auth.get("/transactions/").content.decode()
    assert evil not in page and "&lt;script&gt;" in page
    assert auth.get("/transactions/", {"q": "' OR 1=1 --"}).context["items"].count() == 0


def test_new_forms(auth):
    for path in ["/categories/new/", "/transactions/new/", "/budgets/new/"]:
        assert auth.get(path).status_code == 200
