from django.db import models
from django.core.exceptions import ValidationError
from organization.models import Organization

# Create your models here.
class Product(models.Model):
    brand = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    sale_price = models.DecimalField(decimal_places=2, max_digits=12)
    stock = models.DecimalField(decimal_places=2, max_digits=12)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='products')
    category = models.CharField(max_length=255, blank=True)

    class Meta:
        order_with_respect_to = 'organization'
        unique_together = [['organization','code']]

    def __str__(self):
        return f"{self.brand} / {self.name} / Rs. {self.sale_price} / {self.stock} Remaining"


