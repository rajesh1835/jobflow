
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .forms import InterviewForm
from .models import Interview


def is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def serialize_interview(interview):
    """Return interview details for AJAX responses."""
    return {
        "id": str(interview.pk),
        "round_name": interview.round_name,
        "application_id": str(interview.application_id),
        "job_title": interview.application.job_title,
        "company_name": interview.application.company.name,
        "scheduled_at": interview.scheduled_at.isoformat(),
        "scheduled_date": timezone.localtime(
            interview.scheduled_at
        ).strftime("%d %b %Y"),
        "scheduled_time": timezone.localtime(
            interview.scheduled_at
        ).strftime("%I:%M %p"),
        "interview_type": interview.interview_type,
        "interview_type_display": interview.get_interview_type_display(),
        "meeting_link": interview.meeting_link,
        "status": interview.status,
        "status_display": interview.get_status_display(),
        "notes": interview.notes,
    }


def get_owned_interview(request, pk):
    """Return an interview only if it belongs to the logged-in user."""
    return get_object_or_404(
        Interview.objects.select_related(
            "application",
            "application__company",
        ),
        pk=pk,
        application__user=request.user,
    )


@login_required
def interview_list(request):
    interviews = (
        Interview.objects.filter(application__user=request.user)
        .select_related("application", "application__company")
    )

    context = {
        "interviews": interviews,
        "form": InterviewForm(user=request.user),
        "query": "",
        "selected_status": "",
        "status_choices": Interview.Status.choices,
        "upcoming_count": interviews.filter(
            status=Interview.Status.SCHEDULED,
            scheduled_at__gte=timezone.now(),
        ).count(),
        "completed_count": interviews.filter(
            status=Interview.Status.COMPLETED,
        ).count(),
        "cancelled_count": interviews.filter(
            status=Interview.Status.CANCELLED,
        ).count(),
    }

    return render(request, "interviews/interview_list.html", context)

@login_required
@require_POST
def interview_create(request):
    form = InterviewForm(request.POST, user=request.user)

    if form.is_valid():
        interview = form.save(commit=False)
        interview.save()

        if is_ajax(request):
            return JsonResponse(
                {
                    "success": True,
                    "message": "Interview scheduled successfully.",
                    "interview": serialize_interview(interview),
                },
                status=201,
            )

        messages.success(request, "Interview scheduled successfully.")
        return render(
            request,
            "interviews/interview_list.html",
            {
                "interviews": Interview.objects.filter(
                    application__user=request.user
                ).select_related("application", "application__company"),
                "status_choices": Interview.Status.choices,
            },
        )

    if is_ajax(request):
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )

    return render(
        request,
        "interviews/interview_list.html",
        {
            "interviews": Interview.objects.filter(
                application__user=request.user
            ).select_related("application", "application__company"),
            "form": form,
            "status_choices": Interview.Status.choices,
        },
        status=400,
    )


@login_required
@require_POST
def interview_update(request, pk):
    interview = get_owned_interview(request, pk)

    form = InterviewForm(
        request.POST,
        instance=interview,
        user=request.user,
    )

    if form.is_valid():
        interview = form.save()

        if is_ajax(request):
            return JsonResponse(
                {
                    "success": True,
                    "message": "Interview updated successfully.",
                    "interview": serialize_interview(interview),
                }
            )

        messages.success(request, "Interview updated successfully.")
        return JsonResponse(
            {"success": True, "redirect_url": "/jf/v1/interviews/"}
        )

    if is_ajax(request):
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )

    return JsonResponse(
        {
            "success": False,
            "errors": form.errors.get_json_data(),
        },
        status=400,
    )


@login_required
@require_GET
def interview_detail(request, pk):
    interview = get_owned_interview(request, pk)

    if is_ajax(request):
        return JsonResponse(
            {
                "success": True,
                "interview": serialize_interview(interview),
            }
        )

    return JsonResponse(
        {
            "success": True,
            "interview": serialize_interview(interview),
        }
    )


@login_required
@require_POST
def interview_delete(request, pk):
    interview = get_owned_interview(request, pk)

    interview.delete()

    if is_ajax(request):
        return JsonResponse(
            {
                "success": True,
                "message": "Interview deleted successfully.",
                "id": str(pk),
            }
        )

    messages.success(request, "Interview deleted successfully.")
    return JsonResponse(
        {"success": True, "redirect_url": "/jf/v1/interviews/"}
    )
