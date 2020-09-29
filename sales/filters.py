from .models import SalesInvoice
from invoicing.filters import InvoiceFilter


class SalesInvoiceFilter(InvoiceFilter):
    class Meta(InvoiceFilter.Meta):
        model = SalesInvoice
