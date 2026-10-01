from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, authenticate


# User Registration
def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("home")

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
        return redirect("home")

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

                return redirect("home")

    else:
        form = UserLoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )


# User Logout
def user_logout(request):
    pass