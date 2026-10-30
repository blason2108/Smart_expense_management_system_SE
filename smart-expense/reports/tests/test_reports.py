import csv
import io

import pytest

from categories.models import Category
from transactions.models import Transaction

pytestmark = pytest.mark.django_db


@pytest.fixture
def records(user, other, category):
    private = Category.objects.create(owner=other, name="Private", kind="expense")
    income = Category.objects.create(owner=user, name="Salary", kind="income")
    for owner, c, amount, day, desc in [
        (user, category, 100, "2026-10-20", "Lunch"),
        (user, category, 200, "2026-11-01", "Dinner"),
        (user, income, 1000, "2026-10-01", "Salary"),
        (other, private, 999, "2026-10-20", "Secret"),
    ]:
        Transaction.objects.create(owner=owner, category=c, kind=c.kind, amount=amount, date=day, description=desc)


@pytest.mark.parametrize(
    "params,count",
    [
        ({}, 3),
        ({"month": "2026-10"}, 2),
        ({"start": "2026-10-20", "end": "2026-10-20"}, 1),
        ({"kind": "income"}, 1),
        ({"q": "dinner"}, 1),
        ({"month": "invalid"}, 0),
        ({"start": "2026-11-01", "end": "2026-10-01"}, 0),
    ],
)
def test_search(auth, records, params, count):
    assert auth.get("/transactions/", params).context["items"].count() == count


def test_category_filter(auth, records, category):
    r = auth.get("/transactions/", {"category": category.pk})
    assert r.context["items"].count() == 2


def test_private_filter_rejected(auth, records):
    private = Category.objects.get(name="Private")
    assert auth.get("/reports/", {"category": private.pk}).context["items"].count() == 0


def test_report_summary_and_export(auth, records):
    r = auth.get("/reports/", {"month": "2026-10"})
    assert r.context["income"] == 1000 and r.context["expense"] == 100 and r.context["balance"] == 900
    assert list(r.context["by_category"]) == [{"category__name": "Food", "total": 100}]
    assert len(r.context["by_month"]) == 1
    r = auth.get("/reports/", {"month": "2026-10", "export": "csv"})
    assert r["Content-Type"].startswith("text/csv")
    rows = list(csv.reader(io.StringIO(r.content.decode())))
    assert len(rows) == 7
    assert "Secret" not in r.content.decode() and "Dinner" not in r.content.decode()


def test_csv_formula_escape(auth, user, category):
    Transaction.objects.create(
        owner=user,
        category=category,
        kind="expense",
        date="2026-10-20",
        amount=1,
        description='=HYPERLINK("https://example.test")',
    )
    rows = list(csv.reader(io.StringIO(auth.get("/reports/", {"export": "csv"}).content.decode())))
    assert rows[1][-1].startswith("'=")


def test_invalid_export_is_form(auth):
    assert auth.get("/reports/", {"month": "invalid", "export": "csv"})["Content-Type"].startswith("text/html")


def test_dashboard_isolation(auth, records):
    r = auth.get("/")
    assert r.context["income"] == 1000 and r.context["expense"] == 300 and r.context["balance"] == 700
    assert b"Secret" not in r.content
