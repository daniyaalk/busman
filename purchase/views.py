from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import PurchaseInvoice, PurchaseInvoiceEntry
from .filters import PurchaseFilter
from .forms import PurchaseInvoiceForm

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

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

class PurchaseDetailView(LoginRequiredMixin, UserPassesTestMixin,DetailView):
    model = PurchaseInvoice

    def post(self, request, pk, *args, **kwargs):
        #Set invoice as finalized
        invoice = self.get_object()
        #Reduce inventory
        invoice.finalize(action=invoice.PURCHASE)
        return redirect("purchase-view", pk=pk)

    def test_func(self):
        invoice = self.get_object()
        return invoice.organization == self.request.user.organization

class PurchaseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm

    def test_func(self):
        invoice = self.get_object()
        return invoice.organization == self.request.user.organization and not invoice.finalized

class PurchaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PurchaseInvoice
    success_url = reverse_lazy('purchase-list')

    def test_func(self):
        invoice = self.get_object()
        return invoice.organization == self.request.user.organization

class PurchaseEntryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PurchaseInvoiceEntry
    fields = ['product', 'price', 'quantity']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['pk'] = self.purchase.pk
        context['added_entries'] = self.purchase.entries.all().order_by("-id")
        return context

    def form_valid(self, form):
        self.purchase = get_object_or_404(
            PurchaseInvoice, pk=self.kwargs.get('pk'))
        form.instance.purchase = self.purchase
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('purchase-entry-add', args=[self.purchase.pk])

    def test_func(self):
        self.purchase = get_object_or_404(
            PurchaseInvoice, pk=self.kwargs['pk'])
        return self.purchase.organization == self.request.user.organization


class PurchaseEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = PurchaseInvoiceEntry

    def get_success_url(self):
        return self.purchase.get_absolute_url()

    def test_func(self):
        self.purchase = self.get_object().purchase
        # Don't let the user edit if invoice is finalized
        return self.purchase.organization == self.request.user.organization
