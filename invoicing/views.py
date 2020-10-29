from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django_filters.views import object_filter
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from users.mixins import PermissionsHandlerMixin

"""This file contains the abstract views for Invoicing"""


class InvoiceListView(PermissionsHandlerMixin, ListView):
    model = None
    filterset_class = None
    paginate_by = 25

    def __init__(self):
        self.permissions_required = [self.__class__.__name__ ]
        if self.__class__.__name__ == 'SalesInvoiceListView':
            self.permissions_required = ['sales_permissions']
        if self.__class__.__name__ == 'PurchaseInvoiceListView':
            self.permissions_required = ['purchase_permissions']
        
        self.permissions_level = [1]

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = self.filterset_class(
            self.request.GET, queryset=queryset)

        return self.filterset.qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = self.filterset
        return context


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = None

    def form_valid(self, form):
        form.instance.organization = self.request.user.info.organization
        return super().form_valid(form)


class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = None

    def form_valid(self, form):
        form.instance.organization = self.request.user.info.organization
        return super().form_valid(form)

    def test_func(self):
        invoice = self.get_object()
        # Don't let the user edit if invoice is finalized
        return invoice.organization == self.request.user.info.organization and not invoice.finalized


class InvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = None

    def post(self, request, pk, *args, **kwargs):
        #Set invoice as finalized
        invoice = self.get_object()
        #Reduce inventory
        invoice.finalize(action=self.finalize_action)
        return redirect(self.invoice_finalize_redirect_name, pk=pk)

    def test_func(self):
        invoice = self.get_object()
        return invoice.organization == self.request.user.info.organization


class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = None

    def test_func(self):
        invoice = self.get_object()
        # Don't let the user edit if invoice is finalized
        return invoice.organization == self.request.user.info.organization


class InvoiceEntryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = None
    parent_model = None

    def form_valid(self, form):
        self.invoice = get_object_or_404(
            self.parent_model, pk=self.kwargs.get('pk'))
        form.instance.invoice = self.invoice
        return super().form_valid(form)

    def get_success_url(self):
        return self.invoice.get_absolute_url()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['pk'] = self.invoice.pk
        context['added_entries'] = self.invoice.entries.all()
        return context

    def test_func(self):
        self.invoice = get_object_or_404(
            self.parent_model, pk=self.kwargs.get("pk"))
        # Don't let the user edit if invoice is finalized
        return self.invoice.organization == self.request.user.info.organization and not self.invoice.finalized


class InvoiceEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = None
    parent_model = None

    def get_success_url(self):
        return self.invoice.get_absolute_url()

    def test_func(self):
        self.invoice = self.get_object().invoice
        # Don't let the user edit if invoice is finalized
        return self.invoice.organization == self.request.user.info.organization and not self.invoice.finalized
