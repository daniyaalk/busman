from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
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

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.get_absolute_url()

class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm

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

class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('sales-list')

    def test_func(self):
        invoice = self.get_object()
        return invoice.organization == self.request.user.organization

class EntryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = InvoiceEntry
    form_class = InvoiceEntryForm
    
    def form_valid(self, form):
        self.invoice = get_object_or_404(
            Invoice, pk=self.kwargs.get('pk'))
        form.instance.invoice = self.invoice
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('sales-entry-add', args=[self.invoice.pk])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['pk'] = self.invoice.pk
        context['added_entries'] = self.invoice.entries.all()
        return context
    
    def test_func(self):
        self.invoice = get_object_or_404(Invoice, pk=self.kwargs.get("pk"))
        return self.invoice.organization == self.request.user.organization
        
# class InvoiceEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

#     model = InvoiceEntry

#     def test_func(self):
#         self.invoice = self.get_object().invoice
#         return self.invoice.organization == self.request.user.organization
