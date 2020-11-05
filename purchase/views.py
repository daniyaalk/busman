from django.urls import reverse_lazy
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
    template_name = "purchase/purchaseinvoice_list.html"


class PurchaseInvoiceCreateView(InvoiceCreateView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm

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
