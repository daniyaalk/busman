from .models import PurchaseInvoice
from products.forms import InvoiceForm

class PurchaseInvoiceForm(InvoiceForm):
    class Meta(InvoiceForm.Meta):
        model = PurchaseInvoice