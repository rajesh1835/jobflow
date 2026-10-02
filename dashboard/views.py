from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard/index.html")


# Not developed pages
@login_required
def under_development(request, page_title, icon="construction"):
    return render(
        request,
        "coming_soon.html",
        {
            "page_title": page_title,
            "icon": icon,
        },
    )


@login_required
def applications(request):
    return under_development(
        request,
        "Applications",
        "briefcase-business",
    )


@login_required
def companies(request):
    return under_development(
        request,
        "Companies",
        "building-2",
    )


@login_required
def interviews(request):
    return under_development(
        request,
        "Interviews",
        "calendar-days",
    )


@login_required
def analytics(request):
    return under_development(
        request,
        "Analytics",
        "chart-no-axes-combined",
    )