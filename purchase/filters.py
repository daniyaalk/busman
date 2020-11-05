from .models import PurchaseInvoice
from invoicing.filters import InvoiceFilter

class PurchaseInvoiceFilter(InvoiceFilter):
    class Meta(InvoiceFilter.Meta):
        model = PurchaseInvoice
