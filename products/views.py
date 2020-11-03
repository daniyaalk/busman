from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.mixins import PermissionsHandlerMixin
from django.db.models import Q, Sum
from django.db import transaction, IntegrityError
from organization.models import Organization
from .models import Product
from .forms import ProductForm, BulkAdd
from .filters import ProductFilter
import pandas as pd

# Create your views here.

@login_required
def productlist(request):

    organization = request.user.info.organization
    
    if not hasattr(request.user, 'organization'):
        if not hasattr(request.user, 'permissions'):
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")    
        if request.user.permissions.product_permissions < 1:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")

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


class ProductCreateView(LoginRequiredMixin, PermissionsHandlerMixin, CreateView):
    permissions_required = ['product_permissions',]
    permissions_level =    [2]
    model = Product
    success_url = reverse_lazy('products-add')
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        organization = self.request.user.info.organization
        context = super().get_context_data(**kwargs)
        context['recent'] = Product.objects.filter(
            organization=organization).order_by("-id")[:5]
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.organization = self.request.user.info.organization
            return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, PermissionsHandlerMixin, UpdateView):
    permissions_required = ['product_permissions', ]
    permissions_level = [2]
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products-list')

    def test_func(self):
        return self.request.user.info.organization == self.get_object().organization


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, PermissionsHandlerMixin, DeleteView):
    permissions_required = ['product_permissions', ]
    permissions_level = [3]
    model = Product
    success_url = reverse_lazy('products-list')

    def test_func(self):
        return self.request.user.info.organization == self.get_object().organization

    def delete(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO,
                             "The product was deleted successfully")
        return super().delete(request, *args, **kwargs)


class ProductBulkAddView(LoginRequiredMixin, PermissionsHandlerMixin, FormView):
    permissions_required = ['product_permissions', ]
    permissions_level =    [2]
    form_class = BulkAdd
    template_name = 'products/product_bulk_form.html'
    success_url = reverse_lazy('products-list')
    
    def form_valid(self, form):

        model_equiv = {
            'brand': form.cleaned_data['brand_column'],
            'name': form.cleaned_data['name_column'],
            'sale_price': form.cleaned_data['sale_price_column'],
            'minimum_price': form.cleaned_data['minimum_price_column'],
            'unit': form.cleaned_data['price_unit_column'],
            'category': form.cleaned_data['category_column'],
            'stock': form.cleaned_data['stock_column'],
        }
        # for product in form.bulk_data[:10]:
        #     print(product)

        #Use django.db.trasaction.atomic() here
        # from django.db import transaction

        # try:
        #     with transaction.atomic():
        #         model1.save()
        #         model2.save()
        # except IntegrityError:
        #     handle_exception()
        
        exceptions = []
        try:
            with transaction.atomic():    
                for index, product in form.bulk_data.iterrows():
                    try:
                        Product(
                            brand=product[model_equiv['brand']],
                            name=product[model_equiv['name']],
                            sale_price=product[model_equiv['sale_price']],
                            minimum_price=product[model_equiv['minimum_price']],
                            unit=product[model_equiv['unit']],
                            category=product[model_equiv['category']],
                            stock=product[model_equiv['stock']],
                            organization=self.request.user.info.organization
                            
                        ).save()
                    except Exception as e:
                        exceptions({
                            'index': index,
                            'error': str(e)
                        })

                if len(exceptions) > 0:
                    raise("Error")

        except Exception as e:
            form.add_error(None, 'Please make sure all required fields are filled properly.')
            return super().form_invalid(form)
        
        return super().form_valid(form)
