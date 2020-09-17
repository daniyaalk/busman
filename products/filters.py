import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    price__gt = django_filters.NumberFilter(
        field_name='sale_price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(
        field_name='sale_price', lookup_expr='lt')

    brand = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'brand', 'price__lt', 'price__gt']
