import uuid

from django.conf import settings
from django.db import models


class Interview(models.Model):
    class InterviewType(models.TextChoices):
        ONLINE = "online", "Online"
        PHONE = "phone", "Phone"
        ONSITE = "onsite", "Onsite"

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="interviews",
    )

    round_name = models.CharField(max_length=100)

    scheduled_at = models.DateTimeField()

    interview_type = models.CharField(
        max_length=20,
        choices=InterviewType.choices,
        default=InterviewType.ONLINE,
    )

    meeting_link = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_at"]
        verbose_name = "Interview"
        verbose_name_plural = "Interviews"

    def __str__(self):
        return (
            f"{self.round_name} - "
            f"{self.application.job_title}"
        )
