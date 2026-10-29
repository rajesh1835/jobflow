from django.urls import path
from .views import dashboard, interviews, analytics


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("interviews/", interviews, name="interviews"),
    path("analytics/", analytics, name="analytics"),
]