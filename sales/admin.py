from django.contrib import admin
from .models import SalesInvoice, SalesInvoiceEntry

# Register your models here.


class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ('organization', 'date')
    list_filter = ('organization',)
    sortable_by = ('date',)


admin.site.register(SalesInvoice, SalesInvoiceAdmin)
admin.site.register(SalesInvoiceEntry)
