from django.urls import path
from .views import register, user_login, user_logout, settings_page

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("settings/", settings_page, name="settings"),
]