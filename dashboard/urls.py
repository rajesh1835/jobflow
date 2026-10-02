from django.urls import path
from .views import dashboard, applications, companies, interviews, analytics


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("applications/", applications, name="applications"),
    path("companies/", companies, name="companies"),
    path("interviews/", interviews, name="interviews"),
    path("analytics/", analytics, name="analytics"),
]