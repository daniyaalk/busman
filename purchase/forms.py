from django import forms
from django.utils import timezone
from .models import Purchase

class PurchaseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date',
        'value': timezone.now().strftime("%Y-%m-%d")
    }))

    class Meta:
        model = Purchase
        exclude = ['organization']