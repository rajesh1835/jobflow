from django.contrib import admin
from .models import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        "round_name",
        "application",
        "scheduled_at",
        "interview_type",
        "status",
    )

    list_filter = (
        "status",
        "interview_type",
        "scheduled_at",
    )

    search_fields = (
        "round_name",
        "application__job_title",
        "application__company__name",
    )

    readonly_fields = ("id", "created_at", "updated_at")
