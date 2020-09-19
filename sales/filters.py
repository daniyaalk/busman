from .models import Invoice
import django_filters

class InvoiceFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(lookup_expr='icontains')

    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Invoice
        fields = ['customer_name', 'date']