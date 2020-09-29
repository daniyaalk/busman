from .models import PurchaseInvoice as Purchase
from invoicing.filters import InvoiceFilter

class PurchaseInvoiceFilter(InvoiceFilter):
    class Meta(InvoiceFilter.Meta):
        model = Purchase
