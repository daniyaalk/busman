from django.db import models
from django.core.exceptions import ValidationError
from organization.models import Organization

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        order_with_respect_to = 'organization'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    sale_price = models.DecimalField(decimal_places=2, max_digits=12)
    stock = models.DecimalField(decimal_places=2, max_digits=12)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='producs', null=True, blank=True)

    class Meta:
        order_with_respect_to = 'organization'
        unique_together = [['organization','code']]


