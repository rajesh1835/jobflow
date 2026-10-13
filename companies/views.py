from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CompanyForm
from .models import Company


@login_required
def company_list(request):
    """List the signed-in user's companies and handle create/edit modal posts."""
    user_companies = Company.objects.filter(user=request.user)
    query = request.GET.get("q", "").strip()
    companies = user_companies
    if query:
        companies = companies.filter(name__icontains=query)

    editing_company = None
    modal_open = request.GET.get("modal") == "create"
    if request.GET.get("edit"):
        editing_company = get_object_or_404(
            Company, pk=request.GET["edit"], user=request.user
        )
        modal_open = True

    if request.method == "POST":
        company_id = request.POST.get("company_id", "").strip()
        if company_id:
            editing_company = get_object_or_404(
                Company, pk=company_id, user=request.user
            )
        form = CompanyForm(
            request.POST,
            instance=editing_company,
            user=request.user,
        )
        modal_open = True
        if form.is_valid():
            company = form.save(commit=False)
            if editing_company is None:
                company.user = request.user
            company.save()
            messages.success(
                request,
                "Company updated successfully." if editing_company else "Company added successfully.",
            )
            return redirect("companies:list")
    else:
        form = CompanyForm(instance=editing_company, user=request.user)

    return render(
        request,
        "companies/company_list.html",
        {
            "companies": companies,
            "query": query,
            "company_form": form,
            "editing_company": editing_company,
            "modal_open": modal_open,
        },
    )


@login_required
def company_create(request):
    # Keep the existing route working; the form now lives in the list modal.
    return redirect("companies:list")


@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, user=request.user)
    return render(request, "companies/company_detail.html", {"company": company})


@login_required
def company_update(request, pk):
    # Existing edit links/deep links open the edit modal on the listing page.
    company = get_object_or_404(Company, pk=pk, user=request.user)
    return redirect(f"/jf/v1/companies/?edit={company.pk}")


@login_required
@require_POST
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk, user=request.user)
    company.delete()
    messages.success(request, "Company deleted successfully.")
    return redirect("companies:list")
