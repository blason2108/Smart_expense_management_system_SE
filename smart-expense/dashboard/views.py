from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from budgets.models import Budget
from transactions.models import Transaction
from transactions.services import totals


def health(request):
    return JsonResponse({"status": "ok"})


@login_required
def home(request):
    qs = Transaction.objects.filter(owner=request.user).select_related("category")
    return render(
        request,
        "dashboard/home.html",
        {
            **totals(qs),
            "recent": qs[:10],
            "budgets": Budget.objects.filter(owner=request.user).select_related("category"),
        },
    )
