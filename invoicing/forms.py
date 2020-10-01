from django import forms
from django.utils import timezone
from products.models import Product

"""Abstract form for Invoicing"""
class InvoiceForm(forms.ModelForm):

    date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date',
        'value': timezone.now().strftime("%Y-%m-%d")
    }))

    class Meta:
        exclude = ('organization', 'finalized')
