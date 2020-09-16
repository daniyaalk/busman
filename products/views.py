from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from organization.models import Organization
from .models import Product
from .forms import productform_factory

# Create your views here.
class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Products"
        return context

    def get_queryset(self):
        return Product.objects.filter(organization=self.request.user.organization)

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
