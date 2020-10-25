from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Request(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='join_request')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='join_requests')

    def __str__(self):
        return f"{self.user} to {self.organization}"