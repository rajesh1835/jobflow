from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ApplicationForm
from .models import Application


@login_required
def application_list(request):
    query = request.GET.get("q", "").strip()

    applications = (
        Application.objects.filter(user=request.user)
        .select_related("company")
        .order_by("-updated_at")
    )

    if query:
        applications = applications.filter(
            Q(job_title__icontains=query)
            | Q(company__name__icontains=query)
        )

    editing_application = None

    if request.method == "POST":
        application_id = request.POST.get("application_id")

        if application_id:
            editing_application = get_object_or_404(
                Application,
                pk=application_id,
                user=request.user,
            )

        form = ApplicationForm(
            request.POST,
            instance=editing_application,
            user=request.user
        )


        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()

            if editing_application:
                messages.success(request, "Application updated successfully.")
            else:
                messages.success(request, "Application created successfully.")

            return redirect("applications:list")

        # Reopen modal with validation errors.
        modal_open = True

    else:
        edit_id = request.GET.get("edit")

        if edit_id:
            editing_application = get_object_or_404(
                Application,
                pk=edit_id,
                user=request.user,
            )

        form = ApplicationForm(
            instance=editing_application,
            user=request.user,
        )

        modal_open = bool(editing_application)

    return render(
        request,
        "applications/application_list.html",
        {
            "applications": applications,
            "query": query,
            "application_form": form,
            "editing_application": editing_application,
            "modal_open": modal_open,
        },
    )


@login_required
@require_POST
def application_delete(request, pk):
    application = get_object_or_404(
        Application,
        pk=pk,
        user=request.user,
    )

    application.delete()

    messages.success(request, "Application deleted successfully.")

    return redirect("applications:list")