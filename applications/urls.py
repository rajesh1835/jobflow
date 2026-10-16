from django.urls import path

from . import views

app_name = "applications"

urlpatterns = [
    path("", views.application_list, name="list"),
    path("<uuid:pk>/delete/", views.application_delete, name="delete"),
]
