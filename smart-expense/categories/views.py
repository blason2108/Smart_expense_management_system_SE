from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm
from .models import Category


@login_required
def index(request):
    return render(request, "categories/list.html", {"items": Category.objects.filter(owner=request.user)})


@login_required
def edit(request, pk=None):
    item = get_object_or_404(Category, pk=pk, owner=request.user) if pk else Category(owner=request.user)
    form = CategoryForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            form.add_error("name", "This category already exists.")
        else:
            return redirect("categories:list")
    return render(request, "form.html", {"form": form, "title": "Edit category" if pk else "New category"})


@login_required
def delete(request, pk):
    item = get_object_or_404(Category, pk=pk, owner=request.user)
    if request.method == "POST":
        try:
            item.delete()
        except ProtectedError:
            messages.error(request, "This category is used by a transaction or budget. Remove those records first.")
        return redirect("categories:list")
    return render(request, "confirm.html", {"title": "Delete category", "item": item})
