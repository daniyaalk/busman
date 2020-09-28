from django.contrib import admin
from .models import PurchaseInvoice, PurchaseInvoiceEntry

# Register your models here.
admin.site.register(PurchaseInvoice)
admin.site.register(PurchaseInvoiceEntry)
