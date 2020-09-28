from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import SalesInvoice, SalesInvoiceEntry
from .filters import SalesInvoiceFilter
from .forms import SalesInvoiceForm, SalesInvoiceEntryForm

from products.abstract_views import (
    InvoiceCreateView, 
    InvoiceDetailView, 
    InvoiceUpdateView, 
    InvoiceDeleteView,
    InvoiceEntryCreateView,
    InvoiceEntryDeleteView)

# Create your views here.
@login_required
def invoicelist(request):
    organization = request.user.organization
    invoice_list = SalesInvoice.objects.filter(organization=organization).order_by("-id")
    invoicefilter = SalesInvoiceFilter(request.GET, queryset=invoice_list)

    paginator = Paginator(invoicefilter.qs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {'filter': invoicefilter, 'page_obj': page_obj}

    return render(request, "sales/salesinvoice_list.html", context=context)


class SalesInvoiceCreateView(InvoiceCreateView):
    model = SalesInvoice
    form_class = SalesInvoiceForm

class SalesInvoiceUpdateView(InvoiceUpdateView):
    model = SalesInvoice
    form_class = SalesInvoiceForm
   
class SalesInvoiceDetailView(InvoiceDetailView):
    model = SalesInvoice
    invoice_finalize_redirect_name = 'sales-view'

class SalesInvoiceDeleteView(InvoiceDeleteView):
    model = SalesInvoice
    success_url = reverse_lazy('sales-list')

class SalesInvoiceEntryCreateView(InvoiceEntryCreateView):
    model = SalesInvoiceEntry
    parent_model = SalesInvoice
    form_class = SalesInvoiceEntryForm
        

class SalesInvoiceEntryDeleteView(InvoiceEntryDeleteView):
    model = SalesInvoiceEntry
