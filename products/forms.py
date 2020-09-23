from django import forms
from django.core.validators import ValidationError
from .models import Product
   
class ProductForm(forms.ModelForm):

    unit = forms.CharField(label="Sale price unit:")

    class Meta:
        model = Product
        fields = ['brand', 'name', 'sale_price', 'stock', 'unit', 'category']