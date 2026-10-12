
from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "website",
            "industry",
            "location",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "e.g. Google",
            }),
            "website": forms.URLInput(attrs={
                "placeholder": "https://example.com",
            }),
            "industry": forms.TextInput(attrs={
                "placeholder": "e.g. Software Development",
            }),
            "location": forms.TextInput(attrs={
                "placeholder": "e.g. Bengaluru, India",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Add notes about the company...",
                "rows": 4,
            }),
        }

    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full rounded-xl border border-slate-200 "
                "bg-white px-3.5 py-2.5 text-sm text-slate-800 "
                "outline-none transition "
                "focus:border-slate-400 focus:ring-2 focus:ring-slate-100"
            )

        self.fields["description"].widget.attrs["rows"] = 4


    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not self.user:
            raise forms.ValidationError(
                "Unable to validate the company owner."
            )

        existing_company = Company.objects.filter(
            user=self.user,
            name__iexact=name,
        )

        if self.instance.pk:
            existing_company = existing_company.exclude(
                pk=self.instance.pk
            )

        if existing_company.exists():
            raise forms.ValidationError(
                "You have already added this company."
            )

        return name

    