from django.contrib import admin
from .models import UserInfo, Permissions
# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization')
admin.site.register(UserInfo, UserInfoAdmin)

admin.site.register(Permissions)