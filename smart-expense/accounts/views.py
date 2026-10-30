from django.contrib.auth import login
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save()
        except IntegrityError:
            form.add_error(None, "Account already exists. Use a different username or email.")
        else:
            login(request, user)
            return redirect("dashboard:home")
    return render(request, "form.html", {"form": form, "title": "Create account"})
