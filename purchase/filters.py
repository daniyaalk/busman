from .models import PurchaseInvoice as Purchase
import django_filters

class PurchaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={
        'type': 'date'
    }))

    class Meta:
        model = Purchase
        fields = ['name', 'date']