from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from organization.models import Organization
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, Category
from .forms import ProductForm

# Create your views here.
class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Products"
        return context

    def get_queryset(self):
        return Product.objects.filter(organization=self.request.user.organization)

def addProducts(request):

    organization = request.user.organization
    if request.method == "POST":
        form = ProductForm(request.POST, organization=organization)
        form.instance.organization = organization
        if form.is_valid():
            form.save()
            return redirect("products-add")
    else:
        form = ProductForm(organization=organization)
    
    recent = Product.objects.filter(organization=organization).order_by("-id")[:5]

    context = {
        'form': form,
        'title': 'Add Product',
        'recent': recent
    }
    return render(request, "products/product_form.html", context=context)

# class ProductCreateView(LoginRequiredMixin, CreateView):
#     model = Product
#     form_class = ProductForm
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["formset"] = ProductFormset()
#         return context
