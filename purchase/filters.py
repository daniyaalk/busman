from .models import Purchase
import django_filters

class PurchaseFilter(django_filters.FilterSet):
    vendor_name = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={
        'type': 'date'
    }))

    class Meta:
        model = Purchase
        fields = ['vendor_name', 'date']