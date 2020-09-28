from django.db import models
from decimal import Decimal
from django.urls import reverse_lazy
from organization.models import Organization
from products.models import Product, Invoice, InvoiceEntry

# Create your models here.
class PurchaseInvoice(Invoice):
    class Meta:
        verbose_name_plural = 'Purchase Invoices'
           
    def get_absolute_url(self):
        return reverse_lazy('purchase-view', args=[self.pk])

    @property
    def net_total(self):
        return self.gross_total # Net total and gross total are the same for purchase invoice



class PurchaseInvoiceEntry(InvoiceEntry):
    
    purchase = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='entries')

    class Meta:
        verbose_name_plural = 'Purchase Entries'
