from django import forms
from django.utils import timezone
from .models import PurchaseInvoice

class PurchaseInvoiceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date',
        'value': timezone.now().strftime("%Y-%m-%d")
    }))

    class Meta:
        model = PurchaseInvoice
        exclude = ['organization', 'finalized']