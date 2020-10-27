from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True)

    def has_organization(self):
        if self.organization == None:
            return False
        else:
            return True

    def __str__(self):
        return f"{self.user.username}"

class Permissions(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='permissions')

    dashboard_choices = [
        (0, 'Restrict'),
        (1, 'Allow')
    ]
    editables_choices = [
        (0, 'None'),
        (1, 'View'),
        (2, 'View, Create, Modify'),
        (3, 'View, Create, Modify, Delete'),
    ]
    dashboard_permissions = models.SmallIntegerField(
        choices=dashboard_choices, default=0)
    product_permissions = models.SmallIntegerField(
        choices=editables_choices, default=0)
    sales_permissions = models.SmallIntegerField(
        choices=editables_choices, default=0)
    purchase_permissions = models.SmallIntegerField(
        choices=editables_choices, default=0)
