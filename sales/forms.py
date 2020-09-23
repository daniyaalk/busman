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

    discount = forms.DecimalField(max_digits=12, decimal_places=2, initial=0)

    def save(self, *args, **kwargs):
        self.instance.price = self.instance.product.sale_price-self.cleaned_data["discount"]
        return super().save(*args, **kwargs)

    class Meta:
        model = InvoiceEntry
        exclude = ['invoice', 'price']
