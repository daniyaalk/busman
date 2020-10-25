from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseNotAllowed
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
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

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'organization/organization_edit.html'
    fields = ['name']
    success_url = reverse_lazy('org-settings')
    def get_object(self, queryset=None):
        return self.request.user.organization

class OrganizationRequestFormView(FormView):
    form_class = OrganizationJoinRequestForm
    template_name = "organization/join.html"
    success_url = reverse_lazy('org-join')

    def form_valid(self, form):
        organization = Organization.objects.get(pk=form.cleaned_data["id"])
        obj, created = Request.objects.update_or_create(user=self.request.user, organization=organization)

        messages.success(self.request, 'Your request was sent successfully.')
        return super().form_valid(form)

class OrganizationRequestListView(ListView):
    model = Request
    template_name = 'organization/requests.html'

    def get_object(self):
        return self.request.user.organization.join_requests

@login_required
@csrf_protect
def request_action(request):

    # request = HTTP Request
    # join_request = Join Request (.models.Request)
    #

    if request.method == 'POST':
        join_request = Request.objects.get(pk=request.POST['id'])
        
        if join_request.organization == request.user.organization:
            
            try:
                if request.POST['action'] == 'Accept':
                    join_request.user.info.organization=join_request.organization
                    join_request.user.info.save()
            except Exception as e:
                print(e)
                messages.error(request, "There was an error, please try again later.")
            else:
                join_request.delete()
            
            return redirect('org-requests')

        else:
            return HttpResponseNotAllowed
