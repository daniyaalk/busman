from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django_filters.views import object_filter
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

"""This file contains the abstract views for Invoicing"""

class InvoiceCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

    def test_func(self):
        invoice = self.get_object()
        # Don't let the user edit if invoice is finalized
        return invoice.organization == self.request.user.organization and not invoice.finalized

class InvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    def post(self, request, pk, *args, **kwargs):
        #Set invoice as finalized
        invoice = self.get_object()
        #Reduce inventory
        invoice.finalize(action=self.finalize_action)
        return redirect(self.invoice_finalize_redirect_name, pk=pk)

    def test_func(self):
        invoice = self.get_object()
        return invoice.organization == self.request.user.organization

class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    def test_func(self):
        invoice = self.get_object()
        # Don't let the user edit if invoice is finalized
        return invoice.organization == self.request.user.organization


class InvoiceEntryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

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
        return self.invoice.organization == self.request.user.organization and not self.invoice.finalized

class InvoiceEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    def get_success_url(self):
        return self.invoice.get_absolute_url()

    def test_func(self):
        self.invoice = self.get_object().invoice
        # Don't let the user edit if invoice is finalized
        return self.invoice.organization == self.request.user.organization and not self.invoice.finalized
