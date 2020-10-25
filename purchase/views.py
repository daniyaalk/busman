from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import PurchaseInvoice, PurchaseInvoiceEntry, PURCHASE
from .filters import PurchaseInvoiceFilter
from .forms import PurchaseInvoiceForm

from invoicing.views import (
    InvoiceListView,
    InvoiceCreateView,
    InvoiceDetailView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    InvoiceEntryCreateView,
    InvoiceEntryDeleteView)

# Create your views here.
class PurchaseInvoiceListView(InvoiceListView):
    model = PurchaseInvoice
    filterset_class = PurchaseInvoiceFilter
    paginate_by = 25
    template_name = "purchase/purchaseinvoice_list.html"

class PurchaseInvoiceCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm

    def form_valid(self, form):
        form.instance.organization = self.request.user.info.organization
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
