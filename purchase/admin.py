from django.contrib import admin
from invoicing.admin import InvoiceAdmin, InvoiceEntryAdmin
from .models import PurchaseInvoice, PurchaseInvoiceEntry

# Register your models here.
admin.site.register(PurchaseInvoice, InvoiceAdmin)
admin.site.register(PurchaseInvoiceEntry, InvoiceEntryAdmin)
