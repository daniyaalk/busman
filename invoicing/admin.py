from django.contrib import admin
from .models import Invoice, InvoiceEntry

# Register your models here.
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'date', 'net_total')
    list_display_links = ('organization', 'name')
    list_filter = ('organization',)
    sortable_by = ('date',)

class InvoiceEntryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'invoice')
    list_filter = ('invoice__organization',)
