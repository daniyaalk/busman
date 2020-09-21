from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from products.models import Product
from .models import Invoice, InvoiceEntry
from .filters import InvoiceFilter
from .forms import InvoiceForm, InvoiceEntryForm

# Create your views here.
@login_required
def invoicelist(request):
    organization = request.user.organization
    invoice_list = Invoice.objects.filter(organization=organization).order_by("-id")
    invoicefilter = InvoiceFilter(request.GET, queryset=invoice_list)

    paginator = Paginator(invoicefilter.qs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {'filter': invoicefilter, 'page_obj': page_obj}

    return render(request, "sales/invoice_list.html", context=context)


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy('sales-list')

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    success_url = reverse_lazy('sales-list')

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)
    
    def test_func(self):
        invoice = self.get_object()
        return invoice.organization == self.request.user.organization

class InvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Invoice

    def test_func(self):
        invoice = self.get_object()
        return invoice.organization == self.request.user.organization

@login_required
def addentries(request, pk):
    
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.user.organization != invoice.organization:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        form = InvoiceEntryForm(request.POST)
        form.instance.invoice = invoice
        
        if form.is_valid():
            form.save()
            return redirect('sales-add', pk)
    else:
        form = InvoiceEntryForm()

    form.fields["product"].queryset = Product.objects.filter(organization=request.user.organization)

    added_entries = InvoiceEntry.objects.filter(invoice__pk=pk)
    context = {
        'pk': pk,
        'form': form,
        'added_entries': added_entries
    }
    return render(request, "sales/add_entries.html", context=context)
