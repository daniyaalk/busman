from django.db import models
from django.urls import reverse
from invoicing.models import Invoice, InvoiceEntry

# Create your models here.
SALE = Invoice.SALE
class SalesInvoice(Invoice):

    discount = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, default=0)

    @property
    def net_total(self):
        return self.gross_total*(1-self.discount/100)
    
    def get_absolute_url(self):
        return reverse('sales-view', args=[self.pk])

    
class SalesInvoiceEntry(InvoiceEntry):

    invoice = models.ForeignKey(
        SalesInvoice, on_delete=models.CASCADE, related_name='entries')

    class Meta:
        verbose_name_plural = 'Sales Invoice Entries'
