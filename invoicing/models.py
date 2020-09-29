from django.db import models
from django.urls import reverse
from django.utils.html import format_html
import operator
from decimal import Decimal
from organization.models import Organization
from products.models import Product

# Create your models here.
"""Abstract models for invoicing(Purchase and Sales)"""


class Invoice(models.Model):

    name = models.CharField(max_length=255)  # Name of the vendor or customer
    date = models.DateField()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='%(class)s')

    class finalized(models.IntegerChoices):
        PENDING = 0
        FINALIZED = 1

    finalized = models.BooleanField(
        max_length=20, choices=finalized.choices, default=0)

    class Meta:
        abstract = True
        ordering = ["-id"]

    PURCHASE = operator.add
    SALE = operator.sub

    def finalize(self, action):
        if self.finalized == 0:
            for entry in self.entries.all():
                #Skip if the product has been deleted
                if entry.product:
                    entry.product.stock += action(0, entry.quantity)
                    entry.product.save()
                self.finalized = 1
                self.save()
            return True
        else:
            return False

    @property
    def gross_total(self):

        total = Decimal(0)
        for entry in self.entries.all():
            total += entry.total_price
        return total


class InvoiceEntry(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name='%(class)s')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        abstract = True

    @property
    def total_price(self):
        return self.price * self.quantity
