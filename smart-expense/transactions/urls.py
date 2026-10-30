from django.urls import path

from . import views

app_name = "transactions"
urlpatterns = [
    path("", views.index, name="list"),
    path("new/", views.edit, name="new"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]
