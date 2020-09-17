from django.forms import ModelForm
from django.core.validators import ValidationError
from .models import Product

def productform_factory(organization=None):
    
    class ProductForm(ModelForm):

        class Meta:
            model = Product
            fields = ['brand', 'name', 'code', 'sale_price', 'stock', 'category']

        def clean(self):
            cleaned_data = self.cleaned_data
            # If the code has been changed, check for duplicates
            if "code" in self.changed_data:
                if Product.objects.filter(organization=organization, code=self.cleaned_data['code']).count() != 0:
                    raise ValidationError({'code': 'A product with this code already exists!'})

            return super().clean()

    return ProductForm