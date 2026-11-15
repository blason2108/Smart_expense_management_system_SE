import csv
import io

import pytest
from pypdf import PdfReader

from budgets.models import Budget
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
    assert r.context["by_category"] == [{"category__name": "Food", "total": 100}]
    assert len(r.context["by_month"]) == 1
    r = auth.get("/reports/", {"month": "2026-10", "export": "csv"})
    assert r["Content-Type"].startswith("text/csv")
    rows = list(csv.reader(io.StringIO(r.content.decode())))
    assert len(rows) == 7
    assert "Secret" not in r.content.decode() and "Dinner" not in r.content.decode()


def test_report_charts_and_month_control(auth, records):
    response = auth.get("/reports/", {"month": "2026-10"})
    assert b'value="2026-10"' in response.content
    assert response.content.count(b"<meter ") == 2
    assert response.content.count(b'<meter min="0" max="100.00" value="100.00"') == 2
    assert b"Lunch" in response.content and b"Dinner" not in response.content


def test_report_charts_use_a_common_inr_scale(auth, records, user):
    travel = Category.objects.create(owner=user, name="Travel", kind="expense")
    Transaction.objects.create(owner=user, category=travel, kind="expense", date="2026-11-01", amount=100)

    response = auth.get("/reports/")
    assert response.context["expense_scale"] == 500
    assert response.content.count(b'<meter min="0" max="500.00" value="300.00"') == 2
    assert response.content.count(b'<meter min="0" max="500.00" value="100.00"') == 2

    response = auth.get("/reports/", {"category": travel.pk})
    assert response.content.count(b'<meter min="0" max="100.00" value="100.00"') == 2
    response = auth.get("/reports/", {"kind": "income"})
    assert b"<meter " not in response.content
    assert response.content.count(b"No expenses.") == 2


def test_report_budget_usage_matches_the_budget_and_report_dates(auth, records, user, other, category):
    budget = Budget.objects.create(
        owner=user, category=category, start_date="2026-10-01", end_date="2026-10-31", limit=1000
    )
    Budget.objects.create(
        owner=other, category=Category.objects.get(owner=other), start_date="2026-10-01", end_date="2026-10-31",
        limit=1000,
    )
    Transaction.objects.create(
        owner=user, category=category, kind="expense", date="2026-10-31", amount=750, description="Groceries"
    )

    response = auth.get("/reports/")
    assert response.context["expense"] == 1050
    assert response.context["report_budgets"] == [budget]
    assert response.context["report_budgets"][0].report_usage == 85
    assert response.content.count(b'<meter min="0" max="2000.00"') == 3
    assert b'value="85.0000"' in response.content

    response = auth.get("/reports/", {"month": "2026-10"})
    assert response.context["expense_scale"] == 1000
    assert response.content.count(b'<meter min="0" max="1000.00" value="850.00"') == 2
    assert "₹850.00 / ₹1,000.00" in response.content.decode()
    assert auth.get("/reports/", {"q": "Groceries"}).context["report_budgets"][0].report_usage == 75
    assert auth.get("/reports/", {"month": "2026-11"}).context["report_budgets"] == []


def test_custom_range_and_pdf_export(auth, records):
    period = {"start": "2026-10-20", "end": "2026-11-01"}
    report = auth.get("/reports/", period)
    assert report.context["income"] == 0
    assert report.context["expense"] == 300
    assert report.context["balance"] == -300
    assert [row["total"] for row in report.context["by_month"]] == [100, 200]

    response = auth.get("/reports/", {**period, "export": "pdf"})
    assert response["Content-Type"] == "application/pdf"
    assert response["Content-Disposition"] == 'attachment; filename="expense-report.pdf"'
    text = PdfReader(io.BytesIO(response.content)).pages[0].extract_text()
    assert "Lunch" in text and "Dinner" in text
    assert "Expenses: 300.00 INR" in text and "Balance: -300.00 INR" in text
    assert "Secret" not in text and "Salary" not in text


def test_pdf_wraps_literal_text_and_empty_reports(auth, user, category):
    Transaction.objects.create(
        owner=user, category=category, kind="expense", date="2026-10-20", amount=1, description="<note> & details"
    )
    response = auth.get("/reports/", {"month": "2026-10", "export": "pdf"})
    assert "<note> & details" in PdfReader(io.BytesIO(response.content)).pages[0].extract_text()
    response = auth.get("/reports/", {"month": "2026-12", "export": "pdf"})
    assert "No transactions match." in PdfReader(io.BytesIO(response.content)).pages[0].extract_text()


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


@pytest.mark.parametrize("export", ["csv", "pdf"])
def test_invalid_export_is_form(auth, export):
    assert auth.get("/reports/", {"month": "invalid", "export": export})["Content-Type"].startswith("text/html")


def test_dashboard_isolation(auth, records):
    r = auth.get("/")
    assert r.context["income"] == 1000 and r.context["expense"] == 300 and r.context["balance"] == 700
    assert b"Secret" not in r.content
