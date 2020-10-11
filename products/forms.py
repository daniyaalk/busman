from django import forms
from django.utils import timezone
from .models import Product
import pandas as pd
   
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['brand', 'name', 'sale_price', 'minimum_price', 'stock', 'unit', 'category']
        labels = {
            'sale_price': 'MRP',
            'unit': 'Price Unit'
        }

# Bulk add forms
class BulkAdd(forms.Form):
    bulk_file = forms.FileField(required=True, allow_empty_file=False)
    brand_column = forms.CharField(required=False)
    name_column = forms.CharField(required=True)
    category_column = forms.CharField(required=False)
    sale_price_column = forms.CharField(required=True)
    minimum_price_column = forms.CharField(required=True)
    price_unit_column = forms.CharField(required=False)
    stock_column = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        excel_file = cleaned_data['bulk_file']
        self.bulk_data = pd.read_excel(excel_file)

        #Get fields list, then make sure those columns exist in the excel sheet
        form_fields_list = list(self.fields.keys())
        #Ignoring 0'th field because it is the file object
        for key in form_fields_list[1:]:
            if cleaned_data[key] not in self.bulk_data.keys():
                self.add_error(key, 'Column does not exist in the file')
