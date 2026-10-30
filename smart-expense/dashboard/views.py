from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


def health(request):
    """Unauthenticated liveness probe for Docker/CI smoke tests."""
    return JsonResponse({"status": "ok"})


@login_required
def home(request):
    return render(request, "dashboard/home.html")
