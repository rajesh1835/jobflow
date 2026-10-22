from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from applications.models import Application
from companies.models import Company
from django.db.models import Q, Count

@login_required
def dashboard(request):
    user = request.user

    applications = (
        Application.objects.filter(user=user)
        .select_related("company")
        .order_by("-updated_at")
    )

    # Top statistics
    total_applications = applications.count()

    active_applications = applications.filter(
        status__in=[
            Application.Status.APPLIED,
            Application.Status.SCREENING,
            Application.Status.INTERVIEW,
        ]
    ).count()

    total_interviews = applications.filter(
        status=Application.Status.INTERVIEW
    ).count()

    total_offers = applications.filter(
        status=Application.Status.OFFER
    ).count()

    cards = {
        "total_applications": total_applications,
        "active_applications": active_applications,
        "total_interviews": total_interviews,
        "total_offers": total_offers,
    }

    # Application pipeline
    status_counts = {
        item["status"]: item["count"]
        for item in applications.values("status").annotate(
            count=Count("id")
        )
    }

    pipeline = {
        "applied": status_counts.get(Application.Status.APPLIED, 0),
        "screening": status_counts.get(Application.Status.SCREENING, 0),
        "interview": status_counts.get(Application.Status.INTERVIEW, 0),
        "offer": status_counts.get(Application.Status.OFFER, 0),
        "rejected": status_counts.get(Application.Status.REJECTED, 0),
    }

    # Recent applications
    recent_applications = applications[:5]

    context = {
        "cards": cards,
        "pipeline": pipeline,
        "recent_applications": recent_applications,
        "next_interview": None,
        "total_companies": Company.objects.filter(user=user).count(),
    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )


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