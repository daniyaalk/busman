from django import forms
from .models import Invoice, InvoiceEntry

class InvoiceForm(forms.ModelForm):

    date = forms.DateTimeField(widget=forms.TextInput(attrs={
        'type': 'date'
    }))

    class Meta:
        model = Invoice
        exclude = ['organization']

class InvoiceEntryForm(forms.ModelForm):

    class Meta:
        model = InvoiceEntry
        exclude = ['invoice']