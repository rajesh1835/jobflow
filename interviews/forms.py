
from django import forms

from applications.models import Application
from .models import Interview


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            "application",
            "round_name",
            "scheduled_at",
            "interview_type",
            "meeting_link",
            "notes",
        ]

        widgets = {
            "scheduled_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["application"].queryset = (
                Application.objects.filter(user=user)
                .select_related("company")
                .order_by("company__name", "job_title")
            )
        else:
            self.fields["application"].queryset = Application.objects.none()

        self.fields["scheduled_at"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]
