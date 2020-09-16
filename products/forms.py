from django.forms import ModelForm
from django.core.validators import ValidationError
from .models import Product, Category

def productform_factory(organization=None):
    
    class ProductForm(ModelForm):

        class Meta:
            model = Product
            fields = ['brand', 'name', 'code', 'sale_price', 'stock', 'category']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["category"].queryset = Category.objects.filter(
                organization=organization)
        
        def clean(self):
            cleaned_data = self.cleaned_data
            
            if Product.objects.filter(organization=organization, code=self.cleaned_data['code']).count() != 0:
                raise ValidationError({'code': 'A product with this code already exists!'})

            return super().clean()

    return ProductForm