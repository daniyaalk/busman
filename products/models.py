from django.db import models
from decimal import Decimal
from organization.models import Organization

# Create your models here.
class Product(models.Model):
    brand = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    sale_price = models.DecimalField(decimal_places=2, max_digits=12)
    minimum_price = models.DecimalField(decimal_places=2, max_digits=12)
    stock = models.DecimalField(decimal_places=2, max_digits=12)
    unit = models.CharField(max_length=50, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='products')
    category = models.CharField(max_length=255, blank=True)

    class Meta:
        order_with_respect_to = 'organization'

    def __str__(self):
        return f"{self.brand} / {self.name} / Rs. {self.minimum_price}-{self.sale_price} / {self.stock} Remaining"

"""Abstract models for invoicing(Purchase and Sales)"""
class Invoice(models.Model):

    name = models.CharField(max_length=255) # Name of the vendor or customer
    date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='%(class)s')

    class finalized(models.IntegerChoices):
        PENDING = 0
        FINALIZED = 1
    
    finalized = models.BooleanField(max_length=20, choices=finalized.choices, default=0)

    class Meta:
        abstract = True
        ordering = ["-id"]

    @property
    def gross_total(self):

        total = Decimal(0)
        for entry in self.entries.all():
            total += entry.total_price
        return total

class InvoiceEntry(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='%(class)s')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        abstract = True

    @property
    def total_price(self):
        return self.price * self.quantity
    


