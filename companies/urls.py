
from django.urls import path

from .views import company_list, company_create, company_delete, company_detail, company_update

app_name = "companies"

urlpatterns = [
    path("", company_list, name="list"),
    path("create/", company_create, name="create"),
    path("<uuid:pk>/", company_detail, name="detail"),
    path("<uuid:pk>/edit/", company_update, name="update"),
    path("<uuid:pk>/delete/", company_delete, name="delete"),
]
