import csv
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render

from budgets.models import Budget
from transactions.forms import FilterForm
from transactions.services import selected_transactions, totals

from .pdf import build_pdf


def safe_cell(value):
    text = str(value)
    needs_escape = text.startswith(("\t", "\r", "\n")) or text.lstrip().startswith(("=", "+", "-", "@"))
    return "'" + text if needs_escape else text


def expense_scale(peak):
    magnitude = Decimal(10) ** peak.adjusted()
    return next(magnitude * step for step in (1, 2, 5, 10) if magnitude * step >= peak)


def budgets_with_report_spend(user, expenses):
    matched = (
        expenses.filter(category_id=OuterRef("category_id"), date__range=(OuterRef("start_date"), OuterRef("end_date")))
        .values("category_id")
        .annotate(total=Sum("amount"))
        .values("total")
    )
    budgets = list(
        Budget.objects.filter(owner=user)
        .select_related("category")
        .annotate(report_spent=Subquery(matched))
        .filter(report_spent__isnull=False)
    )
    for budget in budgets:
        budget.report_usage = budget.report_spent / budget.limit * 100
    return budgets


@login_required
def index(request):
    form = FilterForm(request.GET, user=request.user)
    qs = selected_transactions(request.user, form)
    summary = totals(qs)
    if request.GET.get("export") == "pdf" and form.is_valid():
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="expense-report.pdf"'
        build_pdf(response, qs, summary)
        return response

    if request.GET.get("export") == "csv" and form.is_valid():
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="expense-report.csv"'
        writer = csv.writer(response)
        writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
        for row in qs:
            writer.writerow(
                [row.date.isoformat(), row.kind, safe_cell(row.category.name), row.amount, safe_cell(row.description)]
            )
        writer.writerow([])
        for key, value in summary.items():
            writer.writerow([key, value])
        return response
    expenses = qs.filter(kind="expense").order_by()
    by_category = list(expenses.values("category__name").annotate(total=Sum("amount")).order_by("category__name"))
    by_month = list(
        expenses.annotate(month=TruncMonth("date")).values("month").annotate(total=Sum("amount")).order_by("month")
    )
    peak = max((row["total"] for row in by_category + by_month), default=Decimal("1"))
    return render(
        request,
        "reports/list.html",
        {
            "form": form,
            "items": qs,
            "by_category": by_category,
            "by_month": by_month,
            "expense_scale": expense_scale(peak),
            "report_budgets": budgets_with_report_spend(request.user, expenses),
            **summary,
        },
    )
