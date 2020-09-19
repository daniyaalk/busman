from django.contrib import admin
from .models import Invoice, InvoiceEntry

# Register your models here.
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('organization', 'date')
    list_filter = ('organization',)
    sortable_by = ('date',)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceEntry)
