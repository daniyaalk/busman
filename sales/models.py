import decimal
from django.db import models
from django.urls import reverse
from products.models import Product
from organization.models import Organization

# Create your models here.
class Invoice(models.Model):

    date = models.DateField()
    customer_name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invoices')
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('sales-view', args=[self.pk])

    @property
    def gross_total(self):

        total = decimal.Decimal(0)
        for entry in self.entries.all():
            total += entry.total_price
        return total
    
    @property
    def net_total(self):
        return self.gross_total*(1-(self.discount/100))

    
class InvoiceEntry(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='entries')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='in_invoices')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name_plural = "Invoice Entries"
