from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserPreferences
from .forms import UserRegistrationForm, UserLoginForm, UserPreferencesForm


# User Registration
def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("dashboard")

    else:
        form = UserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


# User Login 
def user_login(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=email,
                password=password,
            )

            if user is not None:
                login(request, user)

                return redirect("dashboard")

    else:
        form = UserLoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )


# User Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect("home")


# User Preferences
@login_required
def settings_page(request):
    preferences, created = UserPreferences.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = UserPreferencesForm(
            request.POST,
            instance=preferences,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Your preferences have been saved.")
            return redirect("accounts:settings")
    else:
        form = UserPreferencesForm(instance=preferences)

    return render(
        request,
        "accounts/settings.html",
        {
            "form": form,
            "preferences": preferences,
        },
    )