from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "company",
        "user",
        "status",
        "applied_date",
    )

    list_filter = ("status", "applied_date")
    search_fields = ("job_title", "company__name", "user__email")
    ordering = ("-created_at",)