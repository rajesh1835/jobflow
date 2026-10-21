from django import forms

from companies.models import Company
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "company",
            "job_title",
            "job_url",
            "location",
            "status",
            "applied_date",
            "notes",
        ]

        widgets = {
            "company": forms.Select(
                attrs={
                }
            ),
            "job_title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Python Developer",
                }
            ),
            "job_url": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Bengaluru",
                }
            ),
            "applied_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Add notes about this application...",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["company"].queryset = Company.objects.filter(
            user=user
        ).order_by("name")

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": (
                        "w-full rounded-lg border border-gray-300 "
                        "px-3 py-2 text-sm focus:border-red-500 "
                        "focus:outline-none focus:ring-1 "
                        "focus:ring-red-500"
                    )
                }
            )
