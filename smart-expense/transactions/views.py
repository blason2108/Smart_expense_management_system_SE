from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FilterForm, TransactionForm
from .models import Transaction
from .services import selected_transactions, totals


@login_required
def index(request):
    form = FilterForm(request.GET, user=request.user)
    qs = selected_transactions(request.user, form)
    return render(request, "transactions/list.html", {"form": form, "items": qs, **totals(qs)})


@login_required
def edit(request, pk=None):
    item = get_object_or_404(Transaction, pk=pk, owner=request.user) if pk else None
    form = TransactionForm(request.POST or None, instance=item, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("transactions:list")
    return render(request, "form.html", {"form": form, "title": "Edit transaction" if pk else "New transaction"})


@login_required
def delete(request, pk):
    item = get_object_or_404(Transaction, pk=pk, owner=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("transactions:list")
    return render(request, "confirm.html", {"title": "Delete transaction", "item": f"{item.date}: {item.amount}"})
