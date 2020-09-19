from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from .models import Invoice
from .filters import InvoiceFilter
from .forms import InvoiceForm

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
