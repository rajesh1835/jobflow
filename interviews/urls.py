from django.urls import path

from . import views

app_name = "interviews"

urlpatterns = [
    path("", views.interview_list, name="list"),
    path("create/", views.interview_create, name="create"),
    path("<uuid:pk>/", views.interview_detail, name="detail"),
    path("<uuid:pk>/edit/", views.interview_update, name="update"),
    path("<uuid:pk>/delete/", views.interview_delete, name="delete"),
]
