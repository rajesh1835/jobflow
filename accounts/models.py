from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True)
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    models = UserManager()
    
    def __str__(self):
        return self.email

    # Properties
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def initials(self):
        if self.first_name and self.last_name:
            return (
                f"{self.first_name[0]}{self.last_name[0]}"
            ).upper()

        if self.first_name:
            return self.first_name[:2].upper()

        if self.last_name:
            return self.last_name[:2].upper()

        return self.email[:2].upper()

    @property
    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url

        return None

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"


# User Preferences
class UserPreferences(models.Model):
    class DateFormat(models.TextChoices):
        DMY = "DD/MM/YYYY", "DD/MM/YYYY"
        MDY = "MM/DD/YYYY", "MM/DD/YYYY"
        YMD = "YYYY-MM-DD", "YYYY-MM-DD"

    class DashboardPage(models.TextChoices):
        DASHBOARD = "dashboard", "Dashboard"
        APPLICATIONS = "applications", "Applications"
        INTERVIEWS = "interviews", "Interviews"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preferences",
    )

    timezone = models.CharField(
        max_length=50,
        default="Asia/Kolkata",
    )

    date_format = models.CharField(
        max_length=20,
        choices=DateFormat.choices,
        default=DateFormat.DMY,
    )

    default_interview_duration = models.PositiveSmallIntegerField(
        default=30,
    )

    dashboard_start_page = models.CharField(
        max_length=20,
        choices=DashboardPage.choices,
        default=DashboardPage.DASHBOARD,
    )

    interview_reminders = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    application_updates = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user}"