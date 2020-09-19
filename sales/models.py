from django.db import models
from products.models import Product
from organization.models import Organization

# Create your models here.
class Invoice(models.Model):

    date = models.DateField()
    customer_name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invoices')
    
class InvoiceEntry(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_invoices')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Invoice Entries"