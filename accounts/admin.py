from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
        "is_email_verified",
        "is_active",
        "last_login",
        "date_joined",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
    )

    list_filter = (
        "is_email_verified",
        "is_active",
        "is_staff",
        "date_joined",
    )

    ordering = ("email",)