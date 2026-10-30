from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BudgetForm
from .models import Budget


@login_required
def index(request):
    return render(
        request, "budgets/list.html", {"items": Budget.objects.filter(owner=request.user).select_related("category")}
    )


@login_required
def edit(request, pk=None):
    item = get_object_or_404(Budget, pk=pk, owner=request.user) if pk else None
    form = BudgetForm(request.POST or None, instance=item, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("budgets:list")
    return render(request, "form.html", {"form": form, "title": "Edit budget" if pk else "New budget"})


@login_required
def delete(request, pk):
    item = get_object_or_404(Budget, pk=pk, owner=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("budgets:list")
    return render(request, "confirm.html", {"title": "Delete budget", "item": item.category})
