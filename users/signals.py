from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserInfo

@receiver(post_save, sender=User)
def user_save(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
