from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login


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
