from django.db import models
from decimal import Decimal
from django.urls import reverse_lazy
from organization.models import Organization
from products.models import Product

# Create your models here.
class Purchase(models.Model):
    
    date = models.DateField()
    vendor_name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse_lazy('purchase-view', args=[self.pk])

    @property
    def net_total(self):
        total = Decimal(0)
        for entry in self.entries.all().values('quantity', 'price'):
            total += entry['quantity']*entry['price']
        return total



class PurchaseEntry(models.Model):
    
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='entries')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='in_purhcases')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Purchase Entries'

    @property
    def total_price(self):
        return self.price * self.quantity
