import calendar
from decimal import Decimal

from django.db.models import Sum

from .models import Transaction


def selected_transactions(user, form):
    qs = Transaction.objects.filter(owner=user).select_related("category")
    if not form.is_valid():
        return qs.none()
    data = form.cleaned_data
    if data.get("month"):
        d = data["month"]
        qs = qs.filter(date__range=(d.replace(day=1), d.replace(day=calendar.monthrange(d.year, d.month)[1])))
    for field, lookup in [("start", "date__gte"), ("end", "date__lte"), ("category", "category"), ("kind", "kind")]:
        if data.get(field):
            qs = qs.filter(**{lookup: data[field]})
    if data.get("q"):
        qs = qs.filter(description__icontains=data["q"])
    return qs


def totals(qs):
    sums = {r["kind"]: r["total"] for r in qs.order_by().values("kind").annotate(total=Sum("amount"))}
    income, expense = sums.get("income", Decimal("0.00")), sums.get("expense", Decimal("0.00"))
    return {"income": income, "expense": expense, "balance": income - expense}
