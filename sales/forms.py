from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):

    date = forms.DateTimeField(widget=forms.TextInput(attrs={
        'type': 'date'
    }))

    class Meta:
        model = Invoice
        exclude = ['organization']
