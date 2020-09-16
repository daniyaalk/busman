from django.forms import ModelForm, ModelChoiceField
from .models import Product, Category

class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['brand', 'name', 'code', 'sale_price', 'stock', 'category']
    
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop("organization")
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(
            organization=self.organization)