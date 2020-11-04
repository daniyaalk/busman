from django.contrib import messages
from django.db import transaction
from users.models import UserInfo, Permissions


def delete_member(request, user_id):

    try:
        with transaction.atomic():
            UserInfo.objects.filter(user=user_id).update(organization=None)
            Permissions.objects.filter(user=user_id).delete()
    except:
        messages.error(request, "There was an error removing the user, please try again later.")
    else:
        messages.success(request, "User was removed from your organization.")
