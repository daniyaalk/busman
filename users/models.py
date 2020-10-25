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