from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from organization.models import Organization
from .models import Product
from .forms import productform_factory
from .filters import ProductFilter

# Create your views here.
class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self):
        context = super().get_context_data()
        productfilter = ProductFilter(
            self.request.GET, queryset=self.get_queryset())
        context["filter"] = productfilter
        objects = productfilter.qs
        
        paginate_by = 20
        paginator = Paginator(objects, paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context["is_paginated"] = objects.count() > paginate_by

        context["title"] = "Products"
        return context

    def get_queryset(self):
        return Product.objects.filter(organization=self.request.user.organization).order_by("-id")

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    success_url = reverse_lazy('products-add')
    form_class = productform_factory()
    
    def get_context_data(self, **kwargs):
        organization = self.request.user.organization
        context = super().get_context_data(**kwargs)
        context['recent'] = Product.objects.filter(organization=organization).order_by("-id")[:5]
        return context  

    def get(self, request):
        self.form_class = productform_factory(
            organization=request.user.organization)
        return super().get(request)
    
    def post(self, request):
        self.form_class = productform_factory(
            organization=request.user.organization)
        
        return super().post(request)

    def form_valid(self, form): 
        if form.is_valid():
            form.instance.organization = self.request.user.organization
            return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = productform_factory()
    success_url = reverse_lazy('products-list')

    def get(self, request, **kwargs):
        organization = self.request.user.organization
        self.form_class = productform_factory(organization=organization)
        return super().get(request)
    
    def post(self, request, **kwargs):
        organization = self.request.user.organization
        self.form_class = productform_factory(organization=organization)
        return super().post(request)
    
    def test_func(self):
        return self.request.user.organization == self.get_object().organization