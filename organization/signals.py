from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Organization

@receiver(post_save, sender=Organization)
def organization_saved(sender, instance, created, **kwargs):
    if created:
        user = instance.owner
        user.info.organization = instance
        user.info.save()
        