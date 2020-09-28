from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from organization.models import Organization
from .models import Product
from .forms import ProductForm
from .filters import ProductFilter

# Create your views here.

@login_required
def productlist(request):

    organization = request.user.organization
    products = Product.objects.filter(organization=organization).order_by("-id").annotate(earmarked=Sum(
        'salesinvoiceentry__quantity', filter=Q(salesinvoiceentry__invoice__finalized=0)))
    productfilter = ProductFilter(request.GET, queryset=products)

    paginator = Paginator(productfilter.qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filter': productfilter
    }

    return render(request, "products/product_list.html", context=context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    success_url = reverse_lazy('products-add')
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        organization = self.request.user.organization
        context = super().get_context_data(**kwargs)
        context['recent'] = Product.objects.filter(
            organization=organization).order_by("-id")[:5]
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.organization = self.request.user.organization
            return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products-list')

    def test_func(self):
        return self.request.user.organization == self.get_object().organization


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products-list')

    def test_func(self):
        return self.request.user.organization == self.get_object().organization

    def delete(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
                             "The product was deleted successfully")
        return super().delete(request, *args, **kwargs)
