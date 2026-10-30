import csv

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render

from transactions.forms import FilterForm
from transactions.services import selected_transactions, totals


def safe_cell(value):
    text = str(value)
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@", "\t", "\r")) else text


@login_required
def index(request):
    form = FilterForm(request.GET, user=request.user)
    qs = selected_transactions(request.user, form)
    summary = totals(qs)
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
        {"form": form, "items": qs, "by_category": by_category, "by_month": by_month, **summary},
    )
