from django import forms
from django.utils import timezone
from .models import Product
   
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['brand', 'name', 'sale_price', 'minimum_price', 'stock', 'unit', 'category']
        labels = {
            'sale_price': 'MRP',
            'unit': 'Price Unit'
        }
