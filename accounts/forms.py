from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User
from .models import UserPreferences

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "john@company.com",
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
                "autocomplete": "current-password",
            }
        ),
    )


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = [
            "timezone",
            "date_format",
            "default_interview_duration",
            "dashboard_start_page",
            "interview_reminders",
            "email_notifications",
            "application_updates",
        ]

        widgets = {
            "timezone": forms.Select(
                choices=[
                    ("Asia/Kolkata", "India — Asia/Kolkata"),
                    ("UTC", "UTC"),
                    ("America/New_York", "America/New_York"),
                    ("Europe/London", "Europe/London"),
                ]
            ),
            "default_interview_duration": forms.Select(
                choices=[
                    (15, "15 minutes"),
                    (30, "30 minutes"),
                    (45, "45 minutes"),
                    (60, "1 hour"),
                    (90, "1 hour 30 minutes"),
                ]
            ),
        }