from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum, F
from .decorators import user_has_organization
from .models import Organization, Request
from .forms import OrganizationJoinRequestForm

# Create your views here.
@login_required
@user_has_organization(True)
def dash(request):

    organization = request.user.organization
    
    context = {
        'title': 'Dashboard',
        'organization': organization,
    }

    this_month = datetime.today().date().replace(day=1)
    invoices_this_month = organization.salesinvoice.filter(
        date__gte=this_month, finalized=True)
    context["sale_this_month"] = invoices_this_month.aggregate(sum=Sum(F('entries__price')*F('entries__quantity')))['sum']

    return render(request, "organization/dash.html", context=context)

@login_required
@user_has_organization(False)
def noOrgView(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, "organization/no_org.html", context=context)


class OrganizationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Organization
    fields = ['name']
    success_url = reverse_lazy("org-none")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return not self.request.user.info.has_organization()

def organization_settings(request):
    pass

@login_required
@user_has_organization(False)
def join_organization(request):
    return render(request, "organization/join.html")

class OrganizationRequestFormView(FormView):
    form_class = OrganizationJoinRequestForm
    template_name = "organization/join.html"
    success_url = reverse_lazy('org-join')

    def form_valid(self, form):
        organization = Organization.objects.get(pk=form.cleaned_data["id"])
        obj, created = Request.objects.update_or_create(user=self.request.user, organization=organization)

        messages.success(self.request, 'Your request was sent successfully.')
        return super().form_valid(form)
