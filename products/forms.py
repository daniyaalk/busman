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

"""Abstract form for Invoicing"""
class InvoiceForm(forms.ModelForm):

    date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date',
        'value': timezone.now().strftime("%Y-%m-%d")
    }))

    class Meta:
        exclude = ('organization', 'finalized')
