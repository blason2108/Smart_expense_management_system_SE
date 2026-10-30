from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("categories/", include("categories.urls")),
    path("transactions/", include("transactions.urls")),
    path("budgets/", include("budgets.urls")),
    path("reports/", include("reports.urls")),
    path("django-admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
]
