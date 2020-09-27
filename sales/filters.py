from .models import SalesInvoice
import django_filters


class SalesInvoiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={
        'type': 'date'
    }))

    class Meta:
        model = SalesInvoice
        fields = ['name', 'date']
