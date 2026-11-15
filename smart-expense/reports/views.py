import csv

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render

from transactions.forms import FilterForm
from transactions.services import selected_transactions, totals

from .pdf import build_pdf


def safe_cell(value):
    text = str(value)
    needs_escape = text.startswith(("\t", "\r", "\n")) or text.lstrip().startswith(("=", "+", "-", "@"))
    return "'" + text if needs_escape else text


def expense_shares(groups):
    rows = list(groups)
    total = sum(row["total"] for row in rows)
    for row in rows:
        row["share"] = 100 * row["total"] / total
    return rows


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
    by_category = expenses.values("category__name").annotate(total=Sum("amount")).order_by("category__name")
    by_month = (
        expenses.annotate(month=TruncMonth("date")).values("month").annotate(total=Sum("amount")).order_by("month")
    )
    return render(
        request,
        "reports/list.html",
        {
            "form": form,
            "items": qs,
            "by_category": expense_shares(by_category),
            "by_month": expense_shares(by_month),
            **summary,
        },
    )
