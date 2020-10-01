from django.contrib import admin
from invoicing.admin import InvoiceAdmin, InvoiceEntryAdmin
from .models import SalesInvoice, SalesInvoiceEntry

admin.site.register(SalesInvoice, InvoiceAdmin)
admin.site.register(SalesInvoiceEntry, InvoiceEntryAdmin)
