from .models import PurchaseInvoice
from invoicing.forms import InvoiceForm

class PurchaseInvoiceForm(InvoiceForm):
    class Meta(InvoiceForm.Meta):
        model = PurchaseInvoice