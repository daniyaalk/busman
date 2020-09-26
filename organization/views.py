from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.contrib.auth.decorators import login_required
from .decorators import user_has_organization
from .models import Organization

# Create your views here.
@login_required
@user_has_organization(True)
def dash(request):
    context = {
        'title': 'Dashboard',
        'organization': request.user.organization
    }

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
