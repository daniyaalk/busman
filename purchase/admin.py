from django.contrib import admin
from .models import Purchase, PurchaseEntry

# Register your models here.
admin.site.register(Purchase)
admin.site.register(PurchaseEntry)
