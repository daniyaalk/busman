from django.contrib import admin
from .models import Organization, Request
# Register your models here.

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Request)
