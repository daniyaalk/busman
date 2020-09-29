from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import PurchaseInvoice, PurchaseInvoiceEntry, PURCHASE
from .filters import PurchaseFilter
from .forms import PurchaseInvoiceForm

from products.abstract_views import (
    InvoiceCreateView,
    InvoiceDetailView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    InvoiceEntryCreateView,
    InvoiceEntryDeleteView)

# Create your views here.
@login_required
def purchaselist(request):
    organization = request.user.organization

    purchases = PurchaseInvoice.objects.filter(organization=organization).order_by("-id")
    purchasefilter = PurchaseFilter(request.GET, queryset=purchases)

    paginator = Paginator(purchasefilter.qs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {'filter': purchasefilter, 'page_obj': page_obj}
    return render(request, 'purchase/purchaseinvoice_list.html', context=context)

class PurchaseInvoiceCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

class PurchaseInvoiceDetailView(InvoiceDetailView):
    model = PurchaseInvoice
    finalize_action = PURCHASE
    invoice_finalize_redirect_name = 'purchase-view'

class PurchaseInvoiceUpdateView(InvoiceUpdateView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm

class PurchaseInvoiceDeleteView(InvoiceDeleteView):
    model = PurchaseInvoice
    success_url = reverse_lazy('purchase-list')


class PurchaseInvoiceEntryCreateView(InvoiceEntryCreateView):
    model = PurchaseInvoiceEntry
    parent_model = PurchaseInvoice
    fields = ['product', 'price', 'quantity']

class PurchaseInvoiceEntryDeleteView(InvoiceEntryDeleteView):
    model = PurchaseInvoiceEntry
